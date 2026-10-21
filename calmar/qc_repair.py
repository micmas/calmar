"""Repair tools used after QC review.

The QC panel (:mod:`calmar.qc_panel`) records ratings. When a rating shows a
problem, these tools repair the participant's outputs:

1. **Skull-strip repair** (:func:`run_skull_strip_repair`): HD-BET again,
   usually in ``accurate`` mode, then LINDA again with the new brain mask.
2. **Mask clean-up** (:class:`MaskCleanupPanel`): deterministic
   threshold/morphology/connected-component/hemisphere operations on LINDA's
   native-space lesion, then the edited lesion is re-warped to MNI.
3. **External edit** (:class:`ExternalEditPanel`): export the native T1 and
   lesion to ITK-SNAP, FSLeyes or MRIcroGL, edit by hand, import, re-warp.
4. **Re-run queue** (:class:`RerunQueuePanel`): LINDA again with the best
   existing HD-BET mask for participants marked for repair; in the acute (DWI)
   route, OpenADS again (:func:`rerun_openads`). Tiers 1-3 edit LINDA's lesion
   and are T1-route only; for a poor OpenADS lesion, use the manual mask.
5. **Summary and reset** (:func:`qc_table`, :func:`show_qc_summary`,
   :func:`reset_qc`).

Where things are written
------------------------
* Ratings, the repair flag and an ``edits`` audit log live in the QC sidecar
  of ``Study.qc_anchor``: LINDA's MNI lesion ``<linda_dir>/Lesion_in_MNI.qc.json``
  (T1 route) or ``<openads_dir>/OpenADS_in_MNI.qc.json`` (acute route). Edits of the
  native lesion are also logged in ``<linda_dir>/Prediction3_native.qc.json``.
* The first edit copies LINDA's prediction to ``<linda_dir>/_linda_original/``
  (used as the starting point of later clean-ups and by *Revert*). If LINDA
  is re-run afterwards, the next edit archives the older copy under
  ``_linda_original/superseded/`` so edits always start from the newest
  prediction.
* Every imaging tool (HD-BET, LINDA, antsApplyTransforms) runs in Slurm via
  :func:`calmar.scheduled.in_slurm`. The job stages a copy of the output
  folder and publishes it atomically; the folder it replaces is kept as
  ``<folder>.previous.<jobid>``.

Pure decision rules (which participants are queued, which edits count as
manual work, the clean-up operations) are plain functions so they can be
unit-tested and read without the widget code.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime
import filecmp
from html import escape
from pathlib import Path
import shutil

import ipywidgets as w
import nibabel as nib
import numpy as np
import pandas as pd
from IPython.display import HTML, display

from . import colors
from . import qc as q
from .output import Output
from .scheduled import in_slurm

STAGE_COLUMNS = list(q.STAGES)

# ── Decision rules ───────────────────────────────────────────────────────────

# Tools recorded by manual editing actions in sidecar ``edits`` entries.
MANUAL_EDIT_TOOLS = {"deterministic_ops", "external_round_trip", "niivue_draw"}
# Operations that restore LINDA's prediction (no manual work left to lose).
RESET_OPERATIONS = {"revert_native_to_linda_original"}
# Bookkeeping entries that neither edit the mask nor re-run LINDA.
NEUTRAL_OPERATIONS = {"auto_clear_rerun_flag", "warp_native_to_mni", "reset_qc_ratings"}


def classify_edit(edit):
    """Classify one sidecar ``edits`` entry as ``"run"``, ``"manual"``, ``"reset"`` or None.

    ``run``: LINDA produced a fresh prediction (re-run, re-strip).
    ``manual``: a person changed the lesion (clean-up ops, external editor, paint).
    ``reset``: the lesion was reverted to LINDA's prediction.
    """
    operation = (edit.get("operation") or "").lower()
    tool = (edit.get("tool") or "").lower()
    if operation in RESET_OPERATIONS:
        return "reset"
    if operation in NEUTRAL_OPERATIONS:
        return None
    if "rerun" in operation or "restrip" in operation or operation.startswith("linda"):
        return "run"
    if tool in MANUAL_EDIT_TOOLS or operation in q.OP_REGISTRY or operation in (
            "external_edit", "manual_paint"):
        return "manual"
    return None


def edit_history(*records):
    """Merge the ``edits`` of several QC records in chronological order."""
    edits = [edit for record in records for edit in (record.edits or [])]
    return sorted(edits, key=lambda edit: edit.get("applied_on") or "")


def manual_edits_since_last_run(edits):
    """True when a manual edit follows the latest LINDA run or revert.

    Re-running LINDA then would overwrite that manual work.
    """
    pending = False
    for edit in edits:
        kind = classify_edit(edit)
        if kind in ("run", "reset"):
            pending = False
        elif kind == "manual":
            pending = True
    return pending


def needs_skull_strip_repair(record, *, only_skull_strip_issues=True):
    """Should this participant be in the skull-strip repair queue?

    Queued when the skull-strip stage is rated 3 (poor), or when the reviewer
    marked the participant for repair. With ``only_skull_strip_issues`` a
    marked participant is queued only if the skull-strip stage is rated 3 or
    has an issue tag, because the repair flag is participant-level and may
    have been set for a lesion-mask problem that re-stripping cannot fix.
    """
    stage = record.stages.get("skull_strip") or {}
    poor = stage.get("rating") == 3
    if not (record.marked_for_rerun or poor):
        return False
    return poor or bool(stage.get("issue_tags")) or not only_skull_strip_issues


def skull_strip_queue(entries, study, *, only_skull_strip_issues=True):
    """Return ``(queued, excluded)`` entries for skull-strip repair.

    ``excluded`` lists participants marked for repair whose skull strip has no
    recorded problem (only with ``only_skull_strip_issues``).
    """
    queued, excluded = [], []
    for entry in entries:
        if not Path(entry["t1w"]).exists():
            continue
        record = q.QCRecord.load(study.lesion_mni(entry))
        if needs_skull_strip_repair(record, only_skull_strip_issues=only_skull_strip_issues):
            queued.append(entry)
        elif record.marked_for_rerun:
            excluded.append(entry)
    return queued, excluded


def cleanup_operations(*, threshold=0.5, open_radius=0, close_radius=0,
                       fill_holes=False, keep_largest=0, hemisphere="none"):
    """Build the ordered list of deterministic clean-up operations.

    Order: threshold → morphological opening → closing → fill holes →
    keep N largest connected components → clip to one hemisphere. Zero /
    False / "none" leaves an operation out. Names match ``calmar.qc.OP_REGISTRY``.
    """
    ops = [{"name": "threshold", "params": {"threshold": float(threshold)}}]
    if open_radius:
        ops.append({"name": "morph_open", "params": {"radius": int(open_radius)}})
    if close_radius:
        ops.append({"name": "morph_close", "params": {"radius": int(close_radius)}})
    if fill_holes:
        ops.append({"name": "fill_holes", "params": {}})
    if keep_largest:
        ops.append({"name": "largest_cc", "params": {"n_components": int(keep_largest)}})
    if hemisphere not in (None, "none"):
        ops.append({"name": "hemisphere_clip", "params": {"hemisphere": hemisphere}})
    return ops


def apply_operations(data, affine, ops):
    """Apply operations exactly as ``calmar.qc.apply_ops_and_save`` does."""
    for op in ops:
        params = dict(op.get("params") or {})
        function = q.OP_REGISTRY[op["name"]]
        data = (function(data, affine=affine, **params) if op["name"] == "hemisphere_clip"
                else function(data, **params))
    return data


def mask_change(before, after):
    """Voxel counts kept, removed and added between two masks (nonzero = lesion)."""
    before, after = np.asarray(before) > 0, np.asarray(after) > 0
    n_before, n_after = int(before.sum()), int(after.sum())
    return {"before": n_before, "after": n_after,
            "kept": int((before & after).sum()),
            "removed": int((before & ~after).sum()),
            "added": int((~before & after).sum()),
            "change_pct": (n_after - n_before) / max(n_before, 1) * 100}


def clear_stage_ratings(anchor):
    """Clear every stage rating, tag and note in a QC sidecar (edit log kept).

    Used after LINDA is re-run: the old ratings describe images that no
    longer exist. (``QCRecord.set_stage(rating=None)`` keeps the old rating,
    so the stages are replaced directly.)
    """
    record = q.QCRecord.load(anchor)
    previous = {stage: value for stage, value in record.stages.items()
                if value.get("rating") is not None or value.get("issue_tags") or value.get("notes")}
    if previous:
        record.log_edit(operation="clear_ratings_after_rerun", params={"previous": previous},
                        reviewer=None, tool="qc_repair")
    for stage in q.STAGES:
        record.stages[stage] = {"rating": None, "issue_tags": [], "notes": ""}
    record.rating, record.issue_tags, record.notes = None, [], ""
    record.reviewer = record.reviewed_on = None
    record.save()
    return record


def clear_repair_flag(anchor, *, reason, reviewer, tool):
    """Remove the participant from the repair queues after a successful fix."""
    record = q.QCRecord.load(anchor)
    if record.marked_for_rerun:
        record.marked_for_rerun = False
        record.log_edit(operation="auto_clear_rerun_flag", params={"reason": reason},
                        reviewer=reviewer, tool=tool)
        record.save()


def entry_label(entry):
    return f"{entry['subject']} {entry.get('session') or ''}".strip()


# ── Native-lesion edits (shared by clean-up and external edits) ─────────────

def _history(entry, study):
    return edit_history(q.QCRecord.load(study.lesion_native(entry)),
                        q.QCRecord.load(study.lesion_mni(entry)))


def edit_baseline(entry, study):
    """Return LINDA's newest unedited native prediction, refreshing the backup.

    The backup in ``_linda_original/`` is written once, at the first edit.
    When LINDA was re-run later and the lesion has not been edited since, the
    current file *is* the new prediction: the old backup is archived under
    ``_linda_original/superseded/`` and replaced, so clean-ups and *Revert*
    never fall back to a prediction from an earlier run.
    """
    native = study.lesion_native(entry)
    backup = q.linda_original_dir(native) / native.name
    if not backup.exists():
        return native
    if manual_edits_since_last_run(_history(entry, study)):
        return backup
    if native.exists() and not filecmp.cmp(backup, native, shallow=False):
        archive = backup.parent / "superseded"
        archive.mkdir(exist_ok=True)
        shutil.move(str(backup), archive / f"{datetime.now():%Y%m%dT%H%M%S}_{native.name}")
        shutil.copy2(native, backup)
    return backup


def resync_mni(entry, study, reviewer):
    """Re-warp the edited native lesion to ``Lesion_in_MNI.nii.gz`` in Slurm.

    Returns ``(ok, message)``; a failure leaves the edited native lesion in
    place (it is the source of truth) and explains why MNI was not updated.
    """
    try:
        in_slurm(q.warp_native_lesion_to_mni)(study.linda_dir(entry), reviewer=reviewer or None)
        return True, "Lesion_in_MNI.nii.gz re-warped from the edited native lesion."
    except Exception as error:
        return False, f"MNI re-warp failed, so Lesion_in_MNI.nii.gz is out of date: {error}"


def save_cleanup(entry, study, ops, reviewer):
    """Apply clean-up ``ops`` to LINDA's native lesion, re-warp to MNI, clear the repair flag."""
    native = study.lesion_native(entry)
    source = edit_baseline(entry, study)
    q.apply_ops_and_save(native, ops, reviewer=reviewer, tool="deterministic_ops",
                         source_path=source)
    result = resync_mni(entry, study, reviewer)
    clear_repair_flag(study.lesion_mni(entry), reason="manual_edit_via_tier1_ops",
                      reviewer=reviewer, tool="deterministic_ops")
    return result


