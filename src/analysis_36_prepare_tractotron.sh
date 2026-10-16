#!/bin/bash
# Run inside the allocation of analysis_27_bcb.sh.
set -euo pipefail
test -n "${SLURM_JOB_ID:-}"
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
# The parent's FSL module puts a container Python wrapper on PATH. Keep the
# host interpreter captured before loading modules in analysis_27_bcb.sh.
CALMAR_PYTHON="${CALMAR_PYTHON:?host Python must be provided by analysis_27_bcb.sh}"
module load bcbtoolkit/0.0.0
MASK="${1:?MNI lesion required}"
OUTPUT="${2:?prepared lesion path required}"
ATLAS="${3:?container atlas directory required}"
# The atlas lives inside the container. Copy its actual reference geometry;
# choosing a voxel size alone does not establish a matching image grid.
WRAPPER_DIR="$(dirname "$(readlink -f "$(command -v tractotron_cli.sh)")")"
source "$WRAPPER_DIR/container_runtime.sh"
REFERENCE="$(dirname "$OUTPUT")/../tract_reference.nii.gz"
neurodesk_container exec "$WRAPPER_DIR/bcbtoolkit_0.0.0_20260610.simg" \
    cp "$ATLAS/Arcuate_Fasciculus_L.nii.gz" "$REFERENCE"
"$CALMAR_PYTHON" src/python/prepare_tractotron.py "$MASK" "$REFERENCE" "$OUTPUT"
