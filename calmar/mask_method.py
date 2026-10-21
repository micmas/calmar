"""How a participant's lesion mask was made, and how it agrees with the manual mask.

``mask_method`` describes, for the mask a report uses, the steps that actually
produced it: read from the run records each processing job writes next to its
outputs (``calmar-cache.json`` for a folder, ``<file>.cache.json`` for a file),
not from the current configuration, so the report stays true even if the
configuration changed after processing. A product made before run records
existed is described as such.

``manual_agreement`` compares each automatic template-space mask with the
manual one (Dice, coverage, volume ratio); the report form shows it before a
report is generated, when the participant has a manual mask.
"""
from functools import lru_cache
from html import escape
import json
from pathlib import Path

import numpy as np

from .masks import MASK_LABELS
from .study import mni_masks

NO_RECORD = "no run record (made before run records were kept)"


def _record(path):
    """The run record of a product: its options and commands, or None."""
    path = Path(path)
    record = path / "calmar-cache.json" if path.is_dir() else Path(str(path) + ".cache.json")
    try:
        return json.loads(record.read_text())
    except (OSError, ValueError):
        return None


def _options(path):
    record = _record(path)
    return (record or {}).get("identity", {}).get("options")


def _brain_mask(dirs):
    options = _options(dirs["hdbet"])
    if options is None:
        return f"Brain mask: HD-BET ({NO_RECORD})."
    tool = ("union of HD-BET and SynthStrip (hdbet/1.0.0, synthstrip/7.4.1)"
            if options.get("method") == "hdbet+synthstrip" else "HD-BET (hdbet/1.0.0)")
    return f"Brain mask: {tool}, {options.get('mode', 'fast')} mode."


def _registration(dirs, mni_path):
    """The template registration that produced ``mni_path``."""
    options = _options(mni_path) or {}
    if options.get("registration") == "ants":
        reg = _options(dirs["registration"]) or {}
        seed = f", seed {reg['random_seed']}" if "random_seed" in reg else ""
        return ("Warped to the FSL MNI152 template (MNI152NLin6Asym, 1 mm) with this T1w's ANTs registration "
                f"(ants/2.6.5: affine, then SyN, with the SynthStroke lesion excluded from the cost function{seed}), "
                "nearest-neighbour resampling.")
    if options.get("module", "").startswith("linda") or not options:
        suffix = "" if options else f" ({NO_RECORD})"
        return ("Warped to the FSL MNI152 template (MNI152NLin6Asym, 1 mm) with LINDA's registration of this T1w "
                "(native → LINDA's template → ch2 → MNI152, one nearest-neighbour resampling)" + suffix + ".")
    return f"Warped to the FSL MNI152 template ({options})."


def mask_method(study, entry, source):
    """The steps that produced ``source``'s template-space mask, as sentences."""
    dirs = study.dirs(entry)
    t1 = Path(entry["t1w"]).name
    mni = mni_masks(dirs)[source]
    if source == "linda":
        options = _options(dirs["linda"])
        if options is None:
            return [f"Segmented by LINDA (linda/0.5.1) on the T1w {t1} ({NO_RECORD}).", _registration(dirs, mni)]
        skull = ("using that brain mask instead of LINDA's own skull strip"
                 if options.get("brain_mask_bypass") else "with LINDA's own skull strip")
        return [_brain_mask(dirs) if options.get("brain_mask_bypass") else None,
                f"Segmented by LINDA ({options.get('module', 'linda/0.5.1')}) on the T1w {t1}, {skull}; "
                f"random seed {options.get('random_seed', '—')}, "
                f"{options.get('threads', 1)} thread{'s' if options.get('threads', 1) != 1 else ''}.",
                "Warped to the FSL MNI152 template (MNI152NLin6Asym, 1 mm) with LINDA's own registration "
                "(native → LINDA's template → ch2 → MNI152, one nearest-neighbour resampling)."]
    if source == "synthstroke":
        options = _options(dirs["synthstroke"])
        if options is None:
            segmented = f"Segmented by SynthStroke on the T1w {t1} ({NO_RECORD})."
        else:
            tta = "with" if options.get("tta") else "without"
            segmented = (f"Segmented by SynthStroke ({options.get('module', 'synthstroke/0.0.0')}, synth-plus weights, "
                         f"{tta} test-time augmentation) on the T1w {t1}; predicted voxels outside the brain mask "
                         f"dilated by {options.get('brain_dilation', 2)} voxels were removed.")
        return [_brain_mask(dirs), segmented, _registration(dirs, mni)]
    if source == "manual":
        from .processing import manual_inputs
        mask, reference, space = manual_inputs({"dataset": str(study.dataset), "config": study.config}, entry)
        drawn = f"Expert-drawn mask {Path(mask).name}" if mask else "Expert-drawn mask"
        if space == "mni":
            return [f"{drawn}, provided in template space and used as is."]
        options = _options(dirs["template"] / "_manual_mask_compare") or {}
        if space == "other":
            to_t1 = (f"{drawn}, drawn on {Path(reference).name if reference else 'another scan'}; that scan was "
                     f"rigidly registered to the T1w {t1} (SimpleITK, Mattes mutual information, seed "
                     f"{options.get('sampling_seed', '—')}) and the mask resampled with nearest neighbour.")
        else:
            to_t1 = f"{drawn}, drawn on the T1w {t1}, regridded with nearest neighbour."
        if not options:
            to_t1 = to_t1[:-1] + f" ({NO_RECORD})."
        return [to_t1, _registration(dirs, mni)]
    raise ValueError(f"Unknown mask source: {source!r}")


