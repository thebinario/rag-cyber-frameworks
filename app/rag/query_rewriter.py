from __future__ import annotations

import re
from dataclasses import asdict, dataclass


WORD_PATTERN = re.compile(r"[a-z0-9]+")
STOP_WORDS = {
    "a",
    "an",
    "and",
    "for",
    "how",
    "in",
    "is",
    "looking",
    "of",
    "on",
    "the",
    "to",
    "use",
    "using",
    "what",
    "with",
}

TOOL_QUERY_EXPANSIONS = {
    "gobuster": [
        "subdomain enumeration dns brute force",
        "subdomain discovery dns records",
        "virtual host discovery subdomains",
    ],
}

TECHNIQUE_QUERY_EXPANSIONS = {
    "subdomain": [
        "subdomain enumeration",
        "dns subdomains",
        "discover subdomains dns",
    ],
    "dns": [
        "dns enumeration",
        "domain records dns",
    ],
    "osint": [
        "open source intelligence reconnaissance",
    ],
}


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


def rewrite_query(query: str) -> QueryRewrite:
    normalized_query = " ".join(query.strip().split())
    tokens = _tokenize(normalized_query)
    filtered_terms = [token for token in tokens if token not in STOP_WORDS]

    expanded_queries: list[str] = []
    tool_terms: list[str] = []
    detected_intent = "general retrieval"

    for token in filtered_terms:
        if token in TOOL_QUERY_EXPANSIONS:
            tool_terms.append(token)
            expanded_queries.extend(TOOL_QUERY_EXPANSIONS[token])

        if token in TECHNIQUE_QUERY_EXPANSIONS:
            expanded_queries.extend(TECHNIQUE_QUERY_EXPANSIONS[token])

    if "subdomain" in filtered_terms or "dns" in filtered_terms:
        detected_intent = "subdomain and dns enumeration"
        expanded_queries.append("subdomain enumeration dns reconnaissance")
    elif "osint" in filtered_terms:
        detected_intent = "open source intelligence"
    elif "directory" in filtered_terms or "directories" in filtered_terms:
        detected_intent = "web content discovery"

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
        detected_intent=detected_intent,
        tool_terms=tool_terms,
        query_terms=filtered_terms,
    )
