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
source /opt/neurodesktop/agent_bash_env.sh

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

FINAL_DATA="data/synthetic_edgecases"
FINAL_QC="reports/benchmarks/edgecase_battery_qc.png"
if [ -d "${FINAL_DATA}" ] && [ -s "${FINAL_QC}" ]; then
    [ -s "${FINAL_DATA}.prov.json" ] && [ -s "${FINAL_QC}.prov.json" ] || {
        echo "legacy edge-case outputs exist without provenance" >&2
        exit 1
    }
    echo "edge-case battery and QC already exist with provenance"
    exit 0
fi
[ ! -e "${FINAL_DATA}" ] && [ ! -e "${FINAL_QC}" ] || {
    echo "only part of the edge-case output set exists; preserve or remove it before retrying" >&2
    exit 1
}
mkdir -p data reports/benchmarks
TMP_ROOT="$(mktemp -d data/.synthetic-edgecases.attempt.XXXXXX)"
trap 'rm -rf "${TMP_ROOT}"' EXIT
TMP_DATA="${TMP_ROOT}/dataset"
TMP_QC="${TMP_ROOT}/edgecase_battery_qc.png"

python3 - "${TMP_DATA}" "${TMP_QC}" <<'PY'
import sys
sys.path.insert(0, ".")
from calmar.synthetic import edgecase_install, EDGECASE_SPECS

edgecase_install(sys.argv[1], n_per_cat=3, seed=11)

# ── QC montage: first subject of each category, most-diagnostic modality ──
import numpy as np
import nibabel as nib
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ds = Path(sys.argv[1])
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
out = Path(sys.argv[2])
fig.savefig(out, dpi=130, bbox_inches="tight")
print(f"QC montage prepared → {out}")
PY
[ "$(find "${TMP_DATA}" -maxdepth 1 -name 'sub-*' | wc -l)" -eq 36 ] || {
    echo "edge-case generator did not produce 36 subjects" >&2
    exit 1
}
identify "${TMP_QC}"
neurodesk-astra-provenance publish "${TMP_DATA}" "${FINAL_DATA}" \
    --output-id synthetic_edgecases_dataset --tool python3 --script "$0"
if ! neurodesk-astra-provenance publish "${TMP_QC}" "${FINAL_QC}" \
    --output-id edgecase_battery_qc --tool python3 --script "$0"; then
    mv "${FINAL_DATA}" "${TMP_ROOT}/rollback_dataset"
    mv "${FINAL_DATA}.prov.json" "${TMP_ROOT}/rollback_dataset.prov.json"
    exit 1
fi
