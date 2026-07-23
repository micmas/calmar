"""
aphasia_kb_rag.py — imaging-driven RAG over the aphasia knowledge base.

Given a binary lesion mask in MNI space, this module:

  1. Decodes the lesion to HarvardOxford region overlaps + Neurosynth term
     correlations  (reuses ``decode_lesion.decode_lesion``).
  2. Retrieves the relevant curated findings from the KB
     (reuses ``aphasia_kb.KnowledgeBase``). The join is mostly structured:
     ``region_overlap.kb_region_id`` already names a KB region id, and
     ``term_decoding.impairment`` already names a KB impairment id.
  3. Produces TWO outputs from the *same* retrieved evidence:
       a. a deterministic, fully-cited markdown report  (always; offline),
       b. an optional LLM narrative grounded in (a)      (local, via Ollama).

Design notes
------------
* No outcome/behavioural labels are needed — the imaging itself (via region
  overlap) is the retrieval key. This is retrieval-augmented *explanation*,
  not a trained predictor.
* The KB is small (~60 entries from ~40 papers) and a proof-of-concept.
  The deterministic report never invents anything; the LLM step is
  instructed to use ONLY the provided evidence and to cite entry ids. Both
  carry a research-only, not-clinical-advice caveat.
* The LLM step runs entirely locally against Ollama — no API key, no
  network. Patient-derived lesion data never leaves the machine, which
  matters more here than anywhere else in this repo.
* Which model it uses comes from ``models.yaml`` (role: ``rag``).

CLI
---
    python aphasia_kb_rag.py /path/to/Lesion_in_MNI.nii.gz            # report only
    python aphasia_kb_rag.py /path/to/Lesion_in_MNI.nii.gz --llm     # + LLM narrative
    python aphasia_kb_rag.py /path/to/Lesion_in_MNI.nii.gz -o out.md
"""

from __future__ import annotations

import math
import os
import sys
from pathlib import Path
from typing import Any, Optional

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

# Default KB root = the directory this file lives in.
DEFAULT_KB_ROOT = Path(__file__).resolve().parent

# Model for the (optional) LLM synthesis step comes from models.yaml
# (role: `rag`). Override per-run with --model or APHASIA_RAG_MODEL.
sys.path.insert(0, str(DEFAULT_KB_ROOT))
from model_config import resolve as resolve_model  # noqa: E402

DEFAULT_MODEL = resolve_model("rag")["model"]

# Relative confidence weight by `direction` value (unknown -> 0.5). Used only
# to RANK findings for display; it never changes their wording.
DIRECTION_WEIGHTS = {
    "definite": 1.0, "established": 1.0, "strong": 1.0,
    "likely": 0.8, "probable": 0.8,
    "possible": 0.6, "mixed": 0.5, "unclear": 0.4,
    "contested": 0.3, "unlikely": 0.2, "refuted": 0.1,
}

RESEARCH_CAVEAT = (
    "Research/decision-support only — not a clinical diagnosis or treatment "
    "recommendation. Every statement is sourced from a small, proof-of-concept "
    "literature KB and needs clinician verification."
)


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def _clean(v: Any) -> Any:
    """Coerce pandas NaN / empty placeholders to None."""
    if v is None:
        return None
    try:
        if isinstance(v, float) and math.isnan(v):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(v, str):
        s = v.strip()
        if not s or s.lower() in ("not_reported", "nan", "none", "n/a"):
            return None
        return s
    return v


def _short(v: Any, n: int = 280) -> str:
    s = "" if v is None else str(v)
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def _name_for(kb, entry_id: str) -> str:
    """Best-effort display name for a KB entry id across all buckets."""
    for df in (getattr(kb, "regions", None), getattr(kb, "impairments", None),
               getattr(kb, "therapies", None), getattr(kb, "predictors", None),
               getattr(kb, "ingredients", None)):
        if df is None or getattr(df, "empty", True) or "id" not in df.columns:
            continue
        hit = df[df["id"] == entry_id]
        if not hit.empty:
            row = hit.iloc[0]
            return str(row.get("name") or entry_id)
    return entry_id


# --------------------------------------------------------------------------
# KB loading
# --------------------------------------------------------------------------

def load_kb(kb_root: str | Path | None = None, include=("approved",)):
    """Load the KnowledgeBase. Imported lazily so the rest of the module is
    usable in environments without pandas/yaml installed."""
    root = Path(kb_root) if kb_root else DEFAULT_KB_ROOT
    sys.path.insert(0, str(root))
    from aphasia_kb import KnowledgeBase  # noqa: E402
    return KnowledgeBase(root, include=include)