def revert_to_linda(entry, study, reviewer):
    """Restore LINDA's prediction from ``_linda_original/`` and re-warp to MNI.

    Returns ``(ok, message)``.
    """
    native = study.lesion_native(entry)
    backup = edit_baseline(entry, study)
    if backup == native:
        return False, "No backup found; this lesion has not been edited."
    shutil.copy2(backup, native)
    record = q.QCRecord.load(study.lesion_mni(entry))
    record.log_edit(operation="revert_native_to_linda_original", reviewer=reviewer,
                    tool="deterministic_ops")
    record.save()
    return resync_mni(entry, study, reviewer)


# External editors: pinned Neurodesk modules and the command that opens the
# native T1 with the lesion as an editable overlay/segmentation.
EDITOR_COMMANDS = {
    "ITK-SNAP": "module load itksnap/4.4.0\nitksnap -g {t1} -s {lesion}",
    "FSLeyes": "module load fsl/6.0.7.22\nfsleyes {t1} {lesion} -cm red -a 60",
    "MRIcroGL": "module load mricrogl/1.2.20220720\nMRIcroGL {t1} {lesion}",
}


def edit_folder(edits_dir, entry):
    return Path(edits_dir) / f"{entry['subject']}_{entry.get('session') or 'no-ses'}"


