from __future__ import annotations

import os
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.ingest.ollama_client import OllamaEmbeddingClient, OllamaGenerationClient
from app.rag.generator import (
    DEFAULT_OLLAMA_BASE_URL,
    DEFAULT_OLLAMA_GENERATE_MODEL,
    strip_think_tags,
)
from app.rag.vector_store import DEFAULT_CHROMA_PERSIST_DIRECTORY

from .query_rewrite import rewrite_scenario
from .store import DEFAULT_WRITEUPS_TOP_K, search_writeups


DEFAULT_ANALYSIS_TIMEOUT_SECONDS = 300
DEFAULT_ANALYSIS_OPTIONS: dict[str, object] = {
    "temperature": 0.3,
    "num_ctx": 8192,
    "num_predict": 900,
}
NO_REPORTS_NOTICE = (
    "No similar reports were found in the local writeups index. "
    "Any hypothesis below is general knowledge, not backed by a stored report."
)
# Cosine distance (0 = identical, 1 = unrelated). When even the closest report is farther
# than this, retrieval is weak and the analysis must be treated as speculative.
DEFAULT_WEAK_MATCH_DISTANCE = 0.45
WEAK_MATCH_NOTICE = (
    "WARNING: weak similarity. The closest report has distance {best:.3f} "
    "(threshold {threshold:.2f}), so none of these reports is a strong match for the scenario."
)


def weak_match_threshold() -> float:
    try:
        return float(os.getenv("WRITEUPS_WEAK_MATCH_DISTANCE", DEFAULT_WEAK_MATCH_DISTANCE))
    except ValueError:
        return DEFAULT_WEAK_MATCH_DISTANCE


def weak_match_warning(matches: list[tuple[dict[str, Any], float]]) -> str:
    if not matches:
        return ""
    best = min(distance for _, distance in matches)
    threshold = weak_match_threshold()
    if best <= threshold:
        return ""
    return WEAK_MATCH_NOTICE.format(best=best, threshold=threshold)

ANALYSIS_PROMPT = """You are an assistant for an authorized penetration tester. Reason about the SCENARIO using the SIMILAR REPORTS, which are real past cases.

Rules:
- Use only facts present in the scenario or in the reports. Do not invent endpoints, parameters, versions or results.
- Name the report (by title) each hypothesis comes from. If a hypothesis is general knowledge and not from a report, label it "general".
- A "general" hypothesis must not cite any report anywhere, including in its validation steps. Cite a report only for hypotheses that really come from it.
- Ignore reports that are not really related to the scenario.
- If a WARNING about weak similarity appears below, say clearly in section 5 that the hypotheses are speculative.
- Suggest only low-impact, non-destructive validation steps, within the authorized scope. No exploitation of data you do not own, no denial of service.
- If the information is not enough, say what is missing instead of guessing.

Answer in this format:
1. Reading of the scenario: what the signals indicate.
2. Analogies: which reports apply and why.
3. Hypotheses, most likely first, each with its basis (report title or "general").
4. Safe validation steps for each hypothesis.
5. What cannot be concluded yet, and what information would settle it.

SCENARIO:
{scenario}

SIMILAR REPORTS:
{reports}

Answer:"""


@dataclass(frozen=True)
class ScenarioAnalysis:
    scenario: str
    reports: list[dict[str, Any]]
    distances: list[float]
    context: str
    answer: str
    retrieval_query: str = ""


def format_reports_context(matches: list[tuple[dict[str, Any], float]]) -> str:
    if not matches:
        return NO_REPORTS_NOTICE

    blocks: list[str] = []
    for index, (report, distance) in enumerate(matches, start=1):
        stack = ", ".join(report.get("stack") or []) or "n/a"
        blocks.append(
            "\n".join(
                [
                    f"[{index}] Title: {report.get('title') or 'untitled'} (distance {distance:.3f})",
                    f"    Class: {report.get('vuln_class') or 'n/a'} | Stack: {stack} | Severity: {report.get('severity') or 'unknown'}",
                    f"    Entry point: {report.get('entry_point') or 'n/a'}",
                    f"    Root cause: {report.get('root_cause') or 'n/a'}",
                    f"    Technique: {report.get('technique') or 'n/a'}",
                    f"    Bypass notes: {report.get('bypass_notes') or 'n/a'}",
                    f"    Impact: {report.get('impact') or 'n/a'}",
                ]
            )
        )
    warning = weak_match_warning(matches)
    if warning:
        blocks.insert(0, warning)
    return "\n\n".join(blocks)


def build_analysis_prompt(scenario: str, reports_context: str) -> str:
    return ANALYSIS_PROMPT.format(scenario=scenario.strip(), reports=reports_context)


