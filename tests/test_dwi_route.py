"""Acute (DWI) route: OpenADS on diffusion-weighted images, and the recovery
phase of the evidence the report uses."""
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pandas as pd
import pytest

from calmar.method_choice import MethodChoice
from calmar.study import (Study, analysis_mask_sources, attach_dwi_inventory, derivative_dirs, discover_dwi,
                          discover_dwi_inventory, mni_masks, modality, segmentation_methods,
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
    root = isles(tmp_path)
    entries = discover_dwi(root)
    assert [e["subject"] for e in entries] == ["sub-strokecase0001", "sub-strokecase0002"]
    inventory = discover_dwi_inventory(root)
    assert [e["subject"] for e in inventory] == [
        "sub-strokecase0001", "sub-strokecase0002", "sub-strokecase0003"]
    assert inventory[-1]["adc"] is None
    e = entries[0]
    assert e["t1w"] == e["dwi"] and e["adc"].name.endswith("_adc.nii.gz") and e["modality"] == "dwi"
    chosen, _ = select_participants({"DATASET_SOURCE": "local", **DWI, "MAX_SUBJECTS": 1}, tmp_path)
    assert [c["subject"] for c in chosen] == ["sub-strokecase0001"]


def test_t1_entry_inventory_keeps_dwi_from_same_and_other_sessions(tmp_path):
    t1 = touch(tmp_path / "sub-one" / "ses-t1" / "anat" / "sub-one_ses-t1_T1w.nii.gz")
    same = touch(tmp_path / "sub-one" / "ses-t1" / "dwi" / "sub-one_ses-t1_dwi.nii.gz")
    other = touch(tmp_path / "sub-one" / "ses-acute" / "dwi" / "sub-one_ses-acute_dwi.nii.gz")
    touch(other.with_name("sub-one_ses-acute_adc.nii.gz"))
    entries = attach_dwi_inventory([{"subject": "sub-one", "session": "ses-t1", "t1w": t1}], tmp_path)
    inventory = entries[0]["dwi_inventory"]
    assert [item["dwi"] for item in inventory] == [other, same]
    assert [(item["same_session"], item["openads_ready"]) for item in inventory] == [(False, True), (True, False)]


def test_optional_openads_keeps_another_dwi_session_distinct(tmp_path):
    from calmar.dwi_choice import apply_dwi_selection, openads_options
    t1 = touch(tmp_path / "sub-one" / "ses-chronic" / "anat" / "sub-one_ses-chronic_T1w.nii.gz")
    dwi = touch(tmp_path / "sub-one" / "ses-acute" / "dwi" / "sub-one_ses-acute_dwi.nii.gz")
    adc = touch(dwi.with_name("sub-one_ses-acute_adc.nii.gz"))
    entry = attach_dwi_inventory([{"subject": "sub-one", "session": "ses-chronic", "t1w": t1}], tmp_path)[0]
    assert openads_options(entry)[0]["session"] == "ses-acute"
    namespace = {"CONFIG": {"MODALITY": "t1", "SEGMENTATION_METHODS": ["synthstroke"], "ANALYSE_DWI": None},
                 "SUBJECTS": [entry], "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path}
    apply_dwi_selection(namespace, {"sub-one": openads_options(entry)[0]})
    selected = namespace["SUBJECTS"][0]
    assert selected["session"] == "ses-chronic" and selected["dwi_analysis"]["session"] == "ses-acute"
    assert namespace["CONFIG"]["ANALYSE_DWI"] is None
    assert namespace["CONFIG"]["_DWI_ANALYSIS_SELECTED"] is True
    assert namespace["DWI_SUBJECTS"][0]["t1w"] == dwi
    assert namespace["DWI_SUBJECTS"][0]["adc"] == adc
    assert analysis_mask_sources(namespace["CONFIG"]) == ("synthstroke", "openads", "manual")
    study = Study(namespace["CONFIG"], tmp_path, tmp_path)
    assert study.dirs(selected)["openads"] == tmp_path / "derivatives/openads/sub-one/ses-acute/anat"
    native = touch(study.dirs(selected)["openads"] / "sub-one_ses-acute_space-DWI_desc-lesion_mask.nii.gz")
    touch(study.dirs(selected)["openads"] / "OpenADS_in_MNI.nii.gz")
    assert study.masks(selected)["openads"]["T1w"] == native
    assert study.qc_anchor(selected, "openads").parent.name == "anat"


def test_dwi_choice_close_does_not_register_the_panel_as_its_own_control(tmp_path):
    from calmar.dwi_choice import DWIChoice

    entry = {"subject": "sub-one", "session": "ses-t1", "t1w": str(tmp_path / "t1.nii.gz"),
             "dwi_inventory": [{"subject": "sub-one", "session": "ses-dwi", "same_session": False,
                                "dwi": str(tmp_path / "dwi.nii.gz"), "adc": str(tmp_path / "adc.nii.gz"),
                                "openads_ready": True}]}
    namespace = {"SUBJECTS": [entry], "CONFIG": {}, "RAW_DATASET_DIR": tmp_path,
                 "PROJECT_DIR": tmp_path}
    shell = SimpleNamespace(input_transformers_post=[], kernel=SimpleNamespace(_abort_queues=lambda: None))
    panel = DWIChoice(namespace, shell)
    assert panel.checkpoint.controls == []
    panel.navigation.request = Mock()
    panel._request(True)
    panel.navigation.request.assert_called_once()
    assert panel.navigation.request.call_args.args[0] == "single-test-selection"
    assert panel.navigation.request.call_args.kwargs["all_below"] is True
    panel.close()


def test_datalad_dangling_dwi_and_adc_links_are_discovered_without_fetching(tmp_path):
    folder = tmp_path / "sub-one" / "ses-one" / "dwi"
    folder.mkdir(parents=True)
    dwi = folder / "sub-one_ses-one_dwi.nii.gz"
    adc = folder / "sub-one_ses-one_adc.nii.gz"
    dwi.symlink_to(tmp_path / "annex-dwi")
    adc.symlink_to(tmp_path / "annex-adc")
    assert not dwi.exists() and not adc.exists()
    inventory = discover_dwi_inventory(tmp_path)
    assert inventory[0]["dwi"] == dwi and inventory[0]["adc"] == adc
    assert discover_dwi(tmp_path)[0]["adc"] == adc
    assert not dwi.exists() and not adc.exists()


def test_flat_and_single_inputs_can_inventory_dwi_by_filename(tmp_path):
    flat_dwi = touch(tmp_path / "sub-flat_ses-dwi_dwi.nii.gz")
    assert discover_dwi_inventory(tmp_path)[0]["subject"] == "sub-flat"
    t1 = touch(tmp_path / "sub-one" / "ses-t1" / "anat" / "sub-one_ses-t1_T1w.nii.gz")
    sibling = touch(tmp_path / "sub-one" / "ses-dwi" / "dwi" / "sub-one_ses-dwi_dwi.nii.gz")
    selected, _ = select_participants({"DATASET_SOURCE": "single", "SINGLE_T1W": str(t1)}, t1.parent)
    assert selected[0]["dwi_inventory"][0]["dwi"] == sibling


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
        dict(population="chronic stroke", phase="late_subacute"),             # sample.phase wins
        dict(population="acute and chronic stroke", phase="longitudinal")])   # falls back to the text
    assert [finding_phases(r) for _, r in rows.iterrows()] == [
        {"chronic"}, {"acute"}, set(), {"subacute"}, {"acute", "chronic"}]
    text = phase_summary(rows, "acute")
    assert "2 were studied in the same phase, 2 in another phase" in text and "1 do not state it" in text
    assert "read it with caution" not in text                               # not mostly another phase
    assert "read it with caution" in phase_summary(rows, "subacute")        # 1 same, 3 other


