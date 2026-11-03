import json
import math
import os
from pathlib import Path
import subprocess
from types import SimpleNamespace

import pandas as pd
import pytest

import calmar.dmri_pipeline as dmri_pipeline
from calmar.diffusion import (assess_dwi_series, assess_dwi_sessions,
                              direct_diffusion_section, load_tractometry,
                              tractometry_paths)
from calmar.dmri_choice import (apply_dmri_selection, dmri_analysis_state,
                                dmri_analysis_status, dmri_options, show_dmri_choice)
from calmar.dmri_pipeline import (_bundle_side, _derivative_methods, _hmc_method,
                                  _run, _scalar_rows, preprocess, stage_bids)


def gradients(folder, stem, bvals, *, phase="j-", readout=0.036):
    folder.mkdir(parents=True, exist_ok=True)
    dwi = folder / f"{stem}_dwi.nii.gz"
    dwi.write_bytes(b"annex-placeholder")
    bval = folder / f"{stem}_dwi.bval"
    bval.write_text(" ".join(map(str, bvals)))
    bvec = folder / f"{stem}_dwi.bvec"
    directions = len(bvals)
    nonzero = sum(value >= 100 for value in bvals)
    angles = iter(math.pi * index / max(nonzero, 1) for index in range(nonzero))
    vectors = [(0.0, 0.0, 0.0) if value < 100 else
               (math.cos(angle := next(angles)), math.sin(angle), 0.0) for value in bvals]
    bvec.write_text("\n".join(" ".join(str(vector[axis]) for vector in vectors) for axis in range(3)))
    sidecar = folder / f"{stem}_dwi.json"
    sidecar.write_text(json.dumps({"PhaseEncodingDirection": phase, "TotalReadoutTime": readout}))
    return {"subject": stem.split("_")[0], "session": stem.split("_")[1],
            "dwi": dwi, "bval": bval, "bvec": bvec, "json": sidecar, "adc": None}


def test_trace_dwi_is_not_directional_diffusion():
    item = {"subject": "sub-acute", "session": "ses-1", "dwi": Path("trace_dwi.nii.gz"),
            "bval": None, "bvec": None, "json": None}
    result = assess_dwi_series(item)
    assert not result["tensor_eligible"] and not result["report_eligible"]
    assert "missing bval, bvec, json sidecars" in result["reasons"]


def test_valid_series_and_opposite_phase_pair_are_report_ready(tmp_path):
    bvals = [0] + [1000] * 40
    ap = gradients(tmp_path, "sub-one_ses-dwi_dir-AP", bvals, phase="j-")
    pa = gradients(tmp_path, "sub-one_ses-dwi_dir-PA", bvals, phase="j")
    # Entity-rich stems make the simple fixture parser unsuitable; set the BIDS IDs explicitly.
    for item in (ap, pa):
        item.update(subject="sub-one", session="ses-dwi", same_session=True)
    result = assess_dwi_series(ap)
    assert result["tensor_eligible"] and result["report_eligible"]
    assert result["n_b0"] == 1 and result["n_directions"] == 40 and result["shells"] == [0, 1000]
    sessions = assess_dwi_sessions({"subject": "sub-one", "session": "ses-dwi",
                                    "dwi_inventory": [ap, pa]})
    assert len(sessions) == 1 and sessions[0]["has_reverse_phase"]
    assert sessions[0]["reverse"]["phase_encoding_direction"] == "j"


def test_six_direction_fit_is_not_promoted_to_reporting(tmp_path):
    item = gradients(tmp_path, "sub-one_ses-one", [0] + [1000] * 6)
    result = assess_dwi_series(item)
    assert result["tensor_eligible"] and not result["report_eligible"]
    assert "requires 30" in result["warnings"][0]


def test_repeated_gradient_volumes_do_not_count_as_distinct_directions(tmp_path):
    item = gradients(tmp_path, "sub-one_ses-one", [0] + [1000] * 30)
    # Replace the generated vectors with six directions, each repeated five times.
    vectors = [(math.cos(math.pi * i / 6), math.sin(math.pi * i / 6), 0) for i in range(6)] * 5
    Path(item["bvec"]).write_text("\n".join(
        ["0 " + " ".join(str(v[axis]) for v in vectors) for axis in range(3)]))
    result = assess_dwi_series(item)
    assert result["n_dw_volumes"] == 30 and result["n_directions"] == 6
    assert result["tensor_eligible"] and not result["report_eligible"]


def test_reverse_phase_b0_only_series_is_kept_for_distortion_correction(tmp_path):
    full = gradients(tmp_path, "sub-one_ses-one_dir-AP", [0] + [1000] * 32, phase="j-")
    reverse_b0 = gradients(tmp_path, "sub-one_ses-one_dir-PA", [0, 0, 0], phase="j")
    for item in (full, reverse_b0):
        item.update(subject="sub-one", session="ses-one", same_session=True)
    option = assess_dwi_sessions({"subject": "sub-one", "session": "ses-one",
                                  "dwi_inventory": [full, reverse_b0]})[0]
    assert option["has_reverse_phase"] and option["reverse"]["b0_reference"]
    assert not option["reverse"]["report_eligible"]
    assert len(option["series"]) == 2


