from __future__ import annotations

import os
import re
from dataclasses import asdict, dataclass

from app.ingest.ollama_client import OllamaGenerationClient


WORD_PATTERN = re.compile(r"[a-z0-9]+")

DEFAULT_REWRITER_MODEL = "qwen3.5:4b"
DEFAULT_REWRITER_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_REWRITER_TIMEOUT_SECONDS = 30
DEFAULT_REWRITER_OPTIONS: dict[str, object] = {
    "num_predict": 150,
    "temperature": 0.3,
}

_THINK_PATTERN = re.compile(r"<think>.*?</think>", re.DOTALL)

REWRITER_PROMPT_TEMPLATE = (
    "You are a cybersecurity search query optimizer for a RAG system that indexes "
    "penetration testing frameworks (PTES, NIST SP 800-115, OWASP, OSSTMM), "
    "Kali Linux tool documentation, and HackTricks pentesting guides.\n\n"
    "Given the user question below, generate 5 to 7 alternative search queries that "
    "would retrieve the most relevant chunks from these documents.\n\n"
    "Rules:\n"
    "- Always expand acronyms into full words (OSINT -> open source intelligence, "
    "SQLi -> SQL injection, XSS -> cross site scripting, RCE -> remote code execution)\n"
    "- Each query must be directly relevant to the user question topic\n"
    "- Include specific tool names and CLI commands related to the topic\n"
    "- One query should combine tool name + target protocol/service (e.g. 'hydra ftp brute force')\n"
    "- One query should list tool names specific to the topic (not generic tools)\n"
    "- One query should describe the technique at a conceptual level using full words\n"
    "- If a specific tool is mentioned, include a query with the tool name + command syntax\n"
    "- Keep each query short (3-8 words)\n"
    "- Output ONLY the queries, one per line, no numbering, no explanation\n\n"
    "User question: {question}\n\n"
    "Search queries:"
)


@dataclass(frozen=True)
class QueryRewrite:
    original_query: str
    normalized_query: str
    expanded_queries: list[str]
    detected_intent: str
    tool_terms: list[str]
    query_terms: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _tokenize(text: str) -> list[str]:
    return WORD_PATTERN.findall(text.lower())


def _parse_llm_queries(raw_output: str) -> list[str]:
    cleaned = _THINK_PATTERN.sub("", raw_output).strip()
    queries: list[str] = []
    for line in cleaned.splitlines():
        line = re.sub(r"^\d+[\.\)\-]\s*", "", line).strip()
        line = line.strip("-•* ")
        if len(line) < 5 or len(line) > 200:
            continue
        queries.append(line)
    return queries[:7]


def _generate_expanded_queries(
    question: str,
    base_url: str | None = None,
    model: str | None = None,
) -> list[str]:
    resolved_base_url = base_url or os.getenv("OLLAMA_BASE_URL", DEFAULT_REWRITER_BASE_URL)
    resolved_model = model or os.getenv("OLLAMA_GENERATE_MODEL", DEFAULT_REWRITER_MODEL)
    resolved_timeout = int(
        os.getenv("OLLAMA_REWRITER_TIMEOUT_SECONDS", str(DEFAULT_REWRITER_TIMEOUT_SECONDS))
    )

    client = OllamaGenerationClient(
        base_url=resolved_base_url,
        model=resolved_model,
        timeout_seconds=resolved_timeout,
    )

    try:
        client.is_available()
        prompt = REWRITER_PROMPT_TEMPLATE.format(question=question.strip())
        raw_output = client.generate(prompt, options=DEFAULT_REWRITER_OPTIONS)
        return _parse_llm_queries(raw_output)
    except Exception:
        return []


def rewrite_query(
    query: str,
    base_url: str | None = None,
    model: str | None = None,
) -> QueryRewrite:
    normalized_query = " ".join(query.strip().split())
    tokens = _tokenize(normalized_query)
    filtered_terms = tokens

    expanded_queries = _generate_expanded_queries(
        normalized_query,
        base_url=base_url,
        model=model,
    )

    deduplicated_queries: list[str] = []
    seen = {normalized_query.lower()}
    for expanded_query in expanded_queries:
        normalized_expansion = " ".join(expanded_query.split())
        key = normalized_expansion.lower()
        if not normalized_expansion or key in seen:
            continue
        seen.add(key)
        deduplicated_queries.append(normalized_expansion)

    return QueryRewrite(
        original_query=query,
        normalized_query=normalized_query,
        expanded_queries=deduplicated_queries,
        detected_intent="llm_rewrite",
        tool_terms=[],
        query_terms=filtered_terms,
    )
