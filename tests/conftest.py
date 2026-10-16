import pytest


@pytest.fixture(autouse=True)
def stand_in_template_transforms(tmp_path_factory, monkeypatch):
    """Tests never depend on the real ch2 -> MNI152 transforms (made by analysis_38)."""
    from calmar import templates
    folder = tmp_path_factory.mktemp('templates')
    import nibabel as nib, numpy as np
    for name in ('WARP', 'AFFINE', 'T1', 'T1_BRAIN', 'BRAIN_MASK'):
        path = folder / getattr(templates, name).name
        if path.name.endswith('.nii.gz'):
            nib.save(nib.Nifti1Image(np.ones((4, 4, 4), dtype='float32'), np.eye(4)), path)
        else:
            path.write_bytes(b'stand-in')
        monkeypatch.setattr(templates, name, path)
    monkeypatch.setattr(templates, 'DIR', folder)
