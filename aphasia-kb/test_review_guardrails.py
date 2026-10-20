"""Mock-Ollama test of the auto_review guardrails and review tiers.

Run with:  python3 test_review_guardrails.py
No Ollama or model required — it stands up a fake server on a spare
port (default 11499, override with MOCK_OLLAMA_PORT), so it coexists
with a real Ollama on :11434.
Run this after touching llm_second_opinion, _validate_llm_payload,
classify_tier or promote.validate_review_args.

Every guardrail must fail toward "leave it deferred for a person".
"""
import json
import os
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

CANNED = {"response": ""}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        body = json.dumps({"models": [{"name": "gemma4:26b"},
                                      {"name": "gemma4:31b"}]}).encode()
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
            "done": True,   # the client streams: one chunk that is also the final one
        }).encode() + b"\n"
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


PORT = int(os.environ.get("MOCK_OLLAMA_PORT", "11499"))
srv = HTTPServer(("127.0.0.1", PORT), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()

import auto_review as ar  # noqa: E402
import promote as pr      # noqa: E402

PAPER = ("=== PAGE 3 ===\nLesions to left IFG were associated with reduced "
         "fluency.\n=== PAGE 7 ===\nNo significant association with "
         "treatment outcome was observed.\n")

FM = {
    "id": "left_ifg", "kind": "region", "schema_version": 2.5,
    "created_by": "agent:gemma4:26b",
    "findings": [
        {"id": "f1", "citation": "@Foo2024", "target": "left IFG",
         "target_kind": "region", "claim": "Damage causes nonfluent output.",
         "strength": "moderate", "relationship": "causal",
         "provenance": {"confidence": "medium", "flags": []},
         "source_passages": [{"supports": "claim", "page": 3,
                              "quote": "Lesions to left IFG were associated "
                                       "with reduced fluency."}]},
        {"id": "f2", "citation": "@Foo2024", "target": "left IFG",
         "target_kind": "region", "claim": "Predicts therapy response.",
         "strength": "weak", "relationship": "responder",
         "provenance": {"confidence": "medium", "flags": []},
         "source_passages": [{"supports": "claim", "page": 7,
                              "quote": "No significant association with "
                                       "treatment outcome was observed."}]},
    ],
}
CHECKS = [ar.Check("all_findings_confidence_high", False, blocker=False,
                   details=["f1: confidence='medium'"])]

CHECK_TRUE = {k: True for k in ar._CHECK_KEYS}


def pf(i, ok=True, verdict="agree"):
    d = {"id": i, **CHECK_TRUE, "omissions": "", "concern": "none",
         "verdict": verdict}
    if not ok:
        d["passage_supports_field"] = False
    return d


def approve(ids=("f1", "f2"), ok=True):
    return json.dumps({
        "overall_verdict": "approve",
        "rationale": "Both passages are present on the cited pages and "
                     "state what the claims say.",
        "per_finding": [pf(i, ok=ok) for i in ids],
    })


def run(name, canned, **kw):
    CANNED["response"] = canned
    kw.setdefault("tier", "A")
    kw.setdefault("paper_text", PAPER)
    r = ar.llm_second_opinion(FM, CHECKS, model="gemma4:31b",
                              host=f"http://127.0.0.1:{PORT}", **kw)
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


# ---------------- model review guardrails ----------------
r = run("1. clean approve, Tier A, independent reviewer, paper present",
        approve(), votes=1)
expect(r["verdict_override"] == "approve", "Tier A approval honoured")

r = run("2. clean approve but Tier B",
        approve(), votes=1, tier="B")
expect(r["verdict_override"] is None, "Tier B never model-approved")

r = run("3. reviewer is the extractor model",
        approve(), votes=1, extractor="agent:gemma4:31b")
expect(r["verdict_override"] is None, "non-independent reviewer blocked")

r = run("4. no paper text available",
        approve(), votes=1, paper_text="")
expect(r["verdict_override"] is None, "approve without the paper downgraded")

r = run("5. model skips a finding (only reviews f1)",
        approve(ids=("f1",)), votes=1)
expect(r["verdict_override"] is None, "incomplete review discarded")

r = run("6. model invents a finding id",
        approve(ids=("f1", "f2", "f9")), votes=1)
expect(r["verdict_override"] is None, "confabulated id discarded")

r = run("7. self-contradiction: approves but a check is false",
        approve(ok=False), votes=1)
expect(r["verdict_override"] is None, "incoherent verdict discarded")

r = run("8. reject always honoured, even on Tier B",
        json.dumps({"overall_verdict": "reject",
                    "rationale": "f2's passage states the opposite of the "
                                 "claim it is cited for.",
                    "per_finding": [pf("f1"),
                                    pf("f2", ok=False, verdict="disagree")]}),
        votes=1, tier="B")
expect(r["verdict_override"] == "reject", "reject path fails safe, honoured")

r = run("9. garbage / non-JSON response",
        "I think this draft looks pretty good to me!", votes=1)
expect(r["verdict_override"] is None, "unparseable response discarded")

r = run("10. empty rationale (unauditable)",
        json.dumps({"overall_verdict": "approve", "rationale": "ok",
                    "per_finding": [pf("f1"), pf("f2")]}), votes=1)
expect(r["verdict_override"] is None, "unauditable rationale discarded")

seq = [approve(), json.dumps({
    "overall_verdict": "defer",
    "rationale": "On reflection f2's passage does not support the claim.",
    "per_finding": [pf("f1"), pf("f2", ok=False, verdict="disagree")]}),
    approve()]
it = iter(seq)
r = run("11. votes disagree (3 runs, model flip-flops)",
        lambda: next(it), votes=3)
expect(r["verdict_override"] is None, "non-unanimous approval blocked")

it2 = iter([approve()] * 3)
r = run("12. votes unanimous across 3 runs, Tier A", lambda: next(it2), votes=3)
expect(r["verdict_override"] == "approve", "unanimous Tier A approval honoured")

r = run("13. deprecated allow_override flag has no effect on Tier B",
        approve(), votes=1, tier="B", allow_override=True)
expect(r["verdict_override"] is None, "allow_override ignored")

# ---------------- tier classification ----------------
print("\n--- tier classification")
with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    (root / "drafts" / "regions").mkdir(parents=True)
    (root / "drafts" / "therapies").mkdir(parents=True)
    (root / "regions").mkdir()
    draft = root / "drafts" / "regions" / "left_ifg__Foo2024.md"
    draft.write_text("")
    good = [ar.Check("schema_valid", True, True),
            ar.Check("pdf_quote_match", True, True,
                     details=["matched 2/2 quotes (100%)"])]
    tier, why = ar.classify_tier(FM, good, draft, root=root)
    expect(tier == "B" and any("new entry" in w for w in why),
           "new entry id is Tier B")
    (root / "regions" / "left_ifg.md").write_text("")
    tier, why = ar.classify_tier(FM, good, draft, root=root)
    expect(tier == "A", f"appending clean findings is Tier A ({why})")
    partial = [ar.Check("schema_valid", True, True),
               ar.Check("pdf_quote_match", True, True,
                        details=["matched 9/10 quotes (90%)"])]
    tier, why = ar.classify_tier(FM, partial, draft, root=root)
    expect(tier == "B", "near-match (9/10) is Tier B")
    strong = json.loads(json.dumps(FM)); strong["findings"][0]["strength"] = "strong"
    tier, why = ar.classify_tier(strong, good, draft, root=root)
    expect(tier == "B", "strength=strong is Tier B")
    flagged = json.loads(json.dumps(FM))
    flagged["findings"][1]["provenance"]["flags"] = ["cohort overlap"]
    tier, why = ar.classify_tier(flagged, good, draft, root=root)
    expect(tier == "B", "any provenance.flags is Tier B")
    tdraft = root / "drafts" / "therapies" / "mit__Foo2024.md"
    tdraft.write_text("")
    tier, why = ar.classify_tier(FM, good, tdraft, root=root)
    expect(tier == "B", "therapies bucket is Tier B")
    nr = json.loads(json.dumps(FM)); nr["findings"][0]["method"] = "narrative_review"
    tier, why = ar.classify_tier(nr, good, draft, root=root)
    expect(tier == "B", "narrative_review is Tier B")

# ---------------- promote.py policy ----------------
print("\n--- promote.py review policy")
expect(pr.normalize_reviewer("michele") == "human:michele", "bare name → human:")
expect(pr.normalize_reviewer("model:gemma4:31b") == "model:gemma4:31b",
       "model: prefix passes through")
try:
    pr.normalize_reviewer("auto-reviewer"); expect(False, "auto-reviewer refused")
except ValueError:
    expect(True, "auto-reviewer refused")
expect(pr.validate_review_args("model:gemma4:31b", "A", None, FM) == [],
       "independent model, Tier A: allowed")
expect(pr.validate_review_args("model:gemma4:31b", "B", None, FM) != [],
       "model on Tier B: refused")
expect(pr.validate_review_args("model:gemma4:26b", "A", None, FM) != [],
       "same model as extractor: refused")
expect(pr.validate_review_args("human:michele", None, None, FM) == [],
       "a person needs no tier")

print("\n" + "=" * 60)
print(f"{len(fails)} failure(s)" if fails else "ALL GUARDRAIL TESTS PASSED")
srv.shutdown()
sys.exit(1 if fails else 0)
