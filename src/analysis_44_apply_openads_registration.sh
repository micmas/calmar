#!/usr/bin/env bash
# analysis_44_apply_openads_registration.sh
#
# Warp an image on the participant's DWI grid to FSL MNI152 (MNI152NLin6Asym,
# 1 mm) with OpenADS's own registration (affine + SyN, against its JHU ADC
# template in MNI152 space), in one resampling. Acute (DWI) route; the T1 routes
# use analysis_15 (LINDA) or analysis_42 (registration step). Called inside a
# processing job (calmar.processing.openads_warp_product), not submitted alone.
#
# Usage:
#   bash src/analysis_44_apply_openads_registration.sh \
#       --input     lesion_on_DWI.nii.gz \
#       --reference MNI152NLin6Asym_T1_1mm.nii.gz \
#       --affine    <sub>_aff_space-individual2MNI152.mat \
#       --syn       <sub>_syn_space-MNI1522MNI152.mat \
#       --warp      <sub>_warp_space-MNI1522MNI152.nii.gz \
#       --output    lesion_in_MNI.nii.gz \
#       [--interp NearestNeighbor]
set -euo pipefail
INPUT="" REF="" AFF="" SYN="" WARP="" OUT="" INTERP="NearestNeighbor"
while [ $# -gt 0 ]; do
    case "$1" in
        --input) INPUT="$2"; shift 2 ;;  --reference) REF="$2"; shift 2 ;;
        --affine) AFF="$2"; shift 2 ;;   --syn) SYN="$2"; shift 2 ;;
        --warp) WARP="$2"; shift 2 ;;    --output) OUT="$2"; shift 2 ;;
        --interp) INTERP="$2"; shift 2 ;;
        -h|--help) sed -n '2,19p' "$0"; exit 0 ;;
        *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
done
for f in "$INPUT" "$REF" "$AFF" "$SYN" "$WARP"; do [ -f "$f" ] || { echo "Not found: $f" >&2; exit 3; }; done
[ -n "$OUT" ] || { echo "Need --output" >&2; exit 1; }
source /opt/neurodesktop/agent_bash_env.sh
module load ants/2.6.5
# Last-listed transform is applied first: individual -> MNI affine, then OpenADS's
# SyN stage (its own affine refinement, then the warp).
antsApplyTransforms -d 3 -i "$INPUT" -r "$REF" -n "$INTERP" -o "$OUT" -t "$WARP" -t "$SYN" -t "$AFF"
