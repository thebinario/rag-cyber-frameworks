from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from app.ingest.models import ChunkEmbeddingRecord
from app.ingest.ollama_client import OllamaEmbeddingClient

try:
    import chromadb
    from chromadb.api.models.Collection import Collection
except ImportError:  # pragma: no cover - exercised in runtime environments without Chroma
    chromadb = None
    Collection = Any  # type: ignore[assignment]


DEFAULT_CHROMA_COLLECTION_NAME = "chunk_embeddings"
DEFAULT_CHROMA_PERSIST_DIRECTORY = Path("data") / "vectorstore" / "chroma"
DEFAULT_SEARCH_TOP_K = 5
DEFAULT_RESULT_TEXT_LENGTH = 300


def _require_chromadb() -> Any:
    if chromadb is None:
        raise RuntimeError(
            "chromadb is not installed. Add it to the environment before building or querying the vector index."
        )
    return chromadb


def load_embedding_records(embeddings_path: str | Path) -> list[ChunkEmbeddingRecord]:
    path = Path(embeddings_path)
    records: list[ChunkEmbeddingRecord] = []

    with path.open("r", encoding="utf-8") as file_handle:
        for line in file_handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            records.append(ChunkEmbeddingRecord(**payload))

    return records


def _get_client(persist_directory: str | Path) -> Any:
    chroma_module = _require_chromadb()
    directory = Path(persist_directory)
    directory.mkdir(parents=True, exist_ok=True)
    return chroma_module.PersistentClient(path=str(directory))


def _build_collection_metadata(record: ChunkEmbeddingRecord) -> dict[str, str | int]:
    return {
        "document_id": record.document_id,
        "title": record.title,
        "framework": record.framework,
        "source_type": record.source_type,
        "source_path": record.source_path,
        "chunk_index": record.chunk_index,
        "char_count": record.char_count,
        "embedding_model": record.embedding_model,
    }


def load_vector_collection(
    persist_directory: str | Path,
    collection_name: str = DEFAULT_CHROMA_COLLECTION_NAME,
) -> Collection:
    client = _get_client(persist_directory)
    try:
        return client.get_collection(name=collection_name)
    except Exception as exc:
        raise RuntimeError(
            f"Vector index collection '{collection_name}' was not found in {Path(persist_directory)}."
        ) from exc


def build_vector_index(
    embeddings_path: str | Path,
    persist_directory: str | Path,
    collection_name: str = DEFAULT_CHROMA_COLLECTION_NAME,
) -> dict[str, int | str]:
    records = load_embedding_records(embeddings_path)
    client = _get_client(persist_directory)

    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    valid_records = [record for record in records if record.embedding is not None]
    skipped_records = len(records) - len(valid_records)

    if valid_records:
        collection.add(
            ids=[record.chunk_id for record in valid_records],
            embeddings=[record.embedding for record in valid_records],
            documents=[record.text for record in valid_records],
            metadatas=[_build_collection_metadata(record) for record in valid_records],
        )

    return {
        "records_read": len(records),
        "records_indexed": len(valid_records),
        "records_skipped": skipped_records,
        "collection_name": collection_name,
        "persist_directory": str(Path(persist_directory)),
    }


def search_chunks(
    query: str,
    persist_directory: str | Path,
    top_k: int = DEFAULT_SEARCH_TOP_K,
    collection_name: str = DEFAULT_CHROMA_COLLECTION_NAME,
    base_url: str | None = None,
    model: str | None = None,
) -> list[dict[str, Any]]:
    if not query.strip():
        raise ValueError("query must not be empty")
    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    resolved_base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    resolved_model = model or os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    resolved_timeout = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "10"))

    client = OllamaEmbeddingClient(
        base_url=resolved_base_url,
        model=resolved_model,
        timeout_seconds=resolved_timeout,
    )
    client.is_available()
    query_embedding = client.embed(query)

    collection = load_vector_collection(
        persist_directory=persist_directory,
        collection_name=collection_name,
    )
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    ids = result.get("ids", [[]])[0]
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    search_results: list[dict[str, Any]] = []
    for chunk_id, text, metadata, distance in zip(ids, documents, metadatas, distances):
        search_results.append(
            {
                "chunk_id": chunk_id,
                "distance": distance,
                "text": text,
                "metadata": metadata,
            }
        )

    return search_results
