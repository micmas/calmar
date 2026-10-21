"""Run real notebook cells in an owned kernel against existing local products.

Unlike widget fixtures, this includes real Slurm submission from a notebook
whose PATH has been modified by Neurodesk modules. No inference is allowed.
"""
import argparse
import json
from pathlib import Path
import time
import sys

from jupyter_client import KernelManager
import nbformat

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--artifacts', type=Path, required=True)
    parser.add_argument('--guided', action='store_true')
    args = parser.parse_args()
    args.artifacts = args.artifacts.resolve(); args.artifacts.mkdir(parents=True, exist_ok=True)
    manager = KernelManager(kernel_name='python3')
    manager.start_kernel(cwd=str(ROOT))
    client = manager.client(); client.start_channels(); client.wait_for_ready(timeout=40)
    notebook = nbformat.v4.new_notebook()
    timings = []

    def execute(code, name):
        cell = nbformat.v4.new_code_cell(code)
        notebook.cells.append(cell)
        started = time.monotonic()
        message = client.execute(code, stop_on_error=True)
        errors = []
        while True:
            msg = client.get_iopub_msg(timeout=600)
            if msg.get('parent_header', {}).get('msg_id') != message: continue
            kind, content = msg['msg_type'], msg['content']
            if kind in ('stream', 'display_data', 'execute_result', 'error'):
                output = dict(content); output.pop('transient', None); output['output_type'] = kind
                cell.outputs.append(nbformat.from_dict(output))
                if kind == 'error': errors.append(content)
            if kind == 'status' and content['execution_state'] == 'idle': break
        timings.append({'cell': name, 'seconds': round(time.monotonic()-started, 2), 'errors': errors})
        nbformat.write(notebook, args.artifacts/'executed.ipynb')
        (args.artifacts/'timings.json').write_text(json.dumps(timings, indent=2))
        print(name, timings[-1]['seconds'], 'FAIL' if errors else 'PASS', flush=True)
        if errors: raise RuntimeError(errors[-1]['evalue'])

    def steps(numbers):
        from calmar.guided import source_cell
        for number in numbers:
            code = (f'await run_cells([{number!r}], globals())' if args.guided
                    else ''.join(source_cell(number)['source']))
            execute(code, f'cell-{number}')

    try:
        execute('import os, sys\nfrom pathlib import Path\n'
            'from calmar.guided import run_cells\n'
            'os.environ["CALMAR_REUSE_ONLY"] = "1"\n'
            'import module\nawait module.load("fsl/6.0.7.22")\n'
            'import shutil\nprint("Kernel Python:", sys.executable, "PATH Python:", shutil.which("python"))\n'
            f'_CALMAR_CONFIG_OVERRIDES = {{"REPORTS_SUBDIR": {str(args.artifacts/"reports")!r}}}\n', 'prepare')
        steps([4, 5, 7, 8, 10, 12, 13, 15, 17, 19])
        execute('TEST_SUBJECT_IDX = next(i for i,e in enumerate(SUBJECTS) if e["subject"] == "sub-M2077")\n'
                'CONFIG["TEST_SUBJECT_IDX"] = TEST_SUBJECT_IDX\n', 'select-existing-participant')
        steps([23, 25, 27, "calmar-registration", "calmar-openads", "calmar-manual", 32, 34, 35])
        steps([42, 44, 46, 48, 63, 65, 69, 74, 75, 77])
        execute('INTERP_SUBJECT_IDX = TEST_SUBJECT_IDX\nINTERP_MASK_SOURCE = "synthstroke"\n'
                'INTERP_RUN_DECODING = True\n', 'select-report')
        steps([81, 85, 87])
        execute('assert _rpt_path.is_file()\n'
                'assert _calmar_generated_report_selection[0] == "sub-M2077"\n', 'assert-report')
        # Reopening should reuse results without new jobs or inference.
        execute('_jobs_before = set((PROJECT_DIR/"reports/jobs").iterdir())\n', 'before-reopen')
        steps([15, 25, 27, 32, 34, 69, 81, 85])
        execute('assert set((PROJECT_DIR/"reports/jobs").iterdir()) == _jobs_before\n', 'no-new-jobs-on-reopen')
    finally:
        client.stop_channels(); manager.shutdown_kernel(now=True)


if __name__ == '__main__': main()
