"""Retained, scheduler-only processing with atomic publication and cache identity.

The notebook passes an explicit request; this module never reads notebook state.
Existing derivatives are preserved, and legacy caches are identified as such.
"""
from pathlib import Path
import argparse
import fcntl
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from uuid import uuid4

import nibabel as nib
import numpy as np
from nibabel.processing import resample_from_to

from . import qc as q
from .acquisition import ensure_nifti_content
from .process_output import COMMANDS, TOOLS, record as record_step
from .study import derivative_dirs, file_token, mni_masks, segmentation_methods, stage_selected, template_source
from . import templates
from .brainmask import save_like

MODELS = {"association": "ASS", "projection": "PRO", "commissural": "COM", "whole_brain": "WHO"}
FSL_GRID = ((91, 109, 91), np.array([[-2., 0, 0, 90], [0, 2., 0, -126], [0, 0, 2., -72], [0, 0, 0, 1.]]))
# Bump the relevant version when an algorithm changes, not for edits to UI,
# logging, unrelated stages or Slurm resource directives. Module pins and all
# scientific parameters remain part of each product's options.
ALGORITHM_VERSIONS = {}
# Products whose method changed after run records were introduced: an output
# without a record (made before them) cannot be shown to match the current method
# (brain: union with SynthStrip; linda: seeded, single-threaded), so it is stale.
LEGACY_IS_STALE = {'brain', 'linda'}


def fingerprint(path):
    path = Path(path)
    digest = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            digest.update(block)
    return {'path': str(path.absolute()), 'sha256': digest.hexdigest()}


def validate_image(path, reference=None, binary=False, nonempty=False):
    img = nib.load(str(path))
    data = np.asarray(img.dataobj)
    if data.ndim != 3 or not np.isfinite(data).all() or not np.isfinite(img.affine).all():
        raise ValueError(f'Invalid 3-D image: {path}')
    if binary and not np.isin(data, [0, 1]).all():
        raise ValueError(f'Nonbinary mask: {path}')
    if nonempty and not np.any(data):
        raise ValueError(f'Empty required image: {path}')
    if reference:
        ref = nib.load(str(reference))
        if img.shape != ref.shape or not np.allclose(img.affine, ref.affine, atol=1e-4):
            raise ValueError(f'Grid mismatch: {path} and {reference}')
    return {'shape': list(img.shape), 'nonzero': int(np.count_nonzero(data)),
            'minimum': float(data.min()), 'maximum': float(data.max())}


def publish(tmp, final, output_id):
    subprocess.run(['neurodesk-astra-provenance', 'publish', str(tmp), str(final),
                    '--output-id', output_id, '--tool', sys.executable,
                    '--script', os.environ['CALMAR_EXECUTION_SCRIPT']], check=True)


def product(final, *args, **kwargs):
    final = Path(final)
    final.parent.mkdir(parents=True, exist_ok=True)
    with final.with_name('.'+final.name+'.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        return _product(final, *args, **kwargs)


def _product(final, inputs, options, build, expected, output_id, *, validator=validate_image, overwrite=False):
    """Validate caches; never silently reuse a known stale scientific product."""
    final = Path(final)
    identity = {'inputs': [fingerprint(p) for p in inputs], 'options': options,
                'algorithm_version': ALGORITHM_VERSIONS.get(output_id, 1),
                'implementation': fingerprint(__file__)['sha256'],
                'qc_implementation': fingerprint(q.__file__)['sha256'],
                'loaded_modules': os.environ.get('LOADEDMODULES','')}
    script = os.environ.get('CALMAR_EXECUTION_SCRIPT')
    if script and Path(script).is_file():
        identity['script_sha256'] = fingerprint(script)['sha256']
    record = final / 'calmar-cache.json' if final.suffix == '' else Path(str(final) + '.cache.json')
    def inspect(path):
        images = list(expected(path))
        if not images:
            raise ValueError(f'No expected images declared for {path}')
        return {str(p.relative_to(path) if path.is_dir() else p.name): validator(p) for p in images}
    if final.exists() and not overwrite:
        if not record.exists() and output_id in LEGACY_IS_STALE:
            raise RuntimeError(
                f'Stale output preserved at {final}. It has no run record, so it predates the current '
                f'{output_id} method. Set OVERWRITE to recompute; the old output is kept as *.previous.*.')
        metrics = inspect(final)
        cached = json.loads(record.read_text()) if record.exists() else None
        hashes = [fingerprint(p)['sha256'] for p in expected(final)]
        previous = cached.get('identity', {}) if cached else {}
        compatible = (previous.get('inputs') == identity['inputs']
                      and previous.get('options') == identity['options']
                      and previous.get('algorithm_version', 1) == identity['algorithm_version'])
        if cached is not None and (not compatible or cached.get('images') != hashes):
            changed = sorted(k for k in set(identity['options']) | set(previous.get('options', {}))
                             if identity['options'].get(k) != previous.get('options', {}).get(k))
            raise RuntimeError(
                f'Stale output preserved at {final}. '
                + (f'Method options changed ({", ".join(changed)}). ' if changed else
                   'Its inputs or files changed since it was computed. ')
                + 'Set the stage\'s overwrite option (OVERWRITE, BCB_OVERWRITE or DEEPDISCO_OVERWRITE) '
                  'to recompute; the old output is kept as *.previous.*.')
        # Legacy outputs remain explicitly unverified caches, not newly computed results.
        return {'path': str(final), 'status': 'cached' if record.exists() else 'legacy-cache', 'images': metrics,
                'commands': (cached or {}).get('commands', []), 'tools': (cached or {}).get('tools', {})}
    if os.environ.get('CALMAR_REUSE_ONLY') == '1':
        raise RuntimeError(f'Reuse-only verification requires an existing product: {final}')
    final.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=final.name+'.attempt.', dir=final.parent) as d:
        tmp = Path(d) / final.name
        first_command = len(COMMANDS)
        build(tmp)
        commands = [c.replace(str(tmp), str(final)) for c in COMMANDS[first_command:]]
        names = {c.split()[1] if c.startswith('bash ') else c.split()[0] for c in commands if ' ' in c}
        tools = {key: value for key, value in TOOLS.items() if key.split(' ')[0] in names}
        metrics = inspect(tmp)
        cache = {'identity':identity, 'images':[fingerprint(p)['sha256'] for p in expected(tmp)],
                 'commands': commands, 'tools': tools}
        if tmp.is_dir():
            (tmp/'calmar-cache.json').write_text(json.dumps(cache, indent=2))
        preserved = []
        backup = final.with_name(final.name+'.previous.'+uuid4().hex)
        if overwrite and final.exists():
            # Keep the old product and its provenance, including manual QC.
            companions = [(final,backup), (Path(str(final)+'.prov.json'),Path(str(backup)+'.prov.json')),
                          (Path(str(final)+'.cache.json'),Path(str(backup)+'.cache.json'))]
            if final.is_file():
                companions.append((q.sidecar_path_for(final),Path(str(backup)+'.qc.json')))
            for old,new in companions:
                if old.exists():
                    os.replace(old,new)
                    preserved.append((old,new))
        try:
            publish(tmp, final, output_id)
            if not final.is_dir():
                temp_record = Path(d) / 'identity.json'
                temp_record.write_text(json.dumps(cache, indent=2))
                os.replace(temp_record, record)
        except Exception:
            # A failed replacement must leave the previously usable result.
            if preserved:
                if final.is_dir(): shutil.rmtree(final)
                else: final.unlink(missing_ok=True)
                Path(str(final)+'.prov.json').unlink(missing_ok=True)
                for old,new in reversed(preserved): os.replace(new,old)
            raise
    return {'path': str(final), 'status': 'computed', 'images': metrics, 'commands': commands, 'tools': tools}


