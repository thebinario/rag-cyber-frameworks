from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.runtime import ensure_supported_python

ensure_supported_python()

RAW_DATA_DIR = REPO_ROOT / "data" / "raw"
MANIFEST_PATH = REPO_ROOT / "data" / "processed" / "manifests" / "documents_manifest.json"

SUPPORTED_EXTENSIONS = {
    ".htm": "html",
    ".html": "html",
    ".md": "markdown",
    ".pdf": "pdf",
    ".txt": "text",
}

FRAMEWORK_ORIGINS = {
    "ptes": "https://www.pentest-standard.org/",
    "osstmm": "https://www.isecom.org/OSSTMM.3.pdf",
    "nist": "https://csrc.nist.gov/publications/",
}

DEFAULT_LANGUAGE = "en"
DEFAULT_INGESTION_STATUS = "discovered"


@dataclass(frozen=True)
class DocumentMetadata:
    id: str
    title: str
    framework: str
    source_type: str
    language: str
    path: str
    origin: str
    ingestion_status: str


def slugify(value: str) -> str:
    normalized = value.strip().lower().replace("&", " and ")
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    return normalized.strip("-")


def iter_document_paths(raw_data_dir: Path) -> Iterable[Path]:
    for path in sorted(raw_data_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield path


def build_document_metadata(path: Path) -> DocumentMetadata:
    relative_path = path.relative_to(REPO_ROOT)
    framework = relative_path.parts[2]
    source_type = SUPPORTED_EXTENSIONS[path.suffix.lower()]
    title = path.stem.strip()
    document_id = slugify(f"{framework}-{title}")

    return DocumentMetadata(
        id=document_id,
        title=title,
        framework=framework,
        source_type=source_type,
        language=DEFAULT_LANGUAGE,
        path=relative_path.as_posix(),
        origin=FRAMEWORK_ORIGINS.get(framework, ""),
        ingestion_status=DEFAULT_INGESTION_STATUS,
    )


def build_manifest() -> dict[str, object]:
    documents = [asdict(build_document_metadata(path)) for path in iter_document_paths(RAW_DATA_DIR)]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "document_count": len(documents),
        "documents": documents,
    }


def write_manifest(manifest: dict[str, object], manifest_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    manifest = build_manifest()
    write_manifest(manifest, MANIFEST_PATH)
    print(f"Wrote manifest with {manifest['document_count']} documents to {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
