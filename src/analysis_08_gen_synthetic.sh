#!/bin/bash
#SBATCH --job-name=gen_synthetic
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:20:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=2

# Generation record for the synthetic stroke phantom datasets (seed 7, n=6
# per phase), reproducing exactly what lesion-segmentation-benchmark.ipynb §4
# ran. Pass acute or chronic to materialize one independently; the default
# "both" retains the notebook-era entry point.
# Uses main-env python (nilearn fetches the MNI152 template on first run);
# no neuroimaging module needed.

set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

PHASE="${1:-both}"
case "${PHASE}" in
    acute) PHASES=(acute) ;;
    chronic) PHASES=(chronic) ;;
    both) PHASES=(acute chronic) ;;
    *) echo "usage: $0 {acute|chronic|both}" >&2; exit 2 ;;
esac

mkdir -p data
TMP_ROOT="$(mktemp -d data/.synthetic-base.attempt.XXXXXX)"
trap 'rm -rf "${TMP_ROOT}"' EXIT

for CURRENT_PHASE in "${PHASES[@]}"; do
    FINAL="data/synthetic_${CURRENT_PHASE}"
    if [ -e "${FINAL}" ]; then
        [ -d "${FINAL}" ] && [ -s "${FINAL}.prov.json" ] || {
            echo "legacy or incomplete synthetic dataset: ${FINAL}" >&2
            exit 1
        }
        echo "synthetic ${CURRENT_PHASE} dataset already exists with provenance"
        continue
    fi
    TMP_DATA="${TMP_ROOT}/${CURRENT_PHASE}"
    python3 - "${TMP_DATA}" "${CURRENT_PHASE}" <<'PY'
import sys
sys.path.insert(0, ".")
from calmar.synthetic import synthetic_install

ok = synthetic_install(sys.argv[1], n_subjects=6, seed=7,
                       phase=sys.argv[2])
sys.exit(0 if ok else 1)
PY
    [ "$(find "${TMP_DATA}" -maxdepth 1 -name 'sub-*' | wc -l)" -eq 6 ]
    neurodesk-astra-provenance publish "${TMP_DATA}" "${FINAL}" \
        --output-id "synthetic_${CURRENT_PHASE}_dataset" \
        --tool python3 --script "$0"
done
