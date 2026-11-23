from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.runtime import ensure_supported_python

ensure_supported_python()

from app.writeups import (
    build_embedding_client,
    build_extraction_client,
    compute_content_hash,
    embedding_format,
    discover_writeup_files,
    extract_writeup,
    index_writeup,
    load_writeup_text,
    writeup_is_indexed,
)


DEFAULT_INPUT_DIRECTORY = REPO_ROOT / "data" / "raw" / "writeups"
PROCESSED_DIRECTORY = REPO_ROOT / "data" / "processed" / "writeups"
PERSIST_DIRECTORY = REPO_ROOT / "data" / "vectorstore" / "chroma"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract structured data from security writeups and index them for scenario analysis."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIRECTORY,
        help=f"Folder with writeups (.md, .txt, .html, .pdf). Default: {DEFAULT_INPUT_DIRECTORY}.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-extract and re-index writeups that are already indexed.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    files = discover_writeup_files(args.input_dir)
    if not files:
        print(f"No writeups found in {args.input_dir}. Add .md, .txt, .html or .pdf files there.")
        return

    extraction_client = build_extraction_client()
    embedding_client = build_embedding_client()
    extraction_client.is_available()
    embedding_client.is_available()

    PROCESSED_DIRECTORY.mkdir(parents=True, exist_ok=True)
    print(
        f"{len(files)} files | extraction model: {extraction_client.model} | "
        f"embedding model: {embedding_client.model}"
    )

    indexed = skipped = failed = 0
    for path in files:
        label = path.relative_to(args.input_dir) if path.is_relative_to(args.input_dir) else path
        try:
            text = load_writeup_text(path)
            content_hash = compute_content_hash(text)
            if not args.force and writeup_is_indexed(
                content_hash, PERSIST_DIRECTORY, expected_format=embedding_format(embedding_client)
            ):
                print(f"[skip] already indexed: {label}")
                skipped += 1
                continue

            record = extract_writeup(
                text,
                source_path=str(label),
                client=extraction_client,
                fallback_title=path.stem,
            )
            (PROCESSED_DIRECTORY / f"{record.writeup_id}.json").write_text(
                json.dumps(record.to_dict(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            index_writeup(record, embedding_client, PERSIST_DIRECTORY)
            print(f"[ok]   {label} -> {record.vuln_class or 'unclassified'} | {record.title}")
            indexed += 1
        except Exception as exc:
            print(f"[fail] {label}: {exc}")
            failed += 1

    print(f"\nDone. indexed={indexed} skipped={skipped} failed={failed}")


if __name__ == "__main__":
    main()
