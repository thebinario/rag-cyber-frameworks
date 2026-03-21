from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentMetadata:
    id: str
    title: str
    framework: str
    source_type: str
    language: str
    path: str
    origin: str
    ingestion_status: str


@dataclass(frozen=True)
class DocumentsManifest:
    generated_at: str
    document_count: int
    documents: list[DocumentMetadata]