def mask_method_html(study, entry, source):
    steps = [s for s in mask_method(study, entry, source) if s]
    return "<ol style='margin:2px 0 0 18px;padding:0'>" + "".join(f"<li>{escape(s)}</li>" for s in steps) + "</ol>"


@lru_cache(maxsize=64)
def _agreement(manual, others, stamp):
    import nibabel as nib
    from nibabel.processing import resample_from_to
    ref = nib.load(manual)
    truth = np.asanyarray(ref.dataobj) > .5
    voxel_ml = abs(np.linalg.det(ref.affine[:3, :3])) / 1000.0
    rows = []
    for source, path in others:
        img = nib.load(path)
        if img.shape != ref.shape or not np.allclose(img.affine, ref.affine):
            img = resample_from_to(img, ref, order=0)
        auto = np.asanyarray(img.dataobj) > .5
        both = (auto & truth).sum()
        rows.append({"source": source, "dice": 2 * both / max(auto.sum() + truth.sum(), 1),
                     "covers": both / max(truth.sum(), 1), "inside": both / max(auto.sum(), 1),
                     "ratio": auto.sum() / max(truth.sum(), 1), "volume_ml": auto.sum() * voxel_ml})
    return truth.sum() * voxel_ml, rows


def manual_agreement(masks):
    """``(manual_ml, rows)`` comparing each automatic mask with the manual one in
    template space, or None when there is no manual mask. ``masks``:
    ``{source: MNI path}``."""
    if "manual" not in masks:
        return None
    others = tuple((s, str(p)) for s, p in masks.items() if s != "manual")
    if not others:
        return None
    paths = [masks["manual"], *[p for _, p in others]]
    stamp = tuple(Path(p).stat().st_mtime_ns for p in paths)
    return _agreement(str(masks["manual"]), others, stamp)


def manual_agreement_html(masks):
    found = manual_agreement(masks)
    if found is None:
        return ""
    manual_ml, rows = found
    lines = "".join(
        f"<li>{MASK_LABELS.get(r['source'], r['source'])}: Dice <b>{r['dice']:.2f}</b> · covers "
        f"{r['covers']:.0%} of the manual lesion · {r['inside']:.0%} of it lies inside the manual lesion · "
        f"{r['volume_ml']:.1f} ml ({r['ratio']:.1f}× the manual volume)</li>" for r in rows)
    return ("<div style='font-size:12px;margin:4px 0'><b>Agreement with the manual mask</b> "
            f"({manual_ml:.1f} ml; template space, voxels &gt; 0.5). Dice 1 = identical. Low coverage means the "
            "method misses part of the manual lesion; little inside means it also labels other tissue."
            f"<ul style='margin:2px 0 0 18px;padding:0'>{lines}</ul></div>")