def warp_product(linda, native, final, label, *, overwrite=False):
    """Publish a validated MNI mask only after the complete transform succeeds."""
    reference = linda/'Subject_in_MNI.nii.gz'
    inputs = [native, reference, linda/'Reg3_sub_to_template_warp.nii.gz',
              linda/'Reg3_sub_to_template_affine.mat']
    source = Path(__file__).resolve().parents[1]/'src'
    inputs += [source/'analysis_15_warp_native_to_mni.sh', source/'r'/'warp_native_mask_to_ch2.R']
    inputs += templates.inputs()
    def build(tmp):
        if q.warp_native_mask_to_mni(linda,native,tmp,tool_label=label):
            raise RuntimeError(f'{label} warp failed')
    return product(final, inputs, {'module':'linda/0.5.1','interpolation':'NearestNeighbor',
                                   'template': templates.NAME},
                   build, lambda f:[f], label,
                   validator=lambda p:validate_image(p,reference,binary=True),overwrite=overwrite)


ANTS_MODULE = 'ants/2.6.5'
# antsRegistrationSyN.sh output prefix of the registration step (LINDA not run).
REGISTRATION_PREFIX = 'T1w_to_MNI152_'


def registration_files(registration):
    """The registration step's transforms: native T1w -> MNI152."""
    return (registration/f'{REGISTRATION_PREFIX}1Warp.nii.gz',
            registration/f'{REGISTRATION_PREFIX}0GenericAffine.mat')


def ants_warp_product(registration, native, final, label, *, overwrite=False):
    """Like ``warp_product``, with the registration step's ANTs transforms."""
    reference = registration/'Subject_in_MNI.nii.gz'
    warp, affine = registration_files(registration)
    script = Path(__file__).resolve().parents[1]/'src'/'analysis_42_apply_template_registration.sh'
    def build(tmp):
        run(['bash', script, '--input', native, '--reference', reference, '--warp', warp,
             '--affine', affine, '--output', tmp, '--interp', 'NearestNeighbor'], tmp.parent/f'{label}.log')
    return product(final, [native, reference, warp, affine, script],
                   {'module': ANTS_MODULE, 'interpolation': 'NearestNeighbor', 'template': templates.NAME,
                    'registration': 'ants'},
                   build, lambda f: [f], label,
                   validator=lambda f: validate_image(f, reference, binary=True), overwrite=overwrite)


def template_warp(config, p, native, final, label, *, overwrite=False):
    """Warp a native T1w-space mask to MNI152 with the participant's template
    registration: LINDA's when LINDA runs, else the registration step's."""
    if template_source(config) == 'linda':
        return warp_product(p['linda'], native, final, label, overwrite=overwrite)
    return ants_warp_product(p['registration'], native, final, label, overwrite=overwrite)


def paths(request, entry):
    """Derivative folders of every tool for one entry (see calmar.study)."""
    return derivative_dirs(request['dataset'], request['config'], entry)


def manual_inputs(request, entry):
    """Locate an optional manual lesion mask: ``(mask, reference_scan, space)``.

    With MANUAL_MASK_PATH set, that template is used. Otherwise the dataset's
    publisher masks are searched (``derivatives/*lesion*/sub-X/**/*_desc-lesion_mask``),
    preferring the T1's own session. A mask from another session is still used;
    its session is reported so reviewers can judge the cross-session registration.
    """
    config = request['config']
    sub, ses = entry['subject'], entry.get('session') or ''
    def fmt(value):
        return Path(str(value).format(sub=sub, ses=ses, subject=sub, session=ses))
    if config.get('MANUAL_MASK_PATH'):
        space = config.get('MANUAL_MASK_SPACE', 't1')
        ref = config.get('MANUAL_MASK_REF')
        if space == 'other' and not ref:
            raise ValueError('A manual mask in another scan requires MANUAL_MASK_REF.')
        return fmt(config['MANUAL_MASK_PATH']), fmt(ref) if ref else None, space
    root = Path(request['dataset'])
    hits = []
    roots = ([Path(config['MANUAL_MASK_ROOT'])] if config.get('MANUAL_MASK_ROOT') else
             [root/'derivatives'/folder for folder in
              ['manual-lesion','manual_lesion','lesion_masks','manual_masks']])
    for folder in roots:
        hits.extend((folder/sub).rglob('*_desc-lesion_mask.nii.gz'))
    hits.sort(key=lambda p: (f'_{ses}_' not in p.name, str(p)))
    if not hits:
        return None, None, None
    mask = hits[0]
    mask_ses = next((p for p in mask.parts if p.startswith('ses-')), '')
    ref = root/sub/mask_ses/'anat'/mask.name.replace('_desc-lesion_mask', '')
    return mask, ref, 'other'


