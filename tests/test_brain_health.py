import json
from pathlib import Path
from types import SimpleNamespace

import pytest
import numpy as np
import nibabel as nib
from unittest.mock import patch

from calmar.brain_health import (brain_health_inventory, brain_health_measure_note, brain_health_measure_records,
                                 brain_health_section, load_metrics, output_paths)
from calmar.brain_health_choice import (BrainHealthChoice, apply_brain_health_selection,
                                        available_entries, show_brain_health_choice)
from calmar.brain_health_pipeline import (_native_lesion, _overwrite_requested,
                                          _validate_mask, _wmh_measurements)
from calmar.analysis_choice import RERUN, SKIP, USE_PRIOR
from calmar.study import ENTRY_DATASET


def t1_entry(tmp_path, *, flair=True):
    anat = tmp_path / "sub-1" / "ses-a" / "anat"
    anat.mkdir(parents=True)
    t1 = anat / "sub-1_ses-a_T1w.nii.gz"
    t1.touch()
    if flair:
        (anat / "sub-1_ses-a_FLAIR.nii.gz").touch()
    return {"subject": "sub-1", "session": "ses-a", "t1w": t1}


def test_inventory_keeps_t1_and_same_session_flair_separate(tmp_path):
    entry = t1_entry(tmp_path)
    found = brain_health_inventory({"MODALITY": "t1"}, tmp_path, entry)
    assert found["atrophy_available"] is True
    assert found["wmh_available"] is True
    assert found["flair"].endswith("_FLAIR.nii.gz")


def test_acute_flair_is_not_promoted_to_atrophy(tmp_path):
    dwi = tmp_path / "sub-1" / "ses-a" / "dwi" / "sub-1_ses-a_dwi.nii.gz"
    dwi.parent.mkdir(parents=True)
    dwi.touch()
    anat = dwi.parent.parent / "anat"
    anat.mkdir()
    (anat / "sub-1_ses-a_FLAIR.nii.gz").touch()
    entry = {"subject": "sub-1", "session": "ses-a", "t1w": dwi, "dwi": dwi}
    found = brain_health_inventory({"MODALITY": "dwi"}, tmp_path, entry)
    assert found["atrophy_available"] is False
    assert found["wmh_available"] is True


