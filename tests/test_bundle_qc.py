import gzip
from pathlib import Path

import nibabel as nib
import numpy as np
import pandas as pd

from calmar.bundle_qc import _sample_bundle, measure_bundles


def test_streamline_occupancy_and_profiles_follow_ras_orientation(tmp_path):
    reference = nib.Nifti1Image(np.zeros((6, 6, 6)), np.diag([2., 2., 2., 1.]))
    line = np.array([[4, -2, 4], [4, -2, 4], [4, 8, 4]], dtype=np.float32)
    track = tmp_path / "test.tck"
    nib.streamlines.save(nib.streamlines.Tractogram([line[::-1]], affine_to_rasmm=np.eye(4)), track)

    occupied, profile, count, outside, skipped = _sample_bundle(track, reference, 6)

    assert occupied == {(2, y, 2) for y in range(5)}
    assert profile == [set(), *[{(2, y, 2)} for y in range(5)]]
    assert (count, outside, skipped) == (1, 1, 0)


def test_aslant_profiles_start_at_the_superior_endpoint(tmp_path):
    reference = nib.Nifti1Image(np.zeros((6, 6, 6)), np.eye(4))
    line = np.array([[2, 0, 1], [2, 2, 4]], dtype=np.float32)
    track = tmp_path / "aslant.tck"
    nib.streamlines.save(nib.streamlines.Tractogram([line], affine_to_rasmm=np.eye(4)), track)
    _, profile, _, _, _ = _sample_bundle(track, reference, 5, superior_first=True)

    assert profile[0] == {(2, 2, 4)}
    assert profile[-1] == {(2, 0, 1)}


def test_bundle_qc_keeps_absence_distinct_from_measured_zero(tmp_path, monkeypatch):
    reference = nib.Nifti1Image(np.zeros((6, 6, 6)), np.eye(4))
    lesion = np.zeros(reference.shape, dtype=bool)
    fa = np.full(reference.shape, 0.4)
    md = np.full(reference.shape, 0.0008)
    valid = np.ones(reference.shape, dtype=bool)
    valid[2, 2, 2] = False
    lesion[2, 1, 2] = True
    monkeypatch.setattr("calmar.bundle_qc._inputs",
                        lambda *_: (reference, lesion, fa, md, valid, {}))
    monkeypatch.setattr("calmar.bundle_qc._plot", lambda *_: None)
    for suffix, x in (("L", 2), ("R", 3)):
        track = tmp_path / f"sub-example_space-ACPC_model-ss3t_bundle-AssociationArcuateFasciculus{suffix}_streamlines.tck"
        line = np.array([[x, 0, 2], [x, 4, 2]], dtype=np.float32)
        nib.streamlines.save(nib.streamlines.Tractogram([line], affine_to_rasmm=np.eye(4)), track)
    truncated = tmp_path / "sub-example_space-ACPC_model-ss3t_bundle-AssociationFrontalAslantTractL_streamlines.tck.gz"
    truncated.write_bytes(gzip.compress(b"mrtrix tracks\n")[:-4])
    table = pd.DataFrame([
        {"tract": "Association_ArcuateFasciculusL", "hemisphere": "left", "lesion_overlap_pct": np.nan,
         "valid_voxel_pct": np.nan},
    ])

    result = measure_bundles(Path("unused"), tmp_path, table, tmp_path, 5)
    profiles = pd.read_csv(tmp_path / result["profile_tsv"], sep="\t")

    assert table["lesion_overlap_pct"].tolist() == [20, 0]
    assert table["valid_voxel_pct"].tolist() == [80, 100]
    assert [bundle["status"] for bundle in result["bundles"]] == [
        "measured", "measured", "unreadable streamline file", "no streamline file",
        "no streamline file", "no streamline file"]
    assert profiles.loc[2, "valid_voxels"] == 0 and pd.isna(profiles.loc[2, "md_median_mm2_s"])
    assert profiles.loc[1, "lesion_voxels"] == 1
