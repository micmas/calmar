"""Interactive viewer under each processing step (replaces the QC thumbnails)."""
from pathlib import Path
from types import SimpleNamespace

import nibabel as nib
import numpy as np
import pytest

from calmar import step_viewer as sv
from calmar.step_summary import show_step


def save(path, value=1):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = np.zeros((6, 6, 6), dtype='uint8'); data[2:4, 2:4, 2:4] = value
    nib.save(nib.Nifti1Image(data, np.eye(4)), path)
    return path


@pytest.fixture
def study(tmp_path):
    d = {k: tmp_path/k for k in ('hdbet', 'linda', 'synthstroke', 'bcbtoolkit', 'deepdisco')}
    save(d['hdbet']/'sub-1_T1w_brain_mask.nii.gz')
    save(d['linda']/'Subject_in_MNI.nii.gz')
    save(d['bcbtoolkit']/'Disconnectome_linda.nii.gz')
    masks = {'linda': {'T1w': save(d['linda']/'Prediction3_native.nii.gz'),
                       'MNI': save(d['linda']/'Lesion_in_MNI.nii.gz')},
             'synthstroke': {'T1w': save(d['synthstroke']/'prediction_lesion_mask.nii.gz')}}
    d['template'] = d['linda']
    return SimpleNamespace(dirs=lambda e: d, hdbet_dir=lambda e: d['hdbet'], masks=lambda e: masks)


def entry(tmp_path, subject='sub-1'):
    return {'subject': subject, 'session': None, 't1w': str(save(tmp_path/f'{subject}_T1w.nii.gz', 50))}


def test_layers_per_step(tmp_path, study):
    e = entry(tmp_path)
    background, layers = sv.step_layers('brain', e, study)
    assert background == Path(e['t1w']) and [l['name'] for l in layers] == ['HD-BET brain mask']
    _, layers = sv.step_layers('synthstroke', e, study)
    assert [(l['name'], l['shown']) for l in layers] == [('SynthStroke lesion', True), ('LINDA lesion', False)]
    background, layers = sv.step_layers('bcb', e, study)
    assert background.name == 'Subject_in_MNI.nii.gz'
    assert [(l['role'], l['group']) for l in layers] == [('map', 'linda'), ('lesion', 'linda')]  # only maps that exist
    with pytest.raises(ValueError):
        sv.step_layers('reporting', e, study)


def test_registration_viewer_offers_processed_manual_mask(tmp_path, study):
    study.dirs(None)['registration'] = study.dirs(None)['template']
    manual = save(tmp_path/'linda'/'ExpertMask_in_MNI.nii.gz')
    study.masks(None)['manual'] = {'MNI': manual}
    _, layers = sv.step_layers('registration', entry(tmp_path), study)
    assert [(layer['name'], layer['origin']) for layer in layers][-1] == ('Manual lesion', 'manual')
    assert layers[-1]['path'] == manual and not layers[-1]['shown']


def test_controls_describe_the_layers_and_keep_choices(tmp_path, study, monkeypatch):
    import ipywidgets
    viewer = ipywidgets.HTML()                                           # stands in for NiiVue
    viewer.opts, viewer.volumes = SimpleNamespace(), []
    loads = []
    def set_volumes(nv, specs):
        loads.append(specs)
        nv.volumes = [ipywidgets.HTML() for _ in specs]                  # widgets with model ids
    monkeypatch.setattr(sv.cw, 'fresh_viewer', lambda key, **kw: viewer)
    monkeypatch.setattr(sv.cw, 'set_volumes', set_volumes)
    monkeypatch.setattr(sv, 'display', lambda *a: None)
    shown = sv.show_step_viewer('linda', [entry(tmp_path), entry(tmp_path, 'sub-2')], study)
    controls = shown['controls']
    assert shown['participant'].layout.display == ''                     # menu for several participants
    assert [s['opacity'] > 0 for s in loads[0][1:]] == [True, False]      # brain mask starts hidden
    assert [l['model_id'] for l in controls.layers] == [v.model_id for v in viewer.volumes[1:]]
    assert controls.layers[0]['centre'] is not None and controls.layers[1]['centre'] is None
    assert [r['label'] for r in controls.roles] == ['LINDA lesion', 'Brain mask']
    controls.roles = [{**r, 'shown': True} for r in controls.roles]      # ticked in the browser
    shown['participant'].value = 1
    assert len(loads) == 2 and all(s['opacity'] > 0 for s in loads[1][1:])   # choice kept


