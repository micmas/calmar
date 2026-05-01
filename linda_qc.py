"""
linda_qc.py — QC, manual-fix, and re-run helpers for the LINDA notebook.

Design principles
-----------------
* Every QC rating and every edit operation is recorded in a per-mask
  sidecar JSON (the audit trail). The sidecar lives next to the mask:
  `<mask>.qc.json`.
* When a mask is edited, the original LINDA output is moved to
  `<linda_dir>/_linda_original/Lesion_in_MNI.nii.gz` *exactly once* (the
  first edit). Subsequent edits operate on the canonical
  `Lesion_in_MNI.nii.gz`.
* Every operation is one line in the sidecar's `edits` list with its
  parameters and timestamp — so the full edit history is reproducible.

Contents
--------
* `ISSUE_TAGS`           — controlled vocabulary of issue tags.
* `QCRecord`             — load/save a sidecar JSON.
* Deterministic ops:     `op_threshold`, `op_morph_open`, `op_morph_close`,
                         `op_fill_holes`, `op_largest_cc`,
                         `op_hemisphere_clip`.
* `apply_ops_and_save`   — run a list of ops on a mask and update the sidecar.
* `summarize_qc`         — aggregate sidecars into a DataFrame.
* `mark_for_rerun`       — flag a subject for re-run.
* `list_rerun_queue`     — return subjects currently marked.
* `rerun_subject`        — invoke linda_predict.sh with optional manual seed.

This module deliberately does NOT depend on ipywidgets / ipyniivue — those
are notebook-only concerns. The notebook cells call these helpers and
handle the UI.
"""

from __future__ import annotations

import datetime as dt
import json
import shutil
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import nibabel as nib
import numpy as np
import pandas as pd


# ============================================================
# Controlled vocab — ratings and issue tags
# ------------------------------------------------------------
# Definitions live here so the notebook UI and QC_RUBRIC.md stay in sync.
# ============================================================

RATING_VOCAB = {1: "good", 2: "acceptable", 3: "poor"}

RATING_DEFINITIONS = {
    1: (
        "Mask faithfully represents the lesion. Borders match within "
        "~2-3 voxels of what you would draw by hand. No clusters of "
        "false positives. Native and MNI versions both look correct. "
        "Usable for analysis as-is."
    ),
    2: (
        "Minor issues only. Some boundary inaccuracy or 1-2 small "
        "false-positive clusters that can be cleaned with deterministic "
        "post-processing (threshold, morphology, hemisphere clip). "
        "The core lesion is correctly identified. Usable after Tier-1 "
        "fixes in the cells below."
    ),
    3: (
        "Substantial issues. Examples: a sub-region of the true lesion "
        "is missed entirely, large false-positive clusters in healthy "
        "tissue, lesion in the wrong hemisphere, or a pipeline-stage "
        "failure (registration off, skull-strip bled). Needs manual "
        "painting (Tier 2 / Tier 3) or a re-run with a manual seed."
    ),
}

# Each value is (category, short_definition, tiebreaker_rule).
# `category` groups tags in the rubric and the QC widget; `tiebreaker`
# is the rule for choosing between adjacent tags that feel close.
ISSUE_TAG_DEFINITIONS = {
    # --- Coverage errors (component-level: missed or extra REGIONS) ---
    "lesion_missed_partly": (
        "Coverage",
        "A sub-region of the true lesion is entirely outside the mask "
        "(not just shrunk borders).",
        "If the missed area would need painting in or a regional re-run, "
        "use this; if just lowering the threshold or a morphological "
        "close would catch it, use boundary_too_tight.",
    ),
    "false_positive_cluster": (
        "Coverage",
        "One or more separate clusters of 'lesion' appear in tissue "
        "that is not lesioned.",
        "If extra voxels are *adjacent* to the true lesion, that's "
        "boundary_too_loose, not this.",
    ),
    # --- Boundary errors (edge refinement: same component, wrong edge) ---
    "boundary_too_tight": (
        "Boundary",
        "True lesion identified, but borders shrink in by a few voxels "
        "everywhere - fixable by a lower threshold or a morphological "
        "close.",
        "Use lesion_missed_partly if a whole sub-region is gone.",
    ),
    "boundary_too_loose": (
        "Boundary",
        "True lesion identified, but borders extend a few voxels past "
        "the true edge - fixable by a higher threshold or a "
        "morphological open.",
        "Use false_positive_cluster if the extra voxels are a separate, "
        "non-adjacent blob.",
    ),
    # --- Tissue-class confusions (where false positives land) ---
    "csf_included": (
        "Tissue confusion",
        "Ventricles, sulci, or other CSF spaces are flagged as lesion "
        "(a common LINDA failure in chronic stroke where the cyst has "
        "CSF intensity).",
        "Implies false_positive_cluster or boundary_too_loose; pick "
        "this when the false positives are *specifically* in CSF.",
    ),
    "extracranial_included": (
        "Tissue confusion",
        "Skull, scalp, or air outside the brain is flagged as lesion.",
        "Often co-occurs with skull_strip_failed (the precondition).",
    ),
    # --- Topology issues ---
    "lesion_fragmented": (
        "Topology",
        "True lesion is one connected region, but the mask shows it as "
        "multiple disconnected blobs.",
        "Fixable by morphological close or 'keep N largest components'.",
    ),
    "multiple_lesions_one_missed": (
        "Topology",
        "Patient has multiple distinct lesions; the mask captured some "
        "but not all.",
        "Use lesion_missed_partly only if the missed lesion would "
        "anatomically continue a single captured lesion.",
    ),
    # --- Lateralization ---
    "wrong_hemisphere": (
        "Lateralization",
        "Mask voxels appear in the contralesional (non-affected) "
        "hemisphere.",
        "If only a few voxels, fix with a hemisphere_clip op; if a "
        "large mirror-image lesion, suspect registration_off.",
    ),
    # --- Pipeline-stage failures (not the lesion mask itself) ---
    "skull_strip_failed": (
        "Pipeline",
        "The brain mask is poor - either excludes brain tissue or "
        "includes scalp. Affects everything downstream.",
        "If the skull-strip looks fine in the QC view but extra-cranial "
        "voxels still got into the lesion, use extracranial_included.",
    ),
    "registration_off": (
        "Pipeline",
        "MNI alignment is poor - the lesion is in the right place in "
        "native space but in the wrong place in MNI.",
        "Compare 'Lesion (native)' vs 'Lesion (MNI)' views; if only the "
        "MNI version looks wrong, this is the right tag.",
    ),
    # --- Catch-all ---
    "other": (
        "Other",
        "Something else - please describe in Notes.",
        "Use only when no other tag fits.",
    ),
}

# Backwards-compat: ISSUE_TAGS as a flat list of tag names, in
# rubric-display order.
ISSUE_TAGS = list(ISSUE_TAG_DEFINITIONS.keys())

QC_SCHEMA_VERSION = 2          # bumped: per-stage ratings + HD-BET hooks


# ============================================================
# Per-stage QC vocabularies
# ------------------------------------------------------------
# LINDA's pipeline: skull strip → MNI registration → lesion prediction.
# Visual QC of the registration stage is genuinely hard without
# specialized tools (MNI template overlays with edge highlighting,
# checkerboards, NMI metrics) and the most consequential registration
# failures (lesion warped into wrong tissue) typically show up as a
# lesion-stage observation anyway. So the workflow is two stages:
# skull strip + lesion. Re-add "registration" here if you want it back.
# ============================================================
STAGES = ("skull_strip", "lesion")

STAGE_LABELS = {
    "skull_strip":  "Skull strip / brain extraction",
    "lesion":       "Lesion mask",
}

STAGE_RATING_DEFINITIONS = {
    "skull_strip": {
        1: ("Brain mask cleanly excludes skull and scalp and includes "
            "all of cortex, cerebellum, and brainstem. Usable as-is."),
        2: ("Minor issues: small bits of dura/scalp included, or thin "
            "slivers of cortex excluded — fixable by morphology or a "
            "single round of HD-BET. Lesion QC can usually proceed."),
        3: ("Major issues: large extracranial regions included, brain "
            "tissue excluded, or cerebellum/brainstem dropped. **Re-strip "
            "with HD-BET and re-run LINDA before evaluating downstream "
            "stages — they are not trustworthy until this is fixed.**"),
    },
    "lesion": RATING_DEFINITIONS,
}

