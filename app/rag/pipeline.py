from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path

from .generator import (
    INSUFFICIENT_EVIDENCE_MESSAGE,
    generate_grounded_answer,
    generate_grounded_answer_stream,
)
from .retriever import (
    DEFAULT_RETRIEVAL_MODE,
    RetrievalResult,
    format_retrieval_context,
    retrieve_chunks,
)
from .vector_store import (
    DEFAULT_CHROMA_COLLECTION_NAME,
    DEFAULT_CHROMA_PERSIST_DIRECTORY,
    DEFAULT_SEARCH_TOP_K,
)

MAX_GENERATION_CHUNK_CHARACTERS = 1200
MAX_GENERATION_SOURCES = 5

_LOW_QUALITY_INDICATORS = re.compile(
    r"table of contents|list of abbreviations|glossary|list of acronyms",
    re.IGNORECASE,
)

_ABBREVIATION_LINE = re.compile(r"^[A-Z&/]{2,}\s+\S", re.MULTILINE)


def _is_low_quality_chunk(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < 50:
        return True
    lines = [line.strip() for line in stripped.splitlines() if line.strip()]
    if not lines:
        return True
    avg_line_len = sum(len(line) for line in lines) / len(lines)
    if avg_line_len < 30 and len(lines) >= 3:
        return True
    if _LOW_QUALITY_INDICATORS.search(stripped):
        return True
    dots_ratio = stripped.count(".") / max(len(stripped), 1)
    if dots_ratio > 0.12:
        return True
    abbrev_matches = _ABBREVIATION_LINE.findall(stripped)
    if len(abbrev_matches) >= 3:
        return True
    return False


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


def prepare_rag_context(
    question: str,
    top_k: int = DEFAULT_SEARCH_TOP_K,
    persist_directory: str | Path = DEFAULT_CHROMA_PERSIST_DIRECTORY,
    collection_name: str = DEFAULT_CHROMA_COLLECTION_NAME,
    embed_base_url: str | None = None,
    embed_model: str | None = None,
    retrieval_mode: str = DEFAULT_RETRIEVAL_MODE,
    max_generation_sources: int = MAX_GENERATION_SOURCES,
    max_generation_chunk_characters: int = MAX_GENERATION_CHUNK_CHARACTERS,
) -> tuple[list[RetrievalResult], str]:
    retrieval_top_k = max(top_k, 4) if retrieval_mode != DEFAULT_RETRIEVAL_MODE else top_k
    results = retrieve_chunks(
        query=question,
        top_k=retrieval_top_k,
        persist_directory=persist_directory,
        collection_name=collection_name,
        base_url=embed_base_url,
        model=embed_model,
        retrieval_mode=retrieval_mode,
    )
    filtered_results = [r for r in results if not _is_low_quality_chunk(r.text)]
    selected_results = filtered_results[: min(top_k, max_generation_sources)]
    context = _build_generation_context(
        selected_results,
        top_k=len(selected_results),
        max_chunk_characters=max_generation_chunk_characters,
    )
    return selected_results, context


def run_rag_pipeline(
    question: str,
    top_k: int = DEFAULT_SEARCH_TOP_K,
    persist_directory: str | Path = DEFAULT_CHROMA_PERSIST_DIRECTORY,
    collection_name: str = DEFAULT_CHROMA_COLLECTION_NAME,
    embed_base_url: str | None = None,
    embed_model: str | None = None,
    generate_base_url: str | None = None,
    generate_model: str | None = None,
    retrieval_mode: str = DEFAULT_RETRIEVAL_MODE,
    max_generation_sources: int = MAX_GENERATION_SOURCES,
    max_generation_chunk_characters: int = MAX_GENERATION_CHUNK_CHARACTERS,
    generate_options: dict[str, object] | None = None,
) -> RagAnswer:
    selected_results, context = prepare_rag_context(
        question=question,
        top_k=top_k,
        persist_directory=persist_directory,
        collection_name=collection_name,
        embed_base_url=embed_base_url,
        embed_model=embed_model,
        retrieval_mode=retrieval_mode,
        max_generation_sources=max_generation_sources,
        max_generation_chunk_characters=max_generation_chunk_characters,
    )

    if not selected_results or not context.strip():
        answer = INSUFFICIENT_EVIDENCE_MESSAGE
    else:
        answer = generate_grounded_answer(
            question=question,
            context=context,
            base_url=generate_base_url,
            model=generate_model,
            options=generate_options,
        )

    return RagAnswer(
        question=question,
        answer=answer,
        sources=selected_results,
        context=context,
    )


def stream_rag_answer(
    question: str,
    top_k: int = DEFAULT_SEARCH_TOP_K,
    persist_directory: str | Path = DEFAULT_CHROMA_PERSIST_DIRECTORY,
    collection_name: str = DEFAULT_CHROMA_COLLECTION_NAME,
    embed_base_url: str | None = None,
    embed_model: str | None = None,
    generate_base_url: str | None = None,
    generate_model: str | None = None,
    retrieval_mode: str = DEFAULT_RETRIEVAL_MODE,
    max_generation_sources: int = MAX_GENERATION_SOURCES,
    max_generation_chunk_characters: int = MAX_GENERATION_CHUNK_CHARACTERS,
    generate_options: dict[str, object] | None = None,
) -> tuple[list[RetrievalResult], str, Iterator[str]]:
    selected_results, context = prepare_rag_context(
        question=question,
        top_k=top_k,
        persist_directory=persist_directory,
        collection_name=collection_name,
        embed_base_url=embed_base_url,
        embed_model=embed_model,
        retrieval_mode=retrieval_mode,
        max_generation_sources=max_generation_sources,
        max_generation_chunk_characters=max_generation_chunk_characters,
    )

    if not selected_results or not context.strip():
        def _empty_stream() -> Iterator[str]:
            yield INSUFFICIENT_EVIDENCE_MESSAGE

        return selected_results, context, _empty_stream()

    return selected_results, context, generate_grounded_answer_stream(
        question=question,
        context=context,
        base_url=generate_base_url,
        model=generate_model,
        options=generate_options,
    )
