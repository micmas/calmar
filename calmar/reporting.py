"""Retained reporting computations. Notebook clients receive published artifacts."""
import json
import os
from pathlib import Path
import sys
import tempfile
import hashlib
from uuid import uuid4
from types import SimpleNamespace

import nibabel as nib
import numpy as np
import pandas as pd
from nibabel.processing import resample_from_to

from .processing import publish, validate_image


def file_identity(path):
    path = Path(path)
    stat = path.stat()
    return [str(path.absolute()), stat.st_mtime_ns, stat.st_size]


def pack(value):
    if isinstance(value, pd.DataFrame):
        return {'__dataframe__': value.to_json(orient='split', double_precision=15)}
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): pack(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [pack(v) for v in value]
    if isinstance(value, np.generic):
        return value.item()
    return value


def unpack(value):
    from io import StringIO
    if isinstance(value, dict):
        if set(value) == {'__dataframe__'}:
            return pd.read_json(StringIO(value['__dataframe__']), orient='split')
        return {k: unpack(v) for k, v in value.items()}
    if isinstance(value, list):
        return [unpack(v) for v in value]
    return value


def _file_stamps(value):
    """Cheap identities for files used by a report, without loading images."""
    found = {}
    if isinstance(value, dict):
        for item in value.values(): found.update(_file_stamps(item))
    elif isinstance(value, (list, tuple)):
        for item in value: found.update(_file_stamps(item))
    elif isinstance(value, (str, Path)):
        text = str(value)
        if text.endswith(('.nii', '.nii.gz', '.csv', '.json', '.png', '.safetensors')):
            path = Path(text)
            found[str(path.absolute())] = file_identity(path) if path.is_file() else None
    return found


def run_reporting_task(namespace, task, *, force=False, **parameters):
    """Compute once in Slurm; reopening unchanged results only reads the receipt."""
    from .scheduled import run_step_sync
    request = {'task': task, **pack(parameters)}
    dependencies = [Path(__file__), Path(__file__).with_name('atlas_loader.py'),
                    Path(__file__).with_name('atlas_overlap.py'), Path(__file__).with_name('overlay.py')]
    if task == 'decode':
        kb = Path(parameters['kb_root'])
        dependencies += [p for p in kb.rglob('*') if p.suffix in ('.py', '.md', '.yaml', '.json', '.npz')]
    identity = {'request': request, 'files': _file_stamps(parameters),
                'code': [file_identity(p) for p in dependencies if p.is_file()]}
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    cache = Path(namespace['PROJECT_DIR'])/'reports'/'report-cache'/f'{key}.json'
    if not force and cache.is_file():
        try:
            record = json.loads(cache.read_text())
            stamps = _file_stamps(record['value'])
            if record['outputs'] == stamps and all(stamps.values()):
                print(f'{task}: using prepared results.')
                return unpack(record['value'])
        except (OSError, ValueError, KeyError):
            pass
    result = run_step_sync('reporting', {'PROJECT_DIR': namespace['PROJECT_DIR'],
        '_operation_request': request})
    cache.parent.mkdir(parents=True, exist_ok=True)
    temporary = cache.with_suffix(f'.{uuid4().hex}.tmp')
    temporary.write_text(json.dumps({'value': result['value'], 'job': result.get('job'),
        'outputs': _file_stamps(result['value'])}, indent=2))
    temporary.replace(cache)
    return unpack(result['value'])


def atlas_descriptors(atlases):
    result = {}
    for name, atlas in atlases.items():
        if not isinstance(atlas.maps, (str, Path)):
            raise ValueError('Prepare atlases with the retained atlas step first.')
        labels = atlas.labels
        if hasattr(atlas, 'indices') and not isinstance(labels, dict):
            labels = dict(zip(map(int, atlas.indices), labels))
        result[name] = {'maps': str(atlas.maps), 'labels': pack(labels)}
    return result


def load_atlases(namespace, *, force=False):
    selection = (str(namespace['ATLAS_DIR']), tuple(namespace['CONFIG']['ATLASES']))
    previous = namespace.get('_CALMAR_ATLAS_SELECTION')
    existing = namespace.get('ALL_ATLASES', {})
    if not force and previous == selection and all(
            isinstance(atlas.maps, (str, Path)) and Path(atlas.maps).is_file() for atlas in existing.values()):
        return existing
    result = run_reporting_task(namespace, 'atlases', force=force, atlas_dir=str(namespace['ATLAS_DIR']),
                                names=namespace['CONFIG']['ATLASES'])
    atlases = {name: SimpleNamespace(maps=entry['maps'], labels={int(k): v for k, v in entry['labels'].items()})
               for name, entry in result.items()}
    namespace['_CALMAR_ATLAS_SELECTION'] = selection
    namespace['ALL_ATLASES'] = atlases
    return atlases


def overlap_tables(namespace, entries, sources):
    atlases = atlas_descriptors(namespace['ALL_ATLASES'])
    request_entries = [dict(e, masks={s: str(namespace['_mask_path_for'](e, s)) for s in sources}) for e in entries]
    result = run_reporting_task(namespace, 'overlap', atlases=atlases, entries=request_entries,
                                sources=sources, threshold=namespace['CONFIG']['LESION_THRESHOLD'])
    tables = {}
    for key, path in result.items():
        table = pd.read_csv(path).fillna({'session': ''})
        table.attrs['overlap_status'] = json.loads(Path(path).with_suffix('.status.json').read_text())
        tables[key] = table
    namespace.setdefault('OVERLAP_PATHS', {}).update(result)
    namespace.setdefault('OVERLAP_DFS', {}).update(tables)
    return tables


def execute(request, output):
    if not os.environ.get('SLURM_JOB_ID'):
        raise RuntimeError('Submit analysis_35_reporting.sh with sbatch.')
    task = request['task']
    if task == 'atlases':
        from .atlas_loader import fetch_atlases
        return fetch_atlases(request['names'], Path(request['atlas_dir']), output)
    if task == 'overlap':
        from .atlas_overlap import cached_overlap
        result = {}
        for name, descriptor in request['atlases'].items():
            img = nib.load(descriptor['maps'])
            labels = descriptor['labels']
            if isinstance(labels, dict): labels = {int(k): v for k, v in labels.items()}
            for source in request['sources']:
                key = f'{name}_{source}'
                target = output/f'{key}.csv'
                cached_overlap(target, request['entries'], lambda e: e['masks'][source],
                               name, img, np.asarray(img.dataobj), labels, threshold=request['threshold'])
                result[key] = str(target)
        return result
    if task == 'decode':
        from .kb_paths import add_kb_to_path
        add_kb_to_path(request['kb_root'])
        from aphasia_kb import KnowledgeBase
        from .acquisition import ensure_nifti_content
        if not ensure_nifti_content(Path(request['mask']), Path(request['dataset'])):
            raise FileNotFoundError(request['mask'])
        result = KnowledgeBase(request['kb_root']).decode_lesion(request['mask'], verbose=True)
        (output/'decoding.json').write_text(json.dumps(pack(result), indent=2))
        return pack(result)
    if task == 'disconnectome':
        import matplotlib.pyplot as plt
        from nilearn import image, plotting
        from . import colors
        bcb = nib.load(request['bcb'])
        dd = image.resample_to_img(nib.load(request['deepdisco']), bcb, interpolation='continuous',
                                   force_resample=True, copy_header=True)
        target = output/'deepdisco_on_bcb.nii.gz'; nib.save(dd, target)
        a, b = np.clip(bcb.get_fdata(), 0, 1), np.clip(dd.get_fdata(), 0, 1)
        selected = (a > 0) | (b > 0)
        correlation = (float(np.corrcoef(a[selected], b[selected])[0, 1])
                       if selected.sum() > 10 and np.std(a[selected]) > 0 and np.std(b[selected]) > 0 else float('nan'))
        threshold = request['threshold']
        n_a, n_b, inter = int((a > threshold).sum()), int((b > threshold).sum()), int(((a > threshold) & (b > threshold)).sum())
        difference = nib.Nifti1Image(np.abs(a-b), bcb.affine, bcb.header)
        fig, axes = plt.subplots(3, 1, figsize=(8, 10.5))
        for ax, (img, title, cmap) in zip(axes, [
                (bcb, 'BCBToolkit', colors.cmap('bcbtoolkit', continuous=True)),
                (dd, 'DeepDisco', colors.cmap('deepdisco', continuous=True)),
                (difference, '|BCB - DeepDisco|', 'viridis')]):
            plotting.plot_glass_brain(img, colorbar=True, title=title, cmap=cmap,
                                      vmin=0, vmax=1, plot_abs=False, axes=ax)
        png = output/'comparison.png'; fig.savefig(png, dpi=90, bbox_inches='tight'); plt.close(fig)
        return dict(r=correlation, dice=2*inter/max(n_a+n_b, 1), thr=threshold,
                    n_bcb=n_a, n_dd=n_b, png=str(png), resampled=str(target))
    if task == 'report_overlay':
        import matplotlib.pyplot as plt
        from nilearn import plotting
        from . import colors
        lesion = nib.load(request['mask'])
        background = request['background'] if Path(request['background']).is_file() else None
        cut = plotting.find_xyz_cut_coords(lesion)
        fig = plt.figure(figsize=(9, 5), facecolor='black')
        ax_top = fig.add_axes([0., .52, 1., .46]); ax_bottom = fig.add_axes([0., .02, 1., .46])
        plotting.plot_roi(lesion, bg_img=background, axes=ax_top, cmap=colors.cmap(request['source']),
            display_mode='ortho', cut_coords=cut, alpha=.75, black_bg=True, annotate=False,
            draw_cross=True, colorbar=False, vmin=0, vmax=1)
        plotting.plot_glass_brain(lesion, axes=ax_bottom, display_mode='lyrz', cmap=colors.cmap(request['source']),
            colorbar=False, plot_abs=True, threshold=.5, black_bg=True)
        png = output/'lesion_overlay.png'
        fig.savefig(png, dpi=110, facecolor='black', bbox_inches='tight', pad_inches=.05); plt.close(fig)
        return str(png)
    if task == 'group':
        paths = request['masks']
        if not paths: raise ValueError('No masks selected')
        ref = nib.load(paths[0]); accum = np.zeros(ref.shape, dtype=np.float32)
        for path in paths:
            img = nib.load(path)
            if img.shape != ref.shape or not np.allclose(img.affine, ref.affine):
                img = resample_from_to(img, ref, order=0)
            accum += np.asarray(img.dataobj) > request['threshold']
        target = output/'frequency.nii.gz'
        nib.save(nib.Nifti1Image(accum/len(paths), ref.affine), target)
        validate_image(target, paths[0])
        # Same template the masks are on (FSL MNI152NLin6Asym), shown on the map grid.
        from . import templates
        background = output/'background.nii.gz'
        nib.save(resample_from_to(nib.load(str(templates.T1)), ref, order=1), background)
        return {'map': str(target), 'background': str(background), 'used': len(paths)}
    if task == 'comparison':
        from scipy.ndimage import binary_erosion
        from .overlay import reference_edges
        manual = Path(request['manual']) if request.get('manual') else None
        metrics, errors, outlines, identities = {}, {}, {}, {}
        ref = nib.load(manual) if manual and manual.is_file() else None
        man = np.asarray(ref.dataobj) > 0 if ref is not None else None
        if ref is not None: identities[str(manual)] = file_identity(manual)
        for name, path in request['automatic'].items():
            metrics[name] = None
            if not Path(path).is_file():
                errors[name] = 'No prepared mask'; continue
            img = nib.load(path); data = np.asarray(img.dataobj) > 0
            target = output/f'{name}_boundary.nii.gz'
            nib.save(nib.Nifti1Image((data & ~binary_erosion(data)).astype('uint8'), img.affine), target)
            outlines[name] = str(target); identities[path] = file_identity(path)
            if ref is not None:
                if img.shape != ref.shape or not np.allclose(img.affine, ref.affine):
                    img = resample_from_to(img, ref, order=0)
                auto = np.asarray(img.dataobj) > 0
                a, m, inter = int(auto.sum()), int(man.sum()), int((auto & man).sum())
                metrics[name] = dict(n=a, overlap=inter, dice=2*inter/max(a+m, 1),
                    iou=inter/max(a+m-inter, 1), sens=inter/max(m, 1), prec=inter/max(a, 1))
        edge = None
        if request.get('coreg') and Path(request['coreg']).is_file():
            import shutil
            scan = output/'coreg.nii.gz'; shutil.copy2(request['coreg'], scan)
            edge = str(reference_edges(scan)); identities[request['coreg']] = file_identity(request['coreg'])
        return dict(metrics=metrics, errors=errors, outlines=outlines, identities=identities,
                    manual_voxels=int(man.sum()) if man is not None else None, edges=edge)
    raise ValueError(f'Unknown reporting task: {task}')


def main():
    request_path, final = map(Path, sys.argv[1:])
    if final.exists(): raise FileExistsError(final)
    request = json.loads(request_path.read_text())
    if 'CALMAR_LESION_THRESHOLD' in os.environ:
        threshold = os.environ['CALMAR_LESION_THRESHOLD']
        request['threshold'] = .5 if threshold == 'half' else float(threshold)
    final.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=final.name+'.attempt.', dir=final.parent) as d:
        tmp = Path(d)/'result'; tmp.mkdir()
        value = execute(request, tmp)
        def relocate(v):
            if isinstance(v, str) and v.startswith(str(tmp)+'/'):
                return str(final/Path(v).relative_to(tmp))
            if isinstance(v, dict): return {k: relocate(x) for k, x in v.items()}
            if isinstance(v, list): return [relocate(x) for x in v]
            return v
        (tmp/'summary.json').write_text(json.dumps({'stage': 'reporting', 'job': os.environ['SLURM_JOB_ID'],
            'request': request, 'value': relocate(pack(value)), 'results': []}, indent=2))
        publish(tmp, final, request.get('output_id', 'reporting'))


if __name__ == '__main__': main()
