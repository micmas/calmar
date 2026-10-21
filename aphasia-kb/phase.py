"""
phase.py — recovery phase of a finding's sample (acute … chronic).

Lesion–symptom relationships, predictors and treatment effects differ
by time since stroke: an acute hypoperfusion map (Hillis2004) and a
chronic VLSM (Henseler2014) are different kinds of evidence about the
same region. Until v2.6 the KB recorded this only as free text in
`sample.time_post_onset` ("mean 40.1 months", "median 7 days"), which
nothing could filter on. `sample.phase` makes it a controlled value.

Bands follow the Stroke Recovery and Rehabilitation Roundtable
(Bernhardt et al. 2017, Int J Stroke 12:444):

    hyperacute       0–24 h
    acute            1–7 days
    early_subacute   7 days – 3 months
    late_subacute    3–6 months
    chronic          > 6 months
    mixed            the sample spans bands and no band dominates
    longitudinal     the same patients measured at ≥ 2 phases
    not_reported     the paper does not say (or healthy controls)

`infer_phase(time_post_onset)` turns the free text into a band
deterministically, so existing entries get a value without re-reading
the paper, and the extractor's own value can be checked against the
text it quotes. A lower bound of ≥ 6 months wins over a mean; a range
that straddles bands is `mixed`; two time points is `longitudinal`.
"""
from __future__ import annotations

import re

PHASE_VOCAB = {"hyperacute", "acute", "early_subacute", "late_subacute",
               "chronic", "mixed", "longitudinal", "not_reported"}

# upper bound of each band in days (SRRR)
_BANDS = (("hyperacute", 1), ("acute", 7), ("early_subacute", 92),
          ("late_subacute", 182), ("chronic", 10 ** 9))

_UNIT_DAYS = {"h": 1 / 24, "hr": 1 / 24, "hour": 1 / 24, "hours": 1 / 24,
              "d": 1, "day": 1, "days": 1,
              "wk": 7, "wks": 7, "week": 7, "weeks": 7,
              "mo": 30.4, "mos": 30.4, "month": 30.4, "months": 30.4,
              "y": 365, "yr": 365, "yrs": 365, "year": 365, "years": 365}
_NUM_UNIT = re.compile(
    r"(?P<num>\d+(?:\.\d+)?)\s*(?:-|–|to)?\s*(?P<num2>\d+(?:\.\d+)?)?\s*"
    r"(?P<unit>hours?|hrs?|h\b|days?|d\b|weeks?|wks?|months?|mos?\b|years?|yrs?|y\b)",
    re.I)


def band_of(days: float) -> str:
    for name, upper in _BANDS:
        if days <= upper:
            return name
    return "chronic"


def infer_phase(text: str | None) -> tuple[str, str]:
    """(phase, basis). basis says which rule fired, for the review note."""
    if not text:
        return "not_reported", "no time_post_onset"
    t = str(text).lower().replace("≥", ">=").replace("≤", "<=")
    if "not_reported" in t or "healthy" in t or t.strip() in ("none", "n/a", "na"):
        return "not_reported", "stated as not reported / healthy controls"

    # two or more measurement points on the same patients
    if re.search(r"\b(t1|t2|baseline|follow-?up)\b.*\b(t2|t3|follow-?up|months? later)\b", t) \
            or re.search(r"\band\b.*\bpost-?(stroke|onset)", t) and t.count("post") >= 2 \
            or "longitudinal" in t:
        return "longitudinal", "two or more time points"

    spans = []   # (lo_days, hi_days)
    for m in _NUM_UNIT.finditer(t):
        unit = m.group("unit").lower().rstrip(".")
        unit = unit if unit in _UNIT_DAYS else unit.rstrip("s")
        f = _UNIT_DAYS.get(unit) or _UNIT_DAYS.get(unit + "s")
        if not f:
            continue
        lo = float(m.group("num")) * f
        hi = float(m.group("num2")) * f if m.group("num2") else lo
        spans.append((lo, hi, m.start()))

    # an explicit lower bound settles it: ">= 6 months", "all > 6 months", "minimum 12 months"
    for lo, hi, pos in spans:
        head = t[max(0, pos - 14):pos]
        if re.search(r"(>=|>|≥|at least|minimum|min\.?|all\s*>|over|more than|beyond)\s*$", head) \
                or re.search(r"\b(chronic|post-?stroke)\b", t[pos:pos + 40]) and lo >= 182:
            if lo >= 182:
                return "chronic", f"lower bound {text!r}"

    if not spans:
        if "chronic" in t:
            return "chronic", "the word 'chronic'"
        if "subacute" in t:
            return "early_subacute", "the word 'subacute'"
        if "acute" in t:
            return "acute", "the word 'acute'"
        return "not_reported", "no time found"

    # a stated range that straddles bands → mixed, unless a mean/median is given
    central = None
    for lo, hi, pos in spans:
        head = t[max(0, pos - 12):pos]
        if re.search(r"(mean|median|average|mdn|m\s*=)\s*$", head):
            central = lo
            break
    ranges = [(lo, hi) for lo, hi, _ in spans if hi > lo]
    if ranges and central is None:
        lo, hi = ranges[0]
        if band_of(lo) != band_of(hi):
            return "mixed", f"range {text!r} straddles bands"
        return band_of(lo), f"range {text!r}"
    value = central if central is not None else spans[0][0]
    phase = band_of(value)
    if "chronic" in t and phase != "chronic":
        # "chronic (… 1 year after therapy)" — the word is about the sample,
        # the number about something else; trust the word unless a mean
        # or median contradicts it
        if central is None:
            return "chronic", "the word 'chronic'"
        return "mixed", f"says chronic but mean/median {value:.0f} d"
    return phase, f"{'mean/median' if central is not None else 'value'} {value:.0f} days"


def finding_phase(finding: dict) -> tuple[str, str]:
    """(phase, source) for a finding: stated `sample.phase` wins, else
    inferred from `sample.time_post_onset`."""
    sample = finding.get("sample") or {}
    stated = sample.get("phase")
    if stated in PHASE_VOCAB:
        return stated, "stated"
    phase, _ = infer_phase(sample.get("time_post_onset"))
    return phase, "inferred" if phase != "not_reported" else "none"