def validate_transform(path):
    """A LINDA transform must be fully readable: finite warp data, parseable ITK affine."""
    path = Path(path)
    if path.name.endswith('.nii.gz'):
        data = np.asarray(nib.load(str(path)).dataobj)
        if not data.size or not np.isfinite(data).all():
            raise ValueError(f'Invalid warp field: {path}')
    else:
        import SimpleITK as sitk
        try:
            sitk.ReadTransform(str(path))
        except RuntimeError as error:
            raise ValueError(f'Unreadable ITK transform: {path}') from error
    return path


def seed_env(seed):
    """Environment that fixes ANTs' and R's random number generators inside a
    Neurodesk container (APPTAINERENV_/SINGULARITYENV_ survive --cleanenv)."""
    values = {'ANTS_RANDOM_SEED': str(seed), 'CALMAR_R_SEED': str(seed)}
    return {f'{prefix}{k}': v for k, v in values.items() for prefix in ('', 'APPTAINERENV_', 'SINGULARITYENV_')}


def linda_threads(config):
    """CONFIG["LINDA_THREADS"]: CPU threads for LINDA's registrations. 1 (default)
    makes seeded LINDA bit-identical between runs; 4 is ~2x faster but the same
    T1 then gave Dice 0.96 between runs (src/analysis_39)."""
    threads = int(config.get('LINDA_THREADS', 1))
    if not 1 <= threads <= 16:
        raise ValueError(f'LINDA_THREADS must be between 1 and 16, not {threads}')
    return threads


def mask_session(mask):
    return next((p for p in Path(mask).parts if p.startswith('ses-')), None) if mask else None


def run(command, log, **kwargs):
    from .process_output import run_logged
    return run_logged([str(x) for x in command], log, check=True, **kwargs)


def tract_outputs(folder):
    return sorted([*folder.rglob('*.nii.gz'), *folder.rglob('*.nii'), *folder.rglob('*.csv')])


def validate_tract_output(path):
    if path.suffix != '.csv':
        return validate_image(path)
    import pandas as pd
    table = pd.read_csv(path)
    if table.empty:
        raise ValueError(f'Empty Tractotron table: {path}')
    return {'rows': len(table), 'columns': list(table.columns)}


# ── Template grids ───────────────────────────────────────────────────────────
# LINDA's "MNI" outputs are on the ch2 (Colin27) template: 181x217x181, 1 mm,
# origin (-90,-125,-71). BCBToolkit's tractography and DeepDisco expect the FSL
# MNI152 grids below. Their voxel centres coincide with ch2's integer-mm centres,
# so world-coordinate nearest-neighbour resampling onto them is exact.
FSL_GRID_1MM = ((182, 218, 182), np.array([[-1., 0, 0, 90], [0, 1., 0, -126], [0, 0, 1., -72], [0, 0, 0, 1.]]))


def to_fsl_1mm(mask_path, out_path):
    """Place a binary template-space mask on BCBToolkit's MNI152 1 mm grid by
    world coordinates. (BCBToolkit's own reslice matches ch2 inputs by voxel
    index, which shifts lesions 1 mm posterior and 1 mm inferior.)"""
    img = resample_from_to(nib.load(str(mask_path)), FSL_GRID_1MM, order=0)
    data = (np.asarray(img.dataobj) > .5).astype('uint8')
    nib.save(nib.Nifti1Image(data, FSL_GRID_1MM[1]), str(out_path))
    return out_path


def to_fsl_2mm(mask_path, out_path, method='coverage'):
    """DeepDisco input: binary mask on the FSL MNI152 2 mm grid (91x109x91).

    ``coverage`` keeps a 2 mm voxel when at least half of it is lesion (box
    average with weights 1/4,1/2,1/4 per axis on the 1 mm mask, then sampled at
    the 2 mm centres). ``nearest`` is the original point sampling, which picks
    one 1 mm sub-voxel and can drop thin parts of a lesion.
    """
    img = nib.load(str(mask_path))
    data = (np.asarray(img.dataobj) > .5).astype('float32')
    if method == 'coverage':
        from scipy.ndimage import convolve1d
        if not np.allclose(np.abs(np.diag(img.affine)[:3]), 1.0, atol=1e-3):
            raise ValueError(f'Coverage downsampling expects a 1 mm grid: {mask_path}')
        for axis in range(3):
            data = convolve1d(data, [.25, .5, .25], axis=axis, mode='constant')
    elif method != 'nearest':
        raise ValueError(f'Unknown DeepDisco downsampling: {method!r}')
    sampled = resample_from_to(nib.Nifti1Image(data, img.affine), FSL_GRID, order=0)
    binary = (np.asarray(sampled.dataobj) >= .5).astype('uint8')
    nib.save(nib.Nifti1Image(binary, FSL_GRID[1]), str(out_path))
    return out_path


# ── One function per processing step ────────────────────────────────────────
# Each receives the request config, one entry and its derivative folders, and
# returns a list of published products. ``options`` dicts are part of every
# product's cache identity: changing a value marks existing outputs stale.

def step_acquisition(config, entry, p, request):
    """Fetch (datalad get) the T1w and, if found, the manual mask + its scan."""
    t1 = Path(entry['t1w'])
    mask, ref, _ = manual_inputs(request, entry)
    outputs = []
    for source in [t1] + ([mask] if mask else []) + ([ref] if ref else []):
        if not ensure_nifti_content(source, request['dataset']):
            raise RuntimeError(f'Acquisition failed: {source}')
        outputs.append({'path': str(source), 'image': validate_image(source)})
    return outputs


BRAIN_MASK_METHODS = ('hdbet+synthstrip', 'hdbet')