def test_disconnectome_steps_choose_one_lesion_source(tmp_path, study, monkeypatch):
    import ipywidgets
    viewer = ipywidgets.HTML(); viewer.opts, viewer.volumes = SimpleNamespace(), []
    save(tmp_path/'synthstroke'/'SynthStroke_in_MNI.nii.gz')
    save(tmp_path/'bcbtoolkit'/'Disconnectome_synthstroke.nii.gz')
    study.masks(None)['synthstroke']['MNI'] = tmp_path/'synthstroke'/'SynthStroke_in_MNI.nii.gz'
    def set_volumes(nv, specs):
        nv.volumes = [ipywidgets.HTML() for _ in specs]
    monkeypatch.setattr(sv.cw, 'fresh_viewer', lambda key, **kw: viewer)
    monkeypatch.setattr(sv.cw, 'set_volumes', set_volumes)
    monkeypatch.setattr(sv, 'display', lambda *a: None)
    controls = sv.show_step_viewer('bcb', [entry(tmp_path)], study)['controls']
    assert controls.groups == [['LINDA', 'linda'], ['SynthStroke', 'synthstroke']]
    assert [r['key'] for r in controls.roles] == ['map', 'lesion']
    assert [controls.visible(l) for l in controls.layers] == [True, True, False, False]
    controls.group = 'synthstroke'
    assert [controls.visible(l) for l in controls.layers] == [False, False, True, True]


def test_crosshair_fraction_matches_niivue_ras_grid(tmp_path):
    from calmar.layer_controls import mm_to_frac
    affine = np.array([[-2., 0, 0, 10], [0, 0, 1, -5], [0, 3, 0, 7], [0, 0, 0, 1]])   # flipped, permuted
    path = tmp_path/'oblique.nii.gz'
    nib.save(nib.Nifti1Image(np.zeros((4, 5, 6), dtype='uint8'), affine), path)
    voxel = np.array([1, 2, 3])
    mm = (affine @ [*voxel, 1])[:3]
    # RAS grid: x flipped (4 voxels), y = third axis (6), z = second axis (5).
    expected = [(4 - 1 - 1 + .5) / 4, (3 + .5) / 6, (2 + .5) / 5]
    assert np.allclose(mm_to_frac(path, mm), expected)


def test_show_step_opens_the_viewer_for_participants_with_outputs(monkeypatch):
    calls = []
    monkeypatch.setattr(sv, 'show_step_viewer', lambda stage, entries, study: calls.append((stage, entries)))
    monkeypatch.setattr('calmar.step_summary.display', lambda *a: None)
    one, two = {'subject': 'sub-1', 't1w': 'a'}, {'subject': 'sub-2', 't1w': 'b'}
    result = {'stage': 'linda', 'request': {'entries': [one, two]},
              'results': [{'subject': 'sub-1', 'outputs': [{'path': 'x'}]}, {'subject': 'sub-2', 'outputs': []}]}
    show_step(result, object())
    assert calls == [('linda', [one])]
    show_step({**result, 'stage': 'reporting'}, object())                 # no viewer for this step
    assert len(calls) == 1


