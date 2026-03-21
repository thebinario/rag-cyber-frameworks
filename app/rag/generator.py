from __future__ import annotations

import os

from app.ingest.ollama_client import OllamaGenerationClient


DEFAULT_OLLAMA_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_OLLAMA_GENERATE_MODEL = "qwen3.5:4b"
DEFAULT_OLLAMA_TIMEOUT_SECONDS = 300
INSUFFICIENT_EVIDENCE_MESSAGE = (
    "I do not have enough evidence in the retrieved context to answer that safely."
)


def build_grounded_prompt(question: str, context: str) -> str:
    normalized_question = question.strip()
    normalized_context = context.strip()
    return "\n\n".join(
        [
            "You are a cybersecurity assistant answering strictly from the provided context.",
            "Rules:",
            "1. Answer only with information supported by the context.",
            "2. Do not use outside knowledge.",
            f"3. If the context is insufficient, reply exactly with: {INSUFFICIENT_EVIDENCE_MESSAGE}",
            "4. If the question names a specific tool that does not appear in the context, say that clearly.",
            "5. If the context supports the technique but not the named tool, provide only technique-level guidance grounded in the context.",
            "6. Do not invent commands, flags, or procedures that are not explicitly present in the context.",
            "7. Keep the answer concise and factual.",
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
) -> str:
    if not question.strip():
        raise ValueError("question must not be empty")
    if not context.strip():
        return INSUFFICIENT_EVIDENCE_MESSAGE

    resolved_base_url = base_url or os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_BASE_URL)
    resolved_model = model or os.getenv("OLLAMA_GENERATE_MODEL", DEFAULT_OLLAMA_GENERATE_MODEL)
    resolved_timeout = int(
        os.getenv("OLLAMA_TIMEOUT_SECONDS", str(DEFAULT_OLLAMA_TIMEOUT_SECONDS))
    )

    client = OllamaGenerationClient(
        base_url=resolved_base_url,
        model=resolved_model,
        timeout_seconds=resolved_timeout,
    )
    client.is_available()
    prompt = build_grounded_prompt(question, context)
    return client.generate(prompt)
