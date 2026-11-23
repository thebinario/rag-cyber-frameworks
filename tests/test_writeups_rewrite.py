from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.writeups import analyzer, query_rewrite


class FakeGenerator:
    model = "fake"

    def __init__(self, reply: str = "", fail: bool = False) -> None:
        self.reply = reply
        self.fail = fail
        self.prompts: list[str] = []

    def generate(self, prompt, options=None, response_format=None):
        self.prompts.append(prompt)
        if self.fail:
            raise RuntimeError("ollama down")
        return self.reply


IDOR = {"writeup_id": "idor", "title": "IDOR in orders", "vuln_class": "IDOR"}
XSS = {"writeup_id": "xss", "title": "XSS in admin", "vuln_class": "XSS"}


class RewriteScenarioTests(unittest.TestCase):
    def test_returns_clean_english_query(self):
        client = FakeGenerator('<think>x</think>SEARCH QUERY: "GraphQL mutation accepts foreign orderId. Possible classes: IDOR."')
        self.assertEqual(
            query_rewrite.rewrite_scenario("mutation aceita orderId de outro usuário", client),
            "GraphQL mutation accepts foreign orderId. Possible classes: IDOR.",
        )

    def test_prompt_keeps_original_scenario_and_forbids_new_facts(self):
        client = FakeGenerator("q")
        query_rewrite.rewrite_scenario("orderId de outro usuário", client)
        self.assertIn("orderId de outro usuário", client.prompts[0])
        self.assertIn("Do not add facts", client.prompts[0])

    def test_failure_falls_back_to_empty(self):
        self.assertEqual(query_rewrite.rewrite_scenario("x", FakeGenerator(fail=True)), "")

    def test_can_be_disabled(self):
        client = FakeGenerator("rewritten")
        with mock.patch.dict("os.environ", {"WRITEUPS_QUERY_REWRITE": "off"}):
            self.assertEqual(query_rewrite.rewrite_scenario("x", client), "")
        self.assertEqual(client.prompts, [])

    def test_output_is_length_limited(self):
        long_reply = "word " * 1000
        self.assertLessEqual(len(query_rewrite.rewrite_scenario("x", FakeGenerator(long_reply))), query_rewrite.MAX_REWRITE_CHARACTERS)


class MergeMatchesTests(unittest.TestCase):
    def test_keeps_best_distance_per_report_and_sorts(self):
        merged = analyzer.merge_matches(
            [[(XSS, 0.39), (IDOR, 0.42)], [(IDOR, 0.36), (XSS, 0.40)]],
            top_k=5,
        )
        self.assertEqual([(r["writeup_id"], d) for r, d in merged], [("idor", 0.36), ("xss", 0.39)])

    def test_respects_top_k(self):
        merged = analyzer.merge_matches([[(XSS, 0.5), (IDOR, 0.4)]], top_k=1)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0][0]["writeup_id"], "idor")


class RetrieveSimilarTests(unittest.TestCase):
    def _search(self, query, **kwargs):
        # The original (Portuguese) query ranks XSS first; the English rewrite finds IDOR.
        if "Possible classes" in query:
            return [(IDOR, 0.36), (XSS, 0.41)]
        return [(XSS, 0.39), (IDOR, 0.42)]

    def test_rewrite_is_searched_too_and_best_distance_wins(self):
        client = FakeGenerator("GraphQL foreign orderId. Possible classes: IDOR")
        with mock.patch.object(analyzer, "search_writeups", side_effect=self._search) as search:
            matches, used = analyzer.retrieve_similar("orderId de outro usuário", mock.Mock(), client, top_k=3)

        self.assertEqual(search.call_count, 2)
        self.assertEqual(matches[0][0]["writeup_id"], "idor")
        self.assertEqual(matches[0][1], 0.36)
        self.assertIn("Possible classes", used)

    def test_rewrite_failure_still_searches_with_the_original(self):
        with mock.patch.object(analyzer, "search_writeups", side_effect=self._search) as search:
            matches, used = analyzer.retrieve_similar("orderId de outro usuário", mock.Mock(), FakeGenerator(fail=True))

        self.assertEqual(search.call_count, 1)
        self.assertEqual(used, "")
        self.assertEqual(matches[0][0]["writeup_id"], "xss")

    def test_analysis_prompt_uses_the_original_scenario_not_the_rewrite(self):
        client = FakeGenerator("GraphQL foreign orderId. Possible classes: IDOR")
        with mock.patch.object(analyzer, "search_writeups", side_effect=self._search):
            analyzer.analyze_scenario("orderId de outro usuário", mock.Mock(), client)
        analysis_prompt = client.prompts[-1]
        self.assertIn("orderId de outro usuário", analysis_prompt)
        self.assertNotIn("Possible classes: IDOR\n\nSIMILAR", analysis_prompt)


if __name__ == "__main__":
    unittest.main()
