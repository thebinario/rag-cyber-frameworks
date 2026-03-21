from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .generator import INSUFFICIENT_EVIDENCE_MESSAGE, generate_grounded_answer
from .retriever import RetrievalResult, format_retrieval_context, retrieve_chunks
from .vector_store import (
    DEFAULT_CHROMA_COLLECTION_NAME,
    DEFAULT_CHROMA_PERSIST_DIRECTORY,
    DEFAULT_SEARCH_TOP_K,
)

MAX_GENERATION_CHUNK_CHARACTERS = 1200


@dataclass(frozen=True)
class RagAnswer:
    question: str
    answer: str
    sources: list[RetrievalResult]
    context: str

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["sources"] = [source.to_dict() for source in self.sources]
        return payload


def _build_generation_context(
    results: list[RetrievalResult],
    top_k: int,
    max_chunk_characters: int = MAX_GENERATION_CHUNK_CHARACTERS,
) -> str:
    blocks: list[str] = []

    for index, result in enumerate(results[:top_k], start=1):
        truncated_text = result.text.strip()
        if len(truncated_text) > max_chunk_characters:
            truncated_text = truncated_text[:max_chunk_characters].rstrip() + "..."

        blocks.append(
            "\n".join(
                [
                    f"[Source {index}]",
                    f"chunk_id: {result.chunk_id}",
                    f"title: {result.title}",
                    f"framework: {result.framework}",
                    f"source_path: {result.source_path}",
                    "text:",
                    truncated_text,
                ]
            )
        )

    return "\n\n---\n\n".join(blocks)


def run_rag_pipeline(
    question: str,
    top_k: int = DEFAULT_SEARCH_TOP_K,
    persist_directory: str | Path = DEFAULT_CHROMA_PERSIST_DIRECTORY,
    collection_name: str = DEFAULT_CHROMA_COLLECTION_NAME,
    embed_base_url: str | None = None,
    embed_model: str | None = None,
    generate_base_url: str | None = None,
    generate_model: str | None = None,
) -> RagAnswer:
    retrieval_top_k = max(top_k, 4)
    results = retrieve_chunks(
        query=question,
        top_k=retrieval_top_k,
        persist_directory=persist_directory,
        collection_name=collection_name,
        base_url=embed_base_url,
        model=embed_model,
    )
    selected_results = results[:top_k]
    context = _build_generation_context(selected_results, top_k=top_k)

    if not selected_results or not context.strip():
        answer = INSUFFICIENT_EVIDENCE_MESSAGE
    else:
        answer = generate_grounded_answer(
            question=question,
            context=context,
            base_url=generate_base_url,
            model=generate_model,
        )

    return RagAnswer(
        question=question,
        answer=answer,
        sources=selected_results,
        context=context,
    )
