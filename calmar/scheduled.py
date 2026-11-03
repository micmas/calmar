"""Notebook adapter for retained Slurm steps; display code never runs inference."""
import asyncio
import json
from pathlib import Path
import subprocess
import time
import os
import sys
import hashlib
from functools import wraps
from uuid import uuid4

from .job_progress import JobProgress

SCRIPTS = {name: f'analysis_{number}_{name}.sh' for number,name in
           [(22,'acquisition'),(23,'brain'),(24,'linda'),(25,'synthstroke'),
            (29,'registration'),(43,'openads'),(26,'manual'),(27,'bcb'),(28,'deepdisco'),
            (45,'dmri_preproc'),(46,'dmri_recon'),(47,'dmri_metrics'),
            (48,'brain_health_anatomy'),(49,'brain_health_wmh'),(50,'brain_health_metrics')]}
SCRIPTS['qc_operation'] = 'analysis_30_qc_operation.sh'
SCRIPTS['reporting'] = 'analysis_35_reporting.sh'


def inspect_logs(folder):
    """Retain a readable log review, including empty logs, for each attempt."""
    review = {}
    for name in ('stdout.log', 'stderr.log'):
        path = folder/name
        if not path.is_file():
            raise RuntimeError(f'Missing batch log: {path}')
        with path.open('rb') as stream:
            stream.seek(max(0, path.stat().st_size - 8192))
            tail = stream.read().decode('utf-8', errors='replace')
        review[name] = {'bytes': path.stat().st_size, 'tail': tail}
    (folder/'log-review.json').write_text(json.dumps(review, indent=2))
    if review['stderr.log']['tail'].strip():
        print('Batch stderr (review warnings before accepting outputs):\n'+review['stderr.log']['tail'],flush=True)
    return review


def encode(value):
    if isinstance(value,Path): return {'__path__':str(value)}
    if isinstance(value,(list,tuple)): return [encode(v) for v in value]
    if isinstance(value,dict): return {k:encode(v) for k,v in value.items()}
    return value


def decode(value):
    if isinstance(value,dict):
        if set(value)=={'__path__'}: return Path(value['__path__'])
        return {k:decode(v) for k,v in value.items()}
    if isinstance(value,list): return [decode(v) for v in value]
    return value


def scheduled_operation(function):
    """Route an explicitly requested QC operation through a retained job."""
    @wraps(function)
    def wrapper(*args,**kwargs):
        if os.environ.get('SLURM_JOB_ID'):
            return function(*args,**kwargs)
        namespace={'PROJECT_DIR':Path(__file__).resolve().parents[1],
                   '_operation_request':{'function':function.__name__,'args':encode(args),'kwargs':encode(kwargs)}}
        result=run_step_sync('qc_operation',namespace)
        return decode(result['value'])
    return wrapper


PROCESSING_STAGES = ('acquisition', 'brain', 'linda', 'synthstroke', 'registration', 'openads', 'manual', 'bcb',
                     'deepdisco', 'dmri_preproc', 'dmri_recon', 'dmri_metrics',
                     'brain_health_anatomy', 'brain_health_wmh', 'brain_health_metrics')
# Bump when saved QC evidence changes, so older receipts without it are refreshed.
QC_VERSION = 7


class StepResult(dict):
    """A step's published summary. Shows a short line instead of the raw dict;
    use ``calmar.step_summary.show_step`` for the full table and QC figures."""

    def __repr__(self):
        rows = self.get('results', [])
        return f"<{self.get('stage')} step: {len(rows)} participant result(s); show_step(...) for details>"

    def _repr_pretty_(self, printer, cycle):
        printer.text(repr(self))


def in_slurm(function):
    """Run a ``calmar.qc`` repair helper as a Slurm job (analysis_30_qc_operation.sh).

    ``in_slurm(q.run_hd_bet)(t1, out_dir)`` submits the call, waits for it, and
    returns the helper's return value. Outputs are staged and published
    atomically; inside a job the helper simply runs.
    """
    from . import qc
    if getattr(qc, function.__name__, None) is not function:
        raise ValueError(f'{function.__name__} is not a calmar.qc helper')
    return scheduled_operation(function)


def request_from_namespace(namespace, single=False):
    entries = namespace['SUBJECTS']
    if single:
        entries = [entries[namespace.get('TEST_SUBJECT_IDX',0)]]
    return {'dataset':str(namespace['RAW_DATASET_DIR']), 'config':namespace['CONFIG'],
            'entries':entries}


def _entry_request(request, entry):
    """Resolve mixed-cohort metadata into an ordinary one-entry request."""
    from .study import ENTRY_CONFIG, ENTRY_DATASET, config_for_entry, dataset_for_entry
    clean = {key: value for key, value in entry.items() if key not in (ENTRY_CONFIG, ENTRY_DATASET)}
    config = {key: value for key, value in config_for_entry(request['config'], entry).items()
              if key != 'ADDITIONAL_COHORTS'}
    return {**request, 'dataset': str(dataset_for_entry(request['dataset'], entry)),
            'config': config, 'entries': [clean]}