def step_brain(config, entry, p, request):
    """Brain mask of the whole-head T1w, used by LINDA and to clip SynthStroke.

    BRAIN_MASK="hdbet" (default): the HD-BET (hdbet/1.0.0) mask of brain tissue.
    BRAIN_MASK="hdbet+synthstrip": union with SynthStrip (synthstrip/7.4.1,
    brain + surrounding CSF). HD-BET follows surviving tissue and leaves
    CSF-filled chronic infarct cavities outside the brain; the union keeps them,
    but LINDA then also labels more CSF next to the lesion (8 sessions of
    ds004884: median Dice 0.61 -> 0.59, false positives 45 -> 84 ml; better only
    where >= 40 ml of the lesion lay outside HD-BET). It is therefore offered per
    participant by the skull-strip repair rather than as the default.
    The component masks are kept (``*_desc-hdbet_*``, ``*_desc-synthstrip_*``);
    ``*_brain_mask.nii.gz`` is the mask every later step uses.
    """
    t1 = Path(entry['t1w'])
    stem = t1.name.removesuffix('.nii.gz')
    mode, device = config.get('HDBET_MODE', 'fast'), config.get('HDBET_DEVICE') or 'cpu'
    method = config.get('BRAIN_MASK', 'hdbet')
    if method not in BRAIN_MASK_METHODS:
        raise ValueError(f'BRAIN_MASK must be one of {BRAIN_MASK_METHODS}, not {method!r}')
    def build(tmp):
        result = q.run_hd_bet(t1, tmp, prefer='hd-bet', device=device, mode=mode, desc='hdbet')
        if result['returncode']:
            raise RuntimeError('HD-BET failed')
        validate_image(result['mask'], t1, binary=True, nonempty=True)
        img = nib.load(str(t1))
        mask = np.asarray(nib.load(str(result['mask'])).dataobj) > 0
        if method == 'hdbet+synthstrip':
            strip = q.run_hd_bet(t1, tmp, prefer='mri_synthstrip', desc='synthstrip')
            if strip['returncode']:
                raise RuntimeError('SynthStrip failed')
            validate_image(strip['mask'], t1, binary=True, nonempty=True)
            synth = np.asarray(nib.load(str(strip['mask'])).dataobj) > 0
            record_step(f'brain mask = HD-BET mask OR SynthStrip mask: SynthStrip adds '
                        f'{(synth & ~mask).sum()} voxels, HD-BET adds {(mask & ~synth).sum()}')
            mask |= synth
        save_like(mask, img, tmp/f'{stem}_brain_mask.nii.gz')
        save_like(np.where(mask, np.asarray(img.dataobj), 0), img, tmp/f'{stem}_brain.nii.gz', dtype=np.float32)
    modules = 'hdbet/1.0.0' + (' synthstrip/7.4.1' if method == 'hdbet+synthstrip' else '')
    def expected(d):
        files = [d/f'{stem}_brain_mask.nii.gz', d/f'{stem}_brain.nii.gz', d/f'{stem}_desc-hdbet_brain_mask.nii.gz']
        return files + ([d/f'{stem}_desc-synthstrip_brain_mask.nii.gz'] if method == 'hdbet+synthstrip' else [])
    return [product(p['hdbet'], [t1], {'method': method, 'mode': mode, 'device': device, 'module': modules}, build,
                    expected, 'brain',
                    validator=lambda f: validate_image(f, t1, binary='mask' in f.name, nonempty=True),
                    overwrite=config.get('OVERWRITE', False))]


def step_linda(config, entry, p, request):
    """LINDA 0.5.1 lesion segmentation, then everything into MNI152.

    With USE_HDBET_PREPROCESSING the brain mask of step_brain is passed to
    LINDA's R API (``brain_mask=``), replacing LINDA's own skull strip, which
    over-strips cortex next to large lesions.

    LINDA registers the brain to its ch2 (Colin27) template and writes
    ``Subject_in_MNI``/``Lesion_in_MNI`` there. Those are kept as ``*_in_ch2``;
    the ``*_in_MNI`` files are then rewritten on FSL MNI152 (MNI152NLin6Asym):
    the lesion from the native mask through native -> Penn -> ch2 -> MNI152 in
    one nearest-neighbour resampling, the T1 from ch2 -> MNI152 (linear).
    """
    t1 = Path(entry['t1w'])
    use_brain = config.get('USE_HDBET_PREPROCESSING', True)
    brain = q.find_best_hdbet_mask(p['hdbet']) if use_brain else None
    if use_brain and not brain:
        raise FileNotFoundError('Brain mask missing (run the brain step first)')
    if brain and '_desc-' in brain.name:
        # A skull-strip repair (desc-<mode>) takes precedence over the brain step's
        # mask; it records its own BRAIN_MASK method (chosen per participant).
        repaired_method = q.check_repaired_mask(brain, p['hdbet'], config.get('BRAIN_MASK', 'hdbet'))
    templates.require()
    seed = int(config.get('REGISTRATION_SEED', 1729))
    threads = linda_threads(config)
    if os.environ.get('SLURM_CPUS_PER_TASK') and int(os.environ['SLURM_CPUS_PER_TASK']) != threads:
        raise RuntimeError(f'LINDA_THREADS={threads} but the job has {os.environ["SLURM_CPUS_PER_TASK"]} CPUs; '
                           'submit it with calmar.scheduled.submit_step')
    bids_name = '_'.join(filter(None, [entry['subject'], entry.get('session')])) + '_space-T1w_desc-lesion_mask.nii.gz'
    def build(tmp):
        tmp.mkdir()
        command = (['bash', 'src/analysis_17_linda_predict_with_mask.sh', '--t1', t1, '--mask', brain, '--outdir', tmp]
                   if use_brain else ['linda_predict.sh', t1, tmp])
        # LINDA registers the brain to its template in each of its three prediction
        # rounds; ANTs samples voxels at random, seeded from the clock unless
        # ANTS_RANDOM_SEED is set. Unseeded, the same T1 gave lesions with Dice 0.91.
        if brain and '_desc-' in brain.name:
            record_step(f'brain mask: skull-strip repair {brain.name} (BRAIN_MASK={repaired_method})')
        run(command, tmp/'processing.log', env={**os.environ, **seed_env(seed)})
        record_step(f'ANTS_RANDOM_SEED={seed} and R set.seed({seed}) inside the LINDA container')
        validate_image(tmp/'Prediction3_native.nii.gz', t1)
        shutil.copy2(tmp/'Prediction3_native.nii.gz', tmp/bids_name)
        for name in ('Subject', 'Lesion'):
            os.replace(tmp/f'{name}_in_MNI.nii.gz', tmp/f'{name}_in_ch2.nii.gz')
        if q.warp_native_mask_to_mni(tmp, tmp/'Subject_in_ch2.nii.gz', tmp/'Subject_in_MNI.nii.gz',
                                     interp='Linear', input_space='ch2', reference=templates.T1,
                                     tool_label='ch2_to_mni152'):
            raise RuntimeError('ch2 -> MNI152 warp of the subject image failed')
        if q.warp_native_mask_to_mni(tmp, tmp/'Prediction3_native.nii.gz', tmp/'Lesion_in_MNI.nii.gz',
                                     tool_label='linda_mni152'):
            raise RuntimeError('native -> MNI152 warp of the LINDA lesion failed')
        validate_image(tmp/'Lesion_in_MNI.nii.gz', tmp/'Subject_in_MNI.nii.gz', binary=True)
    result = product(p['linda'], [t1]+([brain] if brain else [])+templates.inputs(),
                     {'module': 'linda/0.5.1', 'brain_mask_bypass': bool(use_brain), 'template': templates.NAME,
                      'random_seed': seed, 'threads': threads},
                     build, lambda d: [d/'Lesion_in_MNI.nii.gz', d/'Prediction3_native.nii.gz', d/'Subject_in_MNI.nii.gz',
                                       d/'Lesion_in_ch2.nii.gz', d/'Subject_in_ch2.nii.gz'],
                     'linda', overwrite=config.get('OVERWRITE', False))
    # SynthStroke and manual masks reuse these transforms: check them here, and
    # list them as outputs so a step receipt is not reused once they disappear.
    # (Not part of the product's image hashes, so existing cache records stay valid.)
    transforms = []
    for name in ('Reg3_sub_to_template_warp.nii.gz', 'Reg3_sub_to_template_affine.mat'):
        path = p['linda']/name
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(f'LINDA output lacks {name}, needed to warp other masks: {p["linda"]}')
        validate_transform(path)
        transforms.append({'path': str(path), 'status': 'validated', 'reason': 'transform for later warps'})
    return [result, *transforms]


