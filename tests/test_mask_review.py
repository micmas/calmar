from types import SimpleNamespace
from unittest.mock import patch

import nibabel as nib
import numpy as np
from ipyniivue import NiiVue

from calmar.overlay import mask_review


def test_cached_coreg_and_masks_share_layers_and_controls(tmp_path):
    image = nib.Nifti1Image(np.ones((3,3,3),dtype=np.uint8), np.eye(4))
    path = tmp_path/'registered.nii.gz'; nib.save(image,path)
    viewer = NiiVue()
    helpers = SimpleNamespace(fresh_viewer=lambda *a, **kw:viewer,
                              vols=lambda specs:[{**{k:v for k,v in s.items() if k != 'path'}, 'data':image.to_bytes()} for s in specs])
    with patch('calmar.overlay.reference_edges', return_value=path):
        panel = mask_review(helpers, 'review', [dict(data=image.to_bytes(),name='T1'),
            dict(data=image.to_bytes(),name='Manual',colormap='blue',opacity=.5),
            dict(data=image.to_bytes(),name='LINDA',colormap='red',opacity=.85)], coreg_path=path)
    try:
        original = list(viewer.volumes)
        assert panel.review_mode.value == 'coreg'
        assert [v.opacity for v in original] == [1., 0., 0., 1.]
        panel.review_mode.value = 'masks'
        assert [v.opacity for v in viewer.volumes] == [1., .5, .85, 0.]
        panel.mask_controls[1].value = False
        panel.review_mode.value = 'coreg'
        panel.review_mode.value = 'masks'
        assert [v.opacity for v in viewer.volumes] == [1., .5, 0., 0.]
        assert all(a is b for a,b in zip(original,viewer.volumes))
    finally:
        viewer.close(); panel.close()


def test_already_aligned_mask_has_no_misleading_coreg_control():
    viewer = NiiVue()
    image = nib.Nifti1Image(np.ones((3,3,3),dtype=np.uint8),np.eye(4)).to_bytes()
    helpers = SimpleNamespace(fresh_viewer=lambda *a, **kw:viewer, vols=lambda specs:specs)
    panel = mask_review(helpers,'review',[dict(data=image,name='T1'),dict(data=image,name='Manual',colormap='blue')])
    try:
        assert panel.review_mode.value == 'masks'
        assert len(panel.review_mode.options) == 1
        assert len(viewer.volumes) == 2
    finally:
        viewer.close(); panel.close()