def _restore_request(result, request):
    """Keep route metadata in notebook results after jobs used clean entries."""
    result['request'] = {**(result.get('request') or {}), **request,
                         'entries': list(request.get('entries', ())) }
    return result


def _all_not_selected(stage, payloads):
    """Build accurate per-route skip results without invoking the scheduler."""
    from .study import stage_selected
    if not all(not stage_selected(stage, payload.get('config', {})) for payload in payloads):
        return None
    parts = [_not_selected(stage, payload) for payload in payloads]
    if len(parts) == 1:
        return parts[0]
    return StepResult({'stage': stage, 'job': '',
                       'request': {**payloads[0], 'entries': [e for p in payloads for e in p['entries']]},
                       'results': [row for part in parts for row in part['results']],
                       'qc_version': QC_VERSION, 'elapsed': 0})


def _result_stamps(result):
    """Watch inputs and published files without loading image arrays."""
    paths = set()
    request = result.get('request', {})
    for entry in request.get('entries', []):
        paths.add(Path(entry['t1w']))
        if entry.get('adc'):
            paths.add(Path(entry['adc']))
        if result.get('stage') in ('dmri_preproc', 'dmri_recon', 'dmri_metrics'):
            for key in ('dwi', 'bval', 'bvec', 'json', 'anatomical_t1w'):
                if entry.get(key):
                    paths.add(Path(entry[key]))
        if result.get('stage', '').startswith('brain_health_'):
            for key in ('flair', 'anatomical_t1w'):
                if entry.get(key):
                    paths.add(Path(entry[key]))
            try:
                from .study import Study
                source = request.get('config', {}).get('BRAIN_HEALTH_MASK_SOURCE', 'manual')
                selected = (Study(request.get('config', {}), request.get('dataset', '.'), '.')
                            .masks(entry).get(source, {}).get('T1w'))
                if selected is not None:
                    paths.add(Path(selected))
            except (KeyError, TypeError, ValueError):
                return None
        from .processing import manual_inputs
        mask, reference, _ = manual_inputs(request, entry)
        paths.update(p for p in (mask, reference) if p is not None)
    for entry in result.get('results', []):
        if (entry.get('qc') or {}).get('png'):
            paths.add(Path(entry['qc']['png']))
        for output in entry.get('outputs', []):
            if not output.get('path'): continue
            path = Path(output['path'])
            if path.is_dir():
                paths.update(path/name for name in output.get('images', {}))
                for marker in ('calmar-selection.json', 'calmar-reconstruction.json'):
                    if (path/marker).is_file():
                        paths.add(path/marker)
                selections = [path/'calmar-selection.json', path.parent/'qsiprep'/'calmar-selection.json']
                selection = next((candidate for candidate in selections if candidate.is_file()), None)
                if selection is not None:
                    try:
                        selected = json.loads(selection.read_text())
                        paths.update(Path(selected[key]) for key in ('anatomical_t1w', 'lesion_mask')
                                     if selected.get(key))
                    except (OSError, ValueError):
                        return None
            else:
                paths.add(path)
            provenance = Path(str(path) + '.prov.json')
            if provenance.is_file():
                paths.add(provenance)
            record = path/'calmar-cache.json' if path.is_dir() else Path(str(path)+'.cache.json')
            if record.is_file():
                paths.add(record)
                paths.update(Path(p['path']) for p in json.loads(record.read_text())['identity']['inputs'])
    if not paths or any(not p.is_file() for p in paths): return None
    return {str(p): [p.stat().st_mtime_ns, p.stat().st_size] for p in paths}


def _result_output_stamps(result):
    """Stamp only published outputs, allowing prior inputs to change safely."""
    paths = set()
    for entry in result.get('results', []):
        if (entry.get('qc') or {}).get('png'):
            paths.add(Path(entry['qc']['png']))
        for output in entry.get('outputs', []):
            if not output.get('path'):
                continue
            path = Path(output['path'])
            if path.is_dir():
                paths.update(path/name for name in output.get('images', {}))
                for marker in ('calmar-selection.json', 'calmar-reconstruction.json'):
                    if (path/marker).is_file():
                        paths.add(path/marker)
            else:
                paths.add(path)
            provenance = Path(str(path) + '.prov.json')
            if provenance.is_file():
                paths.add(provenance)
            record = path/'calmar-cache.json' if path.is_dir() else Path(str(path)+'.cache.json')
            if record.is_file():
                paths.add(record)
    if not paths or any(not path.is_file() for path in paths):
        return None
    return {str(path): [path.stat().st_mtime_ns, path.stat().st_size] for path in paths}


async def run_step(stage, namespace, *, single=False, timeout=43200):
    return await asyncio.to_thread(run_step_sync, stage, namespace, single=single, timeout=timeout)


