"""Local data: images imported into a BIDS dataset, and WAB-R participant data."""
import json
from pathlib import Path

import nibabel as nib
import numpy as np
import pandas as pd
import pytest

from calmar import local_import as li
from calmar import participant_data as pdata
from calmar.participant_report import participant_row, row_to_predictors
from calmar.study import discover_dwi, discover_t1w


def nifti(path, shape=(8, 9, 10), gz=True):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    nib.save(nib.Nifti1Image(np.ones(shape, dtype=np.float32), np.diag([2, 2, 2, 1])), str(path))
    return path


# ── participant data ─────────────────────────────────────────────────────────

def test_participant_ids_are_bids_labels():
    assert pdata.participant_id("12") == "sub-12" == pdata.participant_id("sub-12")
    assert pdata.participant_id("P 0-12") == "sub-P012"
    with pytest.raises(ValueError):
        pdata.participant_id(" - ")


def test_wab_aq_and_suggested_type():
    broca = dict(wab_info_content=5, wab_fluency=2, wab_comprehension=7.5, wab_repetition=4, wab_naming=5)
    assert pdata.wab_aq(broca) == 47.0
    assert pdata.suggest_wab_type(broca) == "Broca's"
    anomic = dict(wab_info_content=9, wab_fluency=8, wab_comprehension=9, wab_repetition=8.5, wab_naming=7)
    assert pdata.suggest_wab_type(anomic) == "Anomic"
    assert pdata.suggest_wab_type(dict(anomic, wab_aq=95)) == "Not aphasic (AQ >= 93.8)"
    assert pdata.suggest_wab_type({"wab_fluency": 2}) is None


def test_check_row_fills_the_aq_and_flags_disagreements():
    row = dict(wab_info_content="5", wab_fluency="2", wab_comprehension="7.5", wab_repetition="4",
               wab_naming="5", wab_type="TranscorticalMotor", sex="female", age_at_stroke="61")
    cleaned, problems, notes = pdata.check_row(row)
    assert not problems and cleaned["wab_aq"] == 47.0 and cleaned["sex"] == "F" and cleaned["age_at_stroke"] == 61
    assert cleaned["wab_type"] == "Transcortical motor"
    assert any("computed" in n for n in notes) and any("differs from the criteria's Broca's" in n for n in notes)
    _, problems, _ = pdata.check_row(dict(wab_aq="140", sex="x", wab_type="Dyslexia"))
    assert len(problems) == 3
    _, _, notes = pdata.check_row(dict(row, wab_aq="60"))
    assert any("differs from the subtests' 47" in n for n in notes)


def test_saving_merges_rows_and_the_report_reads_them(tmp_path):
    (tmp_path / "participants.tsv").write_text("participant_id\tsite_code\nsub-01\tA\n")
    pdata.save_participants(tmp_path, {"sub-01": {"wab_aq": 47.0, "wab_days": 400, "sex": "F"},
                                       "02": {"age_at_stroke": 70}})
    pdata.save_participants(tmp_path, {"sub-01": {"wab_type": "Broca's"}})     # keeps the earlier values
    table = pdata.read_participants(tmp_path)
    assert list(table["participant_id"]) == ["sub-01", "sub-02"] and "site_code" in table
    row = participant_row(tmp_path, "sub-01")
    assert row["wab_aq"] == "47" and row["wab_type"] == "Broca's" and row["site_code"] == "A"
    assert participant_row(tmp_path, "sub-02")["wab_aq"] is None
    assert row_to_predictors(row)["severity_metric"]["value"] == 47.0
    sidecar = json.loads((tmp_path / "participants.json").read_text())
    assert sidecar["wab_days"]["Units"] == "days" and "Broca's" in sidecar["wab_type"]["Levels"]


@pytest.mark.parametrize("suffix", [".csv", ".xlsx"])
def test_spreadsheet_import_matches_columns_and_skips_bad_rows(tmp_path, suffix):
    sheet = pd.DataFrame({"Subject": ["1", "2", "3", "1"], "AQ": ["55.2", "abc", "", "60"],
                          "Gender": ["m", "F", "F", "m"], "Days post onset": ["30", "200", "", "30"],
                          "Clinic notes": ["x", "y", "z", "w"]})
    path = tmp_path / f"cohort{suffix}"
    sheet.to_csv(path, index=False) if suffix == ".csv" else sheet.to_excel(path, index=False)
    dataset = tmp_path / "bids"
    report = pdata.import_spreadsheet(path, dataset, dry_run=True)
    assert not (dataset / "participants.tsv").exists()
    assert list(report["status"]) == ["ok", "skipped", "ok", "skipped"]
    assert "not a number" in report.loc[1, "details"] and "twice" in report.loc[3, "details"]
    pdata.import_spreadsheet(path, dataset, dry_run=False)
    assert participant_row(dataset, "sub-1")["wab_aq"] == "55.2"
    assert participant_row(dataset, "sub-3")["sex"] == "F" and "Clinic notes" not in pdata.read_participants(dataset)


