"""Publish the completed public demo through micmas/calmar's GitHub Pages workflow."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import re
import subprocess
import tempfile
import time


REPO = 'micmas/calmar'
DOMAIN = 'calmar.aphasia-kb.app'
WORKFLOW = '.github/workflows/notebook-page.yml'
OLD_BUILD = '''          python _kb/scripts/build_notebook_page.py --calmar . --notebook "$NOTEBOOK" \\
            --out _site --strict --source-commit "$GITHUB_SHA"'''
NEW_BUILD = '''          if [ "$PUBLISH_DEMO" = "1" ]; then
            python -c 'import json; m=json.load(open("demo/publication.json")); assert m["state"] == "ready" and not m["page"]["unknown"] and not m["page"]["errors"]'
            python _kb/scripts/build_notebook_page.py --calmar . --notebook demo/lesion-interpretation-demo.ipynb \\
              --out _demo_validation --strict --source-commit "$GITHUB_SHA"
            mkdir -p _site
            cp -a demo/. _site/
            python -c 'import json,os; p="_site/build.json"; d=json.load(open(p)); d["notebook_commit"]=os.environ["GITHUB_SHA"]; open(p,"w").write(json.dumps(d,indent=2)+"\\n")'
          else
            python _kb/scripts/build_notebook_page.py --calmar . --notebook "$NOTEBOOK" \\
              --out _site --strict --source-commit "$GITHUB_SHA"
          fi'''


def adapt_workflow(text):
    flag = '  # Set PUBLISH_DEMO to "0" to publish NOTEBOOK again; retain demo/ for the archived run.\n  PUBLISH_DEMO: "1"\n'
    if flag not in text:
        anchor = '  NOTEBOOK: lesion-interpretation-pipeline.ipynb\n'
        if text.count(anchor) != 1:
            raise ValueError('Notebook publication environment changed; manual reconciliation required.')
        text = text.replace(anchor, anchor + flag, 1)
    if '      - demo/**\n' not in text:
        anchor = '      - lesion-interpretation-pipeline.ipynb\n'
        if text.count(anchor) != 1:
            raise ValueError('Publishing workflow triggers changed; manual reconciliation required.')
        text = text.replace(anchor, anchor + '      - demo/**\n', 1)
    if NEW_BUILD not in text:
        if text.count(OLD_BUILD) != 1:
            raise ValueError('Publishing build step changed; manual reconciliation required.')
        text = text.replace(OLD_BUILD, NEW_BUILD, 1)
    return text


def run(*args, cwd=None):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if result.returncode:
        detail = re.sub(r'(?:gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+)',
                        '[REDACTED]', result.stderr[-4000:])
        raise RuntimeError(f'{args[0]} exited {result.returncode}: {detail}')
    return result.stdout.strip()


def publish(bundle, state_dir, run_job):
    record = json.loads((bundle / 'publication.json').read_text())
    if record.get('state') != 'ready' or str(record.get('controller_job')) != str(run_job):
        raise ValueError('Only the completed bundle from the requested controller may be published.')
    if record['page']['unknown'] or record['page']['errors']:
        raise ValueError('Bundle has unknown datasets or failed cells.')
    if record.get('generator') != 'calmar-demo-publication-v1' or not record.get('files'):
        raise ValueError('Bundle has no verified file manifest.')
    theme_commit = (record.get('reader') or {}).get('shared_theme_commit')
    if theme_commit and run('gh', 'api', 'repos/micmas/stroke-aphasia-kb/commits/main', '--jq', '.sha') != theme_commit:
        raise ValueError('Shared themes changed since verification. Reconcile and rebuild before publishing.')
    actual_files = {str(p.relative_to(bundle)) for p in bundle.rglob('*') if p.is_file()}
    if actual_files != set(record['files']) | {'publication.json'}:
        raise ValueError('Bundle contents differ from its publication manifest.')
    for name, digest in record['files'].items():
        if hashlib.sha256((bundle / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f'Bundle file changed after packaging: {name}')
    if any(p.is_symlink() for p in bundle.rglob('*')):
        raise ValueError('The publication bundle must contain actual files, not symlinks.')
    if any(p.stat().st_size >= 95 * 1024**2 for p in bundle.rglob('*') if p.is_file()):
        raise ValueError('A publication file exceeds the GitHub file-size allowance.')
    pages = json.loads(run('gh', 'api', f'repos/{REPO}/pages'))
    if pages.get('cname') != DOMAIN or pages.get('build_type') != 'workflow':
        raise ValueError('The repository no longer has the confirmed Pages configuration.')
    state_dir.mkdir(parents=True, exist_ok=True)
    state = {'state': 'preparing', 'domain': DOMAIN, 'controller_job': str(run_job),
             'publisher_job': os.environ.get('SLURM_JOB_ID'), 'bundle': str(bundle),
             'publish_demo': True, 'restore_normal': 'Set PUBLISH_DEMO to "0" in ' + WORKFLOW}

    def save():
        state['updated_at'] = datetime.now(timezone.utc).isoformat()
        temporary = state_dir / 'status.tmp'
        temporary.write_text(json.dumps(state, indent=2) + '\n')
        temporary.replace(state_dir / 'status.json')

    save()
    def interrupted(signum, frame):
        state['signal'] = signum
        raise InterruptedError(f'Publisher received signal {signum}; check any pushed commit before retrying.')

    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    try:
        checkout = Path(tempfile.mkdtemp(prefix='checkout-', dir=state_dir))
        run('git', 'clone', '--depth=1', '--branch', 'main',
            f'https://github.com/{REPO}.git', str(checkout))
        if record.get('remote_base') and run('git', '-C', str(checkout), 'rev-parse', 'HEAD') != record['remote_base']:
            raise ValueError('Remote changed since theme/navigation reconciliation. Rebuild against the latest remote before publishing.')
        # Work from the latest remote commit without touching the active analysis
        # worktree, its notebook edits, or the user's changed KB submodule pointer.
        target = checkout / 'demo'
        if target.exists():
            prior_path = target / 'publication.json'
            prior = json.loads(prior_path.read_text()) if prior_path.is_file() else {}
            previous_files = {str(p.relative_to(target)) for p in target.rglob('*') if p.is_file()}
            if (prior.get('generator') != 'calmar-demo-publication-v1'
                    or previous_files != set(prior.get('files', {})) | {'publication.json'}):
                raise ValueError('Existing demo directory has unrelated content; refusing to replace it.')
            # Preserve a prior published demo locally before replacing its files.
            target.rename(state_dir / ('previous-demo-' + checkout.name))
        shutil.copytree(bundle, target)
        source_project = Path(__file__).resolve().parents[2]
        implementation_names = []
        for name, digest in record.get('implementation_files', {}).items():
            relative = Path(name)
            if relative.is_absolute() or '..' in relative.parts or relative.parts[0] not in ('src', 'tests'):
                raise ValueError('Implementation file outside the website source roots')
            source_file = source_project / relative
            source_file.resolve().relative_to(source_project)
            if hashlib.sha256(source_file.read_bytes()).hexdigest() != digest:
                raise ValueError(f'Implementation changed after packaging: {name}')
            destination = checkout / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, destination)
            implementation_names.append(name)
        workflow = checkout / WORKFLOW
        workflow_text = adapt_workflow(workflow.read_text())
        if theme_commit:
            workflow_text, matches = re.subn(r'(repository: micmas/stroke-aphasia-kb\s+ref:) [^\n]+',
                                             r'\g<1> ' + theme_commit, workflow_text)
            if matches != 1:
                raise ValueError('Cannot pin the verified shared theme checkout in the workflow')
        workflow.write_text(workflow_text)
        run('git', '-C', str(checkout), 'add', '--', 'demo', WORKFLOW, *implementation_names)
        if not run('git', '-C', str(checkout), 'diff', '--cached', '--name-only'):
            raise RuntimeError('Nothing changed; inspect the prior publication instead of deploying twice.')
        author = run('git', 'config', 'user.name')
        email = run('git', 'config', 'user.email')
        message = ('Publish notebook-first demo with inline saved viewers and figures' if record.get('architecture') == 'notebook-first' else
                   'Fix demo viewers and add a readable participant overview' if record.get('reader')
                   else 'Publish completed four-participant CALMaR demo (PUBLISH_DEMO=1)')
        run('git', '-C', str(checkout), '-c', 'user.name=' + author, '-c', 'user.email=' + email,
            'commit', '-m', message)
        commit = run('git', '-C', str(checkout), 'rev-parse', 'HEAD')
        state.update(state='pushing', commit=commit, checkout=str(checkout))
        save()
        # Credential helper reads the existing authenticated gh session; no token
        # is placed in command arguments, generated files or log output.
        run('git', '-c', 'credential.helper=', '-c', 'credential.helper=!gh auth git-credential',
            '-C', str(checkout), 'push', 'origin', 'HEAD:main')
        state.update(state='awaiting_pages_workflow', pushed=True)
        save()
        workflow_run = None
        for _ in range(12):
            runs = json.loads(run('gh', 'run', 'list', '--repo', REPO,
                '--workflow', 'notebook-page.yml', '--commit', commit,
                '--json', 'databaseId,status,conclusion,url'))
            if runs:
                workflow_run = runs[0]
                break
            time.sleep(10)
        if workflow_run is None:
            raise RuntimeError(f'Commit {commit} pushed, but no Pages workflow appeared within two minutes.')
        state.update(state='deploying', workflow_url=workflow_run['url'],
                     workflow_id=workflow_run['databaseId'])
        save()
        with (state_dir / 'github-pages.log').open('w') as log:
            subprocess.run(['gh', 'run', 'watch', str(workflow_run['databaseId']), '--repo', REPO,
                            '--exit-status', '--interval', '15'], stdout=log, stderr=subprocess.STDOUT,
                           check=True, timeout=2700)
        final = json.loads(run('gh', 'run', 'view', str(workflow_run['databaseId']), '--repo', REPO,
                               '--json', 'status,conclusion,headSha,url'))
        if final['conclusion'] != 'success' or final['headSha'] != commit:
            raise RuntimeError(f'Pages deployment did not succeed for the published commit: {final}')
        state.update(state='published', url=f'https://{DOMAIN}/')
        save()
        print(json.dumps(state, indent=2))
    except BaseException as error:
        state.update(state='failed_after_push' if state.get('pushed') else 'failed', error=str(error))
        save()
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--run-job', required=True)
    parser.add_argument('--state-dir', type=Path, default=Path('analyses/unattended-demo/publication'))
    args = parser.parse_args()
    publish(args.bundle.resolve(), args.state_dir.resolve(), args.run_job)


if __name__ == '__main__':
    main()
