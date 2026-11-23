from __future__ import annotations

import os
import sys
from typing import Protocol

from app.rag.generator import strip_think_tags


MAX_REWRITE_CHARACTERS = 600
REWRITE_OPTIONS: dict[str, object] = {
    "temperature": 0,
    "num_ctx": 4096,
    "num_predict": 160,
}
_DISABLED_VALUES = {"0", "false", "off", "no"}

REWRITE_PROMPT = """Rewrite the pentest scenario below as a short search query in English, for finding similar bug bounty reports.

Rules:
- Translate to English and keep every technical term, endpoint and parameter exactly as written.
- Add up to 3 likely vulnerability classes at the end, as "Possible classes: ...", using standard names (for example IDOR / broken object level authorization, SQL injection, XSS, SSRF).
- Do not add facts about the target that are not in the scenario. No explanations, no lists, 2 sentences at most.

SCENARIO:
{scenario}

SEARCH QUERY:"""


class _Generator(Protocol):
    def generate(self, prompt: str, options: dict[str, object] | None = None) -> str: ...


def rewrite_enabled() -> bool:
    return os.getenv("WRITEUPS_QUERY_REWRITE", "1").strip().lower() not in _DISABLED_VALUES


def build_rewrite_prompt(scenario: str) -> str:
    return REWRITE_PROMPT.format(scenario=scenario.strip())


def rewrite_scenario(scenario: str, client: _Generator) -> str:
    """Return an English retrieval query, or "" when rewriting is off or fails.

    The rewrite is used only to search. The final analysis always sees the original scenario.
    """
    if not rewrite_enabled() or not scenario.strip():
        return ""
    try:
        raw = client.generate(build_rewrite_prompt(scenario), options=REWRITE_OPTIONS)
    except Exception as exc:  # retrieval must still work with the original text
        sys.stderr.write(f"[writeups] query rewrite failed, using the original scenario: {exc}\n")
        return ""

    text = " ".join(strip_think_tags(raw).split())
    text = text.removeprefix("SEARCH QUERY:").strip().strip('"')
    return text[:MAX_REWRITE_CHARACTERS]
