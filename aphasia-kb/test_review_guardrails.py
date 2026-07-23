"""Mock-Ollama test of the auto_review local-model guardrails.

Run with:  python3 test_review_guardrails.py
No Ollama or model required — it stands up a fake server on :11434.
Run this after touching llm_second_opinion or _validate_llm_payload.

Stands up a fake /api/chat + /api/tags on localhost and checks that each
guardrail fails toward "leave it deferred".
"""
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

CANNED = {"response": None}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        body = json.dumps({"models": [{"name": "gemma4:26b"}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        self.rfile.read(n)
        content = CANNED["response"]
        if callable(content):
            content = content()
        body = json.dumps({
            "message": {"content": content},
            "prompt_eval_count": 900, "eval_count": 120,
            "total_duration": 2_000_000_000, "done_reason": "stop",
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


srv = HTTPServer(("127.0.0.1", 11434), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()

import auto_review as ar  # noqa: E402

FM = {
    "id": "left_ifg", "kind": "region", "schema_version": 2.3,
    "findings": [
        {"id": "f1", "citation": "@Foo2024", "target": "left IFG",
         "target_kind": "region", "claim": "Damage causes nonfluent output.",
         "strength": "moderate",
         "provenance": {"confidence": "medium", "flags": []},
         "source_passages": [{"supports": "claim", "page": 3,
                              "quote": "Lesions to left IFG were associated "
                                       "with reduced fluency."}]},
        {"id": "f2", "citation": "@Foo2024", "target": "left IFG",
         "target_kind": "region", "claim": "Predicts therapy response.",
         "strength": "weak",
         "provenance": {"confidence": "medium", "flags": []},
         "source_passages": [{"supports": "claim", "page": 7,
                              "quote": "No significant association with "
                                       "treatment outcome was observed."}]},
    ],
}
CHECKS = [ar.Check("all_findings_confidence_high", False, blocker=False,
                   details=["f1: confidence='medium'"])]


def approve(ids=("f1", "f2"), support=True):
    return json.dumps({
        "overall_verdict": "override_approve",
        "rationale": "The quotes plainly support both claims as written.",
        "per_finding": [{"id": i, "quotes_support_claim": support,
                         "concern": "none", "supports_approval": support}
                        for i in ids],
    })


def run(name, canned, **kw):
    CANNED["response"] = canned
    r = ar.llm_second_opinion(FM, CHECKS, model="gemma4:26b",
                              host="http://127.0.0.1:11434", **kw)
    print(f"\n--- {name}")
    print(f"    override = {r.get('verdict_override')!r}")
    for g in (r.get("guardrails") or []):
        print(f"    guardrail: {g}")
    if r.get("error"):
        print(f"    error: {r['error']}")
    return r


fails = []


def expect(cond, msg):
    print(f"    {'PASS' if cond else 'FAIL'}: {msg}")
    if not cond:
        fails.append(msg)


r = run("1. clean override_approve, override DISABLED (default)",
        approve(), votes=1)
expect(r["verdict_override"] is None, "approval blocked by override lockout")

r = run("2. clean override_approve, override ENABLED",
        approve(), votes=1, allow_override=True)
expect(r["verdict_override"] == "approve", "approval honoured when opted in")

r = run("3. model skips a finding (only reviews f1)",
        approve(ids=("f1",)), votes=1, allow_override=True)
expect(r["verdict_override"] is None, "incomplete review discarded")

r = run("4. model invents a finding id",
        approve(ids=("f1", "f2", "f9")), votes=1, allow_override=True)
expect(r["verdict_override"] is None, "confabulated id discarded")

r = run("5. self-contradiction: approves but marks unsupported",
        approve(support=False), votes=1, allow_override=True)
expect(r["verdict_override"] is None, "incoherent verdict discarded")

r = run("6. escalate_reject always honoured even with override disabled",
        json.dumps({"overall_verdict": "escalate_reject",
                    "rationale": "f2's quote states the opposite of "
                                 "the claim it is cited for.",
                    "per_finding": [
                        {"id": "f1", "quotes_support_claim": True,
                         "concern": "none", "supports_approval": True},
                        {"id": "f2", "quotes_support_claim": False,
                         "concern": "quote contradicts claim",
                         "supports_approval": False}]}),
        votes=1)
expect(r["verdict_override"] == "reject", "reject path fails safe, honoured")

r = run("7. garbage / non-JSON response",
        "I think this draft looks pretty good to me!",
        votes=1, allow_override=True)
expect(r["verdict_override"] is None, "unparseable response discarded")

r = run("8. empty rationale (unauditable)",
        json.dumps({"overall_verdict": "override_approve", "rationale": "ok",
                    "per_finding": [
                        {"id": i, "quotes_support_claim": True,
                         "concern": "none", "supports_approval": True}
                        for i in ("f1", "f2")]}),
        votes=1, allow_override=True)
expect(r["verdict_override"] is None, "unauditable rationale discarded")

# Flip-flopping model: votes disagree across runs.
seq = [approve(), json.dumps({
    "overall_verdict": "agree_defer",
    "rationale": "On reflection f2's quote does not support the claim.",
    "per_finding": [{"id": i, "quotes_support_claim": False,
                     "concern": "weak", "supports_approval": False}
                    for i in ("f1", "f2")]}), approve()]
it = iter(seq)
r = run("9. votes disagree (3 runs, model flip-flops)",
        lambda: next(it), votes=3, allow_override=True)
expect(r["verdict_override"] is None, "non-unanimous override blocked")

it2 = iter([approve()] * 3)
r = run("10. votes unanimous across 3 runs, override enabled",
        lambda: next(it2), votes=3, allow_override=True)
expect(r["verdict_override"] == "approve", "unanimous override honoured")

print("\n" + "=" * 60)
print(f"{len(fails)} failure(s)" if fails else "ALL GUARDRAIL TESTS PASSED")
srv.shutdown()
sys.exit(1 if fails else 0)
