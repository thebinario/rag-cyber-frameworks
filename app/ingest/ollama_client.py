from __future__ import annotations

import json
from urllib import error, request
from typing import Iterator


class OllamaClient:
    def __init__(self, base_url: str, model: str, timeout_seconds: int = 60) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

    def is_available(self) -> None:
        endpoint = f"{self.base_url}/api/tags"
        http_request = request.Request(endpoint, method="GET")

        try:
            with request.urlopen(http_request, timeout=self.timeout_seconds):
                return
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Ollama HTTP {exc.code}: {body}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"Could not connect to Ollama at {self.base_url}: {exc.reason}") from exc

    def _post_json(self, endpoint: str, payload: dict[str, object]) -> dict[str, object]:
        raw_payload = json.dumps(payload).encode("utf-8")
        http_request = request.Request(
            f"{self.base_url}{endpoint}",
            data=raw_payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(http_request, timeout=self.timeout_seconds) as response:
                raw_body = response.read().decode("utf-8")
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Ollama HTTP {exc.code}: {body}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"Could not connect to Ollama at {self.base_url}: {exc.reason}") from exc

        try:
            return json.loads(raw_body)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Ollama returned invalid JSON") from exc


class OllamaEmbeddingClient(OllamaClient):
    def embed(self, text: str) -> list[float]:
        payload = self._post_json(
            "/api/embed",
            {
                "model": self.model,
                "input": text,
            },
        )

        embeddings = payload.get("embeddings")
        if isinstance(embeddings, list) and embeddings:
            embedding = embeddings[0]
            if isinstance(embedding, list) and embedding:
                return embedding

        embedding = payload.get("embedding")
        if isinstance(embedding, list) and embedding:
            return embedding

        raise RuntimeError("Ollama response did not contain a usable embedding")


class OllamaGenerationClient(OllamaClient):
    """Ollama text generation client using the /api/chat endpoint.

    Uses /api/chat instead of /api/generate to support the ``think`` flag
    which disables the reasoning/thinking mode in models like qwen3.5.
    """

    def generate(self, prompt: str, options: dict[str, object] | None = None) -> str:
        request_body: dict[str, object] = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "think": False,
        }
        if options:
            request_body["options"] = options
        payload = self._post_json("/api/chat", request_body)

        message = payload.get("message")
        if isinstance(message, dict):
            content = message.get("content")
            if isinstance(content, str) and content.strip():
                return content.strip()

        raise RuntimeError("Ollama response did not contain a usable text generation")

    def generate_stream(self, prompt: str, options: dict[str, object] | None = None) -> Iterator[str]:
        request_body: dict[str, object] = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
            "think": False,
        }
        if options:
            request_body["options"] = options
        raw_payload = json.dumps(request_body).encode("utf-8")
        http_request = request.Request(
            f"{self.base_url}/api/chat",
            data=raw_payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(http_request, timeout=self.timeout_seconds) as response:
                for raw_line in response:
                    line = raw_line.decode("utf-8").strip()
                    if not line:
                        continue
                    try:
                        payload = json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise RuntimeError("Ollama returned invalid JSON in streaming response") from exc

                    message = payload.get("message")
                    if isinstance(message, dict):
                        content = message.get("content")
                        if isinstance(content, str) and content:
                            yield content

                    if payload.get("done") is True:
                        return
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Ollama HTTP {exc.code}: {body}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"Could not connect to Ollama at {self.base_url}: {exc.reason}") from exc
