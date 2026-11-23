from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from urllib import error

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.writeups import hackerone as h1


def sample_report(**overrides):
    data = {
        "title": "Evernote(WindowsApp) XSS to RCE",
        "vulnerability_information": "## Summary\nXSS in note import.\n\n## Impact\nCommand execution.",
        "weakness": {"name": "Code Injection"},
        "severity_rating": "high",
        "readable_substate": "Resolved",
        "disclosed_at": "2026-11-21T17:00:03.537Z",
        "team": {"handle": "evernote", "profile": {"name": "Evernote"}},
        "reporter": {"username": "someone"},
    }
    data.update(overrides)
    return data


class FakeResponse:
    def __init__(self, payload):
        self._raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")

    def read(self):
        return self._raw

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def http_error(code):
    return error.HTTPError("https://hackerone.com/x", code, "err", {}, io.BytesIO(b""))


class FakeServer:
    """Callable opener: maps report id -> payload or an exception to raise."""

    def __init__(self, responses):
        self.responses = responses
        self.requested = []

    def __call__(self, http_request, timeout):
        report_id = int(http_request.full_url.rsplit("/", 1)[1].removesuffix(".json"))
        self.requested.append(report_id)
        outcome = self.responses[report_id]
        if isinstance(outcome, Exception):
            raise outcome
        return FakeResponse(outcome)