def test_right_hemisphere_lesions_are_explained():
    from calmar.report_evidence import laterality_note
    right = pd.DataFrame([dict(region="right_precentral_gyrus", side="right", lesion_pct=30.0),
                          dict(region="left_precentral_gyrus", side="left", lesion_pct=0.0)])
    assert "right</b> hemisphere" in laterality_note(right)
    left = right.assign(side=["left", "right"])
    assert laterality_note(left) == ""


def openads_outputs(tmp_path):
    entry = {"subject": "sub-strokecase0001", "session": "ses-0001", "t1w": "x"}
    study = Study(DWI, tmp_path, tmp_path)
    d = study.dirs(entry)
    touch(d["openads"] / "sub-strokecase0001_ses-0001_space-DWI_desc-lesion_mask.nii.gz")
    touch(d["openads"] / "OpenADS_in_MNI.nii.gz")
    touch(d["openads"] / "Subject_in_MNI.nii.gz")
    return entry, study, d


def test_acute_qc_rates_openads_and_saves_in_its_folder(tmp_path):
    entry, study, d = openads_outputs(tmp_path)
    touch(study.hdbet_dir(entry) / "x_brain_mask.nii.gz")      # an HD-BET mask must not add a skull-strip stage
    assert study.qc_stages(entry) == ["openads_lesion", "openads_mni_warp"]
    assert study.qc_anchor(entry) == d["openads"] / "OpenADS_in_MNI.nii.gz"
    assert study.qc_dir(entry) == d["openads"]
    t1 = Study({}, tmp_path, tmp_path)
    assert t1.qc_anchor(entry) == t1.lesion_mni(entry) and t1.qc_dir(entry) == t1.linda_dir(entry)


