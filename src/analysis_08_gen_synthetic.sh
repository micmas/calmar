#!/bin/bash
#SBATCH --job-name=gen_synthetic
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:20:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=2

# Generation record for the synthetic stroke phantom datasets (seed 7, n=6
# per phase), reproducing exactly what lesion-segmentation-benchmark.ipynb §4
# ran. Idempotent: synthetic_install() skips phases whose subjects already
# exist, so this is a no-op while the current datasets are present.
# Uses main-env python (nilearn fetches the MNI152 template on first run);
# no neuroimaging module needed.

set -euo pipefail

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

python3 - <<'PY'
import sys
sys.path.insert(0, ".")
from calmar.synthetic import synthetic_install

ok = True
ok &= synthetic_install("data/synthetic_acute",   n_subjects=6, seed=7,
                        phase="acute")
ok &= synthetic_install("data/synthetic_chronic", n_subjects=6, seed=7,
                        phase="chronic")
sys.exit(0 if ok else 1)
PY