def run_step_sync(stage, namespace, *, single=False, timeout=43200):
    """Notebook-namespace adapter kept for the guided runner and older cells."""
    project = Path(namespace['PROJECT_DIR'])
    if stage in ('qc_operation', 'reporting'):
        result = _run_payloads(stage, [namespace['_operation_request']], project, timeout)
    else:
        request = request_from_namespace(namespace, single)
        payloads = _split(stage, request)
        skipped = _all_not_selected(stage, payloads) if stage in PROCESSING_STAGES else None
        result = skipped if skipped is not None else _run_payloads(stage, payloads, project, timeout)
        _restore_request(result, request)
    namespace.setdefault('SCHEDULED_RESULTS', {})[stage] = result
    if stage in PROCESSING_STAGES:
        _record_timings(stage, result, namespace.setdefault('BATCH_TIMINGS', {}))
    return result


def submit_step(stage, entries, study, *, timings=None, timeout=43200):
    """Run one processing step for ``entries`` as Slurm jobs and wait for them.

    One job is submitted per participant (``src/analysis_NN_<stage>.sh``), so
    each has its own log, time limit and cache receipt. Participants whose
    inputs and published outputs are unchanged since their last successful job
    are not resubmitted. While waiting, one status line shows the jobs' state and the
    tool's current step (calmar.job_progress). ``timeout`` (seconds, default
    12 h) only stops the waiting; the jobs keep running. Returns a
    ``StepResult``; nothing runs in the kernel.
    """
    request = {'dataset': str(study.dataset), 'config': study.config, 'entries': list(entries)}
    payloads = _split(stage, request)
    skipped = _all_not_selected(stage, payloads)
    result = skipped if skipped is not None else _run_payloads(stage, payloads, Path(study.project), timeout)
    _restore_request(result, request)
    if timings is not None:
        _record_timings(stage, result, timings, show=False)  # show_step displays the times
    return result


def cached_step_results(stage, entries, study):
    """Inspect reusable receipts for ``entries`` without submitting work.

    The returned list follows the entry order and contains either the reusable
    saved result or ``None``. This is intentionally read-only so notebook
    decision panels can report prior analysis before the user opts in.
    """
    entries = list(entries)
    request = {'dataset': str(study.dataset), 'config': study.config, 'entries': entries}
    payloads = _split(stage, request)
    if len(payloads) != len(entries):
        raise ValueError(f"Cache inspection for {stage} did not resolve one payload per entry.")
    project = Path(study.project)
    results = []
    for payload in payloads:
        result = _cached(stage, payload, project)
        if result is not None and not _prior_matches_dependencies(stage, payload, project):
            result = None
        results.append(result)
    return results


def previous_step_results(stage, entries, study):
    """Inspect prior receipts whose published outputs still exist.

    Unlike :func:`cached_step_results`, this deliberately ignores changed input
    stamps.  It is only used after the notebook has labelled the result as
    prior and the user explicitly chooses to keep it.
    """
    entries = list(entries)
    request = {'dataset': str(study.dataset), 'config': study.config, 'entries': entries}
    payloads = _split(stage, request)
    if len(payloads) != len(entries):
        raise ValueError(f"Prior-result inspection for {stage} did not resolve one payload per entry.")
    return [_previous(stage, payload, Path(study.project)) for payload in payloads]


def usable_previous_step_results(stage, entries, study):
    """Inspect prior receipts the scheduler would honour for explicit reuse.

    This includes the same upstream-receipt check used immediately before job
    submission. Decision panels can therefore avoid offering a reuse action
    that would later be rejected because an upstream stage has advanced.
    """
    entries = list(entries)
    request = {'dataset': str(study.dataset), 'config': study.config, 'entries': entries}
    payloads = _split(stage, request)
    if len(payloads) != len(entries):
        raise ValueError(f"Usable-prior inspection for {stage} did not resolve one payload per entry.")
    project = Path(study.project)
    results = []
    for original in payloads:
        payload = dict(original)
        payload['config'] = dict(original.get('config', {}))
        key = _reuse_prior_key(stage)
        if key:
            payload['config'][key] = True
        prior = _previous(stage, payload, project)
        if prior is not None and not _prior_matches_dependencies(stage, payload, project):
            prior = None
        results.append(prior)
    return results


def _not_selected(stage, request):
    """A step the selected segmentation methods do not need: no job is submitted."""
    from .processing import not_selected_reason
    reason = not_selected_reason(stage, request['config'])
    print(f'{stage}: skipped, {reason}.', flush=True)
    return StepResult({'stage': stage, 'request': request, 'qc_version': QC_VERSION, 'elapsed': 0,
                       'results': [{'subject': e['subject'], 'session': e.get('session'), 'seconds': 0,
                                    'outputs': [{'status': 'skipped', 'reason': reason}]}
                                   for e in request['entries']]})


def _split(stage, request):
    """One payload per participant for processing stages with several entries."""
    if stage in PROCESSING_STAGES and request['entries']:
        return [_entry_request(request, entry) for entry in request['entries']]
    return [request]


