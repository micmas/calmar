#!/usr/bin/env python3
"""
backfill.py — bring findings extracted in an older schema up to v2.7 by
asking the model only for what is missing, never re-extracting claims.

    python backfill.py                          # dry run: papers and missing fields
    python backfill.py --execute                # every paper, drafts and approved entries
    python backfill.py --execute --citation @Breier2008 --citation @Hope2013
    python backfill.py --execute --fields lesion_mapping,phase
    python backfill.py --execute --limit 5      # a first batch

Missing fields, per finding (narrative reviews are skipped):
  lesion_mapping      v2.7 design block, lesion-mapping methods only
  phase               sample.phase (v2.6)
  cohort              sample.cohort (v2.7) — written as not_reported when
                      the sample is not a named, reused dataset, so the
                      paper is not asked again
  author_limitations  missing, or filled with [] by the save-time repair

For each paper the local extraction model reads the full text once with
the list of its findings (claim, method, sample, threshold) and returns
only the requested fields, each with a verbatim quote. A value is written
only when its quote is found in the PDF (quote_check grades exact,
elided, table or anchored) or when the value is "not_reported". The
quote is appended to the finding's source_passages, and the finding gets
a `filled: {by, date, tool, fields}` block, so reports can say "filled in by a
model from the paper" and a reviewer can see what changed. Claims,
existing quotes, statistics and review blocks are never touched.

Approved (canonical) entries are written too (decided 2026-10-26): the
values are metadata about the study, quote-checked, and marked as filled.
An unverified value is not written; the loader keeps inferring that
field from the existing text and labels it inferred. A file is moved to
schema_version 2.7 only when all its findings are complete and it
validates as 2.7.

Each paper costs one model call (~2–4 min on gemma4:31b for a 15-page
paper). One BACKFILLED line per paper goes to extraction_log.md.
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from aphasia_kb import parse_markdown, _validate_v2_entry  # noqa: E402
import lesion_mapping as LM  # noqa: E402
from phase import PHASE_VOCAB, infer_phase  # noqa: E402
from quote_check import PaperText, find_paper, grade_quote  # noqa: E402

BUCKETS = ("regions", "impairments", "therapies", "predictors", "reviews")
ALL_FIELDS = ("lesion_mapping", "phase", "cohort", "author_limitations")
ACCEPT = {"exact", "elided", "table", "anchored"}
LIMITATION_FLAGS = ("author_limitations not extracted by the model",)
LESIONMAP_FLAGS = ("lesion_mapping (v2.7 design) not extracted by the model",)
SUPPORTS = {"lesion_mapping": "method", "phase": "sample", "cohort": "sample",
            "author_limitations": "limitation"}


# --------------------------------------------------------------- targets
def _citation(f: dict) -> str:
    return "@" + str(f.get("citation") or "").strip().strip("'\"").lstrip("@")


def _flagged(f: dict, prefixes) -> bool:
    flags = (f.get("provenance") or {}).get("flags") or []
    return any(str(x).startswith(p) for x in flags for p in prefixes)


def missing_fields(f: dict, wanted=ALL_FIELDS) -> list[str]:
    if not isinstance(f, dict):
        return []
    methods = f.get("method") if isinstance(f.get("method"), list) else [f.get("method")]
    if "narrative_review" in methods or f.get("relationship") == "synthesis":
        return []
    s = f.get("sample") if isinstance(f.get("sample"), dict) else {}
    out = []
    if "lesion_mapping" in wanted and LM.is_lesion_mapping(f) and not isinstance(f.get("lesion_mapping"), dict):
        out.append("lesion_mapping")
    if "phase" in wanted and s.get("phase") not in PHASE_VOCAB:
        out.append("phase")
    if "cohort" in wanted and "cohort" not in s:
        out.append("cohort")
    if "author_limitations" in wanted and (f.get("author_limitations") is None
                                           or _flagged(f, LIMITATION_FLAGS)):
        out.append("author_limitations")
    return out


def collect(kb_root: Path, wanted, only=None, include_canonical=True) -> dict[str, list[dict]]:
    """citation → [{path, canonical, fid, finding, missing}]"""
    papers: dict[str, list[dict]] = {}
    folders = [(kb_root / "drafts" / b, False) for b in BUCKETS]
    if include_canonical:
        folders += [(kb_root / b, True) for b in BUCKETS]
    for folder, canonical in folders:
        for path in sorted(folder.glob("*.md")):
            try:
                fm, _ = parse_markdown(path)
            except Exception as e:  # noqa: BLE001
                print(f"  ⚠ {path.relative_to(kb_root)}: unreadable, skipped ({str(e).splitlines()[0]})")
                continue
            for f in fm.get("findings") or []:
                miss = missing_fields(f, wanted)
                if not miss:
                    continue
                cit = _citation(f)
                if only and cit.lower() not in only:
                    continue
                papers.setdefault(cit, []).append(
                    {"path": path, "canonical": canonical, "fid": f.get("id"),
                     "finding": f, "missing": miss})
    return papers


# ---------------------------------------------------------------- prompt
PROMPT = """You are completing structured records about findings that were ALREADY
extracted from the paper below. Do not change, re-state or add findings.
For each finding listed, give ONLY the fields named in its `fill` list,
read from the paper.

