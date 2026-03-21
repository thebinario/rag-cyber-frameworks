from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.rag import build_vector_index


EMBEDDINGS_PATH = REPO_ROOT / "data" / "processed" / "embeddings" / "chunk_embeddings.jsonl"
PERSIST_DIRECTORY = REPO_ROOT / "data" / "vectorstore" / "chroma"


def main() -> None:
    summary = build_vector_index(EMBEDDINGS_PATH, PERSIST_DIRECTORY)
    print(f"Records read: {summary['records_read']}")
    print(f"Records indexed: {summary['records_indexed']}")
    print(f"Records skipped: {summary['records_skipped']}")
    print(f"Collection name: {summary['collection_name']}")
    print(f"Persist directory: {summary['persist_directory']}")


if __name__ == "__main__":
    main()