# --------------------------------------------------------------------------
# Retrieval
# --------------------------------------------------------------------------

def _findings_for_source(kb, source_id: str) -> list[dict]:
    """All findings whose source entry is `source_id` (uses the long table)."""
    f = getattr(kb, "findings", None)
    if f is None or f.empty or "source_id" not in f.columns:
        return []
    sub = f[f["source_id"] == source_id]
    return [r.to_dict() for _, r in sub.iterrows()]


def _findings_targeting(kb, target_id: str) -> list[dict]:
    """All findings that point AT `target_id` (e.g. a region finding whose
    target is this impairment)."""
    f = getattr(kb, "findings", None)
    if f is None or f.empty or "target" not in f.columns:
        return []
    sub = f[f["target"] == target_id]
    return [r.to_dict() for _, r in sub.iterrows()]


def _finding_record(kb, f: dict, *, base_score: float, reason: str) -> dict:
    direction = _clean(f.get("direction"))
    dw = DIRECTION_WEIGHTS.get(str(direction).lower(), 0.5) if direction else 0.5
    return {
        "source_id":     f.get("source_id"),
        "source_name":   _name_for(kb, f.get("source_id")),
        "source_kind":   _clean(f.get("source_kind")),
        "finding_id":    _clean(f.get("id")),
        "target":        _clean(f.get("target")),
        "target_kind":   _clean(f.get("target_kind")),
        "target_name":   _name_for(kb, f.get("target")) if _clean(f.get("target")) else None,
        "claim":         _clean(f.get("claim")),
        "direction":     direction,
        "citation":      _clean(f.get("citation")),
        "method":        _clean(f.get("method")),
        "design":        _clean(f.get("design")),
        "sample_n":      _clean(f.get("sample_n")),
        "effect_size":   _clean(f.get("stat_effect_size")),
        "match_reason":  reason,
        "score":         round(float(base_score) * dw, 3),
    }


def retrieve(decode_result: dict, kb, *,
             min_overlap_pct: float = 1.0,
             min_term_r: float = 0.0,
             max_findings: int = 40) -> dict:
    """Turn a ``decode_lesion`` result into a ranked bundle of KB evidence.

    Returns a dict with keys: ``regions``, ``terms``, ``findings``, ``kb_meta``.
    """
    region_df = decode_result.get("region_overlap")
    term_df   = decode_result.get("term_decoding")

    # ---- 1. Matched KB regions (from HarvardOxford overlap) --------------
    matched_regions: list[dict] = []
    seen_region_ids: dict[str, dict] = {}
    if region_df is not None and not region_df.empty:
        for _, row in region_df.iterrows():
            pct = float(row.get("overlap_pct") or 0.0)
            if pct < min_overlap_pct:
                continue
            kb_id = _clean(row.get("kb_region_id"))
            rec = {
                "kb_region_id": kb_id,
                "ho_label":     _clean(row.get("ho_label")),
                "hemisphere":   _clean(row.get("hemisphere")),
                "overlap_pct":  pct,
                "overlap_voxels": int(row.get("overlap_voxels") or 0),
                "kb_name":      _name_for(kb, kb_id) if kb_id else None,
                "in_kb":        bool(kb_id),
            }
            matched_regions.append(rec)
            # keep the largest overlap per KB region id
            if kb_id and (kb_id not in seen_region_ids
                          or pct > seen_region_ids[kb_id]["overlap_pct"]):
                seen_region_ids[kb_id] = rec

    # ---- 2. Matched terms / impairments (from Neurosynth correlation) ----
    matched_terms: list[dict] = []
    impairment_hits: dict[str, float] = {}
    if term_df is not None and not term_df.empty:
        for _, row in term_df.iterrows():
            r = float(row.get("r") or 0.0)
            if r <= min_term_r:
                continue
            imp = _clean(row.get("impairment"))
            matched_terms.append({
                "term":        _clean(row.get("term")),
                "r":           round(r, 4),
                "impairment":  imp,
                "impairment_name": _name_for(kb, imp) if imp else None,
            })
            if imp:
                impairment_hits[imp] = max(impairment_hits.get(imp, 0.0), r)

    # ---- 3. Gather findings ---------------------------------------------
    findings: list[dict] = []
    dedup: set[tuple] = set()

    def _add(rec: dict):
        key = (rec["source_id"], rec["finding_id"], rec["target"])
        if key in dedup:
            return
        dedup.add(key)
        findings.append(rec)

    # 3a. Findings authored by each matched region (region -> impairment/...)
    for kb_id, rinfo in seen_region_ids.items():
        base = rinfo["overlap_pct"] / 100.0
        reason = (f"Lesion overlaps {rinfo['ho_label']} "
                  f"({rinfo['overlap_pct']:.0f}%) → KB region '{kb_id}'")
        for f in _findings_for_source(kb, kb_id):
            _add(_finding_record(kb, f, base_score=base, reason=reason))

    # 3b. Findings authored by, or pointing at, each term-implicated impairment
    for imp_id, r in impairment_hits.items():
        base = min(max(r, 0.0), 1.0)
        reason = f"Neurosynth term match → KB impairment '{imp_id}' (r={r:.2f})"
        for f in _findings_for_source(kb, imp_id):
            _add(_finding_record(kb, f, base_score=base, reason=reason))
        for f in _findings_targeting(kb, imp_id):
            _add(_finding_record(kb, f, base_score=base * 0.9, reason=reason))

    findings.sort(key=lambda d: d["score"], reverse=True)
    findings = findings[:max_findings]

    kb_meta = {
        "n_regions":     int(getattr(kb, "regions", _empty()).shape[0]),
        "n_impairments": int(getattr(kb, "impairments", _empty()).shape[0]),
        "n_therapies":   int(getattr(kb, "therapies", _empty()).shape[0]),
        "n_predictors":  int(getattr(kb, "predictors", _empty()).shape[0]),
        "n_findings":    int(getattr(kb, "findings", _empty()).shape[0]),
    }

    return {
        "regions":  matched_regions,
        "terms":    matched_terms,
        "findings": findings,
        "kb_meta":  kb_meta,
    }


