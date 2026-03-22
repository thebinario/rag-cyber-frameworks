from __future__ import annotations

import os
import re
from collections.abc import Iterator

from app.ingest.ollama_client import OllamaGenerationClient


DEFAULT_OLLAMA_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_OLLAMA_GENERATE_MODEL = "qwen3.5:4b"
DEFAULT_OLLAMA_TIMEOUT_SECONDS = 300
INSUFFICIENT_EVIDENCE_MESSAGE = (
    "I do not have enough evidence in the retrieved context to answer that safely."
)

DEFAULT_GENERATION_OPTIONS: dict[str, object] = {
    "num_predict": 512,
    "temperature": 0.3,
}

_THINK_PATTERN = re.compile(r"<think>.*?</think>", re.DOTALL)


def strip_think_tags(text: str) -> str:
    return _THINK_PATTERN.sub("", text).strip()


def build_grounded_prompt(question: str, context: str) -> str:
    normalized_question = question.strip()
    normalized_context = context.strip()
    return "\n\n".join(
        [
            "Answer as a cybersecurity assistant using only the provided context.",
            f"If the context is insufficient, reply exactly with: {INSUFFICIENT_EVIDENCE_MESSAGE}",
            "If a named tool does not appear in the context, say that clearly.",
            "If the context supports only the technique, answer only at technique level.",
            "Do not invent commands, flags, or procedures.",
            "Keep the answer concise and factual.",
            f"Question:\n{normalized_question}",
            f"Context:\n{normalized_context}",
            "Answer:",
        ]
    )


def generate_grounded_answer(
    question: str,
    context: str,
    base_url: str | None = None,
    model: str | None = None,
    options: dict[str, object] | None = None,
) -> str:
    if not question.strip():
        raise ValueError("question must not be empty")
    if not context.strip():
        return INSUFFICIENT_EVIDENCE_MESSAGE

    resolved_base_url = base_url or os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_BASE_URL)
    resolved_model = model or os.getenv("OLLAMA_GENERATE_MODEL", DEFAULT_OLLAMA_GENERATE_MODEL)
    resolved_timeout = int(
        os.getenv(
            "OLLAMA_GENERATE_TIMEOUT_SECONDS",
            os.getenv("OLLAMA_TIMEOUT_SECONDS", str(DEFAULT_OLLAMA_TIMEOUT_SECONDS)),
        )
    )
    resolved_options = {**DEFAULT_GENERATION_OPTIONS, **(options or {})}

    client = OllamaGenerationClient(
        base_url=resolved_base_url,
        model=resolved_model,
        timeout_seconds=resolved_timeout,
    )
    client.is_available()
    prompt = build_grounded_prompt(question, context)
    return strip_think_tags(client.generate(prompt, options=resolved_options))


def generate_grounded_answer_stream(
    question: str,
    context: str,
    base_url: str | None = None,
    model: str | None = None,
    options: dict[str, object] | None = None,
) -> Iterator[str]:
    if not question.strip():
        raise ValueError("question must not be empty")
    if not context.strip():
        yield INSUFFICIENT_EVIDENCE_MESSAGE
        return

    resolved_base_url = base_url or os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_BASE_URL)
    resolved_model = model or os.getenv("OLLAMA_GENERATE_MODEL", DEFAULT_OLLAMA_GENERATE_MODEL)
    resolved_timeout = int(
        os.getenv(
            "OLLAMA_GENERATE_TIMEOUT_SECONDS",
            os.getenv("OLLAMA_TIMEOUT_SECONDS", str(DEFAULT_OLLAMA_TIMEOUT_SECONDS)),
        )
    )
    resolved_options = {**DEFAULT_GENERATION_OPTIONS, **(options or {})}

    client = OllamaGenerationClient(
        base_url=resolved_base_url,
        model=resolved_model,
        timeout_seconds=resolved_timeout,
    )
    client.is_available()
    prompt = build_grounded_prompt(question, context)
    yield from client.generate_stream(prompt, options=resolved_options)
