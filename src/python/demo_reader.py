"""A browser-native reader for the completed public four-participant demo.

Only explicitly named, already computed MNI derivatives are exported. Source MRI,
arbitrary widget URLs and other participants remain outside the publication.
"""
from pathlib import Path
import base64
import hashlib
import html
import json
import re
import shutil
from datetime import datetime

COHORT = [
    ('sub-M2001', 'ses-1076', 'ds004884', 'linda', 'synthstroke', 'Chronic stroke · T1w'),
    ('sub-M2004', 'ses-524', 'ds004884', 'linda', 'synthstroke', 'Chronic stroke · T1w'),
    ('sub-strokecase0001', 'ses-0001', 'ISLES-2022', 'openads', 'openads', 'Acute stroke · DWI + ADC'),
    ('sub-strokecase0002', 'ses-0001', 'ISLES-2022', 'openads', 'openads', 'Acute stroke · DWI + ADC'),
]


def allowed_volumes():
    result = set()
    for subject, session, dataset, route, method, _ in COHORT:
        root = Path('data') / dataset / 'derivatives'
        def at(tool, name):
            return root / tool / subject / session / 'anat' / name
        result.update([at(route, 'Subject_in_MNI.nii.gz'), at(route, 'ExpertMask_in_MNI.nii.gz'),
                       at('bcbtoolkit', f'Disconnectome_{method}.nii.gz')])
        if route == 'linda':
            result.update([at('linda', 'Lesion_in_MNI.nii.gz'), at('synthstroke', 'SynthStroke_in_MNI.nii.gz')])
        else:
            result.add(at('openads', 'OpenADS_in_MNI.nii.gz'))
    return result


def copy_volume(project, staging, relative):
    relative = Path(relative)
    if relative not in allowed_volumes():
        raise ValueError(f'Not an approved demo derivative: {relative}')
    source = project / relative
    source.resolve().relative_to(project.resolve())
    if not source.is_file() or not 0 < source.stat().st_size < 90 * 1024**2:
        raise ValueError(f'Missing or oversized viewer derivative: {relative}')
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:16]
    target = Path('volumes') / (digest + '-' + source.name)
    (staging / target).parent.mkdir(exist_ok=True)
    shutil.copy2(source, staging / target)
    return target.as_posix()


