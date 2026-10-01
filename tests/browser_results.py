"""Exercise the results/report UI on tiny fixtures in an isolated live notebook."""
import argparse
import asyncio
import os
from pathlib import Path
import tempfile
from uuid import uuid4

import nbformat
import requests
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]


async def check(base, token, relative, artifacts):
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=['--no-sandbox','--enable-unsafe-swiftshader'])
        page = await browser.new_page(viewport={'width':1000,'height':850}, extra_http_headers={'Authorization':'token '+token})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        async def authorize(route):
            headers = dict(route.request.headers)
            if not route.request.url.startswith(base+'/'):
                headers.pop('authorization', None)
            await route.continue_(headers=headers)
        await page.route('**/*', authorize)
        try:
            await page.goto(f'{base}/lab/workspaces/calmar-results-{uuid4().hex}/tree/{relative}')
            first = page.locator('.jp-Notebook .jp-CodeCell').first
            await first.wait_for(timeout=30000)
            await first.click()
            await page.keyboard.press('Shift+Enter')
            build = page.get_by_role('button', name='Build selected group map')
            await build.wait_for(timeout=45000)
            await build.scroll_into_view_if_needed()
            assert await build.is_enabled()
            await page.screenshot(path=str(artifacts/'group-controls.png'))
            print('Group controls visible.', flush=True)
            await build.click()
            await page.get_by_text('Group map mask source: synthstroke', exact=False).wait_for(timeout=15000)
            await page.locator('.jp-Notebook canvas').first.wait_for(timeout=45000)
            # The two atlas panels expose the same complete, labelled choices.
            atlas = page.get_by_role('combobox', name='Atlas:', exact=True)
            mask = page.get_by_role('combobox', name='Mask:', exact=True)
            await atlas.first.select_option(index=1)
            await mask.first.select_option(index=1)
            await page.get_by_role('heading', name='Atlas B — Manual mask — sub-ui', exact=True).wait_for()
            await page.get_by_role('heading', name='Atlas B — Manual mask — sub-ui', exact=True).scroll_into_view_if_needed()
            await page.screenshot(path=str(artifacts/'atlas-table.png'))
            await mask.nth(1).select_option(index=1)  # Schaefer network summary
            await atlas.nth(1).select_option(index=1)
            await mask.nth(2).select_option(index=1)
            await page.get_by_role('tab', name='Brain and selected mask', exact=True).click()
            await page.wait_for_timeout(1500)
            await page.get_by_role('button', name='Export selected atlas PDF', exact=True).click()
            await page.get_by_role('link', name='Download selected atlas PDF').wait_for(timeout=15000)
            await page.get_by_role('combobox', name='Lesion mask:', exact=True).select_option(label='Manual')
            await page.get_by_role('combobox', name='Display atlas:', exact=True).select_option(index=1)
            print('Atlas choices and PDF export work.', flush=True)
            generate = page.get_by_role('button', name='Generate participant report')
            await generate.scroll_into_view_if_needed()
            await page.screenshot(path=str(artifacts/'report-inputs.png'))
            await generate.click()
            await page.get_by_role('heading', name='Fixture report: manual · Atlas B', exact=True).wait_for(timeout=30000)
            await page.get_by_role('tab', name='Brain viewer', exact=True).click()
            result_area = page.locator('.jp-Notebook .jp-CodeCell').nth(1).locator('.jp-OutputArea')
            await result_area.locator('canvas').wait_for(timeout=45000)
            await result_area.locator('canvas').scroll_into_view_if_needed()
            await page.wait_for_timeout(2000)
            await result_area.screenshot(path=str(artifacts/'participant-report.png'))
            await page.get_by_role('button', name='Choose another report', exact=True).click()
            await page.get_by_role('button', name='Generate participant report').wait_for(timeout=30000)
            selected = page.get_by_role('combobox', name='Lesion mask:', exact=True).locator('option:checked')
            assert await selected.inner_text() == 'Manual'
            assert not any('Failed to initialize model' in e for e in errors), errors
            assert not await page.get_by_text('Could not load the brain-image viewer:', exact=False).count()
            print('PASS: visible group build; atlas/mask choices and titles; selected PDF export; report form navigates and renders.')
        except Exception:
            print('Browser errors:', errors)
            print((await page.locator('body').inner_text())[-7000:])
            await page.screenshot(path=str(artifacts/'failure.png'))
            raise
        finally:
            await browser.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server-url', required=True)
    parser.add_argument('--artifacts', type=Path, default=ROOT/'notes/browser-results-report')
    args = parser.parse_args()
    base = args.server_url.rstrip('/')
    if not base.startswith(('http://127.0.0.1:', 'http://localhost:')):
        raise ValueError('A loopback server is required.')
    token = os.environ['JUPYTERHUB_API_TOKEN']
    args.artifacts.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='calmar-results-', dir=ROOT/'notes') as temp:
        first = f'''import sys
sys.path.insert(0, {str(ROOT)!r})
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime
import textwrap
import numpy as np
import pandas as pd
import nibabel as nib
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from calmar import widgets as cw
from calmar.guided import source_cell
cw.configure(url_base=False)
root = Path.cwd()
DERIV_DIR = REPORTS_DIR = ATLAS_DIR = root
SUBJECTS = [dict(subject='sub-ui', session=None)]
CONFIG = dict(DEFAULT_ATLAS='Atlas A', LESION_THRESHOLD=.5)
data = np.zeros((24,24,24), dtype=np.float32)
data[5:19,5:19,5:19] = 1
img = nib.Nifti1Image(data, np.eye(4))
for name in ('Subject_in_MNI','mni152_t1_2mm','linda','synthstroke','manual','Atlas A_atlas','Atlas B_atlas'):
    pixels = data.copy()
    if name in ('linda','synthstroke','manual'):
        pixels[:] = 0
        pixels[12:14,12:14,12:14] = 1
    nib.save(nib.Nifti1Image(pixels, np.eye(4)), root/(name+'.nii.gz'))
inventory = {{s:{{'MNI':root/(s+'.nii.gz')}} for s in ('linda','synthstroke','manual')}}
mask_inventory_for = lambda e: inventory
available_mni_sources = lambda e: list(inventory)
deriv_path_for = lambda e: root
row = dict(subject='sub-ui', session='', region='Example ROI', lesion_in_roi_percent=25.,
           roi_coverage_percent=10., overlap_voxels=2, total_lesion_voxels=8)
OVERLAP_DFS = {{f'{{atlas}}_{{s}}':pd.DataFrame([row]) for atlas in ('Atlas A','Atlas B') for s in inventory}}
OVERLAP_DFS.update({{f'Schaefer400_{{s}}':pd.DataFrame([dict(row, region='LH_Vis_1')]) for s in inventory}})
ALL_ATLASES = {{}}
INTERP_KB_ATLASES = ['Atlas A','Atlas B']
INTERP_DISPLAY_ATLAS = 'Atlas A'
class StopExecution(Exception): pass
for number in (67,71,72,74,75):
    exec(''.join(source_cell(number)['source']), globals())
try:
    exec(''.join(source_cell(79)['source']), globals())
except StopExecution:
    pass
'''
        second = '''from calmar.report_ui import ParticipantReport
title = f'<h3>Fixture report: {INTERP_MASK_SOURCE} · {INTERP_DISPLAY_ATLAS}</h3>'
path = root/'ui-report.html'
full = '<html><body>'+title+'<p>UI fixture only.</p></body></html>'
path.write_text(full)
result = ParticipantReport(title, 'QC fixture status', [('Anatomy','<p>UI fixture only.</p>')],
    path, full, root/'Subject_in_MNI.nii.gz', root/(INTERP_MASK_SOURCE+'.nii.gz'), cw)
display(result.widget)
_report_inputs.message.value = 'Participant report ready below.'
'''
        path = Path(temp)/'results.ipynb'
        notebook = nbformat.v4.new_notebook(cells=[
            nbformat.v4.new_code_cell(first,metadata={'calmar':{'role':'report-selection'}}),
            nbformat.v4.new_code_cell(second,metadata={'calmar':{'role':'report-start'}})],
            metadata={'kernelspec':{'name':'conda-base-py','display_name':'Python','language':'python'}})
        nbformat.write(notebook,path)
        relative = path.relative_to('/home/jovyan').as_posix()
        try:
            asyncio.run(check(base,token,relative,args.artifacts))
        finally:
            headers = {'Authorization':'token '+token}
            for session in requests.get(base+'/api/sessions',headers=headers,timeout=10).json():
                if session['path'] == relative:
                    requests.delete(base+'/api/sessions/'+session['id'],headers=headers,timeout=10).raise_for_status()


if __name__ == '__main__':
    main()