def step_synthstroke(config, entry, p, request):
    """SynthStroke (synth-plus weights) lesion segmentation, then warp to MNI152.

    SynthStroke segments the whole head, so voxels outside the brain mask
    (step_brain) dilated by 2 voxels are removed; the untouched prediction is kept as
    ``prediction_lesion_mask_raw.nii.gz``.
    """
    t1 = Path(entry['t1w'])
    weights = Path(config.get('SYNTHSTROKE_WEIGHTS_DIR', 'data/models/synthstroke-synth-plus'))/'model.safetensors'
    brain = q.find_best_hdbet_mask(p['hdbet'])
    if not weights.is_file() or not brain:
        raise FileNotFoundError('Synth-plus weights and the brain mask are required')
    tta = config.get('SYNTHSTROKE_TTA', True)
    def build(tmp):
        tmp.mkdir()
        command = ['synthstroke', '--input', t1, '--outdir', tmp, '--weights', weights] + (['--tta'] if tta else [])
        run(command, tmp/'processing.log', timeout=config.get('SYNTHSTROKE_TIMEOUT', 5400))
        cleaned = q.mask_prediction_to_brain(tmp/'prediction_lesion_mask.nii.gz', brain)
        record_step(f'remove prediction outside the brain mask dilated 2 voxels '
                    f'(calmar.qc.mask_prediction_to_brain): {cleaned and cleaned.get("removed", 0)} voxels removed')
        validate_image(tmp/'prediction_lesion_mask.nii.gz', t1, binary=True)
    overwrite = config.get('OVERWRITE', False)
    outputs = [product(p['synthstroke'], [t1, weights, brain], {'module': 'synthstroke/0.0.0', 'tta': tta, 'brain_dilation': 2},
                       build, lambda d: [d/'prediction_lesion_mask.nii.gz'], 'synthstroke',
                       validator=lambda f: validate_image(f, t1, binary=True), overwrite=overwrite)]
    if template_source(config) == 'linda':
        # Without LINDA, the registration step (which needs this mask) warps it.
        outputs.append(warp_product(p['linda'], p['synthstroke']/'prediction_lesion_mask.nii.gz',
                                    p['synthstroke']/'SynthStroke_in_MNI.nii.gz', 'synthstroke_mni', overwrite=overwrite))
    return outputs


def registration_threads(config):
    """CONFIG["REGISTRATION_THREADS"]: CPU threads of the registration step's SyN
    stage. Its result does not depend on the count (ANTs' reproducible route)."""
    threads = int(config.get('REGISTRATION_THREADS', 4))
    if not 1 <= threads <= 16:
        raise ValueError(f'REGISTRATION_THREADS must be between 1 and 16, not {threads}')
    return threads


def check_initial_collapsed(initial, final):
    """The SyN stage's affine must equal the initial affine it started from;
    otherwise the transforms in the folder would not be the full native -> MNI152 pair."""
    import SimpleITK as sitk
    a, b = (np.array(sitk.ReadTransform(str(f)).GetParameters()) for f in (initial, final))
    if a.shape != b.shape or not np.allclose(a, b, atol=1e-6):
        raise RuntimeError(f'SyN output affine {final} differs from its initial affine {initial}')


