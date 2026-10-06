"""Human-readable notebook step names, retaining stable keys for reruns."""

import re
import time
from contextlib import contextmanager
from html import escape

from IPython.display import HTML, display
from .execution import _notebook_cells


TITLES = {
    4: 'Load software modules', 5: 'Check software', 7: 'Certificate setup',
    8: 'Setup imports', 10: 'Enable step timing', 12: 'Configuration',
    13: 'Prepare workflow checkpoints', 15: 'Load atlases', 17: 'Prepare dataset',
    19: 'Discover subjects', 23: 'HD-BET brain extraction — single subject',
    25: 'LINDA lesion segmentation — single subject',
    27: 'SynthStroke lesion segmentation — single subject',
    30: 'Review registration and lesion masks',
    32: 'BCBToolkit disconnectome — single subject',
    34: 'DeepDisco disconnectome — single subject',
    35: 'Compare disconnectomes and lesion',
    39: 'Choose batch or reporting', 42: 'HD-BET and LINDA — batch',
    44: 'SynthStroke — batch', 46: 'Warp SynthStroke to MNI',
    48: 'Warp manual masks to MNI', 51: 'Quality control',
    53: 'Repair brain extraction', 55: 'Manual mask editing',
    56: 'Inspect manual edits', 57: 'Apply mask edits', 58: 'Refresh QC',
    60: 'Reset QC', 63: 'BCBToolkit disconnectomes — batch',
    65: 'DeepDisco disconnectomes — batch', 69: 'Calculate atlas overlap',
    74: 'Preview and export results', 75: 'Export atlas results',
    77: 'Prepare interpretation', 79: 'Choose report inputs',
    81: 'Generate participant report', 85: 'Functional decoding', 87: 'Available outputs',
}


def step_key(source, cell_id=None):
    if cell_id:
        return cell_id
    marker = re.search(r'^# CALMAR_CELL_ID: ([\w-]+)', source, re.M)
    if marker:
        return marker.group(1)
    for name in ('lesion-interpretation-pipeline.ipynb', 'calmar-guided.ipynb'):
        matches = [cell['id'] for cell in _notebook_cells(name)
                   if cell['cell_type'] == 'code' and ''.join(cell['source']).strip() == source.strip()]
        if len(matches) == 1:
            return matches[0]
    return next((s.strip().lstrip('#').strip()[:80] for s in source.splitlines()
                 if s.strip() and not set(s.strip()) <= set('# =')), '(empty cell)')


def step_title(key):
    key = key.removeprefix('CALMAR_CELL_ID: ').strip()
    match = re.fullmatch(r'calmar-step-(\d+)', key)
    if not match and key != 'calmar-test-participant':
        return key
    title = TITLES.get(int(match[1]), 'Notebook step') if match else 'Choose single-subject participant'
    cells = _notebook_cells('lesion-interpretation-pipeline.ipynb')
    position = next((i for i, c in enumerate(cells, 1) if c['id'] == key), None)
    return f'{title} (cell {position})' if position else title


def format_seconds(seconds):
    if seconds < 60:
        return f'{seconds:.1f} s'
    if seconds < 3600:
        return f'{int(seconds // 60)} min {int(seconds % 60)} s'
    return f'{int(seconds // 3600)} h {int(seconds % 3600 // 60)} min'


def batch_html(label, record):
    records = list(record['participants'].values())
    def table_rows(records):
        return ''.join(
            '<tr>' + ''.join(f'<td style="padding:3px 10px">{escape(str(value))}</td>' for value in
                (r['subject'], r['session'], r['stage'], r['detail'], r['status'], format_seconds(r['seconds']))) + '</tr>'
            for r in records)
    header = ('<table><tr><th>Participant</th><th>Session</th><th>Step</th><th>Mask / model / atlas</th>'
              '<th>Result</th><th>Time</th></tr>')
    details = ''
    if any(r['detail'] for r in records):
        summary = {}
        for row in records:
            key = (row['subject'], row['session'], row['stage'])
            total = summary.setdefault(key, {**row, 'detail': '', 'seconds': 0., 'statuses': set()})
            total['seconds'] += row['seconds']
            total['statuses'].add(row['status'])
            total['status'] = ', '.join(sorted(total['statuses']))
        details = '<details><summary>Mask and atlas breakdown</summary>' + header + table_rows(records) + '</table></details>'
        records = list(summary.values())
    return (f'<h4>{escape(label)} — batch timings</h4>'
            + (header + table_rows(records) + '</table>' if records else '<p>No participant operations ran.</p>')
            + details +
            f'<p>Step elapsed time: <b>{format_seconds(record["seconds"])}</b>. '
            'Cached rows measure the cache check and any preparation, not the original processing time.</p>')


