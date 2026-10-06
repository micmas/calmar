#!/bin/bash
# Select the ISLES-2022 benchmark cohort and write it to a TSV manifest.
#
# Usage:  bash src/analysis_01_select_cohort.sh <N>
#   N = 25  → seeded pilot sample (seed 31, same RNG scheme as the notebook's
#             sample(), union of the 2 subjects already completed in the n=2 run
#             so their cached results stay comparable)
#   N = 250 → the full cohort (sampling is a no-op)
#
# Lightweight metadata-only selection — runs in the login shell, no module.
# Output: reports/benchmarks/cohort_isles2022.tsv  (columns: subject  session)

set -euo pipefail
N="${1:?usage: analysis_01_select_cohort.sh <N subjects>}"

python3 - "$N" <<'PY'
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
if n >= len(entries):
    pick = entries
else:
    rng = random.Random(31)
    pick = set(rng.sample(entries, n))
    # Keep the two subjects completed in the earlier n=2 notebook run.
    for prior in [("sub-strokecase0004", "ses-0001"),
                  ("sub-strokecase0121", "ses-0001")]:
        if prior in entries:
            pick.add(prior)
    pick = sorted(pick)

out = Path("reports/benchmarks/cohort_isles2022.tsv")
out.parent.mkdir(parents=True, exist_ok=True)
tmp = out.with_suffix(".tsv.tmp")
tmp.write_text("".join(f"{s}\t{ses}\n" for s, ses in pick))
tmp.rename(out)
print(f"cohort of {len(pick)} → {out}")
PY