def export_for_editing(entry, study, edits_dir):
    """Copy the native T1 and LINDA lesion into ``<edits_dir>/<sub>_<ses>/``.

    An earlier edited copy that differs from the current lesion is kept as
    ``<name>.replaced-<time>.nii.gz`` instead of being overwritten.
    Returns ``(t1_copy, lesion_copy, kept_copy_or_None)``.
    """
    t1, lesion = Path(entry["t1w"]), study.lesion_native(entry)
    missing = [str(p) for p in (t1, lesion) if not p.exists()]
    if missing:
        raise FileNotFoundError("Missing: " + ", ".join(missing))
    folder = edit_folder(edits_dir, entry)
    folder.mkdir(parents=True, exist_ok=True)
    t1_copy, lesion_copy = folder / t1.name, folder / lesion.name
    kept = None
    if lesion_copy.exists() and not filecmp.cmp(lesion_copy, lesion, shallow=False):
        kept = folder / lesion.name.replace(
            ".nii.gz", f".replaced-{datetime.now():%Y%m%dT%H%M%S}.nii.gz")
        shutil.move(str(lesion_copy), kept)
    shutil.copy2(t1, t1_copy)
    shutil.copy2(lesion, lesion_copy)
    return t1_copy, lesion_copy, kept


def import_edited_mask(entry, study, edits_dir, editor, reviewer):
    """Copy the edited lesion back, re-warp to MNI, clear the repair flag.

    Raises ``FileNotFoundError`` when no edited file exists and ``ValueError``
    when its grid differs from the original. Returns ``(ok, message)`` of the
    MNI re-warp.
    """
    native = study.lesion_native(entry)
    edited = edit_folder(edits_dir, entry) / native.name
    if not edited.exists():
        raise FileNotFoundError(f"{edited} not found. Save the edit there first.")
    edit_baseline(entry, study)
    q.import_external_edit(edited, native, reviewer=reviewer, editor=editor)
    result = resync_mni(entry, study, reviewer)
    clear_repair_flag(study.lesion_mni(entry), reason="manual_edit_via_tier3_external",
                      reviewer=reviewer, tool=editor)
    return result


# ── Slurm repairs ────────────────────────────────────────────────────────────

def _rerun_linda_step(entry, study, config):
    """Recompute LINDA for one participant with the pipeline's own LINDA step
    (processing.step_linda: fixed REGISTRATION_SEED, one thread, ch2 -> MNI152
    outputs and a cache record), replacing the current output. The previous
    LINDA folder is kept as ``<linda_dir>.previous.<id>``."""
    import copy
    from .scheduled import submit_step
    if not config.get("USE_HDBET_PREPROCESSING", True):
        raise ValueError("LINDA repairs pass the brain mask to LINDA, but "
                         "CONFIG['USE_HDBET_PREPROCESSING'] is False.")
    linda_dir = Path(study.linda_dir(entry))
    moved_before = set(linda_dir.parent.glob(linda_dir.name + ".previous.*"))
    rerun = copy.copy(study)
    rerun.config = {**config, "OVERWRITE": True, "RUN_SEGMENTATION": True}
    step = submit_step("linda", [entry], rerun)
    outputs = [o for row in step.get("results", []) for o in row.get("outputs", []) if isinstance(o, dict)]
    if not any(o.get("status") == "computed" and Path(o["path"]).resolve() == linda_dir.resolve()
               for o in outputs):
        raise RuntimeError(f"LINDA was not recomputed for {entry_label(entry)}: {outputs}")
    moved = sorted(set(linda_dir.parent.glob(linda_dir.name + ".previous.*")) - moved_before)
    if moved:
        _carry_qc_history(moved[-1] / study.lesion_mni(entry).name, study.lesion_mni(entry))
    return [f"{Path(o['path']).name} ({o.get('status')})" for o in outputs]


def _carry_qc_history(old_anchor, anchor):
    """The QC sidecar (ratings, edit log) lives in the LINDA folder, which the
    overwrite moved aside: bring it to the new output, merging the edit logs if a
    sidecar was already saved there."""
    import json
    old, new = q.sidecar_path_for(old_anchor), q.sidecar_path_for(anchor)
    if not old.exists():
        return
    if not new.exists():
        shutil.copy2(old, new)
        return
    before, after = json.loads(old.read_text()), json.loads(new.read_text())
    after["edits"] = before.get("edits", []) + [e for e in after.get("edits", []) if e not in before.get("edits", [])]
    after["marked_for_rerun"] = bool(before.get("marked_for_rerun") or after.get("marked_for_rerun"))
    new.write_text(json.dumps(after, indent=2))


