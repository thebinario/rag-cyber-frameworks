from __future__ import annotations

import json
from urllib import error, request


class OllamaEmbeddingClient:
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

    def embed(self, text: str) -> list[float]:
        payload = json.dumps(
            {
                "model": self.model,
                "input": text,
            }
        ).encode("utf-8")
        endpoint = f"{self.base_url}/api/embed"
        http_request = request.Request(
            endpoint,
            data=payload,
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
            payload = json.loads(raw_body)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Ollama returned invalid JSON") from exc

        embeddings = payload.get("embeddings")
        if isinstance(embeddings, list) and embeddings:
            embedding = embeddings[0]
            if isinstance(embedding, list) and embedding:
                return embedding

        embedding = payload.get("embedding")
        if isinstance(embedding, list) and embedding:
            return embedding

        raise RuntimeError("Ollama response did not contain a usable embedding")
