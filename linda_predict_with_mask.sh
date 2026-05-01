#!/usr/bin/env bash
# linda_predict_with_mask.sh
#
# Bash wrapper that runs linda_predict_with_mask.R inside the same
# environment that LINDA itself runs in. On Neurodesk, R + LINDA are
# only available *inside* the LINDA singularity container — the bare
# `Rscript` command is not on PATH from the notebook's conda kernel.
#
# Strategy:
#   1. If `Rscript` is on PATH on the host → run the R stub directly
#      (works on machines where R is installed natively).
#   2. Else, find the LINDA `.simg` container by parsing the
#      `linda_predict.sh` wrapper Neurodesk ships, then run our R stub
#      via `singularity exec <simg> Rscript ...` — exactly the same
#      dance the LINDA wrapper does.
#
# Override knobs (env vars):
#   LINDA_SIMG   — path to the LINDA singularity container (.simg).
#                  Auto-detected from `linda_predict.sh` if unset.
#   SINGULARITY_CMD — singularity / apptainer binary (default:
#                     `singularity`).
#
# Args are passed straight through to the R stub (--t1, --mask,
# --outdir, --quiet, --no-cache).
#
# Exit codes mirror the R stub's:
#   0 success | 1 arg error | 2 LINDA pkg missing
#   3 input file missing | 4 linda_predict() raised

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R_STUB="$SCRIPT_DIR/linda_predict_with_mask.R"

if [[ ! -f "$R_STUB" ]]; then
    echo "ERROR: R stub not found at $R_STUB" >&2
    exit 1
fi

# ---------- 1. host Rscript? ----------
if command -v Rscript >/dev/null 2>&1; then
    echo "[linda_predict_with_mask.sh] Using host Rscript: $(command -v Rscript)"
    exec Rscript "$R_STUB" "$@"
fi

# ---------- 2. dispatch through the LINDA singularity container ----------
SING_CMD="${SINGULARITY_CMD:-singularity}"
if ! command -v "$SING_CMD" >/dev/null 2>&1; then
    # Try `apptainer` as fallback — many newer Neurodesk builds use it.
    if command -v apptainer >/dev/null 2>&1; then
        SING_CMD="apptainer"
    else
        echo "ERROR: neither host Rscript nor singularity/apptainer is on PATH." >&2
        echo "  Install R, or load a Neurodesk module that provides singularity." >&2
        exit 1
    fi
fi

# Auto-detect the .simg path from the linda_predict.sh wrapper if the
# user hasn't pinned it via $LINDA_SIMG.
if [[ -z "${LINDA_SIMG:-}" ]]; then
    LINDA_WRAPPER="$(command -v linda_predict.sh 2>/dev/null || true)"
    if [[ -z "$LINDA_WRAPPER" ]]; then
        echo "ERROR: linda_predict.sh not on PATH — can't auto-detect LINDA container." >&2
        echo "  Either set LINDA_SIMG=/path/to/linda_*.simg, or install/load LINDA." >&2
        exit 1
    fi
    # Pull out the first .simg / .sif path that appears in the wrapper.
    LINDA_SIMG="$(grep -oE '/[^ ]*\.(simg|sif)' "$LINDA_WRAPPER" | head -1 || true)"
fi

if [[ -z "$LINDA_SIMG" || ! -f "$LINDA_SIMG" ]]; then
    echo "ERROR: LINDA container not found at: '${LINDA_SIMG:-<unset>}'" >&2
    echo "  Set LINDA_SIMG to the absolute path of the LINDA .simg / .sif file." >&2
    exit 1
fi

echo "[linda_predict_with_mask.sh] Dispatching via $SING_CMD into:"
echo "[linda_predict_with_mask.sh]   $LINDA_SIMG"

# Mirror the linda_predict.sh invocation (--silent --cleanenv --env DISPLAY
# --pwd $PWD) so our R stub sees the same mounted filesystems and env.
export PWD="$(pwd -P)"
exec "$SING_CMD" --silent exec --cleanenv \
    --env DISPLAY="${DISPLAY:-}" \
    ${neurodesk_singularity_opts:-} \
    --pwd "$PWD" \
    "$LINDA_SIMG" \
    Rscript "$R_STUB" "$@"
