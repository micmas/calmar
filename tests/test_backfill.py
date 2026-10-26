"""backfill.py: which fields are missing, and what is written."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "stroke-aphasia-kb"))

import backfill as B  # noqa: E402
from quote_check import PaperText  # noqa: E402

PAPER = PaperText.from_text(
    "We tested these hypotheses using voxel-based lesion symptom mapping (VLSM) in 48 patients. "
    "All patients were tested in the chronic phase, at least 9 months post-onset.")


def test_missing_fields_skip_reviews_and_complete_findings():
    assert B.missing_fields({"method": "narrative_review"}) == []
    f = {"method": "VLSM", "sample": {"n": 48}, "author_limitations": []}
    assert B.missing_fields(f) == ["lesion_mapping", "phase", "cohort"]
    f.update(lesion_mapping={"analysis": "univariate"}, sample={"phase": "chronic", "cohort": "not_reported"})
    assert B.missing_fields(f) == []


def test_values_need_a_quote_found_in_the_paper():
    ok = {"value": "chronic", "quote": "All patients were tested in the chronic phase"}
    assert B.check("phase", ok, PAPER)[0] == "chronic"
    made_up = {"value": "chronic", "quote": "Patients were scanned two years after stroke."}
    assert B.check("phase", made_up, PAPER)[0] is None
    assert B.check("cohort", {"value": "none", "quote": ""}, PAPER)[0] == "not_reported"
    assert B.check("cohort", {"value": "ARC", "quote": "from the Aphasia Recovery Cohort"}, PAPER)[0] is None


def test_lesion_mapping_vocabulary_and_quotes():
    lm = {"analysis": "univariate", "n_analysed": "48", "lesion_volume_correction": "not_reported",
          "multiple_comparisons": "not_reported"}
    val, quotes, _ = B.check("lesion_mapping", {"value": lm, "quotes": [
        "voxel-based lesion symptom mapping (VLSM) in 48 patients"]}, PAPER)
    assert val["n_analysed"] == 48 and val["min_lesion_overlap"] == "not_reported" and quotes
    bad = dict(lm, multiple_comparisons="holm-ish")
    assert B.check("lesion_mapping", {"value": bad, "quotes": []}, PAPER)[0] is None


def test_design_values_need_a_quote_about_them():
    lm = {"analysis": "univariate", "n_analysed": 48, "lesion_volume_correction": "none",
          "multiple_comparisons": "uncorrected"}
    val, _, why = B.check("lesion_mapping", {"value": lm, "quotes": [
        "voxel-based lesion symptom mapping (VLSM) in 48 patients"]}, PAPER)
    assert val["lesion_volume_correction"] == "not_reported"
    assert val["multiple_comparisons"] == "not_reported" and "no quote states it" in why
