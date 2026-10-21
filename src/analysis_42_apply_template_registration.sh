#!/usr/bin/env bash
# analysis_42_apply_template_registration.sh
#
# Warp a native T1w-space image to FSL MNI152 (MNI152NLin6Asym, 1 mm) with the
# participant's ANTs registration from the registration step
# (src/analysis_29_registration.sh), used when LINDA is not run. With LINDA,
# src/analysis_15_warp_native_to_mni.sh applies LINDA's transforms instead.
# Called inside a processing job (calmar.processing.ants_warp_product), not
# submitted on its own.
#
# Usage:
#   bash src/analysis_42_apply_template_registration.sh \
#       --input     /path/to/prediction_lesion_mask.nii.gz \
#       --reference /path/to/Subject_in_MNI.nii.gz \
#       --warp      /path/to/T1w_to_MNI152_1Warp.nii.gz \
#       --affine    /path/to/T1w_to_MNI152_0GenericAffine.mat \
#       --output    /path/to/SynthStroke_in_MNI.nii.gz \
#       [--interp NearestNeighbor]   # default; keeps a mask binary

set -euo pipefail

INPUT="" REF="" WARP="" AFF="" OUT="" INTERP="NearestNeighbor"
while [ $# -gt 0 ]; do
    case "$1" in
        --input)     INPUT="$2"; shift 2 ;;
        --reference) REF="$2"; shift 2 ;;
        --warp)      WARP="$2"; shift 2 ;;
        --affine)    AFF="$2"; shift 2 ;;
        --output)    OUT="$2"; shift 2 ;;
        --interp)    INTERP="$2"; shift 2 ;;
        -h|--help)   sed -n '2,17p' "$0"; exit 0 ;;
        *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
done
for f in "$INPUT" "$REF" "$WARP" "$AFF"; do
    [ -f "$f" ] || { echo "Not found: $f" >&2; exit 3; }
done
[ -n "$OUT" ] || { echo "Need --output" >&2; exit 1; }

source /opt/neurodesktop/agent_bash_env.sh
module load ants/2.6.5
# The output path is the caller's staging file; it publishes it after validation.
# Transforms apply last-listed first: affine, then the nonlinear warp.
antsApplyTransforms -d 3 -i "$INPUT" -r "$REF" -t "$WARP" -t "$AFF" -n "$INTERP" -o "$OUT"