def build_analysis_client(
    base_url: str | None = None,
    model: str | None = None,
) -> OllamaGenerationClient:
    return OllamaGenerationClient(
        base_url=base_url or os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_BASE_URL),
        model=model or os.getenv("OLLAMA_GENERATE_MODEL", DEFAULT_OLLAMA_GENERATE_MODEL),
        timeout_seconds=int(
            os.getenv(
                "OLLAMA_GENERATE_TIMEOUT_SECONDS",
                os.getenv("OLLAMA_TIMEOUT_SECONDS", str(DEFAULT_ANALYSIS_TIMEOUT_SECONDS)),
            )
        ),
    )


def merge_matches(
    result_sets: list[list[tuple[dict[str, Any], float]]],
    top_k: int,
) -> list[tuple[dict[str, Any], float]]:
    """Combine results of several queries: one entry per writeup, best (smallest) distance wins."""
    best: dict[str, tuple[dict[str, Any], float]] = {}
    for results in result_sets:
        for report, distance in results:
            key = str(report.get("writeup_id") or report.get("source_path") or report.get("title"))
            if key not in best or distance < best[key][1]:
                best[key] = (report, distance)
    return sorted(best.values(), key=lambda item: item[1])[:top_k]


def retrieve_similar(
    scenario: str,
    embed_client: OllamaEmbeddingClient,
    generation_client: OllamaGenerationClient | None = None,
    persist_directory: str | Path = DEFAULT_CHROMA_PERSIST_DIRECTORY,
    top_k: int = DEFAULT_WRITEUPS_TOP_K,
) -> tuple[list[tuple[dict[str, Any], float]], str]:
    """Search with the original scenario and with an English rewrite; return (matches, rewrite used)."""
    retrieval_query = rewrite_scenario(scenario, generation_client) if generation_client is not None else ""

    queries = [scenario]
    if retrieval_query and retrieval_query.lower() != scenario.strip().lower():
        queries.append(retrieval_query)

    result_sets = [
        search_writeups(query, client=embed_client, persist_directory=persist_directory, top_k=top_k)
        for query in queries
    ]
    return merge_matches(result_sets, top_k), retrieval_query if len(queries) > 1 else ""


def _prepare(
    scenario: str,
    embed_client: OllamaEmbeddingClient,
    generation_client: OllamaGenerationClient | None,
    persist_directory: str | Path,
    top_k: int,
) -> tuple[list[tuple[dict[str, Any], float]], str, str, str]:
    if not scenario.strip():
        raise ValueError("scenario must not be empty")

    matches, retrieval_query = retrieve_similar(
        scenario, embed_client, generation_client, persist_directory, top_k
    )
    context = format_reports_context(matches)
    return matches, context, build_analysis_prompt(scenario, context), retrieval_query


def prepare_analysis(
    scenario: str,
    embed_client: OllamaEmbeddingClient,
    persist_directory: str | Path = DEFAULT_CHROMA_PERSIST_DIRECTORY,
    top_k: int = DEFAULT_WRITEUPS_TOP_K,
    generation_client: OllamaGenerationClient | None = None,
) -> tuple[list[tuple[dict[str, Any], float]], str, str]:
    matches, context, prompt, _ = _prepare(scenario, embed_client, generation_client, persist_directory, top_k)
    return matches, context, prompt


def analyze_scenario(
    scenario: str,
    embed_client: OllamaEmbeddingClient,
    generation_client: OllamaGenerationClient,
    persist_directory: str | Path = DEFAULT_CHROMA_PERSIST_DIRECTORY,
    top_k: int = DEFAULT_WRITEUPS_TOP_K,
) -> ScenarioAnalysis:
    matches, context, prompt, retrieval_query = _prepare(
        scenario, embed_client, generation_client, persist_directory, top_k
    )
    answer = strip_think_tags(generation_client.generate(prompt, options=DEFAULT_ANALYSIS_OPTIONS))
    return ScenarioAnalysis(
        scenario=scenario.strip(),
        reports=[report for report, _ in matches],
        distances=[distance for _, distance in matches],
        context=context,
        answer=answer,
        retrieval_query=retrieval_query,
    )


def stream_scenario_analysis(
    scenario: str,
    embed_client: OllamaEmbeddingClient,
    generation_client: OllamaGenerationClient,
    persist_directory: str | Path = DEFAULT_CHROMA_PERSIST_DIRECTORY,
    top_k: int = DEFAULT_WRITEUPS_TOP_K,
) -> tuple[list[tuple[dict[str, Any], float]], str, Iterator[str]]:
    matches, context, prompt, _ = _prepare(
        scenario, embed_client, generation_client, persist_directory, top_k
    )
    return matches, context, generation_client.generate_stream(prompt, options=DEFAULT_ANALYSIS_OPTIONS)
