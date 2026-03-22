from __future__ import annotations

import re
import unicodedata


_BLANK_LINE_PATTERN = re.compile(r"\n{3,}")
_INLINE_WHITESPACE_PATTERN = re.compile(r"[ \t]+")

_NOWIKI_PATTERN = re.compile(r"<nowiki>(.*?)</nowiki>", re.DOTALL)
_FILE_REF_PATTERN = re.compile(r"\[\[:?File:[^\]]*\]\]")
_WIKI_BOLD_ITALIC = re.compile(r"'{2,5}")
_WIKI_TABLE_BLOCK = re.compile(
    r"^\{\|[^\n]*\n(?:.*?\n)*?\|\}", re.MULTILINE
)
_WIKI_TABLE_ROW_SEP = re.compile(r"^\|\-[^\n]*$", re.MULTILINE)
_WIKI_TABLE_START = re.compile(r"^\{\|[^\n]*$", re.MULTILINE)
_WIKI_TABLE_END = re.compile(r"^\|\}$", re.MULTILINE)
_WIKI_LINK = re.compile(r"\[https?://\S+?\s+([^\]]+)\]")
_WIKI_LINK_BARE = re.compile(r"\[(https?://\S+?)\]")

_HTML_FORMAT_TAGS = re.compile(
    r"</?(?:u|i|b|s|em|strong|br|code|pre|span|div|sub|sup|big|small|center"
    r"|blockquote|ref|references|strike|tt|del|ins|mark|abbr|cite|dfn|kbd"
    r"|samp|var|wbr|nowiki)(?:\s[^>]*)?\s*/?>",
    re.IGNORECASE,
)
_BR_TAG = re.compile(r"<br\s*/?>", re.IGNORECASE)


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


def strip_wiki_markup(text: str) -> str:
    result = text

    result = _NOWIKI_PATTERN.sub(r"\1", result)
    result = _FILE_REF_PATTERN.sub("", result)
    result = _WIKI_LINK.sub(r"\1", result)
    result = _WIKI_LINK_BARE.sub(r"\1", result)
    result = _extract_table_content(result)
    result = _WIKI_BOLD_ITALIC.sub("", result)
    result = _BR_TAG.sub("\n", result)
    result = _HTML_FORMAT_TAGS.sub("", result)

    return result


def _extract_table_content(text: str) -> str:
    lines = text.split("\n")
    output: list[str] = []
    in_table = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("{|"):
            in_table = True
            continue
        if stripped == "|}":
            in_table = False
            continue
        if not in_table:
            output.append(line)
            continue

        if stripped.startswith("|-"):
            continue
        if stripped.startswith("!"):
            cells = stripped.lstrip("!").split("!!")
            content = " | ".join(c.strip() for c in cells if c.strip())
            if content:
                output.append(content)
            continue
        if stripped.startswith("|"):
            cells = stripped.lstrip("|").split("||")
            content = " | ".join(c.strip() for c in cells if c.strip())
            if content:
                output.append(content)
            continue
        if stripped:
            output.append(line)

    return "\n".join(output)


def clean_text(text: str) -> str:
    cleaned = normalize_newlines(text)
    cleaned = remove_control_characters(cleaned)
    cleaned = strip_wiki_markup(cleaned)
    cleaned = normalize_whitespace(cleaned)
    cleaned = collapse_blank_lines(cleaned)
    return cleaned.strip()
