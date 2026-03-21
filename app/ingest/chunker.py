from __future__ import annotations

import json
from pathlib import Path

from .models import DocumentChunk, ProcessedDocument


DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200
DEFAULT_MIN_CHUNK_SIZE = DEFAULT_CHUNK_SIZE // 2


def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    min_chunk_size: int = DEFAULT_MIN_CHUNK_SIZE,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    normalized_text = text.strip()
    if not normalized_text:
        return []

    step = chunk_size - chunk_overlap
    raw_chunks: list[str] = []
    start = 0
    text_length = len(normalized_text)

    while start < text_length:
        chunk = normalized_text[start : start + chunk_size].strip()
        if chunk:
            raw_chunks.append(chunk)
        start += step

    if len(raw_chunks) >= 2 and len(raw_chunks[-1]) < min_chunk_size:
        merged_chunk = f"{raw_chunks[-2]}\n\n{raw_chunks[-1]}".strip()
        raw_chunks[-2] = merged_chunk
        raw_chunks.pop()

    return raw_chunks


def build_document_chunks(
    document: ProcessedDocument,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    min_chunk_size: int = DEFAULT_MIN_CHUNK_SIZE,
) -> list[DocumentChunk]:
    chunks = chunk_text(
        document.clean_text,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        min_chunk_size=min_chunk_size,
    )

    return [
        DocumentChunk(
            chunk_id=f"{document.id}-chunk-{chunk_index:04d}",
            document_id=document.id,
            title=document.title,
            framework=document.framework,
            source_type=document.source_type,
            source_path=document.path,
            chunk_index=chunk_index,
            char_count=len(chunk),
            text=chunk,
        )
        for chunk_index, chunk in enumerate(chunks)
    ]


def load_processed_documents(documents_dir: str | Path) -> list[ProcessedDocument]:
    directory = Path(documents_dir)
    documents: list[ProcessedDocument] = []

    for document_path in sorted(directory.glob("*.json")):
        payload = json.loads(document_path.read_text(encoding="utf-8"))
        documents.append(ProcessedDocument(**payload))

    return documents


def write_chunks_jsonl(chunks: list[DocumentChunk], output_path: str | Path) -> None:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("w", encoding="utf-8") as file_handle:
        for chunk in chunks:
            file_handle.write(json.dumps(chunk.to_dict()) + "\n")


def build_chunks(
    documents_dir: str | Path,
    output_path: str | Path,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    min_chunk_size: int = DEFAULT_MIN_CHUNK_SIZE,
) -> tuple[list[DocumentChunk], dict[str, int]]:
    processed_documents = load_processed_documents(documents_dir)

    chunks: list[DocumentChunk] = []
    chunked_documents = 0
    skipped_documents = 0

    for document in processed_documents:
        if document.processing_status != "processed" or not document.clean_text.strip():
            skipped_documents += 1
            continue

        document_chunks = build_document_chunks(
            document,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            min_chunk_size=min_chunk_size,
        )

        if not document_chunks:
            skipped_documents += 1
            continue

        chunks.extend(document_chunks)
        chunked_documents += 1

    write_chunks_jsonl(chunks, output_path)

    summary = {
        "documents_read": len(processed_documents),
        "documents_chunked": chunked_documents,
        "documents_skipped": skipped_documents,
        "chunks_generated": len(chunks),
    }
    return chunks, summary
