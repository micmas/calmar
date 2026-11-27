"""Static, notebook-first export of saved CALMaR output; never executes a cell.

Widget state is interpreted as data, not executed as JavaScript. Only volume paths
actually referenced by a saved viewer and belonging to the four public cases are
copied. Unsaved repair previews and kernel callbacks are explicitly unavailable.
"""
import base64
import copy
from datetime import datetime
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup
from demo_reader import COHORT, notebook_report_links

VIEW = 'application/vnd.jupyter.widget-view+json'


def esc(value):
    return html.escape(str(value), quote=True)


def text(value):
    return ''.join(value) if isinstance(value, list) else str(value or '')


def add_demo_guide(soup, hero):
    hero.select_one('.lead').string = (
        'Follow four saved examples from stroke MRI to a participant report. '
        'See how CALMaR finds the stroke lesion, checks the result, and measures brain volumes '
        'or white-matter changes when the right scans are available. Open an inline viewer '
        'to inspect the saved images and overlays in your browser.')
    links = hero.select_one('.notebook-links')
    if links is None:
        links = soup.new_tag('p', attrs={'class': 'notebook-links'})
        hero.append(links)
    links.clear()
    for href, label in (
        ('#single-subject-test', 'Walk through the first case'),
        ('#optional-diffusion-tract-microstructure-analysis', 'See white-matter results'),
        ('#optional-background-brain-health', 'See brain-health results'),
        ('#generated-participant-report', 'Read participant reports'),
        ('explorer.html', 'Browse by participant'),
    ):
        if href.startswith('#') and soup.find(id=href[1:]) is None:
            continue
        link = soup.new_tag('a', href=href)
        link.string = label
        if links.contents:
            links.append(' ')
        links.append(link)


def explorer_source(checkout):
    demo = checkout / 'demo'
    prior = json.loads((demo / 'publication.json').read_text())
    source = demo / ('explorer.html' if prior.get('architecture') == 'notebook-first' else 'index.html')
    if not source.is_file() or 'reader.js' not in source.read_text() or 'id="explore"' not in source.read_text():
        raise ValueError('The reconciled checkout has no participant explorer')
    return source


def refresh_explorer_links(source, record, assets):
    """Point retained editorial links at the artifacts from the current run."""
    targets = {}
    for path in map(Path, record['reports'] + record['atlas_pdfs']):
        target = assets.mapping[path]
        if path.name in targets and targets[path.name] != target:
            raise ValueError(f'Ambiguous explorer artifact name: {path.name}')
        targets[path.name] = target
    soup = BeautifulSoup(source.read_text(), 'html.parser')
    for link in soup.select('a[href^="assets/"]'):
        url = urlsplit(link['href'])
        match = re.fullmatch(r'assets/[0-9a-f]{16}-(.+)', unquote(url.path))
        if match and match[1] in targets:
            link['href'] = url._replace(path=targets[match[1]]).geturl()
    return str(soup)


