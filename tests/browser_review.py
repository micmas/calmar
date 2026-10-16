"""Exercise review controls and the report shortcut on a tiny disposable fixture."""

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
        browser = await p.chromium.launch(args=['--no-sandbox', '--enable-unsafe-swiftshader'])
        page = await browser.new_page(viewport={'width':1300,'height':1050},
                                      extra_http_headers={'Authorization':'token '+token})
        async def authorize(route):
            headers = dict(route.request.headers)
            if not route.request.url.startswith(base+'/'):
                headers.pop('authorization',None)
            await route.continue_(headers=headers)
        await page.route('**/*', authorize)
        try:
            await page.goto(f'{base}/lab/workspaces/calmar-review-{uuid4().hex}/tree/{relative}')
            cell = page.locator('.jp-Notebook .jp-CodeCell').first
            await cell.wait_for(timeout=30000)
            await cell.click(); await page.keyboard.press('Shift+Enter')
            coreg = page.get_by_role('button', name='1. Coregistration', exact=True)
            await coreg.wait_for(timeout=45000)
            await coreg.scroll_into_view_if_needed()
            canvas = page.locator('.jp-Notebook canvas')
            await canvas.wait_for(timeout=45000)
            await canvas.scroll_into_view_if_needed()
            await page.wait_for_timeout(1500)
            await canvas.evaluate('(el) => { el.dataset.reviewIdentity = "original"; }')
            await page.screenshot(path=str(artifacts/'coregistration.png'))
            await page.get_by_role('button', name='2. Lesion masks', exact=True).click()
            await page.get_by_role('checkbox', name='LINDA', exact=True).uncheck()
            await page.get_by_role('checkbox', name='Manual', exact=True).wait_for()
            await page.wait_for_timeout(500)
            assert await canvas.count() == 1
            assert await canvas.get_attribute('data-review-identity') == 'original'
            await canvas.scroll_into_view_if_needed()
            await page.screenshot(path=str(artifacts/'lesion-masks.png'))
            await coreg.click()
            await page.get_by_role('button', name='2. Lesion masks', exact=True).click()
            assert not await page.get_by_role('checkbox', name='LINDA', exact=True).is_checked()
            await page.get_by_role('button', name='Jump to reporting', exact=True).click()
            await page.get_by_role('heading', name='Report inputs ready', exact=True).wait_for(timeout=30000)
            output = page.locator('.jp-OutputArea-output')
            assert await output.get_by_text('REPORT_PREPARED', exact=True).count() == 1
            assert not await output.get_by_text('BATCH_MUST_NOT_RUN', exact=True).count()
            assert not await output.get_by_text('REPORT_MUST_NOT_GENERATE', exact=True).count()
            await page.get_by_role('heading', name='Report inputs ready', exact=True).scroll_into_view_if_needed()
            await page.screenshot(path=str(artifacts/'report-shortcut.png'))
            print('PASS: one review canvas; cached coregistration; persistent mask toggles; report shortcut bypasses batch and stops before generation.')

            # A separate notebook exercises the new participant gate and batch path.
            select_relative = str(Path(relative).with_name('selection.ipynb'))
            await page.goto(f'{base}/lab/workspaces/calmar-selection-{uuid4().hex}/tree/{select_relative}')
            first = page.locator('.jp-Notebook .jp-CodeCell').first
            await first.wait_for(timeout=30000)
            await first.click(); await page.keyboard.press('Shift+Enter')
            subject = page.get_by_role('combobox', name='Test participant:', exact=True)
            await subject.wait_for(timeout=30000)
            assert 'sub-new' in await subject.locator('option:checked').inner_text()
            assert not await page.locator('.jp-OutputArea-output').get_by_text('SINGLE_TEST_STARTED', exact=True).count()
            await subject.select_option(index=0)
            await page.get_by_role('button', name='Run single-subject test', exact=True).click()
            await page.locator('.jp-OutputArea-output').get_by_text('SINGLE_TEST_STARTED', exact=True).wait_for(timeout=30000)
            await page.get_by_role('button', name='Continue to batch', exact=True).click()
            await page.get_by_role('heading', name='Batch reached QC', exact=True).wait_for(timeout=30000)
            assert not await page.locator('.jp-OutputArea-output').get_by_text('AFTER_QC_MUST_NOT_RUN', exact=True).count()
            await page.screenshot(path=str(artifacts/'participant-and-batch.png'))
            print('PASS: participant defaults to unprocessed; chosen participant starts; Continue to batch runs automatically and stops at QC.')
        except Exception:
            await page.screenshot(path=str(artifacts/'failure.png'))
            print((await page.locator('body').inner_text())[-4000:])
            raise
        finally:
            await browser.close()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--server-url',required=True)
    parser.add_argument('--artifacts', type=Path, default=ROOT/'notes/browser-review')
    args=parser.parse_args()
    base=args.server_url.rstrip('/')
    if not base.startswith(('http://127.0.0.1:', 'http://localhost:')):
        raise ValueError('Use a loopback server.')
    token=os.environ.get('CALMAR_BROWSER_TOKEN') or os.environ['JUPYTERHUB_API_TOKEN']
    artifacts=args.artifacts; artifacts.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='calmar-review-',dir=ROOT/'notes') as directory:
        first=f'''import sys
sys.path.insert(0, {str(ROOT)!r})
from pathlib import Path
import numpy as np
import nibabel as nib
from IPython.display import display, HTML
from calmar import widgets as cw
from calmar.overlay import mask_review
from calmar.execution import pause_before_batch, ExecutionCheckpoint
from calmar.timing import BatchTiming
cw.configure(url_base=False)
root=Path.cwd()
data=np.zeros((24,24,24),dtype=np.float32)
data[3:21,3:21,3:21]=100
data[7:17,7:17,7:17]=50
brain=root/'brain.nii.gz'; registered=root/'registered.nii.gz'
nib.save(nib.Nifti1Image(data,np.eye(4)),brain)
nib.save(nib.Nifti1Image(data,np.eye(4)),registered)
data[:]=0; data[10:15,10:15,10:15]=1
mask=root/'mask.nii.gz'; nib.save(nib.Nifti1Image(data,np.eye(4)),mask)
display(mask_review(cw,'review',[dict(path=str(brain)),
    dict(path=str(mask),name='Manual',colormap='blue',opacity=.5),
    dict(path=str(mask),name='LINDA',colormap='red',opacity=.8)],coreg_path=registered,edge_path=mask))
with BatchTiming(globals(),'Fixture batch') as timer:
    with timer.participant(dict(subject='sub-test',session='ses-1'),'LINDA') as row:
        row['status']='Cached'
TEST_SUBJECT_IDX=1
(root/'saved-qc.json').write_text('unchanged QC fixture')
gate=pause_before_batch()
'''
        cells=[nbformat.v4.new_code_cell(first),
               nbformat.v4.new_code_cell("print('BATCH_MUST_NOT_RUN')",metadata={'calmar':{'role':'batch-start'}}),
               nbformat.v4.new_code_cell("assert INTERP_SUBJECT_IDX == 1\nassert (root/'saved-qc.json').read_text() == 'unchanged QC fixture'\nprint('REPORT_PREPARED')",metadata={'calmar':{'role':'report-setup'}}),
               nbformat.v4.new_code_cell("report_gate=ExecutionCheckpoint(get_ipython(),'Choose report inputs')\ndisplay(HTML('<h3>Report inputs ready</h3>'))\nreport_gate._cancel_queued()",metadata={'calmar':{'role':'report-selection'}}),
               nbformat.v4.new_code_cell("print('REPORT_MUST_NOT_GENERATE')",metadata={'calmar':{'role':'report-start'}})]
        path=Path(directory)/'review.ipynb'
        nbformat.write(nbformat.v4.new_notebook(cells=cells,metadata={'kernelspec':{'name':'conda-base-py','display_name':'Python','language':'python'}}),path)
        selection = f'''import sys
sys.path.insert(0, {str(ROOT)!r})
from pathlib import Path
from IPython.display import display, HTML
from calmar.single_subject import show_single_subject_inputs
from calmar.execution import pause_before_batch, ExecutionCheckpoint
root=Path.cwd()
SUBJECTS=[dict(subject='sub-cached',session='ses-1'), dict(subject='sub-new',session='ses-2')]
CONFIG=dict(RUN_TEST=True)
deriv_path_for=lambda e:root/e['subject']/'linda'
synthstroke_path_for=lambda e:root/e['subject']/'synth'
hdbet_path_for=lambda e:root/e['subject']/'hdbet'
for folder,name in ((deriv_path_for(SUBJECTS[0]),'Lesion_in_MNI.nii.gz'),(synthstroke_path_for(SUBJECTS[0]),'prediction_lesion_mask.nii.gz')):
    folder.mkdir(parents=True,exist_ok=True);(folder/name).write_bytes(b'cache-state fixture')
panel=show_single_subject_inputs(globals())
'''
        selection_cells=[nbformat.v4.new_code_cell(selection),
            nbformat.v4.new_code_cell("assert TEST_SUBJECT_IDX == CONFIG['TEST_SUBJECT_IDX'] == 0\nprint('SINGLE_TEST_STARTED')\ngate=pause_before_batch()",metadata={'calmar':{'role':'single-test-start'}}),
            nbformat.v4.new_code_cell("qc=ExecutionCheckpoint(get_ipython(),'Choose QC')\ndisplay(HTML('<h3>Batch reached QC</h3>'))\nqc._cancel_queued()",metadata={'calmar':{'role':'batch-start'}}),
            nbformat.v4.new_code_cell("print('AFTER_QC_MUST_NOT_RUN')")]
        nbformat.write(nbformat.v4.new_notebook(cells=selection_cells,metadata={'kernelspec':{'name':'conda-base-py','display_name':'Python','language':'python'}}),Path(directory)/'selection.ipynb')
        relative=path.relative_to('/home/jovyan').as_posix()
        try:
            asyncio.run(check(base,token,relative,artifacts))
        finally:
            headers={'Authorization':'token '+token}
            for session in requests.get(base+'/api/sessions',headers=headers,timeout=10).json():
                if str(Path(session['path']).parent)==str(Path(relative).parent):
                    requests.delete(base+'/api/sessions/'+session['id'],headers=headers,timeout=10).raise_for_status()


if __name__=='__main__':
    main()
