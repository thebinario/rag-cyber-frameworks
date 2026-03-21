from __future__ import annotations

import re
import unicodedata


_BLANK_LINE_PATTERN = re.compile(r"\n{3,}")
_INLINE_WHITESPACE_PATTERN = re.compile(r"[ \t]+")


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def remove_control_characters(text: str) -> str:
    filtered_characters: list[str] = []
    for character in text:
        if character in {"\n", "\t"}:
            filtered_characters.append(character)
            continue

        if unicodedata.category(character).startswith("C"):
            continue

        filtered_characters.append(character)

    return "".join(filtered_characters)


def normalize_whitespace(text: str) -> str:
    normalized_lines = []
    for line in text.split("\n"):
        normalized_line = _INLINE_WHITESPACE_PATTERN.sub(" ", line).rstrip()
        normalized_lines.append(normalized_line)
    return "\n".join(normalized_lines)


def collapse_blank_lines(text: str) -> str:
    return _BLANK_LINE_PATTERN.sub("\n\n", text)


def clean_text(text: str) -> str:
    cleaned = normalize_newlines(text)
    cleaned = remove_control_characters(cleaned)
    cleaned = normalize_whitespace(cleaned)
    cleaned = collapse_blank_lines(cleaned)
    return cleaned.strip()
