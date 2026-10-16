"""Saved QC evidence: figures are written and metrics/flags are plausible."""
import nibabel as nib
import numpy as np

from calmar import step_qc
from calmar.study import derivative_dirs


def save(path, data, affine=np.eye(4)):
    path.parent.mkdir(parents=True, exist_ok=True)
    nib.save(nib.Nifti1Image(data.astype('float32'), affine), path)
    return path


def fixture(tmp_path):
    entry = {'subject': 'sub-a', 'session': 'ses-1', 't1w': str(tmp_path/'T1w.nii.gz')}
    dirs = derivative_dirs(tmp_path, {}, entry)
    shape = (40, 40, 40)
    t1 = np.random.default_rng(0).random(shape) + 1
    save(tmp_path/'T1w.nii.gz', t1)
    brain = np.zeros(shape); brain[5:35, 5:35, 5:35] = 1
    save(dirs['hdbet']/'T1w_brain_mask.nii.gz', brain)
    lesion = np.zeros(shape); lesion[10:16, 10:16, 10:16] = 1
    save(dirs['linda']/'Prediction3_native.nii.gz', lesion)
    synth = np.zeros(shape); synth[11:17, 10:16, 10:16] = 1; synth[0:3, 0:3, 0:3] = 1
    save(dirs['synthstroke']/'prediction_lesion_mask.nii.gz', synth)
    return entry, dirs


def test_lesion_figures_metrics_and_flags(tmp_path):
    entry, dirs = fixture(tmp_path)
    linda = step_qc.stage_evidence('linda', entry, dirs, tmp_path/'reports')
    assert linda['metrics']['linda_volume_ml'] == 0.22  # 216 voxels of 1 mm^3
    assert linda['metrics']['linda_components'] == 1
    with open(linda['png'], 'rb') as f:
        assert f.read(8) == b'\x89PNG\r\n\x1a\n'
    synth = step_qc.stage_evidence('synthstroke', entry, dirs, tmp_path/'reports')
    assert synth['metrics']['synthstroke_components'] == 2
    assert 0.7 < synth['metrics']['dice_synthstroke_vs_linda'] < 0.9
    # Tool behaviour is reported, not flagged: the workflow checks only the workflow.
    assert synth['metrics']['synthstroke_fraction_outside_brain'] > .05
    assert synth['flags'] == []


def test_brain_volume_flag_and_cross_session_manual(tmp_path):
    entry, dirs = fixture(tmp_path)
    brain = step_qc.stage_evidence('brain', entry, dirs, tmp_path/'reports')
    assert brain['metrics']['brain_volume_ml'] == 27.0
    assert any('implausible' in f for f in brain['flags'])  # a 27 ml "brain": wrong input or voxel size
    shape = (40, 40, 40)
    manual = np.zeros(shape); manual[10:16, 10:16, 10:16] = 1
    save(dirs['linda']/'_manual_mask_compare'/'ManualLesion_in_T1_sitk.nii.gz', manual)
    info = {'mask_session': 'ses-2', 't1_session': 'ses-1', 'mask_space': 'other'}
    ev = step_qc.stage_evidence('manual', entry, dirs, tmp_path/'reports', manual_info=info)
    assert ev['metrics']['dice_linda_vs_manual'] == 1.0
    assert (ev['metrics']['linda_covers_manual'], ev['metrics']['linda_inside_manual']) == (1.0, 1.0)
    assert any('cross-session' in f for f in ev['flags'])


def test_missing_outputs_produce_no_evidence(tmp_path):
    entry = {'subject': 'sub-b', 'session': None, 't1w': str(tmp_path/'none.nii.gz')}
    dirs = derivative_dirs(tmp_path, {}, entry)
    assert step_qc.stage_evidence('linda', entry, dirs, tmp_path) is None
    assert step_qc.stage_evidence('acquisition', entry, dirs, tmp_path) is None


