from __future__ import annotations

import json
from pathlib import Path

from .models import DocumentMetadata, DocumentsManifest


def load_documents_manifest(manifest_path: str | Path) -> DocumentsManifest:
    path = Path(manifest_path)
    payload = json.loads(path.read_text(encoding="utf-8"))

    required_fields = {"generated_at", "document_count", "documents"}
    missing_fields = required_fields - payload.keys()
    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ValueError(f"Manifest is missing required fields: {missing}")

    documents = [DocumentMetadata(**document) for document in payload["documents"]]
    document_count = payload["document_count"]

    if document_count != len(documents):
        raise ValueError(
            "Manifest document_count does not match the number of document entries"
        )

    return DocumentsManifest(
        generated_at=payload["generated_at"],
        document_count=document_count,
        documents=documents,
    )
