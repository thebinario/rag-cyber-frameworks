from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .vector_store import (
    DEFAULT_CHROMA_COLLECTION_NAME,
    DEFAULT_CHROMA_PERSIST_DIRECTORY,
    DEFAULT_SEARCH_TOP_K,
    search_chunks,
)


@dataclass(frozen=True)
class RetrievalResult:
    chunk_id: str
    document_id: str
    title: str
    framework: str
    source_type: str
    source_path: str
    chunk_index: int
    text: str
    distance: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def retrieve_chunks(
    query: str,
    top_k: int = DEFAULT_SEARCH_TOP_K,
    persist_directory: str | Path = DEFAULT_CHROMA_PERSIST_DIRECTORY,
    collection_name: str = DEFAULT_CHROMA_COLLECTION_NAME,
    base_url: str | None = None,
    model: str | None = None,
) -> list[RetrievalResult]:
    raw_results = search_chunks(
        query=query,
        top_k=top_k,
        persist_directory=persist_directory,
        collection_name=collection_name,
        base_url=base_url,
        model=model,
    )

    retrieval_results: list[RetrievalResult] = []
    for result in raw_results:
        metadata = result["metadata"]
        retrieval_results.append(
            RetrievalResult(
                chunk_id=result["chunk_id"],
                document_id=str(metadata["document_id"]),
                title=str(metadata["title"]),
                framework=str(metadata["framework"]),
                source_type=str(metadata["source_type"]),
                source_path=str(metadata["source_path"]),
                chunk_index=int(metadata["chunk_index"]),
                text=str(result["text"]),
                distance=float(result["distance"]),
            )
        )

    return retrieval_results


def format_retrieval_context(results: list[RetrievalResult]) -> str:
    blocks: list[str] = []

    for index, result in enumerate(results, start=1):
        block = "\n".join(
            [
                f"[Chunk {index}]",
                f"chunk_id: {result.chunk_id}",
                f"document_id: {result.document_id}",
                f"title: {result.title}",
                f"framework: {result.framework}",
                f"source_type: {result.source_type}",
                f"source_path: {result.source_path}",
                f"chunk_index: {result.chunk_index}",
                f"distance: {result.distance}",
                "text:",
                result.text,
            ]
        )
        blocks.append(block)

    return "\n\n---\n\n".join(blocks)