class ParseRefTests(unittest.TestCase):
    def test_accepts_ids_and_urls(self):
        for text in ("2119149", " 2119149 ", "https://hackerone.com/reports/2119149", "https://hackerone.com/reports/2119149/", "https://hackerone.com/reports/2119149.json", "https://hackerone.com/reports/2119149?x=1#a"):
            with self.subTest(text=text):
                self.assertEqual(h1.parse_report_ref(text), 2119149)

    def test_rejects_other_input(self):
        for text in ("", "abc", "https://evil.example/reports/1", "https://hackerone.com/hacktivity", "12345678901"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                h1.parse_report_ref(text)

    def test_read_refs_file_ignores_comments_and_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ids.txt"
            path.write_text("# my list\n2119149\n\nhttps://hackerone.com/reports/4175245  # xss\n2119149\n", encoding="utf-8")
            self.assertEqual(h1.read_report_refs(path), [2119149, 4175245])


class MarkdownTests(unittest.TestCase):
    def test_markdown_has_source_metadata_and_body(self):
        text = h1.report_to_markdown(2119149, sample_report())
        self.assertTrue(text.startswith("# Evernote(WindowsApp) XSS to RCE"))
        self.assertIn("- **Source:** https://hackerone.com/reports/2119149", text)
        self.assertIn("- **Program:** Evernote", text)
        self.assertIn("- **Weakness:** Code Injection", text)
        self.assertIn("- **Severity:** high", text)
        self.assertIn("## Summary\nXSS in note import.", text)

    def test_reporter_name_is_not_copied(self):
        self.assertNotIn("someone", h1.report_to_markdown(1, sample_report()))

    def test_missing_optional_fields_are_left_out(self):
        text = h1.report_to_markdown(1, sample_report(weakness=None, team=None, severity_rating=None))
        self.assertNotIn("**Weakness:**", text)
        self.assertNotIn("**Program:**", text)

    def test_undisclosed_or_empty_reports_are_refused(self):
        with self.assertRaises(h1.ReportUnavailable):
            h1.report_to_markdown(1, sample_report(disclosed_at=None))
        with self.assertRaises(h1.ReportUnavailable):
            h1.report_to_markdown(1, sample_report(vulnerability_information="  "))


class FetchJsonTests(unittest.TestCase):
    def test_request_is_anonymous_and_identifies_itself(self):
        seen = []

        def opener(http_request, timeout):
            seen.append(http_request)
            return FakeResponse(sample_report())

        h1.fetch_report_json(2119149, opener=opener)
        self.assertEqual(seen[0].full_url, "https://hackerone.com/reports/2119149.json")
        headers = {k.lower(): v for k, v in seen[0].header_items()}
        self.assertIn("rag-cyber-frameworks", headers["user-agent"])
        self.assertNotIn("authorization", headers)
        self.assertNotIn("cookie", headers)

    def test_status_mapping(self):
        for code, expected in ((404, h1.ReportUnavailable), (403, h1.ReportUnavailable), (429, h1.RateLimited)):
            with self.subTest(code=code), self.assertRaises(expected):
                h1.fetch_report_json(1, opener=FakeServer({1: http_error(code)}), sleep=lambda s: None)

    def test_server_errors_are_retried_then_fail(self):
        calls, sleeps = [], []

        def opener(http_request, timeout):
            calls.append(1)
            raise http_error(503)

        with self.assertRaises(h1.FetchError):
            h1.fetch_report_json(1, opener=opener, sleep=sleeps.append)
        self.assertEqual(len(calls), h1.MAX_RETRIES + 1)
        self.assertEqual(len(sleeps), h1.MAX_RETRIES)

    def test_non_json_response_means_unavailable(self):
        with self.assertRaises(h1.ReportUnavailable):
            h1.fetch_report_json(1, opener=FakeServer({1: b"<html>login</html>"}))


class FetchReportsTests(unittest.TestCase):
    def run_fetch(self, server, ids, **kwargs):
        sleeps = []
        with tempfile.TemporaryDirectory() as tmp:
            summary = h1.fetch_reports(ids, tmp, opener=server, sleep=sleeps.append, log=lambda m: None, **kwargs)
            files = sorted(p.name for p in Path(tmp).iterdir())
        return summary, files, sleeps

    def test_saves_disclosed_reports_and_reports_the_rest(self):
        server = FakeServer({1: sample_report(), 2: http_error(404), 3: sample_report(disclosed_at=None), 4: http_error(500)})
        summary, files, _ = self.run_fetch(server, [1, 2, 3, 4], delay_seconds=1)
        self.assertEqual(files, ["1.md"])
        self.assertEqual((summary.saved, summary.unavailable, summary.failed), (["1"], ["2", "3"], ["4"]))

    def test_existing_files_are_not_requested_again(self):
        server = FakeServer({1: sample_report()})
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "1.md").write_text("old", encoding="utf-8")
            summary = h1.fetch_reports([1], tmp, opener=server, sleep=lambda s: None, log=lambda m: None)
            self.assertEqual((Path(tmp) / "1.md").read_text(encoding="utf-8"), "old")
        self.assertEqual(server.requested, [])
        self.assertEqual(summary.skipped_existing, ["1"])

    def test_delay_is_applied_between_requests_with_a_floor(self):
        server = FakeServer({1: sample_report(), 2: sample_report(), 3: sample_report()})
        _, _, sleeps = self.run_fetch(server, [1, 2, 3], delay_seconds=0.0)
        self.assertEqual(sleeps, [h1.MIN_DELAY_SECONDS, h1.MIN_DELAY_SECONDS])

    def test_rate_limit_stops_the_whole_run(self):
        server = FakeServer({1: sample_report(), 2: http_error(429), 3: sample_report()})
        summary, files, _ = self.run_fetch(server, [1, 2, 3])
        self.assertEqual(files, ["1.md"])
        self.assertEqual(server.requested, [1, 2])
        self.assertIn("429", summary.stopped_reason)

    def test_repeated_403_is_treated_as_a_block(self):
        server = FakeServer({i: http_error(403) for i in range(1, 8)})
        summary, _, _ = self.run_fetch(server, list(range(1, 8)))
        self.assertEqual(len(server.requested), h1.MAX_CONSECUTIVE_BLOCKS)
        self.assertIn("block", summary.stopped_reason)

    def test_a_single_403_between_good_reports_does_not_stop(self):
        server = FakeServer({1: http_error(403), 2: sample_report(), 3: http_error(403), 4: sample_report()})
        summary, files, _ = self.run_fetch(server, [1, 2, 3, 4])
        self.assertEqual(files, ["2.md", "4.md"])
        self.assertEqual(summary.stopped_reason, "")

    def test_max_reports_caps_requests(self):
        server = FakeServer({i: sample_report() for i in range(1, 6)})
        summary, files, _ = self.run_fetch(server, [1, 2, 3, 4, 5], max_reports=2)
        self.assertEqual(files, ["1.md", "2.md"])
        self.assertIn("--max", summary.stopped_reason)


if __name__ == "__main__":
    unittest.main()
