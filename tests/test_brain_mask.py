"""Brain mask: HD-BET by default; HD-BET OR SynthStrip keeps lesion cavities inside."""
from unittest.mock import patch
import nibabel as nib
import numpy as np
import pytest
from scipy import ndimage

from calmar import qc as q
from calmar.brainmask import ball, close_cavities
from calmar.processing import paths, process

SHAPE = (12, 12, 12)


def save(path, data):
    nib.save(nib.Nifti1Image(np.asarray(data, dtype='uint8'), np.eye(4)), path)
    return path


def cube(lo, hi):
    data = np.zeros(SHAPE, dtype=bool)
    data[lo:hi, lo:hi, lo:hi] = True
    return data


def test_distance_transform_closing_matches_ball_closing():
    g = np.mgrid[:40, 44:88, :36]
    m = (((g[0] - 20) / 15) ** 2 + ((g[1] - 66) / 18) ** 2 + ((g[2] - 18) / 14) ** 2) <= 1
    m &= ~((((g[0] - 33) / 6) ** 2 + ((g[1] - 66) / 5) ** 2 + ((g[2] - 18) / 5) ** 2) <= 1)  # surface cavity
    footprint = ball([4, 4, 4]); pad = max(footprint.shape)
    reference = ndimage.binary_closing(np.pad(m, pad), structure=footprint)[pad:-pad, pad:-pad, pad:-pad]
    reference = ndimage.binary_fill_holes(reference | m)
    assert reference.sum() > m.sum()
    assert np.array_equal(close_cavities(m, (1, 1, 1), 4), reference)


def test_combined_mask_is_found_not_its_parts(tmp_path):
    for name in ('T1w_desc-hdbet_brain_mask', 'T1w_desc-synthstrip_brain_mask', 'T1w_brain_mask'):
        save(tmp_path/f'{name}.nii.gz', cube(2, 8))
    assert q.find_best_hdbet_mask(tmp_path).name == 'T1w_brain_mask.nii.gz'
    for name in ('T1w_desc-hdbet_brain', 'T1w_brain'):
        save(tmp_path/f'{name}.nii.gz', cube(2, 8))
    assert q.find_best_hdbet_brain(tmp_path).name == 'T1w_brain.nii.gz'
    # A skull-strip repair (desc-accurate) still takes precedence.
    save(tmp_path/'T1w_desc-accurate_brain_mask.nii.gz', cube(2, 8))
    assert q.find_best_hdbet_mask(tmp_path).name == 'T1w_desc-accurate_brain_mask.nii.gz'


def test_repair_mask_gets_the_synthstrip_cavity_back(tmp_path):
    # A T1 whose qform and sform differ slightly: the repaired mask must carry
    # the T1's exact header, whatever header HD-BET wrote.
    t1_img = nib.Nifti1Image(np.ones(cube(0, 1).shape, dtype='float32'), np.eye(4))
    t1_img.set_qform(np.diag([1.0000004, 1, 1, 1]), code=1)
    t1_img.set_sform(np.eye(4), code=2)
    t1 = tmp_path/'T1w.nii.gz'
    nib.save(t1_img, t1)
    repaired = save(tmp_path/'T1w_desc-accurate_brain_mask.nii.gz', cube(2, 8))
    with pytest.raises(FileNotFoundError):                                # union needs SynthStrip
        q.add_synthstrip_mask(repaired, tmp_path, t1, 'hdbet+synthstrip')
    assert q.add_synthstrip_mask(repaired, tmp_path, t1) == 0             # default: HD-BET alone
    assert q.check_repaired_mask(repaired, tmp_path, 'hdbet+synthstrip') == 'hdbet'  # recorded choice wins
    save(tmp_path/'T1w_desc-synthstrip_brain_mask.nii.gz', cube(1, 9))
    added = q.add_synthstrip_mask(repaired, tmp_path, t1, 'hdbet+synthstrip')
    assert added == cube(1, 9).sum() - cube(2, 8).sum()
    assert q.check_repaired_mask(repaired, tmp_path) == 'hdbet+synthstrip'
    assert q.repaired_mask_sidecar(repaired).name == 'T1w_desc-accurate_brain_mask.json'
    out = nib.load(repaired)
    assert np.array_equal(np.asarray(out.dataobj) > 0, cube(1, 9))
    assert out.header.get_zooms() == nib.load(t1).header.get_zooms()
    assert np.array_equal(out.header.get_qform(), nib.load(t1).header.get_qform())


