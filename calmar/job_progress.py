"""One status line for the Slurm jobs a notebook cell is waiting for.

While the jobs run, a single line is rewritten in place (carriage return, so it
also works where output is stored server-side and in-place display updates are
not), e.g.

    linda · sub-M2061 ses-252 · Slurm job 45 · running 1:23:10 · round 3/3: SyNCC registration since 09:10 (slowest step, 1-3.5 h)
    synthstroke · 3 jobs · 1 done, 2 running · 0:02:10

and when they finish it is replaced by one closing line ("done in 2:45:30").
The tool's step is read from the ``processing.log`` of the job's in-progress
output folder (``<output>.attempt.*``); LINDA's log is timestamped ("03:52 1st
round of prediction..."). Outside a notebook or terminal (e.g. a log file) a
line is printed only when a state changes. Nothing here touches results.
"""
import re
import sys
import time

# Derivative folder (calmar.study.DERIVATIVE_KEYS) that holds each stage's log.
STAGE_FOLDERS = {'brain': 'hdbet', 'linda': 'linda', 'synthstroke': 'synthstroke',
                 'bcb': 'bcbtoolkit', 'deepdisco': 'deepdisco'}
STATES = {'PENDING': 'queued', 'CONFIGURING': 'starting', 'RUNNING': 'running', 'COMPLETING': 'finishing',
          'COMPLETED': 'done', 'FAILED': 'failed', 'CANCELLED': 'cancelled', 'TIMEOUT': 'time limit reached',
          'OUT_OF_MEMORY': 'out of memory'}
TIMESTAMPED = re.compile(r'^(\d\d:\d\d)\s+(\S.*)$')
ROUND = re.compile(r'(1st|2nd|3rd) round of prediction')
REGISTRATION = re.compile(r'Running registration:\s*(\S+)')
# LINDA's slowest part: its final registration (SyNCC) can take 1-3.5 h on one thread.
SLOW_STEPS = {'SyNCC': 'slowest step, 1-3.5 h'}
WIDTH = 160


def latest_step(log_text):
    """Short description of the newest step in a tool's processing.log."""
    lines = [line.rstrip() for line in log_text.splitlines() if line.strip()]
    stamped = [m for m in (TIMESTAMPED.match(line) for line in lines) if m]
    if not stamped:
        return lines[-1][:80] if lines else ''
    when, what = stamped[-1].groups()
    what = what.replace('All_Command_lines_OK', '').strip().rstrip('.')
    registration = REGISTRATION.search(what)
    if registration:
        what = f'{registration.group(1)} registration'
    rounds = [r.group(1) for r in (ROUND.search(m.group(2)) for m in stamped) if r]
    prefix = f'round {rounds[-1][0]}/3: ' if rounds and not ROUND.search(what) else ''
    note = next((f' ({v})' for k, v in SLOW_STEPS.items() if k in what), '')
    return f'{prefix}{what} since {when}{note}'[:110]


def step_log(stage, payload):
    """Newest processing.log of the job's in-progress output folder, if any."""
    from .study import derivative_dirs
    folder = STAGE_FOLDERS.get(stage)
    entries = payload.get('entries') or []
    if folder is None or len(entries) != 1 or 'dataset' not in payload:
        return None
    final = derivative_dirs(payload['dataset'], payload.get('config', {}), entries[0])[folder]
    logs = [log for attempt in final.parent.glob(f'{final.name}.attempt.*')
            for log in attempt.rglob('processing.log')]
    return max(logs, key=lambda p: p.stat().st_mtime, default=None)


def _clock(seconds):
    seconds = int(seconds)
    return f'{seconds // 3600}:{seconds // 60 % 60:02d}:{seconds % 60:02d}'


def _live():
    """True where a rewritten line displays as one line (notebook or terminal)."""
    try:
        from IPython import get_ipython
        if getattr(get_ipython(), 'kernel', None) is not None:
            return True
    except ImportError:
        pass
    return sys.stdout.isatty()


class JobProgress:
    """Status line of the jobs one ``submit_step`` call waits for."""

    def __init__(self, stage, jobs):
        self.stage, self.jobs, self.rows = stage, jobs, {}
        self.started = time.monotonic()
        self.live, self.shown = _live(), ''
        self.refresh()

    def _who(self, job):
        entries = job['payload'].get('entries') or []
        return ', '.join(' '.join(filter(None, [e.get('subject'), e.get('session')])) for e in entries) or self.stage

    def update(self, job, state, step=None):
        """Record a job's Slurm state (sacct/squeue name) and current step."""
        if step is None:
            log = step_log(self.stage, job['payload']) if state == 'RUNNING' else None
            try:
                step = latest_step(log.read_text(errors='replace')) if log else ''
            except OSError:
                step = ''
        row = (STATES.get(state, state.lower()), step)
        changed = self.rows.get(job['job'], (None, None))[:2] != row
        self.rows[job['job']] = row + (time.monotonic() - job['started'],)
        if not self.live and changed:
            print(f"{self.stage} · {self._who(job)} · Slurm job {job['job']}: {row[0]}" + (f' · {step}' if step else ''),
                  flush=True)

    def line(self):
        rows = [self.rows.get(job['job'], ('submitted', '', 0)) for job in self.jobs]
        if len(self.jobs) == 1:
            state, step, elapsed = rows[0]
            text = (f"{self.stage} · {self._who(self.jobs[0])} · Slurm job {self.jobs[0]['job']} · "
                    f"{state} {_clock(elapsed)}" + (f' · {step}' if step else ''))
        else:
            counts = {}
            for state, *_ in rows:
                counts[state] = counts.get(state, 0) + 1
            text = (f"{self.stage} · {len(self.jobs)} jobs · "
                    + ', '.join(f'{n} {state}' for state, n in counts.items())
                    + f" · {_clock(time.monotonic() - self.started)}")
        return text[:WIDTH]

    def refresh(self):
        """Rewrite the status line (live output only)."""
        if self.live:
            self._write(self.line())

    def finish(self, failed=0):
        """Replace the status line with a closing one."""
        took = _clock(time.monotonic() - self.started)
        if failed:
            text = f'{self.stage} · {failed} of {len(self.jobs)} job(s) failed after {took}'
        elif len(self.jobs) == 1:
            text = f"{self.stage} · {self._who(self.jobs[0])} · done in {took} (Slurm job {self.jobs[0]['job']})"
        else:
            text = f'{self.stage} · {len(self.jobs)} jobs done in {took}'
        if self.live:
            self._write(text)
            print(flush=True)
        else:
            print(text, flush=True)

    def _write(self, text):
        # Pad with spaces: a carriage return only overwrites, it does not clear.
        print('\r' + text.ljust(len(self.shown)), end='', flush=True)
        self.shown = text
