"""QC repair rules and actions with temporary images; Slurm submission is mocked."""
import json
import re
from pathlib import Path
from unittest.mock import patch

import nibabel as nib
import numpy as np
import pytest

from calmar import qc as q
from calmar import qc_repair as r
from calmar.qc_panel import QCDisplay, QCVolumes, brain_extracted_image
from calmar.study import Study

ROOT = Path(__file__).resolve().parents[1]


def save(path, data, affine=np.eye(4)):
    path.parent.mkdir(parents=True, exist_ok=True)
    nib.save(nib.Nifti1Image(np.asarray(data, dtype=np.float32), affine), str(path))
    return path


def lesion_data():
    data = np.zeros((12, 12, 12))
    data[3:8, 3:8, 3:8] = 1
    data[10, 10, 10] = 1  # isolated false-positive voxel
    return data


@pytest.fixture
def setup(tmp_path):
    study = Study({}, tmp_path / "bids", tmp_path)
    entry = dict(subject="sub-1", session="ses-1", t1w=save(tmp_path / "bids" / "sub-1_T1w.nii.gz", np.ones((12, 12, 12))))
    save(study.lesion_native(entry), lesion_data())
    return study, entry


class FakeSlurm:
    """Stands in for calmar.scheduled.in_slurm and records submitted helpers."""

    def __init__(self, results=None):
        self.calls, self.results = [], results or {}

    def __call__(self, function):
        assert getattr(q, function.__name__) is function
        def run(*args, **kwargs):
            self.calls.append((function.__name__, args, kwargs))
            result = self.results.get(function.__name__, 0)
            return result(*args, **kwargs) if callable(result) else result
        return run


def edit(operation, tool="", when="2026-01-01T00:00:00"):
    return {"operation": operation, "tool": tool, "applied_on": when}


def test_edit_classification_and_manual_edit_guard():
    assert r.classify_edit(edit("threshold", "deterministic_ops")) == "manual"
    assert r.classify_edit(edit("external_edit", "external_round_trip")) == "manual"
    assert r.classify_edit(edit("manual_paint", "niivue_draw")) == "manual"
    assert r.classify_edit(edit("rerun_with_mask_bypass")) == "run"
    assert r.classify_edit(edit("restrip_with_hd_bet_and_rerun")) == "run"
    assert r.classify_edit(edit("revert_native_to_linda_original", "deterministic_ops")) == "reset"
    assert r.classify_edit(edit("auto_clear_rerun_flag", "deterministic_ops")) is None
    assert r.classify_edit(edit("warp_native_to_mni", "antsApplyTransforms")) is None
    history = [edit("threshold", "deterministic_ops", "2026-01-01T00:00:01"),
               edit("rerun_with_mask_bypass", "", "2026-01-01T00:00:02")]
    assert not r.manual_edits_since_last_run(history)
    history.append(edit("external_edit", "external_round_trip", "2026-01-01T00:00:03"))
    assert r.manual_edits_since_last_run(history)
    history.append(edit("revert_native_to_linda_original", "deterministic_ops", "2026-01-01T00:00:04"))
    assert not r.manual_edits_since_last_run(history)


def test_edit_history_merges_sidecars_chronologically(tmp_path):
    a, b = q.QCRecord(tmp_path / "a.nii.gz"), q.QCRecord(tmp_path / "b.nii.gz")
    a.edits = [edit("threshold", when="2026-01-02")]
    b.edits = [edit("rerun_with_mask_bypass", when="2026-01-01"), edit("x", when="2026-01-03")]
    assert [e["operation"] for e in r.edit_history(a, b)] == ["rerun_with_mask_bypass", "threshold", "x"]


@pytest.mark.parametrize("marked, rating, tags, only, expected", [
    (False, 3, [], True, True),            # poor skull strip queues by itself
    (True, 1, [], True, False),            # marked for a lesion problem only
    (True, 1, [], False, True),
    (True, 2, ["dura_included"], True, True),
    (False, 2, ["dura_included"], True, False),
])
def test_skull_strip_queue_rule(tmp_path, marked, rating, tags, only, expected):
    record = q.QCRecord(tmp_path / "Lesion_in_MNI.nii.gz", marked_for_rerun=marked)
    record.stages["skull_strip"] = {"rating": rating, "issue_tags": tags, "notes": ""}
    assert r.needs_skull_strip_repair(record, only_skull_strip_issues=only) is expected


