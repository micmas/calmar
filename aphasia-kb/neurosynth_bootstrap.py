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
def run(terms, atlas_path, labels_csv, out_dir, hemisphere="left",
        neurosynth_cache=None, tfidf_threshold=0.001):
    """Generate draft KB region entries from Neurosynth coordinate-based meta-analysis.

    Implements the formerly-stub pipeline using the lightweight coordinate-binning
    approach in ``decode_lesion.py`` (no NiMARE Dataset object constructed; avoids
    OOM on memory-constrained machines). Downloads Neurosynth v7 files (~14.7 MB)
    on first run and caches them.

    For each (atlas region, term) pair with meaningful overlap the function emits
    a draft ``.md`` file under ``out_dir/`` using the TEMPLATE above.  Each draft
    should be reviewed by a clinician before promotion to ``regions/``.

    Parameters
    ----------
    terms : list of str
        Neurosynth vocabulary terms to query.
    atlas_path : str
        Path to a 3-D atlas NIfTI (integer labels).  Ignored if ``labels_csv``
        is provided alongside nilearn's HarvardOxford atlas (recommended).
    labels_csv : str
        CSV with columns ``index,label`` matching the atlas NIfTI label integers.
    out_dir : str
        Output folder for draft ``.md`` files (will be created).
    hemisphere : str
        ``"left"`` (default) | ``"right"`` | ``"bilateral"``.
        Filters output to regions in the specified hemisphere.
    neurosynth_cache : str, optional
        Directory for Neurosynth v7 files.  Defaults to
        ``<this file's parent>/_neurosynth_cache``.
    tfidf_threshold : float
        Minimum tfidf weight for a study to be included in a term's activation map.
    """
    import nibabel as nib
    import numpy as np
    import pandas as pd
    import scipy.sparse as sp
    from scipy.ndimage import gaussian_filter
    from pathlib import Path as _Path

    here = _Path(__file__).parent
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))

    from decode_lesion import (
        ensure_neurosynth_files, _load_neurosynth,
        _mni_to_vox, build_term_map,
    )

    print(f"Bootstrap: terms={terms}, hemisphere={hemisphere}")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── Load Neurosynth files ────────────────────────────────────────────
    cache = ensure_neurosynth_files(neurosynth_cache)
    vocab, feat, meta_df, coords_ns = _load_neurosynth(cache)
    missing = [t for t in terms if t not in vocab]
    if missing:
        print(f"  ⚠ Terms not in vocabulary (skipped): {missing}", file=sys.stderr)
    terms = [t for t in terms if t in vocab]

    # ── Load atlas ───────────────────────────────────────────────────────
    atlas_img   = nib.load(atlas_path)
    atlas_data  = atlas_img.get_fdata().astype(np.int16)
    affine      = atlas_img.affine
    inv_affine  = np.linalg.inv(affine)
    shape       = atlas_img.shape[:3]

    labels_df   = pd.read_csv(labels_csv)
    label_map   = dict(zip(labels_df.iloc[:, 0], labels_df.iloc[:, 1]))

    # ── Build activation maps and find atlas overlaps ────────────────────
    term_map_dir = str(_Path(cache) / "term_maps")
    today        = dt.date.today().isoformat()
    written      = 0

    for term in terms:
        print(f"  Processing term: '{term}' …")
        tmap = build_term_map(
            term, vocab, feat, meta_df, coords_ns,
            inv_affine, shape,
            tfidf_threshold=tfidf_threshold,
            term_map_cache_dir=term_map_dir,
        )

        target_imp = TERM_TO_IMPAIRMENT.get(term.lower(), _slugify(term))

        # Collect per-region stats
        for label_idx, label_name in label_map.items():
            region_mask = atlas_data == int(label_idx)
            if not region_mask.any():
                continue

            # Hemisphere filter
            overlap_vox = np.argwhere(region_mask)
            mni_x = overlap_vox[:, 0] * affine[0, 0] + affine[0, 3]
            mean_x = mni_x.mean()
            if hemisphere == "left"  and mean_x >= 0:
                continue
            if hemisphere == "right" and mean_x <= 0:
                continue

            region_vals = tmap[region_mask]
            n_peaks     = int((region_vals > 0.01).sum())
            max_z       = float(region_vals.max())

            if n_peaks < 3 or max_z < 0.05:
                continue

            # Emit draft file
            id_  = f"{hemisphere}_{_slugify(label_name)}"
            fname = out_dir / f"{id_}.md"

            finding_str = _emit_finding(target_imp, term, n_peaks, max_z)
            term_summary = f"- **{term}**: {n_peaks} supra-threshold voxels, max z={max_z:.2f}"

            with open(fname, "a") as fh:
                if fname.stat().st_size == 0 if fname.exists() else True:
                    fh.write(TEMPLATE.format(
                        id_=id_,
                        name=f"{label_name} ({hemisphere.title()})",
                        atlas_name=Path(atlas_path).stem,
                        atlas_index=label_idx,
                        hemisphere=hemisphere,
                        findings=finding_str,
                        term_summary=term_summary,
                        today=today,
                    ))
                else:
                    # Append finding to existing file
                    fh.write(finding_str)
            written += 1

    print(f"Done. Wrote {written} draft finding entries to {out_dir}/")


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
