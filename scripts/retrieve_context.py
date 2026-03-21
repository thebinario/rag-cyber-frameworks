from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.runtime import ensure_supported_python

ensure_supported_python()

from app.rag import format_retrieval_context, retrieve_chunks
from app.rag.vector_store import DEFAULT_SEARCH_TOP_K


PERSIST_DIRECTORY = REPO_ROOT / "data" / "vectorstore" / "chroma"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Retrieve semantic context from the local vector index.")
    parser.add_argument("query", help="Semantic query to retrieve context for.")
    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_SEARCH_TOP_K,
        help=f"Number of top results to return. Default: {DEFAULT_SEARCH_TOP_K}.",
    )
    parser.add_argument(
        "--show-context",
        action="store_true",
        help="Print the formatted retrieval context after the structured results.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    results = retrieve_chunks(
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
        print()
        print(f"[{index}] chunk_id={result.chunk_id} distance={result.distance}")
        print(f"document_id={result.document_id} title={result.title} framework={result.framework}")
        print(
            f"source_type={result.source_type} source_path={result.source_path} chunk_index={result.chunk_index}"
        )
        print(f"text={result.text}")

    if args.show_context:
        print()
        print("Formatted context:")
        print()
        print(format_retrieval_context(results))


if __name__ == "__main__":
    main()
