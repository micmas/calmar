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
        for number in (23,25,27,29,30,32,34,35,39):
            with self.subTest(cell=number):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    exec(''.join(source_cell(number)['source']), {"RUN_TEST": False, "CONFIG": {"RUN_TEST": False}})
                self.assertEqual(output.getvalue(), 'RUN_TEST = False — continuing into batch processing\n')

    def test_guided_defaults_preserve_selected_cohort(self):
        config = defaults()
        self.assertEqual(config['MAX_SUBJECTS'], 3)
        self.assertCountEqual(config['SUBJECT_FILTER'], ['sub-M2066','sub-M2075','sub-M2176'])

    def test_navigation_targets_exist_once_in_each_notebook(self):
        for name in ('calmar-guided.ipynb', 'lesion-interpretation-pipeline.ipynb'):
            notebook = json.loads((ROOT/name).read_text())
            roles = [c.get('metadata', {}).get('calmar', {}).get('role') for c in notebook['cells']]
            for role in ('batch-start', 'skull-repair', 'after-qc'):
                self.assertEqual(roles.count(role), 1, (name, role))

    def test_cached_hdbet_preview_loads_anatomy_and_thresholded_mask_once(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            t1 = root/'T1w.nii.gz'; t1.write_bytes(b'fixture')
            mask = root/'T1w_brain_mask.nii.gz'; mask.write_bytes(b'fixture')
            show = Mock(return_value=SimpleNamespace(volumes=[SimpleNamespace(),SimpleNamespace()]))
            ns = dict(CONFIG={'RUN_TEST':True}, SUBJECTS=[dict(subject='sub-test',session=None,t1w=t1)],
                Path=Path, cm=masks, q=SimpleNamespace(), importlib=importlib,
                hdbet_path_for=lambda e:root, cw=SimpleNamespace(show=show),
                widgets=ipywidgets, display=lambda *a:None, HTML=lambda s:s)
            with patch.object(importlib,'reload',lambda m:m):
                exec(''.join(source_cell(23)['source']),ns)
            show.assert_called_once()
            volumes=show.call_args.args[1]
            self.assertEqual(volumes[0], {'path':str(t1)})
            self.assertEqual(volumes[1]['cal_min'], .5)
            self.assertEqual(volumes[1]['cal_max'], 1.)
            ns['_hdbet_overlay'].value=False
            self.assertEqual(show.return_value.volumes[1].opacity, 0.)

    def test_local_inputs_keep_derivatives_under_selected_dataset(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary); dataset=root/'local'; dataset.mkdir()
            ns=dict(Path=Path, os=os, cw=SimpleNamespace(configure=lambda **kw:None),
                _CALMAR_CONFIG_OVERRIDES={'PROJECT_DIR':root,'DATASET_SOURCE':'local','LOCAL_DATASET':dataset})
            with contextlib.redirect_stdout(io.StringIO()), patch.dict(os.environ):
                exec(''.join(source_cell(12)['source']),ns)
            self.assertEqual(ns['RAW_DATASET_DIR'],dataset)
            self.assertEqual(ns['DERIV_DIR'],dataset/'derivatives/linda')


class GuidedRunnerTests(unittest.IsolatedAsyncioTestCase):
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
             patch('calmar.guided.source_cell',side_effect=lambda n,c:dict(cell_type='code',source=[sources[n]])), \
             patch('calmar.guided.get_ipython',return_value=InteractiveShell.instance()), \
             patch('calmar.guided.display'):
            with self.assertRaisesRegex(ValueError,'stop'):
                await run_cells([1,2,3],ns)
        self.assertEqual(ns['value'],8)

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
