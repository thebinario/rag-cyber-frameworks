from __future__ import annotations

import hmac
import json
import sys
import threading
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .analyzer import (
    analyze_scenario,
    build_analysis_client,
    weak_match_warning,
)
from .store import DEFAULT_WRITEUPS_TOP_K, build_embedding_client


MAX_BODY_BYTES = 64 * 1024
MAX_TOP_K = 10
MAX_SCENARIO_CHARACTERS = 8000
MAX_LIST_ITEMS = 50
LOOPBACK_HOSTS = ("127.0.0.1", "localhost", "::1")

AnalyzeFunction = Callable[[str, int], dict[str, Any]]


class RequestError(Exception):
    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


def _string_list(payload: dict[str, Any], key: str) -> list[str]:
    value = payload.get(key)
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list) or not all(isinstance(item, (str, int, float)) for item in value):
        raise RequestError(400, f"'{key}' must be a list of strings")
    return [str(item).strip() for item in value[:MAX_LIST_ITEMS] if str(item).strip()]


def build_scenario(payload: dict[str, Any]) -> str:
    """Build the scenario text from either a free-form 'scenario' or structured recon fields."""
    free_text = payload.get("scenario")
    if free_text is not None and not isinstance(free_text, str):
        raise RequestError(400, "'scenario' must be a string")

    parts: list[str] = []
    if free_text and free_text.strip():
        parts.append(free_text.strip())

    host = payload.get("host")
    if isinstance(host, str) and host.strip():
        parts.append(f"Host: {host.strip()}")

    for label, key in (
        ("Technology stack", "stack"),
        ("Endpoints", "endpoints"),
        ("Findings / observed behavior", "findings"),
    ):
        items = _string_list(payload, key)
        if items:
            parts.append(f"{label}: " + "; ".join(items))

    notes = payload.get("notes")
    if isinstance(notes, str) and notes.strip():
        parts.append(f"Notes: {notes.strip()}")

    scenario = "\n".join(parts)
    if not scenario.strip():
        raise RequestError(400, "provide 'scenario' or at least one of: stack, endpoints, findings, notes")
    if len(scenario) > MAX_SCENARIO_CHARACTERS:
        raise RequestError(400, f"scenario is longer than {MAX_SCENARIO_CHARACTERS} characters")
    return scenario


def parse_top_k(payload: dict[str, Any]) -> int:
    value = payload.get("top_k", DEFAULT_WRITEUPS_TOP_K)
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= MAX_TOP_K:
        raise RequestError(400, f"'top_k' must be an integer between 1 and {MAX_TOP_K}")
    return value


def build_default_analyze_function(persist_directory: str | Path) -> AnalyzeFunction:
    embed_client = build_embedding_client()
    generation_client = build_analysis_client()
    lock = threading.Lock()  # one local GPU: run one analysis at a time

    def analyze(scenario: str, top_k: int) -> dict[str, Any]:
        with lock:
            analysis = analyze_scenario(
                scenario,
                embed_client,
                generation_client,
                persist_directory=persist_directory,
                top_k=top_k,
            )
        matches = list(zip(analysis.reports, analysis.distances))
        return {
            "scenario": analysis.scenario,
            "answer": analysis.answer,
            "weak_match": bool(weak_match_warning(matches)),
            "reports": [
                {
                    "title": report.get("title"),
                    "vuln_class": report.get("vuln_class"),
                    "severity": report.get("severity"),
                    "source_path": report.get("source_path"),
                    "distance": round(distance, 4),
                }
                for report, distance in matches
            ],
        }

    return analyze


def make_handler(analyze: AnalyzeFunction, token: str | None = None) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        server_version = "WriteupsAPI/1"

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002 - stdlib signature
            sys.stderr.write(f"[api] {self.address_string()} {format % args}\n")

        def _send_json(self, status: int, body: dict[str, Any]) -> None:
            raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(raw)

        def _check_token(self) -> None:
            if not token:
                return
            supplied = self.headers.get("Authorization", "")
            expected = f"Bearer {token}"
            if not hmac.compare_digest(supplied.encode("utf-8"), expected.encode("utf-8")):
                raise RequestError(401, "missing or invalid bearer token")

        def _read_json_body(self) -> dict[str, Any]:
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                raise RequestError(400, "invalid Content-Length") from None
            if length <= 0:
                raise RequestError(400, "request body is required")
            if length > MAX_BODY_BYTES:
                raise RequestError(413, f"request body is larger than {MAX_BODY_BYTES} bytes")
            raw_body = self.rfile.read(length)
            try:
                text = raw_body.decode("utf-8")
            except UnicodeDecodeError:
                raise RequestError(
                    400,
                    "body must be UTF-8 encoded JSON (Windows PowerShell 5.1 sends Latin-1 by default; "
                    "send the body as UTF-8 bytes with charset=utf-8)",
                ) from None
            try:
                payload = json.loads(text)
            except json.JSONDecodeError:
                raise RequestError(400, "body must be valid JSON") from None
            if not isinstance(payload, dict):
                raise RequestError(400, "body must be a JSON object")
            return payload

        def do_GET(self) -> None:  # noqa: N802 - stdlib naming
            try:
                if self.path == "/health":
                    self._send_json(200, {"status": "ok"})
                else:
                    raise RequestError(404, "not found")
            except RequestError as exc:
                self._send_json(exc.status, {"error": exc.message})

        def do_POST(self) -> None:  # noqa: N802 - stdlib naming
            try:
                if self.path != "/analyze":
                    raise RequestError(404, "not found")
                self._check_token()
                payload = self._read_json_body()
                scenario = build_scenario(payload)
                top_k = parse_top_k(payload)
                self._send_json(200, analyze(scenario, top_k))
            except RequestError as exc:
                self._send_json(exc.status, {"error": exc.message})
            except Exception as exc:  # keep internals out of the response
                sys.stderr.write(f"[api] analysis failed: {exc!r}\n")
                self._send_json(500, {"error": "analysis failed; check the server log"})

    return Handler


def create_server(
    analyze: AnalyzeFunction,
    host: str = "127.0.0.1",
    port: int = 8765,
    token: str | None = None,
) -> ThreadingHTTPServer:
    if host not in LOOPBACK_HOSTS and not token:
        raise ValueError("binding to a non-loopback address requires an API token")
    return ThreadingHTTPServer((host, port), make_handler(analyze, token))
