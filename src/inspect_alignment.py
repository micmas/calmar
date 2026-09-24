"""Bounded before/after alignment QC, executed by the retained Slurm script."""
import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from nibabel.processing import resample_from_to

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import linda_qc as q

root, output = map(Path, sys.argv[1:])
records = {}
for sub, ses in [("sub-M2026", "ses-3098"), ("sub-M2029", "ses-180")]:
    d = root / "derivatives/linda" / sub / ses / "anat"
    ss = root / "derivatives/synthstroke" / sub / ses / "anat"
    out = output / sub / ses
    out.mkdir(parents=True)
    bg = nib.load(d / "Subject_in_MNI.nii.gz")
    b = bg.get_fdata(dtype=np.float32)
    record = {}
    for source, native, original in [
        ("linda", d / "Prediction3_native.nii.gz", d / "Lesion_in_MNI.nii.gz"),
        ("manual", d / "_manual_mask_compare/ManualLesion_in_T1_sitk.nii.gz", d / "ExpertMask_in_MNI.nii.gz"),
        ("synthstroke", ss / "prediction_lesion_mask.nii.gz", ss / "SynthStroke_in_MNI.nii.gz"),
    ]:
        corrected = out / original.name
        rc = q.warp_native_mask_to_mni(d.resolve(), native.resolve(), corrected.resolve())
        if rc:
            raise RuntimeError(f"Warp failed: {sub} {source}, rc={rc}")
        new = nib.load(corrected)
        assert new.shape == bg.shape and np.allclose(new.affine, bg.affine)
        new_data = new.get_fdata(dtype=np.float32)
        assert np.isfinite(new_data).all() and np.isin(new_data, [0, 1]).all()
        old_img = nib.load(original)
        old = resample_from_to(old_img, bg, order=0).get_fdata(dtype=np.float32) > 0
        mask = new_data > 0
        dice = float(2 * (old & mask).sum() / max(old.sum() + mask.sum(), 1))
        record[source] = {"before_after_dice": dice, "old_voxels": int(old.sum()),
                          "new_voxels": int(mask.sum()), "original_shape": list(old_img.shape),
                          "corrected_shape": list(new.shape)}
        if source == "linda":
            assert dice > 0.99, f"Corrected chain does not reproduce LINDA: Dice={dice}"
        points = np.argwhere(mask | old)
        cuts = np.round(np.median(points, axis=0)).astype(int)
        fig, axes = plt.subplots(2, 3, figsize=(12, 8))
        vmax = np.percentile(b[b > 0], 99)
        for row, lesion in enumerate([old, mask]):
            for axis in range(3):
                anatomy = np.take(b, cuts[axis], axis=axis).T
                overlay = np.take(lesion, cuts[axis], axis=axis).T
                ax = axes[row, axis]
                ax.imshow(anatomy, origin="lower", cmap="gray", vmin=0, vmax=vmax)
                ax.imshow(np.ma.masked_where(~overlay, overlay), origin="lower", cmap="autumn", alpha=.55, vmin=0, vmax=1)
                ax.set_title(f"{'Before' if row == 0 else 'Corrected'} — {'sagittal coronal axial'.split()[axis]}")
                ax.axis("off")
        fig.suptitle(f"{sub} {ses} · {source} on Subject_in_MNI")
        fig.tight_layout()
        fig.savefig(out / f"{source}_alignment.png", dpi=110)
        plt.close(fig)
        print(sub, source, record[source], flush=True)
    # Inspect binary overlays from cell 30 without modifying any original data.
    record["native_overlay_headers"] = {}
    for p in [ss / "prediction_lesion_mask.nii.gz", ss / "prediction_lesion_mask_boundary_t1.nii.gz"]:
        if not p.exists():
            record["native_overlay_headers"][p.name] = {"exists": False}
            continue
        im = nib.load(p); data = im.get_fdata(dtype=np.float32)
        record["native_overlay_headers"][p.name] = {
            "min": float(data.min()), "max": float(data.max()),
            "nonzero": int(np.count_nonzero(data)), "size": int(data.size),
            "cal_min": float(im.header["cal_min"]), "cal_max": float(im.header["cal_max"]),
        }
    records[f"{sub}/{ses}"] = record
(output / "metrics.json").write_text(json.dumps(records, indent=2) + "\n")
