from __future__ import annotations

import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.ingest import clean_text


DOCUMENTS_DIR = REPO_ROOT / "data" / "processed" / "documents"


def update_document(document_path: Path) -> None:
    payload = json.loads(document_path.read_text(encoding="utf-8"))
    payload["clean_text"] = clean_text(payload.get("text", ""))
    document_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    updated_count = 0
    failed_count = 0

    for document_path in sorted(DOCUMENTS_DIR.glob("*.json")):
        try:
            update_document(document_path)
            updated_count += 1
        except Exception as exc:
            failed_count += 1
            print(f"Failed to clean {document_path.name}: {exc}")

    print(f"Updated documents: {updated_count}")
    print(f"Failed documents: {failed_count}")
    print(f"Documents directory: {DOCUMENTS_DIR}")


if __name__ == "__main__":
    main()
