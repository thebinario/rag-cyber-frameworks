from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.runtime import ensure_supported_python

ensure_supported_python()

from app.rag import run_rag_pipeline
from app.rag.vector_store import DEFAULT_SEARCH_TOP_K


PERSIST_DIRECTORY = REPO_ROOT / "data" / "vectorstore" / "chroma"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local end-to-end RAG pipeline.")
    parser.add_argument("question", help="Question to answer using retrieved context.")
    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_SEARCH_TOP_K,
        help=f"Number of top chunks to retrieve. Default: {DEFAULT_SEARCH_TOP_K}.",
    )
    parser.add_argument(
        "--show-context",
        action="store_true",
        help="Print the formatted retrieved context used to ground the answer.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    rag_answer = run_rag_pipeline(
        question=args.question,
        top_k=args.top_k,
        persist_directory=PERSIST_DIRECTORY,
    )

    print(f"Question: {rag_answer.question}")
    print()
    print("Answer:")
    print(rag_answer.answer)
    print()
    print("Sources:")

    if not rag_answer.sources:
        print("No sources were retrieved.")
    else:
        for index, source in enumerate(rag_answer.sources, start=1):
            print(
                f"[{index}] chunk_id={source.chunk_id} title={source.title} "
                f"framework={source.framework} distance={source.distance}"
            )

    if args.show_context:
        print()
        print("Context:")
        print()
        print(rag_answer.context)


if __name__ == "__main__":
    main()