def _empty():
    import pandas as pd
    return pd.DataFrame()


# --------------------------------------------------------------------------
# Deterministic report (always produced)
# --------------------------------------------------------------------------

def render_report(retrieval: dict, *,
                  lesion_path: str | None = None,
                  lesion_voxels: int | None = None) -> str:
    """Build a deterministic, fully-cited markdown report from retrieval."""
    L: list[str] = []
    L.append("# Aphasia KB decoding report")
    L.append("")
    if lesion_path:
        L.append(f"**Lesion:** `{lesion_path}`")
    if lesion_voxels is not None:
        L.append(f"**Lesion size:** {lesion_voxels:,} voxels")
    km = retrieval.get("kb_meta", {})
    L.append(f"**KB coverage:** {km.get('n_regions', 0)} regions · "
             f"{km.get('n_impairments', 0)} impairments · "
             f"{km.get('n_therapies', 0)} therapies · "
             f"{km.get('n_predictors', 0)} predictors "
             f"({km.get('n_findings', 0)} findings)")
    L.append("")
    L.append(f"> {RESEARCH_CAVEAT}")
    L.append("")

    # --- Regions ---
    regions = retrieval.get("regions", [])
    L.append("## Lesioned regions (HarvardOxford overlap)")
    L.append("")
    if not regions:
        L.append("_No atlas regions overlapped the lesion above threshold._")
    else:
        for r in regions:
            tag = (f"→ KB region **{r['kb_name']}** (`{r['kb_region_id']}`)"
                   if r.get("in_kb") else "_(no KB region linked)_")
            L.append(f"- **{r['ho_label']}** "
                     f"[{r['hemisphere']}], {r['overlap_pct']:.0f}% of lesion "
                     f"({r['overlap_voxels']:,} vox) {tag}")
    L.append("")

    # --- Terms ---
    terms = retrieval.get("terms", [])
    if terms:
        L.append("## Neurosynth term associations (positive correlation)")
        L.append("")
        for t in terms[:12]:
            imp = (f" → impairment **{t['impairment_name']}** "
                   f"(`{t['impairment']}`)" if t.get("impairment") else "")
            L.append(f"- _{t['term']}_  (r = {t['r']:.2f}){imp}")
        L.append("")

    # --- Findings ---
    findings = retrieval.get("findings", [])
    L.append("## Retrieved KB findings")
    L.append("")
    if not findings:
        L.append("_No KB findings matched this lesion. The KB may not yet "
                 "cover the affected regions — consider extracting more papers._")
    else:
        # group by source entry for readability
        by_source: dict[str, list[dict]] = {}
        order: list[str] = []
        for f in findings:
            key = f"{f['source_name']} (`{f['source_id']}`)"
            if key not in by_source:
                by_source[key] = []
                order.append(key)
            by_source[key].append(f)
        for key in order:
            L.append(f"### {key}")
            L.append("")
            for f in by_source[key]:
                tgt = ""
                if f.get("target_name"):
                    tgt = f" · **{f['target_kind'] or 'target'}:** {f['target_name']}"
                bits = []
                if f.get("direction"):
                    bits.append(f"direction: {f['direction']}")
                if f.get("method"):
                    bits.append(f"method: {f['method']}")
                if f.get("sample_n"):
                    bits.append(f"n = {f['sample_n']}")
                meta = (" · ".join(bits))
                cite = f" [{f['citation']}]" if f.get("citation") else ""
                L.append(f"- {_short(f.get('claim'))}{cite}{tgt}")
                if meta:
                    L.append(f"  <br><sub>{meta}</sub>")
                if f.get("effect_size"):
                    L.append(f"  <br><sub>effect: {_short(f['effect_size'], 200)}</sub>")
                L.append(f"  <br><sub>matched because: {f['match_reason']}</sub>")
            L.append("")

    return "\n".join(L).rstrip() + "\n"