def test_skull_strip_queue_lists_excluded(setup):
    study, entry = setup
    record = q.QCRecord.load(study.lesion_mni(entry))
    record.marked_for_rerun = True
    record.save()
    assert r.skull_strip_queue([entry], study) == ([], [entry])
    assert r.skull_strip_queue([entry], study, only_skull_strip_issues=False) == ([entry], [])


def test_cleanup_operations_order_and_effect():
    ops = r.cleanup_operations(threshold=0.4, open_radius=1, close_radius=2, fill_holes=True,
                               keep_largest=1, hemisphere="left")
    assert [o["name"] for o in ops] == ["threshold", "morph_open", "morph_close", "fill_holes",
                                        "largest_cc", "hemisphere_clip"]
    assert [o["name"] for o in r.cleanup_operations()] == ["threshold"]
    before = lesion_data()
    after = r.apply_operations(before.copy(), np.eye(4), r.cleanup_operations(keep_largest=1))
    change = r.mask_change(before, after)
    assert change == {"before": 126, "after": 125, "kept": 125, "removed": 1, "added": 0,
                      "change_pct": pytest.approx(-100 / 126)}


def test_clear_stage_ratings_really_clears(tmp_path):
    anchor = tmp_path / "Lesion_in_MNI.nii.gz"
    record = q.QCRecord.load(anchor)
    record.set_stage("skull_strip", rating=3, issue_tags=["x"])
    record.set_stage("lesion", rating=2, notes="n")
    record.edits = [edit("restrip_with_hd_bet_and_rerun")]
    record.save()
    r.clear_stage_ratings(anchor)
    saved = json.loads(q.sidecar_path_for(anchor).read_text())
    assert all(s["rating"] is None and not s["issue_tags"] for s in saved["stages"].values())
    assert saved["rating"] is None and saved["notes"] == ""
    # Earlier edits are kept and the cleared ratings are logged.
    assert [e["operation"] for e in saved["edits"]] == ["restrip_with_hd_bet_and_rerun", "clear_ratings_after_rerun"]
    assert saved["edits"][1]["params"]["previous"]["lesion"]["rating"] == 2


def test_save_cleanup_backs_up_edits_and_rewarps_in_slurm(setup):
    study, entry = setup
    q.mark_for_rerun(study.lesion_mni(entry))
    slurm = FakeSlurm()
    with patch.object(r, "in_slurm", slurm):
        ok, _ = r.save_cleanup(entry, study, r.cleanup_operations(keep_largest=1), "rev")
    assert ok and slurm.calls == [("warp_native_lesion_to_mni", (study.linda_dir(entry),), {"reviewer": "rev"})]
    native = study.lesion_native(entry)
    assert np.asarray(nib.load(str(native)).dataobj).sum() == 125
    assert (q.linda_original_dir(native) / native.name).exists()
    assert not q.QCRecord.load(study.lesion_mni(entry)).marked_for_rerun
    # Second clean-up starts from LINDA's prediction, not from the first edit.
    assert r.edit_baseline(entry, study) == q.linda_original_dir(native) / native.name
    with patch.object(r, "in_slurm", slurm):
        assert r.revert_to_linda(entry, study, "rev")[0]
    assert np.asarray(nib.load(str(native)).dataobj).sum() == 126


def test_failed_rewarp_is_reported_not_raised(setup):
    study, entry = setup
    def failing(function):
        def run(*a, **k):
            raise RuntimeError("Job 1: FAILED")
        return run
    with patch.object(r, "in_slurm", failing):
        ok, message = r.save_cleanup(entry, study, r.cleanup_operations(), "rev")
    assert not ok and "out of date" in message


def test_edit_baseline_archives_backup_after_linda_rerun(setup):
    study, entry = setup
    native = study.lesion_native(entry)
    backup = save(q.linda_original_dir(native) / native.name, np.zeros((12, 12, 12)))
    record = q.QCRecord.load(study.lesion_mni(entry))
    record.edits = [edit("threshold", "deterministic_ops", "2026-01-01T00:00:01"),
                    edit("rerun_with_mask_bypass", "", "2026-01-01T00:00:02")]
    record.save()
    assert r.edit_baseline(entry, study) == backup
    assert np.asarray(nib.load(str(backup)).dataobj).sum() == 126  # now the newest prediction
    assert len(list((backup.parent / "superseded").glob("*.nii.gz"))) == 1


