"""
decode_lesion.py — lightweight Neurosynth decoding for aphasia lesion masks.

No NiMARE Dataset object is constructed (avoids OOM on memory-constrained
machines). Instead the Neurosynth v7 coordinate + tfidf files are read
directly, term activation maps are built via voxel binning + Gaussian
smoothing, and the lesion mask is correlated (Pearson r) with each map.

HarvardOxford cortical atlas overlap is computed in parallel to give a
deterministic region-level summary.

Usage (standalone)
------------------
    python decode_lesion.py /path/to/lesion_mni.nii.gz

Usage (programmatic)
--------------------
    from decode_lesion import decode_lesion
    result = decode_lesion("/path/to/lesion.nii.gz")
    print(result["term_decoding"])
    print(result["region_overlap"])

Dependencies (all already in requirements.txt)
-----------------------------------------------
    nibabel, nilearn, numpy, pandas, scipy, scikit-learn
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional

import nibabel as nib
import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy.ndimage import gaussian_filter
from scipy.stats import pearsonr

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Neurosynth download config
# ---------------------------------------------------------------------------
_NS_BASE_URL = (
    "https://github.com/neurosynth/neurosynth-data/raw/"
    "209c33cd009d0b069398a802198b41b9c488b9b7/"
)
_NS_FILES = [
    "data-neurosynth_version-7_coordinates.tsv.gz",
    "data-neurosynth_version-7_metadata.tsv.gz",
    "data-neurosynth_version-7_vocab-terms_source-abstract_type-tfidf_features.npz",
    "data-neurosynth_version-7_vocab-terms_vocabulary.txt",
]

# Language / cognitive terms to decode against (subset of 3228-term vocabulary)
DEFAULT_TERMS = [
    "naming",
    "anomia",
    "aphasia",
    "fluency",
    "verbal fluency",
    "language",
    "language comprehension",
    "speech",
    "speech production",
    "repetition",
    "repetition suppression",
    "comprehension",
    "sentence comprehension",
    "reading",
    "writing",
    "broca",
    "syntax",
    "phonological",
    "semantic",
    "working memory",
]

# Map Neurosynth terms → KB impairment IDs
TERM_TO_IMPAIRMENT = {
    "naming":               "naming",
    "anomia":               "naming",
    "aphasia":              None,        # broad; don't map to a single impairment
    "fluency":              "fluency",
    "verbal fluency":       "fluency",
    "language":             None,
    "language comprehension": "auditory_comprehension",
    "speech":               "fluency",
    "speech production":    "fluency",
    "repetition":           "repetition",
    "repetition suppression": "repetition",
    "comprehension":        "auditory_comprehension",
    "sentence comprehension": "auditory_comprehension",
    "reading":              "reading",
    "writing":              "writing",
    "broca":                "fluency",
    "syntax":               "syntax",
    "phonological":         "phonological_processing",
    "semantic":             "form_to_meaning",
    "working memory":       None,
}

# HarvardOxford label → KB region ID  (left hemisphere only;
# hemisphere is inferred from lesion centroid or overlap voxel x-coordinate)
HO_LABEL_TO_KB_REGION = {
    "Inferior Frontal Gyrus, pars triangularis": "left_ifg_pars_triangularis",
    "Inferior Frontal Gyrus, pars opercularis":  "left_ifg_pars_opercularis",
    "Superior Temporal Gyrus, anterior division": "left_superior_temporal_gyrus",
    "Superior Temporal Gyrus, posterior division": "left_posterior_stg",
    "Middle Temporal Gyrus, posterior division":  "left_middle_temporal_gyrus",
    "Middle Temporal Gyrus, anterior division":   "left_middle_temporal_gyrus",
    "Angular Gyrus":                              "left_angular_gyrus",
    "Supramarginal Gyrus, anterior division":     "left_supramarginal_gyrus_premotor",
    "Supramarginal Gyrus, posterior division":    "left_supramarginal_gyrus_premotor",
    "Precentral Gyrus":                           "left_precentral_gyrus",
    "Frontal Opercular Cortex":                   "left_ifg_pars_opercularis",
    "Parietal Opercular Cortex":                  "left_supramarginal_gyrus_premotor",
    "Planum Temporale":                           "left_posterior_stg",
    "Heschl's Gyrus (includes H1 and H2)":        "left_superior_temporal_gyrus",
    "Planum Polare":                              "left_superior_temporal_gyrus",
}


# ---------------------------------------------------------------------------
# Neurosynth file management
# ---------------------------------------------------------------------------

def _default_cache() -> str:
    """Return the default Neurosynth cache directory (next to this file)."""
    here = Path(__file__).parent
    return str(here / "_neurosynth_cache")


def ensure_neurosynth_files(cache_dir: Optional[str] = None) -> str:
    """Download Neurosynth v7 files if not already present. Returns cache path."""
    import urllib.request

    cache = Path(cache_dir or _default_cache())
    cache.mkdir(parents=True, exist_ok=True)

    for fname in _NS_FILES:
        dest = cache / fname
        if not dest.exists():
            url = _NS_BASE_URL + fname
            logger.info("Downloading %s → %s", fname, dest)
            print(f"  Downloading {fname} (~{_file_size_hint(fname)}) …")
            try:
                urllib.request.urlretrieve(url, str(dest))
            except Exception as exc:
                raise RuntimeError(
                    f"Failed to download {fname} from {url}: {exc}\n"
                    "Check your internet connection."
                ) from exc

    return str(cache)


def _file_size_hint(fname: str) -> str:
    sizes = {
        "coordinates": "3.6 MB",
        "metadata": "1.2 MB",
        "features.npz": "9.9 MB",
        "vocabulary": "< 0.1 MB",
    }
    for k, v in sizes.items():
        if k in fname:
            return v
    return "?"


# ---------------------------------------------------------------------------
# Neurosynth data loaders (lazy, cached in module globals)
# ---------------------------------------------------------------------------

_NS_CACHE: dict = {}


def _load_neurosynth(cache_dir: str) -> tuple:
    """Load vocabulary, feature matrix, metadata, and coordinates.
    Results are cached in module-level _NS_CACHE after first load."""
    key = str(cache_dir)
    if key in _NS_CACHE:
        return _NS_CACHE[key]

    c = Path(cache_dir)
    with open(c / "data-neurosynth_version-7_vocab-terms_vocabulary.txt") as f:
        vocab = [l.strip() for l in f]

    feat = sp.load_npz(
        str(c / "data-neurosynth_version-7_vocab-terms_source-abstract_type-tfidf_features.npz")
    )
    meta = pd.read_csv(
        str(c / "data-neurosynth_version-7_metadata.tsv.gz"), sep="\t"
    )
    coords = pd.read_csv(
        str(c / "data-neurosynth_version-7_coordinates.tsv.gz"), sep="\t"
    )
    result = (vocab, feat, meta, coords)
    _NS_CACHE[key] = result
    return result


# ---------------------------------------------------------------------------
# Term activation map builder
# ---------------------------------------------------------------------------

def _mni_to_vox(xyz: np.ndarray, inv_affine: np.ndarray) -> np.ndarray:
    h = np.column_stack([xyz, np.ones(len(xyz))])
    v = (inv_affine @ h.T).T[:, :3]
    return np.round(v).astype(int)


def build_term_map(
    term: str,
    vocab: list,
    feat: sp.spmatrix,
    meta: pd.DataFrame,
    coords: pd.DataFrame,
    inv_affine: np.ndarray,
    shape: tuple,
    tfidf_threshold: float = 0.001,
    sigma_vox: float = 1.5,
    term_map_cache_dir: Optional[str] = None,
) -> np.ndarray:
    """Return a 3-D float32 activation-density map for one Neurosynth term.

    Uses a simple coordinate-binning + Gaussian-smoothing approach equivalent
    to MKDA density without the full meta-analysis overhead.
    """
    # Check on-disk cache first
    cache_path = None
    if term_map_cache_dir:
        safe = term.replace(" ", "_").replace("/", "-")
        cache_path = Path(term_map_cache_dir) / f"{safe}.npy"
        if cache_path.exists():
            return np.load(str(cache_path))

    tidx = vocab.index(term)
    col = np.asarray(feat[:, tidx].todense()).flatten()
    study_ids = meta.loc[col > tfidf_threshold, "id"].values
    term_coords = coords[coords["id"].isin(study_ids)][["x", "y", "z"]].values.astype(float)

    data = np.zeros(shape, dtype=np.float32)
    if len(term_coords) > 0:
        vx = _mni_to_vox(term_coords, inv_affine)
        m = (
            (vx[:, 0] >= 0) & (vx[:, 0] < shape[0]) &
            (vx[:, 1] >= 0) & (vx[:, 1] < shape[1]) &
            (vx[:, 2] >= 0) & (vx[:, 2] < shape[2])
        )
        np.add.at(data, (vx[m, 0], vx[m, 1], vx[m, 2]), 1)
        data = gaussian_filter(data, sigma=sigma_vox)

    if cache_path is not None:
        Path(term_map_cache_dir).mkdir(parents=True, exist_ok=True)
        np.save(str(cache_path), data)

    return data


# ---------------------------------------------------------------------------
# Atlas overlap
# ---------------------------------------------------------------------------

def atlas_region_overlap(
    lesion_data: np.ndarray,
    atlas_data: np.ndarray,
    atlas_labels: list,
    affine: np.ndarray,
    min_voxels: int = 3,
) -> pd.DataFrame:
    """Compute HarvardOxford atlas region overlap with lesion mask.

    Returns DataFrame with columns: ho_label, label_idx, overlap_voxels,
    overlap_pct, hemisphere, kb_region_id.
    """
    lesion_bin = (lesion_data > 0).astype(bool)
    total_lesion = lesion_bin.sum()
    if total_lesion == 0:
        return pd.DataFrame()

    rows = []
    for label_idx in range(1, len(atlas_labels)):  # skip Background (0)
        region_mask = atlas_data == label_idx
        overlap = int(np.sum(region_mask & lesion_bin))
        if overlap < min_voxels:
            continue

        # Determine hemisphere from mean x-coordinate of overlapping voxels
        overlap_coords = np.argwhere(region_mask & lesion_bin)
        mni_x = (overlap_coords[:, 0] * affine[0, 0] + affine[0, 3])
        hemisphere = "left" if mni_x.mean() < 0 else "right"

        label_name = atlas_labels[label_idx]
        kb_region = None
        if hemisphere == "left":
            kb_region = HO_LABEL_TO_KB_REGION.get(label_name)

        rows.append({
            "ho_label":      label_name,
            "label_idx":     label_idx,
            "overlap_voxels": overlap,
            "overlap_pct":   round(overlap / total_lesion * 100, 1),
            "hemisphere":    hemisphere,
            "kb_region_id":  kb_region or "",
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("overlap_voxels", ascending=False).reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# Main decode function
# ---------------------------------------------------------------------------

def decode_lesion(
    lesion_path: str,
    neurosynth_cache: Optional[str] = None,
    terms: Optional[list] = None,
    tfidf_threshold: float = 0.001,
    min_lesion_voxels: int = 10,
    cache_term_maps: bool = True,
    verbose: bool = True,
) -> dict:
    """Decode a binary lesion mask against Neurosynth language/cognitive terms.

    Parameters
    ----------
    lesion_path : str
        Path to a binary NIfTI lesion mask in MNI space (any resolution;
        will be resampled to match the HarvardOxford 2mm atlas).
    neurosynth_cache : str, optional
        Directory for Neurosynth files. Defaults to
        ``<this file's parent>/_neurosynth_cache``.
    terms : list of str, optional
        Neurosynth vocabulary terms to decode against. Defaults to
        DEFAULT_TERMS (language/cognitive subset).
    tfidf_threshold : float
        Minimum tfidf weight for a study to be included in a term's map.
    min_lesion_voxels : int
        Minimum lesion size in the atlas space before raising a warning.
    cache_term_maps : bool
        Cache per-term activation maps as .npy files (speeds up re-runs).
    verbose : bool
        Print progress messages.

    Returns
    -------
    dict with keys:
        ``lesion_path``       : input path
        ``lesion_voxels``     : total lesion voxel count (atlas space)
        ``region_overlap``    : pd.DataFrame — HarvardOxford region overlap
        ``term_decoding``     : pd.DataFrame — Neurosynth term correlations
        ``neurosynth_available`` : bool — False if download failed
        ``warnings``          : list of str
    """
    if terms is None:
        terms = DEFAULT_TERMS

    cache_dir = neurosynth_cache or _default_cache()
    warnings_out: list = []

    # ------------------------------------------------------------------
    # 1. Load and resample lesion mask to atlas space
    # ------------------------------------------------------------------
    from nilearn.datasets import fetch_atlas_harvard_oxford
    from nilearn.image import resample_to_img

    if verbose:
        print("Loading lesion mask …")
    lesion_img_orig = nib.load(lesion_path)

    ho = fetch_atlas_harvard_oxford("cort-maxprob-thr25-2mm")
    atlas_img   = ho.maps
    atlas_data  = atlas_img.get_fdata().astype(np.uint8)
    affine      = atlas_img.affine
    inv_affine  = np.linalg.inv(affine)
    shape       = atlas_img.shape[:3]

    # Resample lesion to atlas space (nearest-neighbour to keep binary)
    lesion_img = resample_to_img(
        lesion_img_orig, atlas_img, interpolation="nearest"
    )
    lesion_data = (lesion_img.get_fdata() > 0).astype(np.float32)
    lesion_voxels = int(lesion_data.sum())

    if lesion_voxels < min_lesion_voxels:
        msg = (
            f"Lesion has only {lesion_voxels} voxels after resampling to "
            "2mm atlas space — check that the mask is in MNI space and is binary."
        )
        warnings_out.append(msg)
        if verbose:
            print(f"  WARNING: {msg}")

    # ------------------------------------------------------------------
    # 2. Atlas region overlap (always available)
    # ------------------------------------------------------------------
    if verbose:
        print("Computing HarvardOxford atlas overlap …")
    region_df = atlas_region_overlap(lesion_data, atlas_data, ho.labels, affine)

    # ------------------------------------------------------------------
    # 3. Neurosynth term decoding (requires files download on first run)
    # ------------------------------------------------------------------
    neurosynth_ok = False
    term_df = pd.DataFrame()

    try:
        cache_dir = ensure_neurosynth_files(cache_dir)
        vocab, feat, meta, coords_ns = _load_neurosynth(cache_dir)

        # Filter to terms that exist in the vocabulary
        valid_terms = [t for t in terms if t in vocab]
        missing = [t for t in terms if t not in vocab]
        if missing and verbose:
            print(f"  Terms not in Neurosynth vocabulary (skipped): {missing}")

        term_map_dir = os.path.join(cache_dir, "term_maps") if cache_term_maps else None
        if verbose:
            print(f"Decoding {len(valid_terms)} terms against lesion …")

        lesion_flat = lesion_data.flatten()
        rows_t = []
        for term in valid_terms:
            tmap = build_term_map(
                term, vocab, feat, meta, coords_ns,
                inv_affine, shape,
                tfidf_threshold=tfidf_threshold,
                term_map_cache_dir=term_map_dir,
            )
            r, p = pearsonr(lesion_flat, tmap.flatten())
            impairment = TERM_TO_IMPAIRMENT.get(term)
            rows_t.append({
                "term":       term,
                "r":          round(float(r), 4),
                "p":          float(p),
                "impairment": impairment or "",
            })

        term_df = pd.DataFrame(rows_t).sort_values("r", ascending=False).reset_index(drop=True)
        neurosynth_ok = True

    except Exception as exc:
        msg = f"Neurosynth decoding unavailable: {exc}"
        warnings_out.append(msg)
        if verbose:
            print(f"  WARNING: {msg}")

    return {
        "lesion_path":           lesion_path,
        "lesion_voxels":         lesion_voxels,
        "region_overlap":        region_df,
        "term_decoding":         term_df,
        "neurosynth_available":  neurosynth_ok,
        "warnings":              warnings_out,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _main() -> None:
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("lesion", help="Path to binary lesion NIfTI in MNI space.")
    p.add_argument("--cache", default=None,
                   help="Directory for Neurosynth cache (default: ./_neurosynth_cache).")
    p.add_argument("--terms", nargs="+", default=None,
                   help="Override default term list.")
    args = p.parse_args()

    result = decode_lesion(args.lesion, neurosynth_cache=args.cache,
                           terms=args.terms, verbose=True)

    print(f"\n── Lesion: {result['lesion_voxels']} voxels (MNI 2mm atlas space)")

    print("\n── HarvardOxford region overlap:")
    if result["region_overlap"].empty:
        print("   (no regions overlapping lesion)")
    else:
        print(result["region_overlap"].to_string(index=False))

    print("\n── Neurosynth term decoding (top 10):")
    if result["term_decoding"].empty:
        print("   (Neurosynth decoding unavailable)")
    else:
        print(result["term_decoding"].head(10).to_string(index=False))

    if result["warnings"]:
        print("\nWarnings:")
        for w in result["warnings"]:
            print(f"  ! {w}")


if __name__ == "__main__":
    _main()
