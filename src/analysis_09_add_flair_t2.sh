#!/bin/bash
#SBATCH --job-name=syn_modalities_qc
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:10:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1

# Validate and display the five co-registered synthetic modalities. FLAIR and
# T2w are now generated atomically with T1w/DWI/ADC by calmar.synthetic; this
# retained step preserves the historical entry point without mutating a
# published dataset.

set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

FINAL="reports/benchmarks/synthetic_modalities_qc.png"
if [ -e "${FINAL}" ]; then
    [ -s "${FINAL}" ] && [ -s "${FINAL}.prov.json" ] || {
        echo "legacy or incomplete QC montage exists: ${FINAL}" >&2
        exit 1
    }
    echo "synthetic modality QC already exists with provenance: ${FINAL}"
    exit 0
fi

mkdir -p reports/benchmarks
TMP_DIR="$(mktemp -d reports/benchmarks/.synthetic-modalities-qc.attempt.XXXXXX)"
trap 'rm -rf "${TMP_DIR}"' EXIT
TMP="${TMP_DIR}/synthetic_modalities_qc.png"

python3 - "${TMP}" <<'PY'
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np

out = Path(sys.argv[1])
modalities = [("T1w", "anat"), ("T2w", "anat"), ("FLAIR", "anat"),
              ("dwi", "dwi"), ("adc", "dwi")]
fig, axes = plt.subplots(2, 5, figsize=(16, 7))
for row, (phase, sub) in enumerate((("acute", "sub-synacu000"),
                                    ("chronic", "sub-synchr000"))):
    dataset = Path(f"data/synthetic_{phase}")
    mask_image = nib.load(dataset / "derivatives" / sub / f"{sub}_msk.nii.gz")
    lesion = np.asarray(mask_image.dataobj) > 0
    assert lesion.any(), f"empty ground truth for {sub}"
    z = int(np.argmax(lesion.sum(axis=(0, 1))))
    for column, (modality, folder) in enumerate(modalities):
        image = nib.load(dataset / sub / folder / f"{sub}_{modality}.nii.gz")
        data = np.asarray(image.dataobj)
        assert data.shape == lesion.shape and np.isfinite(data).all()
        np.testing.assert_allclose(image.affine, mask_image.affine)
        ax = axes[row, column]
        ax.imshow(data[:, :, z].T, cmap="gray", origin="lower")
        ax.contour(lesion[:, :, z].T, levels=[0.5], colors="lime", linewidths=0.9)
        ax.set_title(f"{phase} · {modality}", fontsize=10)
        ax.axis("off")
fig.suptitle("Synthetic phantoms — five co-registered modalities; ground truth in green",
             fontsize=12)
fig.tight_layout()
fig.savefig(out, dpi=130, bbox_inches="tight")
PY

identify "${TMP}"
neurodesk-astra-provenance publish "${TMP}" "${FINAL}" \
    --output-id synthetic_modalities_qc --tool python3 --script "$0"
