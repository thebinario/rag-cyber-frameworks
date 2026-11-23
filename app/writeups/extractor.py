from __future__ import annotations

import json
import os
import re
from pathlib import Path

from app.ingest.cleaner import clean_text
from app.ingest.ollama_client import OllamaGenerationClient
from app.ingest.source_loaders import get_source_loader
from app.rag.generator import (
    DEFAULT_OLLAMA_BASE_URL,
    DEFAULT_OLLAMA_GENERATE_MODEL,
    strip_think_tags,
)

from .schema import WriteupRecord, compute_content_hash, normalize_extraction


DEFAULT_EXTRACTION_TIMEOUT_SECONDS = 300
DEFAULT_EXTRACTION_OPTIONS: dict[str, object] = {
    "temperature": 0,
    "num_ctx": 8192,
    "num_predict": 700,
}

# A writeup is truncated to head + tail so the prompt fits a small local context window.
MAX_HEAD_CHARACTERS = 9000
MAX_TAIL_CHARACTERS = 3000

SUPPORTED_SUFFIXES = (".md", ".txt", ".html", ".htm", ".pdf")

EXTRACTION_PROMPT = """You are a security analyst. Read the writeup and reply with ONLY one valid JSON object, no extra text.

Fields:
- "title": short title
- "vuln_class": e.g. IDOR, SQL Injection, SSRF, XSS, Auth Bypass, RCE, Race Condition, Business Logic
- "stack": list of technologies mentioned (frameworks, servers, languages, services)
- "entry_point": where the flaw lived (endpoint, parameter, feature)
- "root_cause": the underlying cause in one or two sentences
- "technique": how it was exploited, as a short summary of the steps
- "bypass_notes": filters, WAF rules or validations that were bypassed, if any
- "impact": what an attacker gains
- "severity": one of low, medium, high, critical (only if the text supports it)
- "tags": list of keywords

Rules: use only what the writeup states. If a field is not in the text use "" or []. Do not invent details.

WRITEUP:
{text}
"""

_JSON_OBJECT_PATTERN = re.compile(r"\{.*\}", re.DOTALL)


def prepare_writeup_text(text: str) -> str:
    cleaned = clean_text(text)
    limit = MAX_HEAD_CHARACTERS + MAX_TAIL_CHARACTERS
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[:MAX_HEAD_CHARACTERS]}\n\n[...truncated...]\n\n{cleaned[-MAX_TAIL_CHARACTERS:]}"


def build_extraction_prompt(text: str) -> str:
    return EXTRACTION_PROMPT.format(text=prepare_writeup_text(text))


def parse_json_object(raw: str) -> dict[str, object]:
    """Parse a JSON object out of model output, tolerating think tags and code fences."""
    text = strip_think_tags(raw).strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        match = _JSON_OBJECT_PATTERN.search(text)
        if match is None:
            raise ValueError("model output did not contain a JSON object") from None
        try:
            parsed = json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            raise ValueError(f"model output was not valid JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("model output JSON was not an object")
    return parsed


def build_extraction_client(
    base_url: str | None = None,
    model: str | None = None,
) -> OllamaGenerationClient:
    resolved_model = (
        model
        or os.getenv("OLLAMA_EXTRACT_MODEL")
        or os.getenv("OLLAMA_GENERATE_MODEL", DEFAULT_OLLAMA_GENERATE_MODEL)
    )
    return OllamaGenerationClient(
        base_url=base_url or os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_BASE_URL),
        model=resolved_model,
        timeout_seconds=int(
            os.getenv(
                "OLLAMA_EXTRACT_TIMEOUT_SECONDS",
                os.getenv("OLLAMA_TIMEOUT_SECONDS", str(DEFAULT_EXTRACTION_TIMEOUT_SECONDS)),
            )
        ),
    )


def extract_writeup(
    text: str,
    *,
    source_path: str,
    client: OllamaGenerationClient,
    fallback_title: str = "",
) -> WriteupRecord:
    """Run structured extraction on one writeup. Raises ValueError/RuntimeError on failure."""
    if not text.strip():
        raise ValueError("writeup is empty")

    raw = client.generate(
        build_extraction_prompt(text),
        options=DEFAULT_EXTRACTION_OPTIONS,
        response_format="json",
    )
    payload = parse_json_object(raw)
    return normalize_extraction(
        payload,
        source_path=source_path,
        content_hash=compute_content_hash(text),
        extraction_model=client.model,
        fallback_title=fallback_title,
    )


def load_writeup_text(path: str | Path) -> str:
    _, loader = get_source_loader(path)
    return loader(path)


def discover_writeup_files(directory: str | Path) -> list[Path]:
    root = Path(directory)
    if not root.is_dir():
        return []
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )
