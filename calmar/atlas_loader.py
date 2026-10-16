"""Atlas acquisition used only by the retained reporting job."""
import fcntl
import os
import warnings
from pathlib import Path
from types import SimpleNamespace
import xml.etree.ElementTree as ET

import nibabel as nib
from nilearn import datasets


def fetch_atlases(names, cache, output):
    if not os.environ.get('SLURM_JOB_ID'):
        raise RuntimeError('Atlas acquisition requires the retained Slurm job.')
    cache.mkdir(parents=True, exist_ok=True)
    fetchers = {
        'HarvardOxford': lambda: datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-2mm', data_dir=str(cache)),
        'Destrieux': lambda: datasets.fetch_atlas_destrieux_2009(data_dir=str(cache)),
        'Schaefer400': lambda: datasets.fetch_atlas_schaefer_2018(n_rois=400, yeo_networks=7, data_dir=str(cache)),
        'AAL': lambda: datasets.fetch_atlas_aal(version='SPM12', data_dir=str(cache)),
    }
    result = {}
    # Destrieux's label table lists L/R "Medial_wall" (42, 117), which has no voxels
    # in the volumetric image; nilearn warns about it. No lesion can overlap them.
    warnings.filterwarnings('ignore', message=r'(?s).*missing from the atlas image.*Medial_wall', category=UserWarning)
    with (cache/'.acquisition.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for name in names:
            if name == 'JHU':
                root = Path(os.environ['FSLDIR'])/'data/atlases'
                labels = {int(el.get('index'))+1: el.text.strip() for el in ET.parse(root/'JHU-tracts.xml').findall('.//label')}
                atlas = SimpleNamespace(maps=str(root/'JHU/JHU-ICBM-tracts-maxprob-thr50-2mm.nii.gz'), labels=labels)
            elif name == 'AAL' and (cache/'aal_mirror/AAL.nii.gz').is_file():
                from .anatomy_labels import aal_labels
                atlas = SimpleNamespace(maps=str(cache/'aal_mirror/AAL.nii.gz'), labels=aal_labels(str(cache)))
            else:
                if name not in fetchers: raise ValueError(f'Unknown atlas: {name}')
                atlas = fetchers[name]()
            img = atlas.maps if hasattr(atlas.maps, 'get_fdata') else nib.load(atlas.maps)
            target = output/f'{name}_atlas.nii.gz'
            nib.save(img, target)
            if hasattr(atlas, 'lut'):
                labels = dict(zip(atlas.lut['index'].astype(int), atlas.lut['name'].astype(str)))
            elif isinstance(atlas.labels, dict):
                labels = atlas.labels
            elif hasattr(atlas, 'indices'):
                labels = dict(zip(map(int, atlas.indices), atlas.labels))
            else:
                labels = dict(enumerate(atlas.labels))
            labels = {int(k): v.decode() if isinstance(v, bytes) else str(v) for k, v in labels.items()}
            result[name] = {'maps': str(target), 'labels': labels}
    return result