def _stage_payload(stage, payload):
    """Payload fields that can affect ``stage`` or identify its running job.

    Cross-session DWI inventory belongs only to acquisition reporting. Keeping
    it out of every other stage avoids invalidating T1 processing caches or
    duplicating an already-running job when dataset metadata gains a DWI file.
    DWI sidecars are likewise inventory metadata until a processing stage
    explicitly adopts them.
    """
    payload = dict(payload)
    if stage != 'acquisition' and 'entries' in payload:
        ignored = {'dwi_inventory', 'dmri_analysis', 'brain_health_analysis',
                   'bval', 'bvec', 'json', 'flair',
                   'anatomical_t1w', 'brain_health_components'}
        if stage in ('dmri_preproc', 'dmri_recon', 'dmri_metrics'):
            ignored -= {'bval', 'bvec', 'json'}
        if stage.startswith('brain_health_'):
            ignored -= {'flair', 'anatomical_t1w', 'brain_health_components'}
        # The selected DWI session changes the downstream disconnectome mask,
        # but must not invalidate unrelated T1 processing caches.
        keep_dwi_link = (stage.startswith('brain_health_') and
                         payload.get('config', {}).get('BRAIN_HEALTH_MASK_SOURCE') == 'openads')
        if stage not in ('bcb', 'deepdisco') and not keep_dwi_link:
            ignored.add('dwi_analysis')
        payload['entries'] = [{k: v for k, v in entry.items() if k not in ignored}
                              for entry in payload['entries']]
    return payload


def _identity_key(stage, payload):
    # UI selections already resolve to explicit entries. Their presentation
    # settings and report destinations do not change image-processing results.
    identity = _stage_payload(stage, payload)
    if 'config' in identity:
        from .processing import ALGORITHM_VERSIONS
        presentation = {
            'PROJECT_DIR', 'REPORTS_SUBDIR', 'MASK_COLORS', 'TEST_SUBJECT_IDX', 'RUN_TEST',
            'NIIVUE_URL_BASE', 'VERBOSE', 'ANALYSE_DWI', '_DWI_ANALYSIS_SELECTED',
            'ANALYSE_TRACT_DWI', '_TRACT_DWI_SELECTED',
            'ANALYSE_BRAIN_HEALTH', '_BRAIN_HEALTH_SELECTED',
            'ADDITIONAL_COHORTS', 'OVERWRITE', 'DEEPDISCO_OVERWRITE', 'BCB_OVERWRITE',
            'DMRI_OVERWRITE', 'DMRI_REUSE_PRIOR',
            'OPENADS_OVERWRITE', 'OPENADS_REUSE_PRIOR',
            'BRAIN_HEALTH_OVERWRITE', 'BRAIN_HEALTH_REUSE_PRIOR'}
        config = identity['config']
        if stage.startswith('dmri_'):
            # Direct dMRI reads only its own method settings plus the derivative
            # locations needed to resolve the selected native-T1 lesion mask.
            relevant = {
                'MODALITY', 'SEGMENTATION_METHODS', 'MANUAL_MASK_PATH', 'MANUAL_MASK_ROOT',
                'MANUAL_MASK_SPACE', 'MANUAL_MASK_REF', 'DERIVATIVES_SUBDIR',
                'SYNTHSTROKE_SUBDIR', 'REGISTRATION_SUBDIR', 'OPENADS_SUBDIR',
            }
            identity['config'] = {k: v for k, v in config.items()
                                  if k not in presentation and (k.startswith('DMRI_') or k in relevant)}
        elif stage.startswith('brain_health_'):
            relevant = {
                'MODALITY', 'STROKE_PHASE', 'SEGMENTATION_METHODS', 'MANUAL_MASK_PATH',
                'MANUAL_MASK_ROOT', 'MANUAL_MASK_SPACE', 'MANUAL_MASK_REF',
                'DERIVATIVES_SUBDIR', 'SYNTHSTROKE_SUBDIR', 'OPENADS_SUBDIR',
                'REGISTRATION_SUBDIR',
            }
            stage_keys = {
                'brain_health_anatomy': {'BRAIN_HEALTH_SUBDIR', 'BRAIN_HEALTH_SYNTHSEG_MODE',
                                         'BRAIN_HEALTH_MASK_SOURCE'},
                'brain_health_wmh': {'BRAIN_HEALTH_SUBDIR'},
                'brain_health_metrics': {'BRAIN_HEALTH_SUBDIR', 'BRAIN_HEALTH_SYNTHSEG_MODE',
                                         'BRAIN_HEALTH_MASK_SOURCE', 'BRAIN_HEALTH_LESION_EXCLUSION_MM',
                                         'BRAIN_HEALTH_REGISTRATION_SEED'},
            }[stage]
            identity['config'] = {k: v for k, v in config.items()
                                  if k not in presentation and (k in stage_keys or k in relevant)}
        else:
            identity['config'] = {k: v for k, v in config.items()
                                  if k not in presentation and not k.startswith(('DMRI_', 'BRAIN_HEALTH_'))}
        identity['algorithms'] = ALGORITHM_VERSIONS
    return (stage, json.dumps(identity, default=str, sort_keys=True))


