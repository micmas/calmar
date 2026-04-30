"""
neurosynth_bootstrap.py — generate draft KB entries from Neurosynth meta-analyses.

This is a Stage-2 helper. It is intentionally written as a *scaffold* rather
than a black box: it exposes the few decisions you need to make and emits
draft markdown files into `regions/` (or a sibling `regions_auto/` folder)
with `source: neurosynth_auto`.

The intended workflow is:

    python neurosynth_bootstrap.py \
        --terms naming fluency repetition "auditory comprehension" \
        --atlas /path/to/HarvardOxford-cort-maxprob-thr25-2mm.nii.gz \
        --labels-csv /path/to/HarvardOxford-cort-labels.csv \
        --out regions_auto

Each generated file is a *suggestion*. A clinician reviews each one and
either deletes it or moves it into `regions/`, flipping
`source: neurosynth_auto` to `source: curated`.

Dependencies (install only when you actually run this):
    pip install nimare pandas pyyaml nibabel numpy

We don't import any of these at module load — the imports are inside main()
so the rest of the KB tooling doesn't pull them in.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path


# ============================================================
# Term → impairment mapping
# (which KB impairment each Neurosynth term should generate findings for)
# ============================================================
TERM_TO_IMPAIRMENT = {
    "naming":                  "naming",
    "anomia":                  "naming",
    "speech production":       "fluency",
    "broca":                   "fluency",
    "fluency":                 "fluency",
    "repetition":              "repetition",
    "phonological":            "repetition",
    "auditory comprehension":  "auditory_comprehension",
    "wernicke":                "auditory_comprehension",
    "comprehension":           "auditory_comprehension",
}


# ============================================================
# Markdown emitter
# ============================================================
TEMPLATE = """---
id: {id_}
name: "{name}"
kind: atlas
atlas: "{atlas_name}"
atlas_index: {atlas_index}
hemisphere: {hemisphere}
aliases: []
networks: []
findings:
{findings}
source: neurosynth_auto
last_reviewed: {today}
notes: |
  Auto-generated from Neurosynth coordinate-based meta-analysis.
  Each finding is a SUGGESTION — review and either delete or promote
  to `source: curated` before clinical use.
---

# {name}

## Auto-generated from Neurosynth

Peaks for the following terms fell within this region:

{term_summary}

Replace this section with curated prose once an SLP / neurologist has
reviewed the findings above.
"""


def _emit_finding(target_imp: str, term: str, n_peaks: int, max_z: float) -> str:
    # Conservative defaults — Neurosynth associations alone aren't strong
    # enough for "strong" or "meta-analysis" labels.
    return (
        f"  - target: {target_imp}\n"
        f"    target_kind: impairment\n"
        f"    direction: likely\n"
        f"    strength: weak\n"
        f"    evidence_quality: tentative\n"
        f"    citation: \"@Neurosynth_{term.replace(' ', '_')}\"\n"
        f"    notes: \"{n_peaks} peak(s) intersect this region for term '{term}' "
        f"(max z={max_z:.2f}). Auto-generated; verify before use.\"\n"
    )


def _slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", s.lower()).strip("_")


# ============================================================
# Pipeline (skeleton — see TODOs)
# ============================================================
def run(terms, atlas_path, labels_csv, out_dir, hemisphere="left"):
    """
    Skeleton implementation. The TODOs below are intentional — running this
    requires choosing a Neurosynth client (NiMARE recommended) and downloading
    the dataset, which is too large/slow to embed by default.

    Steps:
      1. Load Neurosynth dataset via NiMARE: `nimare.extract.fetch_neurosynth(...)`
         then `nimare.io.convert_neurosynth_to_dataset(...)`.
      2. For each term in `terms`, run a meta-analysis (e.g. Chi-squared) to get
         a thresholded z-map of regions associated with the term.
      3. Resample the z-map to the atlas grid; for each atlas region, compute
         the max z and the count of supra-threshold peaks inside it.
      4. For each (region, term) pair with a non-trivial overlap, append one
         finding entry to a per-region draft markdown file using TEMPLATE.
    """
    import nibabel as nib              # noqa: F401  (intentional: surface ImportError early)
    import numpy as np                 # noqa: F401
    import pandas as pd                # noqa: F401

    print(f"Bootstrapping with terms: {terms}")
    print(f"Atlas:    {atlas_path}")
    print(f"Labels:   {labels_csv}")
    print(f"Out dir:  {out_dir}")

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # TODO 1: load Neurosynth via NiMARE -----------------------
    raise NotImplementedError(
        "Implement the NiMARE pipeline here. The TEMPLATE / _emit_finding "
        "helpers above are ready to be called once you have, for each "
        "(atlas region, term) pair, a peak count and max z-score.\n\n"
        "Skeleton:\n"
        "  from nimare.extract import fetch_neurosynth\n"
        "  from nimare.io import convert_neurosynth_to_dataset\n"
        "  from nimare.meta.cbma import MKDAChi2\n"
        "  ds_files = fetch_neurosynth(data_dir='./_neurosynth_cache')\n"
        "  ds = convert_neurosynth_to_dataset(ds_files['coordinates'][0],\n"
        "                                     ds_files['metadata'][0])\n"
        "  for term in terms:\n"
        "      sub_ids = ds.get_studies_by_label(f'terms_abstract_tfidf__{term}', 0.001)\n"
        "      meta = MKDAChi2().fit(ds.slice(sub_ids))\n"
        "      zmap = meta.results.get_map('z_desc-association')\n"
        "      # then resample to atlas grid, count peaks per region…"
    )


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--terms", nargs="+", required=True,
                   help="Neurosynth terms to query (e.g. naming fluency).")
    p.add_argument("--atlas", required=True,
                   help="Path to atlas .nii.gz (e.g. HarvardOxford).")
    p.add_argument("--labels-csv", required=True,
                   help="CSV with two columns: index,label (matching atlas).")
    p.add_argument("--out", default="regions_auto",
                   help="Output folder for draft .md files.")
    p.add_argument("--hemisphere", default="left",
                   help="left | right | bilateral (default: left).")
    args = p.parse_args(argv)

    # Validate terms have a known impairment mapping
    unknown = [t for t in args.terms if t.lower() not in TERM_TO_IMPAIRMENT]
    if unknown:
        print(f"  ⚠ unknown terms (no impairment mapping): {unknown}",
              file=sys.stderr)
        print(f"    add them to TERM_TO_IMPAIRMENT in this file first.",
              file=sys.stderr)
        sys.exit(2)

    run(args.terms, args.atlas, args.labels_csv, args.out, args.hemisphere)


if __name__ == "__main__":
    main()