CAVITY_TAG = "lesion_excluded_by_strip"


def repair_brain_mask_method(entry, study, config, brain_mask="auto"):
    """BRAIN_MASK method for one participant's skull-strip repair.

    ``"auto"``: the union with SynthStrip when the reviewer tagged the skull strip
    ``lesion_excluded_by_strip`` (a CSF-filled cavity outside the mask, so LINDA
    cannot label it), otherwise ``CONFIG["BRAIN_MASK"]``. On 8 sessions of
    ds004884 the union raised LINDA's Dice only where >= 40 ml of the expert
    lesion lay outside HD-BET (sub-M2045 0.73 -> 0.77, sub-M2029 0.61 -> 0.70);
    elsewhere the extra CSF it adds became false positives.
    """
    if brain_mask != "auto":
        return brain_mask
    tags = (q.QCRecord.load(study.lesion_mni(entry)).stages.get("skull_strip") or {}).get("issue_tags") or []
    return "hdbet+synthstrip" if CAVITY_TAG in tags else config.get("BRAIN_MASK", "hdbet")


def restrip_participant(entry, study, config, *, hdbet_mode="accurate", device=None,
                        tta=False, brain_mask="auto", dry_run=False, reviewer=None):
    """Run HD-BET again and (unless ``dry_run``) LINDA with the new brain mask, in Slurm.

    HD-BET writes ``<hdbet_dir>/<T1>_desc-<mode>_brain[_mask].nii.gz``; the mask is
    then finished with ``brain_mask`` (see :func:`repair_brain_mask_method`):
    ``"hdbet+synthstrip"`` adds the SynthStrip mask, running SynthStrip first if
    the brain step did not. The method is recorded beside the mask. Unless
    ``dry_run``, LINDA is recomputed by the pipeline's LINDA step, which prefers
    this repaired mask. After success every stage rating is cleared, because the
    rated images were replaced, and the repair flag is removed.
    ``result["mask_warning"]`` is set when the new mask is more than 15% smaller
    than the one it replaces.
    """
    t1, hdbet_dir = entry["t1w"], study.hdbet_dir(entry)
    method = repair_brain_mask_method(entry, study, config, brain_mask)
    old_mask = q.find_best_hdbet_mask(hdbet_dir)
    old_voxels = int(np.count_nonzero(np.asarray(nib.load(str(old_mask)).dataobj))) if old_mask else None
    if method == "hdbet+synthstrip" and not any(Path(hdbet_dir).glob("*_desc-synthstrip_brain_mask.nii.gz")):
        strip = in_slurm(q.run_hd_bet)(t1, hdbet_dir, prefer="mri_synthstrip", desc="synthstrip")
        if strip.get("returncode") != 0 or not strip.get("mask"):
            raise RuntimeError(f"SynthStrip failed (exit {strip.get('returncode')}); inspect the job log.")
    result = in_slurm(q.run_hd_bet)(t1, hdbet_dir, device=device,
                                    mode=hdbet_mode, tta=tta, desc=hdbet_mode)
    if result.get("returncode") != 0 or not result.get("mask"):
        raise RuntimeError(f"HD-BET failed (exit {result.get('returncode')}); inspect the job log.")
    result["brain_mask"] = method
    result["added_synthstrip_voxels"] = q.add_synthstrip_mask(result["mask"], hdbet_dir, t1, method)
    new_voxels = int(np.count_nonzero(np.asarray(nib.load(str(result["mask"])).dataobj)))
    if old_voxels and new_voxels < 0.85 * old_voxels:
        result["mask_warning"] = (f"new brain mask is {100 * (1 - new_voxels / old_voxels):.0f}% smaller "
                                  f"than {Path(old_mask).name}; check it before rating")
    if dry_run:
        return result
    result["linda_outputs"] = _rerun_linda_step(entry, study, config)
    clear_stage_ratings(study.lesion_mni(entry))
    clear_repair_flag(study.lesion_mni(entry), reason="skull_strip_repaired",
                      reviewer=reviewer, tool="restrip_participant")
    return result


def rerun_linda(entry, study, config, reviewer=None):
    """Recompute LINDA in Slurm with the participant's current brain mask.

    Runs the pipeline's LINDA step (seeded, one thread, MNI152 outputs) with
    overwrite; if there is no brain mask yet, the brain step runs first. The
    previous LINDA folder is kept as ``<linda_dir>.previous.<id>``. On success the
    stale stage ratings and the repair flag are cleared. Returns the brain mask used.
    """
    from .scheduled import submit_step
    if q.find_best_hdbet_mask(study.hdbet_dir(entry)) is None:
        print(f"No brain mask for {entry_label(entry)}; running the brain step first.")
        submit_step("brain", [entry], study)
    mask = q.find_best_hdbet_mask(study.hdbet_dir(entry))
    _rerun_linda_step(entry, study, config)
    clear_stage_ratings(study.lesion_mni(entry))
    clear_repair_flag(study.lesion_mni(entry), reason="linda_rerun",
                      reviewer=reviewer, tool="rerun_linda")
    return mask


