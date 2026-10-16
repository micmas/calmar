"""Read existing cohort products in Slurm; emit metrics and real PNG overlays.

This never edits masks or ratings and never labels existing products as a new
imaging run. The PNGs still require human visual inspection after execution.
"""
import json
import os
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import nibabel as nib
from nibabel.processing import resample_from_to
import numpy as np
from PIL import Image, ImageOps

from calmar.processing import MODELS, paths, validate_image
from calmar.reporting import execute as prepare_reporting
from calmar.qc import find_best_hdbet_mask


def snapshot(background, overlay, output, title):
    image = nib.as_closest_canonical(nib.load(background))
    mask = resample_from_to(nib.load(overlay), image, order=0)
    data, values = image.get_fdata(), mask.get_fdata()
    points = np.argwhere(values > 0)
    center = np.median(points, axis=0).astype(int) if len(points) else np.array(data.shape)//2
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    high = np.percentile(data[data > 0], 99) if np.any(data > 0) else 1
    for axis, ax in enumerate(axes):
        cut = np.take(data, center[axis], axis=axis).T
        layer = np.take(values, center[axis], axis=axis).T
        ax.imshow(cut, origin='lower', cmap='gray', vmin=0, vmax=high)
        ax.imshow(np.ma.masked_where(layer <= 0, layer), origin='lower', cmap='autumn',
                  vmin=0, vmax=max(float(values.max()), 1), alpha=.65)
        ax.set_title(f'{("Sagittal", "Coronal", "Axial")[axis]} · voxel {center[axis]}')
        ax.axis('off')
    fig.suptitle(title+' · canonical RAS orientation')
    fig.tight_layout()
    fig.savefig(output, format='png', dpi=120)
    plt.close(fig)
    with Image.open(output) as png:
        if png.format != 'PNG': raise ValueError(f'Not PNG: {output}')
        png.verify()