# --------------------------------------------------------------------------
# Optional LLM synthesis (grounded in the retrieved evidence)
# --------------------------------------------------------------------------

def build_llm_prompt(retrieval: dict) -> tuple[str, str]:
    """Return (system_prompt, user_prompt) for the synthesis step."""
    system = (
        "You are a careful neuropsychology research assistant. You will be "
        "given a structured list of EVIDENCE items retrieved from a curated "
        "aphasia knowledge base for one patient's lesion. Write a concise "
        "clinical-research summary of what the literature in this evidence "
        "implies about likely language impairments, therapy considerations, "
        "and prognostic predictors.\n\n"
        "HARD RULES:\n"
        "1. Use ONLY the evidence provided. Do not add facts, regions, or "
        "claims that are not present in it. If the evidence is thin or "
        "absent, say so plainly.\n"
        "2. After every statement, cite the supporting source id and citation "
        "key in square brackets, e.g. [left_ifg_pars_opercularis · @Fridriksson2018].\n"
        "3. Distinguish strength of evidence using each item's `direction` and "
        "sample size; do not overstate.\n"
        "4. End with one sentence reminding the reader this is research "
        "decision-support, not a clinical diagnosis.\n"
        "Keep it under ~350 words."
    )

    lines = ["EVIDENCE ITEMS:"]
    regions = retrieval.get("regions", [])
    if regions:
        rtxt = ", ".join(
            f"{r['ho_label']} ({r['overlap_pct']:.0f}%"
            + (f", KB:{r['kb_region_id']}" if r.get("in_kb") else "") + ")"
            for r in regions
        )
        lines.append(f"- Lesioned regions: {rtxt}")
    for i, f in enumerate(retrieval.get("findings", []), 1):
        parts = [f"[{i}] source={f['source_id']}"]
        if f.get("target"):
            parts.append(f"target={f['target_kind']}:{f['target']}")
        if f.get("direction"):
            parts.append(f"direction={f['direction']}")
        if f.get("sample_n"):
            parts.append(f"n={f['sample_n']}")
        if f.get("citation"):
            parts.append(f"cite={f['citation']}")
        head = " ".join(parts)
        lines.append(f"- {head}\n    claim: {_short(f.get('claim'), 400)}")
        if f.get("effect_size"):
            lines.append(f"    effect: {_short(f['effect_size'], 200)}")
    if not retrieval.get("findings"):
        lines.append("- (no findings retrieved)")
    user = "\n".join(lines)
    return system, user


