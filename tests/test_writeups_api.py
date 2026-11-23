from __future__ import annotations

import json
import sys
import threading
import unittest
from pathlib import Path
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.writeups import api


def fake_analyze(scenario: str, top_k: int) -> dict:
    return {"scenario": scenario, "answer": "ok", "weak_match": False, "reports": [], "top_k": top_k}


class BuildScenarioTests(unittest.TestCase):
    def test_free_text_scenario(self):
        self.assertEqual(api.build_scenario({"scenario": "  upload renders in admin  "}), "upload renders in admin")

    def test_structured_recon_fields(self):
        text = api.build_scenario(
            {
                "host": "app.example.com",
                "stack": ["Node", "GraphQL"],
                "endpoints": ["/graphql"],
                "findings": "updateOrder accepts foreign orderId",
            }
        )
        self.assertIn("Host: app.example.com", text)
        self.assertIn("Technology stack: Node; GraphQL", text)
        self.assertIn("Endpoints: /graphql", text)
        self.assertIn("Findings / observed behavior: updateOrder accepts foreign orderId", text)

    def test_empty_payload_is_rejected(self):
        with self.assertRaises(api.RequestError) as ctx:
            api.build_scenario({})
        self.assertEqual(ctx.exception.status, 400)

    def test_wrong_types_are_rejected(self):
        for payload in ({"scenario": 5}, {"stack": {"a": 1}}, {"endpoints": [["x"]]}):
            with self.subTest(payload=payload), self.assertRaises(api.RequestError):
                api.build_scenario(payload)

    def test_oversized_scenario_is_rejected(self):
        with self.assertRaises(api.RequestError):
            api.build_scenario({"scenario": "a" * (api.MAX_SCENARIO_CHARACTERS + 1)})

    def test_top_k_validation(self):
        self.assertEqual(api.parse_top_k({}), api.DEFAULT_WRITEUPS_TOP_K)
        self.assertEqual(api.parse_top_k({"top_k": 7}), 7)
        for bad in (0, 11, "3", True, 2.5):
            with self.subTest(bad=bad), self.assertRaises(api.RequestError):
                api.parse_top_k({"top_k": bad})


class ServerTests(unittest.TestCase):
    TOKEN = "s3cret"

    def setUp(self):
        self.server = api.create_server(fake_analyze, host="127.0.0.1", port=0, token=self.TOKEN)
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def _post(self, path, body, token=TOKEN, raw=None):
        data = raw if raw is not None else json.dumps(body).encode()
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        req = request.Request(f"{self.base}{path}", data=data, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=5) as resp:
                return resp.status, json.loads(resp.read())
        except error.HTTPError as exc:
            return exc.code, json.loads(exc.read())

    def test_health_needs_no_token(self):
        with request.urlopen(f"{self.base}/health", timeout=5) as resp:
            self.assertEqual(json.loads(resp.read()), {"status": "ok"})

    def test_analyze_success(self):
        status, body = self._post("/analyze", {"stack": ["Node"], "findings": ["IDOR suspected"], "top_k": 2})
        self.assertEqual(status, 200)
        self.assertEqual(body["answer"], "ok")
        self.assertEqual(body["top_k"], 2)
        self.assertIn("IDOR suspected", body["scenario"])

    def test_missing_or_wrong_token_is_rejected(self):
        self.assertEqual(self._post("/analyze", {"scenario": "x"}, token=None)[0], 401)
        self.assertEqual(self._post("/analyze", {"scenario": "x"}, token="wrong")[0], 401)

    def test_validation_errors(self):
        self.assertEqual(self._post("/analyze", {})[0], 400)
        self.assertEqual(self._post("/analyze", None, raw=b"not json")[0], 400)
        self.assertEqual(self._post("/analyze", None, raw=b"[1,2]")[0], 400)

    def test_latin1_body_gets_a_helpful_error(self):
        raw = '{"scenario": "usuário"}'.encode("latin-1")
        status, body = self._post("/analyze", None, raw=raw)
        self.assertEqual(status, 400)
        self.assertIn("UTF-8", body["error"])

    def test_utf8_accents_are_accepted(self):
        status, body = self._post("/analyze", {"scenario": "usuário não autorizado"})
        self.assertEqual(status, 200)
        self.assertIn("usuário", body["scenario"])

    def test_oversized_body_is_rejected(self):
        status, _ = self._post("/analyze", None, raw=b"x" * (api.MAX_BODY_BYTES + 1))
        self.assertEqual(status, 413)

    def test_unknown_path(self):
        self.assertEqual(self._post("/other", {"scenario": "x"})[0], 404)

    def test_internal_errors_do_not_leak_details(self):
        def broken(scenario, top_k):
            raise RuntimeError("secret internal path /etc/passwd")

        server = api.create_server(broken, host="127.0.0.1", port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            req = request.Request(
                f"http://127.0.0.1:{server.server_address[1]}/analyze",
                data=b'{"scenario": "x"}',
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with self.assertRaises(error.HTTPError) as ctx:
                request.urlopen(req, timeout=5)
            body = ctx.exception.read().decode()
            self.assertEqual(ctx.exception.code, 500)
            self.assertNotIn("passwd", body)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


class BindSafetyTests(unittest.TestCase):
    def test_non_loopback_requires_token(self):
        with self.assertRaises(ValueError):
            api.create_server(fake_analyze, host="0.0.0.0", port=0)


if __name__ == "__main__":
    unittest.main()
