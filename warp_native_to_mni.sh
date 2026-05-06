#!/usr/bin/env bash
# warp_native_to_mni.sh
#
# Apply ANTs transforms to a native-space lesion mask, producing the
# MNI-space version. Mirrors the linda_predict_with_mask.sh dispatch
# pattern: prefer host antsApplyTransforms if available, else run via
# `singularity exec <linda.simg> antsApplyTransforms ...`.
#
# Usage:
#   warp_native_to_mni.sh \
#       --input    /path/to/Prediction3_native.nii.gz \
#       --reference /path/to/template_in_MNI.nii.gz   \
#       --warp     /path/to/Reg3_sub_to_template_warp.nii.gz \
#       --affine   /path/to/Reg3_sub_to_template_affine.mat  \
#       --output   /path/to/Lesion_in_MNI.nii.gz \
#       [--interp NearestNeighbor]   # default; preserves binary masks

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
        -h|--help)
            echo "Usage: $0 --input <native.nii.gz> --reference <template.nii.gz>"
            echo "          --warp <warp.nii.gz> --affine <affine.mat> --output <out.nii.gz>"
            echo "          [--interp NearestNeighbor]"
            exit 0 ;;
        *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
done

[ -z "$INPUT" ] || [ -z "$REF" ] || [ -z "$WARP" ] || [ -z "$AFF" ] || [ -z "$OUT" ] && {
    echo "Need --input, --reference, --warp, --affine, --output" >&2; exit 1; }
[ -f "$INPUT" ] || { echo "Input not found: $INPUT" >&2; exit 3; }
[ -f "$REF" ]   || { echo "Reference not found: $REF" >&2; exit 3; }
[ -f "$WARP" ]  || { echo "Warp not found: $WARP" >&2; exit 3; }
[ -f "$AFF" ]   || { echo "Affine not found: $AFF" >&2; exit 3; }
mkdir -p "$(dirname "$OUT")"

ANTS_CMD=(
    antsApplyTransforms -d 3
    -i "$INPUT" -r "$REF" -o "$OUT"
    -n "$INTERP"
    -t "$WARP" -t "$AFF"
)

# 1. Host antsApplyTransforms?
if command -v antsApplyTransforms >/dev/null 2>&1; then
    echo "[warp_native_to_mni] Using host antsApplyTransforms"
    exec "${ANTS_CMD[@]}"
fi

# 2. Dispatch through the LINDA singularity container
SING_CMD="${SINGULARITY_CMD:-singularity}"
if ! command -v "$SING_CMD" >/dev/null 2>&1; then
    if command -v apptainer >/dev/null 2>&1; then SING_CMD=apptainer
    else
        echo "ERROR: neither host antsApplyTransforms nor singularity is available" >&2
        exit 1
    fi
fi

if [[ -z "${LINDA_SIMG:-}" ]]; then
    LINDA_WRAPPER="$(command -v linda_predict.sh 2>/dev/null || true)"
    if [[ -n "$LINDA_WRAPPER" ]]; then
        LINDA_SIMG="$(grep -oE '/[^ ]*\.(simg|sif)' "$LINDA_WRAPPER" | head -1 || true)"
    fi
fi
if [[ -z "$LINDA_SIMG" ]]; then
    echo "ERROR: cannot find LINDA container — set LINDA_SIMG env var" >&2
    exit 1
fi

echo "[warp_native_to_mni] Dispatching via $SING_CMD into:"
echo "[warp_native_to_mni]   $LINDA_SIMG"
export PWD="$(pwd -P)"
exec "$SING_CMD" --silent exec --cleanenv \
    --env DISPLAY="${DISPLAY:-}" \
    ${neurodesk_singularity_opts:-} \
    --pwd "$PWD" \
    "$LINDA_SIMG" \
    "${ANTS_CMD[@]}"
