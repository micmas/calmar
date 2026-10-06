#!/bin/bash
#SBATCH --job-name=gen_edgecases
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:20:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=2

# Generate the synthetic edge-case battery (seed 11, 3 subjects per
# category, 12 categories → 36 subjects, 5 co-registered modalities each):
# tiny / multifocal / territorial-scale / faint-contrast / periventricular /
# cortical / mixed-chronology / lesion-negative for acute, plus the
# phase-appropriate subset for chronic. Ground truth per subject at
# derivatives/<sub>/<sub>_msk.nii.gz; the mixed-chronology cases carry an
# extra desc-distractorchronic mask (the old cavity that is NOT in GT).
# Idempotent per subject; writes participants.tsv as machine-readable
# category manifest. Also renders a per-category QC montage.

set -euo pipefail

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

python3 - <<'PY'
import sys
sys.path.insert(0, ".")
from calmar.synthetic import edgecase_install, EDGECASE_SPECS

edgecase_install("data/synthetic_edgecases", n_per_cat=3, seed=11)

# ── QC montage: first subject of each category, most-diagnostic modality ──
import numpy as np
import nibabel as nib
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ds = Path("data/synthetic_edgecases")
cats = sorted(EDGECASE_SPECS.items())
fig, axes = plt.subplots(3, 4, figsize=(15, 11))
for ax, (cat, spec) in zip(axes.flat, cats):
    sub = f"sub-{cat}000"
    mod, folder = (("dwi", "dwi") if spec["phase"] == "acute"
                   else ("T1w", "anat"))
    img = nib.load(ds / sub / folder / f"{sub}_{mod}.nii.gz").get_fdata()
    les = nib.load(ds / "derivatives" / sub / f"{sub}_msk.nii.gz").get_fdata() > 0
    z = int(np.argmax(les.sum(axis=(0, 1)))) if les.any() else img.shape[2] // 2
    ax.imshow(img[:, :, z].T, cmap="gray", origin="lower")
    if les.any():
        ax.contour(les[:, :, z].T, levels=[0.5], colors="lime", linewidths=0.9)
    d_p = ds / "derivatives" / sub / f"{sub}_desc-distractorchronic_msk.nii.gz"
    if d_p.exists():
        dis = nib.load(d_p).get_fdata() > 0
        if dis[:, :, z].any():
            ax.contour(dis[:, :, z].T, levels=[0.5], colors="orange",
                       linewidths=0.9)
    vox = int(les.sum())
    ax.set_title(f"{cat} · {mod} · {vox} vox", fontsize=10)
    ax.axis("off")
fig.suptitle("Edge-case battery — GT green; mixed-chronology distractor orange",
             fontsize=12)
fig.tight_layout()
out = Path("reports/benchmarks/edgecase_battery_qc.png")
tmp = out.with_name("edgecase_battery_qc_tmp.png")
fig.savefig(tmp, dpi=130, bbox_inches="tight")
tmp.rename(out)
print(f"QC montage → {out}")
PY