def rerun_openads(entry, study, config, reviewer=None):
    """Acute (DWI) route: recompute OpenADS in Slurm for one participant.

    The previous OpenADS folder is kept as ``<openads_dir>.previous.<id>``; its QC
    sidecar (edit log, repair flag) is carried over, the stale stage ratings are
    cleared and the repair flag removed. The manual mask's template-space copy
    lived in that folder too, so the manual step runs again when one is configured.
    Returns the names and statuses of the new outputs.
    """
    import copy
    from .scheduled import submit_step
    folder, anchor = Path(study.dirs(entry)["openads"]), Path(study.qc_anchor(entry))
    moved_before = set(folder.parent.glob(folder.name + ".previous.*"))
    rerun = copy.copy(study)
    rerun.config = {**config, "OVERWRITE": True, "RUN_SEGMENTATION": True}
    step = submit_step("openads", [entry], rerun)
    outputs = [o for row in step.get("results", []) for o in row.get("outputs", []) if isinstance(o, dict)]
    if not any(o.get("status") == "computed" and Path(o["path"]).resolve() == folder.resolve() for o in outputs):
        raise RuntimeError(f"OpenADS was not recomputed for {entry_label(entry)}: {outputs}")
    moved = sorted(set(folder.parent.glob(folder.name + ".previous.*")) - moved_before)
    if moved:
        _carry_qc_history(moved[-1] / anchor.name, anchor)
    if study.manual_mask_template(entry):
        submit_step("manual", [entry], study)
    clear_stage_ratings(anchor)
    clear_repair_flag(anchor, reason="openads_rerun", reviewer=reviewer, tool="rerun_openads")
    return [f"{Path(o['path']).name} ({o.get('status')})" for o in outputs]


# ── Notebook front ends ──────────────────────────────────────────────────────

REPAIR_MODES = ("single", "step_marked", "batch_marked")
MAX_REPAIR_VIEWERS = 12  # browsers keep ~16 WebGL contexts alive


def run_skull_strip_repair(entries, study, config, *, mode="step_marked", subject_index=0,
                           dry_run=False, hdbet_mode="accurate", device=None, tta=False,
                           brain_mask="auto",
                           only_skull_strip_issues=True,
                           reviewer=None, viewers=None):
    """Notebook front end for :func:`restrip_participant`.

    ``mode``: ``"step_marked"`` repairs the first queued participant (rerun to
    continue), ``"batch_marked"`` all queued participants, ``"single"``
    ``entries[subject_index]`` whether queued or not. ``brain_mask``: see
    :func:`repair_brain_mask_method`. ``viewers`` (the
    ``calmar.widgets`` module) shows each new brain mask over the T1.
    Returns the list of ``(entry, result_or_exception)``.
    """
    if mode not in REPAIR_MODES:
        raise ValueError(f"mode must be one of {REPAIR_MODES}, not {mode!r}")
    print(f"Mode: {mode} · HD-BET {hdbet_mode} · brain mask {brain_mask} · "
          + ("HD-BET only (dry run)" if dry_run else "HD-BET + LINDA re-run"))
    if mode == "single":
        if not 0 <= subject_index < len(entries):
            print(f"subject_index={subject_index} is out of range (0..{len(entries) - 1}).")
            return []
        todo = [entries[subject_index]]
    else:
        todo, excluded = skull_strip_queue(entries, study,
                                           only_skull_strip_issues=only_skull_strip_issues)
        if excluded:
            print(f"Not queued (marked for repair, but the skull strip has no rating 3 or "
                  f"issue tag): {', '.join(entry_label(e) for e in excluded)}")
        if not todo:
            print("No skull-strip repairs are queued. In the QC panel, rate a skull strip 3 "
                  "(or tag a skull-strip issue and mark the participant for repair), save, "
                  "then click Run skull-strip repair.")
            return []
        print(f"Queue: {', '.join(entry_label(e) for e in todo)}")
        if mode == "step_marked":
            todo = todo[:1]
    outcomes = []
    for i, entry in enumerate(todo):
        print(f"\n→ {entry_label(entry)}  (T1w: {entry['t1w']})")
        try:
            result = restrip_participant(entry, study, config, hdbet_mode=hdbet_mode,
                                         device=device, tta=tta, brain_mask=brain_mask, dry_run=dry_run,
                                         reviewer=reviewer)
        except Exception as error:
            print(f"  ✗ Repair failed: {error}")
            outcomes.append((entry, error))
            continue
        outcomes.append((entry, result))
        _report_restrip(result, dry_run)
        if viewers is not None and i < MAX_REPAIR_VIEWERS and Path(result["mask"]).exists():
            display(HTML("<small>T1 with the new brain mask</small>"),
                    viewers.show(f"hdbet_rerun_{i}", [
                        {"path": str(entry["t1w"])},
                        {"path": str(result["mask"]), "colormap": colors.color("hdbet"),
                         "opacity": 0.30, "cal_min": 0.5, "cal_max": 1.0}]))
    if mode == "step_marked" and not dry_run:
        remaining, _ = skull_strip_queue(entries, study,
                                         only_skull_strip_issues=only_skull_strip_issues)
        print(f"\n{len(remaining)} participant(s) still queued."
              + (" Rerun this cell for the next one." if remaining else ""))
    if not dry_run and any(not isinstance(r, Exception) for _, r in outcomes):
        print("Ratings for repaired participants were cleared; rerun the QC panel to rate the new images.")
    return outcomes


def _report_restrip(result, dry_run):
    print(f"  ✓ New brain mask ({result.get('brain_mask', 'hdbet')}): {result['mask']}")
    if result.get("added_synthstrip_voxels"):
        print(f"  Added the SynthStrip mask (lesion cavities): +{result['added_synthstrip_voxels']} voxels")
    if result.get("mask_warning"):
        print(f"  ⚠ {result['mask_warning']}")
    if dry_run:
        print("  Dry run: LINDA, ratings and the repair queue were not changed.")
        return
    print(f"  LINDA recomputed: {', '.join(result.get('linda_outputs') or []) or 'no outputs reported'}")


def _lesion_pool(entries, study):
    from . import masks as cm
    return [e for e in entries if cm.present(study.lesion_native(e))]


def _participant_dropdown(pool):
    return w.Dropdown(options=[(entry_label(e), i) for i, e in enumerate(pool)],
                      description="Participant:", style={"description_width": "initial"},
                      layout=w.Layout(width="340px"))


def _show(panel, background, layers):
    """Load the layers with the same overlay controls as the step viewers."""
    from types import SimpleNamespace
    from .step_viewer import show_layers
    show_layers(panel.viewer, panel.controls, background, layers,
                SimpleNamespace(set_volumes=lambda nv, specs: nv.load_volumes(panel.encode(specs))))


