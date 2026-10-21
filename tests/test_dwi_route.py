"""Acute (DWI) route: OpenADS on diffusion-weighted images, and the recovery
phase of the evidence the report uses."""
import sys
from pathlib import Path

import pandas as pd
import pytest

from calmar.method_choice import MethodChoice
from calmar.study import (Study, derivative_dirs, discover_dwi, mni_masks, modality, segmentation_methods,
                          select_participants, stage_selected, template_source)

KB_ROOT = Path(__file__).resolve().parents[1] / "aphasia-kb"
DWI = {"MODALITY": "dwi"}


def touch(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"x")
    return path


def isles(root):
    for case in ("sub-strokecase0001", "sub-strokecase0002"):
        touch(root / case / "ses-0001" / "dwi" / f"{case}_ses-0001_dwi.nii.gz")
        touch(root / case / "ses-0001" / "dwi" / f"{case}_ses-0001_adc.nii.gz")
        touch(root / case / "ses-0001" / "anat" / f"{case}_ses-0001_FLAIR.nii.gz")
    touch(root / "sub-strokecase0003" / "ses-0001" / "dwi" / "sub-strokecase0003_ses-0001_dwi.nii.gz")   # no ADC
    touch(root / "derivatives" / "x" / "sub-strokecase0001" / "ses-0001" / "dwi" / "y_dwi.nii.gz")
    return root


def test_dwi_discovery_needs_an_adc_and_sets_the_native_image(tmp_path):
    entries = discover_dwi(isles(tmp_path))
    assert [e["subject"] for e in entries] == ["sub-strokecase0001", "sub-strokecase0002"]
    e = entries[0]
    assert e["t1w"] == e["dwi"] and e["adc"].name.endswith("_adc.nii.gz") and e["modality"] == "dwi"
    chosen, _ = select_participants({"DATASET_SOURCE": "local", **DWI, "MAX_SUBJECTS": 1}, tmp_path)
    assert [c["subject"] for c in chosen] == ["sub-strokecase0001"]


def test_the_acute_route_runs_openads_and_not_the_t1_steps():
    assert modality(DWI) == "dwi" and modality({}) == "t1"
    assert segmentation_methods(DWI) == ("openads",) and template_source(DWI) == "openads"
    assert [stage_selected(s, DWI) for s in ("brain", "linda", "synthstroke", "registration", "openads",
                                              "manual", "bcb")] == [False, False, False, False, True, True, True]
    assert not stage_selected("openads", {})
    with pytest.raises(ValueError):
        modality({"MODALITY": "ct"})


def test_template_folder_and_masks_in_the_acute_route(tmp_path):
    entry = {"subject": "sub-strokecase0001", "session": "ses-0001", "t1w": "x"}
    d = derivative_dirs(tmp_path, DWI, entry)
    assert d["template"] == d["openads"] == tmp_path / "derivatives/openads/sub-strokecase0001/ses-0001/anat"
    assert mni_masks(d)["openads"] == d["openads"] / "OpenADS_in_MNI.nii.gz"
    assert mni_masks(d)["manual"] == d["openads"] / "ExpertMask_in_MNI.nii.gz"
    touch(d["openads"] / "sub-strokecase0001_ses-0001_space-DWI_desc-lesion_mask.nii.gz")
    touch(d["openads"] / "OpenADS_in_MNI.nii.gz")
    found = Study(DWI, tmp_path, tmp_path).masks(entry)
    assert set(found["openads"]) == {"T1w", "MNI"}


def test_no_segmentation_choice_in_the_acute_route():
    choice = MethodChoice(dict(DWI))
    assert choice.valid and choice.methods == ["openads"] and "OpenADS" in choice.widget.value


def test_findings_carry_their_study_phase_and_the_report_flags_other_phases():
    sys.path.insert(0, str(KB_ROOT))
    from calmar.report_evidence import finding_phases, phase_summary
    rows = pd.DataFrame([
        dict(population="chronic left-hemisphere stroke survivors", phase=None),
        dict(population="acute stroke patients within 48 h", phase=None),
        dict(population="healthy volunteers", phase=None),
        dict(population="chronic stroke", phase="subacute")])                 # an explicit phase wins
    assert [finding_phases(r) for _, r in rows.iterrows()] == [{"chronic"}, {"acute"}, set(), {"subacute"}]
    text = phase_summary(rows, "acute")
    assert "1 were studied in the same phase, 2 in another phase" in text and "1 do not state it" in text
    assert "read it with caution" in text


def test_right_hemisphere_lesions_are_explained():
    from calmar.report_evidence import laterality_note
    right = pd.DataFrame([dict(region="right_precentral_gyrus", side="right", lesion_pct=30.0),
                          dict(region="left_precentral_gyrus", side="left", lesion_pct=0.0)])
    assert "right</b> hemisphere" in laterality_note(right)
    left = right.assign(side=["left", "right"])
    assert laterality_note(left) == ""
