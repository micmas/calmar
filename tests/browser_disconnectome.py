"""Exercise the real comparison cell in a disposable notebook, using cached files."""
import asyncio
import io
import json
from pathlib import Path
import tempfile
from uuid import uuid4

import nbformat
import requests
from PIL import Image
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]


async def exercise(base, token, relative, artifacts):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(args=['--no-sandbox', '--enable-unsafe-swiftshader'])
        page = await browser.new_page(viewport={'width': 1400, 'height': 1400},
                                     extra_http_headers={'Authorization': 'token '+token})
        errors, files = [], []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('request', lambda r: files.append(r.url.split('?')[0]) if '.nii.gz' in r.url else None)
        async def route_request(route):
            headers = dict(route.request.headers)
            if not route.request.url.startswith(base+'/'):
                headers.pop('authorization', None)
            if '/neurodesktop-ipyniivue.' in route.request.url:
                response = await route.fetch(headers=headers)
                body = await response.text()
                # Expose this disposable viewer for browser assertions only.
                body = body.replace('async function Hg(A,I,B){',
                                    'async function Hg(A,I,B){window.__calmarTestNv=A;')
                await route.fulfill(response=response, body=body)
                return
            await route.continue_(headers=headers)
        await page.route('**/*', route_request)
        try:
            await page.goto(f'{base}/lab/workspaces/calmar-review-{uuid4().hex}/tree/{relative}')
            cell = page.locator('.jp-Notebook .jp-CodeCell').first
            await cell.wait_for(timeout=30000)
            await page.wait_for_timeout(4000)
            await cell.click()
            await page.keyboard.press('Shift+Enter')
            await page.get_by_role('button', name='Centre on lesion', exact=True).wait_for(timeout=45000)
            canvas = cell.locator('canvas')
            await canvas.wait_for(timeout=45000)
            await canvas.scroll_into_view_if_needed()
            async def image_ready():
                for _ in range(30):
                    if await canvas.is_visible():
                        im = Image.open(io.BytesIO(await canvas.screenshot())).convert('RGB')
                        if sum(r > 50 and abs(r-g) < 10 and abs(g-b) < 10 for r,g,b in im.getdata()) > 5000:
                            return
                    await page.wait_for_timeout(500)
                raise AssertionError('No visible anatomy')
            await image_ready()
            await page.get_by_role('button', name='DeepDisco', exact=True).click()
            await page.wait_for_function("window.__calmarTestNv?.volumes[2]?.opacity === 0 && window.__calmarTestNv?.volumes[3]?.opacity > 0")
            await page.get_by_role('button', name='Centre on lesion', exact=True).click()
            await page.wait_for_timeout(1500)
            position = await page.evaluate('Array.from(window.__calmarTestNv.scene.crosshairPos)')
            await cell.locator('.jp-OutputArea').first.screenshot(path=str(artifacts/'before-model-change.png'))
            before = list(files)
            started = asyncio.get_running_loop().time()
            await cell.locator('select').nth(2).select_option(label='commissural')
            await page.wait_for_function("window.__calmarTestNv?.volumes.length === 4 && window.__calmarTestNv.volumes[3].name.includes('commissural')")
            state = await page.evaluate("window.__calmarTestNv.volumes.map(v => ({name:v.name, opacity:v.opacity, min:v.cal_min, max:v.cal_max, imageLength:v.img?.length}))")
            print('Browser layers:', json.dumps(state), flush=True)
            assert position == await page.evaluate('Array.from(window.__calmarTestNv.scene.crosshairPos)')
            await image_ready()
            await page.wait_for_timeout(1500)
            assert 'mod-active' in (await page.get_by_role('button', name='DeepDisco', exact=True).get_attribute('class'))
            assert 'mod-active' not in (await page.get_by_role('button', name='BCBToolkit', exact=True).get_attribute('class'))
            await cell.locator('.jp-OutputArea').first.screenshot(path=str(artifacts/'after-model-change.png'))
            fetched = files[len(before):]
            assert not any('Subject_in_MNI' in p or 'Disconnectome_linda' in p or 'Lesion_in_MNI' in p for p in fetched), fetched
            # A known JupyterLab workspace-restoration warning precedes cell execution.
            unexpected = [e for e in errors if e != 'restore() must be called before `first` has resolved.']
            assert not unexpected, unexpected
            result = dict(model_change_seconds=round(asyncio.get_running_loop().time()-started, 2),
                          new_image_requests=[Path(p).name for p in fetched], page_errors=errors)
            (artifacts/'browser.json').write_text(json.dumps(result, indent=2))
            print(json.dumps(result))
        except Exception:
            await page.screenshot(path=str(artifacts/'failure.png'))
            raise
        finally:
            await browser.close()


def main():
    for config in sorted((Path.home()/'.local/share/jupyter/runtime').glob('jpserver-*.json'),
                         key=lambda p: p.stat().st_mtime, reverse=True):
        cfg = json.loads(config.read_text())
        if 'token' not in cfg: continue
        base = f"http://127.0.0.1:{cfg['port']}{cfg['base_url'].rstrip('/')}"
        token = cfg['token']
        if requests.get(base+'/api/sessions', headers={'Authorization':'token '+token}, timeout=5).ok:
            break
    else:
        raise RuntimeError('No active local Jupyter server found')
    artifacts = ROOT/'notes/disconnectome-review'
    artifacts.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='review-viewer-', dir=ROOT/'notes') as temp:
        path = Path(temp)/'review.ipynb'
        source = f'''import sys, json
from pathlib import Path
sys.path.insert(0, {str(ROOT)!r})
import nibabel as nib
import numpy as np
import ipywidgets as widgets
from IPython.display import HTML, display, clear_output
from calmar import widgets as cw, masks as cm
ROOT=Path({str(ROOT)!r})
cw.configure()
SUBJECTS=[dict(subject='sub-M2066',session='ses-235')]
RUN_TEST=True
TEST_SUBJECT_IDX=0
def folder(e, tool): return ROOT/'data/ds004884/derivatives'/tool/e['subject']/e['session']/'anat'
def deriv_path_for(e): return folder(e,'linda')
def bcb_path_for(e): return folder(e,'bcbtoolkit')
def deepdisco_path_for(e): return folder(e,'deepdisco')
def mask_inventory_for(e): return cm.discover_masks(e,folder(e,'linda'),folder(e,'synthstroke'))
n=json.loads((ROOT/'lesion-interpretation-pipeline.ipynb').read_text())
exec(''.join(next(c for c in n['cells'] if c['id']=='calmar-step-35')['source']))
'''
        nbformat.write(nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(source)], metadata={
            'kernelspec': {'name':'conda-base-py', 'display_name':'Python', 'language':'python'}}), path)
        relative = path.relative_to(Path.home()).as_posix()
        try:
            asyncio.run(exercise(base, token, relative, artifacts))
        finally:
            headers = {'Authorization': 'token '+token}
            for session in requests.get(base+'/api/sessions', headers=headers, timeout=10).json():
                if session.get('path') == relative:
                    requests.delete(base+'/api/sessions/'+session['id'], headers=headers, timeout=10).raise_for_status()


if __name__ == '__main__':
    main()