SKULL_STRIP_TAG_DEFINITIONS = {
    "brain_under_stripped": (
        "Coverage",
        "Skull, scalp, dura, or eyes are still inside the brain mask.",
        "If only thin meningeal tissue is included, that's typically a "
        "rating-2; large dural inclusions are rating-3.",
    ),
    "brain_over_stripped": (
        "Coverage",
        "Brain tissue (cortex, white matter) is outside the brain mask.",
        "Inspect cortical-surface gyri carefully — superficial cortex "
        "is the most commonly mis-excluded region.",
    ),
    "cerebellum_dropped": (
        "Coverage",
        "Cerebellum (or part of it) is excluded from the brain mask.",
        "Common with template-based stripping; HD-BET / SynthStrip "
        "usually fix this.",
    ),
    "brainstem_dropped": (
        "Coverage",
        "Brainstem is excluded from the brain mask.",
        "Often co-occurs with cerebellum_dropped.",
    ),
    "lesion_excluded_by_strip": (
        "Lesion-specific",
        "The lesion area itself is outside the brain mask — typically "
        "because the cyst has CSF intensity and the stripper treated "
        "it as extracranial space.",
        "This is the most consequential failure mode for chronic stroke "
        "data: the lesion gets excluded before LINDA ever sees it. "
        "Re-strip with HD-BET (which is lesion-aware) is the right move.",
    ),
    "asymmetric_strip": (
        "Coverage",
        "One hemisphere is more aggressively stripped than the other.",
        "Often a sign that the registration template doesn't fit — try "
        "re-stripping with a deep-learning method.",
    ),
    "other": (
        "Other",
        "Something else — describe in Notes.",
        "Use only when no other tag fits.",
    ),
}

# Public dict: stage → (tag_dict, rating_dict)
STAGE_VOCAB = {
    "skull_strip":  (SKULL_STRIP_TAG_DEFINITIONS,  STAGE_RATING_DEFINITIONS["skull_strip"]),
    "lesion":       (ISSUE_TAG_DEFINITIONS,        STAGE_RATING_DEFINITIONS["lesion"]),
}


# ============================================================
# Sidecar JSON I/O
# ============================================================
def sidecar_path_for(mask_path: Path) -> Path:
    """`Lesion_in_MNI.nii.gz` -> `Lesion_in_MNI.qc.json` (sibling)."""
    p = Path(mask_path)
    # Drop ".nii.gz" or ".nii"
    name = p.name
    if name.endswith(".nii.gz"):
        stem = name[:-len(".nii.gz")]
    else:
        stem = p.stem
    return p.with_name(f"{stem}.qc.json")


def linda_original_dir(mask_path: Path) -> Path:
    return Path(mask_path).parent / "_linda_original"


def _empty_stage_dict():
    return {s: {"rating": None, "issue_tags": [], "notes": ""}
            for s in STAGES}


@dataclass
class QCRecord:
    """One sidecar JSON. Auto-creates a default if the file doesn't exist.

    v2 schema has a `stages` dict (skull_strip / registration / lesion),
    each carrying its own rating + issue_tags + notes. The legacy
    top-level `rating` / `issue_tags` / `notes` fields are kept as a
    convenience mirror of the *lesion* stage so existing callers keep
    working.
    """
    mask_path: Path
    schema_version: int = QC_SCHEMA_VERSION
    subject: str | None = None
    session: str | None = None
    # Legacy / convenience: mirror the lesion stage
    rating: int | None = None
    issue_tags: list[str] = field(default_factory=list)
    notes: str = ""
    # New in v2
    stages: dict = field(default_factory=_empty_stage_dict)
    # Common
    reviewer: str | None = None
    reviewed_on: str | None = None
    marked_for_rerun: bool = False
    edits: list[dict] = field(default_factory=list)

    @property
    def path(self) -> Path:
        return sidecar_path_for(self.mask_path)

    # --------------------------------------------------------
    # Stage helpers
    # --------------------------------------------------------
    def get_stage(self, stage: str) -> dict:
        if stage not in STAGES:
            raise ValueError(f"Unknown stage {stage!r}; allowed: {STAGES}")
        if stage not in self.stages:
            self.stages[stage] = {"rating": None, "issue_tags": [], "notes": ""}
        return self.stages[stage]

    def set_stage(self, stage: str, *, rating: int | None = None,
                  issue_tags: list[str] | None = None,
                  notes: str | None = None):
        s = self.get_stage(stage)
        if rating is not None:     s["rating"] = rating
        if issue_tags is not None: s["issue_tags"] = list(issue_tags)
        if notes is not None:      s["notes"] = notes
        # Mirror the lesion stage into the top-level convenience fields
        if stage == "lesion":
            self.rating     = s["rating"]
            self.issue_tags = list(s["issue_tags"])
            self.notes      = s["notes"]

    # --------------------------------------------------------
    # I/O
    # --------------------------------------------------------
    @classmethod
    def load(cls, mask_path: Path) -> "QCRecord":
        sp = sidecar_path_for(mask_path)
        if not sp.exists():
            return cls(mask_path=Path(mask_path))
        data = json.loads(sp.read_text())
        # Backwards-compat: if v1 sidecar, lift fields into stages.lesion
        if data.get("schema_version", 1) < 2 or "stages" not in data:
            stages = _empty_stage_dict()
            stages["lesion"]["rating"]     = data.get("rating")
            stages["lesion"]["issue_tags"] = data.get("issue_tags") or []
            stages["lesion"]["notes"]      = data.get("notes") or ""
            data["stages"]         = stages
            data["schema_version"] = QC_SCHEMA_VERSION
        accepted = {"schema_version", "subject", "session", "rating",
                    "issue_tags", "notes", "stages", "reviewer",
                    "reviewed_on", "marked_for_rerun", "edits"}
        return cls(mask_path=Path(mask_path),
                   **{k: v for k, v in data.items() if k in accepted})

    def save(self):
        # Make sure top-level mirror reflects the lesion stage if present
        lesion = self.stages.get("lesion") if self.stages else None
        if lesion:
            self.rating     = lesion.get("rating", self.rating)
            self.issue_tags = list(lesion.get("issue_tags") or self.issue_tags)
            self.notes      = lesion.get("notes") or self.notes
        out = {
            "schema_version":   self.schema_version,
            "subject":          self.subject,
            "session":          self.session,
            "mask":             str(self.mask_path.name),
            # Per-stage block (the new source of truth)
            "stages":           self.stages,
            # Convenience mirror of the lesion stage
            "rating":           self.rating,
            "rating_label":     RATING_VOCAB.get(self.rating) if self.rating else None,
            "issue_tags":       self.issue_tags,
            "notes":            self.notes,
            "reviewer":         self.reviewer,
            "reviewed_on":      self.reviewed_on,
            "marked_for_rerun": self.marked_for_rerun,
            "edits":            self.edits,
        }
        self.path.write_text(json.dumps(out, indent=2) + "\n")
        return self.path

    def log_edit(self, operation: str, params: dict | None = None,
                 reviewer: str | None = None, tool: str = "deterministic_ops",
                 extra: dict | None = None):
        entry = {
            "operation":  operation,
            "params":     params or {},
            "tool":       tool,
            "applied_by": reviewer or self.reviewer,
            "applied_on": dt.datetime.now().isoformat(timespec="seconds"),
        }
        if extra:
            entry.update(extra)
        self.edits.append(entry)


