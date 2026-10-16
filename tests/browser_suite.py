"""Run browser fixtures against an owned server; never touch user sessions."""
import argparse
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.request import urlopen
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--artifacts', type=Path, required=True)
    args = parser.parse_args()
    args.artifacts.mkdir(parents=True, exist_ok=True)
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0)); port = sock.getsockname()[1]
    token = uuid4().hex
    base = f'http://127.0.0.1:{port}'
    env = {**os.environ, 'CALMAR_BROWSER_TOKEN': token}
    # The owned server is mounted at '/', not the parent JupyterHub prefix.
    # Its kernels must discover this server rather than another running server.
    env.pop('JUPYTERHUB_SERVICE_PREFIX', None)
    runtime = args.artifacts.resolve()/'runtime'
    runtime.mkdir(mode=0o700, exist_ok=True)
    env['JUPYTER_RUNTIME_DIR'] = str(runtime)
    with (args.artifacts/'server.log').open('w') as log:
        server = subprocess.Popen([sys.executable, '-m', 'jupyterlab', '--no-browser', '--ip=127.0.0.1',
            f'--port={port}', f'--ServerApp.root_dir={Path.home()}',
            f'--ServerApp.preferred_dir={Path.home()}', f'--FileContentsManager.preferred_dir={Path.home()}',
            f'--IdentityProvider.token={token}'], env=env, stdout=log, stderr=subprocess.STDOUT)
        try:
            for _ in range(150):
                if server.poll() is not None: raise RuntimeError('Owned browser server exited')
                try:
                    with urlopen(f'{base}/api?token={token}', timeout=1): break
                except OSError: time.sleep(.2)
            else: raise TimeoutError('Owned browser server did not start')
            for name in ('workflow', 'review', 'results', 'disconnectome'):
                with (args.artifacts/f'{name}.log').open('w') as result:
                    subprocess.run([sys.executable, str(ROOT/'tests'/f'browser_{name}.py'),
                        '--server-url', base, '--artifacts', str(args.artifacts/name)],
                        env=env, stdout=result, stderr=subprocess.STDOUT, check=True, timeout=360)
                print(f'PASS: {name}', flush=True)
        finally:
            server.terminate()
            try: server.wait(timeout=20)
            except subprocess.TimeoutExpired: server.kill(); server.wait()


if __name__ == '__main__': main()
