"""
lesion_mapping.py — how a lesion-mapping finding was obtained (v2.7),
and which cohort it came from.

Lesion-symptom mapping results depend heavily on design. Moore et al.
2026 (Hum Brain Mapp 47:e70619) ran 384,780 simulated analyses on 959
clinical scans: accuracy varied widely with the sample, the lesion-
volume correction (direct total lesion volume control was best on
every measure), the multiple-comparison correction (FDR gave the best
coverage of the true correlate, permutation the best Dice) and
univariate vs multivariate analysis. A 40-patient uncorrected VLSM and
a 900-patient multivariate analysis with volume control are therefore
different kinds of evidence, and the KB must not present them alike.

`lesion_mapping` (finding level, v2.7) records the design:

    analysis                  univariate | multivariate | region_based
                              | network | not_reported
    n_analysed                int | not_reported   (may differ from sample.n)
    min_lesion_overlap        free text, e.g. ">= 5 patients" | not_reported
    lesion_volume_correction  direct | covariate | none | not_reported
    multiple_comparisons      permutation_fwe | fwe | cluster_fwe | fdr
                              | bonferroni | uncorrected | not_reported

`sample.cohort` (v2.7) names the dataset when it is a known or reused
one ("ARC", "OCS", "PLORAS", a trial ID), so findings from the same
patients are not counted as independent replications.

Entries written before v2.7 have neither; `finding_lesion_mapping()`
and `finding_cohort()` infer what the existing text supports (method,
statistics.threshold, confounders_controlled, population) and say so
(`source = "inferred"`); values written by backfill.py from the paper
(quote-checked, `filled.fields` on the finding) are `source = "filled"`.
Nothing is guessed beyond that text: a field
the text does not settle stays `not_reported`.
"""
from __future__ import annotations

import re

LESION_METHODS = {"LSM", "VLSM", "RLSM", "MLPA", "VBCM",
                  "lesion_network_mapping", "disconnectome"}
ANALYSIS_VOCAB = {"univariate", "multivariate", "region_based", "network", "not_reported"}
VOLUME_VOCAB = {"direct", "covariate", "none", "not_reported"}
CORRECTION_VOCAB = {"permutation_fwe", "fwe", "cluster_fwe", "fdr", "bonferroni",
                    "uncorrected", "not_reported"}
FIELDS = ("analysis", "n_analysed", "min_lesion_overlap",
          "lesion_volume_correction", "multiple_comparisons")

_BY_METHOD = {"VLSM": "univariate", "VBCM": "univariate", "MLPA": "multivariate",
              "MVPA": "multivariate", "RLSM": "region_based",
              "lesion_network_mapping": "network", "disconnectome": "network"}

# Known, reused cohorts. Pattern on population / recruitment text → name.
KNOWN_COHORTS = (
    (r"\baphasia recovery cohort\b|(?-i:\bARC\b)", "ARC"),
    (r"\bPLORAS\b", "PLORAS"),
    (r"\boxford cognitive scree|\bOCS[- ]?(care|bridge)?\b", "OCS"),
    (r"\bSTROKOG\b", "STROKOG"),
    (r"\bmeta[- ]?VCI[- ]?map\b", "Meta VCI Map"),
    (r"\bmoss rehabilitation|\bMRRI\b", "Moss Rehabilitation Research Institute"),
    (r"\bC-STAR\b|center for the study of aphasia recovery", "C-STAR"),
    (r"\bISLES\b", "ISLES"),
    (r"\b(NCT\d{8})\b", None),          # trial registration: use the ID itself
)


def _methods(f: dict) -> list[str]:
    m = f.get("method")
    return [str(x) for x in (m if isinstance(m, list) else [m]) if x]


def is_lesion_mapping(f: dict) -> bool:
    return any(m in LESION_METHODS for m in _methods(f))


def _infer_correction(text: str) -> str:
    t = text.lower()
    if "uncorrected" in t:
        return "uncorrected"
    if "permutation" in t or "liebermeister" in t and "family" in t:
        return "permutation_fwe"
    if "fdr" in t or "false discovery" in t:
        return "fdr"
    if "bonferroni" in t or "holm" in t:
        return "bonferroni"
    if "cluster" in t and ("fwe" in t or "family" in t):
        return "cluster_fwe"
    if "fwe" in t or "family-wise" in t or "familywise" in t:
        return "fwe"
    return "not_reported"


def _infer_volume(texts: list[str]) -> str:
    t = " ".join(texts).lower()
    if re.search(r"\bd?tlvc\b|direct (total )?lesion volume", t):
        return "direct"
    if re.search(r"lesion (volume|size|load)", t):
        return "covariate"
    return "not_reported"


