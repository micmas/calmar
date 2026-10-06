"""Keep full tool logs on disk and concise status messages in the notebook."""

from pathlib import Path
import subprocess


def run_logged(command, log_path, **kwargs):
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, **kwargs)
    print(f'Processing log: {path}')
    if result.returncode:
        print(f'Processing failed (exit {result.returncode}). Last log messages:')
        print('\n'.join(path.read_text(errors='replace').splitlines()[-12:]))
    return result
