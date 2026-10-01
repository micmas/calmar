"""Isolated JupyterLab smoke test. No real acquisition or imaging is executed.

Install tests/requirements-browser.txt and run `python -m playwright install chromium`.
Then run this file from the repository root. The server and fixture kernels are
owned by this test and are stopped afterward. Screenshots/logs go to --artifacts.
"""
import argparse
import asyncio
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
from urllib.request import urlopen
from uuid import uuid4

import nbformat as nb
from playwright.async_api import async_playwright, expect

ROOT = Path(__file__).resolve().parents[1]


async def exercise(base, token, root, artifacts, *, notebook_prefix='', auth_token=''):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(args=['--no-sandbox'])
        page = await browser.new_page(viewport={'width': 1400, 'height': 1000},
            extra_http_headers={'Authorization': 'token '+auth_token} if auth_token else {})
        if auth_token:
            async def local_authorization(route):
                headers = dict(route.request.headers)
                if not route.request.url.startswith(base+'/'):
                    headers.pop('authorization', None)
                await route.continue_(headers=headers)
            await page.route('**/*', local_authorization)
        page.on('dialog', lambda dialog: dialog.accept())
        async def open_run(name):
            await page.goto(f'{base}/lab/workspaces/{uuid4().hex}/tree/{notebook_prefix}{name}?token={token}')
            cell = page.locator('.jp-Notebook .jp-CodeCell').first
            try:
                await cell.wait_for(timeout=10000)
            except Exception:
                await page.reload()
                await cell.wait_for(timeout=30000)
            # Neurodesk's collaborative frontend connects a newly created
            # kernel asynchronously. Reopen once after that first handshake,
            # as users do after installing the widget extension.
            await page.wait_for_timeout(2000)
            await page.reload()
            await cell.wait_for(timeout=60000)
            await page.wait_for_timeout(2000)
            await cell.click()
            await page.keyboard.press('Shift+Enter')
        async def output(text):
            await page.locator('.jp-OutputArea-output').get_by_text(text, exact=True).wait_for(timeout=30000)
        try:
            await open_run('navigation.ipynb')
            button = page.get_by_role('button', name='Continue to batch', exact=True)
            await button.wait_for(timeout=30000)
            await page.get_by_text('Notebook controls could not connect:', exact=False).first.wait_for()
            assert not await page.locator('.jp-OutputArea-output').get_by_text('BATCH_RAN', exact=True).count()
            # The bridge is rendered after the button; allow its ready comm.
            await page.wait_for_timeout(1500)
            await page.locator('.jp-Notebook .jp-CodeCell').last.click()
            await button.click()
            await output('BATCH_RAN')
            await page.get_by_role('button', name='Do QC', exact=True).click()
            await page.get_by_role('button', name='Skip QC', exact=True).click()
            await page.get_by_text('QC was skipped by the user.', exact=False).wait_for()
            assert not await page.locator('.jp-OutputArea-output').get_by_text('MUST_NOT_RUN', exact=True).count()
            await page.screenshot(path=str(artifacts/'navigation.png'), full_page=True)

            await open_run('guided-fixture.ipynb')
            start = page.get_by_role('button', name='Start workflow', exact=True)
            await start.wait_for(timeout=30000)
            await page.wait_for_timeout(1000)
            source = page.locator('.widget-dropdown').filter(has_text='Input type:').locator('select')
            accession = page.locator('.widget-text').filter(has_text='OpenNeuro accession:')
            version = page.locator('.widget-text').filter(has_text='Dataset version:')
            local = page.locator('.widget-text').filter(has_text='Local dataset folder:')
            single = page.locator('.widget-text').filter(has_text='Single T1 file:')
            cohort = page.locator('.widget-text').filter(has_text='Participants (comma-separated):')
            sessions = page.locator('.widget-text').filter(has_text='Sessions (comma-separated):')
            random = page.locator('.widget-checkbox').filter(has_text='Randomly sample participants').locator('input')
            await accession.wait_for(state='visible')
            await single.wait_for(state='hidden')
            await local.wait_for(state='hidden')
            accession_value = await accession.locator('input').input_value()
            participant_value = await cohort.locator('input').input_value()
            session_value = await sessions.locator('input').input_value()
            await cohort.locator('input').fill('')
            await sessions.locator('input').fill('')
            await expect(random).to_be_checked()
            await expect(random).to_be_disabled()
            await page.get_by_text('Random selection:', exact=False).wait_for()
            await page.screenshot(path=str(artifacts/'random-inputs.png'), full_page=True)
            await cohort.locator('input').fill(participant_value)
            await sessions.locator('input').fill(session_value)
            await expect(random).to_be_enabled()
            await expect(random).not_to_be_checked()
            for mode in ('Single T1 file', 'Local BIDS', 'Flat T1 folder', 'OpenNeuro', 'Single T1 file'):
                await source.select_option(label=mode)
                for field, visible in ((accession,mode=='OpenNeuro'), (version,mode=='OpenNeuro'),
                                       (single,mode=='Single T1 file'),
                                       (local,mode in ('Local BIDS','Flat T1 folder')),
                                       (cohort,mode!='Single T1 file')):
                    await field.wait_for(state='visible' if visible else 'hidden', timeout=1500)
            assert await accession.locator('input').input_value() == accession_value
            fixture = root/'single_T1w.nii.gz'
            fixture.write_bytes(b'File-selection fixture only; no imaging is executed.')
            await single.locator('input').fill(str(fixture))
            await page.screenshot(path=str(artifacts/'inputs.png'), full_page=True)
            await start.click()
            await output('INPUTS_ACCEPTED')
            await expect(page.get_by_role('button', name='Do QC', exact=True)).to_have_count(1)
            await expect(page.get_by_role('button', name='Skip QC', exact=True)).to_have_count(1)
            # Workflow actions belong after the rating/save controls.
            save_box = await page.get_by_role('button', name='Save & next participant', exact=True).bounding_box()
            for label in ('Run skull-strip repair', 'Continue after QC'):
                action_box = await page.get_by_role('button', name=label, exact=True).bounding_box()
                assert action_box['y'] >= save_box['y'] + save_box['height']
            chosen = json.loads((root/'reports/guided-inputs.json').read_text())
            assert chosen['DATASET_SOURCE'] == 'single' and chosen['SINGLE_T1W'] == str(fixture)
            assert chosen['SUBJECT_FILTER'] is None and chosen['SESSION_FILTER'] is None
            assert chosen['MAX_SUBJECTS'] == 1 and chosen['TEST_SUBJECT_IDX'] == 0
            assert chosen['RANDOM_SAMPLE'] is False
            async def rate(label, number):
                row = page.locator('.widget-toggle-buttons').filter(has_text=label).filter(
                    has=page.get_by_role('button', name=str(number), exact=True)).first
                await row.get_by_role('button', name=str(number), exact=True).click()
            await rate('Skull strip / brain extraction', 3)
            await page.get_by_role('button', name='Save stage →', exact=True).click()
            await rate('LINDA lesion mask', 2)
            await rate('Manual mask → MNI warp', 1)
            await page.get_by_role('button', name='Save & next participant', exact=True).click()
            for _ in range(50):
                files = list((root/'ratings').rglob('*.qc.json'))
                if files and json.loads(files[0].read_text())['stages']['expert_mni_warp']['rating'] == 1:
                    break
                await page.wait_for_timeout(100)
            assert len(files) == 1
            record = json.loads(files[0].read_text())
            assert [record['stages'][s]['rating'] for s in ('skull_strip','lesion','expert_mni_warp')] == [3,2,1]
            assert record['marked_for_rerun'] is True
            view = page.locator('.widget-toggle-buttons').filter(has_text='View:').last
            assert 'Skull strip' in await view.locator('.mod-active').inner_text()
            await page.get_by_role('button', name='Skip QC', exact=True).click()
            await page.screenshot(path=str(artifacts/'qc.png'), full_page=True)
            await page.get_by_role('button', name='Continue after QC', exact=True).click()
            await output('AFTER_QC_RAN')
            assert not await page.locator('.jp-OutputArea-output').get_by_text('REPAIR_MUST_NOT_RUN', exact=True).count()

            await open_run('existing-qc.ipynb')
            use_existing = page.get_by_role('button', name='Use existing QC', exact=True)
            redo = page.get_by_role('button', name='Redo QC', exact=True)
            await use_existing.wait_for(timeout=30000)
            await expect(page.get_by_role('button', name='Do QC', exact=True)).to_have_count(0)
            await expect(page.get_by_role('button', name='Skip QC', exact=True)).to_have_count(1)
            await page.get_by_text('QC already exists for participants below.', exact=False).wait_for()
            saved = {p:p.read_bytes() for p in (root/'existing-ratings').rglob('*.qc.json')}
            assert len(saved) == 2
            await use_existing.scroll_into_view_if_needed()
            await page.screenshot(path=str(artifacts/'existing-qc.png'))
            await use_existing.click()
            await page.get_by_text('Existing QC kept. Review the unrated stages, starting here.', exact=True).wait_for()
            subject = page.get_by_role('combobox', name='Participant:', exact=True)
            assert 'sub-1' in await subject.locator('option:checked').inner_text()
            view = page.locator('.widget-toggle-buttons').filter(has_text='View:').last
            assert 'LINDA lesion' in await view.locator('.mod-active').inner_text()
            await redo.click()
            await page.get_by_text('Redoing QC from stage 1.', exact=False).wait_for()
            assert 'sub-0' in await subject.locator('option:checked').inner_text()
            assert 'Skull strip' in await view.locator('.mod-active').inner_text()
            assert all(path.read_bytes() == original for path, original in saved.items())
            await page.get_by_role('button', name='Skip QC', exact=True).click()
            await use_existing.click()
            await page.get_by_text('Existing QC kept. Review the unrated stages, starting here.', exact=True).wait_for()
            await page.get_by_role('button', name='Continue after QC', exact=True).click()
            await output('EXISTING_QC_CONTINUED')
            assert all(path.read_bytes() == original for path, original in saved.items())
            (artifacts/'failure.png').unlink(missing_ok=True)
            print('PASS: navigation, QC pause, input modes, rating saves, skip/continue, existing-QC reuse, redo from stage 1, and preservation of saved ratings.')
        except Exception:
            await page.screenshot(path=str(artifacts/'failure.png'), full_page=True)
            print((await page.locator('body').inner_text())[-7000:])
            if (root/'events.txt').exists(): print((root/'events.txt').read_text())
            raise
        finally:
            await browser.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--artifacts', type=Path, default=ROOT/'notes'/'browser-check')
    parser.add_argument('--server-url', help='Use a running local server; only disposable fixture sessions are touched.')
    parser.add_argument('--server-root', type=Path, default=Path('/home/jovyan'))
    args = parser.parse_args()
    args.artifacts.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='calmar-ui-', dir=ROOT/'notes' if args.server_url else None) as temporary:
        root = Path(temporary)
        prefix = f"import sys\nsys.path.insert(0, {str(ROOT)!r})\n"
        prefix += '''from pathlib import Path
from calmar.execution import pause_before_batch, pause_for_qc
class StopExecution(Exception):
    def _render_traceback_(self): return []
'''
        def code(source, role=None):
            return nb.v4.new_code_cell(source, metadata={'calmar': {'role': role}} if role else {})
        notebooks = {
            'navigation.ipynb': [code(prefix+'''checkpoint = pause_before_batch()
# Fail this view's first registry lookup, then exercise recovery via the button.
checkpoint.navigation._esm = checkpoint.navigation._esm.replace(
    "const FrontEnd = await manager.loadClass",
    "if (!window.__calmar_connection_attempted) { window.__calmar_connection_attempted = true; throw Error('Fixture: extension still loading'); } const FrontEnd = await manager.loadClass")
checkpoint.button.on_click(lambda _: Path('events.txt').open('a').write('click ready='+str(checkpoint.navigation.ready)+'\\n'))
checkpoint.navigation.on_msg(lambda _, data, buffers: Path('events.txt').open('a').write(str(data)+'\\n'))
raise StopExecution("Paused")'''),
                code('print("BATCH_RAN")\nqc = pause_for_qc([dict(subject="sub-fixture", session="ses-1")], lambda e: Path("qc"))\nraise StopExecution("QC paused")', 'batch-start'),
                code('print("MUST_NOT_RUN")')],
            'guided-fixture.ipynb': [code(prefix+'from calmar.guided import show_inputs\nshow_inputs(globals())'),
                code('''print("INPUTS_ACCEPTED")
import ipywidgets as w
from calmar.qc_panel import QCPanel
class Viewer(w.HTML):
    def load_volumes(self, volumes): self.value = "Preview fixture — no image processing"
entries = [dict(subject=f"sub-{i}", session="ses-1") for i in range(2)]
directory = lambda e: Path("ratings") / e["subject"] / e["session"]
gate = pause_for_qc(entries, directory, display_controls=False)
panel = QCPanel(entries, lambda e: ["skull_strip", "lesion", "expert_mni_warp"],
    lambda e: directory(e) / "Lesion_in_MNI.nii.gz", lambda *a: [], Viewer(), gate)
display(panel)
raise StopExecution("QC paused")''', 'guided-start'),
                code('print("REPAIR_MUST_NOT_RUN")', 'skull-repair'),
                code('print("AFTER_QC_RAN")', 'after-qc')],
        }
        existing_fixture = prefix + '''import ipywidgets as w
from calmar.qc import QCRecord
from calmar.qc_panel import QCPanel
class Viewer(w.HTML):
    def load_volumes(self, volumes): self.value = "Preview fixture — no image processing"
entries = [dict(subject=f"sub-{i}", session="ses-1") for i in range(2)]
directory = lambda e: Path("existing-ratings") / e["subject"] / e["session"]
anchor = lambda e: directory(e) / "Lesion_in_MNI.nii.gz"
for i, e in enumerate(entries):
    record = QCRecord.load(anchor(e))
    record.subject, record.session = e['subject'], e['session']
    record.reviewer, record.reviewed_on = 'Previous reviewer', '2026-09-01'
    for stage in (["skull_strip", "lesion", "expert_mni_warp"] if i == 0 else ["skull_strip"]):
        record.set_stage(stage, rating=1, notes='Existing review')
    record.save()
gate = pause_for_qc(entries, directory, display_controls=False)
panel = QCPanel(entries, lambda e: ["skull_strip", "lesion", "expert_mni_warp"],
    anchor, lambda *a: [], Viewer(), gate)
display(panel)
raise StopExecution("QC choice required")'''
        notebooks['existing-qc.ipynb'] = [code(existing_fixture),
            code('print("EXISTING_QC_CONTINUED")', 'after-qc')]
        # Use this environment's kernel name, rather than relying on its display label.
        kernel = 'conda-base-py' if Path('/opt/conda').exists() else 'python3'
        for name, cells in notebooks.items():
            nb.write(nb.v4.new_notebook(cells=cells, metadata={'kernelspec': {
                'display_name':'Python', 'language':'python', 'name':kernel}}), root/name)
        if args.server_url:
            import requests
            from urllib.parse import urlparse
            base = args.server_url.rstrip('/')
            if urlparse(base).hostname not in ('127.0.0.1', 'localhost'):
                raise ValueError('The running-server check requires a loopback URL.')
            auth = os.environ.get('CALMAR_BROWSER_TOKEN') or os.environ.get('JUPYTERHUB_API_TOKEN', '')
            notebook_prefix = root.relative_to(args.server_root).as_posix()+'/'
            try:
                asyncio.run(exercise(base, '', root, args.artifacts,
                    notebook_prefix=notebook_prefix, auth_token=auth))
            finally:
                headers = {'Authorization': 'token '+auth}
                response = requests.get(base+'/api/sessions', headers=headers, timeout=10)
                response.raise_for_status()
                for session in response.json():
                    if session.get('path', '').startswith(notebook_prefix):
                        requests.delete(base+'/api/sessions/'+session['id'], headers=headers, timeout=10).raise_for_status()
            return
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0)); port = sock.getsockname()[1]
        token = uuid4().hex
        base = f'http://127.0.0.1:{port}'
        with (args.artifacts/'server.log').open('w') as log:
            server = subprocess.Popen([sys.executable, '-m', 'jupyterlab', '--no-browser', '--ip=127.0.0.1',
                f'--port={port}', f'--ServerApp.root_dir={root}', f'--ServerApp.preferred_dir={root}',
                f'--FileContentsManager.preferred_dir={root}', f'--IdentityProvider.token={token}'],
                cwd=root, stdout=log, stderr=subprocess.STDOUT)
            try:
                for _ in range(150):
                    if server.poll() is not None: raise RuntimeError('Test JupyterLab server exited; inspect server.log')
                    try:
                        with urlopen(f'{base}/api?token={token}', timeout=1): break
                    except OSError: time.sleep(.2)
                else: raise TimeoutError('Test JupyterLab did not start')
                asyncio.run(exercise(base, token, root, args.artifacts))
            finally:
                server.terminate()
                try: server.wait(timeout=20)
                except subprocess.TimeoutExpired: server.kill(); server.wait()


if __name__ == '__main__': main()