def _reusable(stage, payload):
    config = payload.get('config', {})
    route_key = ('OPENADS_OVERWRITE' if stage == 'openads' else
                 'DMRI_OVERWRITE' if stage.startswith('dmri_') else
                 'BRAIN_HEALTH_OVERWRITE' if stage.startswith('brain_health_') else None)
    overwrite = (config.get(route_key, config.get('OVERWRITE', False))
                 if route_key else config.get('OVERWRITE', False))
    overwrite = bool(overwrite or
                     (stage == 'deepdisco' and config.get('DEEPDISCO_OVERWRITE')) or
                     (stage == 'bcb' and config.get('BCB_OVERWRITE')))
    return stage not in ('qc_operation', 'reporting') and not overwrite


_MEMORY_CACHE = {}


def _receipt(stage, payload, project):
    key = _identity_key(stage, payload)
    disk_cache = project/'reports'/'step-cache'/(hashlib.sha256(str(key).encode()).hexdigest()+'.json')
    previous = _MEMORY_CACHE.get(key)
    if disk_cache.is_file():
        try:
            # Disk is authoritative because another notebook kernel may have
            # refreshed this receipt since our process populated memory.
            previous = json.loads(disk_cache.read_text())
            _MEMORY_CACHE[key] = previous
        except (OSError, ValueError):
            return None
    return previous


def _receipt_time(stage, payload, project, receipt):
    if receipt and receipt.get('stored_ns'):
        return int(receipt['stored_ns'])
    key = _identity_key(stage, payload)
    path = project/'reports'/'step-cache'/(hashlib.sha256(str(key).encode()).hexdigest()+'.json')
    try:
        return path.stat().st_mtime_ns
    except OSError:
        return 0


def _receipt_has_outputs(result):
    """Minimum safety check for an explicitly selected prior result."""
    found = False
    for row in result.get('results', []):
        qc = (row.get('qc') or {})
        if qc.get('complete') is False:
            return False
        if qc.get('png'):
            found = True
            if not Path(qc['png']).is_file():
                return False
        for output in row.get('outputs', []):
            if output.get('path'):
                found = True
                path = Path(output['path'])
                if not path.exists():
                    return False
                if path.is_dir() and any(not (path/name).is_file()
                                         for name in output.get('images', {})):
                    return False
    return found


def _previous(stage, payload, project):
    """Prior receipt with extant outputs, even when input stamps changed."""
    previous = _receipt(stage, payload, project)
    if not previous:
        return None
    result = previous.get('result') or {}
    if stage in PROCESSING_STAGES and stage != 'acquisition':
        if result.get('qc_version') != QC_VERSION or not _receipt_has_outputs(result):
            return None
        current_outputs = _result_output_stamps(result)
        if current_outputs is None:
            return None
        saved_outputs = previous.get('output_stamps')
        if saved_outputs is None:
            # Backward-compatible extraction from receipts written before
            # output stamps were stored separately.
            saved = previous.get('stamps') or {}
            saved_outputs = {path: saved.get(path) for path in current_outputs}
        if saved_outputs != current_outputs:
            return None
    return result


def _cached(stage, payload, project):
    """A previous receipt whose inputs and outputs are unchanged, else None."""
    if not _reusable(stage, payload):
        return None
    previous = _receipt(stage, payload, project)
    if not previous:
        return None
    if stage in PROCESSING_STAGES and stage != 'acquisition':
        if previous['result'].get('qc_version') != QC_VERSION:
            return None  # older receipt without saved QC evidence: refresh it
        if any((r.get('qc') or {}).get('complete') is False for r in previous['result'].get('results', [])):
            return None  # QC figure failed last time: retry
    if previous['stamps'] != _result_stamps(previous['result']):
        return None
    return previous['result']


def _reuse_prior_key(stage):
    return ('OPENADS_REUSE_PRIOR' if stage == 'openads' else
            'DMRI_REUSE_PRIOR' if stage.startswith('dmri_') else
            'BRAIN_HEALTH_REUSE_PRIOR' if stage.startswith('brain_health_') else None)


def _reuse_prior_requested(stage, payload):
    config = payload.get('config', {})
    key = _reuse_prior_key(stage)
    return bool(key and config.get(key))


def _stage_dependencies(stage, payload):
    if stage == 'dmri_recon':
        return ('dmri_preproc',)
    if stage == 'dmri_metrics':
        return ('dmri_preproc', 'dmri_recon')
    if stage == 'brain_health_metrics':
        components = payload.get('entries', [{}])[0].get('brain_health_components', ())
        return tuple(
            stage_name for component, stage_name in
            (('atrophy', 'brain_health_anatomy'), ('wmh', 'brain_health_wmh'))
            if component in components)
    return ()


def _receipt_token(stage, payload, project):
    receipt = _receipt(stage, payload, project)
    if not receipt:
        return None
    result = receipt.get('result') or {}
    token = {'job': result.get('job')}
    if receipt.get('stored_ns'):
        token['stored_ns'] = int(receipt['stored_ns'])
    if result.get('log_folder'):
        token['log_folder'] = result['log_folder']
    return token


