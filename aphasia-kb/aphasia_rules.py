"""
aphasia_rules.py — the fixed clinical/display rules used by the participant report.

These rules used to live inline in the notebook's report cell. They are kept
here, next to the knowledge base, so they can be read, cited and unit-tested
(``tests/test_aphasia_rules.py``) and shown to the reader as tables
(:func:`rules_tables`).

Nothing in this module reads patient data or images. Each rule states where it
comes from; rules that are project heuristics without a published source say so
explicitly.

Contents
--------
* WAB aphasia-type profile: ``APHASIA_COMPONENTS``, ``APHASIA_ALIASES``,
  :func:`canonical_aphasia_type`, :func:`decompose_aphasia`.
* Recovery stage from days post-onset: ``RECOVERY_STAGES``, :func:`classify_stage`.
* Recovery stage named in a therapy study's population text:
  ``THERAPY_STAGE_PATTERNS``, :func:`stages_in_population`,
  :func:`therapy_evidence_stages`.
* Display bins for KB evidence scores: ``EVIDENCE_STRENGTH_BINS``,
  :func:`evidence_strength`, :func:`evidence_direction`.
"""

from __future__ import annotations

import re
from pathlib import Path

# ============================================================
# WAB aphasia types → fluency / comprehension / repetition profile
# ============================================================

#: Order of the three axes in every ``APHASIA_COMPONENTS`` tuple.
WAB_AXES = ("fluency", "comprehension", "repetition")

#: Qualitative profile of each WAB aphasia type as (fluency, comprehension,
#: repetition); "+" = relatively preserved, "-" = impaired.
#:
#: Source: the taxonomy of the Western Aphasia Battery (Kertesz A., *Western
#: Aphasia Battery*, 1982; *Western Aphasia Battery–Revised*, PsychCorp, 2007),
#: which assigns the eight types from the Fluency, Auditory Verbal
#: Comprehension and Repetition subtest scores. The 2026-10-09 review checked
#: this table against that taxonomy and found every +/- pattern consistent with
#: it (WAB names mixed transcortical aphasia "Isolation").
#:
#: Only the qualitative pattern is encoded. The WAB's numeric subtest cut-offs
#: are NOT used here (they differ between types, e.g. the comprehension score
#: that counts as "preserved" for Broca's is lower than for anomic aphasia), so
#: a "+" means "within the range of that type", not a fixed score. The report
#: uses this table only to annotate a type name; it never assigns a type.
APHASIA_COMPONENTS = {
    "brocas_aphasia":                ("-", "+", "-"),
    "wernickes_aphasia":             ("+", "-", "-"),
    "conduction_aphasia":            ("+", "+", "-"),
    "anomic_aphasia":                ("+", "+", "+"),
    "global_aphasia":                ("-", "-", "-"),
    "transcortical_motor_aphasia":   ("-", "+", "+"),
    "transcortical_sensory_aphasia": ("+", "-", "+"),
    "mixed_transcortical_aphasia":   ("-", "-", "+"),
}

#: Readable names (WAB wording) for the canonical ids above.
APHASIA_LABELS = {
    "brocas_aphasia": "Broca's",
    "wernickes_aphasia": "Wernicke's",
    "conduction_aphasia": "Conduction",
    "anomic_aphasia": "Anomic",
    "global_aphasia": "Global",
    "transcortical_motor_aphasia": "Transcortical motor",
    "transcortical_sensory_aphasia": "Transcortical sensory",
    "mixed_transcortical_aphasia": "Mixed transcortical (WAB: Isolation)",
}

