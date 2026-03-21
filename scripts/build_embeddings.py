from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.ingest import build_embeddings


CHUNKS_PATH = REPO_ROOT / "data" / "processed" / "chunks" / "chunks.jsonl"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "embeddings" / "chunk_embeddings.jsonl"


def main() -> None:
    _, summary = build_embeddings(CHUNKS_PATH, OUTPUT_PATH)
    print(f"Chunks read: {summary['chunks_read']}")
    print(f"Embeddings generated: {summary['embeddings_generated']}")
    print(f"Chunks failed: {summary['chunks_failed']}")
    print(f"Embedding model: {summary['embedding_model']}")
    print(f"Ollama base URL: {summary['base_url']}")
    print(f"Output file: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
