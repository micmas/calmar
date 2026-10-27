import contextlib
import io
import json
from pathlib import Path
import unittest
import tempfile
from types import SimpleNamespace
from unittest.mock import Mock, patch
import os
import importlib
import asyncio
import ipywidgets
from calmar import masks
from calmar.guided import run_cells
from IPython.core.interactiveshell import InteractiveShell
from calmar.guided import defaults, source_cell

ROOT = Path(__file__).resolve().parents[1]


class GuidedWorkflowTests(unittest.TestCase):
    def test_every_disabled_test_cell_only_prints_continuation(self):
        for number in (20,23,25,27,"calmar-registration","calmar-openads","calmar-manual",
                       "calmar-single-optional",32,34,35,39):
            with self.subTest(cell=number):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    exec(''.join(source_cell(number)['source']), {"RUN_TEST": False, "CONFIG": {"RUN_TEST": False}})
                self.assertEqual(output.getvalue(), 'RUN_TEST = False — continuing into batch processing\n')

    def test_guided_defaults_preserve_selected_cohort(self):
        config = defaults()
        self.assertEqual(config['MAX_SUBJECTS'], 5)
        self.assertCountEqual(config['SUBJECT_FILTER'],
                              ['sub-M2002', 'sub-M2051', 'sub-M2061', 'sub-M2075', 'sub-M2103'])
        self.assertCountEqual(config['ADDITIONAL_COHORTS'][0]['SUBJECT_FILTER'],
                              ['sub-strokecase0004', 'sub-strokecase0009'])

    def test_navigation_targets_exist_once_in_each_notebook(self):
        for name in ('calmar-guided.ipynb', 'lesion-interpretation-pipeline.ipynb'):
            notebook = json.loads((ROOT/name).read_text())
            roles = [role for c in notebook['cells'] for role in {
                c.get('metadata', {}).get('calmar', {}).get('role'),
                *c.get('metadata', {}).get('calmar', {}).get('roles', [])}]
            for role in ('batch-start', 'skull-repair', 'after-qc', 'after-dwi-qc', 'dmri-choice', 'brain-health-choice', 'report-prepare',
                         'report-setup', 'single-test-selection', 'single-test-start'):
                self.assertEqual(roles.count(role), 1, (name, role))

    def test_optional_dwi_uses_the_qc_viewer_only(self):
        source = ''.join(source_cell('calmar-optional-dwi')['source'])
        self.assertIn('show_step(dwi_openads, DWI_STUDY', source)
        self.assertIn('viewer=False', source)
        self.assertIn('open_qc_review(', source)

    def test_optional_analyses_run_in_single_test_and_are_not_repeated_in_batch(self):
        guided = json.loads((ROOT/'calmar-guided.ipynb').read_text())
        source = ''.join(next(cell for cell in guided['cells']
                              if cell.get('id') == 'calmar-guided-single-test')['source'])
        self.assertLess(source.index('calmar-manual'), source.index('calmar-single-optional'))
        self.assertLess(source.index('calmar-single-optional'), source.index('calmar-step-32'))
        for cell_id in ('calmar-optional-dwi', 'calmar-direct-dmri', 'calmar-brain-health'):
            self.assertIn('pending_optional_entries', ''.join(source_cell(cell_id)['source']))

    def test_single_test_runs_every_selected_optional_route(self):
        stages = []
        test_entry = {'subject': 'sub-one', 'session': 'ses-t1'}
        dwi_entry = {'subject': 'sub-one', 'session': 'ses-dwi',
                     'anatomical_session': 'ses-t1', 'dwi': 'dwi.nii.gz'}
        dmri_entry = {'subject': 'sub-one', 'session': 'ses-dmri',
                      'anatomical_session': 'ses-t1', 'dwi': 'dmri.nii.gz'}
        health_entry = {'subject': 'sub-one', 'session': 'ses-t1',
                        'brain_health_components': ['atrophy', 'wmh']}

        def submit(stage, entries, study, timings):
            stages.append((stage, tuple(entries), study))
            return SimpleNamespace(stage=stage)

        namespace = {
            'RUN_TEST': True, 'CONFIG': {'MODALITY': 't1'},
            'SUBJECTS': [test_entry], 'TEST_SUBJECT_IDX': 0,
            'DWI_SUBJECTS': [dwi_entry], 'DMRI_SUBJECTS': [dmri_entry],
            'BRAIN_HEALTH_SUBJECTS': [health_entry],
            'DWI_STUDY': SimpleNamespace(config={}, dataset='.'),
            'DMRI_STUDY': SimpleNamespace(config={}, dataset='.'),
            'study': SimpleNamespace(config={}, dataset='.'), 'BATCH_TIMINGS': {},
            'submit_step': submit, 'show_step': lambda *args, **kwargs: None,
        }
        with patch('calmar.scheduled._result_stamps', return_value={}):
            exec(''.join(source_cell('calmar-single-optional')['source']), namespace)

        self.assertEqual([stage for stage, _, _ in stages], [
            'acquisition', 'openads', 'dmri_preproc', 'dmri_recon', 'dmri_metrics',
            'brain_health_anatomy', 'brain_health_wmh', 'brain_health_metrics'])
        self.assertEqual(set(namespace['_SINGLE_OPTIONAL_COMPLETED']),
                         {'dwi', 'dmri', 'brain_health'})

    def test_optional_failure_does_not_block_other_single_test_routes(self):
        stages = []
        test_entry = {'subject': 'sub-one', 'session': 'ses-t1'}
        dwi_entry = {'subject': 'sub-one', 'session': 'ses-dwi',
                     'anatomical_session': 'ses-t1', 'dwi': 'dwi.nii.gz'}
        health_entry = {'subject': 'sub-one', 'session': 'ses-t1',
                        't1w': 't1.nii.gz', 'brain_health_components': ['atrophy']}

        def submit(stage, entries, study, timings):
            stages.append(stage)
            if stage == 'openads':
                raise RuntimeError('OpenADS failed')
            return {'stage': stage, 'request': {'entries': entries}, 'results': []}

        namespace = {
            'RUN_TEST': True, 'CONFIG': {'MODALITY': 't1'}, 'SUBJECTS': [test_entry],
            'TEST_SUBJECT_IDX': 0, 'DWI_SUBJECTS': [dwi_entry], 'DMRI_SUBJECTS': [],
            'BRAIN_HEALTH_SUBJECTS': [health_entry], 'DWI_STUDY': SimpleNamespace(
                config={}, dataset='.', config_for=lambda entry: {}, dataset_for=lambda entry: '.'),
            'DMRI_STUDY': None, 'study': SimpleNamespace(
                config={}, dataset='.', config_for=lambda entry: {}, dataset_for=lambda entry: '.',
                masks=lambda entry: {}),
            'BATCH_TIMINGS': {}, 'submit_step': submit,
            'show_step': lambda *args, **kwargs: None,
        }
        with patch('calmar.scheduled._result_stamps', return_value={}):
            exec(''.join(source_cell('calmar-single-optional')['source']), namespace)

        self.assertIn('brain_health_metrics', stages)
        self.assertNotIn('brain_health_wmh', stages)
        self.assertEqual(namespace['DWI_ERROR'], 'OpenADS failed')
        self.assertNotIn('dwi', namespace['_SINGLE_OPTIONAL_COMPLETED'])
        self.assertIn('brain_health', namespace['_SINGLE_OPTIONAL_COMPLETED'])

    def test_optional_dwi_batch_skips_reusable_test_entry_but_qcs_every_entry(self):
        from calmar.single_subject import mark_optional_completed

        class StopExecution(Exception):
            pass

        first = {'subject': 'sub-one', 'session': 'ses-dwi',
                 'anatomical_session': 'ses-t1', 't1w': 'first_dwi.nii.gz',
                 'dwi': 'first_dwi.nii.gz', 'adc': 'first_adc.nii.gz'}
        second = {'subject': 'sub-two', 'session': 'ses-dwi',
                  'anatomical_session': 'ses-t1', 't1w': 'second_dwi.nii.gz',
                  'dwi': 'second_dwi.nii.gz', 'adc': 'second_adc.nii.gz'}
        study = SimpleNamespace(config={'OVERWRITE': True}, dataset='.')
        completed = {}
        submitted = []

        def submit(stage, entries, selected_study, timings):
            submitted.append((stage, list(entries)))
            return {'stage': stage, 'request': {'entries': list(entries)}, 'results': []}

        namespace = {
            'CONFIG': {'MODALITY': 't1'}, 'DWI_SUBJECTS': [first, second],
            'DWI_STUDY': study, '_SINGLE_OPTIONAL_COMPLETED': completed,
            'BATCH_TIMINGS': {}, 'submit_step': submit,
            'show_step': lambda *args, **kwargs: None,
            'cw': SimpleNamespace(fresh_viewer=lambda *args, **kwargs: 'viewer', vols='volumes'),
            'StopExecution': StopExecution,
        }
        with patch('calmar.scheduled._result_stamps', return_value={}), \
             patch('calmar.qc_panel.open_qc_review') as review:
            mark_optional_completed(completed, 'dwi', [first], study,
                                    [{'stage': 'openads', 'request': {'entries': [first]}, 'results': []}])
            with self.assertRaises(StopExecution):
                exec(''.join(source_cell('calmar-optional-dwi')['source']), namespace)

        self.assertEqual([(stage, entries) for stage, entries in submitted],
                         [('acquisition', [second]), ('openads', [second])])
        self.assertEqual(review.call_args.args[0], [first, second])

    def test_mixed_atlas_tables_include_each_route_source(self):
        source = ''.join(source_cell('calmar-step-69')['source'])
        self.assertIn('config_for_entry(CONFIG, entry)', source)
        self.assertIn('analysis_mask_sources', source)

    def test_cached_hdbet_preview_loads_anatomy_and_thresholded_mask_once(self):
        from calmar import review
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            t1 = root/'T1w.nii.gz'; t1.write_bytes(b'fixture')
            mask = root/'T1w_brain_mask.nii.gz'; mask.write_bytes(b'fixture')
            show = Mock(return_value=SimpleNamespace(volumes=[SimpleNamespace(),SimpleNamespace()]))
            displayed = []
            with patch('calmar.review.display', side_effect=lambda *a: displayed.extend(a)):
                review.show_brain_mask(dict(subject='sub-test', session=None, t1w=t1), root, SimpleNamespace(show=show))
            show.assert_called_once()
            volumes=show.call_args.args[1]
            self.assertEqual(volumes[0], {'path':str(t1)})
            self.assertEqual(volumes[1]['cal_min'], .5)
            self.assertEqual(volumes[1]['cal_max'], 1.)
            toggle = next(d for d in displayed if isinstance(d, ipywidgets.Checkbox))
            toggle.value=False
            self.assertEqual(show.return_value.volumes[1].opacity, 0.)

    def test_local_inputs_keep_derivatives_under_selected_dataset(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary); dataset=root/'local'; dataset.mkdir()
            ns=dict(Path=Path, os=os, cw=SimpleNamespace(configure=lambda **kw:None), display=lambda *a: None,
                _CALMAR_CONFIG_OVERRIDES={'PROJECT_DIR':root,'DATASET_SOURCE':'local','LOCAL_DATASET':dataset})
            with contextlib.redirect_stdout(io.StringIO()), patch.dict(os.environ):
                exec(''.join(source_cell(12)['source']),ns)
            self.assertEqual(ns['RAW_DATASET_DIR'],dataset)
            self.assertEqual(ns['DERIV_DIR'],dataset/'derivatives/linda')

    def test_isles_source_uses_the_selected_local_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            dataset = root/'ISLES-2022'; dataset.mkdir()
            ns = dict(Path=Path, os=os, cw=SimpleNamespace(configure=lambda **kw:None), display=lambda *a: None,
                _CALMAR_CONFIG_OVERRIDES={'PROJECT_DIR':root, 'DATASET_SOURCE':'isles2022',
                                          'LOCAL_DATASET':dataset, 'MODALITY':'t1'})
            with contextlib.redirect_stdout(io.StringIO()), patch.dict(os.environ):
                exec(''.join(source_cell(12)['source']), ns)
            self.assertEqual(ns['RAW_DATASET_DIR'], dataset)
            self.assertEqual(ns['CONFIG']['MODALITY'], 'dwi')


