"""Read existing cohort outputs, verify table migration and cached decoding."""
from pathlib import Path
import importlib.metadata as metadata
import json
import shutil
import sys
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import pandas as pd
from calmar.anatomy_labels import aal_labels, label_table
from calmar.atlas_overlap import cached_overlap, SIDE_COLUMNS

dataset, atlases, cache, out = map(Path, sys.argv[1:])
assert sys.version_info[:3] == (3, 13, 15)
versions = {name: metadata.version(name) for name in ('nibabel', 'nilearn', 'numpy', 'pandas', 'scipy')}
assert versions == {'nibabel': '5.4.2', 'nilearn': '0.13.1', 'numpy': '2.3.5', 'pandas': '3.0.5', 'scipy': '1.15.3'}
entries = [dict(subject=s, session=t) for s, t in
           [('sub-M2066', 'ses-235'), ('sub-M2075', 'ses-602'), ('sub-M2176', 'ses-1237')]]
deriv = dataset / 'derivatives'
def mask_path(e, source):
    tool, name = ('synthstroke', 'SynthStroke_in_MNI.nii.gz') if source == 'synthstroke' else (
        'linda', 'ExpertMask_in_MNI.nii.gz' if source == 'manual' else 'Lesion_in_MNI.nii.gz')
    return deriv/tool/e['subject']/e['session']/'anat'/name

ho_labels = {int(e.attrib['index'])+1: e.text.strip()
             for e in ET.parse(atlases/'fsl/data/atlases/HarvardOxford-Cortical.xml').iter('label')}
destrieux = pd.read_csv(atlases/'destrieux_2009/destrieux2009_rois_labels_lateralized.csv')
schaefer = pd.read_csv(atlases/'schaefer_2018/Schaefer2018_400Parcels_7Networks_order.txt', sep='\t', header=None)
labels = dict(HarvardOxford=ho_labels, Destrieux=dict(zip(destrieux['index'], destrieux['name'])),
              Schaefer400=dict(zip(schaefer[0], schaefer[1])), AAL=aal_labels(str(atlases)),
              JHU={i: f'Tract_{i}' for i in range(1, 21)})
summary = {'versions': versions, 'cohort': entries, 'overlap': {}}
for atlas_name, mapping in labels.items():
    atlas = nib.load(deriv/'linda'/f'{atlas_name}_atlas.nii.gz')
    data = np.asarray(atlas.dataobj)
    for source in ('linda', 'manual', 'synthstroke'):
        token = 'expert' if source == 'manual' else source
        name = f'lesion_atlas_overlap_{atlas_name}_{token}.csv'
        old = Path('reports')/name
        if old.exists():
            shutil.copy2(old, out/name)
        df = cached_overlap(out/name, entries, lambda e: mask_path(e, source), atlas_name,
                            atlas, data, mapping, threshold=.5)
        df = df.loc[df.subject.isin([e['subject'] for e in entries])].copy()
        if len(df):
            assert (df[SIDE_COLUMNS].sum(axis=1) == df.overlap_voxels).all()
            assert ((df.roi_coverage_percent > 0) & (df.roi_coverage_percent <= 100)).all()
            assert np.isfinite(df.lesion_in_roi_percent).all()
        summary['overlap'][f'{atlas_name}_{source}'] = {
            'rows': len(df), 'statuses': df.attrs['overlap_status'],
            'sides': label_table(df, atlas_name).lesion_hemisphere.value_counts().to_dict()}
        print(atlas_name, source, len(df), 'rows', flush=True)

# Inspect the exact mask whose omission exposed the zero-overlap menu bug,
# alongside the other current participants. Radiological orientation is labelled.
fig, axes = plt.subplots(1, 3, figsize=(13, 5))
for e, ax in zip(entries, axes):
    mask = nib.as_closest_canonical(nib.load(mask_path(e, 'synthstroke')))
    data = np.asarray(mask.dataobj) > .5
    points = np.argwhere(data)
    z = int(np.median(points[:, 2])) if len(points) else data.shape[2]//2
    world = nib.affines.apply_affine(mask.affine, points)
    counts = {side: int(n) for side, n in zip(('left', 'right', 'midline'),
              ((world[:, 0] < -1e-5).sum(), (world[:, 0] > 1e-5).sum(), (abs(world[:, 0]) <= 1e-5).sum()))}
    summary.setdefault('synthstroke_mask_sides', {})[e['subject']] = counts
    from nilearn.image import resample_to_img
    bg = nib.load(deriv/'linda'/e['subject']/e['session']/'anat'/'Subject_in_MNI.nii.gz')
    bg = np.asarray(resample_to_img(bg, mask, force_resample=True, copy_header=True).dataobj)
    ax.imshow(bg[:, :, z].T, origin='lower', cmap='gray')
    ax.contour(data[:, :, z].T, levels=[.5], colors=['lime'], linewidths=.7)
    ax.set_title(f"{e['subject']} SynthStroke\nL {counts['left']} · R {counts['right']} · midline {counts['midline']}")
    ax.set_xlabel('Left hemisphere ← MNI x → Right hemisphere')
    ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig(out/'laterality.png', dpi=130); plt.close(fig)

sys.path.insert(0, str(Path('aphasia-kb').resolve()))
import decode_lesion as decoder
assert all((cache/name).is_file() for name in decoder._NS_FILES), 'Neurosynth cache incomplete'
# The decoder's separate nilearn atlas cache must also exist; forbid acquisition.
assert (Path.home()/'nilearn_data/fsl/data/atlases/HarvardOxford/HarvardOxford-cort-maxprob-thr25-2mm.nii.gz').is_file()
import urllib.request
def no_download(*args, **kwargs):
    raise RuntimeError('Validation uses existing local data only')
urllib.request.urlretrieve = no_download
import aphasia_kb
result = aphasia_kb.KnowledgeBase('aphasia-kb').decode_lesion(str(mask_path(entries[0], 'synthstroke')), verbose=True)
assert result['neurosynth_available'], result['warnings']
assert len(result['term_decoding']) and np.isfinite(result['term_decoding']['r']).all()
result['term_decoding'].to_csv(out/'neurosynth_terms.csv', index=False)
summary['decoding'] = dict(subject=entries[0]['subject'], source='synthstroke',
                           terms=len(result['term_decoding']), warnings=result['warnings'],
                           lesion_voxels=result['lesion_voxels'])
(out/'summary.json').write_text(json.dumps(summary, indent=2))
print(json.dumps(summary['decoding']), flush=True)
