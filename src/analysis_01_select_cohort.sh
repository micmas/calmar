#!/bin/bash
# Select the ISLES-2022 benchmark cohort and write it to a TSV manifest.
#
# Usage:  bash src/analysis_01_select_cohort.sh <N>
#   N = 25  → seeded pilot sample (seed 31, same RNG scheme as the notebook's
#             sample(); the 2 subjects completed in the n=2 run are retained,
#             replacing sampled cases if necessary so the cohort stays n=25)
#   N = 250 → the full cohort (sampling is a no-op)
#
# Lightweight metadata-only selection — runs in the login shell, no module.
# Output: reports/benchmarks/cohort_isles2022_<N>.tsv (subject, session)

set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"
N="${1:?usage: analysis_01_select_cohort.sh <N subjects>}"
N_ID="n${N#n}"
FINAL="reports/benchmarks/cohort_isles2022_${N_ID}.tsv"
if [ -s "${FINAL}" ]; then
    EXPECTED="${N#n}"
    [ "$(wc -l < "${FINAL}")" -eq "${EXPECTED}" ] || {
        echo "${FINAL} exists for a different cohort size; preserve or remove it first" >&2
        exit 1
    }
    [ -s "${FINAL}.prov.json" ] || {
        echo "legacy cohort manifest exists without provenance: ${FINAL}" >&2
        exit 1
    }
    echo "cohort manifest already exists with provenance: ${FINAL}"
    exit 0
fi
mkdir -p reports/benchmarks
TMP="$(mktemp reports/benchmarks/.cohort_isles2022.attempt.XXXXXX.tsv)"
trap 'rm -f "${TMP}"' EXIT

python3 - "${N_ID}" "$TMP" <<'PY'
import random, sys
from pathlib import Path

# Accept "25" or an ASTRA option id like "n25".
n = int(sys.argv[1].lstrip("n"))
ds = Path("data/ISLES-2022")
entries = []
for sub_dir in sorted(p for p in ds.iterdir()
                      if p.is_dir() and p.name.startswith("sub-")):
    for ses_dir in sorted(p for p in sub_dir.iterdir()
                          if p.is_dir() and p.name.startswith("ses-")):
        dwi = sorted((ses_dir / "dwi").glob("*_dwi.nii.gz"))
        adc = sorted((ses_dir / "dwi").glob("*_adc.nii.gz"))
        msk = ds / "derivatives" / sub_dir.name / ses_dir.name / \
              f"{sub_dir.name}_{ses_dir.name}_msk.nii.gz"
        if dwi and adc and msk.exists():
            entries.append((sub_dir.name, ses_dir.name))

print(f"{len(entries)} subjects with DWI+ADC+expert mask")
if n > len(entries):
    raise RuntimeError(f"requested {n} subjects but only {len(entries)} are complete")
if n == len(entries):
    pick = entries
else:
    rng = random.Random(31)
    pick = set(rng.sample(entries, n))
    # Keep the two subjects completed in the earlier n=2 notebook run.
    for prior in [("sub-strokecase0004", "ses-0001"),
                  ("sub-strokecase0121", "ses-0001")]:
        if prior in entries:
            pick.add(prior)
    while len(pick) > n:
        removable = sorted(p for p in pick if p not in {
            ("sub-strokecase0004", "ses-0001"),
            ("sub-strokecase0121", "ses-0001"),
        })
        pick.remove(removable[-1])
    pick = sorted(pick)

out = Path(sys.argv[2])
out.write_text("".join(f"{s}\t{ses}\n" for s, ses in pick))
print(f"cohort of {len(pick)} prepared")
PY
[ -s "${TMP}" ] || { echo "cohort manifest is empty" >&2; exit 1; }
neurodesk-astra-provenance publish "${TMP}" "${FINAL}" \
    --output-id cohort_manifest --tool python3 --script "$0"
echo "cohort manifest → ${FINAL}"