class SavedWidgets:
    def __init__(self, project, staging, state, assets, cases):
        self.project, self.staging, self.state, self.assets = project, staging, state, assets
        self.cases = cases
        self.viewers = {}
        self.volume_sources = {}
        self.omitted = []
        self.controls = {m['state']['viewer_id']: m['state'] for m in state.values()
                         if m['state'].get('_anywidget_id', '').endswith('LayerControls')}
        self.seen_viewers = set()
        self.serial = 0

    def model(self, ref):
        return self.state.get(ref.removeprefix('IPY_MODEL_'), {}).get('state', {})

    def report_subject(self, ref, outputs):
        values, seen = [], set()
        def visit(ref):
            if ref in seen:
                return
            seen.add(ref)
            m = self.model(ref)
            values.append(str(m.get('value', '')))
            for child in m.get('children', []):
                visit(child)
        visit(ref)
        def matches(blob):
            return {c['id'] for c in self.cases if f'interpretation_{c["id"]}_' in blob}
        own = matches(' '.join(values))
        surrounding = matches(json.dumps(outputs))
        if len(own) > 1 or (own and surrounding and own != surrounding):
            raise ValueError('Ambiguous participant association in a saved report widget')
        if own:
            return own.pop()
        return None

    def volume(self, model):
        url = (model.get('path') or {}).get('url', '')
        # This is deliberately not a general URL downloader or file copier.
        prefix = '/files/neurodesktop-storage/calmar/'
        path = unquote(urlsplit(url).path)
        if prefix not in path:
            raise ValueError('Saved volume has no recognised local project path')
        relative = Path(path.split(prefix, 1)[1])
        if '..' in relative.parts or relative.is_absolute() or not str(relative).endswith('.nii.gz'):
            raise ValueError('Invalid saved volume path')
        if relative.parts[0] == 'qc_edits':
            self.omitted.append(str(relative))
            return None
        allowed = False
        for subject, session, dataset, *_ in COHORT:
            parts = relative.parts
            if parts[:2] != ('data', dataset):
                continue
            if parts[2:4] == (subject, session):
                allowed = True  # selected public native input referenced by this saved view
            if len(parts) > 6 and parts[2] == 'derivatives' and parts[4:6] == (subject, session):
                allowed = parts[3] in ('linda', 'hdbet', 'synthstroke', 'openads', 'bcbtoolkit', 'deepdisco')
        if not allowed:
            raise ValueError(f'Volume outside the saved public cohort: {relative}')
        source = self.project / relative
        source.resolve().relative_to(self.project.resolve())
        if not source.is_file() or not 0 < source.stat().st_size < 90 * 1024**2:
            raise ValueError(f'Missing or oversized saved volume: {relative}')
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        target = Path('volumes') / (digest[:16] + '-' + source.name)
        if not (self.staging / target).exists():
            shutil.copy2(source, self.staging / target)
        self.volume_sources[str(relative)] = {'url': target.as_posix(), 'sha256': digest}
        result = {k: model[k] for k in ('name', 'colormap', 'opacity', 'cal_min', 'cal_max')
                  if model.get(k) is not None}
        result['url'] = target.as_posix()
        result['source'] = str(relative)
        result['name'] = source.name
        return result

    def clean_html(self, value):
        soup = BeautifulSoup(self.assets.rewrite(text(value)), 'html.parser')
        # Report styles and scripts are intended for whole documents. The notebook
        # uses its own scoped presentation and never executes saved widget code.
        for tag in soup.select('script, style, link, meta'):
            tag.decompose()
        for node in soup.find_all(True):
            for key in list(node.attrs):
                if key.startswith('on'):
                    del node[key]
            for key in ('href', 'src'):
                if str(node.get(key, '')).lstrip().lower().startswith('javascript:'):
                    del node[key]
        for button in soup.select('button, input, select, textarea'):
            label = button.get_text(' ', strip=True) or button.get('aria-label') or 'Action'
            replacement = soup.new_tag('span', attrs={'class': 'kernel-action'})
            replacement.string = label + ' · requires Neurodesk'
            button.replace_with(replacement)
        return str(soup)

    def viewer(self, ref):
        ref = ref.removeprefix('IPY_MODEL_')
        if ref in self.seen_viewers:
            return ''
        self.seen_viewers.add(ref)
        state = self.model(ref)
        config = self.controls.get(ref, {})
        roles = {r['key']: r.get('label', r['key']) for r in config.get('roles', [])}
        layer_data = {r['model_id']: r for r in config.get('layers', [])}
        layers, omitted = [], False
        for volume_ref in state.get('volumes', []):
            model = self.model(volume_ref)
            volume = self.volume(model)
            if volume is None:
                omitted = True
                continue
            setting = layer_data.get(volume_ref.removeprefix('IPY_MODEL_'), {})
            label = roles.get(setting.get('role'), volume['name'].removesuffix('.nii.gz').replace('_', ' '))
            qualifiers = [setting.get('group'), setting.get('variant')]
            label += (' · ' + ' · '.join(q for q in qualifiers if q)) if any(qualifiers) else ''
            volume.update(label=label, color=setting.get('color', '#888888'),
                          saved_opacity=setting.get('opacity'), centre=setting.get('centre'))
            layers.append(volume)
        if not layers:
            return '<p class="saved-note">No image was loaded in this saved panel. Selecting an atlas or computing a region chart requires Neurodesk. The saved tables and atlas PDFs remain available below.</p>'
        subject = re.search(r'sub-[A-Za-z0-9]+', layers[0]['source']).group()
        space = 'MNI template space' if '_in_MNI' in layers[0]['name'] else 'native image space'
        self.viewers[ref] = {'layers': layers, 'subject': subject, 'space': space,
                             'crosshair': state.get('scene', {}).get('crosshairPos', [.5, .5, .5]),
                             'plane': config.get('plane', state.get('opts', {}).get('sliceType', 3))}
        note = '<p class="saved-note">The unsaved clean-up preview is omitted. This view shows the original saved inputs; applying or saving a repair requires Neurodesk.</p>' if omitted else ''
        return self.viewer_html(ref, subject, space, note)

    def viewer_html(self, ref, subject, space, note=''):
        return f'''<section class="inline-viewer" data-viewer="{esc(ref)}" aria-label="Image viewer for {esc(subject)}">
          <div class="viewer-heading"><strong>{esc(subject)}</strong><span>{esc(space)} · neurological view (left is left)</span></div>
          <div class="viewer-slot"><p>Inspect the saved images at this step.</p></div>
          <button class="open-viewer" type="button">Open inline viewer</button>
          <p class="viewer-status" role="status">Loads on demand. Only one image viewer is active at a time.</p>{note}
          <noscript><p>JavaScript and WebGL2 are needed for interactive images. Saved figures and tables can be read without them.</p></noscript>
        </section>'''

    def report_viewer(self, subject):
        case = next(c for c in self.cases if c['id'] == subject)
        ref = 'report-' + subject
        layers = [{'url': case['background'], 'name': 'Registered_' + case['background_label'] + '.nii.gz',
                   'label': 'Registered ' + case['background_label'], 'colormap': 'gray', 'opacity': 1}]
        for index, mask in enumerate(case['masks']):
            layers.append({'url': mask['url'], 'name': mask['label'] + '.nii.gz', 'label': mask['label'],
                           'colormap': ['green', 'red', 'blue'][index], 'cal_min': .5, 'cal_max': 1,
                           'opacity': .5 if index == 0 else 0, 'color': ['#00cc66', '#ef5555', '#5599ff'][index]})
        self.viewers[ref] = {'layers': layers, 'subject': subject, 'space': 'MNI template space', 'crosshair': [.5, .5, .5]}
        return '<p class="saved-note">Browser view of this report’s existing registered images. Changing the visible mask does not regenerate the report.</p>' + self.viewer_html(ref, subject, 'MNI template space')

    def render(self, ref, report_subject=None, trail=()):
        id = ref.removeprefix('IPY_MODEL_')
        if id in trail:
            raise ValueError('Cycle in widget state')
        m = self.model(id)
        kind = m.get('_anywidget_id', m.get('_model_name', ''))
        if kind.endswith('NotebookNavigation'):
            return ''
        if kind.endswith('LayerControls'):
            return self.viewer(m['viewer_id'])
        if kind.endswith('_DeferredNiiVue'):
            return self.viewer(id)
        if kind in ('HTMLModel', 'HTMLMathModel'):
            return '<div class="saved-html">' + self.clean_html(m.get('value', '')) + '</div>'
        if kind == 'OutputModel':
            out = ''.join(self.output(o, report_subject) for o in m.get('outputs', []))
            return out or '<p class="saved-note">No output was saved in this panel.</p>'
        children = m.get('children', [])
        if kind in ('TabModel', 'AccordionModel'):
            self.serial += 1
            uid = 'saved-tabs-' + str(self.serial)
            titles = m.get('titles', [])
            pieces = []
            buttons = []
            selected = m.get('selected_index') or 0
            for i, child in enumerate(children):
                title = titles[i] if i < len(titles) else f'Panel {i + 1}'
                content = self.report_viewer(report_subject) if title == 'Brain viewer' and report_subject else self.render(child, report_subject, (*trail, id))
                if kind == 'AccordionModel':
                    if 'Participant context and lesion overview' in title and report_subject:
                        case = next(c for c in self.cases if c['id'] == report_subject)
                        content = f'<figure class="saved-report-overlay"><img src="{esc(case["thumbnail"])}" alt="Saved {esc(case["masks"][0]["label"])} lesion overlay for {esc(report_subject)} in MNI space"><figcaption>Saved {esc(case["masks"][0]["label"])} report figure · {esc(report_subject)} · MNI space. Human QC was skipped.</figcaption></figure>' + content
                    # Keep the actual saved state; expose the existing lesion figure
                    # by opening the participant overview in each report.
                    opened = m.get('selected_index') == i or 'Participant context' in title
                    pieces.append(f'<details class="saved-accordion"{" open" if opened else ""}><summary>{esc(title)}</summary>{content}</details>')
                else:
                    buttons.append(f'<button type="button" role="tab" id="{uid}-tab-{i}" aria-controls="{uid}-{i}" aria-selected="{str(i == selected).lower()}" tabindex="{0 if i == selected else -1}">{esc(title)}</button>')
                    pieces.append(f'<section role="tabpanel" id="{uid}-{i}" aria-labelledby="{uid}-tab-{i}" class="saved-tab-panel" data-selected="{str(i == selected).lower()}">{content}</section>')
            return ''.join(pieces) if kind == 'AccordionModel' else f'<div class="saved-tabs"><div class="saved-tab-buttons" role="tablist">{"".join(buttons)}</div>{"".join(pieces)}</div>'
        if children:
            return '<div class="saved-box">' + ''.join(self.render(c, report_subject, (*trail, id)) for c in children) + '</div>'
        label = m.get('description', '')
        if kind == 'ButtonModel':
            return f'<span class="kernel-action">{esc(label)} <small>requires Neurodesk</small></span>'
        if kind.endswith('Model') or kind.endswith('ChoiceButtons'):
            options = m.get('_options_labels', [])
            index = m.get('index')
            if isinstance(index, int) and 0 <= index < len(options):
                value = options[index]
            elif isinstance(index, list):
                value = ', '.join(options[i] for i in index if i < len(options))
            else:
                value = m.get('value', 'not set')
            if isinstance(value, bool):
                value = 'yes' if value else 'no'
            return f'<span class="saved-value"><b>{esc(label or "Saved selection")}</b> {esc(value if value != "" else "not set")}</span>'
        raise ValueError(f'Unsupported saved widget: {kind}')

    def output(self, output, report_subject=None):
        d = output.get('data', {})
        if VIEW in d:
            return self.render(d[VIEW]['model_id'], report_subject)
        if 'text/html' in d:
            return '<div class="saved-html">' + self.clean_html(d['text/html']) + '</div>'
        for mime in ('image/png', 'image/jpeg'):
            if mime in d:
                return f'<img alt="Saved notebook figure" src="data:{mime};base64,{text(d[mime])}">'
        if 'text/plain' in d or output.get('output_type') == 'stream':
            return '<pre>' + esc(text(d.get('text/plain', output.get('text', '')))) + '</pre>'
        if 'text/markdown' in d:
            from markdown_it import MarkdownIt
            return MarkdownIt('commonmark').render(text(d['text/markdown']))
        return ''