def test_acute_qc_ratings_reach_the_summary_and_the_report(tmp_path):
    import calmar.qc as q
    from calmar.participant_report import mask_qc_summary
    from calmar.qc_repair import qc_table
    entry, study, d = openads_outputs(tmp_path)
    record = q.QCRecord.load(study.qc_anchor(entry))
    record.set_stage("openads_lesion", rating=1)
    record.set_stage("openads_mni_warp", rating=3, issue_tags=["template_misaligned"])
    record.save()
    row = qc_table([entry], study).iloc[0]
    assert row["openads_lesion"] == 1 and row["openads_mni_warp"] == 3 and row["skull_strip"] == "n/a"
    assert "openads_mni_warp:template_misaligned" in row["issue_tags"]
    summary = mask_qc_summary(study.qc_anchor(entry), d["openads"] / "OpenADS_in_MNI.nii.gz", "openads")
    assert [s for s, *_ in summary["ratings"]] == ["openads_lesion", "openads_mni_warp"] and summary["poor"]


def test_acute_qc_volumes_show_the_dwi_and_the_warp(tmp_path):
    from calmar.qc_panel import QCVolumes, QCDisplay
    entry, study, d = openads_outputs(tmp_path)
    entry = dict(entry, t1w=str(touch(tmp_path / "dwi.nii.gz")))
    volumes = QCVolumes(study, QCDisplay(lesion_as_boundary=False))
    native = volumes("openads_lesion", entry)
    assert native[0]["path"] == entry["t1w"] and native[1]["name"] == "openads"
    warp = volumes("openads_mni_warp", entry)
    assert warp[0]["path"] == str(d["openads"] / "Subject_in_MNI.nii.gz")
    assert [v["name"] for v in warp[1:]] == ["openads"]


def test_openads_rerun_keeps_qc_history_and_clears_stale_ratings(tmp_path, monkeypatch):
    import calmar.qc as q
    import calmar.scheduled as scheduled
    from calmar.qc_repair import rerun_openads
    entry, study, d = openads_outputs(tmp_path)
    record = q.QCRecord.load(study.qc_anchor(entry))
    record.set_stage("openads_lesion", rating=3)
    record.marked_for_rerun = True
    record.log_edit("note", reviewer="me")
    record.save()
    calls = []

    def fake_submit(stage, entries, rerun_study, **kw):
        calls.append((stage, rerun_study.config.get("OVERWRITE")))
        if stage == "openads":                                   # product() moves the old folder aside
            d["openads"].rename(d["openads"].with_name(d["openads"].name + ".previous.abc"))
            touch(d["openads"] / "OpenADS_in_MNI.nii.gz")
        return {"results": [{"outputs": [{"path": str(d["openads"]), "status": "computed"}]}]}

    monkeypatch.setattr(scheduled, "submit_step", fake_submit)
    rerun_openads(entry, study, dict(DWI), reviewer="me")
    assert calls == [("openads", True)]                         # no manual mask configured
    after = q.QCRecord.load(study.qc_anchor(entry))
    assert after.get_stage("openads_lesion")["rating"] is None and not after.marked_for_rerun
    assert [e["operation"] for e in after.edits][:1] == ["note"]
