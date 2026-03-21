from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.rag.vector_store import (
    DEFAULT_RESULT_TEXT_LENGTH,
    DEFAULT_SEARCH_TOP_K,
    search_chunks,
)


PERSIST_DIRECTORY = REPO_ROOT / "data" / "vectorstore" / "chroma"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search semantic chunks from the local vector index.")
    parser.add_argument("query", help="Semantic query to run against the indexed chunks.")
    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_SEARCH_TOP_K,
        help=f"Number of top results to return. Default: {DEFAULT_SEARCH_TOP_K}.",
    )
    return parser


def _truncate_text(text: str, max_length: int = DEFAULT_RESULT_TEXT_LENGTH) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= max_length:
        return normalized
    return normalized[: max_length - 3].rstrip() + "..."


def main() -> None:
    args = build_parser().parse_args()
    results = search_chunks(
        query=args.query,
        top_k=args.top_k,
        persist_directory=PERSIST_DIRECTORY,
    )

    print(f"Query: {args.query}")
    print(f"Top-k: {args.top_k}")
    print(f"Persist directory: {PERSIST_DIRECTORY}")

    if not results:
        print("No results found.")
        return

    for index, result in enumerate(results, start=1):
        metadata = result["metadata"]
        print()
        print(f"[{index}] chunk_id={result['chunk_id']} distance={result['distance']}")
        print(f"title={metadata['title']} framework={metadata['framework']} document_id={metadata['document_id']}")
        print(
            "source_type="
            f"{metadata['source_type']} source_path={metadata['source_path']} chunk_index={metadata['chunk_index']}"
        )
        print(f"text={_truncate_text(result['text'])}")


if __name__ == "__main__":
    main()
