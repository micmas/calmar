"""The report's description of how its lesion mask was made, and the agreement
with the manual mask shown before a report is generated."""
import json
from pathlib import Path
from types import SimpleNamespace

import nibabel as nib
import numpy as np

from calmar.mask_method import NO_RECORD, manual_agreement, manual_agreement_html, mask_method
from calmar.study import ENTRY_CONFIG, ENTRY_DATASET, Study, derivative_dirs


def mask(path, box):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = np.zeros((10, 10, 10), dtype=np.uint8); data[box] = 1
    nib.save(nib.Nifti1Image(data, np.eye(4)), path)
    return path


def record(path, options):
    path = Path(path)
    target = path/'calmar-cache.json' if path.is_dir() or not path.suffix else Path(str(path) + '.cache.json')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({'identity': {'options': options}}))


def study(tmp_path, config):
    entry = {'subject': 'sub-1', 'session': 'ses-1', 't1w': str(tmp_path/'sub-1_T1w.nii.gz')}
    return SimpleNamespace(dirs=lambda e: derivative_dirs(tmp_path, config, e), dataset=tmp_path, config=config), entry


def test_synthstroke_mask_names_the_registration_that_was_used(tmp_path):
    s, entry = study(tmp_path, {'SEGMENTATION_METHODS': ['synthstroke']})
    d = s.dirs(entry)
    record(d['hdbet'], {'method': 'hdbet', 'mode': 'fast'})
    record(d['synthstroke'], {'module': 'synthstroke/0.0.0', 'tta': True, 'brain_dilation': 2})
    record(d['registration'], {'random_seed': 1729})
    record(d['registration']/'SynthStroke_in_MNI.nii.gz', {'registration': 'ants'})
    steps = mask_method(s, entry, 'synthstroke')
    assert steps[0] == 'Brain mask: HD-BET (hdbet/1.0.0), fast mode.'
    assert 'with test-time augmentation' in steps[1] and 'sub-1_T1w.nii.gz' in steps[1]
    assert 'ANTs registration' in steps[2] and 'seed 1729' in steps[2]


def test_linda_route_and_missing_records_are_stated(tmp_path):
    s, entry = study(tmp_path, {})
    d = s.dirs(entry)
    record(d['synthstroke']/'SynthStroke_in_MNI.nii.gz', {'module': 'linda/0.5.1'})
    steps = mask_method(s, entry, 'synthstroke')
    assert NO_RECORD in steps[0] and NO_RECORD in steps[1]          # brain mask, segmentation
    assert "LINDA's registration" in steps[2] and NO_RECORD not in steps[2]
    record(d['linda'], {'module': 'linda/0.5.1', 'brain_mask_bypass': True, 'random_seed': 7, 'threads': 1})
    steps = [x for x in mask_method(s, entry, 'linda') if x]
    assert 'using that brain mask' in steps[1] and 'random seed 7, 1 thread.' in steps[1]


def test_isles_manual_mask_method_uses_its_dwi_dataset(tmp_path):
    acute = tmp_path / 'ISLES-2022'
    dwi = acute / 'sub-acute' / 'ses-1' / 'dwi' / 'sub-acute_ses-1_dwi.nii.gz'
    mask_path = acute / 'derivatives' / 'sub-acute' / 'ses-1' / 'sub-acute_ses-1_msk.nii.gz'
    mask(dwi, np.s_[1:3, 1:3, 1:3]); mask(mask_path, np.s_[2:4, 2:4, 2:4])
    entry = {'subject': 'sub-acute', 'session': 'ses-1', 't1w': str(dwi), 'dwi': str(dwi),
             ENTRY_DATASET: str(acute),
             ENTRY_CONFIG: {'DATASET_SOURCE': 'isles2022', 'MODALITY': 'dwi',
                            'SEGMENTATION_METHODS': ['openads']}}
    steps = mask_method(Study({}, tmp_path / 'chronic', tmp_path), entry, 'manual')
    assert mask_path.name in steps[0]
    assert 'diffusion-weighted image' in steps[0]


def test_agreement_only_with_a_manual_mask(tmp_path):
    manual = mask(tmp_path/'m.nii.gz', np.s_[2:6, 2:6, 2:6])                # 64 voxels
    synth = mask(tmp_path/'s.nii.gz', np.s_[2:6, 2:6, 2:4])                 # 32, all inside
    assert manual_agreement({'synthstroke': synth}) is None and manual_agreement_html({'synthstroke': synth}) == ''
    manual_ml, [row] = manual_agreement({'manual': manual, 'synthstroke': synth})
    assert manual_ml == 0.064 and row['dice'] == 2 * 32 / 96
    assert (row['covers'], row['inside'], row['ratio']) == (0.5, 1.0, 0.5)
    html = manual_agreement_html({'manual': manual, 'synthstroke': synth})
    assert 'SynthStroke: Dice <b>0.67</b>' in html and 'covers 50% of the manual lesion' in html