def _upstream_receipts(stage, payload, project):
    receipts = {}
    for dependency in _stage_dependencies(stage, payload):
        token = _receipt_token(dependency, payload, project)
        if token is not None:
            receipts[dependency] = token
    return receipts


def _prior_matches_dependencies(stage, payload, project):
    """False when an upstream receipt advanced after this prior was made."""
    dependencies = _stage_dependencies(stage, payload)
    if not dependencies:
        return True
    receipt = _receipt(stage, payload, project)
    if not receipt:
        return False
    saved_result = receipt.get('result') or {}
    saved_receipts = saved_result.get('upstream_receipts') or {}
    saved_jobs = saved_result.get('upstream_jobs') or {}
    prior_time = _receipt_time(stage, payload, project, receipt)
    for dependency in dependencies:
        current = _cached(dependency, payload, project)
        if current is None and _reuse_prior_requested(stage, payload):
            current = _previous(dependency, payload, project)
        if current is None:
            return False  # no verified upstream result to tie this prior to
        current_token = _receipt_token(dependency, payload, project)
        saved_token = saved_receipts.get(dependency)
        if saved_token and current_token:
            if saved_token.get('stored_ns') and current_token.get('stored_ns'):
                if int(saved_token['stored_ns']) != int(current_token['stored_ns']):
                    return False
            elif saved_token.get('log_folder') and current_token.get('log_folder'):
                if saved_token['log_folder'] != current_token['log_folder']:
                    return False
            elif str(saved_token.get('job')) != str(current_token.get('job')):
                return False
            continue
        if dependency in saved_jobs:
            if str(saved_jobs[dependency]) != str(current.get('job')):
                return False
            continue
        dependency_receipt = _receipt(dependency, payload, project)
        if _receipt_time(dependency, payload, project, dependency_receipt) > prior_time:
            return False
    return True


def _prior_dependencies(stage, payload, project):
    """Prior stages that a newly computed downstream result depends on."""
    if not _reuse_prior_requested(stage, payload):
        return []
    dependencies = _stage_dependencies(stage, payload)
    markers = []
    for dependency in dependencies:
        current = _cached(dependency, payload, project)
        if current is not None:
            for row in current.get('results', []):
                markers.extend(row.get('derived_from_prior') or [])
            continue
        prior = _previous(dependency, payload, project)
        if prior is not None:
            markers.append({'stage': dependency, 'job': prior.get('job')})
    unique = []
    for marker in markers:
        if marker not in unique:
            unique.append(marker)
    return unique


def _store(stage, payload, project, result):
    # Overwrite means "do not read before running", not "discard the fresh
    # receipt". Saving the completed rerun makes it current after overwrite is
    # turned off. QC/report operations remain intentionally non-cacheable.
    if stage in ('qc_operation', 'reporting'):
        return
    stamps = _result_stamps(result)
    output_stamps = _result_output_stamps(result)
    if not stamps or not output_stamps:
        return
    key = _identity_key(stage, payload)
    cached = {'stamps': stamps, 'output_stamps': output_stamps,
              'result': result, 'stored_ns': time.time_ns()}
    _MEMORY_CACHE[key] = cached
    disk_cache = project/'reports'/'step-cache'/(hashlib.sha256(str(key).encode()).hexdigest()+'.json')
    disk_cache.parent.mkdir(parents=True, exist_ok=True)
    temp_cache = disk_cache.with_suffix(f'.{uuid4().hex}.tmp')
    temp_cache.write_text(json.dumps(cached, default=str))
    temp_cache.replace(disk_cache)


def _resources(stage, payload):
    """sbatch options that override a script's #SBATCH defaults: LINDA's CPU
    count follows CONFIG["LINDA_THREADS"] (1 = bit-reproducible, the default)."""
    if stage == 'linda':
        from .processing import linda_threads
        return [f'--cpus-per-task={linda_threads(payload.get("config", {}))}']
    if stage == 'registration':
        from .processing import registration_threads
        return [f'--cpus-per-task={registration_threads(payload.get("config", {}))}']
    return []


def _job_label(stage, payload):
    return '_'.join(filter(None, [stage] + [e.get('subject') for e in payload.get('entries', [])][:1]))


