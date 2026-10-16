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
# Control: with the template transforms omitted, the retained wrapper must
# reproduce LINDA's own native -> Penn -> ch2 lesion exactly (Lesion_in_ch2).
# The production chain adds ch2 -> MNI152 to these same transforms.
# Usage: sbatch src/analysis_16_verify_mni_wrapper.sh <dataset> <sub> <ses> <control_output.nii.gz>
DATASET="${1:?dataset root required}"
SUB="${2:?participant required}"
SES="${3:?session required}"
OUT="${4:?control mask output required}"
LINDA_DIR="$DATASET/derivatives/linda/$SUB/$SES/anat"
bash src/analysis_15_warp_native_to_mni.sh \
    --input "$LINDA_DIR/Prediction3_native.nii.gz" \
    --reference "$LINDA_DIR/Subject_in_ch2.nii.gz" \
    --warp "$LINDA_DIR/Reg3_sub_to_template_warp.nii.gz" \
    --affine "$LINDA_DIR/Reg3_sub_to_template_affine.mat" \
    --output "$OUT"
python -c 'import sys,nibabel as n,numpy as np; a,b=map(n.load,sys.argv[1:]); assert np.array_equal(a.get_fdata(),b.get_fdata()); print("Wrapper reproduces LINDA ch2 output exactly.")' "$OUT" "$LINDA_DIR/Lesion_in_ch2.nii.gz"
