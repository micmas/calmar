"""Summarise the brain-extraction comparison and draw the worst cavity cases."""
import glob, json, os, sys
from pathlib import Path
sys.path.insert(0, '.')
import numpy as np
from calmar import step_qc

root = Path(os.environ.get('CALMAR_BRAIN_MASK_RUNS', 'notes/review-20261009/brain-extraction'))
rows = [json.load(open(p)) for p in sorted(glob.glob(str(root / 'runs/*/metrics.json')))]
methods = list(rows[0]['masks'])
print(f'{len(rows)} participants\n')
print(f"{'method':22s} {'lesion outside: median':>22s} {'mean':>6s} {'max':>6s} {'n>5%':>5s} {'n>1%':>5s} "
      f"{'added ml med':>12s} {'max':>6s} {'brain removed ml med':>20s} {'max':>6s} {'volume ml med':>13s}")
for m in methods:
    lo = np.array([r['masks'][m]['lesion_outside_frac'] for r in rows])
    add = np.array([r['masks'][m]['added_beyond_hdbet_and_lesion_ml'] for r in rows])
    rem = np.array([r['masks'][m]['hdbet_brain_removed_ml'] for r in rows])
    vol = np.array([r['masks'][m]['volume_ml'] for r in rows])
    print(f'{m:22s} {np.median(lo):22.4f} {lo.mean():6.3f} {lo.max():6.3f} {(lo > .05).sum():5d} {(lo > .01).sum():5d} '
          f'{np.median(add):12.1f} {add.max():6.1f} {np.median(rem):20.1f} {rem.max():6.1f} {np.median(vol):13.0f}')
secs = {m: np.median([r['seconds'][m] for r in rows if m in r['seconds']]) for m in rows[0]['seconds']}
print('\nmedian seconds (4 CPUs):', secs)

worst = sorted(rows, key=lambda r: -r['masks']['hdbet1_fast']['lesion_outside_frac'])[:3]
colors = {'hdbet1_fast': 'yellow', 'hdbet2': 'orange', 'synthstrip_csf': 'cyan', 'hdbet1_fast_closed': 'magenta'}
fig_rows = []
for r in worst:
    entry = next(e for e in json.load(open(root / 'participants.json')) if e['subject'] == r['subject'] and e['session'] == r['session'])
    anat = step_qc._load(entry['t1w'])
    d = root / 'runs' / f"{r['subject']}_{r['session']}"
    files = {'hdbet1_fast': entry['hdbet_fast'], 'hdbet2': d / 'hdbet2_mask.final.nii.gz',
             'synthstrip_csf': d / 'synthstrip_csf_mask.final.nii.gz', 'hdbet1_fast_closed': d / 'hdbet1_fast_closed_mask.final.nii.gz'}
    expert = step_qc._data(step_qc._load(entry['expert'], anat))
    overlays = [(step_qc._data(step_qc._load(f, anat)), colors[k]) for k, f in files.items()] + [(expert, 'red')]
    fig_rows.append(dict(bg=step_qc._data(anat), overlays=overlays, focus=expert,
                         label=f"{r['subject']} {r['session']} · expert lesion = red · HD-BET 1 fast = yellow · HD-BET 2 = orange · "
                               f"SynthStrip = cyan · HD-BET 1 closed = magenta"))
step_qc.figure(fig_rows, 'Brain masks vs expert lesion: largest cavities', root / 'worst_cases.png')
print('figure:', root / 'worst_cases.png')
