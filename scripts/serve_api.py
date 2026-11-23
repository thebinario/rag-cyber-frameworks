from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.runtime import ensure_supported_python

ensure_supported_python()

from app.writeups.api import build_default_analyze_function, create_server


PERSIST_DIRECTORY = REPO_ROOT / "data" / "vectorstore" / "chroma"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Serve the scenario analysis as a local HTTP API.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address. Default: 127.0.0.1 (local only).")
    parser.add_argument("--port", type=int, default=8765, help="Port. Default: 8765.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    token = os.getenv("WRITEUPS_API_TOKEN") or None

    try:
        server = create_server(
            build_default_analyze_function(PERSIST_DIRECTORY),
            host=args.host,
            port=args.port,
            token=token,
        )
    except ValueError as exc:
        raise SystemExit(f"error: {exc}. Set WRITEUPS_API_TOKEN or bind to 127.0.0.1.")

    auth = "bearer token required" if token else "no auth (loopback only)"
    print(f"Serving on http://{args.host}:{args.port}  [{auth}]  POST /analyze | GET /health")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