def test_external_edit_round_trip(setup, tmp_path):
    study, entry = setup
    edits = tmp_path / "qc_edits"
    t1, lesion, kept = r.export_for_editing(entry, study, edits)
    assert t1.exists() and lesion.exists() and kept is None
    save(lesion, lesion_data() * 0)  # the "edit"
    _, _, kept = r.export_for_editing(entry, study, edits)
    assert kept is not None and kept.exists()  # earlier edit is never overwritten
    save(lesion, lesion_data() * 0)
    slurm = FakeSlurm()
    with patch.object(r, "in_slurm", slurm):
        assert r.import_edited_mask(entry, study, edits, "ITK-SNAP", "rev")[0]
    assert np.asarray(nib.load(str(study.lesion_native(entry))).dataobj).sum() == 0
    assert slurm.calls[0][0] == "warp_native_lesion_to_mni"
    save(lesion, np.zeros((5, 5, 5)))
    with patch.object(r, "in_slurm", slurm), pytest.raises(ValueError):
        r.import_edited_mask(entry, study, edits, "ITK-SNAP", "rev")
    assert "itksnap/4.4.0" in r.EDITOR_COMMANDS["ITK-SNAP"]


class FakeSubmit:
    """Stands in for calmar.scheduled.submit_step and records the steps run."""

    def __init__(self, on_brain=None, status="computed"):
        self.calls, self.on_brain, self.status = [], on_brain, status

    def __call__(self, stage, entries, study):
        self.calls.append((stage, entries, dict(study.config)))
        if stage == "brain" and self.on_brain:
            self.on_brain()
        out = Path(study.linda_dir(entries[0])) if stage == "linda" else Path(f"/out/{stage}")
        if stage == "linda" and self.status == "computed" and out.exists():
            # Like processing.product(overwrite=True): the old folder is moved aside.
            out.rename(out.with_name(out.name + ".previous.x"))
            save(out / "Lesion_in_MNI.nii.gz", lesion_data())
        return {"results": [{"outputs": [{"path": str(out), "status": self.status}]}]}


def cube(lo, hi):
    data = np.zeros((12, 12, 12))
    data[lo:hi, lo:hi, lo:hi] = 1
    return data


def test_restrip_submits_to_slurm_and_clears_ratings(setup):
    study, entry = setup
    anchor = study.lesion_mni(entry)
    save(anchor, lesion_data())
    record = q.QCRecord.load(anchor)
    record.set_stage("skull_strip", rating=3, issue_tags=[r.CAVITY_TAG])  # cavity left out: union
    record.save()
    hdbet = study.hdbet_dir(entry)
    repaired = save(hdbet / "sub-1_T1w_desc-accurate_brain_mask.nii.gz", cube(2, 8))
    save(hdbet / "sub-1_T1w_desc-synthstrip_brain_mask.nii.gz", cube(1, 9))
    slurm, submit = FakeSlurm({"run_hd_bet": {"mask": repaired, "returncode": 0}}), FakeSubmit()
    with patch.object(r, "in_slurm", slurm), patch("calmar.scheduled.submit_step", submit):
        result = r.restrip_participant(entry, study, {}, dry_run=True)
        assert result["brain_mask"] == "hdbet+synthstrip"
        assert result["added_synthstrip_voxels"] == cube(1, 9).sum() - cube(2, 8).sum()
        assert submit.calls == []
        assert q.QCRecord.load(anchor).get_stage("skull_strip")["rating"] == 3
        r.restrip_participant(entry, study, {})
    assert [c[0] for c in slurm.calls] == ["run_hd_bet", "run_hd_bet"]
    name, args, kwargs = slurm.calls[0]
    assert kwargs["desc"] == "accurate" and args[1] == hdbet
    # LINDA is recomputed by the pipeline's LINDA step (seeded, MNI152), with overwrite.
    assert [(c[0], c[2]["OVERWRITE"]) for c in submit.calls] == [("linda", True)]
    assert study.config.get("OVERWRITE") is None
    record = q.QCRecord.load(anchor)
    assert record.get_stage("skull_strip")["rating"] is None
    # QC history carried over the overwritten LINDA folder, with the cleared rating logged.
    cleared = [e for e in record.edits if e["operation"] == "clear_ratings_after_rerun"]
    assert cleared and cleared[-1]["params"]["previous"]["skull_strip"]["rating"] == 3
    assert r.skull_strip_queue([entry], study) == ([], [])


