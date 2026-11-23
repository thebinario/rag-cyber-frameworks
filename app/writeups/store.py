from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from app.ingest.ollama_client import OllamaEmbeddingClient
from app.rag.generator import DEFAULT_OLLAMA_BASE_URL
from app.rag.vector_store import DEFAULT_CHROMA_PERSIST_DIRECTORY

from .schema import WriteupRecord

try:
    import chromadb
except ImportError:
    chromadb = None


DEFAULT_WRITEUPS_COLLECTION_NAME = "writeups"
DEFAULT_WRITEUPS_TOP_K = 4
DEFAULT_OLLAMA_EMBED_MODEL = "nomic-embed-text"
DEFAULT_EMBED_TIMEOUT_SECONDS = 60


def build_embedding_client(
    base_url: str | None = None,
    model: str | None = None,
) -> OllamaEmbeddingClient:
    return OllamaEmbeddingClient(
        base_url=base_url or os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_BASE_URL),
        model=model or os.getenv("OLLAMA_EMBED_MODEL", DEFAULT_OLLAMA_EMBED_MODEL),
        timeout_seconds=int(
            os.getenv(
                "OLLAMA_EMBED_TIMEOUT_SECONDS",
                os.getenv("OLLAMA_TIMEOUT_SECONDS", str(DEFAULT_EMBED_TIMEOUT_SECONDS)),
            )
        ),
    )


def _get_collection(
    persist_directory: str | Path,
    collection_name: str,
    create: bool,
) -> Any:
    if chromadb is None:
        raise RuntimeError("chromadb is not installed. Install requirements.txt first.")

    directory = Path(persist_directory)
    directory.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(directory))

    if create:
        return client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
    try:
        return client.get_collection(name=collection_name)
    except Exception as exc:
        raise RuntimeError(
            f"Writeups collection '{collection_name}' was not found in {directory}. "
            "Run scripts/ingest_writeups.py first."
        ) from exc


def writeup_is_indexed(
    content_hash: str,
    persist_directory: str | Path = DEFAULT_CHROMA_PERSIST_DIRECTORY,
    collection_name: str = DEFAULT_WRITEUPS_COLLECTION_NAME,
) -> bool:
    collection = _get_collection(persist_directory, collection_name, create=True)
    return bool(collection.get(ids=[content_hash[:32]])["ids"])


def index_writeup(
    record: WriteupRecord,
    client: OllamaEmbeddingClient,
    persist_directory: str | Path = DEFAULT_CHROMA_PERSIST_DIRECTORY,
    collection_name: str = DEFAULT_WRITEUPS_COLLECTION_NAME,
) -> None:
    embedding = client.embed(record.search_text())
    collection = _get_collection(persist_directory, collection_name, create=True)
    collection.upsert(
        ids=[record.writeup_id],
        embeddings=[embedding],
        documents=[json.dumps(record.to_dict(), ensure_ascii=False)],
        metadatas=[
            {
                "title": record.title,
                "vuln_class": record.vuln_class,
                "severity": record.severity,
                "source_path": record.source_path,
                "embedding_model": client.model,
            }
        ],
    )


def search_writeups(
    query: str,
    client: OllamaEmbeddingClient,
    persist_directory: str | Path = DEFAULT_CHROMA_PERSIST_DIRECTORY,
    top_k: int = DEFAULT_WRITEUPS_TOP_K,
    collection_name: str = DEFAULT_WRITEUPS_COLLECTION_NAME,
) -> list[tuple[dict[str, Any], float]]:
    """Return (writeup_dict, cosine_distance) pairs, closest first."""
    if not query.strip():
        raise ValueError("query must not be empty")
    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    collection = _get_collection(persist_directory, collection_name, create=False)
    if collection.count() == 0:
        return []

    result = collection.query(
        query_embeddings=[client.embed(query)],
        n_results=min(top_k, collection.count()),
    )
    documents = result.get("documents", [[]])[0]
    distances = result.get("distances", [[]])[0]
    return [(json.loads(document), float(distance)) for document, distance in zip(documents, distances)]
