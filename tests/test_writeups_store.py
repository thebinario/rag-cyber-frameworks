from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.writeups import index_writeup, normalize_extraction, search_writeups, writeup_is_indexed
from app.writeups.schema import compute_content_hash
from app.writeups.store import (
    NOMIC_DOCUMENT_PREFIX,
    NOMIC_EMBEDDING_FORMAT,
    NOMIC_QUERY_PREFIX,
    PLAIN_EMBEDDING_FORMAT,
    embedding_format,
)


class RecordingEmbedder:
    """Keyword-based fake embedder that records every text it receives."""

    def __init__(self, model: str) -> None:
        self.model = model
        self.texts: list[str] = []

    def embed(self, text: str) -> list[float]:
        self.texts.append(text)
        lowered = text.lower()
        return [
            1.0 if "idor" in lowered or "orderid" in lowered else 0.0,
            1.0 if "xss" in lowered or "script" in lowered else 0.0,
            0.1,
        ]


def make_record(title: str, vuln_class: str, body: str, **fields):
    return normalize_extraction(
        {"title": title, "vuln_class": vuln_class, **fields},
        source_path=f"{body}.md",
        content_hash=compute_content_hash(body),
    )


class EmbeddingFormatTests(unittest.TestCase):
    def test_nomic_models_get_prefixes_and_format(self):
        client = RecordingEmbedder("nomic-embed-text:latest")
        self.assertEqual(embedding_format(client), NOMIC_EMBEDDING_FORMAT)

    def test_other_models_stay_plain(self):
        self.assertEqual(embedding_format(RecordingEmbedder("bge-m3")), PLAIN_EMBEDDING_FORMAT)


class PrefixTests(unittest.TestCase):
    def test_documents_and_queries_carry_nomic_prefixes(self):
        client = RecordingEmbedder("nomic-embed-text")
        with tempfile.TemporaryDirectory() as tmp:
            index_writeup(make_record("IDOR orders", "IDOR", "a"), client, tmp)
            search_writeups("orderId swap", client, tmp, top_k=1)
        self.assertTrue(client.texts[0].startswith(NOMIC_DOCUMENT_PREFIX))
        self.assertTrue(client.texts[1].startswith(NOMIC_QUERY_PREFIX))

    def test_non_nomic_models_get_no_prefix(self):
        client = RecordingEmbedder("bge-m3")
        with tempfile.TemporaryDirectory() as tmp:
            index_writeup(make_record("IDOR orders", "IDOR", "a"), client, tmp)
            search_writeups("orderId swap", client, tmp, top_k=1)
        self.assertFalse(any(text.startswith(("search_document:", "search_query:")) for text in client.texts))


class RefreshOldEntriesTests(unittest.TestCase):
    def test_entry_indexed_with_another_format_is_not_considered_indexed(self):
        plain = RecordingEmbedder("bge-m3")
        nomic = RecordingEmbedder("nomic-embed-text")
        record = make_record("IDOR orders", "IDOR", "a")
        with tempfile.TemporaryDirectory() as tmp:
            index_writeup(record, plain, tmp)
            self.assertTrue(writeup_is_indexed(record.content_hash, tmp))
            self.assertTrue(writeup_is_indexed(record.content_hash, tmp, expected_format=PLAIN_EMBEDDING_FORMAT))
            self.assertFalse(writeup_is_indexed(record.content_hash, tmp, expected_format=NOMIC_EMBEDDING_FORMAT))

            index_writeup(record, nomic, tmp)  # re-index replaces it (same id, upsert)
            self.assertTrue(writeup_is_indexed(record.content_hash, tmp, expected_format=NOMIC_EMBEDDING_FORMAT))

    def test_missing_entry_is_not_indexed(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(writeup_is_indexed("f" * 64, tmp, expected_format=NOMIC_EMBEDDING_FORMAT))


class RankingRegressionTests(unittest.TestCase):
    def test_idor_scenario_ranks_the_idor_report_first(self):
        client = RecordingEmbedder("nomic-embed-text")
        with tempfile.TemporaryDirectory() as tmp:
            index_writeup(make_record("XSS in admin panel", "XSS", "x", root_cause="script injection"), client, tmp)
            index_writeup(make_record("IDOR in orders", "IDOR", "i", entry_point="orderId"), client, tmp)
            results = search_writeups("mutation accepts another user's orderId and returns 200", client, tmp, top_k=2)
        self.assertEqual(results[0][0]["vuln_class"], "IDOR")
        self.assertLess(results[0][1], results[1][1])


if __name__ == "__main__":
    unittest.main()
