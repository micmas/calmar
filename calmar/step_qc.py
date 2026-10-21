"""Saved QC evidence for every processing step: one PNG plus plausibility metrics.

Interactive viewers disappear when the notebook is closed or exported. These
figures and numbers are written by the Slurm job next to its results, embedded
by the notebook's step summaries, and therefore survive as a QC record.

Each figure shows the step's output as an *outline* on the image it was
computed from, through the lesion (or brain) centre, so a reviewer can judge
placement rather than just presence.

Two kinds of numbers, deliberately kept apart:
* ``metrics`` describe the outputs (volumes, number of blobs, Dice between
  methods, lesion outside the brain mask). They characterise how a *tool*
  behaved on this lesion and are never flagged: tools legitimately differ by
  lesion type, and judging them is not this check's job.
* ``flags`` are *workflow* checks: an implausible input, an empty output, a
  registration or transform that failed, a mask from another session, an
  invalid map, or an output made with an outdated method.
"""
from pathlib import Path
import os

import numpy as np
import nibabel as nib

from . import masks as cm
from .study import mni_masks

# Outline colours follow the notebook's mask-origin colours.
COLORS = {"linda": "red", "synthstroke": "lime", "manual": "dodgerblue",
          "hdbet": "yellow", "hdbet_tissue": "orange", "template": "cyan", "bcbtoolkit": "magenta",
          "deepdisco": "cyan"}
LABELS = {"linda": "LINDA", "synthstroke": "SynthStroke", "manual": "Manual",
          "hdbet": "brain mask", "hdbet_tissue": "HD-BET part", "template": "MNI152 brain outline"}

# Plausibility ranges that trigger a "look closer" flag.
BRAIN_ML_RANGE = (800, 2000)        # adult brain-tissue volume (checked on the HD-BET part)
WARP_VOLUME_RATIO = (0.5, 2.0)      # template/native lesion volume; outside = transform suspect
MANUAL_OUTSIDE_HEAD_MAX = 0.05      # registered manual mask outside the head = registration failed
# (The head, not the HD-BET brain mask: chronic lesions include CSF-filled
# cavities that brain extraction leaves out, so a correctly registered expert
# mask can legitimately extend beyond the brain mask.)
# Subject_in_MNI vs the FSL MNI152 brain it is registered to, Pearson r inside
# the template brain mask. 2026-10-12, ds004884 with the ch2 -> MNI152 chain:
# 0.63-0.65 (3 participants; individual anatomy and lesions keep it well below 1).
# Under the old ch2-only space the same check gave 0.35-0.54 (39 registrations).
# Below 0.30 suggests a failed registration, not an imperfect one.
TEMPLATE_CORR_MIN = 0.30


# ── image helpers ────────────────────────────────────────────────────────────

def _load(path, like=None, order=0):
    """Load as RAS+ float array, optionally resampled onto ``like``'s grid."""
    img = path if isinstance(path, nib.spatialimages.SpatialImage) else nib.load(str(path))
    img = nib.as_closest_canonical(img)
    if like is not None and (img.shape != like.shape or not np.allclose(img.affine, like.affine, atol=1e-3)):
        from nibabel.processing import resample_from_to
        img = resample_from_to(img, like, order=order)
    return img


def _data(img):
    return np.asanyarray(img.dataobj).astype(np.float32)


def voxel_ml(img):
    return float(abs(np.linalg.det(img.affine[:3, :3]))) / 1000.0


def head_mask(t1):
    """Head (everything that is not background) of a T1: intensity above 5% of the
    robust maximum, closed (dark skull would otherwise connect CSF-filled lesion
    cavities to the background), holes filled, largest connected part."""
    from scipy.ndimage import binary_closing, binary_fill_holes, label
    nz = t1[t1 > 0]
    if not nz.size:
        return np.zeros(t1.shape, bool)
    fg = binary_fill_holes(binary_closing(t1 > 0.05 * np.percentile(nz, 99), iterations=3))
    lab, n = label(fg)
    if n > 1:
        fg = lab == (np.bincount(lab.ravel())[1:].argmax() + 1)
    return fg


