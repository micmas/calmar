"""Keep full tool logs on disk and concise status messages in the notebook."""

from pathlib import Path
import subprocess
import os
import shutil
import shlex
from uuid import uuid4

# Every external command run in this process, in order. Processing jobs copy
# the slice recorded while building a product into its cache record, so the
# notebook can show exactly what ran (including for cached results).
COMMANDS = []
# Executable -> resolved path for each command run. Neurodesk wrappers live in
# their container's folder (e.g. .../containers/linda_0.5.1_20260508/), so this
# records which container build produced an output. None of the imaging tools
# answer --version, so this is the tool identity we can actually observe.
TOOLS = {}


def record(description):
    """Record a step that ran in-process (no command line), e.g. SimpleITK."""
    COMMANDS.append(description)


def run_logged(command, log_path, **kwargs):
    COMMANDS.append(shlex.join(str(c) for c in command))
    executable = str(command[0])
    if executable == 'bash' and len(command) > 1:
        executable = str(command[1])
    resolved = shutil.which(executable) or (executable if Path(executable).exists() else None)
    TOOLS[executable] = os.path.realpath(resolved) if resolved else None
    if executable.endswith('.sh') and executable.startswith(('src/', str(Path.cwd()))):
        # A project wrapper: record what it runs on, i.e. the loaded Neurodesk
        # modules and the container behind their main executables.
        TOOLS[executable + ' (modules)'] = os.environ.get('LOADEDMODULES', '')
        for tool in ('linda_predict.sh', 'antsApplyTransforms', 'run_disco.sh'):
            found = shutil.which(tool)
            if found:
                TOOLS[f'{executable} -> {tool}'] = os.path.realpath(found)
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    check = kwargs.pop('check', False)
    try:
        with path.open('w') as stream:
            result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, **kwargs)
    finally:
        # Atomic publication removes temporary directories even on success.
        # Keep tool logs (including nested FSL diagnostics and timeout output)
        # independently of the image publication lifecycle.
        staging = next((p for p in path.parents if '.attempt.' in p.name), None)
        if staging is not None:
            archive = Path('logs')/'processing_attempts'/os.environ.get('SLURM_JOB_ID', 'local')/uuid4().hex
            for log in staging.rglob('*.log'):
                destination = archive/log.relative_to(staging)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(log, destination)
            print(f'Attempt logs retained: {archive}', flush=True)
    print(f'Processing log: {path}')
    if result.returncode:
        print(f'Processing failed (exit {result.returncode}). Last log messages:')
        print('\n'.join(path.read_text(errors='replace').splitlines()[-12:]))
        if check:
            # Staging directories are removed on failure. Keep the complete tool
            # log outside staging so diagnosis does not depend on its last lines.
            archive = Path('logs')/'processing_failures'/os.environ.get('SLURM_JOB_ID', 'local')
            archive.mkdir(parents=True, exist_ok=True)
            retained = archive/f'{uuid4().hex}-{path.name}'
            shutil.copy2(path, retained)
            print(f'Full failed-attempt log retained: {retained}', flush=True)
            raise subprocess.CalledProcessError(result.returncode, command)
    return result
