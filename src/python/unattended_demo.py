"""Execute a separate, autosaved demo notebook; never edit the source notebook.

Run via src/analysis_58_unattended_demo.sh. Restart the same command after a
failure: existing CALMaR receipts reuse completed jobs and attach running jobs.
Human review is explicitly skipped, not fabricated. Imaging errors still fail.
"""
from __future__ import annotations

import argparse
import asyncio
from contextlib import suppress
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import traceback
from uuid import uuid4

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter


SUBJECTS = ["sub-M2001", "sub-M2004", "sub-strokecase0001", "sub-strokecase0002"]


def atomic_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, prefix=".demo-",
                                     encoding="utf-8", delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f"Source notebook changed; expected one occurrence of {old!r}")
    return text.replace(old, new, 1)


def build_notebook(source, optional, report_subdir):
    nb = nbformat.read(source, as_version=4)
    cells = {c.id: c for c in nb.cells}
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    nb.metadata.pop("widgets", None)
    nb.metadata.kernelspec = {"name": "python3", "display_name": "Python 3", "language": "python"}
    overrides = {
        "SUBJECT_FILTER": SUBJECTS[:2], "SESSION_FILTER": ["ses-1076", "ses-524"],
        "MAX_SUBJECTS": 2, "RANDOM_SAMPLE": False, "RUN_TEST": True, "TEST_SUBJECT_IDX": 0,
        "ANALYSE_DWI": optional == "all", "ANALYSE_TRACT_DWI": optional == "all",
        "ANALYSE_BRAIN_HEALTH": optional == "all", "REPORTS_SUBDIR": report_subdir,
        "OVERWRITE": False, "BCB_OVERWRITE": False, "DEEPDISCO_OVERWRITE": False,
        "DMRI_OVERWRITE": False, "BRAIN_HEALTH_OVERWRITE": False,
        "DMRI_REUSE_PRIOR": True, "BRAIN_HEALTH_REUSE_PRIOR": True,
        "ADDITIONAL_COHORTS": [{"NAME": "ISLES 2022 acute", "DATASET_SOURCE": "isles2022",
            "LOCAL_DATASET": "data/ISLES-2022", "MODALITY": "dwi", "STROKE_PHASE": "acute",
            "SEGMENTATION_METHODS": ["openads"], "SUBJECT_FILTER": SUBJECTS[2:],
            "SESSION_FILTER": ["ses-0001"], "MAX_SUBJECTS": 2}],
    }
    nb.cells.insert(0, nbformat.v4.new_markdown_cell(
        "# Unattended four-participant demo\n\n"
        "One chronic participant runs through the single-case workflow; the remaining "
        "chronic participant and two acute participants run in the batch. Completed "
        "single-case results are reused in cohort summaries. All available optional "
        "analyses are selected when `optional=all`.\n\n"
        "**Human QC is skipped for this demonstration. No passing ratings are invented.** "
        "Static QC images, tables and four participant reports are saved. "
        "Repair/edit controls are displayed but no automatic edits are made. "
        "The source notebook is unchanged. The runner autosaves throughout execution.",
        id="demo-notice"))
    nb.cells.insert(1, nbformat.v4.new_code_cell(
        "import os\nos.environ['CALMAR_KB_UPDATE'] = 'off'\n"
        f"_CALMAR_CONFIG_OVERRIDES = {overrides!r}\n"
        "print('Demo settings:', _CALMAR_CONFIG_OVERRIDES)\n", id="demo-policy"))
    # Embed each job's static QC, even when there is no widget frontend.
    cells["calmar-step-08"].source += '''
import calmar.step_summary as _demo_summary
_demo_show_step_original = _demo_summary.show_step
def _demo_show_step(*args, **kwargs):
    kwargs['images'] = True
    return _demo_show_step_original(*args, **kwargs)
_demo_summary.show_step = _demo_show_step
show_step = _demo_show_step
import calmar.scheduled as _demo_scheduled
_demo_submit_original = _demo_scheduled.submit_step
def _demo_submit(*args, **kwargs):
    kwargs.setdefault('timeout', 48 * 3600)
    return _demo_submit_original(*args, **kwargs)
_demo_scheduled.submit_step = _demo_submit
submit_step = _demo_submit
'''
    cells["calmar-acquire"].source += f"\nassert [e['subject'] for e in SUBJECTS] == {SUBJECTS!r}\n"
    cells["calmar-test-participant"].source = '''
from calmar.single_subject import show_single_subject_inputs
_single_subject_inputs = show_single_subject_inputs(globals())
_single_subject_inputs.subject.value = 0
assert _single_subject_inputs.approve(), _single_subject_inputs.message.value
print('Demo: single-case workflow approved for', SUBJECTS[TEST_SUBJECT_IDX]['subject'])
'''
    cells["calmar-step-39"].source = replace_once(cells["calmar-step-39"].source,
        'raise StopExecution("Choose Continue to batch or Jump to reporting.")',
        '_batch_checkpoint._resume()\n    assert not _batch_checkpoint.paused\n    print("Demo: continuing to the batch; completed test steps are reused.")')
    cells["calmar-step-51"].source = replace_once(cells["calmar-step-51"].source,
        'raise StopExecution("Use existing QC, review/redo QC, or choose Skip QC. Use the buttons above to continue.")',
        'assert get_ipython()._calmar_qc_checkpoint.choose("skipped")\n'
        'print("DEMO: human QC skipped by request; no ratings or repair decisions fabricated.")')
    cells["calmar-optional-dwi"].source = replace_once(cells["calmar-optional-dwi"].source,
        'raise StopExecution("Review or explicitly skip the optional DWI QC, then continue.")',
        'assert get_ipython()._calmar_qc_checkpoint.choose("skipped")\n'
        '    print("DEMO: optional DWI human QC skipped by request.")')
    # Fill any absent report globals from ReportSettings without overriding
    # values supplied by this version of the source notebook or its form.
    cells["calmar-step-77"].source += '''
from dataclasses import fields
from calmar.participant_report import ReportSettings
_demo_report_defaults = ReportSettings()
for _field in fields(_demo_report_defaults):
    globals().setdefault('INTERP_' + _field.name.upper(), getattr(_demo_report_defaults, _field.name))
'''
    cells["calmar-step-79"].source = replace_once(cells["calmar-step-79"].source,
        'raise StopExecution("Choose report inputs and click Generate participant report.")',
        '_report_inputs.choose_participant(SUBJECTS[INTERP_SUBJECT_IDX]["subject"])\n'
        '_report_inputs.choose_mask("openads" if config_for_entry(CONFIG, SUBJECTS[INTERP_SUBJECT_IDX])["MODALITY"] == "dwi" else "synthstroke")\n'
        'assert _report_inputs.approve(), _report_inputs.message.value\n'
        'print("Demo: report form approved using its displayed defaults.")')
    cells["calmar-step-81"].source += '''
DEMO_REPORTS = globals().setdefault('DEMO_REPORTS', [])
DEMO_REPORTS.append(str(PARTICIPANT_REPORT.path))
display(HTML(PARTICIPANT_REPORT.path.read_text()))
print('Saved participant report:', PARTICIPANT_REPORT.path)
'''
    # Materialize the PDF exports normally requested with a button.
    cells["calmar-step-75"].source += '''
from calmar.atlas_pdf import write_atlas_pdf
from calmar.qc_decisions import report_qc_text
DEMO_ATLAS_PDFS = []
for _table_key, _table in OVERLAP_DFS.items():
    _atlas, _source = _table_key.rsplit('_', 1)
    for _entry in SUBJECTS:
        _pdf = write_atlas_pdf(_entry['subject'], _entry.get('session'), _table,
            _atlas, _source, pdf_dir=ATLAS_PDF_DIR, atlas_dir=ATLAS_DIR,
            qc_text=report_qc_text(study.qc_dir(_entry), _entry))
        if _pdf is not None:
            DEMO_ATLAS_PDFS.append(str(_pdf))
print('Saved atlas PDFs:', len(DEMO_ATLAS_PDFS))
'''
    extra = []
    for index in range(1, 4):
        extra.append(nbformat.v4.new_markdown_cell(
            f"### Demo report: {SUBJECTS[index]}", id=f"demo-report-heading-{index}"))
        extra.append(nbformat.v4.new_code_cell(
            f"INTERP_SUBJECT_IDX = {index}\n" + cells["calmar-step-79"].source,
            id=f"demo-report-inputs-{index}"))
        extra.append(nbformat.v4.new_code_cell(cells["calmar-step-81"].source,
            id=f"demo-report-result-{index}"))
    at = nb.cells.index(cells["calmar-step-87"])
    nb.cells[at:at] = extra
    nb.cells.append(nbformat.v4.new_code_cell('''
_demo_errors = {k: globals()[k] for k in ('DWI_ERROR', 'DMRI_ERROR', 'BRAIN_HEALTH_ERROR') if globals().get(k)}
print('Optional analysis errors (must be resolved before declaring success):', _demo_errors)
assert not _demo_errors, _demo_errors
assert len(DEMO_REPORTS) == 4 and all(Path(p).is_file() for p in DEMO_REPORTS)
assert len(set(DEMO_REPORTS)) == 4
_demo_proof = {'token': DEMO_COMPLETION_TOKEN, 'reports': DEMO_REPORTS,
               'atlas_pdfs': DEMO_ATLAS_PDFS, 'participants': [e['subject'] for e in SUBJECTS],
               'human_qc': 'skipped'}
_demo_proof_path = Path(DEMO_COMPLETION_PROOF)
_demo_proof_temporary = _demo_proof_path.with_suffix('.tmp')
_demo_proof_temporary.write_text(json.dumps(_demo_proof, indent=2))
_demo_proof_temporary.replace(_demo_proof_path)
print('Four reports and all selected processing cells completed. Human QC remains skipped.')
''', id="demo-completion-check"))
    nbformat.validate(nb)
    return nb


