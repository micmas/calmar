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
            (26,'manual'),(27,'bcb'),(28,'deepdisco')]}
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


PROCESSING_STAGES = ('acquisition', 'brain', 'linda', 'synthstroke', 'manual', 'bcb', 'deepdisco')
# Bump when saved QC evidence changes, so older receipts without it are refreshed.
QC_VERSION = 6


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


def _result_stamps(result):
    """Watch inputs and published files without loading image arrays."""
    paths = set()
    request = result.get('request', {})
    for entry in request.get('entries', []):
        paths.add(Path(entry['t1w']))
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
            else:
                paths.add(path)
            record = path/'calmar-cache.json' if path.is_dir() else Path(str(path)+'.cache.json')
            if record.is_file():
                paths.add(record)
                paths.update(Path(p['path']) for p in json.loads(record.read_text())['identity']['inputs'])
    if not paths or any(not p.is_file() for p in paths): return None
    return {str(p): [p.stat().st_mtime_ns, p.stat().st_size] for p in paths}


async def run_step(stage, namespace, *, single=False, timeout=43200):
    return await asyncio.to_thread(run_step_sync, stage, namespace, single=single, timeout=timeout)


def run_step_sync(stage, namespace, *, single=False, timeout=43200):
    """Notebook-namespace adapter kept for the guided runner and older cells."""
    project = Path(namespace['PROJECT_DIR'])
    if stage in ('qc_operation', 'reporting'):
        result = _run_payloads(stage, [namespace['_operation_request']], project, timeout)
    else:
        request = request_from_namespace(namespace, single)
        result = _run_payloads(stage, _split(stage, request), project, timeout)
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
    result = _run_payloads(stage, _split(stage, request), Path(study.project), timeout)
    if timings is not None:
        _record_timings(stage, result, timings, show=False)  # show_step displays the times
    return result


def _split(stage, request):
    """One payload per participant for processing stages with several entries."""
    if stage in PROCESSING_STAGES and len(request['entries']) > 1:
        return [{**request, 'entries': [entry]} for entry in request['entries']]
    return [request]


def _identity_key(stage, payload):
    # UI selections already resolve to explicit entries. Their presentation
    # settings and report destinations do not change image-processing results.
    identity = dict(payload)
    if 'config' in identity:
        from .processing import ALGORITHM_VERSIONS
        identity['config'] = {k:v for k,v in identity['config'].items() if k not in (
            'PROJECT_DIR', 'REPORTS_SUBDIR', 'MASK_COLORS', 'TEST_SUBJECT_IDX', 'RUN_TEST',
            'NIIVUE_URL_BASE', 'VERBOSE')}
        identity['algorithms'] = ALGORITHM_VERSIONS
    return (stage, json.dumps(identity, default=str, sort_keys=True))


def _reusable(stage, payload):
    config = payload.get('config', {})
    return stage not in ('qc_operation', 'reporting') and not (
        config.get('OVERWRITE') or config.get('DEEPDISCO_OVERWRITE') or config.get('BCB_OVERWRITE'))


_MEMORY_CACHE = {}


def _cached(stage, payload, project):
    """A previous receipt whose inputs and outputs are unchanged, else None."""
    if not _reusable(stage, payload):
        return None
    key = _identity_key(stage, payload)
    disk_cache = project/'reports'/'step-cache'/(hashlib.sha256(str(key).encode()).hexdigest()+'.json')
    previous = _MEMORY_CACHE.get(key)
    if previous is None and disk_cache.is_file():
        try: previous = json.loads(disk_cache.read_text())
        except (OSError, ValueError): pass
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


def _store(stage, payload, project, result):
    if not _reusable(stage, payload):
        return
    stamps = _result_stamps(result)
    if not stamps:
        return
    key = _identity_key(stage, payload)
    cached = {'stamps': stamps, 'result': result}
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
    return []


def _job_label(stage, payload):
    return '_'.join(filter(None, [stage] + [e.get('subject') for e in payload.get('entries', [])][:1]))


def _attach_running(stage, payload, project):
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
    wanted = json.loads(json.dumps(payload, default=str))
    for submission in (project/'reports'/'jobs').glob('*/submission.json'):
        try:
            info = json.loads(submission.read_text())
            if info.get('job_id') in running and info.get('stage') == stage and \
                    json.loads((submission.parent/'request.json').read_text()) == wanted:
                folder = submission.parent
                print(f"{stage}: Slurm job {info['job_id']} is already running this request; waiting for it.",
                      flush=True)
                return {'job': info['job_id'], 'folder': folder, 'output': folder/'result', 'payload': payload}
        except (OSError, ValueError):
            continue
    return None


def _submit(stage, payload, project):
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
    (folder/'submission.json').write_text(json.dumps({'job_id':job,'command':command,'stage':stage},indent=2))
    return {'job': job, 'folder': folder, 'output': output, 'payload': payload}


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
        cached = _cached(stage, payload, project)
        if cached is not None:
            # Mark the reuse on each participant: their output statuses describe
            # the original job, not this run.
            parts[i] = {**cached, 'reused': True,
                        'results': [{**r, 'reused_from_job': cached.get('job')} for r in cached.get('results', [])]}
        else:
            job = _attach_running(stage, payload, project) or _submit(stage, payload, project)
            job['index'], job['started'] = i, time.monotonic()
            pending.append(job)
    reused = sum(1 for p in parts if p is not None)
    if reused:
        print(f'{stage}: using unchanged results for {reused} participant(s).' if len(payloads) > 1
              else f'{stage}: using unchanged results.', flush=True)
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
        merged = {'stage': stage, 'job': ','.join(str(p.get('job')) for p in parts),
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
