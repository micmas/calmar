"""Choosing the lesion segmentations; without LINDA, the registration step
provides the template registration."""
from pathlib import Path

import pytest

from calmar import masks as cm
from calmar import processing, scheduled
from calmar.guided import normalize_selection
from calmar.methods import methods_table
from calmar.study import Study, derivative_dirs, mni_masks, segmentation_methods, stage_selected, template_source

ENTRY = {'subject': 'sub-1', 'session': 'ses-1', 't1w': 'unused'}


def touch(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b'x')
    return path


def test_methods_default_to_both_and_must_be_known():
    assert segmentation_methods({}) == ('linda', 'synthstroke')
    assert segmentation_methods({'SEGMENTATION_METHODS': ['synthstroke']}) == ('synthstroke',)
    for bad in ([], ['linda', 'deepmedic']):
        with pytest.raises(ValueError):
            segmentation_methods({'SEGMENTATION_METHODS': bad})


def test_registration_runs_only_without_linda():
    with_linda, without = {}, {'SEGMENTATION_METHODS': ['synthstroke']}
    assert (template_source(with_linda), template_source(without)) == ('linda', 'ants')
    assert [stage_selected(s, with_linda) for s in ('linda', 'synthstroke', 'registration', 'bcb')] == \
        [True, True, False, True]
    assert [stage_selected(s, without) for s in ('linda', 'synthstroke', 'registration', 'bcb')] == \
        [False, True, True, True]
    assert stage_selected('registration', {'SEGMENTATION_METHODS': ['linda']}) is False


def test_template_folder_and_masks_follow_the_registration(tmp_path):
    d = derivative_dirs(tmp_path, {}, ENTRY)
    assert d['template'] == d['linda']
    assert mni_masks(d)['synthstroke'] == d['synthstroke']/'SynthStroke_in_MNI.nii.gz'
    d = derivative_dirs(tmp_path, {'SEGMENTATION_METHODS': ['synthstroke']}, ENTRY)
    assert d['template'] == d['registration'] == tmp_path/'derivatives/registration/sub-1/ses-1/anat'
    assert mni_masks(d) == {'linda': d['linda']/'Lesion_in_MNI.nii.gz',
                            'manual': d['registration']/'ExpertMask_in_MNI.nii.gz',
                            'synthstroke': d['registration']/'SynthStroke_in_MNI.nii.gz',
                            'openads': d['openads']/'OpenADS_in_MNI.nii.gz'}


def test_discovery_never_mixes_the_two_registrations(tmp_path):
    config = {'SEGMENTATION_METHODS': ['synthstroke']}
    study = Study(config, tmp_path, tmp_path)
    d = study.dirs(ENTRY)
    touch(d['synthstroke']/'prediction_lesion_mask.nii.gz')
    touch(d['synthstroke']/'SynthStroke_in_MNI.nii.gz')          # warped earlier with LINDA's registration
    touch(d['linda']/'ExpertMask_in_MNI.nii.gz')
    assert study.masks(ENTRY) == {'synthstroke': {'T1w': d['synthstroke']/'prediction_lesion_mask.nii.gz'}}
    touch(d['registration']/'SynthStroke_in_MNI.nii.gz')
    touch(d['registration']/'ExpertMask_in_MNI.nii.gz')
    found = study.masks(ENTRY)
    assert found['synthstroke']['MNI'] == d['registration']/'SynthStroke_in_MNI.nii.gz'
    assert found['manual'] == {'MNI': d['registration']/'ExpertMask_in_MNI.nii.gz'}
    # With LINDA the tool folders are used, as before.
    assert cm.discover_masks(ENTRY, d['linda'], d['synthstroke'])['synthstroke']['MNI'] == \
        d['synthstroke']/'SynthStroke_in_MNI.nii.gz'


def test_disconnectomes_expect_only_selected_segmentations(tmp_path):
    config = {'SEGMENTATION_METHODS': ['synthstroke'], 'BCB_MASKS': 'all'}
    p = derivative_dirs(tmp_path, config, ENTRY)
    _, sources = processing.lesion_sources(config, 'BCB_MASKS', p)
    assert [s for s, _ in sources] == ['manual', 'synthstroke']
    assert dict(sources)['synthstroke'] == p['registration']/'SynthStroke_in_MNI.nii.gz'
    _, sources = processing.lesion_sources({**config, 'BCB_MASKS': 'linda'}, 'BCB_MASKS', p)
    assert [s for s, _ in sources] == ['linda']                     # an explicit choice is kept


def test_unselected_step_submits_no_job(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(scheduled, '_run_payloads', lambda *a, **k: pytest.fail('submitted a job'))
    study = Study({}, tmp_path, tmp_path)
    result = scheduled.submit_step('registration', [ENTRY], study)
    assert result['results'][0]['outputs'][0]['status'] == 'skipped'
    assert "LINDA's registration" in capsys.readouterr().out
    study = Study({'SEGMENTATION_METHODS': ['synthstroke']}, tmp_path, tmp_path)
    assert scheduled.submit_step('linda', [ENTRY], study)['results'][0]['outputs'][0]['reason'] == \
        'LINDA is not in SEGMENTATION_METHODS'


def test_registration_job_gets_its_threads():
    assert scheduled._resources('registration', {'config': {'REGISTRATION_THREADS': 8}}) == ['--cpus-per-task=8']
    with pytest.raises(ValueError):
        processing.registration_threads({'REGISTRATION_THREADS': 0})


def test_unselected_step_is_skipped_inside_a_job(tmp_path, monkeypatch):
    monkeypatch.setenv('SLURM_JOB_ID', '1')
    monkeypatch.setitem(processing.STEPS, 'linda', lambda *a: pytest.fail('ran LINDA'))
    request = {'dataset': str(tmp_path), 'config': {'SEGMENTATION_METHODS': ['synthstroke']}, 'entries': [ENTRY]}
    [result] = processing.process('linda', request)
    assert result['outputs'] == [{'status': 'skipped', 'reason': 'LINDA is not in SEGMENTATION_METHODS'}]


def test_guided_form_checkboxes_set_the_methods():
    base = dict(DATASET_SOURCE='openneuro', SUBJECT_FILTER='sub-1', SESSION_FILTER='', MAX_SUBJECTS=0)
    values = normalize_selection({**base, '_method_linda': False, '_method_synthstroke': True})
    assert values['SEGMENTATION_METHODS'] == ['synthstroke'] and '_method_linda' not in values
    with pytest.raises(ValueError, match='at least one'):
        normalize_selection({**base, '_method_linda': False, '_method_synthstroke': False})


def test_methods_table_describes_the_registration_used():
    steps = lambda config: dict(zip(methods_table(config)['Step'], methods_table(config)['Tool']))
    assert 'LINDA' in steps({})['Template registration']
    without = steps({'SEGMENTATION_METHODS': ['synthstroke']})
    assert 'antsRegistrationSyN' in without['Template registration']
    assert 'Lesion segmentation (LINDA)' not in without
