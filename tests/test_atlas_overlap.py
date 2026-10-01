import json
from unittest.mock import patch

import nibabel as nib
import numpy as np
import pandas as pd

from calmar.atlas_overlap import calculate_overlap, cached_overlap, SIDE_COLUMNS
from calmar.anatomy_labels import label_table
from calmar.atlas_ui import overlap_table


def test_laterality_uses_world_coordinates_and_preserves_total(tmp_path):
    # Reversed x-axis: high array x is anatomically LEFT. One unsided ROI.
    affine = np.diag([-2., 2., 2., 1.]); affine[0, 3] = 4
    atlas = nib.Nifti1Image(np.ones((5, 3, 3), dtype=np.uint8), affine)
    data = np.zeros(atlas.shape, dtype=np.uint8)
    data[3:, 1, 1] = 1
    path = tmp_path / 'mask.nii.gz'
    nib.save(nib.Nifti1Image(data, affine), path)
    stats, total = calculate_overlap(path, atlas, np.asarray(atlas.dataobj), ['Background', 'Unsided ROI'])
    r = stats['Unsided ROI']
    assert total == r['overlap_voxels'] == r['left_overlap_voxels'] == 2
    assert r['right_overlap_voxels'] == r['midline_overlap_voxels'] == 0
    assert r['lesion_in_roi_percent'] == 100
    assert label_table(pd.DataFrame([dict(region='Unsided ROI', **r)]), 'HarvardOxford').lesion_hemisphere.iloc[0] == 'Left'
    data[0, 1, 1] = data[2, 1, 1] = 1
    nib.save(nib.Nifti1Image(data, affine), path)
    stats, total = calculate_overlap(path, atlas, np.asarray(atlas.dataobj), {1: 'Unsided ROI'})
    r = stats['Unsided ROI']
    assert total == sum(r[c] for c in SIDE_COLUMNS) == 4
    assert (r['left_overlap_voxels'], r['right_overlap_voxels'], r['midline_overlap_voxels']) == (2, 1, 1)


def test_cache_migrates_legacy_and_records_zero_missing_and_sessions(tmp_path):
    atlas = nib.Nifti1Image(np.ones((2, 2, 2), dtype=np.uint8), np.eye(4))
    mask = tmp_path / 'mask.nii.gz'
    nib.save(nib.Nifti1Image(np.zeros((2, 2, 2), dtype=np.uint8), np.eye(4)), mask)
    entries = [dict(subject='sub-one', session=s) for s in ('ses-a', 'ses-b', 'ses-missing')]
    resolver = lambda e: tmp_path/'missing.nii.gz' if e['session'] == 'ses-missing' else mask
    csv = tmp_path / 'overlap.csv'
    # A stale legacy positive row must disappear when the refreshed result is zero.
    pd.DataFrame([dict(subject='sub-one', session='ses-a', region='Old', overlap_voxels=7)]).to_csv(csv, index=False)
    args = (csv, entries, resolver, 'Test', atlas, np.asarray(atlas.dataobj), ['Background', 'ROI'])
    df = cached_overlap(*args)
    assert df.empty and set(SIDE_COLUMNS).issubset(df.columns)
    assert len(df.attrs['overlap_status']) == 3
    assert 'no lesion voxels intersect' in overlap_table(df, 'sub-one', 'ses-b', 'Test', 'manual')
    assert 'Mask unavailable' in overlap_table(df, 'sub-one', 'ses-missing', 'Test', 'manual')
    assert csv.with_suffix('.before-laterality.csv').exists()
    with patch('calmar.atlas_overlap.calculate_overlap', side_effect=AssertionError('cached zero reran')):
        cached_overlap(*args)
    # Changing the mask invalidates BOTH sessions' cached zero results.
    nib.save(atlas, mask)
    refreshed = cached_overlap(*args)
    assert set(refreshed.session) == {'ses-a', 'ses-b'}
    assert len(refreshed) == 2
    assert np.isfinite(refreshed.lesion_in_roi_percent).all()


def test_old_table_never_claims_bilateral_lesion_from_atlas_name():
    row = dict(region='Frontal Pole', subject='sub-a', session='', overlap_voxels=2,
               total_lesion_voxels=2, lesion_in_roi_percent=100., roi_coverage_percent=2.)
    html = overlap_table(pd.DataFrame([row]), 'sub-a', '', 'HarvardOxford', 'manual')
    assert 'Not calculated' in html
    assert 'Bilateral ROI</td>' not in html