def test_disconnectome_qc_uses_only_produced_maps(tmp_path):
    entry, dirs = fixture(tmp_path)
    shape = (40, 40, 40)
    save(dirs['linda']/'Subject_in_MNI.nii.gz', np.random.default_rng(1).random(shape))
    heat = np.zeros(shape); heat[10:20, 10:20, 10:20] = .8
    produced = save(dirs['deepdisco']/'DeepDisco_linda_association.nii.gz', heat)
    save(dirs['deepdisco']/'DeepDisco_expert_whole_brain.nii.gz', heat)  # old file, not in this run
    outputs = [{'path': str(produced), 'status': 'computed'},
               {'status': 'stale', 'reason': 'Stale output preserved at x'}]
    ev = step_qc.stage_evidence('deepdisco', entry, dirs, tmp_path/'r', outputs=outputs)
    assert set(ev['metrics']) == {'linda_voxels_above_0.5'}  # association model used; manual map ignored
    assert ev['png'] and ev['complete']
    assert any('Stale' in f for f in ev['flags'])
    empty = save(dirs['bcbtoolkit']/'Disconnectome_linda.nii.gz', np.zeros(shape))
    ev = step_qc.stage_evidence('bcb', entry, dirs, tmp_path/'r', outputs=[{'path': str(empty), 'status': 'cached'}])
    assert any('empty' in f for f in ev['flags'])


def test_failed_figure_is_marked_incomplete(tmp_path, monkeypatch):
    entry, dirs = fixture(tmp_path)
    monkeypatch.setattr(step_qc, '_linda', lambda *a: (_ for _ in ()).throw(OSError('disk full')))
    ev = step_qc.stage_evidence('linda', entry, dirs, tmp_path)
    assert ev['complete'] is False and 'disk full' in ev['flags'][0]


def test_template_correlation_runs_on_a_template_grid_image(tmp_path, monkeypatch):
    from calmar import templates
    from nilearn import datasets
    tpl = datasets.load_mni152_template(resolution=2)
    data = np.asanyarray(tpl.dataobj).astype('float32')
    monkeypatch.setattr(templates, 'T1_BRAIN', save(tmp_path/'tpl.nii.gz', data, tpl.affine))
    monkeypatch.setattr(templates, 'BRAIN_MASK', save(tmp_path/'tplmask.nii.gz', (data > data.mean()).astype('float32'), tpl.affine))
    path = save(tmp_path/'Subject_in_MNI.nii.gz', data, tpl.affine)
    r, mask = step_qc.template_correlation(path)
    assert r > 0.99 and mask.any()          # the template correlates with itself
    shuffled = save(tmp_path/'noise.nii.gz', np.random.default_rng(0).random(data.shape), tpl.affine)
    assert step_qc.template_correlation(shuffled)[0] < step_qc.TEMPLATE_CORR_MIN


def test_render_failure_is_marked_incomplete(tmp_path, monkeypatch):
    entry, dirs = fixture(tmp_path)
    monkeypatch.setattr(step_qc, 'figure', lambda *a, **k: (_ for _ in ()).throw(OSError('cannot write png')))
    ev = step_qc.stage_evidence('linda', entry, dirs, tmp_path)
    assert ev['complete'] is False and ev['metrics']['linda_components'] == 1


def test_workflow_checks_for_warps_and_manual_registration(tmp_path):
    assert step_qc.warp_check('linda', 100, 120) == []
    assert 'transform' in step_qc.warp_check('linda', 100, 15)[0]
    entry, dirs = fixture(tmp_path)
    shape = (40, 40, 40)
    t1 = np.zeros(shape); t1[8:32, 8:32, 8:32] = 1 + np.random.default_rng(2).random((24, 24, 24))  # head + background
    save(tmp_path/'T1w.nii.gz', t1)
    brain = np.zeros(shape); brain[12:28, 12:28, 12:28] = 1
    save(dirs['hdbet']/'T1w_brain_mask.nii.gz', brain)
    cavity = np.zeros(shape); cavity[8:14, 10:16, 10:16] = 1     # inside the head, partly outside the brain mask
    save(dirs['linda']/'_manual_mask_compare'/'ManualLesion_in_T1_sitk.nii.gz', cavity)
    ok = step_qc.stage_evidence('manual', entry, dirs, tmp_path/'r', manual_info={'mask_session': 'ses-1'})
    assert ok['metrics']['manual_fraction_outside_brain'] > 0 and ok['flags'] == []   # cavity: not a failure
    misplaced = np.zeros(shape); misplaced[0:6, 0:6, 0:6] = 1    # in the background: registration failed
    save(dirs['linda']/'_manual_mask_compare'/'ManualLesion_in_T1_sitk.nii.gz', misplaced)
    bad = step_qc.stage_evidence('manual', entry, dirs, tmp_path/'r', manual_info={'mask_session': 'ses-1'})
    assert any('registration failed' in f for f in bad['flags'])