Every value must come with a short verbatim quote (one or two sentences,
copied exactly from the paper, no paraphrase, no "..." inside unless the
paper has it) that states it. If the paper does not say, give the value
"not_reported" (or [] for author_limitations) and an empty quote.

Fields:
- lesion_mapping (lesion-symptom mapping design of the analysis behind the finding):
    analysis: univariate | multivariate | region_based | network | not_reported
    n_analysed: number of patients in THIS analysis (integer) or "not_reported"
    min_lesion_overlap: e.g. ">= 5 patients", "10% of the sample", or "not_reported"
    lesion_volume_correction: direct (direct total lesion volume control, dTLVC) |
        covariate (lesion volume entered as a covariate or regressed out of the scores) |
        none (the paper says it was not controlled) | not_reported
    multiple_comparisons: permutation_fwe | fwe | cluster_fwe | fdr | bonferroni |
        uncorrected | not_reported
  Give up to 3 quotes in "quotes" (the sentences stating the correction, the
  volume control and the sample used).
- phase: recovery phase of the sample (Stroke Recovery and Rehabilitation
  Roundtable): hyperacute (0-24 h) | acute (1-7 days) | early_subacute
  (7 days-3 months) | late_subacute (3-6 months) | chronic (> 6 months) |
  mixed | longitudinal (same patients at >= 2 phases) | not_reported
- cohort: the name of a named, reused dataset the patients come from
  (e.g. "ARC" = Aphasia Recovery Cohort, "PLORAS", "OCS", "STROKOG", a trial
  registration such as "NCT01927302"), or "not_reported" when the sample was
  recruited for this study only.
- author_limitations: list of the limitations the AUTHORS state (short
  phrases), [] if none are stated.

Findings often come from the same analysis. When a finding's answers are
identical to an earlier finding's, write {{"key": "K7", "same_as": "K3"}}
instead of repeating them.

Answer with JSON only, in this shape (include only the requested fields):
{{"findings": [
  {{"key": "K1",
    "lesion_mapping": {{"value": {{"analysis": "...", "n_analysed": 0, "min_lesion_overlap": "...",
                                   "lesion_volume_correction": "...", "multiple_comparisons": "..."}},
                        "quotes": ["..."]}},
    "phase": {{"value": "...", "quote": "..."}},
    "cohort": {{"value": "...", "quote": "..."}},
    "author_limitations": {{"value": ["..."], "quote": "..."}}}}
]}}

Findings:
{findings}