def test_linda_repair_refuses_settings_that_skip_it(setup):
    study, entry = setup
    save(study.hdbet_dir(entry) / "sub-1_T1w_brain_mask.nii.gz", cube(2, 8))
    with patch("calmar.scheduled.submit_step", FakeSubmit()), pytest.raises(ValueError):
        r.rerun_linda(entry, study, {"USE_HDBET_PREPROCESSING": False})
    submit = FakeSubmit(status="skipped")
    with patch("calmar.scheduled.submit_step", submit), pytest.raises(RuntimeError, match="not recomputed"):
        r.rerun_linda(entry, study, {"RUN_SEGMENTATION": False})
    assert submit.calls[0][2]["RUN_SEGMENTATION"] is True


def test_restrip_brain_mask_method(setup):
    study, entry = setup
    hdbet = study.hdbet_dir(entry)
    repaired = save(hdbet / "sub-1_T1w_desc-accurate_brain_mask.nii.gz", cube(2, 8))
    synth = hdbet / "sub-1_T1w_desc-synthstrip_brain_mask.nii.gz"
    def extractor(t1, out_dir, *, prefer=None, **kwargs):
        if prefer == "mri_synthstrip":
            return {"mask": save(synth, cube(1, 9)), "returncode": 0}
        return {"mask": save(repaired, cube(2, 8)), "returncode": 0}
    # Default, no cavity tag: HD-BET alone, SynthStrip not run.
    slurm = FakeSlurm({"run_hd_bet": extractor})
    with patch.object(r, "in_slurm", slurm):
        result = r.restrip_participant(entry, study, {}, dry_run=True)
    assert (result["brain_mask"], result["added_synthstrip_voxels"]) == ("hdbet", 0)
    assert [c[2].get("prefer") for c in slurm.calls] == [None] and not synth.exists()
    assert json.loads(q.repaired_mask_sidecar(repaired).read_text())["BrainMask"] == "hdbet"
    # Union chosen for this participant: SynthStrip runs first, as the brain step did not.
    slurm = FakeSlurm({"run_hd_bet": extractor})
    with patch.object(r, "in_slurm", slurm):
        result = r.restrip_participant(entry, study, {}, brain_mask="hdbet+synthstrip", dry_run=True)
    assert [c[2].get("prefer") for c in slurm.calls] == ["mri_synthstrip", None]
    assert result["added_synthstrip_voxels"] == cube(1, 9).sum() - cube(2, 8).sum()
    assert q.check_repaired_mask(repaired, hdbet) == "hdbet+synthstrip"
    synth.unlink()
    with patch.object(r, "in_slurm", FakeSlurm({"run_hd_bet": {"returncode": 1}})), \
            pytest.raises(RuntimeError, match="SynthStrip failed"):
        r.restrip_participant(entry, study, {}, brain_mask="hdbet+synthstrip", dry_run=True)


def test_cavity_tag_selects_the_union(setup):
    study, entry = setup
    assert r.repair_brain_mask_method(entry, study, {}) == "hdbet"
    assert r.repair_brain_mask_method(entry, study, {"BRAIN_MASK": "hdbet+synthstrip"}) == "hdbet+synthstrip"
    record = q.QCRecord.load(study.lesion_mni(entry))
    record.set_stage("skull_strip", rating=2, issue_tags=[r.CAVITY_TAG])
    record.save()
    assert r.repair_brain_mask_method(entry, study, {}) == "hdbet+synthstrip"
    assert r.repair_brain_mask_method(entry, study, {}, "hdbet") == "hdbet"


def test_rerun_runs_brain_step_first_when_no_mask(setup):
    study, entry = setup
    made = study.hdbet_dir(entry) / "sub-1_T1w_brain_mask.nii.gz"
    submit = FakeSubmit(on_brain=lambda: save(made, cube(2, 8)))
    slurm = FakeSlurm()
    with patch.object(r, "in_slurm", slurm), patch("calmar.scheduled.submit_step", submit):
        assert r.rerun_linda(entry, study, {"HDBET_MODE": "fast"}) == made
    assert [(c[0], c[2].get("OVERWRITE")) for c in submit.calls] == [("brain", None), ("linda", True)]
    assert slurm.calls == []


