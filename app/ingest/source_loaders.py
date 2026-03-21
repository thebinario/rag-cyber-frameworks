from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from typing import Callable

from pypdf import PdfReader


class _HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if text:
            self._chunks.append(text)

    def get_text(self) -> str:
        return "\n".join(self._chunks)


def load_markdown(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def load_text_file(path: str | Path) -> str:
    file_path = Path(path)
    for encoding in ("utf-8", "latin-1"):
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return file_path.read_text(encoding="utf-8", errors="replace")


def load_html(path: str | Path) -> str:
    parser = _HTMLTextExtractor()
    parser.feed(load_text_file(path))
    parser.close()
    return parser.get_text()


def load_pdf(path: str | Path) -> str:
    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(page.strip() for page in pages if page.strip())


SOURCE_LOADERS: dict[str, tuple[str, Callable[[str | Path], str]]] = {
    ".html": ("html", load_html),
    ".htm": ("html", load_html),
    ".md": ("markdown", load_markdown),
    ".pdf": ("pdf", load_pdf),
    ".txt": ("text", load_text_file),
}


def get_source_loader(path: str | Path) -> tuple[str, Callable[[str | Path], str]]:
    suffix = Path(path).suffix.lower()
    try:
        return SOURCE_LOADERS[suffix]
    except KeyError as error:
        raise ValueError(f"Unsupported source file type: {suffix}") from error
