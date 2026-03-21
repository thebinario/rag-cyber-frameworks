from __future__ import annotations

import sys


MIN_SUPPORTED_PYTHON = (3, 12)
MAX_SUPPORTED_PYTHON_EXCLUSIVE = (3, 14)
PREFERRED_PYTHON = "3.13"


def ensure_supported_python() -> None:
    current = sys.version_info[:2]
    if MIN_SUPPORTED_PYTHON <= current < MAX_SUPPORTED_PYTHON_EXCLUSIVE:
        return

    current_text = ".".join(str(part) for part in sys.version_info[:3])
    minimum_text = ".".join(str(part) for part in MIN_SUPPORTED_PYTHON)
    maximum_text = ".".join(str(part) for part in MAX_SUPPORTED_PYTHON_EXCLUSIVE)
    raise RuntimeError(
        "Unsupported Python runtime. "
        f"Found Python {current_text}, but this repository requires >= {minimum_text} and < {maximum_text}. "
        f"Use Python {PREFERRED_PYTHON} to create the project virtual environment."
    )