def test_selection_is_opt_in_and_keeps_anatomical_session(tmp_path):
    item = gradients(tmp_path / "sub-one/ses-dwi/dwi", "sub-one_ses-dwi", [0] + [1000] * 32)
    item.update(subject="sub-one", session="ses-dwi", same_session=False)
    entry = {"subject": "sub-one", "session": "ses-chronic", "t1w": tmp_path / "t1.nii.gz",
             "dwi_inventory": [item]}
    option = dmri_options(entry)[0]
    namespace = {"CONFIG": {"ANALYSE_TRACT_DWI": None}, "SUBJECTS": [entry],
                 "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path}
    selected = apply_dmri_selection(namespace, {"sub-one": (entry, option)})
    assert selected[0]["session"] == "ses-dwi"
    assert selected[0]["anatomical_session"] == "ses-chronic"
    assert namespace["SUBJECTS"][0]["dmri_analysis"]["n_directions"] == 32
    assert namespace["CONFIG"]["_TRACT_DWI_SELECTED"] is True
    saved = json.loads((tmp_path / "reports/dmri-selection.json").read_text())
    assert saved["selection"][0]["has_reverse_phase"] is False


def test_selection_links_directional_dwi_to_each_anatomical_session(tmp_path):
    entries = []
    choices = {}
    for index, anatomical_session in enumerate(("ses-t1a", "ses-t1b"), start=1):
        dwi_session = f"ses-dwi{index}"
        item = gradients(tmp_path / dwi_session, f"sub-one_{dwi_session}", [0] + [1000] * 32)
        item.update(subject="sub-one", session=dwi_session, same_session=False)
        entry = {"subject": "sub-one", "session": anatomical_session,
                 "t1w": tmp_path / f"{anatomical_session}_T1w.nii.gz", "dwi_inventory": [item]}
        entries.append(entry)
        choices[("sub-one", anatomical_session)] = (entry, dmri_options(entry)[0])
    namespace = {"CONFIG": {"ANALYSE_TRACT_DWI": None}, "SUBJECTS": entries,
                 "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path}

    selected = apply_dmri_selection(namespace, choices)

    assert [entry["anatomical_session"] for entry in selected] == ["ses-t1a", "ses-t1b"]
    assert [entry["dmri_analysis"]["session"] for entry in namespace["SUBJECTS"]] == [
        "ses-dwi1", "ses-dwi2"]


def test_diffusion_choice_panel_names_the_route_as_microstructure(tmp_path):
    from calmar.dmri_choice import DMRIChoice

    item = gradients(tmp_path, "sub-one_ses-dwi", [0] + [1000] * 32)
    item.update(subject="sub-one", session="ses-dwi", same_session=False)
    entry = {"subject": "sub-one", "session": "ses-t1", "t1w": tmp_path / "t1.nii.gz",
             "dwi_inventory": [item]}
    namespace = {"CONFIG": {"MODALITY": "t1"}, "SUBJECTS": [entry],
                 "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path}
    shell = SimpleNamespace(input_transformers_post=[], kernel=SimpleNamespace(_abort_queues=lambda: None))

    panel = DMRIChoice(namespace, shell)
    try:
        assert "Optional diffusion tract-microstructure analysis" in panel.children[0].value
        assert "separate from OpenADS" in panel.children[0].value
        assert "Prior-analysis status is checked without running tools" in panel.children[0].value
        assert "Choose one action per participant" in panel.children[0].value
        assert panel.rows[0][3].label.startswith("ses-dwi · different session")
        assert "not analysed" not in panel.rows[0][3].label
        assert panel.rows[0][2].value == "skip"
        heading = panel.rows[0][5].value
        assert "○ Not analysed" in heading
        assert "<details" in heading and "&nbsp;Details</summary>" in heading
        assert "○ not analysed yet" in heading
        assert panel.analyse.description == "Apply choices and continue"
        assert panel.skip.description == "Skip all and continue"
        assert panel.skip.button_style == "warning"
    finally:
        panel.close()


def test_diffusion_choice_updates_compact_status_when_session_changes(tmp_path, monkeypatch):
    from calmar.dmri_choice import DMRIChoice

    options = [
        {"session": "ses-current", "same_session": True, "has_reverse_phase": True,
         "shells": [0, 1000], "n_directions": 64, "warnings": []},
        {"session": "ses-old", "same_session": False, "has_reverse_phase": False,
         "shells": [0, 1000], "n_directions": 32,
         "warnings": ["no opposite phase-encoding DWI"]},
        {"session": "ses-blocked", "same_session": False, "has_reverse_phase": False,
         "shells": [0, 1000], "n_directions": 32, "warnings": []},
    ]
    states = {
        "ses-current": {"status": "✓ analysed already (reusable)", "kind": "reusable",
                        "current_complete": True, "prior_available": True, "outputs_exist": True,
                        "rerun_required": False},
        "ses-old": {"status": (
            "⚠ input file date or size differs for this or an earlier stage: QSIPrep"),
                    "kind": "changed", "current_complete": False, "prior_available": True,
                    "outputs_exist": True, "rerun_required": False},
        "ses-blocked": {"status": "◐ partly analysed: QSIPrep; later outputs not reusable: QSIRecon",
                        "kind": "partial", "current_complete": False, "prior_available": True,
                        "outputs_exist": True, "rerun_required": True},
    }
    monkeypatch.setattr("calmar.dmri_choice.dmri_options", lambda entry: options)
    monkeypatch.setattr(
        "calmar.dmri_choice.dmri_analysis_state",
        lambda namespace, entry, option: states[option["session"]])
    entry = {"subject": "sub-one", "session": "ses-current", "t1w": tmp_path / "t1.nii.gz"}
    namespace = {"CONFIG": {"MODALITY": "t1"}, "SUBJECTS": [entry],
                 "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path}
    shell = SimpleNamespace(input_transformers_post=[], kernel=SimpleNamespace(_abort_queues=lambda: None))

    panel = DMRIChoice(namespace, shell)
    try:
        _, _, action, choice, _, heading = panel.rows[0]
        assert "✓ Reusable" in heading.value
        assert action.value == "use_prior"
        assert "✓ analysed already (reusable)" in heading.value
        assert ("⚠ input file date or size differs for this or an earlier stage: QSIPrep"
                in heading.value)
        assert heading.value.count("analysed already") == 1

        choice.value = 1
        assert "⚠ Saved result may be out of date" in heading.value
        assert "✓ Reusable" not in heading.value
        assert action.value == "skip"
        assert "1 scan warning" in heading.value
        assert "⚠ 1 scan warning" not in heading.value
        assert "<b>ses-old (selected)</b>" in heading.value
        assert "no opposite phase-encoding DWI" in heading.value

        choice.value = 2
        assert "◐ Partial" in heading.value
        assert [value for _, value in action.options] == ["rerun", "skip"]
        assert action.value == "skip"
    finally:
        panel.close()


def test_configured_diffusion_analysis_refuses_unmatched_outputs(tmp_path, monkeypatch):
    from calmar.dmri_choice import show_dmri_choice

    option = {"session": "ses-dwi", "same_session": True, "has_reverse_phase": False,
              "warnings": [], "n_directions": 32, "shells": [0, 1000], "primary": {
        "dwi": str(tmp_path / "dwi.nii.gz"), "bval": str(tmp_path / "dwi.bval"),
        "bvec": str(tmp_path / "dwi.bvec"), "json": str(tmp_path / "dwi.json")},
        "series": []}
    entry = {"subject": "sub-one", "session": "ses-t1", "t1w": tmp_path / "t1.nii.gz"}
    namespace = {"CONFIG": {"MODALITY": "t1", "ANALYSE_TRACT_DWI": True},
                 "SUBJECTS": [entry], "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path}
    state = {"status": "⚠ existing QSIRecon", "current_complete": False,
             "prior_available": False, "outputs_exist": True, "rerun_required": True}
    monkeypatch.setattr("calmar.dmri_choice.dmri_options", lambda entry: [option])
    monkeypatch.setattr("calmar.dmri_choice.dmri_analysis_state", lambda *args: state)

    with pytest.raises(RuntimeError, match="DMRI_OVERWRITE=True"):
        show_dmri_choice(namespace)


def test_configured_diffusion_analysis_allows_explicit_rerun(tmp_path, monkeypatch):
    from calmar.dmri_choice import show_dmri_choice

    option = {"session": "ses-dwi", "same_session": True, "has_reverse_phase": False,
              "warnings": [], "n_directions": 32, "shells": [0, 1000], "primary": {
        "dwi": str(tmp_path / "dwi.nii.gz"), "bval": str(tmp_path / "dwi.bval"),
        "bvec": str(tmp_path / "dwi.bvec"), "json": str(tmp_path / "dwi.json")},
        "series": []}
    entry = {"subject": "sub-one", "session": "ses-t1", "t1w": tmp_path / "t1.nii.gz"}
    namespace = {"CONFIG": {"MODALITY": "t1", "ANALYSE_TRACT_DWI": True,
                            "DMRI_OVERWRITE": True},
                 "SUBJECTS": [entry], "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path}
    state = {"status": "↻ rerun requested", "current_complete": False,
             "prior_available": True, "outputs_exist": True, "rerun_required": True}
    monkeypatch.setattr("calmar.dmri_choice.dmri_options", lambda entry: [option])
    monkeypatch.setattr("calmar.dmri_choice.dmri_analysis_state", lambda *args: state)

    assert show_dmri_choice(namespace) is None
    assert namespace["CONFIG"]["ANALYSE_TRACT_DWI"] is True


def test_diffusion_choice_reports_complete_partial_and_unmatched_prior_analysis(tmp_path, monkeypatch):
    item = gradients(tmp_path / "raw", "sub-one_ses-dwi", [0] + [1000] * 32)
    item.update(subject="sub-one", session="ses-dwi", same_session=False)
    entry = {"subject": "sub-one", "session": "ses-t1", "t1w": tmp_path / "t1.nii.gz",
             "dwi_inventory": [item]}
    option = dmri_options(entry)[0]
    namespace = {"CONFIG": {"MODALITY": "t1"}, "SUBJECTS": [entry],
                 "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path}

    def cached(stage, entries, study):
        return [{"stage": stage}] if stage == "dmri_preproc" else [None]

    monkeypatch.setattr("calmar.scheduled.cached_step_results", cached)
    assert dmri_analysis_status(namespace, entry, option) == "◐ partly analysed: QSIPrep"

    with monkeypatch.context() as patcher:
        patcher.setattr(
            "calmar.scheduled.cached_step_results",
            lambda stage, entries, study: ([{"stage": stage}]
                                           if stage in ("dmri_preproc", "dmri_recon") else [None]))
        patcher.setattr(
            "calmar.scheduled.previous_step_results",
            lambda stage, entries, study: [{"stage": stage}])
        patcher.setattr(
            "calmar.scheduled.usable_previous_step_results",
            lambda stage, entries, study: [{"stage": stage}])
        state = dmri_analysis_state(namespace, entry, option)
        assert state["status"] == (
            "◐ partly analysed: QSIPrep, QSIRecon; "
            "input file date or size differs for this or an earlier stage: final metrics")
        assert state["kind"] == "partial_changed"
        assert state["rerun_required"] is False

    monkeypatch.setattr("calmar.scheduled.cached_step_results",
                        lambda stage, entries, study: [{"stage": stage}])
    assert dmri_analysis_status(namespace, entry, option) == "✓ analysed already (reusable)"

    monkeypatch.setattr("calmar.scheduled.cached_step_results",
                        lambda stage, entries, study: [None])
    prior = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsiprep"
    prior.mkdir(parents=True)
    # An empty/incomplete metrics directory is not a final metrics output.
    (tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/dwi/metrics").mkdir(parents=True)
    status = dmri_analysis_status(namespace, entry, option)
    assert status == "⚠ existing QSIPrep; no reusable receipt for current inputs/settings"
    assert dmri_analysis_state(namespace, entry, option)["rerun_required"] is True
    namespace["CONFIG"]["DMRI_OVERWRITE"] = True
    assert dmri_analysis_status(namespace, entry, option) == \
        "↻ rerun requested in CONFIG; existing results will not be reused"

    namespace["CONFIG"].pop("DMRI_OVERWRITE")
    monkeypatch.setattr(
        "calmar.scheduled.cached_step_results",
        lambda stage, entries, study: [{"stage": stage}] if stage == "dmri_recon" else [None])
    assert dmri_analysis_status(namespace, entry, option) == \
        "⚠ existing QSIPrep, QSIRecon; no reusable receipt for current inputs/settings"

    (prior.parent / "qsirecon").mkdir()
    monkeypatch.setattr(
        "calmar.scheduled.cached_step_results",
        lambda stage, entries, study: [{"stage": stage}] if stage == "dmri_preproc" else [None])
    assert dmri_analysis_status(namespace, entry, option) == \
        "◐ partly analysed: QSIPrep; later outputs not reusable: QSIRecon"

    def unavailable(stage, entries, study):
        raise ValueError("broken receipt")

    monkeypatch.setattr("calmar.scheduled.cached_step_results", unavailable)
    assert dmri_analysis_status(namespace, entry, option) == \
        "⚠ analysis status unavailable (ValueError)"


def test_dmri_status_finds_real_receipt_after_selection_and_rerun_for_mixed_cohort(
        tmp_path, monkeypatch):
    from calmar.scheduled import QC_VERSION, _split, _store
    from calmar.study import ENTRY_CONFIG, ENTRY_DATASET

    dataset = tmp_path / "cohort"
    item = gradients(dataset / "sub-one/ses-dwi/dwi", "sub-one_ses-dwi", [0] + [1000] * 32)
    item.update(subject="sub-one", session="ses-dwi", same_session=False)
    t1 = dataset / "sub-one/ses-t1/anat/sub-one_ses-t1_T1w.nii.gz"
    t1.parent.mkdir(parents=True)
    t1.write_bytes(b"t1")
    entry = {
        "subject": "sub-one", "session": "ses-t1", "t1w": t1,
        "dwi_inventory": [item], ENTRY_DATASET: str(dataset),
        ENTRY_CONFIG: {"DMRI_HMC_METHOD": "eddy"},
    }
    namespace = {
        "CONFIG": {"MODALITY": "t1", "ANALYSE_TRACT_DWI": None}, "SUBJECTS": [entry],
        "RAW_DATASET_DIR": tmp_path / "base", "PROJECT_DIR": tmp_path / "project",
    }
    option = dmri_options(entry)[0]
    apply_dmri_selection(namespace, {("sub-one", "ses-t1"): (entry, option)})
    selected = namespace["DMRI_SUBJECTS"][0]
    study = namespace["DMRI_STUDY"]
    request = {"dataset": str(study.dataset), "config": study.config, "entries": [selected]}
    payload = _split("dmri_preproc", request)[0]
    product = tmp_path / "published-qsiprep-result.txt"
    product.write_text("published")
    result = {
        "stage": "dmri_preproc", "job": "91", "request": payload, "qc_version": QC_VERSION,
        "results": [{"subject": "sub-one", "session": "ses-dwi", "seconds": 1,
                     "outputs": [{"path": str(product), "status": "computed"}],
                     "qc": {"complete": True}}],
    }
    _store("dmri_preproc", payload, study.project, result)
    # Reproduce a fresh notebook kernel: the status must round-trip through the
    # JSON receipt on disk, not the process-local cache populated by _store.
    monkeypatch.setattr("calmar.scheduled._MEMORY_CACHE", {})

    # apply_dmri_selection added dmri_analysis to SUBJECTS. Rechecking the cell
    # must strip that report link and find the same exact mixed-cohort receipt.
    rerun_entry = namespace["SUBJECTS"][0]
    rerun_option = dmri_options(rerun_entry)[0]
    current = dmri_analysis_state(namespace, rerun_entry, rerun_option)
    assert current["status"] == "◐ partly analysed: QSIPrep"
    assert current["rerun_required"] is False

    t1.write_bytes(b"changed-t1")
    changed = dmri_analysis_state(namespace, rerun_entry, rerun_option)
    assert changed["status"] == \
        "⚠ input file date or size differs for this or an earlier stage: QSIPrep"
    assert changed["prior_available"] is True
    assert changed["rerun_required"] is False


def test_configured_dmri_choice_still_prints_prior_status(tmp_path, monkeypatch, capsys):
    item = gradients(tmp_path, "sub-one_ses-dwi", [0] + [1000] * 32)
    item.update(subject="sub-one", session="ses-dwi", same_session=False)
    entry = {"subject": "sub-one", "session": "ses-t1", "t1w": tmp_path / "t1.nii.gz",
             "dwi_inventory": [item]}
    namespace = {"CONFIG": {"MODALITY": "t1", "ANALYSE_TRACT_DWI": False},
                 "SUBJECTS": [entry], "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path}
    monkeypatch.setattr("calmar.scheduled.cached_step_results",
                        lambda stage, entries, study: [None])
    assert show_dmri_choice(namespace) is None
    output = capsys.readouterr().out
    assert "disabled in CONFIG" in output
    assert "sub-one ses-dwi: ○ not analysed yet" in output


def test_primary_trace_dwi_route_is_not_mislabelled_as_t1_for_qsiprep(tmp_path, capsys):
    item = gradients(tmp_path, "sub-acute_ses-one", [0] + [1000] * 32)
    item.update(subject="sub-acute", session="ses-one", same_session=True)
    entry = {"subject": "sub-acute", "session": "ses-one", "t1w": item["dwi"],
             "dwi": item["dwi"], "dwi_inventory": [item]}
    namespace = {"CONFIG": {"MODALITY": "dwi", "ANALYSE_TRACT_DWI": True},
                 "SUBJECTS": [entry], "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path}
    assert show_dmri_choice(namespace) is None
    assert namespace["DMRI_SUBJECTS"] == []
    assert "requires a genuine T1w" in capsys.readouterr().out


def test_non_directional_dwi_status_is_separate_from_openads(tmp_path, capsys):
    dwi = tmp_path / "sub-one_ses-one_dwi.nii.gz"
    dwi.write_bytes(b"trace-dwi")
    entry = {"subject": "sub-one", "session": "ses-t1", "t1w": tmp_path / "t1.nii.gz",
             "dwi_inventory": [{"subject": "sub-one", "session": "ses-one", "dwi": dwi,
                                "bval": None, "bvec": None, "json": None}]}
    namespace = {"CONFIG": {"MODALITY": "t1"}, "SUBJECTS": [entry],
                 "RAW_DATASET_DIR": tmp_path, "PROJECT_DIR": tmp_path}

    assert show_dmri_choice(namespace) is None

    output = capsys.readouterr().out
    assert "none qualifies for the separate tract-microstructure workflow" in output
    assert "gradient-bearing 4-D series" in output
    assert "independent of OpenADS DWI+ADC acute-lesion segmentation" in output

    namespace["SUBJECTS"] = [{"subject": "sub-two", "session": "ses-t1",
                              "t1w": tmp_path / "other_t1.nii.gz"}]
    assert show_dmri_choice(namespace) is None
    assert "No gradient-bearing diffusion MRI was found" in capsys.readouterr().out


def tractometry(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([
        {"tract": "Arcuate fasciculus", "hemisphere": "left", "lesion_overlap_pct": 22.5,
         "fa": 0.38, "md_mm2_s": 0.00091, "summary_statistic": "median",
         "valid_voxel_pct": 84.0},
        {"tract": "Arcuate fasciculus", "hemisphere": "right", "lesion_overlap_pct": 0.0,
         "fa": 0.45, "md_mm2_s": 0.00078, "summary_statistic": "median",
         "valid_voxel_pct": 91.0},
    ]).to_csv(path, sep="\t", index=False)


def test_direct_tractometry_is_separate_and_conservative_in_report(tmp_path):
    entry = {"subject": "sub-one", "session": "ses-t1",
             "dmri_analysis": {"subject": "sub-one", "session": "ses-dwi"}}
    table, metadata = tractometry_paths(tmp_path, {}, entry)
    tractometry(table)
    metadata.write_text(json.dumps({"n_directions": 40, "shells": [0, 1000],
                                    "session": "ses-dwi", "anatomical_session": "ses-t1",
                                    "preprocessor": "QSIPrep 26.1.1",
                                    "hmc_method": "tortoise",
                                    "warnings": ["no opposite phase-encoding DWI"]}))
    html = direct_diffusion_section(tmp_path, {}, entry)
    assert "participant&rsquo;s own directional diffusion" in html
    assert "do not validate or numerically combine" in html
    assert "must therefore not be read as proof" in html
    assert "Arcuate fasciculus" in html and "22.5%" in html and "QSIPrep 26.1.1" in html
    assert "tortoise motion/eddy correction" in html
    assert "diffusion session ses-dwi" in html and "lesion/anatomy session ses-t1" in html


def test_selected_but_unprocessed_diffusion_does_not_hide_normative_result(tmp_path):
    entry = {"subject": "sub-one", "session": "ses-t1",
             "dmri_analysis": {"subject": "sub-one", "session": "ses-dwi"}}
    html = direct_diffusion_section(tmp_path, {}, entry)
    assert "no validated tractometry table" in html
    assert "normative BCB/DeepDisco section remains separate" in html


def test_invalid_tractometry_is_rejected(tmp_path):
    path = tmp_path / "tract.tsv"
    tractometry(path)
    table = pd.read_csv(path, sep="\t")
    table.loc[0, "fa"] = 1.5
    table.to_csv(path, sep="\t", index=False)
    with pytest.raises(ValueError, match="fa"):
        load_tractometry(path)
    tractometry(path)
    table = pd.read_csv(path, sep="\t")
    table.loc[0, "md_mm2_s"] = 0.82
    table.to_csv(path, sep="\t", index=False)
    with pytest.raises(ValueError, match="physical mm²/s"):
        load_tractometry(path)


def test_qsirecon_wide_bundle_statistics_are_normalized(tmp_path):
    source = tmp_path / "sub-one_bundles-DSIStudio_scalarstats.tsv"
    pd.DataFrame([{
        "bundle_Association_ArcuateFasciculusL_DTI_fa_mean": 0.41,
        "bundle_Association_ArcuateFasciculusL_DTI_fa_median": 0.39,
        "bundle_Association_ArcuateFasciculusL_DTI_md_median": 0.00082,
        "bundle_Association_ArcuateFasciculusR_DTI_fa_median": 0.46,
        "bundle_Association_ArcuateFasciculusR_DTI_md_median": 0.00076,
    }]).to_csv(source, sep="\t", index=False)
    table, sources = _scalar_rows(tmp_path)
    left = table[table["hemisphere"] == "left"].iloc[0]
    assert left["fa"] == 0.39 and left["md_mm2_s"] == 0.00082
    assert left["summary_statistic"] == "median"
    assert pd.isna(left["lesion_overlap_pct"]) and sources == [source]
    assert _bundle_side("Association_ExtremeCapsuleL") == "left"
    assert _bundle_side("Association_SuperiorLongitudinalFasciculus1R") == "right"
    assert _bundle_side("Commissure_CorpusCallosumBody") == "bilateral/unspecified"


def test_qsirecon_long_bundle_statistics_are_normalized_with_physical_md_units(tmp_path):
    source = tmp_path / "sub-one_model-ss3t_bundlestats.csv"
    pd.DataFrame([
        {"bundle_name": "Association_ArcuateFasciculusL", "dti_fa": 0.39, "md": 0.82},
        {"bundle_name": "Association_ArcuateFasciculusR", "dti_fa": 0.46, "md": 0.76},
    ]).to_csv(source, index=False)
    table, sources = _scalar_rows(tmp_path)
    left = table[table["hemisphere"] == "left"].iloc[0]
    assert left["fa"] == 0.39
    assert left["md_mm2_s"] == pytest.approx(0.00082)
    assert left["summary_statistic"] == "mean"
    assert sources == [source]


def test_qsirecon_md_units_are_checked_and_mixed_schemas_are_refused(tmp_path):
    ambiguous = tmp_path / "ambiguous_bundlestats.csv"
    pd.DataFrame([{
        "bundle_name": "Association_ArcuateFasciculusL", "dti_fa": 0.39, "md": 0.02,
    }]).to_csv(ambiguous, index=False)
    with pytest.raises(RuntimeError, match="ambiguous or implausible units"):
        _scalar_rows(tmp_path)

    ambiguous.unlink()
    pd.DataFrame([
        {"bundle_name": "Association_ArcuateFasciculusL", "dti_fa": 0.39, "md": 0.82},
        {"bundle_name": "Association_ArcuateFasciculusR", "dti_fa": 0.46, "md": 0.00076},
    ]).to_csv(tmp_path / "mixed_bundlestats.csv", index=False)
    with pytest.raises(RuntimeError, match="mix units within one table"):
        _scalar_rows(tmp_path)

    (tmp_path / "mixed_bundlestats.csv").unlink()
    pd.DataFrame([{
        "bundle_name": "Association_ArcuateFasciculusL", "dti_fa": 0.39, "md": 0.82,
    }]).to_csv(tmp_path / "valid_bundlestats.csv", index=False)
    pd.DataFrame([{
        "bundle_Association_ArcuateFasciculusL_DTI_fa_median": 0.39,
        "bundle_Association_ArcuateFasciculusL_DTI_md_median": 0.00082,
    }]).to_csv(tmp_path / "also_scalarstats.tsv", sep="\t", index=False)
    with pytest.raises(RuntimeError, match="both wide scalarstats and long bundlestats"):
        _scalar_rows(tmp_path)


def test_legacy_median_tractometry_contract_remains_readable(tmp_path):
    path = tmp_path / "legacy.tsv"
    pd.DataFrame([{
        "tract": "Arcuate fasciculus", "hemisphere": "left",
        "lesion_overlap_pct": 1.0, "fa_median": 0.4,
        "md_median_mm2_s": 0.0008, "valid_voxel_pct": 90.0,
    }]).to_csv(path, sep="\t", index=False)
    table = load_tractometry(path)
    assert table.loc[0, "fa"] == 0.4
    assert table.loc[0, "md_mm2_s"] == 0.0008
    assert table.loc[0, "summary_statistic"] == "median"


def test_old_direct_metrics_are_hidden_when_current_run_declines_dmri(tmp_path):
    entry = {"subject": "sub-one", "session": "ses-dwi"}
    table, _ = tractometry_paths(tmp_path, {}, entry)
    tractometry(table)
    assert direct_diffusion_section(tmp_path, {}, entry) is None


def test_staged_bids_keeps_diffusion_session_and_records_cross_session_anatomy(tmp_path):
    dataset = tmp_path / "data"
    dwi_item = gradients(dataset / "sub-one/ses-dwi/dwi", "sub-one_ses-dwi", [0] + [1000] * 32)
    t1w = dataset / "sub-one/ses-t1/anat/sub-one_ses-t1_T1w.nii.gz"
    mask = dataset / "manual/sub-one_ses-t1_desc-lesion_mask.nii.gz"
    for path in (t1w, mask):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"fixture")
    entry = {"subject": "sub-one", "session": "ses-dwi", "t1w": t1w,
             "anatomical_session": "ses-t1", "anatomical_t1w": t1w,
             "dmri_assessment": {"series": [dwi_item]}}
    request = {"dataset": str(dataset), "entries": [entry],
               "config": {"MODALITY": "t1", "SEGMENTATION_METHODS": ["synthstroke"],
                          "MANUAL_MASK_PATH": str(mask), "MANUAL_MASK_SPACE": "t1",
                          "DMRI_MASK_SOURCE": "manual"}}
    staged = tmp_path / "staged"
    provenance = stage_bids(request, entry, staged)
    assert (staged / "sub-one/ses-dwi/anat/sub-one_ses-dwi_T1w.nii.gz").is_file()
    assert (staged / "sub-one/ses-dwi/anat/sub-one_ses-dwi_label-lesion_roi.nii.gz").is_file()
    assert list((staged / "sub-one/ses-dwi/dwi").glob("*_dwi.bval"))
    assert provenance["cross_session_anatomy"] is True


def test_failed_dmri_tool_surfaces_its_log_tail(tmp_path, monkeypatch):
    log = tmp_path / "tool.log"
    crash = tmp_path / "work/crash-fixture.txt"

    def fail(command, **kwargs):
        kwargs["stdout"].write("specific QSIPrep diagnostic\n")
        crash.parent.mkdir()
        crash.write_text("crash detail")
        return SimpleNamespace(returncode=23)

    monkeypatch.setattr(dmri_pipeline.subprocess, "run", fail)
    with pytest.raises(RuntimeError, match="specific QSIPrep diagnostic") as error:
        _run(["qsiprep", "input", "output"], log, failure_dir=tmp_path / "retained")
    assert "exit status 23" in str(error.value)
    assert "diagnostics retained" in str(error.value)
    assert log.read_text() == "specific QSIPrep diagnostic\n"
    assert (tmp_path / "retained/tool.log").is_file()
    assert list((tmp_path / "retained").glob("*-crash-fixture.txt"))


def test_failed_dmri_tool_keeps_original_error_when_diagnostic_copy_fails(tmp_path, monkeypatch):
    log = tmp_path / "tool.log"

    def fail(command, **kwargs):
        kwargs["stdout"].write("specific tool failure\n")
        return SimpleNamespace(returncode=17)

    monkeypatch.setattr(dmri_pipeline.subprocess, "run", fail)
    monkeypatch.setattr(dmri_pipeline.shutil, "copy2",
                        lambda *args, **kwargs: (_ for _ in ()).throw(OSError("disk full")))
    with pytest.raises(RuntimeError, match="specific tool failure") as error:
        _run(["qsirecon", "input", "output"], log, failure_dir=tmp_path / "retained")
    assert "exit status 17" in str(error.value)
    assert "Diagnostics could not be retained: disk full" in str(error.value)


def test_first_publish_failure_retains_completed_attempt(tmp_path, monkeypatch):
    attempt = tmp_path / "attempt"
    attempt.mkdir()
    (attempt / "finished-output").write_text("recoverable")
    final = tmp_path / "published"

    monkeypatch.setenv("SLURM_JOB_ID", "321")
    monkeypatch.setattr(dmri_pipeline.subprocess, "run",
                        lambda *args, **kwargs: (_ for _ in ()).throw(
                            subprocess.CalledProcessError(1, args[0])))
    with pytest.raises(subprocess.CalledProcessError):
        dmri_pipeline._publish(attempt, final, "dmri_recon", "qsirecon", "script.sh")

    retained = list(tmp_path.glob("published.publish-failed.321.*"))
    assert len(retained) == 1
    assert (retained[0] / "finished-output").read_text() == "recoverable"
    assert not attempt.exists() and not final.exists()


def test_tortoise_is_the_selected_qsiprep_hmc_default():
    assert _hmc_method({}) == "tortoise"
    assert _hmc_method({"DMRI_HMC_METHOD": "eddy"}) == "eddy"
    with pytest.raises(ValueError, match="tortoise, eddy or shoreline"):
        _hmc_method({"DMRI_HMC_METHOD": "unknown"})


def test_existing_qsiprep_derivative_fails_before_staging(tmp_path, monkeypatch):
    entry = {"subject": "sub-one", "session": "ses-dwi"}
    request = {"dataset": str(tmp_path), "entries": [entry], "config": {}}
    final = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsiprep"
    final.mkdir(parents=True)
    monkeypatch.setenv("SLURM_JOB_ID", "123")
    monkeypatch.setenv("CALMAR_EXECUTION_SCRIPT", "src/analysis_45_dmri_preproc.sh")
    monkeypatch.setattr(dmri_pipeline, "stage_bids",
                        lambda *args, **kwargs: pytest.fail("staging should not run"))
    with pytest.raises(FileExistsError, match="DMRI_OVERWRITE=True"):
        preprocess(request, tmp_path / "result")


def test_preprocess_passes_selected_hmc_method_to_qsiprep(tmp_path, monkeypatch):
    entry = {"subject": "sub-one", "session": "ses-dwi", "t1w": "unused"}
    request = {"dataset": str(tmp_path), "entries": [entry],
               "config": {"DMRI_HMC_METHOD": "tortoise"}}
    commands = []

    def staged(request, entry, destination):
        Path(destination).mkdir(parents=True)
        return {"cross_session_anatomy": False}

    def run(command, log, **kwargs):
        commands.append([str(value) for value in command])
        produced = Path(command[2])
        produced.mkdir(parents=True)
        (produced / "sub-one_desc-preproc_dwi.nii.gz").write_bytes(b"fixture")
        (produced / "sub-one.html").write_text("report")
        Path(log).write_text("log")

    monkeypatch.setenv("SLURM_JOB_ID", "123")
    monkeypatch.setenv("CALMAR_EXECUTION_SCRIPT", "src/analysis_45_dmri_preproc.sh")
    monkeypatch.setattr(dmri_pipeline, "stage_bids", staged)
    monkeypatch.setattr(dmri_pipeline, "_run", run)
    monkeypatch.setattr(dmri_pipeline, "_publish", lambda *args, **kwargs: None)
    monkeypatch.setattr(dmri_pipeline, "_publish_result", lambda *args, **kwargs: None)
    preprocess(request, tmp_path / "result")
    command = commands[0]
    assert command[command.index("--hmc-method") + 1] == "tortoise"


def test_metrics_methods_come_from_published_derivatives(tmp_path):
    entry = {"subject": "sub-one", "session": "ses-dwi"}
    request = {"dataset": str(tmp_path), "entries": [entry],
               "config": {"DMRI_HMC_METHOD": "tortoise", "DMRI_RECON_SPEC": "wrong-current-value"}}
    preproc = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsiprep"
    recon = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsirecon"
    preproc.mkdir(parents=True)
    recon.mkdir(parents=True)
    (preproc / "calmar-selection.json").write_text(json.dumps({"hmc_method": "eddy"}))
    (recon / "calmar-reconstruction.json").write_text(json.dumps({"recon_spec": "published-spec"}))
    assert _derivative_methods(request, entry) == ("eddy", "published-spec")


def test_metrics_hmc_method_can_come_from_retained_legacy_qsiprep_log(tmp_path):
    entry = {"subject": "sub-one", "session": "ses-dwi"}
    request = {"dataset": str(tmp_path), "entries": [entry], "config": {}}
    preproc = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsiprep"
    recon = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsirecon"
    preproc.mkdir(parents=True)
    recon.mkdir(parents=True)
    (preproc / "calmar-selection.json").write_text(json.dumps({"subject": "sub-one"}))
    (preproc / "calmar-qsiprep.log").write_text(
        "Processing preview: TORTOISE + DRBUDDI (--hmc-method tortoise --sdc-method drbuddi)\n")
    (recon / "calmar-reconstruction.json").write_text(json.dumps({"recon_spec": "published-spec"}))
    assert _derivative_methods(request, entry) == ("tortoise", "published-spec")


def test_reconstruction_command_uses_installed_spec_name_and_license(tmp_path, monkeypatch):
    entry = {"subject": "sub-one", "session": "ses-dwi", "t1w": str(tmp_path / "T1w.nii.gz")}
    license_file = tmp_path / "license.txt"
    license_file.write_text("fixture")
    request = {"dataset": str(tmp_path), "entries": [entry],
               "config": {"FS_LICENSE": str(license_file)}}
    preproc = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsiprep"
    preproc.mkdir(parents=True)
    commands = []
    def run(command, log, **kwargs):
        commands.append([str(value) for value in command])
        produced = Path(command[2])
        produced.mkdir(parents=True)
        (produced / "sub-one_scalarstats.tsv").write_text("x\n1\n")
        (produced / "sub-one_streamlines.tck.gz").write_bytes(b"x")
        (produced / "sub-one.html").write_text("report")
        Path(log).write_text("log")
    monkeypatch.setenv("SLURM_JOB_ID", "123")
    monkeypatch.setenv("CALMAR_EXECUTION_SCRIPT", "src/analysis_46_dmri_recon.sh")
    monkeypatch.setattr(dmri_pipeline, "_run", run)
    monkeypatch.setattr(dmri_pipeline, "_observed_reconstruction", lambda *args: {
        "recon_spec": "ss3t_fod_autotrack", "qsirecon_version": "26.0.1",
        "qsiprep_version": "26.1.1"})
    monkeypatch.setattr(dmri_pipeline, "_publish", lambda *args, **kwargs: None)
    monkeypatch.setattr(dmri_pipeline, "_publish_result", lambda *args, **kwargs: None)
    dmri_pipeline.reconstruct(request, tmp_path / "result")
    command = commands[0]
    assert command[command.index("--recon-spec") + 1] == "ss3t_fod_autotrack"
    assert command[command.index("--fs-license-file") + 1] == str(license_file)


def test_reconstruction_publish_failure_retains_rerunnable_attempt(tmp_path, monkeypatch):
    entry = {"subject": "sub-one", "session": "ses-dwi", "t1w": str(tmp_path / "T1w.nii.gz")}
    license_file = tmp_path / "license.txt"
    license_file.write_text("fixture")
    request = {"dataset": str(tmp_path), "entries": [entry],
               "config": {"FS_LICENSE": str(license_file)}}
    preproc = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsiprep"
    preproc.mkdir(parents=True)

    def run(command, log, **kwargs):
        produced = Path(command[2])
        produced.mkdir(parents=True)
        pd.DataFrame([{
            "bundle_name": "Association_ArcuateFasciculusL", "dti_fa": 0.4, "md": 0.8,
        }]).to_csv(produced / "sub-one_bundlestats.csv", index=False)
        (produced / "sub-one_streamlines.tck.gz").write_bytes(b"tract")
        (produced / "sub-one.html").write_text("report")
        Path(log).write_text("completed")

    monkeypatch.setenv("SLURM_JOB_ID", "456")
    monkeypatch.setenv("CALMAR_EXECUTION_SCRIPT", "src/analysis_46_dmri_recon.sh")
    monkeypatch.setattr(dmri_pipeline, "_run", run)
    monkeypatch.setattr(dmri_pipeline, "_observed_reconstruction", lambda *args: {
        "recon_spec": "ss3t_fod_autotrack", "qsirecon_version": "26.0.1",
        "qsiprep_version": "26.1.1"})
    def fail_publish(temporary, final, *args, **kwargs):
        failed = Path(final).with_name("qsirecon.publish-failed.456.fixture")
        os.replace(temporary, failed)
        Path(str(failed) + ".prov.json").write_text("partial publisher sidecar")
        error = subprocess.CalledProcessError(1, ["publish"])
        error.calmar_failed_path = failed
        raise error

    monkeypatch.setattr(dmri_pipeline, "_publish", fail_publish)

    with pytest.raises(RuntimeError, match="provenance publication failed") as error:
        dmri_pipeline.reconstruct(request, tmp_path / "result")
    retained = preproc.parent / "qsirecon.failed.456"
    assert str(retained) in str(error.value)
    assert (retained / "produced/sub-one_bundlestats.csv").is_file()
    assert (retained / "produced/calmar-reconstruction.json").is_file()
    assert (retained / "qsirecon.log").read_text() == "completed"
    assert (retained / "failed-publication.prov.json").read_text() == "partial publisher sidecar"


def test_reconstruction_contract_failure_names_and_retains_missing_artifacts(tmp_path, monkeypatch):
    entry = {"subject": "sub-one", "session": "ses-dwi", "t1w": str(tmp_path / "T1w.nii.gz")}
    license_file = tmp_path / "license.txt"
    license_file.write_text("fixture")
    request = {"dataset": str(tmp_path), "entries": [entry],
               "config": {"FS_LICENSE": str(license_file)}}
    preproc = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsiprep"
    preproc.mkdir(parents=True)

    def run(command, log, **kwargs):
        produced = Path(command[2])
        produced.mkdir(parents=True)
        (produced / "sub-one_scalarstats.tsv").write_text("x\n1\n")
        (produced / "sub-one.html").write_text("report")
        Path(log).write_text("successful QSIRecon log")

    monkeypatch.setenv("SLURM_JOB_ID", "456")
    monkeypatch.setenv("CALMAR_EXECUTION_SCRIPT", "src/analysis_46_dmri_recon.sh")
    monkeypatch.setattr(dmri_pipeline, "_run", run)

    with pytest.raises(RuntimeError, match="required bundle streamlines") as error:
        dmri_pipeline.reconstruct(request, tmp_path / "result")

    retained = preproc.parent / "qsirecon.failed.456"
    assert str(retained) in str(error.value)
    assert (retained / "qsirecon.log").read_text() == "successful QSIRecon log"
    assert (retained / "produced/sub-one_scalarstats.tsv").is_file()
    inventory = json.loads((retained / "artifact-inventory.json").read_text())
    assert inventory["missing_required_artifacts"] == ["bundle streamlines"]
    assert inventory["matched_artifact_counts"] == {
        "tractometry statistics": 1, "bundle streamlines": 0, "HTML report": 1}
    assert {item["path"] for item in inventory["files"]} == {
        "sub-one.html", "sub-one_scalarstats.tsv"}


def test_reconstruction_contract_failure_uses_unique_folder_and_keeps_work(tmp_path, monkeypatch):
    entry = {"subject": "sub-one", "session": "ses-dwi", "t1w": str(tmp_path / "T1w.nii.gz")}
    license_file = tmp_path / "license.txt"
    license_file.write_text("fixture")
    request = {"dataset": str(tmp_path), "entries": [entry],
               "config": {"FS_LICENSE": str(license_file), "DMRI_OVERWRITE": True}}
    parent = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi"
    (parent / "qsiprep").mkdir(parents=True)
    existing = parent / "qsirecon"
    existing.mkdir()
    (existing / "published-result").write_text("untouched")
    occupied = parent / "qsirecon.failed.456"
    occupied.mkdir()
    (occupied / "earlier-attempt").write_text("preserved")

    def run(command, log, **kwargs):
        produced = Path(command[2])
        produced.mkdir(parents=True)
        (produced / "sub-one_scalarstats.tsv").write_text("x\n1\n")
        (produced / "sub-one.html").write_text("report")
        work = Path(command[command.index("-w") + 1])
        work.mkdir(parents=True)
        (work / "resume-cache").write_text("retained")
        Path(log).write_text("successful QSIRecon log")

    monkeypatch.setenv("SLURM_JOB_ID", "456")
    monkeypatch.setenv("CALMAR_EXECUTION_SCRIPT", "src/analysis_46_dmri_recon.sh")
    monkeypatch.setattr(dmri_pipeline, "_run", run)

    with pytest.raises(RuntimeError) as error:
        dmri_pipeline.reconstruct(request, tmp_path / "result")

    retained = Path(str(error.value).split("retained in ", 1)[1].rstrip("."))
    assert retained != occupied and retained.name.startswith("qsirecon.failed.456.")
    assert (occupied / "earlier-attempt").read_text() == "preserved"
    assert (retained / "work/resume-cache").read_text() == "retained"
    assert (existing / "published-result").read_text() == "untouched"


def test_complete_retained_reconstruction_can_be_published_without_rerunning(tmp_path, monkeypatch):
    entry = {"subject": "sub-one", "session": "ses-dwi"}
    request = {"dataset": str(tmp_path), "entries": [entry], "config": {}}
    retained = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsirecon.failed.81"
    produced = retained / "produced"
    produced.mkdir(parents=True)
    pd.DataFrame([{
        "bundle_name": "Association_ArcuateFasciculusL", "dti_fa": 0.4, "md": 0.8,
    }]).to_csv(produced / "sub-one_model-ss3t_bundlestats.csv", index=False)
    (produced / "sub-one_streamlines.tck.gz").write_bytes(b"tract")
    (produced / "sub-one.html").write_text("report")
    (produced / "calmar-qsirecon.log").write_text("earlier CALMaR log")
    (produced / "calmar-reconstruction.json").write_text('{"earlier": true}\n')
    (retained / "qsirecon.log").write_text("completed QSIRecon")
    published = []
    results = []

    monkeypatch.setenv("SLURM_JOB_ID", "88")
    monkeypatch.setenv("CALMAR_EXECUTION_SCRIPT", "src/analysis_57_recover_dmri_recon.sh")
    monkeypatch.setattr(dmri_pipeline, "_observed_reconstruction", lambda *args: {
        "recon_spec": "ss3t_fod_autotrack", "qsirecon_version": "26.0.1",
        "qsiprep_version": "26.1.1"})
    monkeypatch.setattr(dmri_pipeline.subprocess, "run", lambda *args, **kwargs:
                        SimpleNamespace(stdout="qsirecon version 26.0.1", stderr=""))
    def publish(*args, **kwargs):
        staged = Path(args[0])
        published.append((args, json.loads((staged / "calmar-reconstruction.json").read_text()),
                          (staged / "calmar-qsirecon.log").read_text()))

    monkeypatch.setattr(dmri_pipeline, "_publish", publish)
    monkeypatch.setattr(dmri_pipeline, "_publish_result", lambda *args, **kwargs: results.append(args))
    dmri_pipeline.recover_reconstruction(request, retained, tmp_path / "result")

    _, record, staged_log = published[0]
    assert record["compute_job"] == "81" and record["recovery_job"] == "88"
    assert record["tractometry_tables"] == ["sub-one_model-ss3t_bundlestats.csv"]
    assert staged_log == "completed QSIRecon"
    assert published[0][0][2:4] == ("dmri_recon", "qsirecon")
    assert (produced / "calmar-reconstruction.json").read_text() == '{"earlier": true}\n'
    assert (produced / "calmar-qsirecon.log").read_text() == "earlier CALMaR log"
    assert results[0][1] == "dmri_recon"


def test_observed_reconstruction_is_read_from_tool_records(tmp_path):
    produced = tmp_path / "produced"
    config = produced / "sub-one/log/run/qsirecon.toml"
    config.parent.mkdir(parents=True)
    config.write_text("""
[environment]
version = "26.0.1"
[execution]
participant_label = ["one"]
processing_list = ["sub-one/ses-dwi/dwi/sub-one_ses-dwi_dwi.nii.gz:sub-one/anat/T1w.nii.gz"]
[workflow]
recon_spec = "ss3t_fod_autotrack"
""")
    derivative = produced / "derivatives/recon/sub-one/ses-dwi"
    derivative.mkdir(parents=True)
    (produced / "dataset_description.json").write_text(json.dumps({"GeneratedBy": [
        {"Name": "qsirecon", "Version": "26.0.1"},
        {"Name": "qsiprep", "Version": "26.1.1"},
    ]}))
    observed = dmri_pipeline._observed_reconstruction(
        produced, {"subject": "sub-one", "session": "ses-dwi"})
    assert observed == {"recon_spec": "ss3t_fod_autotrack",
                        "qsirecon_version": "26.0.1", "qsiprep_version": "26.1.1"}

    config.write_text(config.read_text().replace('["one"]', '["two"]'))
    with pytest.raises(RuntimeError, match="not participant one"):
        dmri_pipeline._observed_reconstruction(produced, entry={
            "subject": "sub-one", "session": "ses-dwi"})


def test_sessionless_recovery_refuses_sessioned_tool_record(tmp_path):
    produced = tmp_path / "produced"
    config = produced / "sub-one/log/run/qsirecon.toml"
    config.parent.mkdir(parents=True)
    config.write_text("""
[environment]
version = "26.0.1"
[execution]
participant_label = ["one"]
processing_list = ["sub-one/ses-dwi/dwi/sub-one_ses-dwi_dwi.nii.gz:sub-one/anat/T1w.nii.gz"]
[workflow]
recon_spec = "ss3t_fod_autotrack"
""")
    (produced / "derivatives/recon/sub-one/ses-dwi").mkdir(parents=True)
    (produced / "dataset_description.json").write_text(json.dumps({"GeneratedBy": [
        {"Name": "qsirecon", "Version": "26.0.1"},
    ]}))
    with pytest.raises(RuntimeError, match="sessioned, but the request has no session"):
        dmri_pipeline._observed_reconstruction(
            produced, {"subject": "sub-one", "session": None})


def test_recovery_version_match_is_exact(tmp_path, monkeypatch):
    entry = {"subject": "sub-one", "session": "ses-dwi"}
    request = {"dataset": str(tmp_path), "entries": [entry], "config": {}}
    retained = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsirecon.failed.81"
    produced = retained / "produced"
    produced.mkdir(parents=True)
    pd.DataFrame([{
        "bundle_name": "Association_ArcuateFasciculusL", "dti_fa": 0.4, "md": 0.8,
    }]).to_csv(produced / "sub-one_bundlestats.csv", index=False)
    (produced / "sub-one_streamlines.tck.gz").write_bytes(b"tract")
    (produced / "sub-one.html").write_text("report")
    (retained / "qsirecon.log").write_text("completed")
    monkeypatch.setenv("SLURM_JOB_ID", "88")
    monkeypatch.setenv("CALMAR_EXECUTION_SCRIPT", "src/analysis_57_recover_dmri_recon.sh")
    monkeypatch.setattr(dmri_pipeline, "_observed_reconstruction", lambda *args: {
        "recon_spec": "ss3t_fod_autotrack", "qsirecon_version": "26.0.1",
        "qsiprep_version": "26.1.1"})
    monkeypatch.setattr(dmri_pipeline.subprocess, "run", lambda *args, **kwargs:
                        SimpleNamespace(stdout="qsirecon version 26.0.10", stderr=""))
    with pytest.raises(RuntimeError, match="used 26.0.1.*26.0.10"):
        dmri_pipeline.recover_reconstruction(request, retained, tmp_path / "result")


def test_recovery_publish_failure_leaves_original_attempt_rerunnable(tmp_path, monkeypatch):
    entry = {"subject": "sub-one", "session": "ses-dwi"}
    request = {"dataset": str(tmp_path), "entries": [entry], "config": {}}
    retained = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsirecon.failed.81"
    produced = retained / "produced"
    produced.mkdir(parents=True)
    source = produced / "sub-one_bundlestats.csv"
    pd.DataFrame([{
        "bundle_name": "Association_ArcuateFasciculusL", "dti_fa": 0.4, "md": 0.8,
    }]).to_csv(source, index=False)
    (produced / "sub-one_streamlines.tck.gz").write_bytes(b"tract")
    (produced / "sub-one.html").write_text("report")
    (retained / "qsirecon.log").write_text("completed")
    monkeypatch.setenv("SLURM_JOB_ID", "88")
    monkeypatch.setenv("CALMAR_EXECUTION_SCRIPT", "src/analysis_57_recover_dmri_recon.sh")
    monkeypatch.setattr(dmri_pipeline, "_observed_reconstruction", lambda *args: {
        "recon_spec": "ss3t_fod_autotrack", "qsirecon_version": "26.0.1",
        "qsiprep_version": "26.1.1"})
    monkeypatch.setattr(dmri_pipeline.subprocess, "run", lambda *args, **kwargs:
                        SimpleNamespace(stdout="qsirecon version 26.0.1", stderr=""))

    def fail_publish(temporary, final, *args, **kwargs):
        failed = Path(final).with_name("qsirecon.publish-failed.88.fixture")
        os.replace(temporary, failed)
        error = subprocess.CalledProcessError(1, ["publish"])
        error.calmar_failed_path = failed
        raise error

    monkeypatch.setattr(dmri_pipeline, "_publish", fail_publish)
    with pytest.raises(subprocess.CalledProcessError):
        dmri_pipeline.recover_reconstruction(request, retained, tmp_path / "result")
    assert source.is_file()
    assert (retained / "qsirecon.log").read_text() == "completed"
    assert not (produced / "calmar-reconstruction.json").exists()
    assert not (produced / "calmar-qsirecon.log").exists()
    assert (retained.parent / "qsirecon.publish-failed.88.fixture").is_dir()


def test_recovery_refuses_requested_spec_that_differs_from_observed(tmp_path, monkeypatch):
    entry = {"subject": "sub-one", "session": "ses-dwi"}
    request = {"dataset": str(tmp_path), "entries": [entry],
               "config": {"DMRI_RECON_SPEC": "different_spec"}}
    retained = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsirecon.failed.81"
    produced = retained / "produced"
    produced.mkdir(parents=True)
    pd.DataFrame([{
        "bundle_name": "Association_ArcuateFasciculusL", "dti_fa": 0.4, "md": 0.8,
    }]).to_csv(produced / "sub-one_bundlestats.csv", index=False)
    (produced / "sub-one_streamlines.tck.gz").write_bytes(b"tract")
    (produced / "sub-one.html").write_text("report")
    (retained / "qsirecon.log").write_text("completed")
    monkeypatch.setenv("SLURM_JOB_ID", "88")
    monkeypatch.setenv("CALMAR_EXECUTION_SCRIPT", "src/analysis_57_recover_dmri_recon.sh")
    monkeypatch.setattr(dmri_pipeline, "_observed_reconstruction", lambda *args: {
        "recon_spec": "ss3t_fod_autotrack", "qsirecon_version": "26.0.1",
        "qsiprep_version": "26.1.1"})
    monkeypatch.setattr(dmri_pipeline.subprocess, "run",
                        lambda *args, **kwargs: pytest.fail("version check must follow spec check"))
    with pytest.raises(RuntimeError, match="used 'ss3t_fod_autotrack'.*records 'different_spec'"):
        dmri_pipeline.recover_reconstruction(request, retained, tmp_path / "result")


def test_retained_reconstruction_recovery_refuses_incomplete_attempt(tmp_path, monkeypatch):
    entry = {"subject": "sub-one", "session": "ses-dwi"}
    request = {"dataset": str(tmp_path), "entries": [entry], "config": {}}
    retained = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsirecon.failed.81"
    (retained / "produced").mkdir(parents=True)
    (retained / "qsirecon.log").write_text("completed QSIRecon")
    monkeypatch.setenv("SLURM_JOB_ID", "88")
    monkeypatch.setenv("CALMAR_EXECUTION_SCRIPT", "src/analysis_57_recover_dmri_recon.sh")
    monkeypatch.setattr(dmri_pipeline, "_publish",
                        lambda *args, **kwargs: pytest.fail("incomplete output must not publish"))
    with pytest.raises(RuntimeError, match="missing tractometry statistics"):
        dmri_pipeline.recover_reconstruction(request, retained, tmp_path / "result")


def test_qsiprep_contract_failure_retains_completed_attempt(tmp_path, monkeypatch):
    entry = {"subject": "sub-one", "session": "ses-dwi", "t1w": str(tmp_path / "T1w.nii.gz")}
    request = {"dataset": str(tmp_path), "entries": [entry], "config": {}}

    def staged(request, entry, destination):
        Path(destination).mkdir(parents=True)
        return {"cross_session_anatomy": False}

    def run(command, log, **kwargs):
        produced = Path(command[2])
        produced.mkdir(parents=True)
        (produced / "sub-one_desc-preproc_dwi.nii.gz").write_bytes(b"fixture")
        Path(log).write_text("successful QSIPrep log")

    monkeypatch.setenv("SLURM_JOB_ID", "789")
    monkeypatch.setenv("CALMAR_EXECUTION_SCRIPT", "src/analysis_45_dmri_preproc.sh")
    monkeypatch.setattr(dmri_pipeline, "stage_bids", staged)
    monkeypatch.setattr(dmri_pipeline, "_run", run)

    with pytest.raises(RuntimeError, match="required HTML report") as error:
        preprocess(request, tmp_path / "result")

    retained = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsiprep.failed.789"
    assert str(retained) in str(error.value)
    assert (retained / "qsiprep.log").read_text() == "successful QSIPrep log"
    assert (retained / "produced/sub-one_desc-preproc_dwi.nii.gz").is_file()


def test_contract_output_survives_inventory_write_failure(tmp_path, monkeypatch):
    attempt = tmp_path / "attempt"
    produced = attempt / "produced"
    produced.mkdir(parents=True)
    (produced / "valuable-output.nii.gz").write_bytes(b"result")
    original_write_text = Path.write_text

    def fail_inventory(path, *args, **kwargs):
        if path.name == "artifact-inventory.json":
            raise OSError("simulated full disk")
        return original_write_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", fail_inventory)
    retained, diagnostic_error = dmri_pipeline._retain_contract_failure(
        attempt, tmp_path / "qsirecon.failed.1", ["HTML report"], {"HTML report": 0})

    assert not attempt.exists()
    assert (retained / "produced/valuable-output.nii.gz").read_bytes() == b"result"
    assert "simulated full disk" in diagnostic_error
