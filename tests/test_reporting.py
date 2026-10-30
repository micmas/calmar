import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import nibabel as nib
import numpy as np
import pandas as pd
import pytest

from calmar.reporting import execute, pack, unpack, run_reporting_task


def image(path, data, affine=None):
    nib.save(nib.Nifti1Image(np.asarray(data, dtype=np.uint8), np.eye(4) if affine is None else affine), path)
    return str(path)


def test_reporting_requires_scheduler(tmp_path, monkeypatch):
    monkeypatch.delenv('SLURM_JOB_ID', raising=False)
    with pytest.raises(RuntimeError, match='sbatch'):
        execute({'task': 'group'}, tmp_path)


def test_comparison_restores_metrics_and_outlines_without_changing_inputs(tmp_path, monkeypatch):
    monkeypatch.setenv('SLURM_JOB_ID', 'fixture')
    manual = np.zeros((5,5,5), dtype=np.uint8); manual[1:4,1:4,1:4] = 1
    auto = manual.copy(); auto[0,0,0] = 1
    paths = [image(tmp_path/'manual.nii.gz', manual), image(tmp_path/'auto.nii.gz', auto)]
    before = [Path(p).read_bytes() for p in paths]
    out = tmp_path/'out'; out.mkdir()
    result = execute({'task': 'comparison', 'manual': paths[0], 'automatic': {'LINDA': paths[1]}, 'coreg': None}, out)
    assert result['manual_voxels'] == 27
    assert result['metrics']['LINDA']['dice'] == pytest.approx(54/55)
    assert result['metrics']['LINDA']['sens'] == 1
    assert np.count_nonzero(nib.load(result['outlines']['LINDA']).get_fdata()) == 27
    assert [Path(p).read_bytes() for p in paths] == before


def test_group_resamples_shifted_affine_and_keeps_denominator(tmp_path, monkeypatch):
    monkeypatch.setenv('SLURM_JOB_ID', 'fixture')
    data = np.zeros((5,5,5), dtype=np.uint8); data[2,2,2] = 1
    shifted = np.eye(4); shifted[0,3] = 1
    paths = [image(tmp_path/'one.nii.gz', data), image(tmp_path/'two.nii.gz', data, shifted)]
    out = tmp_path/'out'; out.mkdir()
    with patch('nilearn.datasets.load_mni152_template', return_value=nib.load(paths[0])):
        result = execute({'task': 'group', 'masks': paths, 'threshold': .5}, out)
    frequency = nib.load(result['map']).get_fdata()
    assert result['used'] == 2
    assert frequency[2,2,2] == frequency[3,2,2] == .5
    assert frequency.sum() == 1


def test_decoding_dataframe_survives_json_transport():
    original = {'term_decoding': pd.DataFrame({'term': ['language'], 'r': [.23]}), 'available': True}
    restored = unpack(json.loads(json.dumps(pack(original))))
    pd.testing.assert_frame_equal(original['term_decoding'], restored['term_decoding'])


def test_client_passes_explicit_request_without_running_computation(tmp_path):
    with patch('calmar.scheduled.run_step_sync', return_value={'value': {'ok': True}}) as submit:
        assert run_reporting_task({'PROJECT_DIR': tmp_path}, 'group', masks=['mask.nii.gz'], threshold=.5) == {'ok': True}
    stage, namespace = submit.call_args.args
    assert stage == 'reporting'
    assert namespace['_operation_request']['task'] == 'group'


def test_decode_client_resolves_legacy_relative_kb_to_selected_root(tmp_path):
    kb_root = Path(__file__).resolve().parents[1] / 'stroke-aphasia-kb'
    with patch('calmar.kb_location.resolve_kb_root',
               return_value=(kb_root, 'CALMaR submodule')), \
            patch('calmar.scheduled.run_step_sync', return_value={'value': {'ok': True}}) as submit:
        result = run_reporting_task({'PROJECT_DIR': tmp_path}, 'decode', mask='mask.nii.gz',
                                    dataset='data', kb_root='stroke-aphasia-kb')
    assert result == {'ok': True}
    request = submit.call_args.args[1]['_operation_request']
    assert request['kb_root'] == str(kb_root)
    assert request['kb_reason'] == 'CALMaR submodule'


def test_decode_output_records_selected_kb_provenance(tmp_path, monkeypatch):
    monkeypatch.setenv('SLURM_JOB_ID', 'fixture')
    kb_root = Path(__file__).resolve().parents[1] / 'stroke-aphasia-kb'
    fake_module = SimpleNamespace(KnowledgeBase=lambda root: SimpleNamespace(
        decode_lesion=lambda mask, verbose: {'neurosynth_available': False, 'warnings': []}))
    output = tmp_path / 'out'
    output.mkdir()
    state = {'commit': 'abc123', 'date': '2026-10-27', 'uncommitted': True}
    with patch('calmar.kb_paths.load_kb_modules', return_value=(fake_module,)), \
            patch('calmar.acquisition.ensure_nifti_content', return_value=True), \
            patch('calmar.kb_location.kb_git_state', return_value=state):
        result = execute({'task': 'decode', 'mask': 'mask.nii.gz', 'dataset': 'data',
                          'kb_root': str(kb_root), 'kb_reason': 'CALMaR submodule'}, output)
    expected = {'root': str(kb_root), 'reason': 'CALMaR submodule', **state}
    assert result['knowledge_base'] == expected
    assert json.loads((output / 'decoding.json').read_text())['knowledge_base'] == expected


def test_atlas_setup_reuses_published_maps_until_selection_or_force_changes(tmp_path):
    from calmar.reporting import load_atlases
    path = tmp_path/'atlas.nii.gz'; path.write_bytes(b'published fixture')
    namespace = {'PROJECT_DIR': tmp_path, 'ATLAS_DIR': tmp_path, 'CONFIG': {'ATLASES': ['Test']}}
    with patch('calmar.reporting.run_reporting_task', return_value={
            'Test': {'maps': str(path), 'labels': {'1': 'ROI'}}}) as run:
        first = load_atlases(namespace)
        assert load_atlases(namespace) is first
        run.assert_called_once()
        load_atlases(namespace, force=True)
        assert run.call_count == 2


def test_report_reopen_reuses_disk_cache_but_changed_input_or_output_rebuilds(tmp_path):
    mask = tmp_path/'mask.nii.gz'; mask.write_bytes(b'original input')
    png = tmp_path/'comparison.png'; png.write_bytes(b'published result')
    ns = {'PROJECT_DIR': tmp_path}
    with patch('calmar.scheduled.run_step_sync', return_value={'value': {'png': str(png)}, 'job':'fixture'}) as run:
        for _ in range(2):
            assert run_reporting_task(dict(ns), 'report_overlay', mask=str(mask))['png'] == str(png)
        assert run.call_count == 1
        mask.write_bytes(b'changed input')
        run_reporting_task(ns, 'report_overlay', mask=str(mask))
        assert run.call_count == 2
        png.write_bytes(b'changed output')
        run_reporting_task(ns, 'report_overlay', mask=str(mask))
        assert run.call_count == 3
