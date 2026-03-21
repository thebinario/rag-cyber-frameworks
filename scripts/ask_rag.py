from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.runtime import ensure_supported_python

ensure_supported_python()

from app.rag import (
    DEFAULT_RETRIEVAL_MODE,
    EXPANDED_RETRIEVAL_MODE,
    run_rag_pipeline,
    stream_rag_answer,
)
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
    parser.add_argument(
        "--no-stream",
        action="store_true",
        help="Disable streaming and wait for the full answer before printing.",
    )
    parser.add_argument(
        "--retrieval-mode",
        choices=[DEFAULT_RETRIEVAL_MODE, EXPANDED_RETRIEVAL_MODE],
        default=DEFAULT_RETRIEVAL_MODE,
        help=f"Retrieval mode to use. Default: {DEFAULT_RETRIEVAL_MODE}.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    print(f"Question: {args.question}")
    print()
    print("Answer:")

    if args.no_stream:
        rag_answer = run_rag_pipeline(
            question=args.question,
            top_k=args.top_k,
            persist_directory=PERSIST_DIRECTORY,
            retrieval_mode=args.retrieval_mode,
        )
        print(rag_answer.answer)
        sources = rag_answer.sources
        context = rag_answer.context
    else:
        sources, context, answer_stream = stream_rag_answer(
            question=args.question,
            top_k=args.top_k,
            persist_directory=PERSIST_DIRECTORY,
            retrieval_mode=args.retrieval_mode,
        )
        answer_parts: list[str] = []
        for chunk in answer_stream:
            answer_parts.append(chunk)
            print(chunk, end="", flush=True)
        print()
        print()
        rag_answer = None

    print("Sources:")

    final_sources = sources if args.no_stream else sources
    if not final_sources:
        print("No sources were retrieved.")
    else:
        for index, source in enumerate(final_sources, start=1):
            print(
                f"[{index}] chunk_id={source.chunk_id} title={source.title} "
                f"framework={source.framework} distance={source.distance}"
            )

    if args.show_context:
        final_context = context if args.no_stream else context
        print()
        print("Context:")
        print()
        print(final_context)


if __name__ == "__main__":
    main()