def build_notebook_first(project, staging, notebook, state, record, assets, remote_checkout, theme_checkout):
    if not remote_checkout or not theme_checkout:
        raise ValueError('A reconciled remote checkout and shared theme checkout are required')
    remote_checkout, theme_checkout = remote_checkout.resolve(), theme_checkout.resolve()
    for checkout in (remote_checkout, theme_checkout):
        if subprocess.check_output(['git', '-C', str(checkout), 'status', '--porcelain'], text=True).strip():
            raise ValueError(f'Reconciliation checkout must be clean: {checkout}')
    remote_base = subprocess.check_output(['git', '-C', str(remote_checkout), 'rev-parse', 'HEAD'], text=True).strip()
    # Retain the latest editorial page and palette as the secondary explorer.
    (staging / 'explorer.html').write_text(refresh_explorer_links(explorer_source(remote_checkout), record, assets))
    shutil.copy2(remote_checkout / 'demo/reader.css', staging / 'reader.css')
    shutil.copy2(remote_checkout / 'demo/reader.js', staging / 'reader.js')
    cases = json.loads((staging / 'cases.json').read_text())['cases']
    renderer = SavedWidgets(project, staging, state, assets, cases)
    nb = notebook_report_links(notebook, assets, record)
    nb['metadata'].pop('widgets', None)
    count = 0
    for cell in nb['cells']:
        outputs = cell.get('outputs', [])
        cell_context = copy.deepcopy(outputs)
        for o in outputs:
            d = o.get('data', {})
            if VIEW in d:
                renderer.seen_viewers = set()
                subject = renderer.report_subject(d[VIEW]['model_id'], cell_context)
                rendered = renderer.render(d[VIEW]['model_id'], subject)
                count += 1
                if not any(token in rendered for token in ('inline-viewer', 'saved-tabs', '<img', '<table', 'saved-accordion')) and rendered.count('kernel-action') > 0:
                    rendered = '<details class="kernel-settings"><summary>Saved settings, messages and actions · Neurodesk required to change them</summary>' + rendered + '</details>'
                o['data'] = {'text/html': '<div class="saved-widget">' + rendered + '</div>'}
            elif 'text/html' in d:
                o['data'] = {'text/html': renderer.clean_html(d['text/html'])}
    # The download footer describes the main page's inline viewers.
    nb['cells'][-1]['source'] = text(nb['cells'][-1]['source']).replace('[browser viewer](index.html#explore)', '[secondary participant explorer](explorer.html#explore)')
    spec = importlib.util.spec_from_file_location('notebook_first_builder', theme_checkout / 'scripts/build_notebook_page.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    page, info = builder.build(nb, 'From MRI to a cited report',
                              'micmas/calmar · demo/lesion-interpretation-demo.ipynb',
                              builder.EXPLORER_CSS.read_text() + '\n' + builder.PAGE_CSS.read_text())
    soup = BeautifulSoup(page, 'html.parser')
    soup.body['class'] = list(soup.body.get('class', [])) + ['notebook-first']
    for script in soup.find_all('script'):
        if 'const toc = document.querySelector' not in script.get_text():
            script.decompose()
    # Fold repetitive progress streams as one block per cell, keeping the
    # scientific tables, figures, and explanatory text in their original place.
    for cell in soup.select('section.cell'):
        logs = cell.select(':scope > pre, :scope > details.log')
        if logs:
            details = soup.new_tag('details', attrs={'class': 'execution-log'})
            summary = soup.new_tag('summary')
            summary.string = 'Saved execution log'
            details.append(summary)
            logs[0].insert_before(details)
            for log in logs:
                details.append(log.extract())
    for table in soup.select('article.nb table'):
        wrap = soup.new_tag('div', attrs={'class': 'table-scroll', 'tabindex': '0', 'role': 'region', 'aria-label': 'Saved results table'})
        table.wrap(wrap)
    figure_count = 0
    for img in soup.select('article.nb img'):
        src = img.get('src', '')
        if src.startswith('data:image/'):
            header, encoded = src.split(',', 1)
            if ';base64' in header:
                raw = base64.b64decode(encoded)
                suffix = '.png' if 'image/png' in header else '.jpg' if 'jpeg' in header else '.svg'
                target = 'assets/figure-' + hashlib.sha256(raw).hexdigest()[:20] + suffix
                (staging / target).write_bytes(raw)
                img['src'] = target
        img['loading'] = 'lazy'
        img['decoding'] = 'async'
        img['alt'] = img.get('alt') or 'Figure saved during the executed demo'
        figure_count += 1
    info['images'] = figure_count
    info['widgets'] = count
    info['widget_state'] = True
    info['inline_viewers'] = len(renderer.viewers)
    hero = soup.select_one('.hero')
    for fact in hero.select('.facts li'):
        if fact.get_text().startswith('Results'):
            fact.clear()
            fact.append(BeautifulSoup(f'<span class="k">Results</span> {figure_count} saved figures · {len(renderer.viewers)} inline viewers · 4 participants', 'html.parser'))
    byline = soup.new_tag('p', attrs={'class': 'notebook-byline'})
    completed = datetime.fromisoformat(record['completed_at'])
    byline.string = ('A research project led by Michèle Masson-Trottier, developed in the open. '
                     f'Demo completed {completed.day} {completed:%B %Y}.')
    hero.append(byline)
    notice = soup.new_tag('div', attrs={'class': 'run-notice'})
    notice.append(BeautifulSoup('<strong>Saved demonstration · human QC was skipped.</strong> Viewer interactions change the display only. Processing, edits and review decisions require a running Neurodesk session. Evidence may include draft or unreviewed findings; this is a research example.', 'html.parser'))
    hero.append(notice)
    add_demo_guide(soup, hero)
    launch = soup.select_one('#launch')
    disclosure = soup.new_tag('details', attrs={'class': 'launch-disclosure'})
    title = soup.new_tag('summary')
    title.string = 'Run or edit this workflow in Neurodesk'
    disclosure.append(title)
    launch.wrap(disclosure)
    for h in soup.select('article.nb h1'):
        h.name = 'h2'
    for link in soup.select('.app-header .nav a'):
        if 'Run it' in link.get_text():
            link.string = 'Run in Neurodesk'
    for name in ('notebook-first.css', 'notebook-first.js'):
        shutil.copy2(project / 'src/web/demo' / name, staging / name)
    # Add shared navigation before our layout overrides, exactly as deployment does.
    (staging / 'index.html').write_text(str(soup))
    subprocess.run(['python', str(theme_checkout / 'scripts/style_project_site.py'), str(staging)], check=True)
    soup = BeautifulSoup((staging / 'index.html').read_text(), 'html.parser')
    soup.head.append(soup.new_tag('link', rel='stylesheet', href='notebook-first.css'))
    soup.head.append(soup.new_tag('link', rel='icon', href='data:,'))
    soup.body.append(soup.new_tag('script', type='module', src='notebook-first.js'))
    final = str(soup)
    (staging / 'index.html').write_text(final)
    (staging / 'notebook.html').write_text(final)
    (staging / 'inline-viewers.json').write_text(json.dumps(renderer.viewers, indent=2) + '\n')
    (staging / 'viewer-sources.json').write_text(json.dumps(renderer.volume_sources, indent=2) + '\n')
    return info, {'remote_base': remote_base, 'shared_theme_commit': subprocess.check_output(
        ['git', '-C', str(theme_checkout), 'rev-parse', 'HEAD'], text=True).strip(),
        'inline_viewers': len(renderer.viewers), 'saved_figures': figure_count,
        'omitted_unsaved_previews': sorted(set(renderer.omitted)),
        'source_hashes_notebook': {str(p.relative_to(project)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in [Path(__file__), project / 'src/web/demo/notebook-first.js', project / 'src/web/demo/notebook-first.css']}}