def _infer_analysis(f: dict, threshold: str) -> str:
    for m in _methods(f):
        if m in _BY_METHOD:
            return _BY_METHOD[m]
    t = threshold.lower()
    if re.search(r"sccan|multivariate|support vector|svr|machine learning", t):
        return "multivariate"
    return "not_reported"


def finding_lesion_mapping(f: dict) -> tuple[dict | None, str]:
    """(design dict, 'stated' | 'inferred') — None for non-lesion findings."""
    if not is_lesion_mapping(f):
        return None, ""
    stated = f.get("lesion_mapping")
    if isinstance(stated, dict) and stated:
        out = {k: stated.get(k, "not_reported") for k in FIELDS}
        filled = (f.get("filled") or {}).get("fields") or []
        return out, ("filled" if "lesion_mapping" in filled else "stated")
    thr = str((f.get("statistics") or {}).get("threshold") or "")
    conf = [str(c) for c in (f.get("confounders_controlled") or [])]
    n = (f.get("sample") or {}).get("n", "not_reported")
    return {
        "analysis": _infer_analysis(f, thr),
        "n_analysed": n if isinstance(n, int) else "not_reported",
        "min_lesion_overlap": "not_reported",
        "lesion_volume_correction": _infer_volume(conf + [thr]),
        "multiple_comparisons": _infer_correction(thr),
    }, "inferred"


def orientation(lm: dict | None) -> str:
    """Moore 2026: FDR maximises coverage of the true correlate
    (sensitivity); permutation / FWE maximise spatial precision
    (specificity)."""
    if not lm:
        return ""
    mc = lm.get("multiple_comparisons")
    if mc in ("fdr", "uncorrected"):
        return "sensitivity"
    if mc in ("permutation_fwe", "fwe", "cluster_fwe", "bonferroni"):
        return "specificity"
    return ""


def design_cautions(lm: dict | None) -> list[str]:
    """Plain-language cautions a reader should see next to the finding."""
    if not lm:
        return []
    out = []
    vol = lm.get("lesion_volume_correction")
    if vol == "none":
        out.append("lesion volume not controlled")
    elif vol == "not_reported":
        out.append("lesion-volume control not stated")
    mc = lm.get("multiple_comparisons")
    if mc == "uncorrected":
        out.append("no correction for multiple comparisons")
    elif mc == "not_reported":
        out.append("multiple-comparison correction not stated")
    n = lm.get("n_analysed")
    if lm.get("analysis") == "multivariate" and isinstance(n, int) and n < 100:
        out.append(f"multivariate analysis with n = {n} (< 100)")
    elif isinstance(n, int) and n < 30:
        out.append(f"small sample (n = {n})")
    return out


def finding_cohort(f: dict) -> tuple[str | None, str]:
    """(cohort name, 'stated' | 'inferred' | '') for one finding."""
    s = f.get("sample") or {}
    c = s.get("cohort")
    if c and str(c).strip().lower() not in ("not_reported", "none", ""):
        filled = (f.get("filled") or {}).get("fields") or []
        return str(c).strip(), ("filled" if "cohort" in filled else "stated")
    text = " ".join(str(s.get(k) or "") for k in ("population", "recruitment"))
    for pat, name in KNOWN_COHORTS:
        m = re.search(pat, text, re.I)
        if m:
            return (name or m.group(1).upper()), "inferred"
    return None, ""


_OVERLAP = re.compile(r"cohort overlaps with (@[\w\-]+)", re.I)


def cohort_groups(rows: list[dict]) -> dict[str, str]:
    """citation → group label. Papers are joined when they share a
    cohort name or one flags `cohort overlaps with @Other`; a paper
    joined to nothing is its own group. Used to count independent
    evidence instead of findings."""
    parent: dict[str, str] = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    by_cohort: dict[str, str] = {}
    names: dict[str, str] = {}
    for r in rows:
        cit = r.get("citation")
        if not cit:
            continue
        find(cit)
        c = r.get("cohort")
        if c:
            names.setdefault(cit, c)
            if c in by_cohort:
                union(cit, by_cohort[c])
            else:
                by_cohort[c] = cit
        for other in _OVERLAP.findall(" ".join(r.get("flags") or [])):
            union(cit, other)
    groups: dict[str, list[str]] = {}
    for cit in list(parent):
        groups.setdefault(find(cit), []).append(cit)
    label = {}
    for root, members in groups.items():
        cohort = next((names[m] for m in sorted(members) if m in names), None)
        lab = cohort or (" + ".join(sorted(members)) if len(members) > 1 else root)
        for m in members:
            label[m] = lab
    return label
