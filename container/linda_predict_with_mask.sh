#!/usr/bin/env bash
# linda_predict_with_mask.sh — IN-CONTAINER entrypoint
#
# Ships INSIDE the LINDA Neurodesk container, alongside linda_predict.sh.
# Neurodesk's transparent-singularity layer auto-generates a host-side
# wrapper at /cvmfs/.../linda_<ver>_<date>/linda_predict_with_mask.sh
# so users can call this exactly the same way as linda_predict.sh.
#
# What it does:
#   Calls linda_predict() in R with a pre-computed brain_mask, which
#   bypasses LINDA's internal n4_skull_strip(). Useful for stroke
#   patients where template-based brain extraction over-strips cortex
#   near the lesion. Pass HD-BET's mask and LINDA will use it as-is.
#
# Usage (from the host, via Neurodesk wrapper):
#   linda_predict_with_mask.sh \
#       --t1     /path/to/T1w.nii.gz       \
#       --mask   /path/to/brain_mask.nii.gz \
#       --outdir /path/to/linda_out
#
# Optional flags: --quiet | --verbose (default) | --no-cache

set -euo pipefail

# Where the R stub was installed in the container. Adjust to wherever
# you put it during container build.
R_STUB="${LINDA_MASK_R_STUB:-/usr/local/share/LINDA/linda_predict_with_mask.R}"

if [[ ! -f "$R_STUB" ]]; then
    echo "ERROR: R stub not found at $R_STUB" >&2
    echo "  Set LINDA_MASK_R_STUB env var or fix the install path." >&2
    exit 1
fi

if ! command -v Rscript >/dev/null 2>&1; then
    echo "ERROR: Rscript not on PATH inside the container." >&2
    exit 1
fi

exec Rscript "$R_STUB" "$@"