# ============================================================
# Deterministic operations
# ============================================================
def _binarize(data: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    return (data > threshold).astype(np.uint8)


def op_threshold(data: np.ndarray, threshold: float = 0.5, **_) -> np.ndarray:
    """Re-binarize a probability map at `threshold`."""
    return _binarize(data, threshold)


def op_morph_open(data: np.ndarray, radius: int = 1, **_) -> np.ndarray:
    from scipy.ndimage import binary_opening, generate_binary_structure
    s = generate_binary_structure(3, 1)
    return binary_opening(data > 0, structure=s, iterations=radius).astype(np.uint8)


def op_morph_close(data: np.ndarray, radius: int = 1, **_) -> np.ndarray:
    from scipy.ndimage import binary_closing, generate_binary_structure
    s = generate_binary_structure(3, 1)
    return binary_closing(data > 0, structure=s, iterations=radius).astype(np.uint8)


def op_fill_holes(data: np.ndarray, **_) -> np.ndarray:
    from scipy.ndimage import binary_fill_holes
    return binary_fill_holes(data > 0).astype(np.uint8)


def op_largest_cc(data: np.ndarray, n_components: int = 1, **_) -> np.ndarray:
    """Keep the N largest connected components."""
    from scipy.ndimage import label
    bin_ = (data > 0).astype(np.uint8)
    labeled, n = label(bin_)
    if n == 0:
        return bin_
    sizes = np.bincount(labeled.ravel())
    sizes[0] = 0  # background
    keep = np.argsort(sizes)[::-1][:n_components]
    out = np.isin(labeled, keep).astype(np.uint8)
    return out


def op_hemisphere_clip(data: np.ndarray, affine: np.ndarray,
                       hemisphere: str = "left", margin_mm: float = 0.0,
                       **_) -> np.ndarray:
    """
    Zero out voxels outside the requested hemisphere (in MNI space).
    `hemisphere` is the hemisphere to *keep* (`left` keeps x < 0).
    """
    bin_ = (data > 0).astype(np.uint8)
    ii, jj, kk = np.indices(data.shape)
    coords = np.stack([ii, jj, kk, np.ones_like(ii)], axis=-1).reshape(-1, 4)
    mni = (affine @ coords.T).T[:, :3].reshape(data.shape + (3,))
    x = mni[..., 0]
    if hemisphere == "left":
        keep = x < (0 + margin_mm)
    elif hemisphere == "right":
        keep = x > (0 - margin_mm)
    else:
        return bin_
    return (bin_ & keep.astype(np.uint8)).astype(np.uint8)


OP_REGISTRY = {
    "threshold":        op_threshold,
    "morph_open":       op_morph_open,
    "morph_close":      op_morph_close,
    "fill_holes":       op_fill_holes,
    "largest_cc":       op_largest_cc,
    "hemisphere_clip":  op_hemisphere_clip,
}


# ============================================================
# Apply ops and save (with backup)
# ============================================================
def _backup_original_once(mask_path: Path) -> Path | None:
    """Move LINDA's original to _linda_original/ if not already done."""
    backup_dir = linda_original_dir(mask_path)
    backup = backup_dir / mask_path.name
    if backup.exists():
        return backup
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(mask_path, backup)
    return backup


def apply_ops_and_save(mask_path: Path, ops: list[dict],
                       reviewer: str, tool: str = "deterministic_ops",
                       *, source_path: Path | None = None) -> Path:
    """
    Apply a list of operations to `mask_path` and save the result.

    `ops` is a list of {"name": "<op_name>", "params": {...}}.

    Returns the path to the (overwritten) mask. The original is preserved
    in `_linda_original/<mask_name>` (created on first edit).
    """
    if not ops:
        return mask_path
    src = Path(source_path or mask_path)
    img = nib.load(str(src))
    data = img.get_fdata()
    affine = img.affine

    for op in ops:
        name = op["name"]
        params = dict(op.get("params") or {})
        fn = OP_REGISTRY.get(name)
        if fn is None:
            raise ValueError(f"Unknown op {name!r}")
        if name == "hemisphere_clip":
            data = fn(data, affine=affine, **params)
        else:
            data = fn(data, **params)

    _backup_original_once(mask_path)
    out_img = nib.Nifti1Image(data.astype(np.uint8), affine, img.header)
    nib.save(out_img, str(mask_path))

    rec = QCRecord.load(mask_path)
    for op in ops:
        rec.log_edit(operation=op["name"], params=op.get("params"),
                     reviewer=reviewer, tool=tool)
    rec.save()
    return mask_path


def import_external_edit(edited_path: Path, target_mask_path: Path,
                         reviewer: str, editor: str = "external") -> Path:
    """Import an externally-edited mask back into the canonical location."""
    edited_img = nib.load(str(edited_path))
    target_img = nib.load(str(target_mask_path))
    if edited_img.shape != target_img.shape:
        raise ValueError(
            f"Shape mismatch: edited {edited_img.shape} != "
            f"target {target_img.shape}; refusing to import."
        )
    if not np.allclose(edited_img.affine, target_img.affine, atol=1e-3):
        raise ValueError("Affine mismatch: edited mask is not in the same "
                         "space as the target; refusing to import.")
    _backup_original_once(target_mask_path)
    nib.save(edited_img, str(target_mask_path))

    rec = QCRecord.load(target_mask_path)
    rec.log_edit(operation="external_edit", params={"editor": editor},
                 reviewer=reviewer, tool="external_round_trip",
                 extra={"source_path": str(edited_path)})
    rec.save()
    return target_mask_path


def log_paint_edit(mask_path: Path, before_data: np.ndarray,
                   after_data: np.ndarray, reviewer: str):
    """Compute voxels added/removed by a paint session and log them."""
    added = int(np.sum((after_data > 0) & (before_data == 0)))
    removed = int(np.sum((after_data == 0) & (before_data > 0)))
    rec = QCRecord.load(mask_path)
    rec.log_edit(operation="manual_paint",
                 params={"voxels_added": added, "voxels_removed": removed},
                 reviewer=reviewer, tool="niivue_draw")
    rec.save()


# ============================================================
# QC summary
# ============================================================
def summarize_qc(deriv_dir: Path) -> pd.DataFrame:
    """Walk `deriv_dir` for *.qc.json sidecars and return a DataFrame."""
    rows = []
    for sp in Path(deriv_dir).rglob("*.qc.json"):
        try:
            d = json.loads(sp.read_text())
        except Exception:
            continue
        rows.append({
            "subject":          d.get("subject"),
            "session":          d.get("session"),
            "rating":           d.get("rating"),
            "rating_label":     d.get("rating_label"),
            "issue_tags":       ";".join(d.get("issue_tags") or []),
            "notes":            d.get("notes") or "",
            "reviewer":         d.get("reviewer"),
            "reviewed_on":      d.get("reviewed_on"),
            "marked_for_rerun": d.get("marked_for_rerun"),
            "n_edits":          len(d.get("edits") or []),
            "last_edit_op":     ((d.get("edits") or [{}])[-1].get("operation")
                                 if d.get("edits") else None),
            "sidecar_path":     str(sp),
        })
    return pd.DataFrame(rows)


def write_qc_summary_csv(deriv_dir: Path, out_path: Path | None = None) -> Path:
    """Build the summary and write it to `qc_summary.csv` (or `out_path`)."""
    df = summarize_qc(deriv_dir)
    out = Path(out_path or (Path(deriv_dir) / "qc_summary.csv"))
    df.to_csv(out, index=False)
    return out


# ============================================================
# Lesion boundary (cached) — for low-opacity QC visualization
# ============================================================
def lesion_boundary_path(lesion_path: Path, thickness: int = 1) -> Path:
    """Path where the boundary version of a lesion mask is cached.
    `thickness` is included in the filename so different thicknesses
    don't overwrite each other."""
    p = Path(lesion_path)
    name = p.name
    if name.endswith(".nii.gz"):
        stem = name[:-len(".nii.gz")]
        suffix = ".nii.gz"
    else:
        stem = p.stem
        suffix = p.suffix
    return p.with_name(f"{stem}_boundary_t{thickness}{suffix}")


def ensure_lesion_boundary(lesion_path: Path, thickness: int = 1) -> Path:
    """
    Compute (and cache) the binary boundary of a lesion mask.

    `thickness` controls how many voxels wide the boundary ring is:
        1 = thin (default; one-voxel rim)
        2 = medium
        3 = thick

    The boundary is `mask & ~erode(mask, iterations=thickness)`.
    Cached file lives next to the mask (one cache per thickness),
    regenerated only when older than the source.
    """
    from scipy.ndimage import binary_erosion

    if thickness < 1:
        raise ValueError(f"thickness must be >= 1, got {thickness}")
    src = Path(lesion_path)
    out = lesion_boundary_path(src, thickness=thickness)
    if out.exists() and out.stat().st_mtime >= src.stat().st_mtime:
        return out
    img = nib.load(str(src))
    data = img.get_fdata() > 0
    eroded = binary_erosion(data, iterations=thickness)
    boundary = (data & ~eroded).astype(np.uint8)
    nib.save(nib.Nifti1Image(boundary, img.affine, img.header), str(out))
    return out


# ============================================================
# Reset / clear QC
# ============================================================
def reset_qc_sidecars(deriv_dir: Path,
                      *, subject: str | None = None,
                      session: str | None = None,
                      stage: str | None = None,
                      keep_edits: bool = True,
                      dry_run: bool = True) -> list[Path]:
    """
    Clear stored QC. Returns the list of sidecar files that were
    affected. With `dry_run=True` (default) nothing is written.

    Three flavors:

      1. **Stage-level reset** (stage given) — sets only that stage's
         rating + tags + notes back to empty. Other stages are kept.

      2. **Sidecar-level reset** (no stage given) — clears ALL stages
         in the matching sidecars. With `keep_edits=True` (default) the
         per-edit history (deterministic ops, paint, HD-BET, etc.)
         is preserved as audit trail.

      3. **Sidecar-level full delete** (`keep_edits=False`) — deletes
         the .qc.json file outright. Use this when you really want a
         clean slate for these subjects.

    Filter scope:
      - subject=None, session=None: every sidecar under deriv_dir
      - subject="sub-XXX": only that subject's sidecars
      - subject + session: only that one (subject, session) pair

    Examples:
      # Preview clearing every QC under derivatives:
      reset_qc_sidecars(DERIV_DIR)
      # Actually clear, but preserve edit history:
      reset_qc_sidecars(DERIV_DIR, dry_run=False)
      # Reset only the skull_strip stage for sub-M2040:
      reset_qc_sidecars(DERIV_DIR, subject="sub-M2040",
                        stage="skull_strip", dry_run=False)
      # Nuke a single subject's sidecar entirely (no audit trail):
      reset_qc_sidecars(DERIV_DIR, subject="sub-M2040", session="ses-842",
                        keep_edits=False, dry_run=False)
    """
    if stage is not None and stage not in STAGES:
        raise ValueError(f"Unknown stage {stage!r}; allowed: {STAGES}")

    affected = []
    for sp in Path(deriv_dir).rglob("*.qc.json"):
        try:
            data = json.loads(sp.read_text())
        except Exception:
            continue
        if subject and data.get("subject") != subject:
            continue
        if session and data.get("session") != session:
            continue

        if stage is not None:
            # Stage-level reset
            stages = data.get("stages") or {}
            if stage not in stages:
                continue
            if dry_run:
                affected.append(sp); continue
            stages[stage] = {"rating": None, "issue_tags": [], "notes": ""}
            data["stages"] = stages
            if stage == "lesion":
                data["rating"] = None
                data["rating_label"] = None
                data["issue_tags"] = []
                data["notes"] = ""
            sp.write_text(json.dumps(data, indent=2) + "\n")
            affected.append(sp)
        else:
            # Sidecar-level reset
            if dry_run:
                affected.append(sp); continue
            if not keep_edits:
                sp.unlink()
                affected.append(sp)
                continue
            # Keep edits; clear ratings + stages
            data["stages"] = _empty_stage_dict()
            data["rating"] = None
            data["rating_label"] = None
            data["issue_tags"] = []
            data["notes"] = ""
            data["reviewer"] = None
            data["reviewed_on"] = None
            data["marked_for_rerun"] = False
            sp.write_text(json.dumps(data, indent=2) + "\n")
            affected.append(sp)

    return affected


# ============================================================
# Re-run queue
# ============================================================
def mark_for_rerun(mask_path: Path, marked: bool = True,
                   reviewer: str | None = None):
    rec = QCRecord.load(mask_path)
    rec.marked_for_rerun = marked
    if reviewer and not rec.reviewer:
        rec.reviewer = reviewer
    rec.save()


def list_rerun_queue(deriv_dir: Path) -> pd.DataFrame:
    df = summarize_qc(deriv_dir)
    if df.empty:
        return df
    return df[df["marked_for_rerun"] == True].copy()


def rerun_subject(t1w_path: Path, linda_out_dir: Path, *,
                  manual_seed: Path | None = None,
                  reviewer: str | None = None,
                  linda_cmd: str = "linda_predict.sh") -> int:
    """
    Re-run LINDA on a subject. If `manual_seed` is given, pass it as the
    third argument (LINDA's manual-seed entry point). Returns the
    subprocess exit code; appends an edit log entry on success.

    NOTE: the exact LINDA command-line for manual-seed re-runs depends on
    the LINDA version. Adjust `linda_cmd` if your install differs.
    """
    cmd = [linda_cmd, str(t1w_path), str(linda_out_dir)]
    if manual_seed is not None:
        cmd.append(str(manual_seed))
    print(f"  ▶ {' '.join(cmd)}")
    res = subprocess.run(cmd)
    if res.returncode == 0:
        mask = linda_out_dir / "Lesion_in_MNI.nii.gz"
        if mask.exists():
            rec = QCRecord.load(mask)
            rec.marked_for_rerun = False     # cleared on successful re-run
            rec.log_edit(
                operation=("rerun_with_seed" if manual_seed else "rerun_as_is"),
                params={"manual_seed": str(manual_seed) if manual_seed else None},
                reviewer=reviewer, tool="linda_predict",
            )
            rec.save()
    return res.returncode


# Path to the R stub that calls LINDA with brain_mask= bypass.
# Lives next to this module.
_LINDA_R_STUB     = Path(__file__).parent / "linda_predict_with_mask.R"
# Bash wrapper that auto-routes to host Rscript or to Rscript inside
# the LINDA singularity container. Used by default on Neurodesk where
# R only exists inside the container.
_LINDA_BASH_STUB  = Path(__file__).parent / "linda_predict_with_mask.sh"


def run_linda_with_mask_via_R(
    t1w_path: Path,
    brain_mask: Path,
    linda_out_dir: Path,
    *,
    reviewer: str | None = None,
    r_cmd: str = "R",
    verbose: bool = True,
    cache: bool = True,
) -> int:
    """
    Bridge helper for Neurodesk users whose LINDA container deploys `R`
    on PATH but not `Rscript` (and where the in-container
    `linda_predict_with_mask.sh` wrapper hasn't been built yet).

    Calls `R --no-save -e '...'` with an inline LINDA invocation that
    uses `brain_mask=` to bypass internal skull stripping. Mirrors the
    file-on-disk approach but skips the Rscript dependency entirely.

    Same return-code semantics as `run_linda_with_mask()`: 0 on success,
    nonzero on R failure.
    """
    linda_out_dir = Path(linda_out_dir)
    linda_out_dir.mkdir(parents=True, exist_ok=True)

    # Build the R command. We escape paths via repr() so apostrophes /
    # spaces don't break the inline expression.
    t1   = str(Path(t1w_path).resolve())
    mask = str(Path(brain_mask).resolve())
    out  = str(linda_out_dir.resolve())
    verbose_lit = "TRUE" if verbose else "FALSE"
    cache_lit   = "TRUE" if cache   else "FALSE"
    r_expr = (
        "suppressPackageStartupMessages(library(LINDA)); "
        f"outputs <- linda_predict("
        f"file={t1!r}, brain_mask={mask!r}, outdir={out!r}, "
        f"verbose={verbose_lit}, cache={cache_lit}); "
        f"save(outputs, file=file.path({out!r}, 'linda_outputs.RData')); "
        "cat('[run_linda_with_mask_via_R] DONE\\n')"
    )

    cmd = [r_cmd, "--no-save", "--quiet", "-e", r_expr]
    print(f"  ▶ (R --no-save) bypassing LINDA's skull-strip with HD-BET mask")
    print(f"      T1     = {t1}")
    print(f"      mask   = {mask}")
    print(f"      outdir = {out}")
    res = subprocess.run(cmd)

    if res.returncode == 0:
        lesion = linda_out_dir / "Lesion_in_MNI.nii.gz"
        if lesion.exists():
            rec = QCRecord.load(lesion)
            rec.marked_for_rerun = False
            rec.log_edit(
                operation="rerun_with_mask_bypass_via_R",
                params={"brain_mask_source": mask, "r_cmd": r_cmd},
                reviewer=reviewer, tool="R --no-save -e",
            )
            rec.save()
    return res.returncode


# Common system locations to look for a host Rscript binary.
_RSCRIPT_SEARCH_PATHS = [
    "/usr/bin/Rscript",
    "/usr/local/bin/Rscript",
    "/opt/R/bin/Rscript",
    "/opt/conda/bin/Rscript",
]


def _find_rscript(explicit: str = "Rscript") -> str | None:
    """Locate a host Rscript binary, or None if not found.

    Search order:
      1. The explicit command (PATH lookup or absolute path).
      2. A few static fallback paths.

    NOTE: this only checks the *host* — on Neurodesk the host has no R
    and Rscript only exists inside the LINDA singularity container. In
    that case `run_linda_with_mask()` falls back to the bash wrapper
    which dispatches through `singularity exec`.
    """
    import shutil as _sh
    p = _sh.which(explicit) or (explicit if Path(explicit).is_absolute()
                                and Path(explicit).exists() else None)
    if p:
        return p
    for cand in _RSCRIPT_SEARCH_PATHS:
        if Path(cand).is_file():
            return cand
    return None


def run_linda_with_mask(
    t1w_path: Path,
    brain_mask: Path,
    linda_out_dir: Path,
    *,
    reviewer: str | None = None,
    rscript_cmd: str = "Rscript",
    r_stub: Path | None = None,
    verbose: bool = True,
    cache: bool = True,
) -> int:
    """
    Run LINDA via its R API, passing a pre-computed brain mask so LINDA
    bypasses its own (template-based) skull-stripping. This sidesteps the
    over-stripping failure mode where lesion-induced template-registration
    error causes LINDA's internal n4_skull_strip to drop large chunks of
    cortex near the lesion.

    LINDA writes its outputs directly into `linda_out_dir` (the R API
    respects the `outdir=` arg), so unlike the shell wrapper there's no
    "outputs landed adjacent to input" relocation step.

    Returns the Rscript exit code. Appends a sidecar edit log entry on
    success, identifying the mask source for provenance.
    """
    stub = Path(r_stub) if r_stub else _LINDA_R_STUB
    if not stub.exists():
        raise FileNotFoundError(
            f"LINDA R stub not found at {stub}. Expected it next to "
            f"linda_qc.py — was the file checked in?"
        )

    # Routing logic (in priority order):
    #   1. Explicit override: `rscript_cmd` set to anything other than
    #      "Rscript" → call that Rscript on the R stub directly.
    #   2. **Container wrapper**: `linda_predict_with_mask.sh` on PATH
    #      → call it like any other CLI. This is what Neurodesk ships
    #      in the LINDA container alongside `linda_predict.sh`. Cleanest
    #      path: the host wrapper does the singularity exec for us.
    #   3. **Local bash wrapper**: the `linda_predict_with_mask.sh`
    #      that ships in this repo, which auto-discovers the LINDA
    #      `.simg` from `linda_predict.sh` and dispatches via
    #      `singularity exec`. Fallback for older container versions
    #      that don't yet bundle the in-container script.
    #   4. **Host Rscript**: native R install, if you have one.
    import shutil as _sh
    explicit_override = (rscript_cmd != "Rscript")
    container_wrapper = _sh.which("linda_predict_with_mask.sh")

    args_tail = [
        "--t1",     str(t1w_path),
        "--mask",   str(brain_mask),
        "--outdir", str(linda_out_dir),
    ]

    if explicit_override:
        resolved = _find_rscript(rscript_cmd)
        if resolved is None:
            raise FileNotFoundError(
                f"Cannot find Rscript at the requested location "
                f"({rscript_cmd!r})."
            )
        cmd = [resolved, str(stub), *args_tail]
        print(f"  ▶ (host Rscript override) {' '.join(cmd)}")
    elif container_wrapper:
        # Cleanest path — Neurodesk's transparent-singularity wrapper
        # for the in-container script. Same UX as linda_predict.sh.
        cmd = [container_wrapper, *args_tail]
        print(f"  ▶ (container wrapper) {' '.join(cmd)}")
    elif _LINDA_BASH_STUB.exists():
        # Local bash wrapper — does the singularity exec dance itself.
        cmd = ["bash", str(_LINDA_BASH_STUB), *args_tail]
        print(f"  ▶ (local bash wrapper → singularity exec) "
              f"{' '.join(cmd)}")
    else:
        resolved = _find_rscript("Rscript")
        if resolved is None:
            raise FileNotFoundError(
                "Cannot find any way to invoke LINDA's R API:\n"
                "  • `linda_predict_with_mask.sh` not on PATH (would "
                "be installed by the LINDA Neurodesk container)\n"
                "  • the local bash wrapper at "
                f"{_LINDA_BASH_STUB} is missing\n"
                "  • no host Rscript found\n\n"
                "Fixes:\n"
                "  • Update the LINDA module so its container ships "
                "linda_predict_with_mask.sh, OR\n"
                "  • Pull the repo (the local wrapper ships next to "
                "this module), OR\n"
                "  • Set CONFIG['HDBET_RSCRIPT_CMD'] to an absolute "
                "Rscript path, OR\n"
                "  • Drop back to legacy padding mode with "
                "CONFIG['HDBET_USE_MASK_BYPASS'] = False."
            )
        cmd = [resolved, str(stub), *args_tail]
        print(f"  ▶ (host Rscript) {' '.join(cmd)}")

    if not verbose:
        cmd.append("--quiet")
    if not cache:
        cmd.append("--no-cache")

    res = subprocess.run(cmd)

    if res.returncode == 0:
        mask = linda_out_dir / "Lesion_in_MNI.nii.gz"
        if mask.exists():
            rec = QCRecord.load(mask)
            rec.marked_for_rerun = False
            rec.log_edit(
                operation="rerun_with_mask_bypass",
                params={"brain_mask_source": str(brain_mask)},
                reviewer=reviewer, tool="linda_predict_with_mask.R",
            )
            rec.save()
    return res.returncode


# ============================================================
# Brain extraction integration (HD-BET / SynthStrip)
# ============================================================
def _which(cmd: str) -> str | None:
    return shutil.which(cmd)


def detect_brain_extractor() -> str | None:
    """Return 'hd-bet', 'mri_synthstrip', or None — whichever is on PATH."""
    for c in ("hd-bet", "mri_synthstrip"):
        if _which(c):
            return c
    return None


def _has_nvidia_gpu() -> bool:
    """Quick GPU check via nvidia-smi. Returns False on any failure."""
    try:
        result = subprocess.run(
            ["nvidia-smi"], capture_output=True, timeout=5,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False


# Neurodesk module-load hints (used in error messages)
NEURODESK_MODULES = {
    "hd-bet":         "hd-bet/1.0.0",
    "mri_synthstrip": "fsl/6.0.7.4",         # SynthStrip ships with FSL >= 6.0.5
}


def brain_extractor_help_text() -> str:
    """A clear, ready-to-paste hint for loading HD-BET or SynthStrip on Neurodesk."""
    return (
        "No brain extractor on PATH yet.\n"
        "\n"
        "Scroll up to the cell titled \"Optional: load brain-extractor "
        "modules (Neurodesk)\" near the top of THIS notebook and run it,\n"
        "then come back here and re-run this cell.\n"
        "\n"
        "If that cell isn't there, paste this into a new cell anywhere\n"
        "above and run it once per session:\n"
        "\n"
        "    import module\n"
        "    await module.load('hd-bet/1.0.0')         # preferred\n"
        "    # or, if HD-BET isn't available:\n"
        "    await module.load('fsl/6.0.7.4')          # provides mri_synthstrip\n"
        "\n"
        "Outside Neurodesk, install one of:\n"
        "    pip install hd-bet                        # HD-BET\n"
        "    # or download FreeSurfer / SynthStrip\n"
    )


def run_hd_bet(t1w_path: Path, out_dir: Path,
               *, prefer: str | None = None,
               extra_args: list[str] | None = None,
               device: str | None = None,
               mode: str = "fast",
               tta: bool = False) -> dict:
    """
    Run HD-BET (preferred) or SynthStrip on `t1w_path`.

    Writes:
      <out_dir>/<stem>_brain.nii.gz       — skull-stripped image
      <out_dir>/<stem>_brain_mask.nii.gz  — binary brain mask

    Returns a dict with `brain`, `mask`, `tool`, `returncode`. Raises
    `RuntimeError` if neither HD-BET nor SynthStrip is installed.

    Device / mode (HD-BET only):
      device : "cpu", "0" (GPU id), or None (auto: GPU if available, else CPU)
      mode   : "fast" (single model, ~10× faster on CPU; recommended) or
               "accurate" (5-model ensemble; only practical with a GPU)
      tta    : test-time augmentation (much slower, marginal gain; default off)

    On Neurodesk, you may need to load the appropriate module first
    in a separate cell of THIS notebook:
        await module.load('hd-bet/1.0.0')
        # or
        await module.load('fsl/6.0.7.4')           # for mri_synthstrip
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t1 = Path(t1w_path)
    stem = t1.name
    if stem.endswith(".nii.gz"):
        stem = stem[:-len(".nii.gz")]
    elif stem.endswith(".nii"):
        stem = stem[:-len(".nii")]
    brain = out_dir / f"{stem}_brain.nii.gz"
    mask  = out_dir / f"{stem}_brain_mask.nii.gz"

    tool = prefer or detect_brain_extractor()
    if tool is None:
        raise RuntimeError(brain_extractor_help_text())

    if tool == "hd-bet":
        # Auto-detect device if caller didn't specify
        if device is None:
            device = "0" if _has_nvidia_gpu() else "cpu"
        # HD-BET writes <prefix>.nii.gz (brain) and <prefix>_mask.nii.gz
        prefix = out_dir / f"{stem}_hdbet"
        cmd = [
            "hd-bet", "-i", str(t1), "-o", str(prefix),
            "-device", str(device),
            "-mode", mode,
            "-tta", "1" if tta else "0",
        ]
        if extra_args:
            cmd.extend(extra_args)
        if device == "cpu" and mode == "accurate":
            print("  ⚠ HD-BET in 'accurate' mode is *very* slow on CPU "
                  "(5-model ensemble). Consider mode='fast'.")
        print(f"  ▶ {' '.join(cmd)}")
        res = subprocess.run(cmd)
        if res.returncode == 0:
            # HD-BET names: <prefix>.nii.gz and <prefix>_mask.nii.gz
            hd_brain = Path(f"{prefix}.nii.gz")
            hd_mask  = Path(f"{prefix}_mask.nii.gz")
            if hd_brain.exists(): shutil.move(str(hd_brain), brain)
            if hd_mask.exists():  shutil.move(str(hd_mask),  mask)
        return {"tool": "hd-bet", "brain": brain, "mask": mask,
                "returncode": res.returncode}

    if tool == "mri_synthstrip":
        cmd = ["mri_synthstrip",
               "-i", str(t1), "-o", str(brain), "-m", str(mask)]
        if extra_args:
            cmd.extend(extra_args)
        print(f"  ▶ {' '.join(cmd)}")
        res = subprocess.run(cmd)
        return {"tool": "mri_synthstrip", "brain": brain, "mask": mask,
                "returncode": res.returncode}

    raise ValueError(f"Unknown brain extractor: {tool!r}")


def replace_linda_skull_strip(linda_out_dir: Path,
                              new_brain_mask: Path,
                              new_brain_image: Path | None = None,
                              *, reviewer: str | None = None) -> dict:
    """
    Swap LINDA's BrainMask + N4corrected_Brain with HD-BET / SynthStrip
    versions. The originals are preserved in `_linda_original/`.

    `new_brain_image` is optional — if provided, replaces
    `N4corrected_Brain.nii.gz`. Otherwise, only the brain mask is
    replaced and the next LINDA run will re-derive the brain image.

    After swapping, you typically want to call `rerun_subject` so LINDA
    re-derives the registration and lesion prediction from the corrected
    inputs.
    """
    linda_out_dir = Path(linda_out_dir)
    targets = [
        ("BrainMask.nii.gz",          Path(new_brain_mask)),
    ]
    if new_brain_image is not None:
        targets.append(("N4corrected_Brain.nii.gz", Path(new_brain_image)))
    for name, src in targets:
        dst = linda_out_dir / name
        # Backup original on first swap
        if dst.exists():
            backup_dir = dst.parent / "_linda_original"
            backup_dir.mkdir(exist_ok=True)
            backup = backup_dir / name
            if not backup.exists():
                shutil.copy2(dst, backup)
        shutil.copy2(src, dst)

    # Log on the lesion sidecar
    lesion = linda_out_dir / "Lesion_in_MNI.nii.gz"
    if lesion.exists():
        rec = QCRecord.load(lesion)
        rec.log_edit(
            operation="replace_skull_strip",
            params={
                "new_brain_mask":  str(new_brain_mask),
                "new_brain_image": str(new_brain_image) if new_brain_image else None,
                "tool":            "hd-bet_or_synthstrip",
            },
            reviewer=reviewer, tool="upstream_repair",
        )
        rec.save()
    return {"replaced": [n for n, _ in targets], "linda_dir": linda_out_dir}


def make_brain_with_padding(t1_path: Path, brain_mask_path: Path,
                            output_path: Path,
                            *, padding_mm: float = 8.0,
                            fake_skull_intensity_pct: float = 40.0,
                            csf_rim_mm: float = 2.0,
                            csf_intensity_pct: float = 5.0) -> Path:
    """
    Build a synthetic T1 image where the brain is intact and surrounded
    by an anatomically-realistic two-layer rim:

        brain  →  CSF (thin, dark)  →  skull (thicker, medium)  →  zero

    The two-rim design mimics the real T1 brain-edge pattern (CSF in
    the subarachnoid space → meninges/skull → scalp). This gives
    LINDA's ANTs-based stripper a more stable target — its
    template-prior expects a CSF/skull boundary, not a brain/air one,
    and tends to bite less aggressively into the brain when it sees
    the expected pattern.

    Output structure (concentric, inside out):
      1. inside HD-BET brain mask         : original T1 intensities (brain)
      2. CSF rim  (csf_rim_mm thick)      : csf_intensity_pct of brain mean
      3. Skull rim (padding_mm thick)     : fake_skull_intensity_pct of brain mean
      4. outside skull rim                : 0

    Args:
        t1_path: original T1 (with skull intact)
        brain_mask_path: HD-BET-derived brain mask (binary)
        output_path: where to write the padded T1
        padding_mm: SKULL rim thickness in mm (default 8)
        fake_skull_intensity_pct: skull rim intensity as % of brain mean
                    (default 40 — roughly mimics dura/skull on T1)
        csf_rim_mm: CSF rim thickness in mm (default 2; set to 0 to
                    disable the inner rim and use the old single-rim
                    behaviour)
        csf_intensity_pct: CSF rim intensity as % of brain mean
                    (default 5 — CSF is very dark on T1)

    Returns the output path. Both input volumes must share the same
    affine and shape; we don't resample.
    """
    from scipy.ndimage import binary_dilation

    t1 = nib.load(str(t1_path))
    mask_img = nib.load(str(brain_mask_path))
    if t1.shape != mask_img.shape:
        raise ValueError(
            f"Shape mismatch: T1 {t1.shape} vs brain mask "
            f"{mask_img.shape}"
        )
    if not np.allclose(t1.affine, mask_img.affine, atol=1e-3):
        raise ValueError("Affine mismatch between T1 and brain mask")

    t1_data = t1.get_fdata()
    mask_data = mask_img.get_fdata() > 0
    if mask_data.sum() == 0:
        raise ValueError(f"Brain mask is empty: {brain_mask_path}")

    voxel_size = max(abs(t1.affine[0, 0]), 0.1)
    csf_voxels   = max(0, int(round(csf_rim_mm / voxel_size)))
    skull_voxels = max(1, int(round(padding_mm / voxel_size)))

    # Two concentric dilations: first to the CSF edge, then further
    # to the skull edge.
    if csf_voxels > 0:
        csf_dilated = binary_dilation(mask_data, iterations=csf_voxels)
    else:
        csf_dilated = mask_data
    skull_dilated = binary_dilation(csf_dilated, iterations=skull_voxels)

    csf_rim   = csf_dilated   & ~mask_data
    skull_rim = skull_dilated & ~csf_dilated

    brain_mean  = float(t1_data[mask_data].mean())
    csf_value   = brain_mean * (csf_intensity_pct / 100.0)
    skull_value = brain_mean * (fake_skull_intensity_pct / 100.0)

    padded = np.zeros_like(t1_data, dtype=t1_data.dtype)
    padded[mask_data] = t1_data[mask_data]
    if csf_voxels > 0:
        padded[csf_rim] = csf_value
    padded[skull_rim] = skull_value

    n_brain = int(mask_data.sum())
    n_csf   = int(csf_rim.sum())
    n_skull = int(skull_rim.sum())
    print(f"  padded T1: brain {n_brain:,} (intensity ~{brain_mean:.0f})"
          f"  +  CSF rim {n_csf:,} ({csf_voxels}vox @ ~{csf_value:.1f})"
          f"  +  skull rim {n_skull:,} ({skull_voxels}vox @ ~{skull_value:.1f})")

    nib.save(nib.Nifti1Image(padded, t1.affine, t1.header),
             str(output_path))
    return output_path


def promote_misplaced_linda_output(linda_out_dir: Path,
                                   *, dry_run: bool = True) -> dict:
    """
    Recovery helper: if a previous restrip_and_rerun left LINDA's
    new outputs in `<linda_out_dir>.parent/_hdbet_work/linda/` instead
    of `linda_out_dir/`, move them to the canonical location.

    Returns {"found": bool, "moved": [filenames], "actual_dir": Path}.

    Use when QC keeps showing pre-HD-BET outputs even though the
    HD-BET re-run ran. Typically that means LINDA wrote outputs
    adjacent to the HD-BET-stripped T1 (`_hdbet_work/linda/`) instead
    of into linda_out_dir.

    `dry_run=True` (default) only reports what would be moved.
    """
    linda_out_dir = Path(linda_out_dir)
    candidate = linda_out_dir.parent / "_hdbet_work" / "linda"
    if not candidate.exists():
        return {"found": False, "moved": [], "actual_dir": candidate}

    files = sorted(candidate.iterdir())
    nii_files = [f for f in files if f.is_file()
                 and (f.name.endswith(".nii.gz") or f.name.endswith(".nii"))]

    if dry_run:
        return {"found": True, "moved": [f.name for f in nii_files],
                "actual_dir": candidate, "dry_run": True}

    # Backup canonical first (only the files we're about to overwrite)
    backup_dir = linda_out_dir / "_linda_original"
    backup_dir.mkdir(exist_ok=True)
    for src in nii_files:
        canonical = linda_out_dir / src.name
        if canonical.exists():
            backup = backup_dir / src.name
            if not backup.exists():
                shutil.copy2(canonical, backup)
            canonical.unlink()
        shutil.move(str(src), str(linda_out_dir / src.name))
    # Try to clean up the empty subdir
    try:
        candidate.rmdir()
    except OSError:
        pass
    return {"found": True, "moved": [f.name for f in nii_files],
            "actual_dir": candidate, "dry_run": False}


def hdbet_then_linda(t1w_path: Path, linda_out_dir: Path,
                     *, work_dir: Path | None = None,
                     reviewer: str | None = None,
                     linda_cmd: str = "linda_predict.sh",
                     use_mask_bypass: bool = True,
                     use_padding: bool = True,
                     padding_mm: float = 8.0,
                     csf_rim_mm: float = 2.0,
                     hdbet_mode: str = "fast",
                     hdbet_device: str | None = None,
                     rscript_cmd: str = "Rscript") -> dict:
    """
    First-pass version of `restrip_and_rerun` (no backup, no QC reset).
    Use this for the *initial* segmentation when there are no prior
    LINDA outputs to preserve.

    Two modes (in order of preference):

    A. **Mask-bypass mode** (`use_mask_bypass=True`, default):
       1. Run HD-BET on the T1 → brain mask.
       2. Call `linda_predict(file=T1, brain_mask=hdbet_mask)` via the
          R stub. LINDA's internal n4_skull_strip is *bypassed*, so
          template-registration error on lesioned brains can't drop
          cortex. Outputs land directly in `linda_out_dir` (no
          relocation step).

    B. **Legacy padding mode** (`use_mask_bypass=False`):
       1. Run HD-BET on the T1 → brain mask.
       2. If `use_padding`, build a padded T1 (brain + CSF rim + skull
          rim) so LINDA's internal stripper has anatomy-shaped intensity
          to grab onto and doesn't bleed into the brain.
       3. Run LINDA on the padded T1 via `linda_predict.sh`.
       4. Move LINDA's outputs (which it writes adjacent to its input)
          into `linda_out_dir`.

    Mask-bypass is the right answer; padding is kept as a fallback in
    case the R stub or the LINDA R API isn't available on a given box.

    Raises RuntimeError if no brain extractor is on PATH — see
    `brain_extractor_help_text()`.

    Returns a dict with the brain extractor used, the input fed to
    LINDA, the mode used, LINDA's exit code, and (legacy mode only)
    which files landed in linda_out_dir.
    """
    if detect_brain_extractor() is None:
        raise RuntimeError(brain_extractor_help_text())

    work = Path(work_dir or (linda_out_dir.parent / "_hdbet_work"))
    bx = run_hd_bet(t1w_path, work, mode=hdbet_mode, device=hdbet_device)
    if bx["returncode"] != 0:
        return {"phase": "brain_extraction", **bx,
                "linda_returncode": None, "moved": []}

    # ---------- mode A: mask bypass via R API ----------
    if use_mask_bypass:
        linda_out_dir.mkdir(parents=True, exist_ok=True)
        rc = run_linda_with_mask(
            t1w_path, bx["mask"], linda_out_dir,
            reviewer=reviewer, rscript_cmd=rscript_cmd,
        )
        return {
            "phase":       "complete",
            **bx,
            "mode":        "mask_bypass",
            "linda_input": str(t1w_path),
            "use_padding": False,
            "padding_mm":  None,
            "linda_returncode": rc,
            "moved":       [],
        }

    # ---------- mode B: legacy padding + linda_predict.sh ----------
    linda_input = bx["brain"]
    if use_padding:
        padded = work / f"{Path(t1w_path).name.replace('.nii.gz', '').replace('.nii', '')}_padded.nii.gz"
        try:
            make_brain_with_padding(t1w_path, bx["mask"], padded,
                                    padding_mm=padding_mm,
                                    csf_rim_mm=csf_rim_mm)
            linda_input = padded
        except Exception as e:
            print(f"  ⚠ Padding failed ({e}); using bare brain.")

    rc = rerun_subject(linda_input, linda_out_dir,
                       reviewer=reviewer, linda_cmd=linda_cmd)

    # LINDA writes outputs adjacent to its input — move them to canonical
    actual_out_dir = Path(linda_input).parent / "linda"
    moved = []
    if actual_out_dir.exists() and actual_out_dir.resolve() != linda_out_dir.resolve():
        linda_out_dir.mkdir(parents=True, exist_ok=True)
        for src in actual_out_dir.iterdir():
            if not src.is_file():
                continue
            dst = linda_out_dir / src.name
            if dst.exists():
                dst.unlink()
            shutil.move(str(src), str(dst))
            moved.append(src.name)
        try:
            actual_out_dir.rmdir()
        except OSError:
            pass

    return {
        "phase": "complete",
        **bx,
        "mode":        "legacy_padding",
        "linda_input": str(linda_input),
        "use_padding": use_padding,
        "padding_mm":  padding_mm if use_padding else None,
        "linda_returncode": rc,
        "moved":       moved,
    }


def restrip_and_rerun(t1w_path: Path, linda_out_dir: Path,
                      *, work_dir: Path | None = None,
                      reviewer: str | None = None,
                      linda_cmd: str = "linda_predict.sh",
                      use_mask_bypass: bool = True,
                      use_padding: bool = True,
                      padding_mm: float = 8.0,
                      csf_rim_mm: float = 2.0,
                      rscript_cmd: str = "Rscript") -> dict:
    """
    One-shot: run HD-BET on `t1w_path`, then re-run LINDA. The original
    LINDA outputs are preserved in `_linda_original/` for revert.

    Two modes (in order of preference):

    A. **Mask-bypass mode** (`use_mask_bypass=True`, default):
       Pass HD-BET's mask straight to LINDA via the R API
       (`linda_predict(brain_mask=...)`). LINDA's internal
       `n4_skull_strip` is skipped entirely, sidestepping the failure
       mode where lesion-induced template-registration error drops
       cortex near the lesion.

    B. **Legacy padding mode** (`use_mask_bypass=False`):
       Wrap the HD-BET brain in a CSF + skull rim and feed the padded
       image to `linda_predict.sh`. Kept as a fallback for boxes where
       the R API isn't available.

    `use_padding` / `padding_mm` / `csf_rim_mm` only apply in legacy
    mode. In mask-bypass mode they are ignored (no padding is needed —
    the bypass is what fixes the over-stripping).

    IMPORTANT: We *clear* the .nii.gz files in `linda_out_dir` after
    backing them up, because LINDA's caches skip work when outputs
    already exist. Without the clear, the re-run is a no-op.

    Returns a dict with: brain extractor used, mode used, the path
    actually fed to LINDA, LINDA's exit code, per-file regeneration
    status, and any mask-coverage warnings.
    """
    work = Path(work_dir or (linda_out_dir.parent / "_hdbet_work"))
    bx = run_hd_bet(t1w_path, work)
    if bx["returncode"] != 0:
        return {"phase": "brain_extraction", **bx, "linda_returncode": None}

    # Decide what we'll feed LINDA + which mode label to record.
    padded_path = None  # only set in legacy mode
    if use_mask_bypass:
        mode = "mask_bypass"
        linda_input = t1w_path  # original T1; mask is supplied separately
        print(f"  Mode: mask-bypass — feeding HD-BET mask to LINDA's R API")
    else:
        mode = "legacy_padding"
        linda_input = bx["brain"]
        if use_padding:
            padded_path = work / f"{Path(t1w_path).stem.replace('.nii','')}_padded.nii.gz"
            try:
                make_brain_with_padding(
                    t1w_path, bx["mask"], padded_path,
                    padding_mm=padding_mm,
                    csf_rim_mm=csf_rim_mm,
                )
                linda_input = padded_path
                print(f"  Using padded brain as LINDA input: {padded_path}")
            except Exception as e:
                print(f"  ⚠ Padding failed ({e}); falling back to bare brain.")
                padded_path = None
                linda_input = bx["brain"]

    # 1. Back up everything LINDA wrote into linda_out_dir
    orig_dir = linda_out_dir / "_linda_original"
    orig_dir.mkdir(exist_ok=True)
    pre_run_mtimes: dict[str, float] = {}
    for f in linda_out_dir.glob("*.nii.gz"):
        backup = orig_dir / f.name
        if not backup.exists():
            shutil.copy2(f, backup)
        pre_run_mtimes[f.name] = f.stat().st_mtime

    # 2. CLEAR the canonical files so LINDA can't skip them. The
    #    backups in _linda_original/ are still safe for revert.
    cleared = []
    for f in linda_out_dir.glob("*.nii.gz"):
        try:
            f.unlink()
            cleared.append(f.name)
        except OSError as e:
            print(f"  ⚠ couldn't delete {f.name} before re-run: {e}")
    if cleared:
        print(f"  Cleared {len(cleared)} stale .nii.gz file(s) from "
              f"{linda_out_dir} before re-running LINDA.")

    # 3. Run LINDA — either via the R API (mask-bypass) or the shell
    #    wrapper (legacy padding).
    if use_mask_bypass:
        rc = run_linda_with_mask(
            t1w_path, bx["mask"], linda_out_dir,
            reviewer=reviewer, rscript_cmd=rscript_cmd,
        )
        # The R API writes directly to outdir — no relocation needed.
        moved = []
    else:
        # NOTE: linda_predict.sh writes outputs to `linda/` adjacent to
        # its input. We move them into linda_out_dir below.
        rc = rerun_subject(linda_input, linda_out_dir,
                           reviewer=reviewer, linda_cmd=linda_cmd)
        actual_out_dir = Path(linda_input).parent / "linda"
        moved = []
        if (actual_out_dir.exists()
                and actual_out_dir.resolve() != linda_out_dir.resolve()):
            print(f"  Moving new LINDA output from {actual_out_dir} → "
                  f"{linda_out_dir}")
            linda_out_dir.mkdir(parents=True, exist_ok=True)
            for src in actual_out_dir.iterdir():
                if not src.is_file():
                    continue
                dst = linda_out_dir / src.name
                if dst.exists():
                    dst.unlink()
                shutil.move(str(src), str(dst))
                moved.append(src.name)
            try:
                actual_out_dir.rmdir()
            except OSError:
                pass
            print(f"  Moved {len(moved)} file(s) into canonical linda/ dir.")

    # 4. Verify regeneration: which canonical files are newer than
    #    they were before the re-run? Surface this in the result so
    #    the caller can warn the user if LINDA didn't actually produce
    #    fresh output.
    regenerated = []
    missing_after = []
    for name in pre_run_mtimes:
        new_path = linda_out_dir / name
        if not new_path.exists():
            missing_after.append(name)
        elif new_path.stat().st_mtime > pre_run_mtimes[name]:
            regenerated.append(name)

    # 5. Sanity check: did the new brain mask shrink suspiciously?
    #    Common when HD-BET runs in `fast` mode and drops cerebellum
    #    or brainstem.
    mask_warning = None
    new_mask = linda_out_dir / "BrainMask.nii.gz"
    orig_mask = orig_dir / "BrainMask.nii.gz"
    if new_mask.exists() and orig_mask.exists():
        try:
            new_n = int((nib.load(str(new_mask)).get_fdata() > 0).sum())
            old_n = int((nib.load(str(orig_mask)).get_fdata() > 0).sum())
            if old_n > 0:
                ratio = new_n / old_n
                if ratio < 0.85:
                    mask_warning = (
                        f"New brain mask covers {new_n:,} voxels vs "
                        f"original {old_n:,} (ratio {ratio:.2f}). "
                        f"This is suspicious shrinkage — typically means "
                        f"cerebellum or brainstem was dropped. "
                        f"Consider re-running with HDBET_MODE='accurate' "
                        f"(slower but covers more tissue)."
                    )
        except Exception as e:
            mask_warning = f"Could not check mask coverage: {e}"

    # 6. Log on the sidecar AND clear the QC stage ratings — they
    #    were about a different image, so they're now stale.
    lesion = linda_out_dir / "Lesion_in_MNI.nii.gz"
    if lesion.exists():
        rec = QCRecord.load(lesion)
        # Snapshot the pre-rerun stage ratings into the edit log so the
        # audit trail keeps "what we used to think" before clearing.
        prior_stages = {st: dict(rec.stages.get(st) or {})
                        for st in STAGES}
        rec.log_edit(
            operation="restrip_with_hd_bet_and_rerun",
            params={"brain_extractor": bx["tool"],
                    "mode": mode,
                    "skull_stripped_t1": str(bx["brain"]),
                    "brain_mask": str(bx["mask"]),
                    "linda_input": str(linda_input),
                    "use_padding": bool(padded_path is not None),
                    "padding_mm": padding_mm if padded_path else None,
                    "regenerated_files": regenerated,
                    "missing_after_rerun": missing_after,
                    "mask_warning": mask_warning,
                    "prior_stages_snapshot": prior_stages,
                    "qc_invalidated": True},
            reviewer=reviewer, tool="upstream_repair",
        )
        # Clear the stages — the new images need fresh QC.
        for st in STAGES:
            rec.set_stage(st, rating=None, issue_tags=[], notes="")
        rec.marked_for_rerun = False
        rec.reviewer = None
        rec.reviewed_on = None
        rec.save()

    return {
        "phase": "complete",
        **bx,
        "mode":              mode,
        "linda_input":       str(linda_input),
        "linda_returncode":  rc,
        "regenerated_files": regenerated,
        "missing_after_rerun": missing_after,
        "mask_warning":      mask_warning,
    }
