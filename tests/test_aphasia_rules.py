"""Unit tests for the clinical/display rules used by the participant report."""
from pathlib import Path
import sys

import pytest

KB_ROOT = Path(__file__).resolve().parents[1] / "aphasia-kb"
sys.path.insert(0, str(KB_ROOT))
import aphasia_rules as rules  # noqa: E402


# WAB / WAB-R taxonomy: (fluency, comprehension, repetition), + = preserved.
WAB_TAXONOMY = {
    "Global": ("-", "-", "-"),
    "Broca": ("-", "+", "-"),
    "Isolation": ("-", "-", "+"),
    "Transcortical motor": ("-", "+", "+"),
    "Wernicke": ("+", "-", "-"),
    "Transcortical sensory": ("+", "-", "+"),
    "Conduction": ("+", "+", "-"),
    "Anomic": ("+", "+", "+"),
}


@pytest.mark.parametrize("name,profile", WAB_TAXONOMY.items())
def test_wab_profiles_match_the_wab_taxonomy(name, profile):
    assert rules.decompose_aphasia(name) == profile


def test_every_profile_is_distinct_and_covers_all_eight_wab_types():
    assert len(rules.APHASIA_COMPONENTS) == 8
    assert len(set(rules.APHASIA_COMPONENTS.values())) == 8
    assert set(rules.APHASIA_LABELS) == set(rules.APHASIA_COMPONENTS)


@pytest.mark.parametrize("text,canonical", [
    ("Broca", "brocas_aphasia"), ("Broca's aphasia", "brocas_aphasia"), ("WERNICKE", "wernickes_aphasia"),
    ("TranscorticalMotor", "transcortical_motor_aphasia"),  # spelling used in ds004884
    ("TCS", "transcortical_sensory_aphasia"), ("anomia", "anomic_aphasia"),
    ("mixed_transcortical_aphasia", "mixed_transcortical_aphasia"), ("anomic aphasia", "anomic_aphasia"),
])
def test_type_spellings_are_recognised(text, canonical):
    assert rules.canonical_aphasia_type(text) == canonical


@pytest.mark.parametrize("text", [None, "", "  ", "n/a", "dysarthria", "fluency"])
def test_non_wab_values_are_not_decomposed(text):
    assert rules.decompose_aphasia(text) is None


@pytest.mark.parametrize("days,stage", [
    (0, "acute"), (13.9, "acute"), (14, "subacute"), (179, "subacute"),
    (180, "chronic"), (8798, "chronic"), ("42", "subacute"),
    (None, None), ("n/a", None), (float("nan"), None), (-1, None),
])
def test_recovery_stage_boundaries(days, stage):
    assert rules.classify_stage(days)[0] == stage


def test_stage_text_matching_does_not_count_subacute_as_acute():
    assert rules.stages_in_population("subacute stroke") == {"subacute"}
    assert rules.stages_in_population("acute and chronic") == {"acute", "chronic"}
    assert rules.stages_in_population(">= 6 months post onset") == {"chronic"}
    assert rules.stages_in_population(None) == set()


def test_therapy_stages_are_read_from_front_matter(tmp_path):
    (tmp_path / "therapies").mkdir()
    (tmp_path / "therapies" / "x.md").write_text(
        "---\nid: therapy_x\nfindings:\n  - sample: {population: 'subacute stroke'}\n"
        "  - sample: {population: 'chronic aphasia'}\n---\nBody\n")
    (tmp_path / "therapies" / "broken.md").write_text("---\n: : :\n---\n")
    assert rules.therapy_evidence_stages(tmp_path) == {"therapy_x": {"subacute", "chronic"}}


@pytest.mark.parametrize("score,stars", [
    (0, 0), (0.009, 0), (0.01, 1), (-1.49, 1), (1.5, 2), (2.99, 2), (3, 3), (-5.9, 3), (6, 4), (40, 4)])
def test_evidence_strength_bins(score, stars):
    assert rules.evidence_strength(score)[0] == stars


def test_direction_sign():
    assert [rules.evidence_direction(s) for s in (2, -0.5, 0)] == ["likely", "unlikely", "ambiguous"]


def test_rule_tables_show_every_rule():
    tables = list(rules.rules_tables().values())
    assert len(tables[0]) == len(rules.APHASIA_COMPONENTS)
    assert len(tables[1]) == len(rules.RECOVERY_STAGES)
    assert len(tables[2]) == len(rules.EVIDENCE_STRENGTH_BINS)


def test_kb_maps_spelling_variants_of_wab_type_to_impairments():
    import aphasia_kb
    kb = aphasia_kb.KnowledgeBase.__new__(aphasia_kb.KnowledgeBase)
    assert kb.wab_to_impairments("TranscorticalMotor") == kb.wab_to_impairments("transcortical motor") != []
    assert kb.wab_to_impairments("Broca") == ["brocas_aphasia"]
    assert kb.wab_to_impairments("unknown type") == []


def test_therapy_gating_uses_the_same_aliases_as_the_display_rules():
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'aphasia-kb'))
    from aphasia_kb import KnowledgeBase
    import aphasia_rules
    kb = KnowledgeBase.__new__(KnowledgeBase)  # mapping needs no loaded KB
    for name in ('Isolation', 'TranscorticalMotor', "Broca's aphasia", 'Wernicke', 'Anomic'):
        assert aphasia_rules.canonical_aphasia_type(name)
        assert kb.wab_to_impairments(name), name
    assert kb.wab_to_impairments('Isolation') == ['global_aphasia']
    assert kb.wab_to_impairments('None') == []