async def execute(args, project, destination):
    started_ns = time.time_ns()
    source = project / args.source
    nb = build_notebook(source, args.optional, args.reports)
    attempt = destination / "attempts" / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                                         + "-" + os.environ.get("SLURM_JOB_ID", "build"))
    attempt.mkdir(parents=True)
    shutil.copy2(source, attempt / "source.ipynb")
    shutil.copy2(Path(__file__), attempt / "unattended_demo.py")
    output = destination / "progress.ipynb"
    token = uuid4().hex
    proof = attempt / "completion-proof.json"
    nb.cells[1].source += f"\nDEMO_COMPLETION_TOKEN = {token!r}\nDEMO_COMPLETION_PROOF = {str(proof)!r}\n"
    status = {"state": "prepared", "job_id": os.environ.get("SLURM_JOB_ID"),
              "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "optional": args.optional, "participants": SUBJECTS, "attempt": str(attempt),
              "notebook": str(attempt / "executed.ipynb"), "progress_notebook": str(output),
              "python": sys.version, "human_qc": "skipped"}
    client = NotebookClient(nb, timeout=None, iopub_timeout=180, raise_on_iopub_timeout=True,
                            kernel_name="python3", allow_errors=False, store_widget_state=True,
                            resources={"metadata": {"path": str(project)}})

    def save():
        client.set_widgets_metadata()
        status["saved_at"] = datetime.now(timezone.utc).isoformat()
        text = nbformat.writes(nb)
        atomic_text(attempt / "executed.ipynb", text)
        if not args.build_only:
            atomic_text(output, text)
        atomic_text(destination / "status.json", json.dumps(status, indent=2) + "\n")
        atomic_text(attempt / "status.json", json.dumps(status, indent=2) + "\n")

    save()
    if args.build_only:
        print(attempt / "executed.ipynb")
        return
    if "SLURM_JOB_ID" not in os.environ:
        raise RuntimeError("Execute via sbatch src/analysis_58_unattended_demo.sh")

    loop = asyncio.get_running_loop()
    controller = asyncio.current_task()

    def on_signal(signum):
        status['signal'] = signum
        controller.cancel()

    for signum in (signal.SIGTERM, signal.SIGUSR1):
        loop.add_signal_handler(signum, on_signal, signum)

    async def autosave():
        while True:
            await asyncio.sleep(60)
            save()

    periodic = asyncio.create_task(autosave())

    def autosave_finished(task):
        if not task.cancelled() and task.exception() is not None:
            status['autosave_error'] = str(task.exception())
            controller.cancel()

    periodic.add_done_callback(autosave_finished)
    try:
        # A notebook controller is not an imaging worker. Remove inherited Slurm
        # markers so in_slurm helpers submit jobs, and do not leak controller
        # thread limits into the imaging jobs' environments.
        kernel_env = {k: v for k, v in os.environ.items()
                      if not k.startswith(('SLURM_', 'SBATCH_', 'APPTAINERENV_', 'SINGULARITYENV_'))
                      and k not in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
                                    'ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS')}
        async with client.async_setup_kernel(cwd=str(project), env=kernel_env):
            for index, cell in enumerate(nb.cells):
                if cell.cell_type != "code":
                    continue
                status.update(state="running", cell_index=index, cell_id=cell.id)
                print(f"START {index}: {cell.id}", flush=True)
                save()
                await client.async_execute_cell(cell, index)
                status["last_completed_cell"] = cell.id
                save()
                print(f"DONE  {index}: {cell.id}", flush=True)
        evidence = json.loads(proof.read_text())
        if (evidence.get('token') != token or evidence.get('participants') != SUBJECTS
                or len(set(evidence.get('reports', []))) != 4
                or not evidence.get('atlas_pdfs')
                or not all(Path(p).is_file() and Path(p).stat().st_mtime_ns >= started_ns
                           for p in evidence['reports'] + evidence['atlas_pdfs'])):
            raise RuntimeError('Independent completion proof is missing or invalid.')
        status['reports'] = evidence['reports']
        status['atlas_pdfs'] = evidence['atlas_pdfs']
        html, _ = HTMLExporter().from_notebook_node(nb)
        final_html = attempt / "lesion-interpretation-demo.html"
        atomic_text(final_html, html)
        status['html'] = str(final_html)
        status.update(state="completed", completed_at=datetime.now(timezone.utc).isoformat())
        save()
        completion = (project / args.completion).resolve()
        completion.parent.mkdir(parents=True, exist_ok=True)
        staged = completion.with_name(completion.name + ".attempt." + os.environ["SLURM_JOB_ID"])
        atomic_text(staged, json.dumps(status, indent=2) + "\n")
        subprocess.run(["neurodesk-astra-provenance", "publish", str(staged), str(completion),
                        "--output-id", "demo_run", "--tool", sys.executable,
                        "--script", os.environ.get("CALMAR_DEMO_SCRIPT", str(Path(__file__).resolve())),
                        "--replace"], check=True)
        shutil.copy2(completion, attempt / 'completion.json')
        shutil.copy2(Path(str(completion) + '.prov.json'), attempt / 'completion.json.prov.json')
    except BaseException as error:
        was_interrupted = status.get('signal') is not None or isinstance(error, KeyboardInterrupt)
        detail = (f"Controller received signal {status['signal']}; child jobs may still be running."
                  if status.get('signal') is not None else status.get('autosave_error', str(error)))
        status.update(state="interrupted" if was_interrupted else "failed",
                      error=detail, traceback=traceback.format_exc())
        save()
        raise
    finally:
        periodic.cancel()
        with suppress(BaseException):
            await periodic
        for signum in (signal.SIGTERM, signal.SIGUSR1):
            loop.remove_signal_handler(signum)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="lesion-interpretation-pipeline.ipynb")
    parser.add_argument("--output-dir", default="analyses/unattended-demo/run")
    parser.add_argument("--reports", default="reports/unattended-demo")
    parser.add_argument("--completion", default="analyses/unattended-demo/run/completion.json")
    parser.add_argument("--optional", choices=("all", "main"), default="all")
    parser.add_argument("--build-only", action="store_true")
    args = parser.parse_args()
    project = Path.cwd().resolve()
    destination = (project / args.output_dir).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / ".runner.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        asyncio.run(execute(args, project, destination))


if __name__ == "__main__":
    main()