def build_reader(project, staging, record, assets):
    from bs4 import BeautifulSoup
    cases = []
    for subject, session, dataset, route, method, subtitle in COHORT:
        root = Path('data') / dataset / 'derivatives'
        def volume(tool, name):
            return copy_volume(project, staging, root / tool / subject / session / 'anat' / name)
        reports = [Path(p) for p in record['reports'] if Path(p).name == f'interpretation_{subject}_{session}_{method}.html']
        if len(reports) != 1:
            raise ValueError(f'Expected one {method} report for {subject}, got {len(reports)}')
        report = reports[0]
        soup = BeautifulSoup(report.read_text(), 'html.parser')
        image = soup.find('img', alt='Lesion overlay (MNI space)')
        if image is None or not image['src'].startswith('data:image/png;base64,'):
            raise ValueError(f'Report has no saved overlay: {subject}')
        thumbnail = f'assets/{subject}-overlay.png'
        (staging / thumbnail).write_bytes(base64.b64decode(image['src'].split(',', 1)[1], validate=True))
        masks = [{'label': 'SynthStroke' if method == 'synthstroke' else 'OpenADS',
                  'url': volume(method, 'SynthStroke_in_MNI.nii.gz' if method == 'synthstroke' else 'OpenADS_in_MNI.nii.gz')}]
        if route == 'linda':
            masks.append({'label': 'LINDA', 'url': volume(route, 'Lesion_in_MNI.nii.gz')})
        masks.append({'label': 'Expert mask', 'url': volume(route, 'ExpertMask_in_MNI.nii.gz')})
        pdfs = [{'label': Path(p).stem.removeprefix(f'{subject}_{session}_').replace('_', ' · '),
                 'url': assets.mapping[Path(p)]} for p in record['atlas_pdfs'] if f'{subject}_{session}_' in Path(p).name]
        cases.append({'id': subject, 'session': session, 'dataset': dataset, 'subtitle': subtitle,
                      'background_label': 'T1w' if route == 'linda' else 'DWI',
                      'background': volume(route, 'Subject_in_MNI.nii.gz'), 'masks': masks,
                      'disconnectome': volume('bcbtoolkit', f'Disconnectome_{method}.nii.gz'),
                      'report': assets.mapping[report], 'thumbnail': thumbnail, 'pdfs': pdfs})
    vendor = project / 'analyses/unattended-demo/web-tools/node_modules/@niivue/niivue'
    version = json.loads((vendor / 'package.json').read_text())['version']
    if version != '0.69.0':
        raise ValueError(f'Expected Niivue 0.69.0, found {version}')
    source = project / 'src/web/demo'
    (staging / 'vendor').mkdir()
    shutil.copy2(vendor / 'dist/index.js', staging / 'vendor/niivue.js')
    shutil.copy2(source / 'LICENSE-niivue.txt', staging / 'vendor/LICENSE-niivue.txt')
    for name in ('reader.css', 'reader.js'):
        shutil.copy2(source / name, staging / name)
    data = {'cases': cases, 'completed': record['completed_at'], 'controller_job': record['job_id'], 'niivue': '0.69.0'}
    (staging / 'cases.json').write_text(json.dumps(data, indent=2) + '\n')
    cards = []
    for c in cases:
        pdf_links = ''.join(f'<li><a href="{p["url"]}">{html.escape(p["label"])} <span>PDF ↗</span></a></li>' for p in c['pdfs'])
        cards.append(f'''<article class="case-card" id="{c['id']}">
          <a href="{c['report']}" class="preview"><img src="{c['thumbnail']}" alt="Saved {c['masks'][0]['label']} lesion overlay for {c['id']}" loading="lazy" width="1001" height="539"></a>
          <div class="case-body"><p class="eyebrow">{c['subtitle']}</p><h3>{c['id']}</h3>
          <p>{c['dataset']} · {c['session']} · {c['masks'][0]['label']}</p>
          <div class="case-actions"><a class="primary" href="{c['report']}">Read report <span>↗</span></a>
          <button class="text-button explore-case" data-case="{c['id']}">Explore scan ↑</button></div>
          <details class="downloads"><summary>Atlas maps <span>{len(c['pdfs'])} PDFs</span></summary><ul>{pdf_links}</ul></details></div></article>''')
    template = (source / 'index.html').read_text()
    template = template.replace('<!-- CASE_CARDS -->', '\n'.join(cards))
    template = template.replace('{{PARTICIPANTS}}', f'{len(cases):02d}')
    template = template.replace('{{DATASETS}}', f'{len({c["dataset"] for c in cases}):02d}')
    template = template.replace('{{PDFS}}', str(len(record['atlas_pdfs'])))
    template = template.replace('{{COMPLETED}}', datetime.fromisoformat(record['completed_at']).strftime('%d %B %Y'))
    (staging / 'index.html').write_text(template)
    sources = [Path(__file__), *(source / name for name in ('index.html', 'reader.css', 'reader.js'))]
    return {'cases': len(cases), 'renderer': 'niivue/0.69.0',
            'source_hashes': {str(p.relative_to(project)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
            'volume_files': len(list((staging / 'volumes').glob('*')))}


def readable_notebook(page):
    """Preserve the record, folding noisy cell outputs and explaining kernel controls."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page, 'html.parser')
    for paragraph in soup.select('p.small.muted'):
        if 'interactive panels' in paragraph.get_text():
            paragraph.string = 'Image viewers are available in the browser demo. Processing and QC controls require a running Neurodesk session.'
    for widget in soup.select('.widget'):
        widget.clear()
        link = soup.new_tag('a', href='index.html#explore')
        link.string = 'Explore images in the browser viewer →'
        widget.append(link)
        note = soup.new_tag('p')
        note.string = 'Processing, repair and QC controls are available in the running notebook.'
        widget.append(note)
    for script in soup.find_all('script'):
        if 'const toc = document.querySelector' not in script.get_text():
            script.decompose()
    favicon = soup.new_tag('link', rel='icon', href='data:,')
    if soup.head:
        soup.head.append(favicon)
    for cell in soup.select('section.cell'):
        if cell.select('.out-image, .out-html, .out-md'):
            continue
        details = soup.new_tag('details', attrs={'class': 'saved-cell'})
        summary = soup.new_tag('summary')
        original = cell.select_one('details.code > summary')
        summary.string = original.get_text().replace('Show code', 'Code and logs', 1) if original else 'Saved execution log'
        details.append(summary)
        # Keep only one disclosure around text-only cells.
        for nested in cell.select('details.code, details.log'):
            label = nested.find('summary')
            if label:
                label.decompose()
            nested.unwrap()
        for child in list(cell.contents):
            details.append(child.extract())
        cell.append(details)
    banner = soup.new_tag('p', attrs={'style': 'padding:1rem;background:#eef5f2;border-radius:8px;'})
    link = soup.new_tag('a', href='index.html')
    link.string = '← Back to the interactive demo'
    banner.append(link)
    soup.select_one('.nb-main').insert(0, banner)
    return str(soup)


def notebook_report_links(nb, assets, record):
    """Do not nest complete report documents (their global CSS/JS) in a notebook."""
    import copy
    result = copy.deepcopy(nb)
    for cell in result['cells']:
        for output in cell.get('outputs', []):
            data = output.get('data', {})
            raw = data.get('text/html', '')
            text = ''.join(raw) if isinstance(raw, list) else raw
            if 'calmarPrintState' not in text and '<!doctype html' not in text.lower():
                continue
            matches = [Path(p) for p in record['reports'] if Path(p).name.split('_')[1] in text]
            if not matches:
                matches = [Path(p) for p in record['reports']]
            links = ''.join(f'<li><a href="{assets.mapping[p]}">Read the report for {html.escape(p.name.split("_")[1])} ↗</a></li>' for p in matches)
            output['data'] = {'text/html': '<p>Full participant report, including sources and figures:</p><ul>'+links+'</ul>'}
    return result