class BatchTiming:
    """Time one batch execution and its non-overlapping participant operations."""

    def __init__(self, namespace, label):
        self.namespace, self.label = namespace, label
        self.record = dict(seconds=0., participants={})

    def __enter__(self):
        self.started = time.perf_counter()
        self.namespace.setdefault('BATCH_TIMINGS', {})[self.label] = self.record
        return self

    @contextmanager
    def participant(self, entry, stage=None, detail=''):
        row = dict(subject=entry['subject'], session=entry.get('session') or '',
                   stage=stage or self.label, detail=detail, status='Completed', seconds=0.)
        start = time.perf_counter()
        try:
            yield row
        except BaseException:
            row['status'] = 'Interrupted or failed'
            raise
        finally:
            row['seconds'] = time.perf_counter() - start
            key = (row['subject'], row['session'], row['stage'], detail)
            self.record['participants'][key] = row

    def __exit__(self, *error):
        self.record['seconds'] = time.perf_counter() - self.started
        display(HTML(batch_html(self.label, self.record)))


def show_timings(namespace, min_seconds=.5, top=None, slowest_first=False):
    timings = namespace.get('STEP_TIMINGS', {})
    rows = [(key, sec) for key, sec in timings.items() if sec >= min_seconds]
    if top and len(rows) > top:
        keep = {key for key, _ in sorted(rows, key=lambda item: item[1], reverse=True)[:top]}
        rows = [row for row in rows if row[0] in keep]
    if slowest_first:
        rows.sort(key=lambda item: item[1], reverse=True)
    body = ''.join(f'<tr><td>{escape(step_title(key))}</td><td>{format_seconds(sec)}</td></tr>' for key, sec in rows)
    html = ('<h4>Step timings</h4><table><tr><th>Step</th><th>Time</th></tr>' + body +
            f'<tr><td><b>Total (latest run of each step)</b></td><td>{format_seconds(sum(timings.values()))}</td></tr></table>'
            '<p>Includes computation and waiting inside each step. Reruns replace the earlier duration. '
            'Browser image loading and time spent reviewing controls are not included.</p>')
    for label, record in namespace.get('BATCH_TIMINGS', {}).items():
        html += '<details><summary>' + escape(label) + ' — participants</summary>' + batch_html(label, record) + '</details>'
    totals = {}
    for record in namespace.get('BATCH_TIMINGS', {}).values():
        for row in record['participants'].values():
            key = (row['subject'], row['session'])
            totals[key] = totals.get(key, 0.) + row['seconds']
    if totals:
        html += '<h4>Batch time per participant</h4><table><tr><th>Participant / session</th><th>Time</th></tr>'
        html += ''.join(f'<tr><td>{escape(" ".join(key).strip())}</td><td>{format_seconds(sec)}</td></tr>' for key, sec in totals.items())
        html += '</table><p>Sum of the latest recorded batch operations; shared setup is excluded.</p>'
    display(HTML(html))


def install_timing(namespace, shell):
    """Replace old hooks on rerun; guided runners record their constituent steps."""
    namespace['STEP_TIMINGS'] = {key.removeprefix('CALMAR_CELL_ID: '): value
                                for key, value in namespace.get('STEP_TIMINGS', {}).items()}
    namespace.setdefault('BATCH_TIMINGS', {})
    namespace['show_timings'] = lambda **kw: show_timings(namespace, **kw)
    if shell is None:
        return
    # Also remove the notebook's previous inline implementation after upgrading.
    for event, name in (('pre_run_cell', '_timing_pre'), ('post_run_cell', '_timing_post')):
        for callback in list(shell.events.callbacks.get(event, [])):
            if callback is namespace.get(name) or callback in getattr(shell, '_calmar_timing_hooks', ()):
                shell.events.unregister(event, callback)
    state = {}
    def before(info):
        from .execution import _request_cell_id
        state.update(start=time.perf_counter(), source=getattr(info, 'raw_cell', '') or '',
                     cell_id=_request_cell_id(shell))
    def after(result):
        if 'start' not in state:
            return
        # The guided runner times each canonical step, not the enclosing runner again.
        if 'await run_cells(' not in state['source']:
            namespace['STEP_TIMINGS'][step_key(state['source'], state['cell_id'])] = time.perf_counter() - state['start']
        state.clear()
    shell.events.register('pre_run_cell', before)
    shell.events.register('post_run_cell', after)
    shell._calmar_timing_hooks = (before, after)
