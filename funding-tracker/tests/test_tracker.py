"""Run with:  python3 -m unittest discover -s tests   (from the funding-tracker directory)"""
import json
import os
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tracker import golden, llm  # noqa: E402
from tracker.events import build_events  # noqa: E402
from tracker.extract import Rules, extract, find_money  # noqa: E402


class GoldenTest(unittest.TestCase):
    def test_golden_accuracy(self):
        r = golden.evaluate()
        msg = "\n".join(f"{f['title']}: {f['diff']}" for f in r["failures"][:10])
        self.assertGreaterEqual(r["accuracy"], 0.95, msg)


class MoneyTest(unittest.TestCase):
    def cases(self):
        return [
            ("raises $1.5B", 1.5e9), ("raises €3 billion", 3.3e9), ("raises $300M", 3e8), ("Rs 3,054-crore IPO", 3054e7 * 0.012),
            ("获1.5亿美元融资", 1.5e8), ("完成近10亿元融资", 1e9 * 0.14), ("估值1万4000亿美元", 1.4e12), ("61 Billion Yuan", 61e9 * 0.14),
        ]

    def test_parse(self):
        for text, want in self.cases():
            got = find_money(text)
            self.assertTrue(got, text)
            self.assertAlmostEqual(got[0].usd, want, delta=want * 0.01, msg=text)

    def test_roles(self):
        m = find_money("raises $1B at a $10B post-money valuation with ARR reaching $200M")
        self.assertEqual([x.role for x in m], ["amount", "valuation", "arr"])


class EventMergeTest(unittest.TestCase):
    def test_same_round_reported_twice_merges(self):
        rules = Rules()
        titles = [("2026-04-29", "OpenAI raises record $122B round at $852B valuation"),
                  ("2026-06-09", "OpenAI Files for IPO After Raising $122 Billion at $852 Billion Valuation")]
        enriched = [{"id": str(i), "title": t, "date": d, "source": f"s{i}", "url": "", "x": extract(t, rules).as_dict()}
                    for i, (d, t) in enumerate(titles)]
        evs = [e for e in build_events(enriched) if e.event == "funding"]
        self.assertEqual(len(evs), 1)
        self.assertEqual(evs[0].mentions, 2)


class LLMClientTest(unittest.TestCase):
    def test_openai_compatible_client(self):
        class H(BaseHTTPRequestHandler):
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                assert body["messages"][0]["role"] == "system"
                out = {"items": [{"company": "Foo", "event": "funding", "status": "closed", "amount_usd": "5000000",
                                  "valuation_usd": None, "arr_usd": None, "round": "Seed", "acquirer": None}]}
                data = json.dumps({"choices": [{"message": {"content": json.dumps(out)}}]}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def log_message(self, *a):
                pass

        srv = HTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        os.environ.update({"FT_LLM_API_KEY": "test", "FT_LLM_BASE_URL": f"http://127.0.0.1:{srv.server_port}"})
        try:
            res = llm.extract_batch(["Foo snags $5M seed"])
        finally:
            srv.shutdown()
            srv.server_close()
            os.environ.pop("FT_LLM_API_KEY")
            os.environ.pop("FT_LLM_BASE_URL")
        self.assertEqual(res[0]["company"], "Foo")
        self.assertEqual(res[0]["amount_usd"], 5e6)


if __name__ == "__main__":
    unittest.main()