#: Free-text spellings of a WAB type → canonical id. Matching ignores case,
#: apostrophes, spaces, hyphens and underscores (see
#: :func:`canonical_aphasia_type`), so "TranscorticalMotor" (as written in
#: ds004884 ``participants.tsv``) and "Broca's aphasia" are recognised.
APHASIA_ALIASES = {
    "broca": "brocas_aphasia", "broca's": "brocas_aphasia",
    "brocas": "brocas_aphasia", "broca aphasia": "brocas_aphasia",
    "wernicke": "wernickes_aphasia", "wernicke's": "wernickes_aphasia",
    "wernickes": "wernickes_aphasia", "wernicke aphasia": "wernickes_aphasia",
    "conduction": "conduction_aphasia",
    "anomic": "anomic_aphasia", "anomia": "anomic_aphasia",
    "global": "global_aphasia",
    "transcortical motor": "transcortical_motor_aphasia",
    "tcm": "transcortical_motor_aphasia",
    "transcortical sensory": "transcortical_sensory_aphasia",
    "tcs": "transcortical_sensory_aphasia",
    "mixed transcortical": "mixed_transcortical_aphasia",
    "isolation": "mixed_transcortical_aphasia",
}


def _squash(text: str) -> str:
    """Lowercase and drop everything but letters (for tolerant matching)."""
    return re.sub(r"[^a-z]", "", str(text).lower())


_LOOKUP = {}
for _alias, _canonical in APHASIA_ALIASES.items():
    _LOOKUP[_squash(_alias)] = _canonical
    _LOOKUP[_squash(_alias + " aphasia")] = _canonical
for _canonical in APHASIA_COMPONENTS:
    _LOOKUP[_squash(_canonical)] = _canonical


def canonical_aphasia_type(name) -> str | None:
    """Canonical id (e.g. ``"brocas_aphasia"``) for a WAB type string, or None.

    >>> canonical_aphasia_type("TranscorticalMotor")
    'transcortical_motor_aphasia'
    """
    if not name or not str(name).strip():
        return None
    return _LOOKUP.get(_squash(name))


def decompose_aphasia(name) -> tuple[str, str, str] | None:
    """(fluency, comprehension, repetition) "+"/"-" profile, or None if unknown."""
    canonical = canonical_aphasia_type(name)
    return APHASIA_COMPONENTS.get(canonical) if canonical else None


# ============================================================
# Recovery stage from days post-onset
# ============================================================

#: (stage id, label, first day included, first day excluded).
#:
#: Source: Stroke Recovery and Rehabilitation Roundtable consensus (Bernhardt
#: et al., 2017, Int J Stroke 12:444–450): acute 1–7 d, early subacute 7 d–3 mo,
#: late subacute 3–6 mo, chronic > 6 months; the two subacute bands are merged
#: here. The same bands give each KB finding's ``sample.phase``
#: (aphasia-kb/phase.py), so a participant's stage and the evidence's phase are
#: compared on one scale. (Until 2026-10-22 the acute/subacute cut was an
#: unsourced 14 days.) Day 7 is subacute here; phase.py counts a sample whose
#: time post onset is exactly 7 days as acute.
#:
#: Days are the participant's ``wab_days`` (stroke onset → WAB assessment), so
#: the stage describes the assessment, not the scan, unless both coincide.
RECOVERY_STAGES = (
    ("acute",    "Acute (<7 d)",         0,   7),
    ("subacute", "Subacute (7 d–6 mo)",  7,   180),
    ("chronic",  "Chronic (>6 mo)",      180, None),
)


def classify_stage(days) -> tuple[str | None, str]:
    """(stage id, label) for days post-onset; (None, "unknown") when missing.

    Boundaries follow ``RECOVERY_STAGES``: day 7 is subacute, day 180 chronic.
    Negative or non-numeric values are treated as unknown.
    """
    try:
        days = float(days)
    except (TypeError, ValueError):
        return None, "unknown"
    if days != days or days < 0:  # NaN or before onset
        return None, "unknown"
    for stage, label, low, high in RECOVERY_STAGES:
        if days >= low and (high is None or days < high):
            return stage, label
    return None, "unknown"


# ============================================================
# Recovery stage named in a therapy finding's study population
# ============================================================