def test_selection_is_opt_in_and_attaches_report_metadata(tmp_path):
    entry = t1_entry(tmp_path)
    namespace = {"SUBJECTS": [entry], "CONFIG": {"MODALITY": "t1"},
                 "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path}
    available = available_entries(namespace)
    apply_brain_health_selection(namespace, available)
    assert namespace["BRAIN_HEALTH_SUBJECTS"][0]["brain_health_components"] == ["atrophy", "wmh"]
    assert namespace["SUBJECTS"][0]["brain_health_analysis"]["components"] == ["atrophy", "wmh"]
    assert json.loads((tmp_path / "reports" / "brain-health-selection.json").read_text())["analyse_brain_health"]


def test_brain_health_panel_uses_the_shared_optional_action_controls(tmp_path):
    entry = t1_entry(tmp_path, flair=False)
    namespace = {"SUBJECTS": [entry], "CONFIG": {"MODALITY": "t1"},
                 "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path}
    shell = SimpleNamespace(input_transformers_post=[], kernel=SimpleNamespace(_abort_queues=lambda: None))
    panel = BrainHealthChoice(namespace, shell)
    try:
        assert "Choose one action per participant" in panel.children[0].value
        assert "single-scan measures are not diagnostic" in panel.children[0].value
        assert panel.rows[0][3].value == "skip"
        heading = panel.rows[0][6].value
        assert "○ Not analysed" in heading
        assert "T1 volumetry" in heading
        assert "&nbsp;Details</summary>" in heading
        assert "aria-label='Details for sub-1 · ses-a'" in heading
        assert panel.analyse.description == "Apply choices and continue"
        assert panel.skip.description == "Skip all and continue"
        assert panel.skip.button_style == "warning"
    finally:
        panel.close()


def test_brain_health_existing_output_is_resolved_in_mixed_cohort_dataset(tmp_path):
    primary = tmp_path / "primary"
    additional = tmp_path / "additional"
    entry = t1_entry(additional, flair=False)
    entry[ENTRY_DATASET] = str(additional)
    existing = output_paths(additional, {"MODALITY": "t1"}, {
        **entry, "brain_health_components": ["atrophy"]})["anatomy"]
    existing.mkdir(parents=True)
    namespace = {"SUBJECTS": [entry], "CONFIG": {"MODALITY": "t1"},
                 "RAW_DATASET_DIR": primary, "PROJECT_DIR": tmp_path / "project"}
    shell = SimpleNamespace(input_transformers_post=[], kernel=SimpleNamespace(_abort_queues=lambda: None))
    panel = BrainHealthChoice(namespace, shell)
    try:
        action = panel.rows[0][3]
        assert [value for _, value in action.options] == [RERUN, SKIP]
        assert action.value == SKIP
        assert "⚠ Unmatched saved files" in panel.rows[0][6].value
        assert "existing brain-health output" in panel.rows[0][6].value
    finally:
        panel.close()


def test_configured_brain_health_requires_explicit_policy_for_unmatched_output(tmp_path, capsys):
    entry = t1_entry(tmp_path, flair=False)
    existing = output_paths(tmp_path, {"MODALITY": "t1"}, {
        **entry, "brain_health_components": ["atrophy"]})["anatomy"]
    existing.mkdir(parents=True)
    namespace = {"SUBJECTS": [entry],
                 "CONFIG": {"MODALITY": "t1", "ANALYSE_BRAIN_HEALTH": True},
                 "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path / "project"}

    with pytest.raises(RuntimeError, match="BRAIN_HEALTH_OVERWRITE=True"):
        show_brain_health_choice(namespace)

    namespace["CONFIG"]["BRAIN_HEALTH_OVERWRITE"] = True
    assert show_brain_health_choice(namespace) is None
    output = capsys.readouterr().out
    assert "selected for 1 participant" in output
    assert "rerun requested in CONFIG" in output


def test_brain_health_compact_heading_updates_with_flair_choice(tmp_path, monkeypatch):
    entry = t1_entry(tmp_path)
    anat = Path(entry["t1w"]).parent
    second = anat / "sub-1_ses-a_run-2_FLAIR.nii.gz"
    second.touch()

    def state(namespace, source, inventory, components):
        reusable = Path(inventory["flair"]).name == second.name
        return {
            "status": ("✓ analysed already (reusable)" if reusable else "○ not analysed yet"),
            "kind": "reusable" if reusable else "new",
            "current_complete": reusable, "prior_available": reusable,
            "outputs_exist": reusable, "rerun_required": False,
        }

    monkeypatch.setattr("calmar.brain_health_choice.brain_health_analysis_state", state)
    namespace = {"SUBJECTS": [entry], "CONFIG": {"MODALITY": "t1"},
                 "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path}
    shell = SimpleNamespace(input_transformers_post=[], kernel=SimpleNamespace(_abort_queues=lambda: None))
    panel = BrainHealthChoice(namespace, shell)
    try:
        _, _, _, action, flair_choice, _, heading = panel.rows[0]
        assert flair_choice is not None
        assert "○ Not analysed" in heading.value
        assert action.value == SKIP

        flair_choice.value = str(second)
        assert "✓ Reusable" in heading.value
        assert second.name in heading.value
        assert action.value == USE_PRIOR
    finally:
        panel.close()


def test_selection_keeps_sessions_of_same_subject_distinct(tmp_path):
    first = t1_entry(tmp_path / "first", flair=False)
    second = t1_entry(tmp_path / "second", flair=False)
    second["session"] = "ses-b"
    namespace = {"SUBJECTS": [first, second], "CONFIG": {"MODALITY": "t1"},
                 "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path}
    available = available_entries(namespace)
    assert set(available) == {("sub-1", "ses-a"), ("sub-1", "ses-b")}
    apply_brain_health_selection(namespace, {("sub-1", "ses-b"): available[("sub-1", "ses-b")]})
    assert "brain_health_analysis" not in namespace["SUBJECTS"][0]
    assert namespace["SUBJECTS"][1]["brain_health_analysis"]["session"] == "ses-b"


def test_declining_hides_stale_outputs_from_report(tmp_path):
    entry = t1_entry(tmp_path, flair=False)
    paths = output_paths(tmp_path, {}, entry)
    paths["metrics"].mkdir(parents=True)
    paths["metrics_json"].write_text(json.dumps({"measurements": {}}))
    assert brain_health_section(tmp_path, {}, entry) is None


def test_report_keeps_descriptive_caveats_and_no_fazekas(tmp_path):
    entry = t1_entry(tmp_path)
    entry["brain_health_analysis"] = {"components": ["atrophy", "wmh"]}
    path = output_paths(tmp_path, {}, entry)["metrics_json"]
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({
        "anatomy": True, "wmh": True, "stroke_phase": "acute", "flair": "scan_FLAIR.nii.gz",
        "components": ["atrophy", "wmh"], "lesion_mask_source": "manual",
        "lesion_exclusion_mm": 3.0, "synthseg_mode": "robust",
        "qc_status": "requires_visual_review", "warnings": ["acute oedema may remain"],
        "measurements": {
            "intracranial_volume_ml": 1400, "brain_parenchymal_fraction": .71,
            "lesion_adjusted_brain_parenchymal_fraction": .73,
            "lateral_ventricle_fraction": .021, "left_lateral_ventricle_ml": 12,
            "right_lateral_ventricle_ml": 17, "total_flair_hyperintensity_ml": 20,
            "wmh_candidate_ml": 8, "stroke_excluded_hyperintensity_ml": 12,
            "wmh_fraction_icv": .0057,
        }}))
    html = brain_health_section(tmp_path, {}, entry)
    assert "single scan" in html
    assert "WMH candidate" in html
    assert "No automated Fazekas" in html
    assert "values are provisional" in html


def test_metric_validation_rejects_impossible_fraction(tmp_path):
    path = tmp_path / "metrics.json"
    path.write_text(json.dumps({"measurements": {"brain_parenchymal_fraction": 1.2}}))
    with pytest.raises(ValueError, match="Implausible"):
        load_metrics(path)


def test_missing_metrics_is_reported_not_fabricated(tmp_path):
    entry = t1_entry(tmp_path, flair=False)
    entry["brain_health_analysis"] = {"components": ["atrophy"]}
    assert "no validated metrics" in brain_health_section(tmp_path, {}, entry)


def test_report_measure_contract_includes_method_units_qc_and_explicit_missing(tmp_path):
    entry = t1_entry(tmp_path, flair=False)
    entry["brain_health_analysis"] = {"components": ["atrophy"]}
    path = output_paths(tmp_path, {}, entry)["metrics_json"]
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({
        "components": ["atrophy"], "anatomy": True, "wmh": False,
        "synthseg_mode": "robust", "lesion_mask_source": "manual",
        "lesion_exclusion_mm": None, "qc_status": "passed",
        "methods": {"anatomy": {"tool": "SynthSeg", "version": "8.2.1"}},
        "measurements": {"brain_parenchymal_fraction": .71},
    }))
    records = {record["id"]: record for record in brain_health_measure_records(tmp_path, {}, entry)}
    assert records["brain_parenchymal_fraction"] == {
        "id": "brain_parenchymal_fraction", "kb_id": "brain_parenchymal_fraction",
        "label": "Brain parenchymal fraction", "value": .71, "units": "fraction",
        "method": "SynthSeg 8.2.1, robust mode", "qc_status": "passed",
        "missing_reason": None, "brain_health": True,
    }
    assert records["brain_tissue_volume_ml"]["value"] is None
    assert records["brain_tissue_volume_ml"]["qc_status"] == "passed"


def test_selected_brain_health_with_no_output_returns_missing_records(tmp_path):
    entry = t1_entry(tmp_path, flair=False)
    entry["brain_health_analysis"] = {"components": ["atrophy"]}
    records = brain_health_measure_records(tmp_path, {}, entry)
    assert records and all(record["value"] is None for record in records)
    assert all(record["method"] == "missing" and record["qc_status"] == "missing" for record in records)
    assert all("metrics file is missing" in record["missing_reason"] for record in records)
    note = brain_health_measure_note(tmp_path, {}, entry, stroke_phase="chronic")
    assert "cannot establish atrophy" in note and "not an automatic diagnosis" in note
    assert "perilesional gliosis" not in note  # no FLAIR/WMH component was selected


def test_no_stroke_exclusion_never_labels_raw_burden_as_nonstroke():
    raw = np.ones((2, 2, 2), dtype=bool)
    measured = _wmh_measurements(raw, None, .001, 1.0)
    assert measured["total_flair_hyperintensity_ml"] == pytest.approx(.008)
    assert measured["wmh_candidate_ml"] is None
    assert measured["stroke_excluded_hyperintensity_ml"] is None


def test_brain_health_overwrite_uses_route_override_then_global_policy():
    assert _overwrite_requested({"config": {"OVERWRITE": True}}) is True
    assert _overwrite_requested({
        "config": {"OVERWRITE": True, "BRAIN_HEALTH_OVERWRITE": False}}) is False
    assert _overwrite_requested({
        "config": {"OVERWRITE": False, "BRAIN_HEALTH_OVERWRITE": True}}) is True


def test_empty_wmh_is_a_valid_zero_measurement():
    raw = np.zeros((2, 2, 2), dtype=bool)
    measured = _wmh_measurements(raw, np.zeros_like(raw), .001, 1.0)
    assert measured["total_flair_hyperintensity_ml"] == 0
    assert measured["wmh_candidate_ml"] == 0
    assert measured["wmh_fraction_icv"] == 0


def test_empty_outcome_mask_is_allowed_but_empty_lesion_is_not(tmp_path):
    reference = tmp_path / "reference.nii.gz"
    empty = tmp_path / "empty.nii.gz"
    image = nib.Nifti1Image(np.zeros((3, 3, 3), dtype=np.uint8), np.eye(4))
    nib.save(image, reference)
    nib.save(image, empty)
    _validate_mask(empty, reference, allow_empty=True)
    with pytest.raises(RuntimeError, match="Empty mask"):
        _validate_mask(empty, reference)


def test_openads_lesion_from_another_session_is_rejected(tmp_path):
    entry = {"subject": "sub-1", "session": "ses-t1", "t1w": tmp_path / "T1w.nii.gz",
             "dwi_analysis": {"session": "ses-dwi", "dwi": tmp_path / "DWI.nii.gz"}}
    request = {"dataset": str(tmp_path),
               "config": {"MODALITY": "t1", "SEGMENTATION_METHODS": ["linda"],
                          "BRAIN_HEALTH_MASK_SOURCE": "openads"}}
    with patch("calmar.brain_health_pipeline.Study.masks",
               return_value={"openads": {"T1w": tmp_path / "lesion.nii.gz"}}):
        with pytest.raises(ValueError, match="same session"):
            _native_lesion(request, entry)
