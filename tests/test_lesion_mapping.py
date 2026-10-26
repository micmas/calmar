"""v2.7 lesion-mapping design and cohort grouping (aphasia-kb/lesion_mapping.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "aphasia-kb"))

import lesion_mapping as L  # noqa: E402


def _finding(**kw):
    f = {"method": "VLSM", "sample": {"n": 40, "population": "chronic stroke"},
         "statistics": {"threshold": "p < .05"}, "confounders_controlled": []}
    f.update(kw)
    return f


def test_non_lesion_findings_have_no_design():
    assert L.finding_lesion_mapping({"method": "fMRI_activation"}) == (None, "")


def test_inference_reads_only_what_the_text_says():
    lm, src = L.finding_lesion_mapping(_finding(
        statistics={"threshold": "binomial test, FDR-corrected"},
        confounders_controlled=["lesion volume", "age"]))
    assert src == "inferred"
    assert lm["analysis"] == "univariate" and lm["multiple_comparisons"] == "fdr"
    assert lm["lesion_volume_correction"] == "covariate" and lm["n_analysed"] == 40
    assert lm["min_lesion_overlap"] == "not_reported"
    assert L.orientation(lm) == "sensitivity" and L.design_cautions(lm) == []


def test_unstated_design_gives_cautions_not_guesses():
    lm, _ = L.finding_lesion_mapping(_finding())
    assert lm["multiple_comparisons"] == "not_reported"
    assert lm["lesion_volume_correction"] == "not_reported"
    assert "lesion-volume control not stated" in L.design_cautions(lm)
    assert "multiple-comparison correction not stated" in L.design_cautions(lm)


def test_stated_design_wins_and_small_multivariate_is_flagged():
    lm, src = L.finding_lesion_mapping(_finding(method="MLPA", lesion_mapping={
        "analysis": "multivariate", "n_analysed": 58, "lesion_volume_correction": "direct",
        "multiple_comparisons": "permutation_fwe"}))
    assert src == "stated" and L.orientation(lm) == "specificity"
    assert L.design_cautions(lm) == ["multivariate analysis with n = 58 (< 100)"]


def test_cohort_inference_and_grouping():
    assert L.finding_cohort(_finding(sample={"population": "the Aphasia Recovery Cohort (ARC)"})) == ("ARC", "inferred")
    assert L.finding_cohort(_finding(sample={"population": "arcuate damage"})) == (None, "")
    assert L.finding_cohort(_finding(sample={"cohort": "PLORAS"})) == ("PLORAS", "stated")
    groups = L.cohort_groups([
        {"citation": "@A", "cohort": "ARC"}, {"citation": "@B", "cohort": "ARC"},
        {"citation": "@C", "flags": ["cohort overlaps with @D (same n=12)"]}, {"citation": "@D"},
        {"citation": "@E"}])
    assert groups["@A"] == groups["@B"] == "ARC"
    assert groups["@C"] == groups["@D"] and groups["@E"] == "@E"
