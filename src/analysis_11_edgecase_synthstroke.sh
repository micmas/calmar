#!/bin/bash
#SBATCH --job-name=edge_synthstroke
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:45:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=4

# SynthStroke (T1w) across the whole edge-case battery — the fast tool
# (~15 s/subject), doubling as the worked example of an edge-case runner:
# a new tool's runner only needs to write
#   derivatives/segmentation-benchmark/synthetic_edgecases/<tool>/<sub>/...
# and analysis_12 will score it per category automatically.

if [ "${1:-}" = "--version" ]; then
    if [ "${CALMAR_PROVENANCE_COMPONENT:-synthstroke}" = "hdbet" ]; then
        echo "hd-bet 1.0.0 (CALMaR benchmark workflow)"
    else
        echo "synthstroke 0.0.0 (CALMaR benchmark workflow)"
    fi
    exit 0
fi

set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

PYBIN="$(command -v python3)"
PROVENANCE_TOOL="${PROJECT_DIR}/src/analysis_11_edgecase_synthstroke.sh"
PROFILE="${1:-historical_baseline}"
HDBET_MODE="${2:-fast}"
case "${PROFILE}" in
    historical_baseline) TOOL_TAG="synthstroke-${PROFILE}" ;;
    calmar_current) TOOL_TAG="synthstroke-${PROFILE}-hdbet-${HDBET_MODE}" ;;
    *) echo "usage: $0 {historical_baseline|calmar_current} {fast|accurate}" >&2; exit 2 ;;
esac
module load synthstroke/0.0.0
if [ "${PROFILE}" = calmar_current ]; then
    module load hdbet/1.0.0
fi

ATTEMPT=""
BRAIN_ATTEMPT=""
cleanup() {
    [ -z "${ATTEMPT}" ] || rm -rf "${ATTEMPT}"
    [ -z "${BRAIN_ATTEMPT}" ] || rm -rf "${BRAIN_ATTEMPT}"
}
trap cleanup EXIT

DS="data/synthetic_edgecases"
DERIV="derivatives/segmentation-benchmark/synthetic_edgecases"
fail=0
while IFS=$'\t' read -r SUB _phase _cat _vox; do
    [ "${SUB}" = "participant_id" ] && continue
    T1="${DS}/${SUB}/anat/${SUB}_T1w.nii.gz"
    WORK="${DERIV}/${TOOL_TAG}/${SUB}/anat"
    BIDS_MASK="${WORK}/${SUB}_space-T1w_desc-lesion_mask.nii.gz"
    echo "── ${SUB} (${PROFILE}; hd-bet=${HDBET_MODE})"
    [ -s "${T1}" ] || { echo "  T1w missing → FAIL"; fail=1; continue; }
    if [ -e "${BIDS_MASK}" ]; then
        if [ -s "${BIDS_MASK}" ] && [ -s "${BIDS_MASK}.prov.json" ]; then
            echo "  cached with provenance ✔"; continue
        fi
        echo "  legacy or incomplete mask exists: ${BIDS_MASK}"; fail=1; continue
    fi
    mkdir -p "${WORK}" "${DERIV}"
    BRAIN_MASK=""
    if [ "${PROFILE}" = calmar_current ]; then
        WEIGHTS="data/models/synthstroke-synth-plus/model.safetensors"
        [ -s "${WEIGHTS}" ] || { echo "  synth-plus weights missing: ${WEIGHTS}"; fail=1; continue; }
        BRAIN_DIR="${WORK}/preproc-hdbet-${HDBET_MODE}"
        BRAIN_MASK="${BRAIN_DIR}/${SUB}_T1w_brain_mask.nii.gz"
        if [ -e "${BRAIN_MASK}" ] && [ ! -s "${BRAIN_MASK}.prov.json" ]; then
            echo "  legacy HD-BET mask exists without provenance: ${BRAIN_MASK}"; fail=1; continue
        fi
        if [ ! -s "${BRAIN_MASK}" ]; then
            mkdir -p "${BRAIN_DIR}"
            BRAIN_ATTEMPT="$(mktemp -d "${DERIV}/.hdbet-${SUB}.attempt.XXXXXX")"
            if ! hd-bet -i "${T1}" -o "${BRAIN_ATTEMPT}/${SUB}_T1w_brain.nii.gz" \
                -mode "${HDBET_MODE}" -device cpu -tta 0; then
                rm -rf "${BRAIN_ATTEMPT}"; BRAIN_ATTEMPT=""
                echo "  HD-BET FAILED"; fail=1; continue
            fi
            BRAIN_TMP="${BRAIN_ATTEMPT}/${SUB}_T1w_brain_mask.nii.gz"
            if [ ! -s "${BRAIN_TMP}" ]; then
                rm -rf "${BRAIN_ATTEMPT}"; BRAIN_ATTEMPT=""
                echo "  HD-BET produced no mask"; fail=1; continue
            fi
            if ! CALMAR_PROVENANCE_COMPONENT=hdbet \
                neurodesk-astra-provenance publish "${BRAIN_TMP}" "${BRAIN_MASK}" \
                    --output-id edgecase_synthstroke_brain_masks \
                    --tool "${PROVENANCE_TOOL}" --script "$0"; then
                rm -rf "${BRAIN_ATTEMPT}"; BRAIN_ATTEMPT=""
                echo "  HD-BET publication FAILED"; fail=1; continue
            fi
            rm -rf "${BRAIN_ATTEMPT}"
            BRAIN_ATTEMPT=""
        fi
    fi
    ATTEMPT="$(mktemp -d "${DERIV}/.synthstroke-${SUB}.attempt.XXXXXX")"
    SYNTH_ARGS=(--input "${T1}" --outdir "${ATTEMPT}")
    if [ "${PROFILE}" = calmar_current ]; then
        SYNTH_ARGS+=(--weights "${WEIGHTS}" --tta)
    fi
    if ! synthstroke "${SYNTH_ARGS[@]}"; then
        rm -rf "${ATTEMPT}"
        ATTEMPT=""
        echo "  synthstroke FAILED"; fail=1; continue
    fi
    PRED="${ATTEMPT}/prediction_lesion_mask.nii.gz"
    if [ ! -s "${PRED}" ]; then
        rm -rf "${ATTEMPT}"
        ATTEMPT=""
        echo "  expected output missing"; fail=1; continue
    fi
    if ! "${PYBIN}" - "${PRED}" "${BRAIN_MASK}" <<'PY'
import sys
import nibabel as nib
import numpy as np
if sys.argv[2]:
    from calmar.qc import mask_prediction_to_brain
    result = mask_prediction_to_brain(sys.argv[1], sys.argv[2])
    assert result is not None
img = nib.load(sys.argv[1])
data = np.asarray(img.dataobj)
assert data.ndim == 3 and np.isfinite(data).all()
assert int((data > 0).sum()) < data.size // 2
PY
    then
        rm -rf "${ATTEMPT}"; ATTEMPT=""
        echo "  SynthStroke validation FAILED"; fail=1; continue
    fi
    if ! neurodesk-astra-provenance publish "${PRED}" "${BIDS_MASK}" \
        --output-id edgecase_synthstroke_masks \
        --tool "${PROVENANCE_TOOL}" --script "$0"; then
        rm -rf "${ATTEMPT}"; ATTEMPT=""
        echo "  SynthStroke publication FAILED"; fail=1; continue
    fi
    rm -rf "${ATTEMPT}"
    ATTEMPT=""
    echo "  saved ✔"
done < "${DS}/participants.tsv"
exit "${fail}"