def test_manual_metrics_read_as_a_few_lines():
    from calmar.step_summary import _metric_lines
    metrics = {'mask_space': 'other', 'mask_session': 'ses-529', 't1_session': 'ses-602',
               'manual_volume_ml': 25.4, 'manual_components': 4, 'manual_fraction_outside_brain': 0.01,
               'manual_fraction_outside_head': 0, 'dice_linda_vs_manual': 0.323,
               'dice_synthstroke_vs_manual': 0.743, 'manual_mni_volume_ml': 36.1, 'dice_linda_vs_manual_mni': 0.32}
    assert _metric_lines(metrics) == [
        ('Manual mask', 'drawn on another scan, rigidly registered to this T1 (mask from ses-529, T1 from ses-602)'),
        ('Manual lesion', '25.4 ml in 4 blobs, 36.1 ml in template, 1% outside brain mask, 0% outside head'),
        ('Agreement (Dice)', 'LINDA vs Manual <b>0.32</b> · LINDA vs Manual (template) <b>0.32</b> · '
                             'SynthStroke vs Manual <b>0.74</b>')]
    assert _metric_lines({'odd_metric': 2}) == [('odd_metric', '2')]          # unknown metrics still shown


def test_deepdisco_viewer_chooses_lesion_source_and_model(tmp_path, study, monkeypatch):
    import ipywidgets
    viewer = ipywidgets.HTML(); viewer.opts, viewer.volumes = SimpleNamespace(), []
    for model in ('whole_brain', 'projection'):
        save(tmp_path/'deepdisco'/f'DeepDisco_linda_{model}.nii.gz')
    def set_volumes(nv, specs):
        nv.volumes = [ipywidgets.HTML() for _ in specs]
    monkeypatch.setattr(sv.cw, 'fresh_viewer', lambda key, **kw: viewer)
    monkeypatch.setattr(sv.cw, 'set_volumes', set_volumes)
    monkeypatch.setattr(sv, 'display', lambda *a: None)
    controls = sv.show_step_viewer('deepdisco', [entry(tmp_path)], study)['controls']
    assert controls.variants == [['Whole brain', 'whole_brain'], ['Projection', 'projection']]
    assert [(l['role'], l['variant']) for l in controls.layers] == [('map', 'whole_brain'), ('map', 'projection'), ('lesion', '')]
    assert [controls.visible(l) for l in controls.layers] == [True, False, True]
    controls.variant = 'projection'                                        # map follows, lesion stays
    assert [controls.visible(l) for l in controls.layers] == [False, True, True]


def test_manual_viewer_offers_the_registered_reference_scan(tmp_path, study):
    save(tmp_path/'linda'/'_manual_mask_compare'/'T2_in_T1_sitk.nii.gz', 80)
    _, layers = sv.step_layers('manual', entry(tmp_path), study)
    assert (layers[-1]['name'], layers[-1]['kind'], layers[-1]['shown']) == ('Registered reference scan', 'scan', False)
    assert sv._spec(layers[-1], True)['colormap'] == 'gray'


def test_manual_metrics_explain_a_low_dice():
    from calmar.step_summary import _metric_lines
    lines = dict(_metric_lines({'manual_volume_ml': 131.0, 'linda_volume_ml': 221.6, 'dice_linda_vs_manual': 0.568,
                                'linda_covers_manual': 0.765, 'linda_inside_manual': 0.452}))
    assert lines['Versus manual'] == ('LINDA covers 76% of the manual lesion and 45% of LINDA lies inside it '
                                      '(1.7× the manual volume: larger)')


def test_new_background_reloads_overlays_it_would_otherwise_reuse(tmp_path):
    """NiiVue keeps "loading" when a held overlay is put over a new background
    (another participant over the same template mask): reload the overlays."""
    from calmar import widgets
    a, b, template = (save(tmp_path/f'{n}.nii.gz') for n in ('a', 'b', 'template'))
    viewer = SimpleNamespace(volumes=[])
    widgets.set_volumes(viewer, [{'path': str(a)}, {'path': str(template)}])
    first_template = viewer.volumes[1]
    widgets.set_volumes(viewer, [{'path': str(a)}, {'path': str(template), 'opacity': 0}])
    assert viewer.volumes[1] is first_template                     # same background: reused
    widgets.set_volumes(viewer, [{'path': str(b)}, {'path': str(template)}])
    assert viewer.volumes[1] is not first_template                 # new background: reloaded