def test_form_saves_one_participant(tmp_path):
    form = pdata.ParticipantForm(tmp_path, ["sub-01"])
    form.pid.value = "01"
    for name, value in dict(wab_info_content="5", wab_fluency="2", wab_comprehension="7.5",
                            wab_repetition="4", wab_naming="5").items():
        form.fields[name].value = value
    assert "Broca&#x27;s" in form.suggestion.value
    form.use_suggestion.click()
    assert form.submit() and form.fields["wab_aq"].value == "47"
    assert participant_row(tmp_path, "sub-01")["wab_type"] == "Broca's"
    form.fields["wab_aq"].value = "200"
    assert not form.submit() and "outside" in form.message.value


# ── images ───────────────────────────────────────────────────────────────────

def test_imported_images_are_found_by_discovery(tmp_path):
    dataset = tmp_path / "bids"
    li.import_images(dataset, "01", "1", {"T1w": nifti(tmp_path / "in" / "t1.nii", gz=False)})
    li.import_images(dataset, "02", None, {"dwi": nifti(tmp_path / "in" / "dwi.nii.gz"),
                                            "adc": nifti(tmp_path / "in" / "adc.nii.gz")})
    t1 = dataset / "sub-01" / "ses-1" / "anat" / "sub-01_ses-1_T1w.nii.gz"
    assert t1.exists() and nib.load(str(t1)).shape == (8, 9, 10)
    assert (dataset / "dataset_description.json").exists()
    assert [e["subject"] for e in discover_t1w(dataset)] == ["sub-01"]
    assert [(e["subject"], e["adc"].name) for e in discover_dwi(dataset)] == [("sub-02", "sub-02_adc.nii.gz")]


def test_import_checks_the_set_before_writing(tmp_path):
    dataset = tmp_path / "bids"
    t1 = nifti(tmp_path / "t1.nii.gz")
    with pytest.raises(ValueError, match="both the DWI"):
        li.import_images(dataset, "01", None, {"T1w": t1, "dwi": nifti(tmp_path / "dwi.nii.gz")})
    with pytest.raises(ValueError, match="3-D image"):
        li.import_images(dataset, "01", None, {"T1w": nifti(tmp_path / "raw4d.nii.gz", (4, 4, 4, 30))})
    assert not dataset.exists()
    li.import_images(dataset, "01", None, {"T1w": t1})
    with pytest.raises(FileExistsError):
        li.import_images(dataset, "01", None, {"T1w": t1})
    li.import_images(dataset, "01", None, {"T1w": t1}, overwrite=True)


def test_series_roles_are_guessed_from_dicom_metadata():
    assert li.guess_role({"SeriesDescription": "t1_mprage_sag_p2_iso", "ImageType": ["ORIGINAL", "PRIMARY"]}) == "T1w"
    assert li.guess_role({"SeriesDescription": "ep2d_diff_3scan_trace", "ImageType": ["DERIVED", "ADC"]}) == "adc"
    assert li.guess_role({"SeriesDescription": "ep2d_diff_3scan_trace", "ImageType": ["DERIVED", "TRACEW"]}) == "dwi"
    assert li.guess_role({"SeriesDescription": "ep2d_diff_mddw", "bvec": True}) is None   # raw 4-D series
    assert li.guess_role({"SeriesDescription": "t2_tirm_tra_dark-fluid FLAIR"}) == "FLAIR"
    assert li.guess_role({"SeriesDescription": "localizer"}) is None


def test_converted_series_are_listed_with_their_published_paths(tmp_path):
    from calmar.dicom_import import series
    out = tmp_path / "images"
    nifti(out / "002_t1_mprage.nii.gz")
    (out / "002_t1_mprage.json").write_text(json.dumps({"SeriesDescription": "t1_mprage", "ImageType": ["ORIGINAL"]}))
    nifti(out / "005_diff.nii.gz", (4, 4, 4, 30))
    records = series(out, tmp_path / "final" / "images")
    assert [(Path(r["nifti"]).parent.name, r["guess"], r["shape"]) for r in records] == [
        ("images", "T1w", [8, 9, 10]), ("images", None, None)]


def test_notebook_cells_show_the_panels_only_for_local_data(tmp_path, monkeypatch, capsys):
    import calmar.local_import, calmar.participant_data
    cells = {c["id"]: "".join(c["source"]) for c in
             json.loads((Path(__file__).resolve().parents[1] / "lesion-interpretation-pipeline.ipynb").read_text())["cells"]}
    shown = []
    monkeypatch.setattr("IPython.display.display", lambda *a, **k: shown.extend(a))
    sheet = tmp_path / "cohort.csv"
    sheet.write_text("Subject,AQ\n7,80\n")
    for source in ("openneuro", "local"):
        ns = dict(CONFIG={"DATASET_SOURCE": source}, RAW_DATASET_DIR=tmp_path / "bids", PROJECT_DIR=tmp_path,
                  SUBJECTS=[{"subject": "sub-01"}], display=lambda *a, **k: shown.extend(a))
        exec(cells["calmar-local-import"], ns)
        exec(cells["calmar-participant-data"].replace("PARTICIPANT_SPREADSHEET = None",
                                                      f"PARTICIPANT_SPREADSHEET = {str(sheet)!r}"), ns)
        if source == "openneuro":
            assert "_local_import" not in ns and "_participant_form" not in ns
    assert isinstance(ns["_local_import"], calmar.local_import.LocalImportPanel)
    assert "sub-01" in ns["_participant_form"].pid.options
    assert "Dry run: 1 participant" in capsys.readouterr().out
