from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.runtime import ensure_supported_python

ensure_supported_python()

from app.writeups.hackerone import (
    DEFAULT_DELAY_SECONDS,
    DEFAULT_MAX_REPORTS,
    MIN_DELAY_SECONDS,
    fetch_reports,
    parse_report_ref,
    read_report_refs,
)


DEFAULT_OUTPUT_DIRECTORY = REPO_ROOT / "data" / "raw" / "writeups"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download publicly disclosed HackerOne reports as Markdown files for local indexing."
    )
    parser.add_argument("reports", nargs="*", help="Report ids or URLs, e.g. 2119149 or https://hackerone.com/reports/2119149")
    parser.add_argument("-f", "--from-file", type=Path, help="Text file with one report id or URL per line ('#' starts a comment).")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIRECTORY, help=f"Default: {DEFAULT_OUTPUT_DIRECTORY}.")
    parser.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_DELAY_SECONDS,
        help=f"Seconds between requests. Default {DEFAULT_DELAY_SECONDS}; values below {MIN_DELAY_SECONDS} are raised to {MIN_DELAY_SECONDS}.",
    )
    parser.add_argument("--max", type=int, default=DEFAULT_MAX_REPORTS, dest="max_reports", help=f"Max downloads per run. Default {DEFAULT_MAX_REPORTS}.")
    parser.add_argument("--force", action="store_true", help="Download again even if the file already exists.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    ids: list[int] = []
    try:
        for ref in args.reports:
            report_id = parse_report_ref(ref)
            if report_id not in ids:
                ids.append(report_id)
        if args.from_file:
            for report_id in read_report_refs(args.from_file):
                if report_id not in ids:
                    ids.append(report_id)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))

    if not ids:
        parser.error("give at least one report id/URL or --from-file")

    print(f"{len(ids)} report(s) | delay {max(args.delay, MIN_DELAY_SECONDS)}s | output {args.output_dir}")
    summary = fetch_reports(
        ids,
        args.output_dir,
        delay_seconds=args.delay,
        max_reports=args.max_reports,
        force=args.force,
    )

    print(
        f"\nDone. saved={len(summary.saved)} already_had={len(summary.skipped_existing)} "
        f"unavailable={len(summary.unavailable)} failed={len(summary.failed)}"
    )
    if summary.stopped_reason:
        print(f"Stopped early: {summary.stopped_reason}")
    if summary.saved:
        print("Next: python scripts/ingest_writeups.py")


if __name__ == "__main__":
    main()
