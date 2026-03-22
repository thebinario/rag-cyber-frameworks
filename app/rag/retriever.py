from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from app.ingest.models import DocumentChunk

from .query_rewriter import QueryRewrite, rewrite_query
from .vector_store import (
    DEFAULT_CHROMA_COLLECTION_NAME,
    DEFAULT_CHROMA_PERSIST_DIRECTORY,
    DEFAULT_SEARCH_TOP_K,
    search_chunks,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CHUNKS_PATH = REPO_ROOT / "data" / "processed" / "chunks" / "chunks.jsonl"
DEFAULT_INTERNAL_TOP_K = 20
MAX_EXPANDED_QUERIES = 7
WORD_PATTERN = re.compile(r"[a-z0-9]+")
DEFAULT_RETRIEVAL_MODE = "expanded"
EXPANDED_RETRIEVAL_MODE = "expanded"
VALID_RETRIEVAL_MODES = {DEFAULT_RETRIEVAL_MODE, EXPANDED_RETRIEVAL_MODE}

_PRACTICAL_INTENT_WORDS = {"how", "use", "example", "command", "run", "execute", "tutorial", "usage", "syntax"}
_CLI_COMMAND_PATTERN = re.compile(
    r"(?:^|\n)\s*(?:(?:root@|\\$|#|>)\s*\S+|(?:sudo\s+)?\S+\s+-[a-zA-Z])"
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
    retrieval_score: float
    matched_terms: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _tokenize(text: str) -> set[str]:
    return set(WORD_PATTERN.findall(text.lower()))


def _load_chunk_map(chunks_path: str | Path = DEFAULT_CHUNKS_PATH) -> dict[str, DocumentChunk]:
    path = Path(chunks_path)
    chunk_map: dict[str, DocumentChunk] = {}

    with path.open("r", encoding="utf-8") as file_handle:
        for line in file_handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            chunk = DocumentChunk(**payload)
            chunk_map[chunk.chunk_id] = chunk

    return chunk_map


def _build_query_candidates(query_rewrite: QueryRewrite) -> list[str]:
    return [query_rewrite.normalized_query] + query_rewrite.expanded_queries[:MAX_EXPANDED_QUERIES]


def _merge_raw_results(
    query_candidates: list[str],
    persist_directory: str | Path,
    collection_name: str,
    base_url: str | None,
    model: str | None,
    internal_top_k: int,
) -> dict[str, dict[str, object]]:
    merged_results: dict[str, dict[str, object]] = {}

    for candidate in query_candidates:
        raw_results = search_chunks(
            query=candidate,
            top_k=internal_top_k,
            persist_directory=persist_directory,
            collection_name=collection_name,
            base_url=base_url,
            model=model,
        )
        for result in raw_results:
            chunk_id = str(result["chunk_id"])
            previous = merged_results.get(chunk_id)
            if previous is None or float(result["distance"]) < float(previous["distance"]):
                merged_results[chunk_id] = result

    return merged_results


def _expand_neighbor_results(
    merged_results: dict[str, dict[str, object]],
    chunk_map: dict[str, DocumentChunk],
) -> dict[str, dict[str, object]]:
    expanded_results = dict(merged_results)

    for result in list(merged_results.values()):
        metadata = result["metadata"]
        document_id = str(metadata["document_id"])
        chunk_index = int(metadata["chunk_index"])

        for neighbor_index in (chunk_index - 1, chunk_index + 1):
            if neighbor_index < 0:
                continue
            neighbor_chunk_id = f"{document_id}-chunk-{neighbor_index:04d}"
            if neighbor_chunk_id in expanded_results:
                continue
            neighbor = chunk_map.get(neighbor_chunk_id)
            if neighbor is None:
                continue

            expanded_results[neighbor_chunk_id] = {
                "chunk_id": neighbor.chunk_id,
                "distance": float(result["distance"]) + 0.015,
                "text": neighbor.text,
                "metadata": {
                    "document_id": neighbor.document_id,
                    "title": neighbor.title,
                    "framework": neighbor.framework,
                    "source_type": neighbor.source_type,
                    "source_path": neighbor.source_path,
                    "chunk_index": neighbor.chunk_index,
                },
            }

    return expanded_results


def _collect_search_terms(query_rewrite: QueryRewrite) -> set[str]:
    terms: set[str] = set()
    for term in query_rewrite.query_terms:
        if len(term) > 2:
            terms.add(term)
    for expanded_query in query_rewrite.expanded_queries:
        for term in _tokenize(expanded_query):
            if len(term) > 2:
                terms.add(term)
    return terms


def _has_practical_intent(query_terms: list[str]) -> bool:
    return bool(set(query_terms) & _PRACTICAL_INTENT_WORDS)


def _has_cli_examples(text: str) -> bool:
    return bool(_CLI_COMMAND_PATTERN.search(text))


def _extract_tool_names(query_terms: list[str]) -> set[str]:
    return {t for t in query_terms if len(t) > 2 and t.isalpha() and t.islower()}


def _score_result(
    result: dict[str, object],
    query_rewrite: QueryRewrite,
    all_search_terms: set[str],
) -> tuple[float, list[str]]:
    result_text = str(result["text"])
    metadata = result["metadata"]
    haystack_text = " ".join(
        [
            result_text,
            str(metadata["title"]),
            str(metadata["framework"]),
            str(metadata["source_path"]),
        ]
    )
    haystack_terms = _tokenize(haystack_text)

    matched_terms = sorted(all_search_terms & haystack_terms)

    lexical_score = len(matched_terms) * 0.05

    practical_boost = 0.0
    if _has_practical_intent(query_rewrite.query_terms) and _has_cli_examples(result_text):
        practical_boost = 0.15

    tool_boost = 0.0
    query_tool_names = _extract_tool_names(query_rewrite.query_terms)
    doc_id_lower = str(metadata.get("document_id", "")).lower()
    title_lower = str(metadata.get("title", "")).lower()
    for tool_name in query_tool_names:
        if tool_name in doc_id_lower or tool_name in title_lower:
            tool_boost = 0.12
            break

    retrieval_score = lexical_score + practical_boost + tool_boost - float(result["distance"])
    return retrieval_score, matched_terms


def retrieve_chunks(
    query: str,
    top_k: int = DEFAULT_SEARCH_TOP_K,
    persist_directory: str | Path = DEFAULT_CHROMA_PERSIST_DIRECTORY,
    collection_name: str = DEFAULT_CHROMA_COLLECTION_NAME,
    base_url: str | None = None,
    model: str | None = None,
    chunks_path: str | Path = DEFAULT_CHUNKS_PATH,
    retrieval_mode: str = DEFAULT_RETRIEVAL_MODE,
    rewriter_base_url: str | None = None,
    rewriter_model: str | None = None,
) -> list[RetrievalResult]:
    if retrieval_mode not in VALID_RETRIEVAL_MODES:
        supported_modes = ", ".join(sorted(VALID_RETRIEVAL_MODES))
        raise ValueError(f"retrieval_mode must be one of: {supported_modes}")

    query_rewrite = rewrite_query(
        query,
        base_url=rewriter_base_url,
        model=rewriter_model,
    )
    if retrieval_mode == EXPANDED_RETRIEVAL_MODE:
        query_candidates = _build_query_candidates(query_rewrite)
        internal_top_k = max(DEFAULT_INTERNAL_TOP_K, top_k * 4)
    else:
        query_candidates = [query_rewrite.normalized_query]
        internal_top_k = top_k

    merged_results = _merge_raw_results(
        query_candidates=query_candidates,
        persist_directory=persist_directory,
        collection_name=collection_name,
        base_url=base_url,
        model=model,
        internal_top_k=internal_top_k,
    )
    expanded_results = merged_results
    if retrieval_mode == EXPANDED_RETRIEVAL_MODE:
        chunk_map = _load_chunk_map(chunks_path)
        expanded_results = _expand_neighbor_results(merged_results, chunk_map)

    all_search_terms = _collect_search_terms(query_rewrite)

    retrieval_results: list[RetrievalResult] = []
    for result in expanded_results.values():
        metadata = result["metadata"]
        retrieval_score, matched_terms = _score_result(result, query_rewrite, all_search_terms)
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
                retrieval_score=retrieval_score,
                matched_terms=matched_terms,
            )
        )

    retrieval_results.sort(
        key=lambda result: (
            -result.retrieval_score,
            result.distance,
            result.chunk_index,
        )
    )
    return _diversify_results(retrieval_results, top_k)


MAX_CHUNKS_PER_DOCUMENT = 3


def _diversify_results(
    results: list[RetrievalResult],
    top_k: int,
) -> list[RetrievalResult]:
    selected: list[RetrievalResult] = []
    doc_counts: dict[str, int] = {}

    for result in results:
        if len(selected) >= top_k:
            break
        count = doc_counts.get(result.document_id, 0)
        if count >= MAX_CHUNKS_PER_DOCUMENT:
            continue
        selected.append(result)
        doc_counts[result.document_id] = count + 1

    return selected


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
                f"retrieval_score: {result.retrieval_score}",
                f"matched_terms: {', '.join(result.matched_terms) if result.matched_terms else 'none'}",
                "text:",
                result.text,
            ]
        )
        blocks.append(block)

    return "\n\n---\n\n".join(blocks)
