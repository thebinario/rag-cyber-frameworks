from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.runtime import ensure_supported_python

ensure_supported_python()

from app.ingest import build_chunks


DOCUMENTS_DIR = REPO_ROOT / "data" / "processed" / "documents"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "chunks" / "chunks.jsonl"


def main() -> None:
    _, summary = build_chunks(DOCUMENTS_DIR, OUTPUT_PATH)
    print(f"Documents read: {summary['documents_read']}")
    print(f"Documents chunked: {summary['documents_chunked']}")
    print(f"Documents skipped: {summary['documents_skipped']}")
    print(f"Chunks generated: {summary['chunks_generated']}")
    print(f"Output file: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
