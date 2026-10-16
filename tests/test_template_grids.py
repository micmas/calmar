"""World-coordinate placement of ch2 template masks on the FSL MNI152 grids."""
import nibabel as nib
import numpy as np
import pytest

from calmar.processing import FSL_GRID, FSL_GRID_1MM, to_fsl_1mm, to_fsl_2mm

# LINDA's ch2 template grid: 181x217x181, 1 mm, RAS, origin (-90,-125,-71).
CH2 = np.array([[1., 0, 0, -90], [0, 1., 0, -125], [0, 0, 1., -71], [0, 0, 0, 1]])


def ch2_mask(tmp_path, voxels):
    data = np.zeros((181, 217, 181), dtype='uint8')
    for v in voxels:
        data[v] = 1
    path = tmp_path/'Lesion_in_MNI.nii.gz'
    nib.save(nib.Nifti1Image(data, CH2), path)
    return path


def world(affine, index):
    return nib.affines.apply_affine(affine, index)


def test_bcb_input_keeps_world_position(tmp_path):
    # A single voxel at a known MNI coordinate must stay at that coordinate.
    voxel = (120, 100, 90)
    target = world(CH2, voxel)
    out = to_fsl_1mm(ch2_mask(tmp_path, [voxel]), tmp_path/'fsl.nii.gz')
    img = nib.load(out)
    assert img.shape == FSL_GRID_1MM[0]
    hits = np.argwhere(np.asarray(img.dataobj) > 0)
    assert len(hits) == 1
    np.testing.assert_allclose(world(img.affine, hits[0]), target)
    # Matching by voxel index (BCBToolkit's own reslice) would be 1 mm off in y and z.
    assert not np.allclose(world(img.affine, voxel), target)


def test_deepdisco_coverage_keeps_half_filled_blocks(tmp_path):
    # A 2 mm-thick slab is kept; one thin 1 mm sheet in an empty region is not
    # half of any 2 mm voxel and is dropped by coverage (point sampling may keep it).
    slab = [(x, y, z) for x in range(100, 110) for y in range(100, 110) for z in range(81, 84)]
    path = ch2_mask(tmp_path, slab)
    out = nib.load(to_fsl_2mm(path, tmp_path/'dd.nii.gz', 'coverage'))
    assert out.shape == FSL_GRID[0]
    np.testing.assert_allclose(out.affine, FSL_GRID[1])
    data = np.asarray(out.dataobj)
    assert set(np.unique(data)) <= {0, 1}
    kept = np.argwhere(data > 0)
    centres = np.array([world(out.affine, k) for k in kept])
    # Every kept 2 mm voxel centre lies inside the slab's world extent (+/- 1 mm).
    lo, hi = world(CH2, (100, 100, 81)), world(CH2, (109, 109, 83))
    assert len(kept) and (centres >= lo - 1).all() and (centres <= hi + 1).all()
    # Expected volume is preserved within one voxel layer.
    assert abs(len(kept) * 8 - len(slab)) <= 0.5 * len(slab)


def test_unknown_downsampling_is_rejected(tmp_path):
    with pytest.raises(ValueError, match='Unknown'):
        to_fsl_2mm(ch2_mask(tmp_path, [(90, 90, 90)]), tmp_path/'x.nii.gz', 'mean')


def test_misspelt_method_options_are_rejected(tmp_path, monkeypatch):
    from calmar.processing import step_bcb, step_deepdisco
    from calmar.study import derivative_dirs
    entry = {'subject': 'sub-a', 'session': None, 't1w': 'unused'}
    p = derivative_dirs(tmp_path, {}, entry)
    with pytest.raises(ValueError, match='BCB_INPUT_GRID'):
        step_bcb({'BCB_INPUT_GRID': 'mni'}, entry, p, {})
    with pytest.raises(ValueError, match='DEEPDISCO_DOWNSAMPLING'):
        step_deepdisco({'DEEPDISCO_DOWNSAMPLING': 'mean'}, entry, p, {})