def llm_summary(retrieval: dict, *,
                model: str | None = None,
                host: str | None = None,
                max_tokens: int | None = None) -> dict:
    """Generate a grounded narrative with a LOCAL model via Ollama.

    Returns ``{"text": str|None, "backend": str|None, "model": str|None,
    "error": str|None}``.

    Never raises — returns an ``error`` string instead, so a missing or
    unreachable model never blocks the deterministic report path, which
    is the actual product here. The narrative is a convenience layer on
    top of evidence that has already been retrieved and cited.
    """
    cfg = resolve_model("rag", model)
    model = cfg["model"]
    max_tokens = max_tokens or cfg["max_tokens"]
    system, user = build_llm_prompt(retrieval)

    try:
        from ollama_client import DEFAULT_HOST, OllamaError, chat
    except ImportError as ex:
        return {"text": None, "backend": None, "model": model,
                "error": f"ollama_client unavailable: {ex}"}

    try:
        res = chat(user, model=model, system=system, max_tokens=max_tokens,
                   host=host or DEFAULT_HOST, temperature=0.2,
                   num_ctx=cfg["num_ctx"], verbose=False)
    except OllamaError as ex:
        return {"text": None, "backend": "ollama", "model": model,
                "error": str(ex)}
    except Exception as ex:  # noqa: BLE001
        return {"text": None, "backend": "ollama", "model": model,
                "error": f"{type(ex).__name__}: {ex}"}

    text = (res.get("text") or "").strip()
    if not text:
        return {"text": None, "backend": "ollama", "model": model,
                "error": "empty response from local model"}
    # A truncated narrative can read as complete while silently dropping
    # findings — flag it rather than presenting it as the whole picture.
    if res.get("truncated_output"):
        text += ("\n\n_(Narrative truncated at the token limit — the "
                 "deterministic report above is complete.)_")
    return {"text": text, "backend": "ollama", "model": model, "error": None}


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def decode_and_explain(lesion_path: str | Path,
                       kb_root: str | Path | None = None, *,
                       use_llm: bool = False,
                       model: str | None = None,
                       host: str | None = None,
                       min_overlap_pct: float = 1.0,
                       min_term_r: float = 0.0,
                       max_findings: int = 40,
                       decode_kwargs: dict | None = None) -> dict:
    """End-to-end: decode the lesion, retrieve KB evidence, build the report,
    and (optionally) an LLM narrative.

    Returns ``{decode, retrieval, report_md, llm}``. ``decode_lesion`` and the
    LLM SDKs are imported lazily so this module loads cheaply.
    """
    from decode_lesion import decode_lesion  # lazy: needs nibabel/nilearn

    decode = decode_lesion(str(lesion_path), **(decode_kwargs or {}))
    kb = load_kb(kb_root)
    retrieval = retrieve(decode, kb,
                         min_overlap_pct=min_overlap_pct,
                         min_term_r=min_term_r,
                         max_findings=max_findings)
    report_md = render_report(
        retrieval,
        lesion_path=str(lesion_path),
        lesion_voxels=decode.get("lesion_voxels"),
    )
    llm = None
    if use_llm:
        llm = llm_summary(retrieval, model=model, host=host)
        if llm.get("text"):
            report_md += ("\n\n---\n\n## LLM narrative "
                          f"<sub>({llm['backend']} · {llm['model']} · "
                          f"local)</sub>\n\n"
                          f"{llm['text']}\n")
        else:
            report_md += ("\n\n---\n\n## LLM narrative\n\n"
                          f"_Not generated: {llm.get('error')}_\n")
    return {"decode": decode, "retrieval": retrieval,
            "report_md": report_md, "llm": llm}


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _cli(argv=None):
    import argparse
    ap = argparse.ArgumentParser(
        description="Imaging-driven RAG over the aphasia knowledge base.")
    ap.add_argument("lesion", help="Binary lesion mask in MNI space (.nii.gz)")
    ap.add_argument("--kb-root", default=None, help="KB directory (default: this file's dir)")
    ap.add_argument("--llm", action="store_true", help="Also generate the LLM narrative")
    ap.add_argument("--model", default=None,
                    help=f"Ollama model tag. Default from models.yaml "
                         f"(currently {DEFAULT_MODEL}).")
    ap.add_argument("--ollama-host", default=None,
                    help="Ollama base URL (default: http://localhost:11434).")
    ap.add_argument("--min-overlap-pct", type=float, default=1.0)
    ap.add_argument("--min-term-r", type=float, default=0.0)
    ap.add_argument("-o", "--output", default=None, help="Write the report markdown here")
    args = ap.parse_args(argv)

    res = decode_and_explain(
        args.lesion, args.kb_root,
        use_llm=args.llm, model=args.model, host=args.ollama_host,
        min_overlap_pct=args.min_overlap_pct, min_term_r=args.min_term_r,
    )
    if args.output:
        Path(args.output).write_text(res["report_md"], encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(res["report_md"])


if __name__ == "__main__":
    _cli()
