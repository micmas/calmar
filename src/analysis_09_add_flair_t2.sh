#!/bin/bash
#SBATCH --job-name=syn_flair_t2
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:15:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=2

# Add FLAIR and T2w to every synthetic phantom (both phases), derived
# deterministically from the existing T1w and ground-truth mask so the
# original T1w/DWI/ADC volumes and all previous results stay untouched.
# Gives each subject 5 co-registered modalities — enough to feed tools like
# DeepISLES (DWI+ADC+FLAIR) or T1+FLAIR chronic models.
#
# Lesion signatures (values echo the generator's conventions):
#   acute:   FLAIR moderately hyperintense (subacute-visible; NOTE this
#            phantom does not model hyperacute DWI-FLAIR mismatch),
#            T2w hyperintense.
#   chronic: CSF-like cavity (T2w bright, FLAIR suppressed core) with a
#            FLAIR-bright gliotic rim (1-2 voxels around the cavity).
# Non-lesion contrast: T2w ~ inverted T1 with bright CSF; FLAIR = T2-like
# with CSF suppressed. Light smoothing + seeded Gaussian noise.
# Pure main-env python; no neuroimaging module needed. Idempotent.

set -euo pipefail

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

python3 - <<'PY'
import numpy as np
import nibabel as nib
from pathlib import Path
from scipy.ndimage import gaussian_filter, binary_dilation

for gi, (phase, tag) in enumerate([("acute", "synacu"), ("chronic", "synchr")]):
    ds = Path(f"data/synthetic_{phase}")
    for i in range(6):
        sub = f"sub-{tag}00{i}"
        t1_p = ds / sub / "anat" / f"{sub}_T1w.nii.gz"
        msk_p = ds / "derivatives" / sub / f"{sub}_msk.nii.gz"
        fl_p = ds / sub / "anat" / f"{sub}_FLAIR.nii.gz"
        t2_p = ds / sub / "anat" / f"{sub}_T2w.nii.gz"
        if fl_p.exists() and t2_p.exists():
            print(f"{phase}/{sub}: cached ✔")
            continue
        t1_img = nib.load(t1_p)
        t1 = t1_img.get_fdata().astype(np.float32)
        les = nib.load(msk_p).get_fdata() > 0
        brain = t1 > 1.0
        t = np.clip(t1 / 700.0, 0, 1.5)          # generator's tissue scale
        csf = brain & (t < 0.25)

        t2 = np.zeros_like(t1)
        t2[brain] = 400 + 500 * (1 - np.clip(t[brain], 0, 1))
        t2[csf] = 1300
        fl = np.zeros_like(t1)
        fl[brain] = 350 + 450 * (1 - np.clip(t[brain], 0, 1))
        fl[csf] = 100

        if phase == "acute":
            fl[les] = 900
            t2[les] = 1000
        else:
            rim = binary_dilation(les, iterations=2) & ~les & brain
            t2[les] = 1300
            fl[les] = 120
            fl[rim] = 850
            t2[rim] = 900

        rng = np.random.RandomState(9000 + 10 * gi + i)
        for arr, out in [(fl, fl_p), (t2, t2_p)]:
            img = gaussian_filter(arr, 0.6)
            img[brain] += rng.normal(0, 15, size=int(brain.sum()))
            img = np.clip(img, 0, None).astype(np.float32)
            tmp = out.with_name(out.name.replace(".nii.gz", "_tmp.nii.gz"))
            nib.save(nib.Nifti1Image(img, t1_img.affine, t1_img.header), tmp)
            tmp.rename(out)
        print(f"{phase}/{sub}: wrote FLAIR + T2w ✔")

# ── QC montage: one subject per phase, all 5 modalities + GT contour ──
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

MODS = [("T1w", "anat"), ("T2w", "anat"), ("FLAIR", "anat"),
        ("dwi", "dwi"), ("adc", "dwi")]
fig, axes = plt.subplots(2, 5, figsize=(16, 7))
for r, (phase, tag, sub) in enumerate([("acute", "synacu", "sub-synacu000"),
                                        ("chronic", "synchr", "sub-synchr000")]):
    ds = Path(f"data/synthetic_{phase}")
    les = nib.load(ds / "derivatives" / sub / f"{sub}_msk.nii.gz").get_fdata() > 0
    z = int(np.argmax(les.sum(axis=(0, 1))))
    for c, (mod, folder) in enumerate(MODS):
        img = nib.load(ds / sub / folder / f"{sub}_{mod}.nii.gz").get_fdata()
        ax = axes[r, c]
        ax.imshow(img[:, :, z].T, cmap="gray", origin="lower")
        ax.contour(les[:, :, z].T, levels=[0.5], colors="lime", linewidths=0.9)
        ax.set_title(f"{phase} · {mod}", fontsize=10)
        ax.axis("off")
fig.suptitle("Synthetic phantoms — 5 co-registered modalities, ground truth in green",
             fontsize=12)
fig.tight_layout()
out = Path("reports/benchmarks/synthetic_modalities_qc.png")
tmp = out.with_name("synthetic_modalities_qc_tmp.png")
fig.savefig(tmp, dpi=130, bbox_inches="tight")
tmp.rename(out)
print(f"QC montage → {out}")
PY