class GuidedRunnerTests(unittest.IsolatedAsyncioTestCase):
    async def test_navigation_reconnects_stale_ready_state_and_reports_timeout(self):
        from calmar.notebook_navigation import NotebookNavigation
        retry = Mock()
        nav = NotebookNavigation(ipywidgets.HTML(), on_error=retry)
        self.addCleanup(nav.close)
        nav.ready = True
        nav.send = Mock()
        callback = Mock()
        nav.request('report-setup', callback)
        nav.send.assert_called_once_with(dict(action='connect'))
        callback.assert_not_called()
        nav._connection_timeout()
        self.assertIn('did not respond', nav.message.value)
        retry.assert_called_once()
        callback.assert_not_called()

    async def test_navigation_retries_connection_and_prepares_once(self):
        from calmar.notebook_navigation import NotebookNavigation
        nav = NotebookNavigation(ipywidgets.HTML())
        self.addCleanup(nav.close)
        nav.send = Mock()
        callback = Mock(return_value=True)
        nav._receive(None, {'event':'error', 'connection':True, 'message':'Extension loading'}, [])
        self.assertTrue(nav.request('guided-start', callback))
        nav.send.assert_called_once_with(dict(action='connect'))
        callback.assert_not_called()
        nav._receive(None, {'event':'ready'}, [])
        nav._receive(None, {'event':'ready'}, [])
        prepared = [c.args[0] for c in nav.send.call_args_list if c.args[0]['action'] == 'prepare']
        self.assertEqual(len(prepared), 1)
        self.assertEqual(prepared[0]['role'], 'guided-start')
        callback.assert_not_called()
        nav._receive(None, {'event':'approved'}, [])
        await asyncio.sleep(.01)
        callback.assert_called_once()
        nav.send.assert_called_with(dict(action='execute'))

    async def test_awaitable_steps_share_namespace_and_stop_on_failure(self):
        sources={1:'import asyncio\nawait asyncio.sleep(0)\nvalue = 7',
                 2:'value += 1\nraise ValueError("stop")', 3:'value = 999'}
        ns={}
        with patch('calmar.guided.notebook_cells',return_value=[]), \
             patch('calmar.guided.source_cell',side_effect=lambda n,c:dict(id=f'calmar-step-{n:02}',cell_type='code',source=[sources[n]])), \
             patch('calmar.guided.get_ipython',return_value=InteractiveShell.instance()), \
             patch('calmar.guided.display'):
            with self.assertRaisesRegex(ValueError,'stop'):
                await run_cells([1,2,3],ns)
        self.assertEqual(ns['value'],8)
        self.assertEqual(list(ns['STEP_TIMINGS']), ['calmar-step-01', 'calmar-step-02'])

    async def test_frontend_continuation_waits_until_queue_cancellation_finishes(self):
        from calmar.notebook_navigation import NotebookNavigation
        nav=NotebookNavigation(ipywidgets.HTML())
        self.addCleanup(nav.close)
        kernel=SimpleNamespace(_aborting=True)
        nav.send=Mock()
        callback=Mock(return_value=True)
        nav.pending=callback
        with patch('IPython.get_ipython',return_value=SimpleNamespace(kernel=kernel)):
            nav._receive(None,{'event':'approved'},[])
        await asyncio.sleep(.02)
        nav.send.assert_not_called()
        kernel._aborting=False
        await asyncio.sleep(.02)
        callback.assert_called_once()
        nav.send.assert_called_once_with(dict(action='execute'))
