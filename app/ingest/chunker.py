from __future__ import annotations

import json
import re
from pathlib import Path

from .models import DocumentChunk, ProcessedDocument


DEFAULT_CHUNK_SIZE = 1200
DEFAULT_MIN_CHUNK_SIZE = 200
DEFAULT_MAX_CHUNK_SIZE = 2000

# Heading pattern: wiki-style (= Title =, == Sub ==, etc.) or markdown (# Title, ## Sub)
_HEADING_PATTERN = re.compile(
    r"^(?:={1,6})\s+.+?\s+(?:={1,6})$|^#{1,6}\s+.+$",
    re.MULTILINE,
)

# Sentence boundary for splitting long paragraphs
_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def _split_into_sections(text: str) -> list[tuple[str, str]]:
    """Split text into (heading, body) pairs based on heading markers.

    Returns a list of tuples where heading may be empty for the preamble
    (text before the first heading).
    """
    matches = list(_HEADING_PATTERN.finditer(text))

    if not matches:
        return [("", text.strip())]

    sections: list[tuple[str, str]] = []

    # Preamble before first heading
    preamble = text[: matches[0].start()].strip()
    if preamble:
        sections.append(("", preamble))

    for i, match in enumerate(matches):
        heading = match.group(0).strip()
        body_start = match.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip()
        sections.append((heading, body))

    return sections


def _split_paragraphs(text: str) -> list[str]:
    """Split text on double newlines into paragraphs."""
    parts = re.split(r"\n{2,}", text)
    return [p.strip() for p in parts if p.strip()]


def _split_at_sentences(text: str, max_size: int) -> list[str]:
    """Split a long text at sentence boundaries to fit max_size.

    Falls back to line boundaries if sentence splitting is not effective
    (e.g. command-line help text with no sentence-ending punctuation).
    """
    sentences = _SENTENCE_BOUNDARY.split(text)

    # If sentence split didn't help (single block), try splitting by lines
    if len(sentences) <= 1 and len(text) > max_size:
        sentences = [line for line in text.split("\n") if line.strip()]

    chunks: list[str] = []
    current = ""

    for part in sentences:
        sep = "\n" if "\n" in text and len(sentences) > 2 else " "
        candidate = f"{current}{sep}{part}".strip() if current else part
        if len(candidate) <= max_size:
            current = candidate
        else:
            if current:
                chunks.append(current)
            # If a single part still exceeds max_size, force-split it
            if len(part) > max_size:
                for i in range(0, len(part), max_size):
                    chunks.append(part[i : i + max_size].strip())
                current = ""
            else:
                current = part

    if current:
        chunks.append(current)

    return chunks


def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    min_chunk_size: int = DEFAULT_MIN_CHUNK_SIZE,
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
) -> list[str]:
    """Split text into semantically coherent chunks.

    Strategy:
    1. Split on headings (==/##) into sections
    2. Within each section, split on paragraphs (double newline)
    3. Accumulate paragraphs into chunks up to chunk_size
    4. If a single paragraph exceeds max_chunk_size, split at sentence boundaries
    5. Prepend heading context to each chunk for better embedding quality
    6. Merge small trailing chunks into the previous one
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    normalized_text = text.strip()
    if not normalized_text:
        return []

    sections = _split_into_sections(normalized_text)
    raw_chunks: list[str] = []

    for heading, body in sections:
        if not body and not heading:
            continue

        heading_prefix = f"{heading}\n\n" if heading else ""
        heading_len = len(heading_prefix)

        paragraphs = _split_paragraphs(body)
        if not paragraphs:
            if heading:
                raw_chunks.append(heading)
            continue

        current_parts: list[str] = []
        current_len = heading_len

        for paragraph in paragraphs:
            para_len = len(paragraph)

            # If a single paragraph is too large, split at sentences
            if para_len > max_chunk_size - heading_len:
                # Flush current accumulator first
                if current_parts:
                    raw_chunks.append(heading_prefix + "\n\n".join(current_parts))
                    current_parts = []
                    current_len = heading_len

                sentence_chunks = _split_at_sentences(paragraph, max_chunk_size - heading_len)
                for sc in sentence_chunks:
                    raw_chunks.append(heading_prefix + sc)
                continue

            # Check if adding this paragraph would exceed chunk_size
            separator_len = 2 if current_parts else 0  # \n\n between parts
            if current_len + separator_len + para_len > chunk_size and current_parts:
                raw_chunks.append(heading_prefix + "\n\n".join(current_parts))
                current_parts = []
                current_len = heading_len

            current_parts.append(paragraph)
            current_len += (2 if len(current_parts) > 1 else 0) + para_len

        if current_parts:
            raw_chunks.append(heading_prefix + "\n\n".join(current_parts))

    # Merge small trailing chunks into previous
    if len(raw_chunks) >= 2 and len(raw_chunks[-1]) < min_chunk_size:
        raw_chunks[-2] = f"{raw_chunks[-2]}\n\n{raw_chunks[-1]}".strip()
        raw_chunks.pop()

    # Filter out empty chunks
    return [c for c in raw_chunks if c.strip()]


def build_document_chunks(
    document: ProcessedDocument,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    min_chunk_size: int = DEFAULT_MIN_CHUNK_SIZE,
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
) -> list[DocumentChunk]:
    chunks = chunk_text(
        document.clean_text,
        chunk_size=chunk_size,
        min_chunk_size=min_chunk_size,
        max_chunk_size=max_chunk_size,
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
    min_chunk_size: int = DEFAULT_MIN_CHUNK_SIZE,
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
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
            min_chunk_size=min_chunk_size,
            max_chunk_size=max_chunk_size,
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
