#!/bin/bash
#SBATCH --job-name=calmar_notebook_verify
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:30:00
#SBATCH --mem=6G
#SBATCH --cpus-per-task=2
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
cd "${SLURM_SUBMIT_DIR:-$PWD}"
# Static publication and browser checks only. Never invokes analysis code.
python -m pytest -q tests/test_demo_publication.py tests/test_demo_reader.py tests/test_notebook_first.py
node src/web/demo/verify_notebook_first.cjs "${1:?bundle}" "${2:?verification output}"
# Verify that the native brain-mask screenshot contains the intended yellow
# overlay, not Niivue's silent grayscale fallback for unknown colour names.
python - "$2/inline-native.png" <<'PY'
import sys
from PIL import Image
pixels = Image.open(sys.argv[1]).convert('RGB').getdata()
yellow = sum(r > 100 and g > 100 and b < .75 * min(r, g) for r, g, b in pixels)
assert yellow > 500, f'Missing rendered yellow overlay: {yellow} pixels'
print(f'Validated coloured overlay: {yellow} yellow pixels')
PY
