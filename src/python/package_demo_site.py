"""Package a completed demo for the existing GitHub Pages notebook workflow.

Copies linked report assets. The secondary reader exports an exact allowlist of
registered derivatives; notebook-first additionally exports saved viewer inputs
from the selected public cohort. No data folders are recursively published.
The preview option produces a clearly marked local draft and cannot be published
by the deployment script. The main notebook and knowledge base remain untouched.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import html
from html.parser import HTMLParser
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit


EXPECTED = {"sub-M2001", "sub-M2004", "sub-strokecase0001", "sub-strokecase0002"}
LINK = re.compile(r'''\b(href|src)\s*=\s*(["'])(.*?)\2''', re.I | re.S)
EXTENSIONS = {'.html', '.htm', '.pdf', '.png', '.jpg', '.jpeg', '.svg', '.gif',
              '.css', '.js', '.json', '.tsv', '.csv', '.woff', '.woff2', '.ttf'}


def check_links(root):
    missing = []

    class Links(HTMLParser):
        def __init__(self, path):
            super().__init__()
            self.path = path

        def handle_starttag(self, tag, attrs):
            for key, value in attrs:
                if key not in ('src', 'href') or not value:
                    continue
                url = urlsplit(value)
                if url.scheme or url.netloc or not url.path:
                    continue
                if url.path.startswith('/'):
                    if '/files/' in url.path or url.path.startswith('/home/'):
                        missing.append(value)
                    continue
                if not (self.path.parent / unquote(url.path)).is_file():
                    missing.append(value)

    for path in root.rglob('*.html'):
        Links(path).feed(path.read_text())
    if missing:
        raise ValueError(f'Publication has broken local links: {missing[:20]}')


class Assets:
    def __init__(self, project, output):
        self.project, self.output = project.resolve(), output
        self.mapping = {}
        self.unavailable = set()

    def add(self, source):
        # Filter the user-facing path before following DataLad annex symlinks.
        source = Path(os.path.abspath(source))
        relative = source.relative_to(self.project)
        source.resolve().relative_to(self.project)
        if source.suffix.lower() not in EXTENSIONS or not source.is_file():
            raise ValueError(f'Not a supported report asset: {source}')
        # Data-derived assets must belong to this explicitly selected public cohort.
        participants = set(re.findall(r'(?<![A-Za-z0-9])sub-[A-Za-z]*\d[A-Za-z0-9]*', str(relative)))
        if participants - EXPECTED:
            raise ValueError(f'Asset names an unselected participant: {relative}')
        if relative.parts[0] not in ('data', 'reports', 'analyses'):
            raise ValueError(f'Asset is outside the analysis output roots: {relative}')
        if relative.parts[0] == 'data' and source.suffix.lower() in ('.json', '.csv', '.tsv') and not participants:
            raise ValueError(f'Dataset-wide metadata is not a selected participant asset: {relative}')
        if source in self.mapping:
            return self.mapping[source]
        digest = hashlib.sha256(str(relative).encode()).hexdigest()[:16]
        target = f'assets/{digest}-{source.name}'
        self.mapping[source] = target
        dest = self.output / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix.lower() in ('.html', '.htm', '.svg'):
            text = self.rewrite(source.read_text(), base=source.parent, asset=True)
            dest.write_text(text)
        else:
            shutil.copy2(source, dest)
        return target

    def resolve(self, url, base):
        if '${' in url or '{{' in url:
            return None  # JavaScript/template placeholders are not file links.
        parsed = urlsplit(html.unescape(url))
        if parsed.scheme in ('data', 'mailto', 'javascript') or not parsed.path:
            return None
        path = unquote(parsed.path)
        if '/files/' in path and not parsed.netloc:
            tail = path.split('/files/', 1)[1]
            candidates = [self.project / tail, *[p / tail for p in self.project.parents]]
            return next((p for p in candidates if p.is_file()), candidates[0])
        if parsed.scheme or parsed.netloc or path.startswith('//'):
            return None
        if path.startswith('/home/'):
            return Path(path)
        if path.startswith('/'):
            return None
        return base / path

    def rewrite(self, text, *, base=None, asset=False):
        base = base or self.project

        def replace(match):
            kind, quote, url = match.groups()
            source = self.resolve(url, base)
            if source is None:
                return match.group(0)
            try:
                target = self.add(source)
            except (ValueError, OSError):
                self.unavailable.add(url)
                # Unsupported local downloads (e.g. raw NIfTI) stay labelled but
                # cease being links to a private Jupyter session.
                return 'title="Available in the running notebook only"'
            suffix = urlsplit(html.unescape(url)).fragment
            target = Path(target).name if asset else target
            if suffix:
                target += '#' + suffix
            return f'{kind}={quote}{html.escape(target, quote=True)}{quote}'

        return LINK.sub(replace, text)

    def tree(self, value):
        if isinstance(value, dict):
            result = {}
            for key, item in value.items():
                if key in ('_esm', '_js', '_css'):
                    result[key] = item
                elif key in ('url', 'path') and isinstance(item, str) and (
                        '/files/' in item or item.startswith('/home/')):
                    source = self.resolve(item, self.project)
                    try:
                        result[key] = self.add(source) if source is not None else None
                    except (ValueError, OSError, TypeError):
                        result[key] = None
                    if result[key] is None:
                        self.unavailable.add(item)
                else:
                    result[key] = self.tree(item)
            return result
        if isinstance(value, list):
            return [self.tree(item) for item in value]
        if isinstance(value, str) and ('href=' in value or 'src=' in value):
            return self.rewrite(value)
        return value


def package(project, completion, destination, *, preview=None, run_job=None, reader=False, notebook_first=False, remote_checkout=None, theme_checkout=None):
    if reader and preview:
        raise ValueError('The browser reader requires a completed run.')
    if preview:
        record = {'notebook': str(preview), 'reports': [], 'atlas_pdfs': [], 'state': 'preview'}
    else:
        record = json.loads(completion.read_text())
        if record.get('state') != 'completed' or set(record.get('participants', [])) != EXPECTED:
            raise ValueError('Refusing to package an incomplete or unexpected cohort.')
        if run_job and str(record.get('job_id')) != str(run_job):
            raise ValueError('Completion manifest belongs to another controller job.')
        provenance = Path(str(completion) + '.prov.json')
        if not provenance.is_file():
            raise ValueError('Completion provenance is missing.')
        receipt = json.loads(provenance.read_text())
        if (receipt.get('output_id') != 'demo_run'
                or str(receipt.get('slurm_job_id')) != str(record.get('job_id'))
                or receipt.get('artifact_sha256') != hashlib.sha256(completion.read_bytes()).hexdigest()):
            raise ValueError('Completion manifest does not match its provenance receipt.')
        if len(set(record.get('reports', []))) != 4 or not record.get('atlas_pdfs'):
            raise ValueError('Four participant reports and atlas PDFs are required.')
    source = Path(record['notebook']).resolve()
    source.relative_to(project)
    nb = json.loads(source.read_text())
    original_state = nb.get('metadata', {}).get('widgets', {}).get('application/vnd.jupyter.widget-state+json', {}).get('state', {})
    code = [c for c in nb['cells'] if c['cell_type'] == 'code' and ''.join(c['source']).strip()]
    if not preview and any(c.get('execution_count') is None or
                           any(o.get('output_type') == 'error' for o in c.get('outputs', []))
                           for c in code):
        raise ValueError('Notebook contains an unexecuted or failed cell.')
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError(f'Preserve the previous bundle; choose a fresh path: {destination}')
    staging = Path(tempfile.mkdtemp(prefix=destination.name + '.attempt.', dir=destination.parent))
    assets = Assets(project, staging)
    downloads = []
    for path in record['reports'] + record['atlas_pdfs']:
        target = assets.add(path)
        downloads.append((Path(path).name, target))
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            cell['outputs'] = assets.tree(cell.get('outputs', []))
    if 'widgets' in nb.get('metadata', {}):
        nb['metadata']['widgets'] = assets.tree(nb['metadata']['widgets'])
    viewer_note = ('Explore the registered images in the [browser viewer](index.html#explore). '
                   'Processing and QC controls require the notebook in Neurodesk.\n\n' if reader else
                   'Live MRI viewers and computation require opening the notebook in Neurodesk; '
                   'raw MRI volumes are not hosted here.\n\n')
    nb['cells'].append({'cell_type': 'markdown', 'id': 'demo-public-downloads', 'metadata': {},
        'source': ['## Saved demo downloads\n\nHuman QC was skipped for this demonstration. '
                   'This page preserves static figures and reports. ' + viewer_note,
                   *[f'- [{label}]({target})\n' for label, target in downloads]]})
    if preview:
        nb['cells'].insert(0, {'cell_type': 'markdown', 'id': 'demo-preview-only', 'metadata': {},
                              'source': ['# PREVIEW ONLY — processing is incomplete\n']})
    public_notebook = staging / 'lesion-interpretation-demo.ipynb'
    public_notebook.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + '\n')
    builder = project / 'stroke-aphasia-kb/scripts/build_notebook_page.py'
    spec = importlib.util.spec_from_file_location('calmar_page_builder', builder)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    css = module.EXPLORER_CSS.read_text() + '\n' + module.PAGE_CSS.read_text()
    render_nb = nb
    if reader:
        from demo_reader import notebook_report_links
        render_nb = notebook_report_links(nb, assets, record)
    page, info = module.build(render_nb, 'CALMaR: from an MRI to a cited report',
                              'micmas/calmar · demo/lesion-interpretation-demo.ipynb', css)
    if info['unknown'] or (info['errors'] and not preview):
        raise ValueError(f'Page validation failed: {info}')
    (staging / 'index.html').write_text(page)
    reader_info = None
    if reader:
        from demo_reader import build_reader, readable_notebook
        (staging / 'notebook.html').write_text(readable_notebook(page))
        reader_info = build_reader(project, staging, record, assets)
    if notebook_first:
        from notebook_first import build_notebook_first
        info, notebook_info = build_notebook_first(project, staging, nb, original_state, record,
                                                  assets, remote_checkout, theme_checkout)
        if info['unknown'] or info['errors']:
            raise ValueError(f'Notebook-first page validation failed: {info}')
        reader_info.update(notebook_info)
    check_links(staging)
    manifest = {'generator': 'calmar-demo-publication-v1',
                'state': 'preview' if preview else 'ready', 'controller_job': record.get('job_id'),
                'created_at': datetime.now(timezone.utc).isoformat(),
                'source_notebook_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                'page_builder_sha256': hashlib.sha256(builder.read_bytes()).hexdigest(),
                'participants': sorted(EXPECTED), 'human_qc': 'skipped',
                'page_styles_sha256': hashlib.sha256(css.encode()).hexdigest(),
                'page_builder_commit': subprocess.check_output(
                    ['git', '-C', str(builder.parent.parent), 'rev-parse', 'HEAD'], text=True).strip(),
                'page_builder_worktree_dirty': bool(subprocess.check_output(
                    ['git', '-C', str(builder.parent.parent), 'status', '--porcelain'], text=True).strip()),
                'assets': len(assets.mapping), 'local_links_disabled': len(assets.unavailable),
                'page': info, 'reader': reader_info}
    if notebook_first:
        manifest['remote_base'] = notebook_info['remote_base']
        manifest['architecture'] = 'notebook-first'
        implementation = [project / p for p in (
            'src/python/package_demo_site.py', 'src/python/publish_demo_site.py',
            'src/python/demo_reader.py', 'src/python/notebook_first.py',
            'src/analysis_60_package_demo_site.sh', 'src/analysis_61_publish_demo_site.sh',
            'src/analysis_62_demo_web_dependencies.sh', 'src/analysis_63_verify_demo_reader.sh',
            'src/analysis_64_verify_notebook_first.sh', 'tests/test_demo_publication.py',
            'tests/test_demo_reader.py', 'tests/test_notebook_first.py')]
        implementation += sorted((project / 'src/web/demo').glob('*'))
        manifest['implementation_files'] = {str(p.relative_to(project)): hashlib.sha256(p.read_bytes()).hexdigest()
                                             for p in implementation if p.is_file()}
    (staging / 'build.json').write_text(json.dumps({
        'notebook': 'demo/lesion-interpretation-demo.ipynb', 'notebook_commit': '',
        'built': manifest['created_at'], 'cells': info['cells'], 'outputs': info['outputs'],
        'widgets': info['widgets'], 'panels_without_state': info['panels'],
        'figures': info['images'], 'datasets': info['datasets'],
        'architecture': 'notebook-first' if notebook_first else 'reader' if reader else 'notebook-export',
        'inline_viewers': info.get('inline_viewers', 0),
        'figure_count_basis': 'Inline image occurrences, including embedded HTML and saved report figures',
        'controller_job': record.get('job_id'), 'human_qc': 'skipped'}, indent=2) + '\n')
    manifest['files'] = {str(path.relative_to(staging)): hashlib.sha256(path.read_bytes()).hexdigest()
                         for path in sorted(staging.rglob('*')) if path.is_file()}
    (staging / 'publication.json').write_text(json.dumps(manifest, indent=2) + '\n')
    subprocess.run(['neurodesk-astra-provenance', 'publish', str(staging), str(destination),
                    '--output-id', 'demo_site', '--tool', sys.executable,
                    '--script', str(project / 'src/analysis_60_package_demo_site.sh')], check=True)
    print(json.dumps(manifest, indent=2))
    print('Publication bundle:', destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--completion', type=Path, default=Path('analyses/unattended-demo/run/completion.json'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--run-job')
    parser.add_argument('--preview', type=Path)
    parser.add_argument('--reader', action='store_true', help='Build the browser-native demo reader and retain the notebook separately.')
    parser.add_argument('--notebook-first', action='store_true')
    parser.add_argument('--remote-checkout', type=Path)
    parser.add_argument('--theme-checkout', type=Path)
    args = parser.parse_args()
    package(Path.cwd().resolve(), args.completion, args.output, preview=args.preview, run_job=args.run_job,
            reader=args.reader or args.notebook_first, notebook_first=args.notebook_first,
            remote_checkout=args.remote_checkout, theme_checkout=args.theme_checkout)


if __name__ == '__main__':
    main()
