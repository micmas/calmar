#!/usr/bin/env bash
# Compatibility entry point; the retained analytical step lives under src/.
set -euo pipefail
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
exec bash "$PROJECT_DIR/src/analysis_15_warp_native_to_mni.sh" "$@"
