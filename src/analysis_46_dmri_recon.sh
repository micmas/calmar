#!/bin/bash
#SBATCH --job-name=calmar_dmri_recon
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=12:00:00
#SBATCH --mem=48G
#SBATCH --cpus-per-task=8
# Selected direct-dMRI reconstruction from the published QSIPrep derivative:
# QSIRecon bundles/tractometry or DIPY weighted-least-squares DTI maps. Reports
# keep the two methods distinct and never call a missing bundle disconnection.
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"
export CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
REQUEST="${1:?request JSON required}"
FINAL="${2:?result directory required}"
shift 2
DMRI_METHOD="${CALMAR_DMRI_METHOD:-$("${CALMAR_PYTHON}" -c \
    'import json,sys; print(json.load(open(sys.argv[1]))["config"].get("DMRI_METHOD", "qsirecon"))' \
    "${REQUEST}")}"
export CALMAR_DMRI_METHOD="${DMRI_METHOD}"
export CALMAR_DIPY_VERSION=1.12.1
export CALMAR_EXECUTION_SCRIPT="$0"
export PYTHONPATH="${PROJECT_DIR}${PYTHONPATH:+:${PYTHONPATH}}"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}"
export OPENBLAS_NUM_THREADS=1
case "${DMRI_METHOD}" in
    qsirecon)
        module load qsirecon/26.0.1
        export FS_LICENSE="${FS_LICENSE:-/home/jovyan/license.txt}"
        test -f "${FS_LICENSE}"
        export APPTAINERENV_FS_LICENSE="${FS_LICENSE}"
        export SINGULARITYENV_FS_LICENSE="${FS_LICENSE}"
        for variable in OMP_NUM_THREADS OPENBLAS_NUM_THREADS; do
            export "APPTAINERENV_${variable}=${!variable}"
            export "SINGULARITYENV_${variable}=${!variable}"
        done
        ;;
    dipy_dti)
        # No DIPY Neurodesk module is installed. Use the pinned host package;
        # the Python entry point verifies the CLI reports exactly 1.12.1.
        command -v dipy_fit_dti >/dev/null
        ;;
    *)
        echo "Unsupported DMRI_METHOD: ${DMRI_METHOD}" >&2
        exit 2
        ;;
esac
for dependency in "$@"; do test -f "${dependency}/summary.json"; done
"${CALMAR_PYTHON}" -m calmar.dmri_pipeline dmri_recon "${REQUEST}" "${FINAL}"
