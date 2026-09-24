#!/usr/bin/env bash
# warp_native_to_mni.sh
#
# Apply ANTs transforms to a native-space lesion mask, producing the
# MNI-space version using LINDA 0.5.1 native→Penn→ch2 transforms.
# Reference must be Subject_in_MNI.nii.gz, not the intermediate Penn image.
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

# Always use the same LINDA package and bundled Penn→ch2 transforms as prediction.
source /opt/neurodesktop/agent_bash_env.sh
module load linda/0.5.1
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
R_SCRIPT="${PROJECT_DIR}/src/warp_native_mask_to_ch2.R"
LINDA_IMAGE="/cvmfs/neurodesk.ardc.edu.au/containers/linda_0.5.1_20260508/linda_0.5.1_20260508.simg"
SING_CMD="${SINGULARITY_CMD:-singularity}"
if ! command -v "$SING_CMD" >/dev/null 2>&1; then SING_CMD=apptainer; fi
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS="${SLURM_CPUS_PER_TASK:-4}"
TMP_DIR="$(mktemp -d "${OUT}.attempt.XXXXXX")"
trap 'rm -rf "$TMP_DIR"' EXIT
TMP="$TMP_DIR/$(basename "$OUT")"
"$SING_CMD" --silent exec --cleanenv \
    --env "ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=$ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS" \
    ${neurodesk_singularity_opts:-} --pwd "$PROJECT_DIR" "$LINDA_IMAGE" \
    R --vanilla --slave -f "$R_SCRIPT" --args \
    "$INPUT" "$REF" "$WARP" "$AFF" "$TMP" "$INTERP"
python -c 'import sys,nibabel as n,numpy as np; a,b=map(n.load,sys.argv[1:]); assert a.shape==b.shape and np.allclose(a.affine,b.affine); assert np.isfinite(a.get_fdata()).all()' "$TMP" "$REF"
REPLACE=()
if [ -e "$OUT" ]; then
    BACKUP_DIR="$(mktemp -d "${OUT}.previous.XXXXXX")"
    cp -p "$OUT" "$BACKUP_DIR/"
    if [ -f "${OUT}.prov.json" ]; then cp -p "${OUT}.prov.json" "$BACKUP_DIR/"; fi
    REPLACE=(--replace)
fi
neurodesk-astra-provenance publish "$TMP" "$OUT" \
    --output-id mni_mask --tool R --script "$0" "${REPLACE[@]}"
