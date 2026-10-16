import importlib.util
from pathlib import Path

import nibabel as nib
import numpy as np


def test_preparation_uses_atlas_affine_and_shape(tmp_path, monkeypatch):
    script = Path(__file__).parents[1]/'src/python/prepare_tractotron.py'
    spec = importlib.util.spec_from_file_location('prepare_tractotron', script)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    monkeypatch.setenv('SLURM_JOB_ID', 'fixture')
    mask, ref, output = (tmp_path/name for name in ('mask.nii.gz', 'ref.nii.gz', 'out.nii.gz'))
    data = np.zeros((6, 6, 6), dtype='uint8'); data[3, 3, 3] = 1
    nib.save(nib.Nifti1Image(data, np.eye(4)), mask)
    affine = np.eye(4); affine[:3, 3] = 2
    nib.save(nib.Nifti1Image(np.zeros((3, 4, 3)), affine), ref)
    before = mask.read_bytes()
    module.prepare(str(mask), str(ref), str(output))
    result = nib.load(output)
    assert result.shape == (3, 4, 3)
    assert np.array_equal(result.affine, affine)
    assert result.get_fdata()[1, 1, 1] == 1
    assert result.get_fdata().sum() == 1
    assert mask.read_bytes() == before