def test_qc_table_reset_and_counts(setup):
    study, entry = setup
    record = q.QCRecord.load(study.lesion_mni(entry))
    record.set_stage("lesion", rating=3, issue_tags=["lesion_missed_partly"])
    record.marked_for_rerun = True
    record.save()
    table = r.qc_table([entry], study)
    assert table.loc[0, "lesion"] == 3 and table.loc[0, "skull_strip"] == "n/a"
    assert table.loc[0, "issue_tags"] == "lesion:lesion_missed_partly"
    assert r.rating_counts(table).loc["lesion", "3 poor"] == 1
    assert r.reset_qc([entry], study, stage="lesion") == [record.path]
    assert q.QCRecord.load(study.lesion_mni(entry)).get_stage("lesion")["rating"] == 3  # dry run
    r.reset_qc([entry], study, dry_run=False)
    saved = q.QCRecord.load(study.lesion_mni(entry))
    assert saved.get_stage("lesion")["rating"] is None and not saved.marked_for_rerun
    assert saved.edits[-1]["operation"] == "reset_qc_ratings"
    r.reset_qc([entry], study, keep_edits=False, dry_run=False)
    assert not record.path.exists()
    with pytest.raises(ValueError):
        r.reset_qc([entry], study, stage="registration")


def test_qc_volumes(setup):
    study, entry = setup
    d = study.linda_dir(entry)
    n4 = save(d / "N4corrected.nii.gz", np.full((12, 12, 12), 2.0))
    save(d / "BrainMask.nii.gz", lesion_data())
    volumes = QCVolumes(study)
    extracted = volumes("skull_strip", entry)
    assert extracted == [{"path": str(d / "_qc_brain_extracted.nii.gz")}]
    assert nib.load(extracted[0]["path"]).get_fdata().sum() == 2 * 126
    assert brain_extracted_image(n4, save(d / "small.nii.gz", np.ones((2, 2, 2))), d / "x.nii.gz") is None
    plain = QCVolumes(study, QCDisplay(skull_strip_show_extracted=False))("skull_strip", entry)
    assert [v["path"] for v in plain] == [str(n4), str(d / "BrainMask.nii.gz")]
    lesion = volumes("lesion", entry)
    assert lesion[0]["path"] == str(n4) and lesion[1]["path"].endswith("_boundary_t1.nii.gz")
    save(d / "Subject_in_MNI.nii.gz", np.ones((12, 12, 12)))
    save(d / "ExpertMask_in_MNI.nii.gz", lesion_data())
    warp = volumes("expert_mni_warp", entry, show_synth=False)
    assert [Path(v["path"]).name for v in warp] == ["Subject_in_MNI.nii.gz", "ExpertMask_in_MNI.nii.gz"]


GUARDED = ("run_hd_bet", "run_linda_with_mask", "run_linda_with_mask_via_R", "hdbet_then_linda",
           "restrip_and_rerun", "rerun_subject", "warp_native_mask_to_mni",
           "warp_native_lesion_to_mni", "coregister_t2_mask_to_t1")


def test_imaging_helpers_only_run_through_slurm():
    sources = [(ROOT / "calmar" / "qc_repair.py").read_text(), (ROOT / "calmar" / "qc_panel.py").read_text()]
    cells = json.loads((ROOT / "lesion-interpretation-pipeline.ipynb").read_text())["cells"]
    ids = {f"calmar-step-{n}" for n in range(49, 61)}
    sources += ["".join(c["source"]) for c in cells if c.get("id") in ids]
    for source in sources:
        for name in GUARDED:
            for match in re.finditer(rf"q\.{name}\b", source):
                assert source[max(0, match.start() - 9):match.start()] == "in_slurm(", name
        assert "importlib.reload" not in source and "antsApplyTransforms(" not in source


def test_qc_history_is_merged_when_new_sidecar_was_saved(tmp_path):
    old_anchor, anchor = tmp_path / "old" / "Lesion_in_MNI.nii.gz", tmp_path / "new" / "Lesion_in_MNI.nii.gz"
    old = q.QCRecord.load(save(old_anchor, lesion_data()))
    old.log_edit(operation="before_repair", tool="t"); old.marked_for_rerun = True; old.save()
    new = q.QCRecord.load(save(anchor, lesion_data()))
    new.log_edit(operation="after_repair", tool="t"); new.save()
    r._carry_qc_history(old_anchor, anchor)
    merged = q.QCRecord.load(anchor)
    assert [e["operation"] for e in merged.edits] == ["before_repair", "after_repair"]
    assert merged.marked_for_rerun