def step_registration(config, entry, p, request):
    """Template registration when LINDA is not run (LINDA's own is used otherwise).

    The brain-extracted T1w (step_brain's mask) is registered to the FSL MNI152
    brain with ANTs (ants/2.6.5). The SynthStroke lesion, dilated by 2 voxels, is
    left out of the moving image's cost-function mask so it does not pull the
    warp (cost-function masking, Brett et al. 2001). ANTs' reproducible route:
    an affine stage with one thread and a fixed seed (Mattes MI is not
    deterministic multithreaded), then SyN (cross-correlation) from it with
    REGISTRATION_THREADS. Outputs: the transforms, ``Subject_in_MNI`` (whole-head
    T1w, linear) and ``SynthStroke_in_MNI`` (nearest neighbour).
    """
    from scipy.ndimage import binary_dilation
    t1 = Path(entry['t1w'])
    brain = q.find_best_hdbet_mask(p['hdbet'])
    lesion = p['synthstroke']/'prediction_lesion_mask.nii.gz'
    if not brain:
        raise FileNotFoundError('Brain mask missing (run the brain step first)')
    if not lesion.is_file():
        raise FileNotFoundError('SynthStroke lesion missing (run the SynthStroke step first): '
                                'it is excluded from the registration')
    templates.require()
    seed = int(config.get('REGISTRATION_SEED', 1729))
    threads = registration_threads(config)
    warp_name, affine_name = (f.name for f in registration_files(Path()))
    def build(tmp):
        tmp.mkdir()
        img = nib.load(str(t1))
        mask = np.asarray(nib.load(str(brain)).dataobj) > 0
        lesion_data = np.asarray(resample_from_to(nib.load(str(lesion)), img, order=0).dataobj) > 0
        save_like(np.where(mask, np.asarray(img.dataobj), 0), img, tmp/'T1w_brain.nii.gz', dtype=np.float32)
        excluded = binary_dilation(lesion_data, iterations=2)
        save_like(mask & ~excluded, img, tmp/'cost_function_mask.nii.gz')
        record_step(f'moving cost-function mask = brain mask ({brain.name}) minus the SynthStroke lesion '
                    f'dilated 2 voxels: {int((mask & excluded).sum())} brain voxels excluded')
        fixed, masks = templates.T1_BRAIN, f'{templates.BRAIN_MASK},{tmp/"cost_function_mask.nii.gz"}'
        log = tmp.parent/'processing.log'
        run(['antsRegistrationSyN.sh', '-d', 3, '-t', 'a', '-n', 1, '-e', seed, '-f', fixed,
             '-m', tmp/'T1w_brain.nii.gz', '-x', masks, '-o', tmp.parent/'affine_'], log)
        run(['antsRegistrationSyN.sh', '-d', 3, '-t', 'so', '-n', threads, '-e', seed, '-f', fixed,
             '-m', tmp/'T1w_brain.nii.gz', '-x', masks, '-i', tmp.parent/'affine_0GenericAffine.mat',
             '-o', tmp.parent/REGISTRATION_PREFIX], tmp.parent/'syn.log')
        # The SyN run starts from the affine (-i); with ANTs' default collapsing
        # (-z 1) its 0GenericAffine already contains it (checked in build).
        check_initial_collapsed(tmp.parent/'affine_0GenericAffine.mat',
                                tmp.parent/f'{REGISTRATION_PREFIX}0GenericAffine.mat')
        for name in (warp_name, affine_name, f'{REGISTRATION_PREFIX}1InverseWarp.nii.gz'):
            shutil.copy2(tmp.parent/name, tmp/name)
        run(['antsApplyTransforms', '-d', 3, '-i', t1, '-r', templates.T1, '-t', tmp/warp_name, '-t', tmp/affine_name,
             '-n', 'Linear', '-o', tmp/'Subject_in_MNI.nii.gz'], tmp.parent/'subject.log')
        validate_image(tmp/'Subject_in_MNI.nii.gz', templates.T1)
        for name in (warp_name, affine_name):
            validate_transform(tmp/name)
    overwrite = config.get('OVERWRITE', False)
    registration = product(p['registration'], [t1, brain, lesion, templates.T1_BRAIN, templates.BRAIN_MASK, templates.T1],
                           {'module': ANTS_MODULE, 'template': templates.NAME, 'random_seed': seed,
                            'stages': 'affine (MI, 1 thread) + SyN (CC)', 'cost_function_mask': 'brain minus SynthStroke lesion dilated 2'},
                           build, lambda d: [d/'Subject_in_MNI.nii.gz', d/'cost_function_mask.nii.gz'],
                           'registration', overwrite=overwrite)
    return [registration,
            ants_warp_product(p['registration'], lesion, mni_masks(p)['synthstroke'],
                              'synthstroke_mni', overwrite=overwrite)]


def step_manual(config, entry, p, request):
    """Bring the optional manual mask into T1 space, then warp it to MNI152.

    MANUAL_MASK_SPACE: ``t1`` (nearest-neighbour regrid only), ``other``
    (rigid Mattes-MI registration of its scan to the T1, seeded), ``mni``
    (used directly).
    """
    t1 = Path(entry['t1w'])
    mask, ref, space = manual_inputs(request, entry)
    if mask is None:
        return [{'status': 'skipped', 'reason': 'No optional manual mask available'}]
    overwrite = config.get('OVERWRITE', False)
    final_mni = p['template']/'ExpertMask_in_MNI.nii.gz'
    seed = config.get('REGISTRATION_SEED', 1729)
    name = 'ManualLesion_in_T1_sitk.nii.gz' if space == 'other' else 'ManualLesion_in_T1.nii.gz'
    def build(tmp):
        tmp.mkdir()
        if space == 'other':
            record_step(f'SimpleITK rigid registration {ref} -> {t1} (Mattes MI, 3 levels, seed {seed}); '
                        f'mask resampled nearest-neighbour (calmar.qc.coregister_t2_mask_to_t1)')
            q.coregister_t2_mask_to_t1(t1, ref, mask, tmp/name, t2_out_path=tmp/'T2_in_T1_sitk.nii.gz', sampling_seed=seed)
        elif space == 't1':
            record_step(f'nibabel nearest-neighbour regrid of {mask} onto {t1}')
            nib.save(resample_from_to(nib.load(mask), nib.load(t1), order=0), tmp/name)
        else:
            raise ValueError('MNI manual inputs must be used directly, without a native-space comparison')
        validate_image(tmp/name, t1)
    if space == 'mni':
        outputs = [product(final_mni, [mask], {'space': 'mni'}, lambda tmp: shutil.copy2(mask, tmp), lambda f: [f], 'manual',
                           validator=lambda f: validate_image(f, p['template']/'Subject_in_MNI.nii.gz', binary=True),
                           overwrite=overwrite)]
    else:
        cmp = p['template']/'_manual_mask_compare'
        outputs = [product(cmp, [t1, mask]+([ref] if ref else []), {'space': space, 'registration': 'rigid-MattesMI', 'sampling_seed': seed},
                           build, lambda d: [d/name], 'manual_native',
                           validator=lambda f: validate_image(f, t1, binary=True), overwrite=overwrite),
                   template_warp(config, p, cmp/name, final_mni, 'manual_mni', overwrite=overwrite)]
    validate_image(final_mni, p['template']/'Subject_in_MNI.nii.gz')
    return outputs