def _controls(viewer):
    from .layer_controls import LayerControls
    from .step_viewer import viewer_layout
    if hasattr(viewer, "opts"):
        viewer_layout(viewer)
    return LayerControls(plane=3)


def _preview_color():
    linda = colors.color("linda")
    return next(c for c in ("blue", "cyan", "green") if c != linda)


class MaskCleanupPanel(w.VBox):
    """Deterministic clean-up of LINDA's native lesion with a live preview.

    The preview starts from LINDA's unedited prediction (see
    :func:`edit_baseline`), so settings are not applied on top of earlier
    clean-ups. *Apply & save* calls :func:`save_cleanup`; *Revert* calls
    :func:`revert_to_linda`. Both re-warp to MNI in Slurm (the kernel waits).
    """

    def __init__(self, entries, study, viewer, *, encode_volumes, reviewer="",
                 preview_path=None):
        self.pool, self.study, self.viewer, self.encode = _lesion_pool(entries, study), study, viewer, encode_volumes
        self.controls = _controls(viewer)
        self.preview_path = Path(preview_path or Path(study.project) / "qc_edits" / "_cleanup_preview.nii.gz")
        self.subject = _participant_dropdown(self.pool)
        style = {"description_width": "initial"}
        self.threshold = w.FloatSlider(value=0.5, min=0.1, max=0.95, step=0.05, description="Threshold:",
                                       continuous_update=False, style=style)
        self.open_radius = w.IntSlider(value=0, min=0, max=3, description="Opening radius:",
                                       continuous_update=False, style=style)
        self.close_radius = w.IntSlider(value=0, min=0, max=3, description="Closing radius:",
                                        continuous_update=False, style=style)
        self.fill = w.Checkbox(value=False, description="Fill holes")
        self.keep = w.IntSlider(value=0, min=0, max=5, description="Keep N largest (0 = all):",
                                continuous_update=False, style=style)
        self.hemisphere = w.Dropdown(options=["none", "left", "right"], value="none",
                                     description="Hemisphere clip:", style=style)
        self.reviewer = w.Text(value=reviewer, description="Reviewer:", style=style)
        self.apply_button = w.Button(description="Apply & save", button_style="primary")
        self.revert_button = w.Button(description="Revert to LINDA original", button_style="warning")
        self.stats, self.message, self.job_output = w.HTML(), w.HTML(), Output()
        preview = _preview_color()
        legend = w.HTML(f"<small>LINDA prediction <b style='color:{colors.css('linda')}'>{colors.color('linda')}</b> · "
                        f"after clean-up <b style='color:{colors.CSS[preview]}'>{preview}</b> "
                        "(LINDA-only voxels are removed; clean-up-only voxels are added)</small>")
        if not self.pool:
            super().__init__([w.HTML("<em>No LINDA native lesion masks to clean up.</em>")])
            return
        super().__init__([w.HBox([self.subject, self.reviewer]),
                          w.HBox([self.threshold, self.open_radius, self.close_radius]),
                          w.HBox([self.fill, self.keep, self.hemisphere]),
                          w.HBox([self.apply_button, self.revert_button]),
                          self.stats, self.message, self.job_output, legend, self.controls, viewer])
        for control in (self.subject, self.threshold, self.open_radius, self.close_radius,
                        self.fill, self.keep, self.hemisphere):
            control.observe(self.preview, names="value")
        self.apply_button.on_click(lambda _: self.apply())
        self.revert_button.on_click(lambda _: self.revert())
        self.preview()

    @property
    def entry(self):
        return self.pool[self.subject.value]

    def operations(self):
        return cleanup_operations(threshold=self.threshold.value, open_radius=self.open_radius.value,
                                  close_radius=self.close_radius.value, fill_holes=self.fill.value,
                                  keep_largest=self.keep.value, hemisphere=self.hemisphere.value)

    def preview(self, *_):
        native = self.study.lesion_native(self.entry)
        backup = q.linda_original_dir(native) / native.name
        source = backup if backup.exists() and manual_edits_since_last_run(
            _history(self.entry, self.study)) else native
        image = nib.load(str(source))
        before = image.get_fdata()
        after = apply_operations(before.copy(), image.affine, self.operations())
        change = mask_change(before, after)
        self.preview_path.parent.mkdir(parents=True, exist_ok=True)
        nib.save(nib.Nifti1Image(after.astype(np.uint8), image.affine, image.header), str(self.preview_path))
        self.stats.value = (
            f"<small>LINDA {change['before']:,} voxels → after clean-up {change['after']:,} "
            f"({change['change_pct']:+.1f}%): kept {change['kept']:,}, "
            f"<b>removed {change['removed']:,}</b>, <b>added {change['added']:,}</b>. "
            f"{len(self.operations())} operation(s); nothing is saved until Apply &amp; save.</small>")
        from .step_viewer import _layer
        preview = _preview_color()
        try:
            _show(self, self.entry["t1w"], [
                _layer("LINDA prediction", "linda", source, "lesion", opacity=0.35),
                _layer("After clean-up", "cleanup", self.preview_path, "lesion", opacity=0.35,
                       colormap=preview, css=colors.CSS[preview])])
        except Exception as error:
            self.message.value = f"Viewer unavailable: {escape(str(error))}"

    def _run(self, action, done):
        self.message.value = "Working; the MNI re-warp runs as a Slurm job…"
        with self.job_output:
            self.job_output.clear_output()
            try:
                ok, note = action()
            except Exception as error:
                ok, note = False, str(error)
        self.message.value = (f"<b>{'✓' if ok else '⚠'} {escape(done)}</b> "
                              f"<small>{escape(note)}</small>")
        self.preview()

    def apply(self):
        reviewer = self.reviewer.value.strip()
        self._run(lambda: save_cleanup(self.entry, self.study, self.operations(), reviewer),
                  f"Saved {self.study.lesion_native(self.entry).name} (LINDA prediction kept in _linda_original/).")

    def revert(self):
        reviewer = self.reviewer.value.strip()
        self._run(lambda: revert_to_linda(self.entry, self.study, reviewer),
                  f"Reverted {self.study.lesion_native(self.entry).name}.")


