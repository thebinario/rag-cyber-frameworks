from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .loader import load_documents_manifest
from .models import DocumentMetadata, ProcessedDocument
from .source_loaders import get_source_loader


def build_processed_document(
    document: DocumentMetadata,
    repo_root: Path,
    output_dir: Path,
) -> ProcessedDocument:
    source_path = repo_root / Path(document.path)
    output_path = output_dir / f"{document.id}.json"
    processed_at = datetime.now(timezone.utc).isoformat()

    try:
        loader_type, loader = get_source_loader(source_path)
        text = loader(source_path)
        processing_status = "processed"
        error = None
    except Exception as exc:
        loader_type = source_path.suffix.lower().lstrip(".") or "unknown"
        text = ""
        processing_status = "failed"
        error = str(exc)

    return ProcessedDocument(
        id=document.id,
        title=document.title,
        framework=document.framework,
        source_type=document.source_type,
        language=document.language,
        path=document.path,
        origin=document.origin,
        ingestion_status=document.ingestion_status,
        processing_status=processing_status,
        loader_type=loader_type,
        text=text,
        error=error,
        processed_at=processed_at,
        output_path=output_path.relative_to(repo_root).as_posix(),
    )


def write_processed_document(processed_document: ProcessedDocument, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{processed_document.id}.json"
    output_path.write_text(
        json.dumps(processed_document.to_dict(), indent=2) + "\n",
        encoding="utf-8",
    )


def process_documents(
    manifest_path: str | Path,
    output_dir: str | Path,
    repo_root: str | Path | None = None,
) -> list[ProcessedDocument]:
    manifest_file = Path(manifest_path)
    root = Path(repo_root) if repo_root is not None else manifest_file.resolve().parents[3]
    destination = Path(output_dir)
    if not destination.is_absolute():
        destination = root / destination

    manifest = load_documents_manifest(manifest_file)
    processed_documents: list[ProcessedDocument] = []

    for document in manifest.documents:
        processed_document = build_processed_document(document, root, destination)
        write_processed_document(processed_document, destination)
        processed_documents.append(processed_document)

    return processed_documents