def lesion_sources(config, key, p):
    """Template-space masks selected for a disconnectome step."""
    masks = mni_masks(p)
    selected = config.get(key, 'all')
    sources = list(masks) if selected == 'all' else (['linda', 'manual'] if selected == 'both' else [selected])
    # Segmentations that were not selected are not expected ("all"/"both").
    run = segmentation_methods(config)
    if selected in ('all', 'both'):
        sources = [s for s in sources if s == 'manual' or s in run]
    return selected, [(s, masks[s]) for s in sources]


def _keep_stale(outputs, make, legacy_note=None):
    """A method change marks old disconnectomes stale: report it, keep going.

    Outputs from before run records ("legacy-cache") cannot be checked against
    the current options; ``legacy_note`` says what may differ.
    """
    try:
        result = make()
        if legacy_note and result.get('status') == 'legacy-cache':
            result['reason'] = legacy_note
        outputs.append(result)
    except RuntimeError as error:
        if 'Stale output preserved' not in str(error):
            raise
        outputs.append({'status': 'stale', 'reason': str(error)})


def step_deepdisco(config, entry, p, request):
    """DeepDisco (deepdisco/20251008) disconnectome for each selected mask."""
    selected, sources = lesion_sources(config, 'DEEPDISCO_MASK_SOURCE', p)
    method = config.get('DEEPDISCO_DOWNSAMPLING', 'coverage')
    if method not in ('coverage', 'nearest'):
        raise ValueError(f'DEEPDISCO_DOWNSAMPLING must be "coverage" or "nearest", not {method!r}')
    models = list(MODELS) if config.get('DEEPDISCO_RUN_ALL', True) else config['DEEPDISCO_MODELS']
    outputs = []
    for source, mask in sources:
        if not mask.exists() and selected in ('all', 'both'):
            outputs.append({'path': str(mask), 'status': 'missing', 'reason': f'{source} MNI mask unavailable'})
            continue
        validate_image(mask)
        for model in models:
            final = p['deepdisco']/f'DeepDisco_{file_token(source)}_{model}.nii.gz'
            def build(tmp, mask=mask, model=model):
                input_path = to_fsl_2mm(mask, tmp.parent/'input.nii.gz', method)
                record_step(f'{mask} -> FSL MNI152 2 mm grid ({method} downsampling, threshold 0.5)')
                run(['deepdisco-cli', '--input', input_path, '--model', MODELS[model], '--output', tmp], tmp.parent/'processing.log')
            # Options of the original point-sampling method are unchanged, so
            # outputs made with it stay valid when it is selected explicitly.
            options = {'model': model, 'threshold': .5, 'module': 'deepdisco/20251008'}
            if method != 'nearest':
                options['downsampling'] = method
            _keep_stale(outputs, lambda: product(final, [mask], options, build, lambda f: [f], 'deepdisco',
                                                 overwrite=config.get('DEEPDISCO_OVERWRITE', False)),
                        legacy_note=None if method == 'nearest' else
                        'Output predates run records, so it was probably made with the earlier nearest-neighbour '
                        'downsampling; set DEEPDISCO_OVERWRITE=True to recompute with coverage downsampling.')
    return outputs


def step_bcb(config, entry, p, request):
    """BCBToolkit disconnectome (bcbtoolkit/0.0.0, run_disco.sh) per mask.

    The mask is first placed on BCBToolkit's MNI152 1 mm grid by world
    coordinates (BCB_INPUT_GRID="mni152"); the map is returned to the mask's
    grid the same way, so all disconnectomes share LINDA's template grid.
    """
    selected, sources = lesion_sources(config, 'BCB_MASKS', p)
    grid = config.get('BCB_INPUT_GRID', 'mni152')
    if grid not in ('mni152', 'native'):
        raise ValueError(f'BCB_INPUT_GRID must be "mni152" or "native", not {grid!r}')
    overwrite = config.get('BCB_OVERWRITE', config.get('OVERWRITE', False))
    outputs = []
    for source, mask in sources:
        if not mask.exists() and selected in ('all', 'both'):
            outputs.append({'path': str(mask), 'status': 'missing', 'reason': f'{source} MNI mask unavailable'})
            continue
        validate_image(mask)
        token = file_token(source)
        final = p['bcbtoolkit']/f'Disconnectome_{token}.nii.gz'
        def build(tmp, mask=mask):
            inputs = tmp.parent/'input'; inputs.mkdir()
            if grid == 'mni152':
                to_fsl_1mm(mask, inputs/'Lesion_in_MNI.nii.gz')
                record_step(f'{mask} -> FSL MNI152 1 mm grid (world-coordinate nearest neighbour)')
            else:
                shutil.copy2(mask, inputs/'Lesion_in_MNI.nii.gz')
            out = tmp.parent/'disco'; out.mkdir()
            try:
                run(['run_disco.sh', '-l', inputs, '-o', out], tmp.parent/'processing.log',
                    env={**os.environ, 'FSLOUTPUTTYPE': 'NIFTI_GZ'})
            except subprocess.CalledProcessError as error:
                if error.returncode in (132, -4):
                    raise RuntimeError('BCBToolkit failed with SIGILL. No validated Python fallback is available; '
                                       'the incomplete disconnectome has not been published.') from error
                raise
            images = sorted(out.rglob('*.nii*'))
            if len(images) != 1:
                raise RuntimeError(f'Expected one disconnectome, found {images}')
            if grid == 'mni152':
                back = resample_from_to(nib.load(str(images[0])), nib.load(str(mask)), order=1)
                nib.save(back, str(tmp))
                record_step('disconnectome -> lesion mask grid (world-coordinate linear)')
            else:
                shutil.copy2(images[0], tmp)
        options = {'module': 'bcbtoolkit/0.0.0'}
        if grid == 'mni152':
            options['input_grid'] = 'fsl-mni152-1mm-world'
        _keep_stale(outputs, lambda: product(final, [mask], options, build, lambda f: [f], 'bcb', overwrite=overwrite),
                    legacy_note=None if grid == 'native' else
                    'Output predates run records, so it was probably made before the BCB grid correction '
                    '(lesion read 1 mm posterior and 1 mm inferior); set BCB_OVERWRITE=True to recompute.')
        if config.get('BCB_RUN_TRACTOTRON', False) and shutil.which('tractotron_cli.sh'):
            atlas = str(Path(os.environ.get('BCBTOOLKIT_ROOT', '/opt/BCBToolKit'))/'Tools/HCP1065/prob')
            tract_final = p['bcbtoolkit']/('Tractotron_probs' if source == 'linda' else f'Tractotron_probs_{token}')
            def build_tract(tmp, mask=mask):
                inputs = tmp.parent/'tract_input'; inputs.mkdir()
                tmp.mkdir()
                prepared = inputs/'Lesion_in_MNI.nii.gz'
                run(['bash', 'src/analysis_36_prepare_tractotron.sh', mask, prepared, atlas], tmp/'preparation.log')
                shutil.copy2(Path(str(prepared)+'.grid.json'), tmp/'input_grid.json')
                run(['tractotron_cli.sh', '-l', inputs, '-t', atlas, '-o', tmp], tmp/'processing.log',
                    env={**os.environ, 'FSLOUTPUTTYPE': 'NIFTI_GZ'})
            outputs.append(product(tract_final, [mask, Path('src/analysis_36_prepare_tractotron.sh'),
                                   Path('src/python/prepare_tractotron.py')],
                                   {'module': 'bcbtoolkit/0.0.0', 'atlas': atlas, 'grid': 'atlas-reference'},
                                   build_tract, tract_outputs, 'tractotron', validator=validate_tract_output,
                                   overwrite=config.get('OVERWRITE', False)))
    return outputs


