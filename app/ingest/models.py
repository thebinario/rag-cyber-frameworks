from __future__ import annotations

from dataclasses import asdict, dataclass


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


@dataclass(frozen=True)
class ProcessedDocument:
    id: str
    title: str
    framework: str
    source_type: str
    language: str
    path: str
    origin: str
    ingestion_status: str
    processing_status: str
    loader_type: str
    text: str
    error: str | None
    processed_at: str
    output_path: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
