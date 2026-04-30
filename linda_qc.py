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
                            fake_skull_intensity_pct: float = 40.0) -> Path:
    """
    Build a synthetic T1 image where the brain is intact and surrounded
    by a thin rim of low-intensity "fake skull" voxels. Designed to be
    fed into LINDA so its internal brain extractor has a non-brain rim
    to strip, instead of biting into a brain-air boundary and
    over-stripping the brain.

    Output structure:
      - inside HD-BET brain mask  : original T1 intensities (brain)
      - in the dilated rim        : fake_skull_intensity_pct of brain mean
      - outside the dilated rim   : 0

    Args:
        t1_path: original T1 (with skull intact)
        brain_mask_path: HD-BET-derived brain mask (binary)
        output_path: where to write the padded T1
        padding_mm: rim thickness in mm (default 8 — wide enough that
                    LINDA's stripper doesn't bleed past it).
        fake_skull_intensity_pct: rim intensity as % of brain mean
                    (default 40 — roughly mimics dura/skull on T1).

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
    padding_voxels = max(1, int(round(padding_mm / voxel_size)))
    dilated = binary_dilation(mask_data, iterations=padding_voxels)

    brain_mean = float(t1_data[mask_data].mean())
    rim_value = brain_mean * (fake_skull_intensity_pct / 100.0)

    padded = np.zeros_like(t1_data, dtype=t1_data.dtype)
    padded[mask_data] = t1_data[mask_data]
    rim_voxels = dilated & ~mask_data
    padded[rim_voxels] = rim_value

    n_brain = int(mask_data.sum())
    n_rim = int(rim_voxels.sum())
    print(f"  padded T1: {n_brain:,} brain voxels (kept), "
          f"{n_rim:,} rim voxels @ intensity {rim_value:.1f}, "
          f"{padding_voxels}-voxel ({padding_mm:.0f}mm) padding")

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
                     use_padding: bool = True,
                     padding_mm: float = 8.0,
                     hdbet_mode: str = "fast",
                     hdbet_device: str | None = None) -> dict:
    """
    First-pass version of `restrip_and_rerun` (no backup, no QC reset).
    Use this for the *initial* segmentation when there are no prior
    LINDA outputs to preserve.

    Workflow:
      1. Run HD-BET (or SynthStrip) on the original T1 → brain mask.
      2. If `use_padding`, build a padded T1 (brain + fake-skull rim).
      3. Run LINDA on the padded T1.
      4. Move LINDA's output (which it writes adjacent to its input)
         into `linda_out_dir`.

    Raises RuntimeError if no brain extractor is on PATH — see
    `brain_extractor_help_text()`.

    Returns a dict with the brain extractor used, the input fed to
    LINDA, LINDA's exit code, and which files landed in linda_out_dir.
    """
    if detect_brain_extractor() is None:
        raise RuntimeError(brain_extractor_help_text())

    work = Path(work_dir or (linda_out_dir.parent / "_hdbet_work"))
    bx = run_hd_bet(t1w_path, work, mode=hdbet_mode, device=hdbet_device)
    if bx["returncode"] != 0:
        return {"phase": "brain_extraction", **bx,
                "linda_returncode": None, "moved": []}

    linda_input = bx["brain"]
    if use_padding:
        padded = work / f"{Path(t1w_path).name.replace('.nii.gz', '').replace('.nii', '')}_padded.nii.gz"
        try:
            make_brain_with_padding(t1w_path, bx["mask"], padded,
                                    padding_mm=padding_mm)
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
        "linda_input": str(linda_input),
        "use_padding": use_padding,
        "padding_mm": padding_mm if use_padding else None,
        "linda_returncode": rc,
        "moved": moved,
    }


def restrip_and_rerun(t1w_path: Path, linda_out_dir: Path,
                      *, work_dir: Path | None = None,
                      reviewer: str | None = None,
                      linda_cmd: str = "linda_predict.sh",
                      use_padding: bool = True,
                      padding_mm: float = 8.0) -> dict:
    """
    One-shot: run HD-BET on `t1w_path`, then re-run LINDA on the
    skull-stripped image. The original LINDA outputs are preserved.

    Strategy: rather than mucking with LINDA's intermediate files
    (which is fragile across versions), we pass the brain-extracted T1
    as the new input.

    `use_padding` (default True): wrap the HD-BET-stripped brain in a
    thin rim of low-intensity "fake skull" before handing to LINDA, so
    LINDA's own brain extractor has something to strip and doesn't
    bleed past the brain-air boundary. Set to False to feed the bare
    HD-BET output directly (older behavior, sometimes over-strips).

    `padding_mm`: rim thickness when use_padding=True (default 8mm —
    wide enough that LINDA's stripper doesn't bite into the brain).

    IMPORTANT: We *clear* the .nii.gz files in `linda_out_dir` after
    backing them up, because LINDA's predict.sh skips work when
    outputs already exist. Without the clear, the re-run is a no-op.

    Returns a dict with the brain extractor used, the path to the T1
    actually fed to LINDA, LINDA's exit code, per-file regeneration
    status, and any mask-coverage warnings.
    """
    work = Path(work_dir or (linda_out_dir.parent / "_hdbet_work"))
    bx = run_hd_bet(t1w_path, work)
    if bx["returncode"] != 0:
        return {"phase": "brain_extraction", **bx, "linda_returncode": None}

    # Optionally build a padded T1 (brain + fake-skull rim) and feed
    # THAT to LINDA, instead of the bare brain-extracted image.
    linda_input = bx["brain"]
    padded_path = None
    if use_padding:
        padded_path = work / f"{Path(t1w_path).stem.replace('.nii','')}_padded.nii.gz"
        try:
            make_brain_with_padding(
                t1w_path, bx["mask"], padded_path,
                padding_mm=padding_mm,
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

    # 3. Run LINDA on the (possibly padded) skull-stripped T1.
    #    NOTE: linda_predict.sh writes .nii.gz output to a `linda/`
    #    subdirectory ADJACENT TO THE INPUT T1, not into the supplied
    #    output_dir. We work around that in step 3.5 by moving them.
    rc = rerun_subject(linda_input, linda_out_dir,
                       reviewer=reviewer, linda_cmd=linda_cmd)

    # 3.5. Find where LINDA actually wrote outputs (adjacent to the
    #      input we just gave it) and move them into linda_out_dir.
    actual_out_dir = Path(linda_input).parent / "linda"
    moved = []
    if actual_out_dir.exists() and actual_out_dir.resolve() != linda_out_dir.resolve():
        print(f"  Moving new LINDA output from {actual_out_dir} → {linda_out_dir}")
        linda_out_dir.mkdir(parents=True, exist_ok=True)
        for src in actual_out_dir.iterdir():
            if not src.is_file():
                continue
            dst = linda_out_dir / src.name
            # If a stale copy exists at canonical, replace it
            if dst.exists():
                dst.unlink()
            shutil.move(str(src), str(dst))
            moved.append(src.name)
        # Try to remove the now-empty actual_out_dir
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
                    "skull_stripped_t1": str(bx["brain"]),
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
        "linda_returncode": rc,
        "regenerated_files": regenerated,
        "missing_after_rerun": missing_after,
        "mask_warning": mask_warning,
    }