class ExternalEditPanel(w.VBox):
    """Round trip of LINDA's native lesion through an external editor.

    *Export* copies the native T1 and lesion to ``<edits_dir>/<sub>_<ses>/``
    and shows the terminal command; *Import* runs :func:`import_edited_mask`.
    """

    def __init__(self, entries, study, viewer, *, edits_dir, encode_volumes, reviewer="",
                 editor="ITK-SNAP"):
        self.pool, self.study, self.viewer, self.encode = _lesion_pool(entries, study), study, viewer, encode_volumes
        self.controls = _controls(viewer)
        self.edits_dir = Path(edits_dir)
        self.subject = _participant_dropdown(self.pool)
        self.editor = w.Dropdown(options=list(EDITOR_COMMANDS), value=editor, description="Editor:")
        self.reviewer = w.Text(value=reviewer, description="Reviewer:", style={"description_width": "initial"})
        self.export_button = w.Button(description="Export for editing", button_style="info", icon="upload")
        self.import_button = w.Button(description="Import edited mask", button_style="primary", icon="download")
        self.caption, self.instructions, self.job_output = w.HTML(), w.HTML(), Output()
        if not self.pool:
            super().__init__([w.HTML("<em>No LINDA native lesion masks to edit.</em>")])
            return
        super().__init__([w.HBox([self.subject, self.editor, self.reviewer]), self.caption, self.controls, viewer,
                          w.HBox([self.export_button, self.import_button]), self.instructions, self.job_output])
        self.subject.observe(self.preview, names="value")
        self.export_button.on_click(lambda _: self.export())
        self.import_button.on_click(lambda _: self.import_edit())
        self.preview()

    @property
    def entry(self):
        return self.pool[self.subject.value]

    def preview(self, *_):
        lesion = self.study.lesion_native(self.entry)
        self.caption.value = (f"<b>{escape(entry_label(self.entry))}</b> <small>native T1 + current "
                              f"LINDA lesion ({colors.color('linda')})</small>")
        try:
            from .step_viewer import _layer
            _show(self, self.entry["t1w"], [_layer("LINDA lesion", "linda", lesion, "lesion", opacity=0.45)])
        except Exception as error:
            self.caption.value += f"<br><small>Viewer unavailable: {escape(str(error))}</small>"

    def export(self):
        try:
            t1, lesion, kept = export_for_editing(self.entry, self.study, self.edits_dir)
        except FileNotFoundError as error:
            self.instructions.value = f"<b>✗ {escape(str(error))}</b>"
            return False
        command = EDITOR_COMMANDS[self.editor.value].format(t1=t1, lesion=lesion)
        note = (f"<p>Your earlier edit was kept as <code>{escape(kept.name)}</code>.</p>" if kept else "")
        self.instructions.value = (
            f"<div style='border:1px solid #2196F3;border-radius:6px;padding:12px'>"
            f"<b>Exported to <code>{escape(str(t1.parent))}</code></b>{note}"
            "<ol><li>Open the Neurodesktop (the full desktop, not JupyterLab) and start a Terminal.</li>"
            f"<li>Run:<pre>{escape(command)}</pre></li>"
            f"<li>Correct the lesion in {escape(self.editor.value)} and save it over "
            f"<code>{escape(lesion.name)}</code> in the same folder (ITK-SNAP: Segmentation → Save).</li>"
            "<li>Click <b>Import edited mask</b>.</li></ol></div>")
        return True

    def import_edit(self):
        self.instructions.value = "Importing; the MNI re-warp runs as a Slurm job…"
        with self.job_output:
            self.job_output.clear_output()
            try:
                ok, note = import_edited_mask(self.entry, self.study, self.edits_dir,
                                              self.editor.value, self.reviewer.value.strip())
            except (FileNotFoundError, ValueError) as error:
                self.instructions.value = f"<b>✗ {escape(str(error))}</b>"
                return False
        self.instructions.value = (
            f"<b>✓ Imported into <code>{escape(str(self.study.lesion_native(self.entry)))}</code></b>. "
            f"LINDA's prediction is kept in <code>_linda_original/</code>.<br>"
            f"<small>{'✓' if ok else '⚠'} {escape(note)} Rerun the QC panel to rate the corrected mask.</small>")
        self.preview()
        return ok


class RerunQueuePanel(w.VBox):
    """Participants marked for repair, each with a *Re-run LINDA* button
    (*Re-run OpenADS* in the acute (DWI) route).

    Re-running is blocked for participants whose lesion was edited by hand
    since the last LINDA run (it would overwrite that work) unless
    ``allow_overwriting_edits`` is True.
    """

    def __init__(self, entries, study, config, *, allow_overwriting_edits=False, reviewer=None):
        from .study import modality
        self.study, self.config, self.reviewer = study, config, reviewer
        self.acute = modality(config) == "dwi"
        tool = "OpenADS" if self.acute else "LINDA"
        self.job_output = Output()
        rows = []
        for entry in entries:
            record = q.QCRecord.load(study.qc_anchor(entry))
            if not record.marked_for_rerun:
                continue
            edited = not self.acute and manual_edits_since_last_run(_history(entry, study))
            blocked = edited and not allow_overwriting_edits
            ratings = ", ".join(f"{s}={record.stages[s].get('rating')}" for s in q.STAGES
                                if (record.stages.get(s) or {}).get("rating"))
            text = (f"<b>{escape(entry_label(entry))}</b> · {escape(ratings or 'no ratings')}"
                    + (" · <span style='color:#a00'>edited by hand since the last LINDA run — "
                       "re-run blocked</span>" if blocked else ""))
            button = w.Button(description=f"Re-run {tool}", button_style="primary", disabled=blocked)
            button.on_click(lambda _, e=entry: self.rerun(e))
            rows.append(w.HBox([button, w.HTML(text)]))
        header = (f"<b>{len(rows)} participant(s) marked for repair.</b>" if rows
                  else "<em>No participants are marked for repair.</em>")
        super().__init__([w.HTML(header), *rows, self.job_output])

    def rerun(self, entry):
        with self.job_output:
            self.job_output.clear_output()
            try:
                if self.acute:
                    outputs = rerun_openads(entry, self.study, self.config, reviewer=self.reviewer)
                    print(f"✓ OpenADS re-run for {entry_label(entry)}: {', '.join(outputs)}. "
                          "Ratings were cleared; rerun the QC panel to rate the new outputs.")
                    return
                mask = rerun_linda(entry, self.study, self.config, reviewer=self.reviewer)
                print(f"✓ LINDA re-run for {entry_label(entry)} with brain mask {mask}. "
                      "Ratings were cleared; rerun the QC panel to rate the new outputs.")
            except Exception as error:
                print(f"✗ Re-run failed for {entry_label(entry)}: {error}")


