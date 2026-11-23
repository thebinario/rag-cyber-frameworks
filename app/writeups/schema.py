from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field


ALLOWED_SEVERITIES = ("low", "medium", "high", "critical")
UNKNOWN_SEVERITY = "unknown"

MAX_FIELD_CHARACTERS = 1200
MAX_LIST_ITEMS = 12


@dataclass(frozen=True)
class WriteupRecord:
    """Structured, normalized view of one security writeup/report."""

    writeup_id: str
    title: str
    vuln_class: str
    stack: list[str]
    entry_point: str
    root_cause: str
    technique: str
    bypass_notes: str
    impact: str
    severity: str
    tags: list[str]
    source_path: str
    content_hash: str
    extraction_model: str = ""
    extra: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def search_text(self) -> str:
        """Text that is embedded for retrieval. Structured fields only, no raw body."""
        parts = [
            self.title,
            self.vuln_class,
            " ".join(self.stack),
            self.entry_point,
            self.root_cause,
            self.technique,
            self.bypass_notes,
            " ".join(self.tags),
        ]
        return "\n".join(part for part in parts if part.strip())


def compute_content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _clean_str(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        value = "; ".join(str(item) for item in value)
    text = " ".join(str(value).split())
    return text[:MAX_FIELD_CHARACTERS]


def _clean_str_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        value = [part for part in value.replace(";", ",").split(",")]
    if not isinstance(value, (list, tuple)):
        return []

    cleaned: list[str] = []
    seen: set[str] = set()
    for item in value:
        text = _clean_str(item)
        key = text.lower()
        if not text or key in seen:
            continue
        seen.add(key)
        cleaned.append(text)
        if len(cleaned) >= MAX_LIST_ITEMS:
            break
    return cleaned


def normalize_severity(value: object) -> str:
    text = _clean_str(value).lower()
    return text if text in ALLOWED_SEVERITIES else UNKNOWN_SEVERITY


def normalize_extraction(
    payload: dict[str, object],
    *,
    source_path: str,
    content_hash: str,
    extraction_model: str = "",
    fallback_title: str = "",
) -> WriteupRecord:
    """Turn raw model output into a WriteupRecord. Missing fields become empty, never invented."""
    title = _clean_str(payload.get("title")) or fallback_title
    vuln_class = _clean_str(payload.get("vuln_class"))

    if not (title or vuln_class):
        raise ValueError("extraction has neither a title nor a vulnerability class")

    return WriteupRecord(
        writeup_id=content_hash[:32],
        title=title,
        vuln_class=vuln_class,
        stack=_clean_str_list(payload.get("stack")),
        entry_point=_clean_str(payload.get("entry_point")),
        root_cause=_clean_str(payload.get("root_cause")),
        technique=_clean_str(payload.get("technique")),
        bypass_notes=_clean_str(payload.get("bypass_notes")),
        impact=_clean_str(payload.get("impact")),
        severity=normalize_severity(payload.get("severity")),
        tags=_clean_str_list(payload.get("tags")),
        source_path=source_path,
        content_hash=content_hash,
        extraction_model=extraction_model,
    )