Paper ({citation}):
{paper}
"""


def _finding_line(key: str, t: dict) -> str:
    f = t["finding"]
    s = f.get("sample") or {}
    st = f.get("statistics") or {}
    m = f.get("method")
    parts = [f"{key}", f"claim: {str(f.get('claim') or '').strip()}",
             f"method: {', '.join(m) if isinstance(m, list) else m}",
             f"sample: n={s.get('n')}; {s.get('population') or ''}; {s.get('time_post_onset') or ''}",
             f"threshold: {st.get('threshold') or ''}",
             f"fill: {', '.join(t['missing'])}"]
    return "- " + " | ".join(parts)


def build_prompt(citation: str, targets: list[dict], paper_text: str) -> tuple[str, dict]:
    keys = {f"K{i}": t for i, t in enumerate(targets, 1)}
    lines = "\n".join(_finding_line(k, t) for k, t in keys.items())
    return PROMPT.format(findings=lines, citation=citation, paper=paper_text), keys


# ----------------------------------------------------------------- check
def _verified(quote, paper: PaperText) -> str | None:
    q = (quote or "").strip()
    if not q:
        return None
    g = grade_quote(q, paper)
    return g if g in ACCEPT else None


_VOLUME_WORDS = re.compile(r"volume|lesion size|lesion load|tlvc", re.I)
_CORRECTION_WORDS = re.compile(r"correct|fwe|family|fdr|false discovery|bonferroni|holm|permutation|"
                               r"multiple comparison|threshold|p\s*[<=≤]|p[\s-]*values?|alpha|α\s*=|"
                               r"\ba\s*=\s*0?\.\d", re.I)


def check(field: str, item, paper: PaperText):
    """(value, [verified quotes], note) — value None means: do not write."""
    if not isinstance(item, dict):
        return None, [], "no answer"
    val = item.get("value")
    quotes = item.get("quotes") if field == "lesion_mapping" else [item.get("quote")]
    quotes = [q for q in (quotes or []) if isinstance(q, str) and q.strip()]
    good = [q for q in quotes if _verified(q, paper)]
    if field == "lesion_mapping":
        if not isinstance(val, dict):
            return None, [], "no value"
        lm = {k: val.get(k, "not_reported") for k in LM.FIELDS}
        if lm["analysis"] not in LM.ANALYSIS_VOCAB or \
                lm["lesion_volume_correction"] not in LM.VOLUME_VOCAB or \
                lm["multiple_comparisons"] not in LM.CORRECTION_VOCAB:
            return None, [], f"off-vocabulary {lm}"
        n = lm["n_analysed"]
        if isinstance(n, str) and n.strip().isdigit():
            lm["n_analysed"] = int(n)
        elif not isinstance(n, int):
            lm["n_analysed"] = "not_reported"
        if not isinstance(lm["min_lesion_overlap"], str) or not lm["min_lesion_overlap"].strip():
            lm["min_lesion_overlap"] = "not_reported"
        informative = any(lm[k] != "not_reported" for k in LM.FIELDS)
        if informative and not good:
            return None, [], "no quote found in the PDF"
        # A design value needs a verified quote that is about it: "none" or
        # "uncorrected" from a sentence that never mentions volume or a
        # correction is the model filling a gap, not the paper.
        said = " ".join(good)
        downgraded = []
        if lm["lesion_volume_correction"] != "not_reported" and not _VOLUME_WORDS.search(said):
            lm["lesion_volume_correction"] = "not_reported"
            downgraded.append("lesion_volume_correction")
        if lm["multiple_comparisons"] != "not_reported" and not _CORRECTION_WORDS.search(said):
            lm["multiple_comparisons"] = "not_reported"
            downgraded.append("multiple_comparisons")
        return lm, good, (f"{', '.join(downgraded)} → not_reported (no quote states it)"
                          if downgraded else "")
    if field == "phase":
        if val not in PHASE_VOCAB:
            return None, [], f"off-vocabulary {val!r}"
        if val != "not_reported" and not good:
            return None, [], "no quote found in the PDF"
        return val, good, ""
    if field == "cohort":
        if not isinstance(val, str) or not val.strip():
            return None, [], "no value"
        val = val.strip()[:60]
        if val.lower() in ("not_reported", "none", "n/a"):
            return "not_reported", [], ""
        if not good:
            return None, [], "no quote found in the PDF"
        return val, good, ""
    if field == "author_limitations":
        if not isinstance(val, list):
            return None, [], "no list"
        val = [str(x).strip() for x in val if str(x).strip()]
        if val and not good:
            return None, [], "no quote found in the PDF"
        return val, good, ""
    return None, [], "unknown field"


# ----------------------------------------------------------------- write
def _page_of(doc, quote: str):
    try:
        from review_sheet import locate
        pno, _ = locate(doc, quote, None)
        return pno + 1 if pno is not None else "not_reported"
    except Exception:  # noqa: BLE001
        return "not_reported"


def _dump(path: Path, fm: dict, body: str, canonical: bool) -> None:
    if canonical:   # promote.py's writer, so diffs stay small
        text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False)
        path.write_text(f"---\n{text}---\n{body}", encoding="utf-8")
    else:           # extract.py's writer
        text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=100)
        out = f"---\n{text.rstrip()}\n---\n"
        if body.strip():
            out += body if body.endswith("\n") else body + "\n"
        path.write_text(out, encoding="utf-8")


def _complete(fm: dict) -> bool:
    for f in fm.get("findings") or []:
        if missing_fields(f, ("lesion_mapping", "phase")):
            return False
    return True


def _maybe_bump(fm: dict, path: Path) -> bool:
    """schema_version → 2.7 when complete and it validates no worse."""
    try:
        if float(fm.get("schema_version") or 0) >= 2.7 or not _complete(fm):
            return False
    except (TypeError, ValueError):
        return False
    before, after = [], []
    _validate_v2_entry(copy.deepcopy(fm), str(path), before)
    trial = copy.deepcopy(fm)
    trial["schema_version"] = 2.7
    _validate_v2_entry(trial, str(path), after)
    if len(after) <= len(before):
        fm["schema_version"] = 2.7
        return True
    return False


def apply(targets_by_key: dict, answer: dict, paper: PaperText, pdf: Path,
          model: str, execute: bool) -> tuple[int, int, list[str]]:
    """Write verified values. Returns (written, skipped, notes)."""
    try:
        import pymupdf as fitz
    except ImportError:  # pragma: no cover
        import fitz
    doc = fitz.open(str(pdf))
    by_key = {str(a.get("key")): a for a in (answer.get("findings") or []) if isinstance(a, dict)}
    today = dt.date.today().isoformat()
    files: dict[Path, tuple[dict, str, bool]] = {}
    written = skipped = 0
    notes: list[str] = []
    for key, t in targets_by_key.items():
        path = t["path"]
        if path not in files:
            fm, body = parse_markdown(path)
            files[path] = (fm, body, t["canonical"])
        fm = files[path][0]
        f = next((x for x in fm.get("findings") or [] if isinstance(x, dict) and x.get("id") == t["fid"]), None)
        if f is None:
            continue
        a = by_key.get(key, {})
        if a.get("same_as"):            # "identical to an earlier finding"
            a = by_key.get(str(a["same_as"]), {})
        filled = []
        for field in t["missing"]:
            val, quotes, why = check(field, a.get(field), paper)
            if why and val is not None:
                notes.append(f"{path.name} {t['fid']} {field}: {why}")
            if val is None:
                skipped += 1
                notes.append(f"{path.name} {t['fid']} {field}: not written ({why})")
                if field == "phase":   # same deterministic fallback as normalize_drafts
                    s = f.setdefault("sample", {}) if isinstance(f.get("sample"), dict) or f.get("sample") is None else None
                    if isinstance(s, dict):
                        s["phase"] = infer_phase(s.get("time_post_onset"))[0]
                continue
            if field == "lesion_mapping":
                f["lesion_mapping"] = val
                prov = f.get("provenance") or {}
                if prov.get("flags"):
                    prov["flags"] = [x for x in prov["flags"]
                                     if not any(str(x).startswith(p) for p in LESIONMAP_FLAGS)]
            elif field in ("phase", "cohort"):
                if not isinstance(f.get("sample"), dict):
                    f["sample"] = {}
                f["sample"][field] = val
            elif field == "author_limitations":
                f["author_limitations"] = val
                prov = f.get("provenance") or {}
                if prov.get("flags") and (val or not quotes):
                    prov["flags"] = [x for x in prov["flags"]
                                     if not any(str(x).startswith(p) for p in LIMITATION_FLAGS)]
            have = {str(p.get("quote")) for p in f.get("source_passages") or [] if isinstance(p, dict)}
            for q in quotes:
                if q not in have:
                    f.setdefault("source_passages", []).append(
                        {"section": "added by backfill", "page": _page_of(doc, q),
                         "quote": q, "supports": SUPPORTS[field]})
                    have.add(q)
            filled.append(field)
            written += 1
        if filled:
            prev = f.get("filled") or {}
            f["filled"] = {"by": f"model:{model}", "date": today, "tool": "backfill.py",
                           "fields": sorted(set(prev.get("fields") or []) | set(filled))}
    doc.close()
    for path, (fm, body, canonical) in files.items():
        if _maybe_bump(fm, path):
            notes.append(f"{path.name}: schema_version → 2.7")
        if execute:
            _dump(path, fm, body, canonical)
    return written, skipped, notes


# ------------------------------------------------------------------- run
def _paper_text(pdf: Path) -> str:
    from extract import _extract_pdf_text
    return _extract_pdf_text(pdf)[0]


def run_paper(citation: str, targets: list[dict], papers_dir: Path, model: str,
              host: str, execute: bool, response_file: Path | None) -> tuple[int, int]:
    pdf = find_paper(citation, papers_dir)
    if pdf is None or pdf.suffix.lower() != ".pdf":
        print(f"  ✗ no PDF for {citation} in {papers_dir}")
        return 0, 0
    text = _paper_text(pdf)
    prompt, keys = build_prompt(citation, targets, text)
    if response_file:
        raw = response_file.read_text(encoding="utf-8")
    else:
        from extract import call_ollama, parse_response  # noqa: F401
        raw = call_ollama(prompt, model, max_tokens=max(2000, 400 * len(keys)), host=host)
        (ROOT / f"_last_backfill_response_{citation.lstrip('@')}.txt").write_text(raw, encoding="utf-8")
    from extract import parse_response
    try:
        answer = parse_response(raw)
    except Exception as e:  # noqa: BLE001
        print(f"  ✗ {citation}: response is not JSON ({e}); nothing written")
        return 0, 0
    paper = PaperText.from_pdf(pdf)
    written, skipped, notes = apply(keys, answer, paper, pdf, model, execute)
    for n in notes:
        print(f"    {n}")
    if execute and written:
        fields = sorted({m for t in targets for m in t["missing"]})
        with (ROOT / "extraction_log.md").open("a", encoding="utf-8") as fh:
            fh.write(f"{dt.date.today().isoformat()} | BACKFILLED | {citation} | "
                     f"{', '.join(fields)} | {written} value(s) written, {skipped} not "
                     f"(no quote found) across {len(keys)} finding(s) | model: {model}\n")
    return written, skipped


def _cli(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--execute", action="store_true", help="call the model and write")
    ap.add_argument("--citation", action="append", help="only these papers (repeatable)")
    ap.add_argument("--fields", default=",".join(ALL_FIELDS),
                    help=f"comma list from {', '.join(ALL_FIELDS)}")
    ap.add_argument("--drafts-only", action="store_true", help="leave approved entries alone")
    ap.add_argument("--limit", type=int, default=0, help="stop after N papers")
    ap.add_argument("--papers-dir", type=Path, default=ROOT / "papers")
    ap.add_argument("--model", default=None, help="default: the extract role in models.yaml")
    ap.add_argument("--from-response", type=Path, default=None,
                    help="apply a saved model response (one --citation) instead of calling the model")
    args = ap.parse_args(argv)

    wanted = tuple(x.strip() for x in args.fields.split(",") if x.strip())
    bad = [x for x in wanted if x not in ALL_FIELDS]
    if bad:
        ap.error(f"unknown field(s): {bad}")
    only = {("@" + c.lstrip("@")).lower() for c in args.citation} if args.citation else None
    papers = collect(ROOT, wanted, only, include_canonical=not args.drafts_only)
    order = sorted(papers, key=lambda c: c.lower())
    if args.limit:
        order = order[: args.limit]
    n_find = sum(len(papers[c]) for c in order)
    print(f"{len(order)} paper(s), {n_find} finding(s) with missing fields ({', '.join(wanted)})")
    for c in order:
        miss = sorted({m for t in papers[c] for m in t["missing"]})
        where = "approved + drafts" if any(t["canonical"] for t in papers[c]) and \
            not all(t["canonical"] for t in papers[c]) else (
            "approved" if papers[c][0]["canonical"] else "drafts")
        has_pdf = find_paper(c, args.papers_dir) is not None
        print(f"  {c:28} {len(papers[c]):3} finding(s)  {where:18} {', '.join(miss)}"
              + ("" if has_pdf else "   ✗ no PDF"))
    if not args.execute and not args.from_response:
        print("\nDry run. Add --execute to ask the model and write the verified values.")
        return 0
    if args.from_response and len(order) != 1:
        ap.error("--from-response needs exactly one --citation")

    from extract import DEFAULT_OLLAMA_HOST
    from model_config import resolve
    model = resolve("extract", args.model)["model"]
    t0 = time.monotonic()
    tot_w = tot_s = 0
    for i, c in enumerate(order, 1):
        started = dt.datetime.now()
        print(f"\n=== [{i}/{len(order)}] {c}  ({len(papers[c])} finding(s))  started {started:%H:%M:%S}")
        try:
            w, s = run_paper(c, papers[c], args.papers_dir, model, DEFAULT_OLLAMA_HOST,
                             execute=True, response_file=args.from_response)
        except Exception as e:  # noqa: BLE001 — one paper must not stop the batch
            print(f"  ❌ {c}: {e}")
            continue
        tot_w += w
        tot_s += s
        elapsed = time.monotonic() - t0
        left = elapsed / i * (len(order) - i)
        print(f"  ✓ {w} value(s) written, {s} not written · "
              f"{elapsed / 60:.0f} min so far, ~{left / 60:.0f} min left")
    print(f"\nDone: {tot_w} value(s) written, {tot_s} left for the loader to infer "
          f"(no verified quote). Review: git diff aphasia-kb/")
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
