#!/bin/bash
#SBATCH --job-name=calmar_mni_wrapper_check
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:05:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=2
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
module load linda/0.5.1
DATASET="${1:?dataset root required}"
OUT="${2:?control mask output required}"
LINDA_DIR="$DATASET/derivatives/linda/sub-M2026/ses-3098/anat"
bash src/analysis_15_warp_native_to_mni.sh \
    --input "$LINDA_DIR/Prediction3_native.nii.gz" \
    --reference "$LINDA_DIR/Subject_in_MNI.nii.gz" \
    --warp "$LINDA_DIR/Reg3_sub_to_template_warp.nii.gz" \
    --affine "$LINDA_DIR/Reg3_sub_to_template_affine.mat" \
    --output "$OUT"
python -c 'import sys,nibabel as n,numpy as np; a,b=map(n.load,sys.argv[1:]); assert np.array_equal(a.get_fdata(),b.get_fdata()); print("Final wrapper reproduces LINDA exactly.")' "$OUT" "$LINDA_DIR/Lesion_in_MNI.nii.gz"