STEPS = {'acquisition': step_acquisition, 'brain': step_brain, 'linda': step_linda,
         'synthstroke': step_synthstroke, 'registration': step_registration, 'manual': step_manual,
         'bcb': step_bcb, 'deepdisco': step_deepdisco}


NOT_SELECTED = {'linda': 'LINDA is not in SEGMENTATION_METHODS',
                'synthstroke': 'SynthStroke is not in SEGMENTATION_METHODS',
                'registration': "not needed: LINDA's registration to the template is used"}


def skipped(entry, started, reason):
    return {'subject': entry['subject'], 'session': entry.get('session'),
            'seconds': time.monotonic()-started, 'outputs': [{'status': 'skipped', 'reason': reason}]}


def process(stage, request):
    """Run one step for every entry of the request (inside a Slurm job)."""
    if not os.environ.get('SLURM_JOB_ID'):
        raise RuntimeError('Submit the retained analysis script with sbatch.')
    if stage not in STEPS:
        raise ValueError(stage)
    config = request['config']
    reports = Path(config.get('PROJECT_DIR') or '.')/config.get('REPORTS_SUBDIR', 'reports')
    results = []
    for entry in request['entries']:
        started = time.monotonic()
        if stage == 'brain' and not config.get('USE_HDBET_PREPROCESSING', True):
            results.append(skipped(entry, started, 'HD-BET preprocessing disabled')); continue
        if stage in ('brain', 'linda', 'synthstroke', 'registration') and not config.get('RUN_SEGMENTATION', True):
            results.append(skipped(entry, started, 'RUN_SEGMENTATION=False')); continue
        if not stage_selected(stage, config):
            results.append(skipped(entry, started, NOT_SELECTED[stage])); continue
        p = paths(request, entry)
        outputs = STEPS[stage](config, entry, p, request)
        result = {'subject': entry['subject'], 'session': entry.get('session'),
                  'seconds': time.monotonic()-started, 'outputs': outputs}
        manual_info = None
        if stage == 'manual':
            mask, ref, space = manual_inputs(request, entry)
            manual_info = {'mask_file': str(mask) if mask else None, 'mask_space': space,
                           'mask_session': mask_session(mask), 't1_session': entry.get('session')}
            result['manual'] = manual_info
        from .step_qc import stage_evidence
        evidence = stage_evidence(stage, entry, p, reports, manual_info=manual_info, outputs=outputs)
        if evidence:
            result['qc'] = evidence
        results.append(result)
    return results


def main():
    from .scheduled import QC_VERSION
    parser = argparse.ArgumentParser()
    parser.add_argument('stage',choices=list(STEPS))
    parser.add_argument('request',type=Path)
    parser.add_argument('output',type=Path)
    args = parser.parse_args()
    request = json.loads(args.request.read_text())
    if 'CALMAR_HDBET_MODE' in os.environ:
        request['config']['HDBET_MODE'] = os.environ['CALMAR_HDBET_MODE']
    if 'CALMAR_TTA' in os.environ:
        request['config']['SYNTHSTROKE_TTA'] = os.environ['CALMAR_TTA'] == 'enabled'
    if 'CALMAR_REGISTRATION_SEED' in os.environ:
        request['config']['REGISTRATION_SEED'] = int(os.environ['CALMAR_REGISTRATION_SEED'].removeprefix('seed'))
    if args.output.exists(): raise FileExistsError(args.output)
    results = process(args.stage,request)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=args.output.name+'.attempt.',dir=args.output.parent) as d:
        tmp = Path(d)/'result'; tmp.mkdir()
        (tmp/'summary.json').write_text(json.dumps({'stage':args.stage,'request':request,'job':os.environ['SLURM_JOB_ID'],'results':results,
                                                    'qc_version':QC_VERSION},indent=2,default=str))
        publish(tmp,args.output,args.stage)


if __name__ == '__main__': main()
