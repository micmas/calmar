"""Real NiiVue rendering/restoration with a delayed bundle and tiny test image.

Uses disposable notebooks on a running loopback JupyterHub server. No analysis
or user notebook is executed. CALMAR_BROWSER_TOKEN or JUPYTERHUB_API_TOKEN
provides authentication; credentials are never written to logs.
"""
import argparse
import asyncio
import json
import io
import os
from pathlib import Path
import tempfile
from urllib.parse import urlparse
from uuid import uuid4

import nbformat as nb
import requests
from PIL import Image
from playwright.async_api import async_playwright
from jupyter_server.services.kernels.connection.base import deserialize_msg_from_ws_v1

ROOT = Path(__file__).resolve().parents[1]


async def exercise(base, token, relative, artifacts, busy_seconds=0):
    errors = []
    console = []
    sockets = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=['--no-sandbox', '--enable-unsafe-swiftshader'])
        page = await browser.new_page(viewport={'width':1200,'height':900},
            extra_http_headers={'Authorization':'token '+token})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda msg: console.append(msg.text[:1000]) if msg.type in ('error', 'warning') else None)
        def watch_socket(socket):
            record = {'path': urlparse(socket.url).path, 'closed': False, 'sent': [], 'received': []}
            sockets.append(record)
            socket.on('close', lambda: record.update(closed=True))
            def record_frame(direction, payload):
                try:
                    if isinstance(payload, bytes):
                        # Collaborative-document sockets also use binary frames;
                        # their first bytes are not a Jupyter offset count.
                        count = int.from_bytes(payload[:8], 'little')
                        if not 5 <= count <= min(64, len(payload) // 8):
                            raise ValueError('Not a Jupyter kernel frame')
                        channel, parts = deserialize_msg_from_ws_v1(payload)
                        message = dict(zip(('header', 'parent_header', 'metadata', 'content'),
                                           (json.loads(p) for p in parts[:4])))
                    else:
                        message = json.loads(payload)
                    content = message.get('content', {})
                    record[direction].append({
                        'type': message.get('header', {}).get('msg_type'),
                        'status': content.get('execution_state', content.get('status')),
                        'model': content.get('data', {}).get('state', {}).get('_model_name'),
                        'code': content.get('code', '')[:100],
                        'text': content.get('text', '')[:1000],
                    })
                except (ValueError, UnicodeDecodeError, AttributeError, IndexError):
                    record[direction].append({'binary_bytes': len(payload)})
            socket.on('framesent', lambda payload: record_frame('sent', payload))
            socket.on('framereceived', lambda payload: record_frame('received', payload))
        page.on('websocket', watch_socket)
        async def route_request(route):
            headers = dict(route.request.headers)
            if not route.request.url.startswith(base+'/'):
                headers.pop('authorization', None)
            if '/neurodesktop-ipyniivue.' in route.request.url:
                await asyncio.sleep(3)  # Exceeds anywidget's two-second model timeout.
            await route.continue_(headers=headers)
        await page.route('**/*', route_request)
        try:
            await page.goto(f'{base}/lab/workspaces/calmar-viewer-{uuid4().hex}/tree/{relative}')
            cell = page.locator('.jp-Notebook .jp-CodeCell').first
            try:
                await cell.wait_for(timeout=10000)
            except Exception:
                await page.reload()
                await cell.wait_for(timeout=30000)
            await page.wait_for_timeout(5000)
            await cell.click()
            started = asyncio.get_running_loop().time()
            await page.keyboard.press('Shift+Enter')
            control = page.get_by_role('checkbox', name='Show fixture')
            await control.wait_for(timeout=30000 + busy_seconds * 1000)
            await control.uncheck()
            await control.check()
            canvas = page.locator('.jp-Notebook canvas')
            await canvas.wait_for(timeout=45000 + busy_seconds * 1000)
            async def wait_for_image():
                # A WebGL canvas with crosshairs alone is not a loaded image.
                for _ in range(30):
                    shot = Image.open(io.BytesIO(await canvas.screenshot())).convert('RGB')
                    bright = sum(r > 50 and abs(r-g) < 10 and abs(g-b) < 10
                                 for r, g, b in shot.getdata())
                    if bright > 5000:
                        return
                    await page.wait_for_timeout(1000)
                raise AssertionError('Viewer canvas has no visible fixture image')
            await wait_for_image()
            elapsed = asyncio.get_running_loop().time() - started
            print(f'Image visible after {elapsed:.1f}s; simulated computation lasts {busy_seconds}s.', flush=True)
            if busy_seconds >= 30:
                assert elapsed < busy_seconds, 'Image waited for the kernel to finish'
            await page.get_by_text('VIEWER_READY', exact=True).wait_for(timeout=busy_seconds*1000+30000)
            await page.screenshot(path=str(artifacts/'viewer.png'))
            await page.get_by_role('button', name='Change image', exact=True).click()
            await page.get_by_text('Replacement selected', exact=True).wait_for(timeout=10000)
            await page.wait_for_timeout(2000)
            await page.screenshot(path=str(artifacts/'changed-viewer.png'))
            # The checkpoint must block batch work while allowing this earlier
            # image cell to close/rebuild its viewer and return to idle.
            await page.locator('.jp-Notebook .jp-CodeCell').last.click()
            await page.keyboard.press('Shift+Enter')
            await page.get_by_text('InputRejected:', exact=False).first.wait_for(timeout=15000)
            assert not await page.locator('.jp-OutputArea-output').get_by_text('BATCH_MUST_NOT_RUN', exact=True).count()
            await cell.click()
            await page.keyboard.press('Shift+Enter')
            await page.locator('.jp-OutputArea-output').get_by_text('VIEWER_READY', exact=True).wait_for(timeout=30000)
            await canvas.wait_for(timeout=45000)
            await control.uncheck()
            await control.check()
            await wait_for_image()
            assert '*' not in (await cell.locator('.jp-InputPrompt').inner_text())
            await page.screenshot(path=str(artifacts/'rerun-while-paused.png'))
            await page.reload()
            await canvas.wait_for(timeout=45000)
            await page.wait_for_timeout(2000)
            await control.uncheck()
            await control.check()
            await wait_for_image()
            assert not any('Failed to initialize model' in e for e in errors), errors
            assert not await page.get_by_text('Could not load the brain-image viewer:',exact=False).count()
            await page.screenshot(path=str(artifacts/'restored-viewer.png'))
            print('PASS: images load, change, rerun while batch stays paused, and restore with a delayed bundle.')
        except Exception:
            print('Browser errors:', errors)
            print('Console errors:', console[-10:])
            (artifacts/'websocket-events.json').write_text(json.dumps(sockets, indent=2))
            await page.screenshot(path=str(artifacts/'failure.png'))
            print((await page.locator('body').inner_text())[-5000:])
            raise
        finally:
            await browser.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server-url', required=True)
    parser.add_argument('--server-root', type=Path, default=Path('/home/jovyan'))
    parser.add_argument('--artifacts', type=Path, default=ROOT/'notes/browser-viewer')
    parser.add_argument('--busy-seconds', type=int, default=0,
                        help='Simulate a busy kernel after first displaying the viewer.')
    args = parser.parse_args()
    base = args.server_url.rstrip('/')
    if urlparse(base).hostname not in ('127.0.0.1','localhost'):
        raise ValueError('A loopback server URL is required.')
    token = os.environ.get('CALMAR_BROWSER_TOKEN') or os.environ['JUPYTERHUB_API_TOKEN']
    args.artifacts.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='calmar-viewer-',dir=ROOT/'notes') as temp:
        path = Path(temp)/'viewer.ipynb'
        source = f'''# CALMAR_CELL_ID: calmar-step-35
import sys
sys.path.insert(0, {str(ROOT)!r})
import numpy as np
import nibabel as nib
import ipywidgets as w
from calmar import widgets as cw
cw.configure(url_base=False)
grid = np.indices((64,64,64)) - 32
data = np.maximum(0, 900 - (grid*grid).sum(axis=0)).astype(np.float32)
data += np.random.default_rng(7).uniform(0, 1, data.shape).astype(np.float32)
nib.save(nib.Nifti1Image(data, np.eye(4)), 'viewer-fixture.nii.gz')
nv = cw.show('fixture', [{{'path':'viewer-fixture.nii.gz'}}], height=350)
toggle = w.Checkbox(value=True, description='Show fixture')
toggle.observe(lambda c: setattr(nv.volumes[0], 'opacity', float(c['new'])), names='value')
change = w.Button(description='Change image')
status = w.HTML()
def replace(_):
    nv.load_volumes([{{'path':'viewer-fixture.nii.gz', 'colormap':'hot'}}])
    status.value = 'Replacement selected'
change.on_click(replace)
display(w.VBox([toggle, change, status, nv]))
fixture_runs = globals().get('fixture_runs', 0) + 1
if fixture_runs == 1:
    import time
    time.sleep({args.busy_seconds})
from calmar.execution import pause_before_batch
gate = pause_before_batch()
assert gate.paused
_restorable_state = w.Widget.get_manager_state()
print('VIEWER_READY')
'''
        nb.write(nb.v4.new_notebook(cells=[nb.v4.new_code_cell(source, id='calmar-step-35'),
            nb.v4.new_code_cell("# CALMAR_CELL_ID: calmar-step-42\nprint('BATCH_MUST_NOT_RUN')",
                                id='calmar-step-42', metadata={'calmar': {'role': 'batch-start'}})],metadata={
            'kernelspec':{'name':'conda-base-py','display_name':'Python','language':'python'}}), path)
        relative = path.relative_to(args.server_root).as_posix()
        try:
            asyncio.run(exercise(base,token,relative,args.artifacts,args.busy_seconds))
        finally:
            headers={'Authorization':'token '+token}
            response=requests.get(base+'/api/sessions',headers=headers,timeout=10)
            response.raise_for_status()
            for session in response.json():
                if session.get('path') == relative:
                    requests.delete(base+'/api/sessions/'+session['id'],headers=headers,timeout=10).raise_for_status()


if __name__ == '__main__':
    main()
