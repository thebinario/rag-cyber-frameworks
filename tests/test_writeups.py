from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.writeups import analyzer, extractor
from app.writeups.schema import (
    UNKNOWN_SEVERITY,
    compute_content_hash,
    normalize_extraction,
)


class FakeGenerationClient:
    model = "fake-model"

    def __init__(self, reply: str) -> None:
        self.reply = reply
        self.calls: list[dict[str, object]] = []

    def generate(self, prompt, options=None, response_format=None):
        self.calls.append({"prompt": prompt, "options": options, "response_format": response_format})
        return self.reply

    def generate_stream(self, prompt, options=None):
        yield self.reply


class ParseJsonObjectTests(unittest.TestCase):
    def test_plain_json(self):
        self.assertEqual(extractor.parse_json_object('{"a": 1}'), {"a": 1})

    def test_code_fence_and_think_tags(self):
        raw = '<think>hmm</think>\n```json\n{"title": "x"}\n```'
        self.assertEqual(extractor.parse_json_object(raw), {"title": "x"})

    def test_json_surrounded_by_text(self):
        self.assertEqual(extractor.parse_json_object('Here: {"a": "b"} done'), {"a": "b"})

    def test_rejects_non_json(self):
        with self.assertRaises(ValueError):
            extractor.parse_json_object("no json at all")

    def test_rejects_non_object(self):
        with self.assertRaises(ValueError):
            extractor.parse_json_object("[1, 2, 3]")


class NormalizeExtractionTests(unittest.TestCase):
    def _normalize(self, payload):
        return normalize_extraction(payload, source_path="a.md", content_hash=compute_content_hash("body"))

    def test_fills_missing_fields_without_inventing(self):
        record = self._normalize({"title": "IDOR in orders"})
        self.assertEqual(record.vuln_class, "")
        self.assertEqual(record.stack, [])
        self.assertEqual(record.severity, UNKNOWN_SEVERITY)

    def test_invalid_severity_becomes_unknown(self):
        self.assertEqual(self._normalize({"title": "t", "severity": "catastrophic"}).severity, UNKNOWN_SEVERITY)

    def test_severity_is_case_insensitive(self):
        self.assertEqual(self._normalize({"title": "t", "severity": "HIGH"}).severity, "high")

    def test_lists_are_deduplicated_and_accept_strings(self):
        record = self._normalize({"title": "t", "stack": "Node, node, GraphQL", "tags": ["a", "A", "b"]})
        self.assertEqual(record.stack, ["Node", "GraphQL"])
        self.assertEqual(record.tags, ["a", "b"])

    def test_requires_title_or_class(self):
        with self.assertRaises(ValueError):
            self._normalize({"impact": "something"})

    def test_fallback_title_is_used(self):
        record = normalize_extraction(
            {"vuln_class": "XSS"}, source_path="a.md", content_hash="a" * 64, fallback_title="file-name"
        )
        self.assertEqual(record.title, "file-name")

    def test_search_text_uses_structured_fields(self):
        record = self._normalize({"title": "T", "vuln_class": "SSRF", "root_cause": "no allowlist"})
        self.assertIn("SSRF", record.search_text())
        self.assertIn("no allowlist", record.search_text())


class ExtractWriteupTests(unittest.TestCase):
    def test_extract_uses_json_format_and_zero_temperature(self):
        client = FakeGenerationClient('{"title": "SQLi in search", "vuln_class": "SQL Injection"}')
        record = extractor.extract_writeup("some writeup body", source_path="w.md", client=client)

        self.assertEqual(record.vuln_class, "SQL Injection")
        self.assertEqual(record.extraction_model, "fake-model")
        self.assertEqual(client.calls[0]["response_format"], "json")
        self.assertEqual(client.calls[0]["options"]["temperature"], 0)

    def test_empty_writeup_is_rejected(self):
        with self.assertRaises(ValueError):
            extractor.extract_writeup("   ", source_path="w.md", client=FakeGenerationClient("{}"))

    def test_long_text_is_truncated_to_head_and_tail(self):
        text = "A" * 50000
        prepared = extractor.prepare_writeup_text(text)
        self.assertLess(len(prepared), 13000)
        self.assertIn("[...truncated...]", prepared)

    def test_discover_only_supported_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("x")
            (root / "b.pdf").write_bytes(b"")
            (root / "c.exe").write_text("x")
            (root / "sub").mkdir()
            (root / "sub" / "d.txt").write_text("x")
            names = [path.name for path in extractor.discover_writeup_files(root)]
        self.assertEqual(names, ["a.md", "b.pdf", "d.txt"])

    def test_discover_missing_directory_returns_empty(self):
        self.assertEqual(extractor.discover_writeup_files("/nonexistent/path"), [])


class AnalyzerTests(unittest.TestCase):
    REPORT = {
        "title": "IDOR in orders API",
        "vuln_class": "IDOR",
        "stack": ["Node", "GraphQL"],
        "severity": "high",
        "entry_point": "orderId",
        "root_cause": "missing ownership check",
        "technique": "swap the id",
        "bypass_notes": "",
        "impact": "read other users orders",
        "source_path": "idor.md",
    }

    def test_context_without_reports_is_explicit(self):
        self.assertEqual(analyzer.format_reports_context([]), analyzer.NO_REPORTS_NOTICE)

    def test_context_lists_report_fields(self):
        context = analyzer.format_reports_context([(self.REPORT, 0.123)])
        self.assertIn("IDOR in orders API", context)
        self.assertIn("missing ownership check", context)
        self.assertIn("0.123", context)

    def test_prompt_contains_scenario_reports_and_safety_rules(self):
        prompt = analyzer.build_analysis_prompt("GraphQL mutation returns 200", "REPORTS-HERE")
        self.assertIn("GraphQL mutation returns 200", prompt)
        self.assertIn("REPORTS-HERE", prompt)
        self.assertIn("non-destructive", prompt)

    def test_analyze_scenario_wires_retrieval_and_generation(self):
        generation = FakeGenerationClient("<think>x</think>Final analysis")
        with mock.patch.object(analyzer, "search_writeups", return_value=[(self.REPORT, 0.2)]) as search:
            result = analyzer.analyze_scenario("scenario text", embed_client=mock.Mock(), generation_client=generation, top_k=3)

        self.assertEqual(search.call_args.kwargs["top_k"], 3)
        self.assertEqual(result.answer, "Final analysis")
        self.assertEqual(result.reports[0]["title"], "IDOR in orders API")
        self.assertIn("IDOR in orders API", generation.calls[0]["prompt"])

    def test_empty_scenario_is_rejected(self):
        with self.assertRaises(ValueError):
            analyzer.analyze_scenario("  ", embed_client=mock.Mock(), generation_client=FakeGenerationClient(""))

    def test_record_roundtrips_through_json(self):
        record = normalize_extraction({"title": "t"}, source_path="a.md", content_hash="b" * 64)
        self.assertEqual(json.loads(json.dumps(record.to_dict()))["title"], "t")


if __name__ == "__main__":
    unittest.main()
