"""
compare_extraction.py — compare a local-model extraction against the
curated entries you already have for the same paper.

The point is calibration: before trusting gemma4 on 40 unread papers,
run it on one you've already curated and see how it differs.

    # 1. sandbox extraction (touches nothing)
    python extract.py --pdf papers/Goldenberg1994.pdf \
        --out-dir _compare/gemma4

    # 2. compare against the approved entries
    python compare_extraction.py --citation @Goldenberg1994 \
        --candidate-dir _compare/gemma4

What it reports, roughly in order of how much it should worry you:

  1. QUOTE FIDELITY — does every source_passage actually appear in the
     PDF? This is the one that matters. A fabricated quote is not a
     quality difference, it's a disqualifier: the whole KB design rests
     on quotes being verbatim and checkable.
  2. SCHEMA VALIDITY — would these drafts even pass auto_review?
  3. COVERAGE — did it find the same findings, more, or fewer?
  4. CALIBRATION — does it rate strength/confidence higher than the
     curated version? Systematic over-confidence is the failure mode to
     watch for in a smaller model.

Coverage differences are NOT automatically failures. Two careful readers
extract different findings from the same paper. Read the claims before
concluding the local model is worse — it may have found something real
that the earlier pass missed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from aphasia_kb import _validate_v2_entry, parse_markdown  # noqa: E402

BUCKETS = ("regions", "impairments", "therapies", "predictors")
STRENGTH_RANK = {"weak": 1, "moderate": 2, "strong": 3, "definitive": 4}
CONF_RANK = {"low": 1, "medium": 2, "high": 3}


def _citations_match(a: str, b: str) -> bool:
    return (a or "").lstrip("@").lower() == (b or "").lstrip("@").lower()


def _find_entries(root: Path, citation: str) -> list[Path]:
    """All .md entries under `root` relevant to this citation.

    Two matching modes, unioned, because entries are named two different
    ways in this repo:
      * by filename suffix `<id>__<citation>` — how extract.py/promote
        name single-source drafts (and how candidate sandboxes look);
      * by CONTENT — canonical entries are organised by topic
        (`left_arcuate_fasciculus_slf.md`) and aggregate findings from
        several papers, so the citation only appears inside a finding.
    Filename matching alone silently misses the entire curated corpus
    for any paper whose findings were folded into topic entries.
    """
    key = citation.lstrip("@")
    out: set[Path] = set()
    for bucket in BUCKETS:
        for d in (root / bucket, root / "drafts" / bucket):
            if not d.is_dir():
                continue
            for p in d.glob("*.md"):
                if p.stem.endswith(f"__{key}"):
                    out.add(p)
                    continue
                fm, _ = parse_markdown(p)
                if fm and any(_citations_match(f.get("citation"), citation)
                              for f in (fm.get("findings") or [])):
                    out.add(p)
    return sorted(out)


def _load_findings(paths: list[Path], citation: str | None = None) -> list[dict]:
    """Load findings from `paths`. When `citation` is given, keep ONLY
    findings citing that paper — essential for topic entries that mix
    findings from several papers, so a paper's ground truth isn't
    inflated by unrelated findings sharing the same file."""
    findings = []
    for p in paths:
        fm, _ = parse_markdown(p)
        if not fm:
            continue
        for f in fm.get("findings") or []:
            if citation and not _citations_match(f.get("citation"), citation):
                continue
            f = dict(f)
            f["_entry"] = p.stem
            f["_path"] = p
            findings.append(f)
    return findings


def _schema_issues(paths: list[Path]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for p in paths:
        fm, _ = parse_markdown(p)
        issues: list[str] = []
        if not fm:
            issues.append("no frontmatter")
        else:
            fm["_path"] = str(p)
            _validate_v2_entry(fm, str(p), issues)
        if issues:
            out[p.name] = issues
    return out


def _quote_check(findings: list[dict], papers_dir: Path) -> dict:
    """Grade every quote against the source PDF.

    Graded, not pass/fail, because PDF text extraction is lossy: quotes
    that legitimately span a column break, page break or figure caption
    come back mangled even when the curator copied them faithfully.
    Across this KB's *approved* entries roughly 13% of quotes fail a
    strict containment test, and the overwhelming majority of those are
    extraction artifacts rather than bad quotes.

    So we separate FOUR outcomes, not two:
      exact    — verbatim (modulo the shared normalizer)
      anchored — a long opening run matches, then diverges. Almost always
                 a PDF layout artifact; the quote is real.
      near     — not verbatim, but a high-similarity passage exists at
                 the same spot. This is a PARAPHRASE or a silent fix of
                 an OCR error in the PDF (e.g. the model "corrects"
                 "showed Jess improvement" to "less"). The content is
                 real; the quote just isn't verbatim — a quality issue
                 for a verbatim-quote KB, but NOT fabrication.
      absent   — no similar passage anywhere. THIS is the fabrication
                 signal, and the only one that should condemn a model.

    Keeping `near` distinct matters: a model that paraphrases is fixable
    with a stricter prompt; a model that invents quotes is not usable at
    all. Collapsing them (as a naive verbatim check does) would condemn
    the first for the crime of the second.
    """
    import difflib

    from auto_review import _extract_pdf_text, _normalize

    ANCHOR = 60      # chars that must match to call a quote "anchored"
    NEAR_RATIO = 0.82   # similarity to call a non-verbatim quote "near"

    def _near_match(q: str, text: str) -> bool:
        """Is there a passage in `text` highly similar to `q`?

        Anchor on a few words to locate the region cheaply, then run
        difflib only on that window — sliding difflib over the whole PDF
        would be far too slow. Try several anchors so an OCR error in the
        opening words doesn't hide an otherwise-real quote.
        """
        words = q.split()
        if len(words) < 5:
            return False
        for start in (0, 3, len(words) // 2):
            anchor = " ".join(words[start:start + 4])
            if len(anchor) < 8:
                continue
            idx = text.find(anchor)
            if idx < 0:
                continue
            lo = max(0, idx - start * 8)
            window = text[lo:lo + len(q) + 60]
            if difflib.SequenceMatcher(None, q, window[:len(q)]).ratio() \
                    >= NEAR_RATIO:
                return True
        return False

    cache: dict[str, str] = {}
    exact = anchored = near = absent = total = 0
    absent_list: list[str] = []
    anchored_list: list[str] = []
    near_list: list[str] = []
    no_quotes: list[str] = []

    for f in findings:
        cite = (f.get("citation") or "").lstrip("@")
        sps = f.get("source_passages") or []
        if not sps:
            no_quotes.append(f"{f['_entry']}:{f.get('id')}")
            continue
        if cite not in cache:
            pdf = next((papers_dir / f"{cite}{e}" for e in (".pdf", ".txt")
                        if (papers_dir / f"{cite}{e}").exists()), None)
            if pdf is None:
                cache[cite] = ""
            else:
                try:
                    cache[cite] = _normalize(_extract_pdf_text(pdf)).casefold()
                except Exception:
                    cache[cite] = ""
        text = cache.get(cite, "")
        if not text:
            continue
        for sp in sps:
            raw = (sp.get("quote") or "").strip()
            if not raw:
                continue
            total += 1
            q = _normalize(raw).casefold()
            where = f"{f['_entry']}:{f.get('id')} p.{sp.get('page','?')}"
            if q in text:
                exact += 1
            elif len(q) > ANCHOR and q[:ANCHOR] in text:
                anchored += 1
                anchored_list.append(f"{where} “{raw[:70]}…”")
            elif _near_match(q, text):
                near += 1
                near_list.append(f"{where} “{raw[:80]}…”")
            else:
                absent += 1
                absent_list.append(f"{where} “{raw[:90]}…”")
    return {"total": total, "exact": exact, "anchored": anchored,
            "near": near, "absent": absent, "absent_list": absent_list,
            "anchored_list": anchored_list, "near_list": near_list,
            "no_quotes": no_quotes}


def _summarise(label: str, paths: list[Path], findings: list[dict],
               papers_dir: Path) -> dict:
    return {
        "label": label,
        "paths": paths,
        "findings": findings,
        "schema": _schema_issues(paths),
        "quotes": _quote_check(findings, papers_dir),
    }


def _print_side(a: dict, b: dict) -> None:
    W1, W2 = 28, 24
    print(f"\n{'':<{W1}}{a['label']:<{W2}}{b['label']}")
    print("-" * (W1 + W2 + 20))

    def row(name, x, y):
        print(f"{name:<{W1}}{str(x):<{W2}}{y}")

    row("entries", len(a["paths"]), len(b["paths"]))
    row("findings", len(a["findings"]), len(b["findings"]))
    row("entries w/ schema issues", len(a["schema"]), len(b["schema"]))

    for side in (a, b):
        q = side["quotes"]
        t = q["total"] or 1
        side["_ok"] = q["exact"] + q["anchored"]
        side["_okpct"] = 100 * side["_ok"] / t
        side["_abspct"] = 100 * q["absent"] / t

    row("quotes total", a["quotes"]["total"], b["quotes"]["total"])
    row("  exact match", a["quotes"]["exact"], b["quotes"]["exact"])
    row("  anchored (PDF artifact)",
        a["quotes"]["anchored"], b["quotes"]["anchored"])
    row("  near (paraphrase/OCR)",
        a["quotes"].get("near", 0), b["quotes"].get("near", 0))
    row("  ABSENT (fabrication?)",
        f"{a['quotes']['absent']} ({a['_abspct']:.0f}%)",
        f"{b['quotes']['absent']} ({b['_abspct']:.0f}%)")


def _print_detail(side: dict) -> None:
    q = side["quotes"]
    if q["absent_list"]:
        print(f"\n⚠ {side['label']}: {len(q['absent_list'])} quote(s) with no "
              f"similar passage in the PDF — possible fabrication, check "
              f"by hand:")
        for m in q["absent_list"][:12]:
            print(f"    ✗ {m}")
        if len(q["absent_list"]) > 12:
            print(f"    … and {len(q['absent_list']) - 12} more")
    if q.get("near_list"):
        print(f"\nℹ {side['label']}: {len(q['near_list'])} quote(s) "
              f"paraphrased or OCR-corrected (content real, not verbatim):")
        for m in q["near_list"][:8]:
            print(f"    ~ {m}")
    if q["no_quotes"]:
        print(f"\n⚠ {side['label']}: finding(s) with NO source_passages: "
              f"{', '.join(q['no_quotes'][:8])}")
    if side["schema"]:
        print(f"\n⚠ {side['label']}: schema issues:")
        for name, issues in list(side["schema"].items())[:6]:
            print(f"    {name}: {issues[0]}"
                  + (f"  (+{len(issues)-1} more)" if len(issues) > 1 else ""))


def _print_claims(side: dict) -> None:
    print(f"\n{side['label']} — claims extracted:")
    if not side["findings"]:
        print("    (none)")
    for f in side["findings"]:
        claim = " ".join((f.get("claim") or "").split())
        conf = (f.get("provenance") or {}).get("confidence")
        print(f"  · [{f.get('target')}] strength={f.get('strength')} "
              f"conf={conf}")
        print(f"      {claim[:180]}{'…' if len(claim) > 180 else ''}")


def _print_calibration(ref: dict, cand: dict) -> None:
    def avg(findings, key, ranks):
        vals = [ranks.get(f.get(key) if key == "strength"
                          else (f.get("provenance") or {}).get("confidence"))
                for f in findings]
        vals = [v for v in vals if v]
        return sum(vals) / len(vals) if vals else None

    rs, cs = avg(ref["findings"], "strength", STRENGTH_RANK), \
        avg(cand["findings"], "strength", STRENGTH_RANK)
    rc, cc = avg(ref["findings"], "confidence", CONF_RANK), \
        avg(cand["findings"], "confidence", CONF_RANK)
    if rs and cs:
        d = cs - rs
        note = ("  ← candidate rates evidence STRONGER than the curated "
                "version" if d > 0.4 else "")
        print(f"\nmean strength   curated={rs:.2f}  candidate={cs:.2f}{note}")
    if rc and cc:
        d = cc - rc
        note = ("  ← candidate is MORE confident than the curated version"
                if d > 0.4 else "")
        print(f"mean confidence curated={rc:.2f}  candidate={cc:.2f}{note}")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--citation", required=True,
                   help="Citation key, e.g. @Goldenberg1994")
    p.add_argument("--candidate-dir", type=Path, required=True,
                   help="Directory the sandbox extraction wrote to "
                        "(extract.py --out-dir)")
    p.add_argument("--reference-root", type=Path, default=HERE,
                   help=f"Where the curated entries live (default: {HERE})")
    p.add_argument("--papers-dir", type=Path, default=HERE / "papers")
    p.add_argument("--show-claims", action="store_true",
                   help="Print every claim from both sides for manual reading. "
                        "Recommended — the numbers can't tell you whether a "
                        "coverage difference is a miss or a genuine find.")
    args = p.parse_args(argv)

    ref_paths = _find_entries(args.reference_root, args.citation)
    cand_paths = _find_entries(args.candidate_dir, args.citation)

    if not ref_paths:
        print(f"❌ no curated entries found for {args.citation} under "
              f"{args.reference_root}")
        return 2
    if not cand_paths:
        print(f"❌ no candidate entries found for {args.citation} under "
              f"{args.candidate_dir}\n"
              f"   Did the sandbox extraction return 0 drafts?")
        return 2

    ref = _summarise("curated (reference)", ref_paths,
                     _load_findings(ref_paths, args.citation), args.papers_dir)
    cand = _summarise("local model", cand_paths,
                      _load_findings(cand_paths, args.citation),
                      args.papers_dir)

    print(f"\n=== {args.citation} ===")
    _print_side(ref, cand)
    _print_detail(cand)
    _print_detail(ref)
    _print_calibration(ref, cand)
    if args.show_claims:
        _print_claims(ref)
        _print_claims(cand)

    # Verdict is deliberately narrow. Quote fidelity is the one thing
    # measurable without judgement, and it's graded against the CURATED
    # side's own rate on the same paper — not against 100%, which no
    # extractor achieves here because PDF text extraction is lossy.
    q, rq = cand["quotes"], ref["quotes"]
    print("\n" + "=" * 76)
    if not q["total"]:
        print("? No candidate quotes to verify — check the drafts by hand.")
        return 0

    print(f"Baseline for comparison: the curated entries for this paper "
          f"score {rq['absent']}/{rq['total']} absent "
          f"({ref['_abspct']:.0f}%).")

    if q["absent"] == 0:
        print("✓ Every candidate quote was located in the PDF. Quote "
              "fidelity is sound.")
        print("  Now read the claims above — coverage and wording are "
              "what's left to judge, and only you can.")
    elif cand["_abspct"] <= max(ref["_abspct"] + 5, 5):
        print(f"~ {q['absent']} candidate quote(s) absent "
              f"({cand['_abspct']:.0f}%), in line with the curated "
              f"baseline.")
        print("  Probably PDF-extraction noise rather than fabrication, "
              "but spot-check the listed quotes.")
    else:
        print(f"✗ {q['absent']} of {q['total']} candidate quotes "
              f"({cand['_abspct']:.0f}%) had no match in the PDF — "
              f"materially worse than the curated baseline.")
        print("  Suspect truncation FIRST: did the extraction run print a "
              "num_ctx warning? A model shown half a paper will "
              "confabulate the rest.")
        print("  If context was fine, this model is not safe for "
              "extraction.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