# ── Summary and reset ────────────────────────────────────────────────────────

def qc_table(entries, study):
    """One row per participant: rating per stage, tags, repair flag, edit count."""
    rows = []
    for entry in entries:
        anchor = study.qc_anchor(entry)
        record = q.QCRecord.load(anchor)
        stages = set(study.qc_stages(entry))
        row = {"subject": entry["subject"], "session": entry.get("session") or ""}
        for stage in STAGE_COLUMNS:
            rating = (record.stages.get(stage) or {}).get("rating")
            row[stage] = rating if stage in stages else "n/a"
        row["issue_tags"] = "; ".join(f"{stage}:{tag}" for stage in STAGE_COLUMNS
                                      for tag in (record.stages.get(stage) or {}).get("issue_tags") or [])
        row["marked_for_repair"] = bool(record.marked_for_rerun)
        edits = edit_history(record, q.QCRecord.load(study.lesion_native(entry)))
        row["n_edits"] = len(edits)
        row["last_edit"] = edits[-1].get("operation") if edits else ""
        row["reviewer"] = record.reviewer or ""
        row["reviewed_on"] = record.reviewed_on or ""
        row["sidecar"] = str(record.path)
        rows.append(row)
    return pd.DataFrame(rows, columns=["subject", "session", *STAGE_COLUMNS, "issue_tags",
                                       "marked_for_repair", "n_edits", "last_edit",
                                       "reviewer", "reviewed_on", "sidecar"])


def rating_counts(table):
    """Counts of 1/2/3/unrated per stage (stages not available are left out)."""
    counts = {}
    for stage in STAGE_COLUMNS:
        values = [v for v in table[stage] if v != "n/a"] if stage in table else []
        counts[stage] = {f"{rating} {q.RATING_VOCAB[rating]}": sum(1 for v in values if v == rating)
                         for rating in (1, 2, 3)}
        counts[stage]["unrated"] = sum(1 for v in values if v not in (1, 2, 3))
    return pd.DataFrame(counts).T


def show_qc_summary(entries, study, out_path):
    """Write ``qc_summary.csv`` and plot ratings per stage and issue-tag counts."""
    import matplotlib.pyplot as plt
    table = qc_table(entries, study)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out_path, index=False)
    print(f"QC summary for {len(table)} participant(s) written to {out_path}")
    if table.empty:
        return table
    counts = rating_counts(table)
    counts = counts[counts.sum(axis=1) > 0]
    tags = Counter(tag.split(":", 1)[1] for value in table["issue_tags"] for tag in value.split("; ") if tag)
    fig, axes = plt.subplots(1, 2, figsize=(13, 4))
    counts.rename(index=q.STAGE_LABELS).plot.barh(
        stacked=True, ax=axes[0], color=["#3aaf3a", "#e6a23c", "#d9534f", "#c8c8c8"])
    axes[0].set_xlabel("participants")
    axes[0].set_title(f"Ratings per stage · {int(table['marked_for_repair'].sum())} marked for repair")
    if tags:
        names, values = zip(*tags.most_common()[::-1])
        axes[1].barh(names, values, color="#5078a0")
        axes[1].set_title("Issue tags (all stages)")
    else:
        axes[1].text(0.5, 0.5, "no issue tags", ha="center", va="center")
        axes[1].set_axis_off()
    plt.tight_layout()
    plt.show()
    display(table.drop(columns=["sidecar"]))
    return table


def reset_qc(entries, study, *, subject=None, session=None, stage=None,
             keep_edits=True, dry_run=True):
    """Clear saved QC ratings for the selected participants.

    ``subject``/``session`` None means all; ``stage`` None means every stage
    plus the reviewer and repair flag. ``keep_edits=False`` (with
    ``stage=None``) deletes the sidecar file, edit history included.
    ``dry_run`` only lists what would change. Returns the affected sidecars.
    """
    if stage is not None and stage not in q.STAGES:
        raise ValueError(f"Unknown stage {stage!r}; choose one of {q.STAGES}")
    affected = []
    for entry in entries:
        if subject and entry["subject"] != subject:
            continue
        if session and (entry.get("session") or "") != session:
            continue
        record = q.QCRecord.load(study.qc_anchor(entry))
        if not record.path.exists():
            continue
        affected.append(record.path)
        if dry_run:
            continue
        if stage is None and not keep_edits:
            record.path.unlink()
            continue
        for name in ([stage] if stage else q.STAGES):
            record.stages[name] = {"rating": None, "issue_tags": [], "notes": ""}
        if stage in (None, "lesion"):
            record.rating, record.issue_tags, record.notes = None, [], ""
        if stage is None:
            record.reviewer = record.reviewed_on = None
            record.marked_for_rerun = False
        record.log_edit(operation="reset_qc_ratings", params={"stage": stage}, tool="reset_qc")
        record.save()
    return affected
