from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.runtime import ensure_supported_python

ensure_supported_python()

from app.ingest import process_documents


MANIFEST_PATH = REPO_ROOT / "data" / "processed" / "manifests" / "documents_manifest.json"
OUTPUT_DIR = REPO_ROOT / "data" / "processed" / "documents"


def main() -> None:
    processed_documents = process_documents(MANIFEST_PATH, OUTPUT_DIR, repo_root=REPO_ROOT)
    processed_count = sum(document.processing_status == "processed" for document in processed_documents)
    failed_count = len(processed_documents) - processed_count

    print(f"Processed documents: {processed_count}")
    print(f"Failed documents: {failed_count}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