#: Keyword patterns searched in ``findings[].sample.population`` of therapy
#: entries. Source: project heuristic (no published source); a finding can
#: match several stages. "chronic" also matches ">6 months" / ">=180".
THERAPY_STAGE_PATTERNS = (
    ("acute",    re.compile(r"\bacute", re.I)),
    ("subacute", re.compile(r"subacute", re.I)),
    ("chronic",  re.compile(r"chronic|>[=]?\s*6\s*months?|>=\s*180", re.I)),
)


def stages_in_population(text) -> set[str]:
    """Recovery stages named in a study-population description."""
    text = str(text or "")
    return {stage for stage, pattern in THERAPY_STAGE_PATTERNS if pattern.search(text)}


def therapy_evidence_stages(kb_root) -> dict[str, set[str]]:
    """{therapy id: stages of the populations its findings were studied in}.

    Reads the YAML front matter of ``<kb_root>/therapies/*.md``. Files that do
    not parse are skipped (the report then shows no stage warning for them).
    """
    import yaml
    result = {}
    for path in sorted((Path(kb_root) / "therapies").glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
            match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
            if not match:
                continue
            meta = yaml.safe_load(match.group(1)) or {}
            stages = set()
            for finding in meta.get("findings") or []:
                stages |= stages_in_population((finding.get("sample") or {}).get("population"))
            if stages:
                result[meta.get("id") or path.stem] = stages
        except Exception:  # one malformed entry must not hide the report
            continue
    return result


# ============================================================
# Display of KB evidence scores
# ============================================================

#: (upper bound of |score|, stars, label). Source: project display heuristic,
#: NOT a published evidence grading. ``score`` is the KB's summed, signed
#: finding weight (strength × study design × confidence; see
#: ``aphasia_kb.KnowledgeBase.interpret_overlap``).
EVIDENCE_STRENGTH_BINS = (
    (0.01, 0, "no net evidence"),
    (1.5, 1, "weak / preliminary"),
    (3.0, 2, "moderate"),
    (6.0, 3, "strong"),
    (None, 4, "very strong / replicated"),
)


def evidence_strength(score) -> tuple[int, str]:
    """(number of stars, label) for a KB score; uses |score|."""
    value = abs(float(score))
    for upper, stars, label in EVIDENCE_STRENGTH_BINS:
        if upper is None or value < upper:
            return stars, label
    raise AssertionError("unreachable")


def evidence_direction(score) -> str:
    """'likely' for a positive net score, 'unlikely' if negative, else 'ambiguous'."""
    return "likely" if score > 0 else ("unlikely" if score < 0 else "ambiguous")


# ============================================================
# Tables for the notebook / report
# ============================================================

def rules_tables():
    """The rules above as DataFrames, keyed by a short title."""
    import pandas as pd
    wab = pd.DataFrame(
        [(APHASIA_LABELS[k], *v) for k, v in APHASIA_COMPONENTS.items()],
        columns=["WAB aphasia type", "Fluency", "Comprehension", "Repetition"])
    stages = pd.DataFrame(
        [(label, f"{low} ≤ days" + (f" < {high}" if high is not None else ""))
         for _, label, low, high in RECOVERY_STAGES],
        columns=["Recovery stage", "Days post-onset (wab_days)"])
    bounds, low = [], 0.0
    for upper, stars, label in EVIDENCE_STRENGTH_BINS:
        bounds.append(("★" * stars or "—", label,
                       f"{low:g} ≤ |score|" + (f" < {upper:g}" if upper is not None else "")))
        low = upper if upper is not None else low
    strength = pd.DataFrame(bounds, columns=["Stars", "Evidence strength", "KB score range"])
    return {
        "WAB type profile (Kertesz WAB/WAB-R taxonomy; + preserved, - impaired)": wab,
        "Recovery stage (Bernhardt et al. 2017 bands: 7 d, 6 mo)": stages,
        "Evidence strength stars (project display heuristic)": strength,
    }
