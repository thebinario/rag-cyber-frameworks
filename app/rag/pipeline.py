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
    results = retrieve_chunks(
        query=question,
        top_k=top_k,
        persist_directory=persist_directory,
        collection_name=collection_name,
        base_url=embed_base_url,
        model=embed_model,
    )
    context = format_retrieval_context(results)

    if not results or not context.strip():
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
        sources=results,
        context=context,
    )