def dice(a, b):
    a, b = a > 0.5, b > 0.5
    total = a.sum() + b.sum()
    return float(2 * (a & b).sum() / total) if total else float("nan")


def components(mask):
    from scipy.ndimage import label
    return int(label(mask > 0.5)[1])


def _centre(mask):
    pts = np.argwhere(mask > 0.5)
    if not len(pts):
        return None
    c = pts.mean(axis=0)
    return pts[np.argmin(((pts - c) ** 2).sum(axis=1))]


def _slices(mask, shape, n=5):
    """Axial slices spanning the mask's extent (or the volume if empty)."""
    z = np.where((mask > 0.5).any(axis=(0, 1)))[0] if mask is not None else []
    lo, hi = (z.min(), z.max()) if len(z) else (int(shape[2] * .25), int(shape[2] * .75))
    return sorted(set(np.linspace(lo, hi, n + 2)[1:-1].round().astype(int))) or [shape[2] // 2]


def _window(bg):
    nz = bg[bg > 0]
    return (0, float(np.percentile(nz, 99.5))) if nz.size else (0, 1)


def _panel(ax, bg, overlays, axis, index, heat=None):
    """Draw one slice: grey background, optional heat map, mask outlines."""
    take = lambda a: np.rot90(np.take(a, index, axis=axis))
    vmin, vmax = _window(bg)
    ax.imshow(take(bg), cmap="gray", vmin=vmin, vmax=vmax, interpolation="nearest")
    if heat is not None:
        h = take(heat[0])
        ax.imshow(np.ma.masked_less(h, heat[2]), cmap=heat[1], vmin=heat[2], vmax=1,
                  alpha=.7, interpolation="nearest")
    if axis in (1, 2):  # RAS data, rotated: subject left is on the image left
        ax.text(.03, .97, "L", color="white", fontsize=8, transform=ax.transAxes, va="top")
        ax.text(.97, .97, "R", color="white", fontsize=8, transform=ax.transAxes, va="top", ha="right")
    for data, color in overlays:
        sl = take(data)
        if (sl > 0.5).any() and (sl <= 0.5).any():
            ax.contour(sl, levels=[0.5], colors=[color], linewidths=1.0)
    ax.set_axis_off()


def figure(rows, title, out_png):
    """rows: list of dict(bg, overlays=[(data, colour)], focus, label, heat)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ncol = 7
    fig, axes = plt.subplots(len(rows), ncol, figsize=(2.1 * ncol, 2.3 * len(rows) + .5),
                             squeeze=False, facecolor="black")
    for r, row in enumerate(rows):
        bg, overlays, focus = row["bg"], row.get("overlays", []), row.get("focus")
        centre = _centre(focus) if focus is not None else None
        if centre is None:
            centre = np.array(bg.shape) // 2
        for c, z in enumerate(_slices(focus, bg.shape)[:5]):
            _panel(axes[r, c], bg, overlays, 2, z, row.get("heat"))
        _panel(axes[r, 5], bg, overlays, 1, centre[1], row.get("heat"))
        _panel(axes[r, 6], bg, overlays, 0, centre[0], row.get("heat"))
        for c in range(len(_slices(focus, bg.shape)[:5]), 5):
            axes[r, c].set_axis_off()
    fig.suptitle(title, color="white", fontsize=11)
    # Row labels are figure text, not axes titles: a long axes title would make
    # tight_layout shrink every panel to fit it.
    fig.tight_layout(rect=(0, 0, 1, .96), h_pad=2.0)
    for r, row in enumerate(rows):
        box = axes[r, 0].get_position()
        fig.text(box.x0, box.y1 + .005, row.get("label", ""), color="white", fontsize=9, va="bottom")
    out_png = Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_png.with_name(f".{out_png.name}.{os.getpid()}.tmp.png")
    fig.savefig(tmp, dpi=100, facecolor="black")
    plt.close(fig)
    os.replace(tmp, out_png)
    return out_png


def legend(*keys):
    return " · ".join(f"{LABELS.get(k, k)} = {COLORS[k]}" for k in keys)


# ── per-stage evidence ───────────────────────────────────────────────────────

def _brain(dirs, entry, t1):
    from .qc import find_best_hdbet_mask
    mask = find_best_hdbet_mask(dirs["hdbet"])
    if not cm.present(mask):
        return None
    anat = _load(t1)
    brain = _data(_load(mask, anat))
    vox = voxel_ml(anat)
    ml = float((brain > .5).sum() * vox)
    metrics = {"brain_volume_ml": round(ml, 1)}
    overlays, keys = [(brain, COLORS["hdbet"])], ["hdbet"]
    tissue_ml = ml
    # With BRAIN_MASK="hdbet+synthstrip" the mask is HD-BET OR SynthStrip
    # (processing.step_brain); show the HD-BET part too, so the CSF / cavity
    # voxels SynthStrip added are visible.
    tissue_path = next(iter(sorted(Path(dirs["hdbet"]).glob("*_desc-hdbet_brain_mask.nii.gz"))), None)
    if tissue_path is not None and "_desc-" not in Path(mask).name:
        tissue = _data(_load(tissue_path, anat))
        tissue_ml = float((tissue > .5).sum() * vox)
        metrics["hdbet_volume_ml"] = round(tissue_ml, 1)
        metrics["added_by_synthstrip_ml"] = round(float(((brain > .5) & (tissue <= .5)).sum() * vox), 1)
        overlays.append((tissue, COLORS["hdbet_tissue"])); keys.append("hdbet_tissue")
    flags = [] if BRAIN_ML_RANGE[0] <= tissue_ml <= BRAIN_ML_RANGE[1] else [
        f"brain volume {tissue_ml:.0f} ml is implausible for an adult (expected {BRAIN_ML_RANGE[0]}–{BRAIN_ML_RANGE[1]} ml); "
        "check the input image and its voxel size"]
    rows = [dict(bg=_data(anat), overlays=overlays, focus=brain, label="T1w · " + legend(*keys))]
    return rows, metrics, flags


def template_correlation(subject_in_mni):
    """Correlation of the warped T1 with the MNI152 template it was registered to
    (FSL MNI152NLin6Asym brain, calmar.templates), inside the template brain mask."""
    from . import templates
    sub = _load(subject_in_mni)
    t = _data(_load(templates.T1_BRAIN, sub, order=1))
    m = _data(_load(templates.BRAIN_MASK, sub)) > .5
    s = _data(sub)
    if m.sum() < 1000:
        return float("nan"), m
    return float(np.corrcoef(s[m], t[m])[0, 1]), m


def _lesion_metrics(name, mask, anat, brain=None):
    ml = float((mask > .5).sum() * voxel_ml(anat))
    out = {f"{name}_volume_ml": round(ml, 2), f"{name}_components": components(mask)}
    flags = [f"{LABELS[name]} mask is empty: later steps have no lesion to analyse for this source"] if ml == 0 else []
    if brain is not None and ml:
        outside = float(((mask > .5) & (brain <= .5)).sum() / (mask > .5).sum())
        out[f"{name}_fraction_outside_brain"] = round(outside, 3)
    return out, flags


def warp_check(name, native_ml, template_ml):
    """Lesion volume should survive the native -> template warp within brain-size
    scaling; a large change means the transform was applied wrongly."""
    if not native_ml or template_ml is None:
        return []
    ratio = template_ml / native_ml
    if WARP_VOLUME_RATIO[0] <= ratio <= WARP_VOLUME_RATIO[1]:
        return []
    return [f"{LABELS[name]} lesion volume changes ×{ratio:.2f} from native to template "
            f"({native_ml:.1f} → {template_ml:.1f} ml); the transform may have been applied wrongly"]


def _linda(dirs, entry, t1):
    from .qc import find_best_hdbet_mask
    native = dirs["linda"] / "Prediction3_native.nii.gz"
    sub_mni = dirs["linda"] / "Subject_in_MNI.nii.gz"
    if not cm.present(native):
        return None
    anat = _load(t1)
    lesion = _data(_load(native, anat))
    brain_path = find_best_hdbet_mask(dirs["hdbet"])
    brain = _data(_load(brain_path, anat)) if cm.present(brain_path) else None
    metrics, flags = _lesion_metrics("linda", lesion, anat, brain)
    rows = [dict(bg=_data(anat), overlays=[(lesion, COLORS["linda"])], focus=lesion,
                 label="Native T1w · " + legend("linda"))]
    if cm.present(sub_mni):
        corr, tpl_mask = template_correlation(sub_mni)
        mni = _load(sub_mni)
        les_mni = dirs["linda"] / "Lesion_in_MNI.nii.gz"
        lm = _data(_load(les_mni, mni)) if cm.present(les_mni) else np.zeros(mni.shape)
        metrics["template_correlation"] = round(corr, 3)
        metrics["linda_mni_volume_ml"] = round(float((lm > .5).sum() * voxel_ml(mni)), 2)
        flags += warp_check("linda", metrics["linda_volume_ml"], metrics["linda_mni_volume_ml"])
        if not corr >= TEMPLATE_CORR_MIN:
            flags.append(f"warped T1 correlates unusually weakly with MNI152 (r={corr:.2f}; "
                         f"typical 0.35–0.55): the registration every template-space output relies on may have failed")
        rows.append(dict(bg=_data(mni), overlays=[(tpl_mask.astype(float), COLORS["template"]),
                                                  (lm, COLORS["linda"])], focus=lm,
                         label=f"Subject_in_MNI · {legend('template', 'linda')} · r={corr:.2f}"))
    return rows, metrics, flags


def _registration(dirs, entry, t1):
    """Template registration without LINDA: the warped T1 against MNI152, and the
    SynthStroke lesion's volume before and after the warp."""
    sub_mni = dirs["registration"] / "Subject_in_MNI.nii.gz"
    if not cm.present(sub_mni):
        return None
    corr, tpl_mask = template_correlation(sub_mni)
    mni = _load(sub_mni)
    metrics, flags = {"template_correlation": round(corr, 3)}, []
    if not corr >= TEMPLATE_CORR_MIN:
        flags.append(f"warped T1 correlates unusually weakly with MNI152 (r={corr:.2f}; "
                     f"typical 0.35–0.55): the registration every template-space output relies on may have failed")
    overlays, lesion = [(tpl_mask.astype(float), COLORS["template"])], None
    native, warped = dirs["synthstroke"] / "prediction_lesion_mask.nii.gz", mni_masks(dirs)["synthstroke"]
    if cm.present(native) and cm.present(warped):
        anat = _load(t1)
        native_ml = float((_data(_load(native, anat)) > .5).sum() * voxel_ml(anat))
        lesion = _data(_load(warped, mni))
        metrics["synthstroke_mni_volume_ml"] = round(float((lesion > .5).sum() * voxel_ml(mni)), 2)
        flags += warp_check("synthstroke", native_ml, metrics["synthstroke_mni_volume_ml"])
        overlays.append((lesion, COLORS["synthstroke"]))
    keys = ["template"] + (["synthstroke"] if lesion is not None else [])
    rows = [dict(bg=_data(mni), overlays=overlays, focus=lesion,
                 label=f"Subject_in_MNI · {legend(*keys)} · r={corr:.2f}")]
    return rows, metrics, flags


def _native_masks(dirs, entry, anat):
    """Native-space lesion masks that exist for this entry, on the T1 grid."""
    found = {}
    for source, path in [("linda", dirs["linda"] / "Prediction3_native.nii.gz"),
                         ("synthstroke", dirs["synthstroke"] / "prediction_lesion_mask.nii.gz"),
                         ("manual", dirs["template"] / "_manual_mask_compare" / "ManualLesion_in_T1_sitk.nii.gz"),
                         ("manual", dirs["template"] / "_manual_mask_compare" / "ManualLesion_in_T1.nii.gz")]:
        if source not in found and cm.present(path):
            found[source] = _data(_load(path, anat))
    return found


def _synthstroke(dirs, entry, t1):
    from .qc import find_best_hdbet_mask
    pred = dirs["synthstroke"] / "prediction_lesion_mask.nii.gz"
    if not cm.present(pred):
        return None
    anat = _load(t1)
    found = _native_masks(dirs, entry, anat)
    brain_path = find_best_hdbet_mask(dirs["hdbet"])
    brain = _data(_load(brain_path, anat)) if cm.present(brain_path) else None
    metrics, flags = _lesion_metrics("synthstroke", found["synthstroke"], anat, brain)
    raw = dirs["synthstroke"] / "prediction_lesion_mask_raw.nii.gz"
    if cm.present(raw):
        removed = float(((_data(_load(raw, anat)) > .5).sum() - (found["synthstroke"] > .5).sum()) * voxel_ml(anat))
        metrics["synthstroke_removed_outside_brain_ml"] = round(removed, 2)
    if "linda" in found:
        metrics["dice_synthstroke_vs_linda"] = round(dice(found["synthstroke"], found["linda"]), 3)
    warped, sub_mni = mni_masks(dirs)["synthstroke"], dirs["template"] / "Subject_in_MNI.nii.gz"
    if cm.present(warped) and cm.present(sub_mni):
        mni = _load(sub_mni)
        metrics["synthstroke_mni_volume_ml"] = round(float((_data(_load(warped, mni)) > .5).sum() * voxel_ml(mni)), 2)
        flags += warp_check("synthstroke", metrics["synthstroke_volume_ml"], metrics["synthstroke_mni_volume_ml"])
    keys = [k for k in ("synthstroke", "linda") if k in found]
    rows = [dict(bg=_data(anat), overlays=[(found[k], COLORS[k]) for k in keys],
                 focus=found["synthstroke"], label="Native T1w · " + legend(*keys))]
    return rows, metrics, flags


def _manual(dirs, entry, t1, manual_info=None):
    anat = _load(t1)
    found = _native_masks(dirs, entry, anat)
    manual_info = manual_info or {}
    metrics = {k: v for k, v in manual_info.items() if v is not None}
    flags = []
    if manual_info.get("mask_session") and entry.get("session") and manual_info["mask_session"] != entry["session"]:
        flags.append(f"manual mask drawn on {manual_info['mask_session']}, T1 is {entry['session']}: "
                     "cross-session registration; lesion extent may differ between scans")
    rows = []
    if "manual" in found:
        from .qc import find_best_hdbet_mask
        brain_path = find_best_hdbet_mask(dirs["hdbet"])
        brain = _data(_load(brain_path, anat)) if cm.present(brain_path) else None
        m, f = _lesion_metrics("manual", found["manual"], anat, brain)
        metrics.update(m); flags += f
        # The expert drew the lesion inside the head; if our registration of their
        # scan to the T1 put part of it in the background, the registration failed.
        outside = float((found["manual"] > .5)[~head_mask(_data(anat))].sum() / max((found["manual"] > .5).sum(), 1))
        metrics["manual_fraction_outside_head"] = round(outside, 3)
        if outside > MANUAL_OUTSIDE_HEAD_MAX:
            flags.append(f"{outside:.0%} of the registered manual mask lies outside the head: "
                         "the reference-scan registration failed (see row 2)")
        manual = found["manual"] > .5
        for other in ("linda", "synthstroke"):
            if other in found:
                metrics[f"dice_{other}_vs_manual"] = round(dice(found[other], found["manual"]), 3)
                # Dice alone hides the direction of disagreement: report the
                # tool's volume, how much of the manual lesion it covers and
                # how much of it lies inside the manual lesion.
                auto = found[other] > .5
                metrics[f"{other}_volume_ml"] = round(float(auto.sum() * voxel_ml(anat)), 2)
                metrics[f"{other}_covers_manual"] = round(float((auto & manual).sum() / max(manual.sum(), 1)), 3)
                metrics[f"{other}_inside_manual"] = round(float((auto & manual).sum() / max(auto.sum(), 1)), 3)
        keys = [k for k in ("manual", "linda", "synthstroke") if k in found]
        rows.append(dict(bg=_data(anat), overlays=[(found[k], COLORS[k]) for k in keys],
                         focus=found["manual"], label="Native T1w · " + legend(*keys)))
        ref = dirs["template"] / "_manual_mask_compare" / "T2_in_T1_sitk.nii.gz"
        if cm.present(ref):
            rows.append(dict(bg=_data(_load(ref, anat, order=1)), overlays=[(found["manual"], COLORS["manual"])],
                             focus=found["manual"],
                             label="Reference scan registered to T1 · manual outline should sit on the lesion"))
    expert = dirs["template"] / "ExpertMask_in_MNI.nii.gz"
    sub_mni = dirs["template"] / "Subject_in_MNI.nii.gz"
    if cm.present(expert) and cm.present(sub_mni):
        mni = _load(sub_mni)
        e = _data(_load(expert, mni))
        overlays = [(e, COLORS["manual"])]
        metrics["manual_mni_volume_ml"] = round(float((e > .5).sum() * voxel_ml(mni)), 2)
        flags += warp_check("manual", metrics.get("manual_volume_ml"), metrics["manual_mni_volume_ml"])
        if cm.present(dirs["linda"] / "Lesion_in_MNI.nii.gz"):
            l = _data(_load(dirs["linda"] / "Lesion_in_MNI.nii.gz", mni))
            metrics["dice_linda_vs_manual_mni"] = round(dice(l, e), 3)
            overlays.append((l, COLORS["linda"]))
        rows.append(dict(bg=_data(mni), overlays=overlays, focus=e,
                         label="Subject_in_MNI · " + legend("manual", "linda")))
    return (rows, metrics, flags) if rows else None


USABLE = ("computed", "cached", "legacy-cache")


def _produced_maps(stage, outputs):
    """{source: map path} for maps this step actually produced or validly reused.

    DeepDisco: the whole-brain model when produced, else the first model.
    """
    tokens = {"linda": "linda", "synthstroke": "synthstroke", "expert": "manual"}
    found = {}
    for output in outputs or []:
        if output.get("status") not in USABLE or not output.get("path"):
            continue
        name = Path(output["path"]).name
        for token, source in tokens.items():
            if stage == "bcb" and name == f"Disconnectome_{token}.nii.gz":
                found[source] = Path(output["path"])
            elif stage == "deepdisco" and name.startswith(f"DeepDisco_{token}_"):
                if source not in found or name.endswith("_whole_brain.nii.gz"):
                    found[source] = Path(output["path"])
    return found


def _disconnectome(stage, dirs, entry, t1, outputs=None):
    sub_mni = dirs["template"] / "Subject_in_MNI.nii.gz"
    maps = _produced_maps(stage, outputs)
    flags = [f"{o.get('reason', 'stale output')[:160]}" for o in outputs or [] if o.get("status") == "stale"]
    if not cm.present(sub_mni) or not maps:
        return ([], {}, flags) if flags else None
    mni = _load(sub_mni)
    bg = _data(mni)
    lesions = mni_masks(dirs)
    rows, metrics = [], {}
    for source in ("linda", "synthstroke", "manual"):
        if source not in maps:
            continue
        path = maps[source]
        raw = np.asanyarray(nib.load(str(path)).dataobj)
        if not np.isfinite(raw).all():
            flags.append(f"{LABELS[source]} map contains non-finite values")
        if np.nanmax(raw) <= 0:
            flags.append(f"{LABELS[source]} map is empty")
        elif np.nanmin(raw) < -1e-3 or np.nanmax(raw) > 1 + 1e-3:
            flags.append(f"{LABELS[source]} map outside 0–1 (range {np.nanmin(raw):.2g}–{np.nanmax(raw):.2g})")
        heat = _data(_load(path, mni, order=1))
        metrics[f"{source}_voxels_above_0.5"] = int((heat > .5).sum())
        if stage == "deepdisco":
            token = "expert" if source == "manual" else source
            bcb = dirs["bcbtoolkit"] / f"Disconnectome_{token}.nii.gz"
            if cm.present(bcb):
                b = _data(_load(bcb, mni, order=1))
                # Same definition as the comparison panel: voxels where either map is > 0.
                both = (b > 0) | (heat > 0)
                if both.sum() > 1:
                    metrics[f"{source}_r_vs_bcb"] = round(float(np.corrcoef(b[both], heat[both])[0, 1]), 3)
        lesion = _data(_load(lesions[source], mni)) if cm.present(lesions[source]) else None
        model = "" if stage == "bcb" else path.name.removesuffix(".nii.gz").split("_", 2)[-1]
        rows.append(dict(bg=bg, overlays=[(lesion, COLORS[source])] if lesion is not None else [],
                         focus=heat > .5, heat=(heat, "magma", .1),
                         label=f"{LABELS[source]} lesion outline + "
                               f"{'BCBToolkit disconnectome' if stage == 'bcb' else 'DeepDisco ' + model} (≥0.1)"))
    return rows, metrics, flags


TITLES = {"brain": "HD-BET brain extraction", "linda": "LINDA lesion segmentation",
          "synthstroke": "SynthStroke lesion segmentation", "manual": "Manual mask alignment",
          "registration": "Template registration (ANTs)",
          "bcb": "BCBToolkit disconnectome", "deepdisco": "DeepDisco disconnectome"}


def png_path(reports_dir, stage, entry):
    stem = "_".join(x for x in (entry["subject"], entry.get("session")) if x)
    return Path(reports_dir) / "qc" / "steps" / stage / f"{stem}.png"


def stage_evidence(stage, entry, dirs, reports_dir, *, manual_info=None, outputs=None):
    """Write the step's QC PNG and return ``{"png", "metrics", "flags"}``.

    Returns None for stages without image evidence or when nothing exists yet.
    A failure to draw never hides a processing result: it is reported as a flag.
    """
    t1 = Path(entry["t1w"])
    makers = {"brain": _brain, "linda": _linda, "synthstroke": _synthstroke, "registration": _registration,
              "manual": lambda d, e, t: _manual(d, e, t, manual_info),
              "bcb": lambda d, e, t: _disconnectome("bcb", d, e, t, outputs),
              "deepdisco": lambda d, e, t: _disconnectome("deepdisco", d, e, t, outputs)}
    if stage not in makers:
        return None
    try:
        made = makers[stage](dirs, entry, t1)
    except Exception as error:  # evidence is advisory; keep the processing result
        # "complete": False makes the scheduler retry the step instead of reusing it.
        return {"png": None, "metrics": {}, "flags": [f"QC figure failed: {error}"], "complete": False}
    if made is None:
        return None
    rows, metrics, flags = made
    if not rows:  # nothing drawable (e.g. only stale maps): report the flags
        return {"png": None, "metrics": metrics, "flags": flags, "complete": True}
    label = " ".join(x for x in (entry["subject"], entry.get("session")) if x)
    try:
        png = figure(rows, f"{TITLES[stage]} — {label}", png_path(reports_dir, stage, entry))
    except Exception as error:
        return {"png": None, "metrics": metrics, "flags": flags + [f"QC figure failed: {error}"], "complete": False}
    return {"png": str(png), "metrics": metrics, "flags": flags, "complete": True}
