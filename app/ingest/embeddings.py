from __future__ import annotations

import json
import os
from pathlib import Path

from .models import ChunkEmbeddingRecord, DocumentChunk
from .ollama_client import OllamaEmbeddingClient


DEFAULT_OLLAMA_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_OLLAMA_EMBED_MODEL = "nomic-embed-text"
DEFAULT_OLLAMA_TIMEOUT_SECONDS = 10


def load_chunks(chunks_path: str | Path) -> list[DocumentChunk]:
    path = Path(chunks_path)
    chunks: list[DocumentChunk] = []

    with path.open("r", encoding="utf-8") as file_handle:
        for line in file_handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            chunks.append(DocumentChunk(**payload))

    return chunks


def build_embedding_record(
    chunk: DocumentChunk,
    client: OllamaEmbeddingClient,
    service_error: str | None = None,
) -> ChunkEmbeddingRecord:
    if service_error is not None:
        embedding = None
        error_message = service_error
    else:
        try:
            embedding = client.embed(chunk.text)
            error_message = None
        except Exception as exc:
            embedding = None
            error_message = str(exc)

    return ChunkEmbeddingRecord(
        chunk_id=chunk.chunk_id,
        document_id=chunk.document_id,
        title=chunk.title,
        framework=chunk.framework,
        source_type=chunk.source_type,
        source_path=chunk.source_path,
        chunk_index=chunk.chunk_index,
        char_count=chunk.char_count,
        text=chunk.text,
        embedding_model=client.model,
        embedding=embedding,
        error=error_message,
    )


def write_embedding_records(records: list[ChunkEmbeddingRecord], output_path: str | Path) -> None:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("w", encoding="utf-8") as file_handle:
        for record in records:
            file_handle.write(json.dumps(record.to_dict()) + "\n")


def build_embeddings(
    chunks_path: str | Path,
    output_path: str | Path,
    base_url: str | None = None,
    model: str | None = None,
) -> tuple[list[ChunkEmbeddingRecord], dict[str, int | str]]:
    resolved_base_url = base_url or os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_BASE_URL)
    resolved_model = model or os.getenv("OLLAMA_EMBED_MODEL", DEFAULT_OLLAMA_EMBED_MODEL)
    resolved_timeout = int(
        os.getenv("OLLAMA_TIMEOUT_SECONDS", str(DEFAULT_OLLAMA_TIMEOUT_SECONDS))
    )
    client = OllamaEmbeddingClient(
        base_url=resolved_base_url,
        model=resolved_model,
        timeout_seconds=resolved_timeout,
    )

    chunks = load_chunks(chunks_path)
    service_error: str | None = None

    try:
        client.is_available()
    except Exception as exc:
        service_error = str(exc)

    records = [build_embedding_record(chunk, client, service_error=service_error) for chunk in chunks]
    write_embedding_records(records, output_path)

    success_count = sum(record.embedding is not None for record in records)
    failure_count = len(records) - success_count
    summary: dict[str, int | str] = {
        "chunks_read": len(chunks),
        "embeddings_generated": success_count,
        "chunks_failed": failure_count,
        "embedding_model": resolved_model,
        "base_url": resolved_base_url,
    }
    return records, summary