def _attach_running(stage, payload, project, upstream_receipts=None):
    """A queued or running job that was submitted for exactly this payload (for
    example before the notebook lost its connection), so a rerun of the cell
    waits for it instead of submitting a duplicate. None if there is none."""
    try:
        queue = subprocess.run(['squeue', '-h', '-u', os.environ.get('USER', ''), '-o', '%i',
                                f'--name=calmar_{_job_label(stage, payload)}'],
                               capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    running = set(queue.stdout.split())
    if not running:
        return None
    wanted = json.loads(json.dumps(_stage_payload(stage, payload), default=str))
    for submission in (project/'reports'/'jobs').glob('*/submission.json'):
        try:
            info = json.loads(submission.read_text())
            previous = _stage_payload(stage, json.loads((submission.parent/'request.json').read_text()))
            if info.get('job_id') in running and info.get('stage') == stage and previous == wanted:
                expected = upstream_receipts or {}
                if 'upstream_receipts' not in info and expected:
                    raise RuntimeError(
                        f"{stage}: active Slurm job {info['job_id']} predates dependency provenance; "
                        "wait for it to finish, then rerun this cell.")
                if (info.get('upstream_receipts') or {}) != expected:
                    raise RuntimeError(
                        f"{stage}: active Slurm job {info['job_id']} was submitted for older upstream "
                        "results; wait for it to finish, then rerun this cell.")
                folder = submission.parent
                print(f"{stage}: Slurm job {info['job_id']} is already running this request; waiting for it.",
                      flush=True)
                return {'job': info['job_id'], 'folder': folder, 'output': folder/'result',
                        'payload': payload,
                        'upstream_receipts': info.get('upstream_receipts') or {}}
        except (OSError, ValueError):
            continue
    return None


def _submit(stage, payload, project, upstream_receipts=None):
    folder = project/'reports'/'jobs'/uuid4().hex
    folder.mkdir(parents=True)
    (project/'logs').mkdir(exist_ok=True)
    request = folder/'request.json'
    request.write_text(json.dumps(payload,default=str,indent=2))
    output = folder/'result'
    # Job IDs can be reused after a server restart. Per-attempt paths avoid
    # overwriting historical logs or mistaking an old log for a launched job.
    label = _job_label(stage, payload)
    command = ['sbatch','--parsable', '--export=ALL', f'--job-name=calmar_{label}',
               '--output',str(folder/'stdout.log'), '--error',str(folder/'stderr.log'),
               *_resources(stage, payload), str(project/'src'/SCRIPTS[stage]),str(request),str(output)]
    # Notebook module loads can put a container's Python wrapper ahead of the
    # kernel interpreter. That wrapper strips SLURM_* via --cleanenv.
    submitted = subprocess.run(command,cwd=project,text=True,capture_output=True,check=True,
                               env={**os.environ, 'CALMAR_PYTHON': sys.executable})
    job = submitted.stdout.strip().split(';')[0]
    if not job.isdigit(): raise RuntimeError(f'Invalid Slurm job ID: {submitted.stdout}')
    info = {'job_id': job, 'command': command, 'stage': stage,
            'upstream_receipts': upstream_receipts or {}}
    (folder/'submission.json').write_text(json.dumps(info, indent=2))
    return {'job': job, 'folder': folder, 'output': output, 'payload': payload,
            'upstream_receipts': upstream_receipts or {}}


def _poll(stage, job, progress=None):
    """True when finished successfully, False while pending; raises on failure.
    ``progress`` (calmar.job_progress.JobProgress) is told each job's state."""
    accounting = subprocess.run(['sacct','-j',job['job'],'--noheader','-P','--format=JobIDRaw,State,ExitCode'],capture_output=True,text=True,check=True)
    rows = [line.split('|') for line in accounting.stdout.splitlines() if line.split('|')[0] == job['job']]
    folder, number = job['folder'], job['job']
    if rows:
        state,code = rows[-1][1:3]
        if progress is not None:
            progress.update(job, state.split()[0] if state else 'PENDING')
        if state == 'COMPLETED':
            inspect_logs(folder)
            output = job['output']
            if code != '0:0' or not (output/'summary.json').is_file() or not Path(str(output)+'.prov.json').is_file():
                raise RuntimeError(f'Job {number}: incomplete publication or nonzero exit ({code})')
            result = json.loads((output/'summary.json').read_text())
            provenance = json.loads(Path(str(output)+'.prov.json').read_text())
            if (str(result.get('job')) != number or result.get('stage') != stage
                    or str(provenance.get('slurm_job_id')) != number
                    or provenance.get('output_id') != stage):
                raise RuntimeError(f'Job {number}: publication belongs to a different job or stage; inspect {folder}')
            result['log_folder'] = str(folder)
            job['result'] = result
            return True
        if state.startswith(('FAILED','CANCELLED','TIMEOUT','OUT_OF_MEMORY','NODE_FAIL','PREEMPTED','BOOT_FAIL','DEADLINE','REVOKED')):
            if (folder/'stdout.log').is_file() and (folder/'stderr.log').is_file():
                inspect_logs(folder)
            raise RuntimeError(f'Job {number}: {state} ({code}); inspect {folder}')
        if state == 'RUNNING' and time.monotonic()-job['started'] > 60 and not (folder/'stdout.log').exists():
            raise RuntimeError(f'Job {number} is marked running but has no batch log. Check slurmd health; job ID retained in {folder}. It has not been cancelled; use scancel {number} before retrying.')
    queue = subprocess.run(['squeue','-j',number,'-h','-o','%T|%R'],capture_output=True,text=True,check=True)
    if progress is not None and not rows:
        progress.update(job, queue.stdout.split('|')[0].strip() or 'PENDING')
    if any(reason in queue.stdout for reason in ['PartitionConfig','PartitionNodeLimit','PartitionTimeLimit','DependencyNeverSatisfied']):
        raise RuntimeError(f'Job {number} needs scheduler intervention: {queue.stdout.strip()}')
    return False


def _run_payloads(stage, payloads, project, timeout):
    """Submit uncached payloads, wait for all, and merge their results."""
    started = time.monotonic()
    parts, pending = [None]*len(payloads), []
    for i, payload in enumerate(payloads):
        if stage in PROCESSING_STAGES:
            from .study import stage_selected
            if not stage_selected(stage, payload.get('config', {})):
                parts[i] = _not_selected(stage, payload)
                continue
        current = _cached(stage, payload, project)
        if current is not None and not _prior_matches_dependencies(stage, payload, project):
            current = None
        explicit_prior = (_previous(stage, payload, project)
                          if (current is None and _reuse_prior_requested(stage, payload)
                              and _prior_matches_dependencies(stage, payload, project)) else None)
        cached = current or explicit_prior
        if cached is not None:
            # Mark the reuse on each participant: their output statuses describe
            # the original job, not this run.
            marker = ({'prior_result_from_job': cached.get('job')} if explicit_prior is not None else
                      {'reused_from_job': cached.get('job')})
            parts[i] = {**cached, 'reused': True, 'explicit_prior': explicit_prior is not None,
                        'results': [{**r, **marker} for r in cached.get('results', [])]}
        else:
            upstream_receipts = _upstream_receipts(stage, payload, project)
            try:
                job = (_attach_running(stage, payload, project, upstream_receipts) or
                       _submit(stage, payload, project, upstream_receipts))
            except RuntimeError as error:
                active = ' '.join(item['job'] for item in pending)
                suffix = (f" Already submitted job(s) still active: {active}."
                          if active else "")
                raise RuntimeError(str(error) + suffix) from error
            job['index'], job['started'] = i, time.monotonic()
            pending.append(job)
    reused = sum(1 for p in parts if p is not None and p.get('reused'))
    if reused:
        prior = sum(1 for p in parts if p is not None and p.get('explicit_prior'))
        unchanged = reused - prior
        messages = []
        if unchanged:
            messages.append(f'using unchanged results for {unchanged} participant(s)')
        if prior:
            messages.append(f'using explicitly selected prior results for {prior} participant(s)')
        print(f'{stage}: ' + '; '.join(messages) + '.', flush=True)
    failures = []
    progress = JobProgress(stage, list(pending)) if pending else None
    while pending and time.monotonic()-started < timeout:
        for job in list(pending):
            try:
                done = _poll(stage, job, progress)
            except RuntimeError as error:
                progress.update(job, 'FAILED', str(error).split(';')[0])
                failures.append(str(error)); pending.remove(job); continue
            if done:
                pending.remove(job)
                dependencies = _prior_dependencies(stage, job['payload'], project)
                if dependencies:
                    job['result']['results'] = [
                        {**row, 'derived_from_prior': dependencies}
                        for row in job['result'].get('results', [])]
                upstream = job.get('upstream_receipts') or {}
                if upstream:
                    job['result']['upstream_receipts'] = upstream
                    job['result']['upstream_jobs'] = {
                        dependency: token.get('job')
                        for dependency, token in upstream.items()}
                parts[job['index']] = job['result']
                _store(stage, job['payload'], project, job['result'])
        if progress is not None and pending:
            progress.refresh()
        if pending:
            time.sleep(10)
    if progress is not None and not pending:
        progress.finish(failed=len(failures))
    if pending:
        ids = ' '.join(j['job'] for j in pending)
        raise TimeoutError(f'Job(s) {ids} still outstanding; recover with squeue -j and sacct -j. '
                           f'They have not been cancelled; use scancel before retrying.')
    if failures:
        raise RuntimeError(f'{stage}: {len(failures)} job(s) failed:\n' + '\n'.join(failures))
    for part in parts:
        for entry in part.get('results', []):
            if part.get('log_folder'):
                entry.setdefault('log_folder', part['log_folder'])
    if len(parts) == 1:
        merged = parts[0]
    else:
        merged = {'stage': stage, 'job': ','.join(str(p['job']) for p in parts if p.get('job')),
                  'request': {**payloads[0], 'entries': [e for p in payloads for e in p['entries']]},
                  'results': [r for p in parts for r in p['results']], 'qc_version': QC_VERSION}
    merged = StepResult(merged)
    merged['elapsed'] = time.monotonic()-started
    return merged


def _record_timings(stage, result, timings, show=True):
    from .timing import batch_html
    from IPython.display import HTML, display
    records = {}
    for entry in result.get('results', []):
        key = (entry['subject'],entry.get('session') or '',stage,'')
        status = ', '.join(sorted({p.get('status','Validated') for p in entry.get('outputs', [])})) or 'no outputs'
        records[key] = dict(subject=entry['subject'],session=entry.get('session') or '',stage=stage,
            detail='',seconds=entry.get('seconds', 0.),status=status)
    record = dict(participants=records,seconds=result.get('elapsed', 0.))
    timings[stage] = record
    if show:
        display(HTML(batch_html(stage,record)))
