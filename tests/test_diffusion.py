import json
import math
from pathlib import Path

import pandas as pd
import pytest

import calmar.dmri_pipeline as dmri_pipeline
from calmar.diffusion import (assess_dwi_series, assess_dwi_sessions,
                              direct_diffusion_section, load_tractometry,
                              tractometry_paths)
from calmar.dmri_choice import apply_dmri_selection, dmri_options, show_dmri_choice
from calmar.dmri_pipeline import _bundle_side, _scalar_rows, stage_bids


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


def tractometry(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([
        {"tract": "Arcuate fasciculus", "hemisphere": "left", "lesion_overlap_pct": 22.5,
         "fa_median": 0.38, "md_median_mm2_s": 0.00091, "valid_voxel_pct": 84.0},
        {"tract": "Arcuate fasciculus", "hemisphere": "right", "lesion_overlap_pct": 0.0,
         "fa_median": 0.45, "md_median_mm2_s": 0.00078, "valid_voxel_pct": 91.0},
    ]).to_csv(path, sep="\t", index=False)


def test_direct_tractometry_is_separate_and_conservative_in_report(tmp_path):
    entry = {"subject": "sub-one", "session": "ses-t1",
             "dmri_analysis": {"subject": "sub-one", "session": "ses-dwi"}}
    table, metadata = tractometry_paths(tmp_path, {}, entry)
    tractometry(table)
    metadata.write_text(json.dumps({"n_directions": 40, "shells": [0, 1000],
                                    "session": "ses-dwi", "anatomical_session": "ses-t1",
                                    "preprocessor": "QSIPrep 26.1.1",
                                    "warnings": ["no opposite phase-encoding DWI"]}))
    html = direct_diffusion_section(tmp_path, {}, entry)
    assert "participant&rsquo;s own directional diffusion" in html
    assert "do not validate or numerically combine" in html
    assert "must therefore not be read as proof" in html
    assert "Arcuate fasciculus" in html and "22.5%" in html and "QSIPrep 26.1.1" in html
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
    table.loc[0, "fa_median"] = 1.5
    table.to_csv(path, sep="\t", index=False)
    with pytest.raises(ValueError, match="fa_median"):
        load_tractometry(path)
    tractometry(path)
    table = pd.read_csv(path, sep="\t")
    table.loc[0, "md_median_mm2_s"] = 0.82
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
    assert left["fa_median"] == 0.39 and left["md_median_mm2_s"] == 0.00082
    assert pd.isna(left["lesion_overlap_pct"]) and sources == [source]
    assert _bundle_side("Association_ExtremeCapsuleL") == "left"
    assert _bundle_side("Association_SuperiorLongitudinalFasciculus1R") == "right"
    assert _bundle_side("Commissure_CorpusCallosumBody") == "bilateral/unspecified"


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


def test_reconstruction_command_uses_installed_spec_name_and_license(tmp_path, monkeypatch):
    entry = {"subject": "sub-one", "session": "ses-dwi", "t1w": str(tmp_path / "T1w.nii.gz")}
    license_file = tmp_path / "license.txt"
    license_file.write_text("fixture")
    request = {"dataset": str(tmp_path), "entries": [entry],
               "config": {"FS_LICENSE": str(license_file)}}
    preproc = tmp_path / "derivatives/calmar-dmri/sub-one/ses-dwi/qsiprep"
    preproc.mkdir(parents=True)
    commands = []
    def run(command, log):
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
    monkeypatch.setattr(dmri_pipeline, "_publish", lambda *args, **kwargs: None)
    monkeypatch.setattr(dmri_pipeline, "_publish_result", lambda *args, **kwargs: None)
    dmri_pipeline.reconstruct(request, tmp_path / "result")
    command = commands[0]
    assert command[command.index("--recon-spec") + 1] == "ss3t_fod_autotrack"
    assert command[command.index("--fs-license-file") + 1] == str(license_file)
