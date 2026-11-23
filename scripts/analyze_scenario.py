from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.runtime import ensure_supported_python

ensure_supported_python()

from app.writeups import (
    analyze_scenario,
    build_analysis_client,
    build_embedding_client,
    stream_scenario_analysis,
)
from app.writeups.store import DEFAULT_WRITEUPS_TOP_K


PERSIST_DIRECTORY = REPO_ROOT / "data" / "vectorstore" / "chroma"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reason about a pentest scenario using similar indexed writeups."
    )
    parser.add_argument("scenario", nargs="?", help="Scenario description (stack, endpoint, observed behavior).")
    parser.add_argument("-f", "--file", type=Path, help="Read the scenario from a text file.")
    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_WRITEUPS_TOP_K,
        help=f"Number of similar writeups to retrieve. Default: {DEFAULT_WRITEUPS_TOP_K}.",
    )
    parser.add_argument("--no-stream", action="store_true", help="Wait for the full answer before printing.")
    parser.add_argument("--show-context", action="store_true", help="Print the retrieved reports sent to the model.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    scenario = args.file.read_text(encoding="utf-8") if args.file else args.scenario
    if not scenario or not scenario.strip():
        parser.error("provide the scenario as an argument or with --file")

    embed_client = build_embedding_client()
    generation_client = build_analysis_client()
    embed_client.is_available()
    generation_client.is_available()

    if args.no_stream:
        analysis = analyze_scenario(
            scenario,
            embed_client,
            generation_client,
            persist_directory=PERSIST_DIRECTORY,
            top_k=args.top_k,
        )
        print(analysis.answer)
        reports = analysis.reports
        distances = analysis.distances
        context = analysis.context
    else:
        matches, context, answer_stream = stream_scenario_analysis(
            scenario,
            embed_client,
            generation_client,
            persist_directory=PERSIST_DIRECTORY,
            top_k=args.top_k,
        )
        for chunk in answer_stream:
            print(chunk, end="", flush=True)
        print()
        reports = [report for report, _ in matches]
        distances = [distance for _, distance in matches]

    print("\nSimilar reports used:")
    if not reports:
        print("None. The local writeups index is empty or has no match.")
    for index, (report, distance) in enumerate(zip(reports, distances), start=1):
        print(f"[{index}] {report.get('title')} | {report.get('vuln_class')} | distance={distance:.3f} | {report.get('source_path')}")

    if args.show_context:
        print("\nContext:\n")
        print(context)


if __name__ == "__main__":
    main()