def run_brain(tmp_path, monkeypatch, config):
    monkeypatch.setenv('SLURM_JOB_ID', 'fixture')
    t1 = tmp_path/'sub-x_T1w.nii.gz'
    nib.save(nib.Nifti1Image(np.full(SHAPE, 100, dtype='int16'), np.eye(4)), t1)
    entry = {'subject': 'sub-x', 't1w': str(t1)}
    request = {'dataset': str(tmp_path), 'entries': [entry], 'config': config}
    hdbet = cube(3, 9); hdbet[3:5, 3:9, 3:9] = False                    # cavity HD-BET leaves out
    def fake_extractor(t1w, out, *, prefer, desc, **kwargs):
        out.mkdir(parents=True, exist_ok=True)                           # as run_hd_bet does
        mask = out/f'sub-x_T1w_desc-{desc}_brain_mask.nii.gz'
        save(mask, hdbet if prefer == 'hd-bet' else cube(2, 10))
        return {'returncode': 0, 'mask': mask, 'brain': out/f'sub-x_T1w_desc-{desc}_brain.nii.gz'}
    with patch('calmar.processing.q.run_hd_bet', side_effect=fake_extractor) as extractor, \
            patch('calmar.processing.publish', side_effect=lambda a, b, c: a.rename(b)):
        process('brain', request)
    return paths(request, entry)['hdbet'], hdbet, extractor


def test_union_brain_mask_is_hdbet_or_synthstrip(tmp_path, monkeypatch):
    out, hdbet, extractor = run_brain(tmp_path, monkeypatch, {'BRAIN_MASK': 'hdbet+synthstrip'})
    assert [c.kwargs['prefer'] for c in extractor.call_args_list] == ['hd-bet', 'mri_synthstrip']
    final = np.asarray(nib.load(out/'sub-x_T1w_brain_mask.nii.gz').dataobj) > 0
    assert np.array_equal(final, hdbet | cube(2, 10))
    assert (out/'sub-x_T1w_desc-synthstrip_brain_mask.nii.gz').is_file()
    brain = np.asarray(nib.load(out/'sub-x_T1w_brain.nii.gz').dataobj)
    assert (brain[final] == 100).all() and (brain[~final] == 0).all()


def test_default_brain_mask_is_hdbet_alone(tmp_path, monkeypatch):
    out, hdbet, extractor = run_brain(tmp_path, monkeypatch, {})
    assert [c.kwargs['prefer'] for c in extractor.call_args_list] == ['hd-bet']
    assert np.array_equal(np.asarray(nib.load(out/'sub-x_T1w_brain_mask.nii.gz').dataobj) > 0, hdbet)


def test_unknown_brain_mask_method_is_rejected(tmp_path, monkeypatch):
    with pytest.raises(Exception, match='BRAIN_MASK must be one of'):
        run_brain(tmp_path, monkeypatch, {'BRAIN_MASK': 'bet'})


def test_saved_mask_keeps_the_t1_header_exactly(tmp_path):
    # Scanner exports often have a qform and sform that differ in the 6th decimal.
    # Rebuilding the header from one affine changes the voxel size and LINDA's
    # ITK then rejects the T1/mask pair.
    from calmar.brainmask import save_like
    qform = np.array([[0.99905, 0.03998, 0.01733, -85.2], [-0.03997, 0.99920, -0.00069, -97.3],
                      [-0.01734, 0, 0.99985, -131.2], [0, 0, 0, 1]])
    sform = qform.copy(); sform[0, 0] = 0.999046
    t1 = nib.Nifti1Image(np.zeros(SHAPE, dtype='int16'), None)
    t1.set_qform(qform, 1); t1.set_sform(sform, 1)
    out = nib.load(save_like(cube(2, 8), t1, tmp_path/'mask.nii.gz'))
    assert np.array_equal(out.header.get_qform(), t1.header.get_qform())
    assert np.array_equal(out.header.get_sform(), t1.header.get_sform())
    assert out.header.get_zooms() == t1.header.get_zooms()
    assert out.get_data_dtype() == np.uint8


def test_unrecorded_repair_must_match_the_brain_mask_method(tmp_path):
    # Repairs made before the method was recorded beside the mask.
    union = 'hdbet+synthstrip'
    repaired = save(tmp_path/'T1w_desc-accurate_brain_mask.nii.gz', cube(2, 8))
    assert q.check_repaired_mask(repaired, tmp_path) == 'hdbet'          # nothing to check
    with pytest.raises(FileNotFoundError):
        q.check_repaired_mask(repaired, tmp_path, union)
    save(tmp_path/'T1w_desc-synthstrip_brain_mask.nii.gz', cube(1, 9))
    with pytest.raises(RuntimeError, match='made for BRAIN_MASK="hdbet"'):
        q.check_repaired_mask(repaired, tmp_path, union)                  # repair made under "hdbet"
    save(repaired, cube(1, 9))
    assert q.check_repaired_mask(repaired, tmp_path, union) == union


def test_repaired_mask_on_another_grid_is_rejected(tmp_path):
    repaired = save(tmp_path/'T1w_desc-accurate_brain_mask.nii.gz', cube(1, 9))
    nib.save(nib.Nifti1Image(cube(1, 9).astype('uint8'), np.diag([2., 2, 2, 1])),
             tmp_path/'T1w_desc-synthstrip_brain_mask.nii.gz')
    with pytest.raises(ValueError, match='different grids'):
        q.check_repaired_mask(repaired, tmp_path, 'hdbet+synthstrip')