def inspect(request, output):
    if not os.environ.get('SLURM_JOB_ID'):
        raise RuntimeError('Submit analysis_32_inspect_acceptance.sh with sbatch.')
    rows, problems = [], []
    for entry in request['entries']:
        directories = paths(request, entry)
        linda, synth = directories['linda'], directories['synthstroke']
        t1 = Path(entry['t1w'])
        reference = linda/'Subject_in_MNI.nii.gz'
        manual_dir = linda/'_manual_mask_compare'
        manual = next((manual_dir/n for n in ('ManualLesion_in_T1_sitk.nii.gz','ManualLesion_in_T1.nii.gz')
                       if (manual_dir/n).is_file()), manual_dir/'ManualLesion_in_T1_sitk.nii.gz')
        cohort_tag = '_'.join(filter(None, (entry['subject'],entry.get('session'))))
        masks = {
            'linda':(linda/'Prediction3_native.nii.gz',linda/'Lesion_in_MNI.nii.gz'),
            'manual':(manual,linda/'ExpertMask_in_MNI.nii.gz'),
            'synthstroke':(synth/'prediction_lesion_mask.nii.gz',synth/'SynthStroke_in_MNI.nii.gz'),
        }
        brain = find_best_hdbet_mask(directories['hdbet'])
        brain_row = dict(subject=entry['subject'], session=entry.get('session'), source='hdbet',
                         kind='brain', path=str(brain), execution='existing product inspected; not recomputed')
        try:
            brain_row['metrics'] = validate_image(brain, t1, binary=True, nonempty=True)
            png = output/f'{cohort_tag}_hdbet_brain.png'
            snapshot(t1, brain, png, f'{cohort_tag} · HD-BET brain mask')
            brain_row.update(png=png.name, status='numerically checked; visual review pending')
        except Exception as error:
            brain_row.update(status='failed', error=str(error))
            problems.append(f'{cohort_tag}/hdbet: {error}')
        rows.append(brain_row)
        agreement_dir = output/f'{cohort_tag}_agreement'
        agreement_dir.mkdir()
        agreement = prepare_reporting({'task': 'comparison', 'manual': str(manual),
            'automatic': {'LINDA': str(masks['linda'][0]), 'SynthStroke': str(masks['synthstroke'][0])},
            'coreg': str(manual_dir/'T2_in_T1_sitk.nii.gz')}, agreement_dir)
        if agreement['edges']:
            edge = Path(agreement['edges'])
            png = output/f'{cohort_tag}_registration_coreg.png'
            edge_metrics = validate_image(edge, t1, binary=True, nonempty=True)
            snapshot(t1, edge, png, f'{cohort_tag} · registered T2 edges on T1')
            rows.append(dict(subject=entry['subject'], session=entry.get('session'),
                source='registration', kind='coreg', path=str(manual_dir/'T2_in_T1_sitk.nii.gz'),
                execution='existing registration inspected; not recomputed',
                metrics=edge_metrics, png=png.name,
                status='numerically checked; visual review pending'))
        # This directory is atomically renamed on publication. Store generated
        # artifact paths relative to the metrics file, never the staging path.
        agreement['outlines'] = {name: str(Path(path).relative_to(agreement_dir))
                                 for name, path in agreement['outlines'].items()}
        if agreement['edges']:
            agreement['edges'] = str(Path(agreement['edges']).relative_to(agreement_dir))
        (agreement_dir/'metrics.json').write_text(json.dumps(agreement, indent=2))
        for source, (native, mni) in masks.items():
            token = 'expert' if source == 'manual' else source
            products = [('native',native,t1,True),('mni',mni,reference,True),
                        ('bcb',directories['bcbtoolkit']/f'Disconnectome_{token}.nii.gz',reference,False)]
            products += [(model,directories['deepdisco']/f'DeepDisco_{token}_{model}.nii.gz',reference,False)
                         for model in MODELS]
            for kind, path, background, binary in products:
                row = dict(subject=entry['subject'],session=entry.get('session'),source=source,
                           kind=kind,path=str(path),execution='existing product inspected; not recomputed')
                try:
                    row['metrics'] = validate_image(path,background if binary else None,binary=binary)
                    img = nib.load(path)
                    row['metrics']['nonzero_volume_ml'] = float(row['metrics']['nonzero']*abs(np.linalg.det(img.affine[:3,:3]))/1000)
                    row['metrics']['affine'] = img.affine.tolist()
                    row['warning'] = 'Empty image: review required' if row['metrics']['nonzero']==0 else ''
                    png = output/f'{cohort_tag}_{source}_{kind}.png'
                    snapshot(background,path,png,f'{cohort_tag} · {source} · {kind}')
                    row['png'] = png.name
                    row['status'] = 'numerically checked; visual review pending'
                except Exception as error:
                    row['status'] = 'failed'
                    row['error'] = str(error)
                    problems.append(f'{cohort_tag}/{source}/{kind}: {error}')
                rows.append(row)
    # Compact sheets make it practical to inspect every source/model, while
    # retaining each full-size three-plane overlay for closer review.
    for entry in request['entries']:
        tag = '_'.join(filter(None, (entry['subject'], entry.get('session'))))
        for group, kinds in [('masks', ['brain', 'native', 'mni']),
                             ('disconnectomes', ['bcb', *MODELS])]:
            sheet = Image.new('RGB', (1800, 220*len(kinds)), 'white')
            for row, kind in enumerate(kinds):
                for column, source in enumerate(('linda', 'manual', 'synthstroke')):
                    panel_kind = kind
                    if kind == 'brain':
                        if column == 2: continue
                        source = 'hdbet' if column == 0 else 'registration'
                        panel_kind = 'brain' if column == 0 else 'coreg'
                    png = output/f'{tag}_{source}_{panel_kind}.png'
                    if png.is_file():
                        with Image.open(png) as img:
                            panel = ImageOps.contain(img.convert('RGB'), (600, 220))
                            sheet.paste(panel, (column*600, row*220))
            sheet.save(output/f'{tag}_{group}_contact.png', format='PNG')
    (output/'metrics.json').write_text(json.dumps({'job':os.environ['SLURM_JOB_ID'],'rows':rows},indent=2))
    if problems:
        raise RuntimeError('Acceptance inspection incomplete:\n'+'\n'.join(problems))
    (output/'summary.json').write_text(json.dumps({'participants':len(request['entries']),
        'images':len(rows),'visual_review':'pending','results':[]},indent=2))


if __name__ == '__main__':
    inspect(json.loads(Path(sys.argv[1]).read_text()),Path(sys.argv[2]))
