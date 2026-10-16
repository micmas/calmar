"""Score the LINDA brain-mask comparison (src/analysis_41) against the expert lesions.

Per session and brain mask: Dice, sensitivity, precision, LINDA volume, false
positives (LINDA outside the expert lesion), and how much of the expert lesion
lying outside the HD-BET mask (the cavity part) LINDA detects. Draws the
sessions side by side (expert red, LINDA with HD-BET mask yellow, LINDA with the
union mask cyan).
"""
import json, os, sys
from pathlib import Path
sys.path.insert(0, '.')
import nibabel as nib, numpy as np
from calmar import step_qc

root = Path(os.environ.get('CALMAR_BRAIN_MASK_RUNS', 'notes/review-20261009/brain-extraction'))
tasks = json.load(open(root / 'linda_tasks.json'))
sessions = {}
for t in tasks:
    sessions.setdefault((t['subject'], t['session']), {})[t['mask_name']] = t
rows, fig_rows = [], []
for (sub, ses), by_mask in sessions.items():
    t1 = step_qc._load(by_mask['hdbet1_fast']['t1w'])
    vox = float(np.prod(t1.header.get_zooms()[:3])) / 1000
    load = lambda p: step_qc._data(step_qc._load(p, t1)) > .5
    expert = load(by_mask['hdbet1_fast']['expert'])
    hdbet = load(by_mask['hdbet1_fast']['mask'])
    cavity = expert & ~hdbet
    row = {'subject': sub, 'session': ses, 'expert_ml': round(expert.sum() * vox, 1),
           'expert_outside_hdbet_ml': round(cavity.sum() * vox, 1)}
    preds = {}
    for name in ('hdbet1_fast', 'union'):
        p = root / 'linda' / f'{sub}_{ses}_{name}' / 'Prediction3_native.nii.gz'
        if not p.exists():
            row[name] = None
            continue
        pred = preds[name] = load(p)
        tp = (pred & expert).sum()
        row[name] = {'dice': round(2 * tp / max(pred.sum() + expert.sum(), 1), 3),
                     'sensitivity': round(tp / max(expert.sum(), 1), 3),
                     'precision': round(tp / max(pred.sum(), 1), 3),
                     'linda_ml': round(pred.sum() * vox, 1),
                     'false_positive_ml': round((pred & ~expert).sum() * vox, 1),
                     'cavity_detected_frac': round((pred & cavity).sum() / cavity.sum(), 3) if cavity.sum() else None}
    rows.append(row)
    if len(preds) == 2:
        overlays = [(expert, 'red'), (preds['hdbet1_fast'], 'yellow'), (preds['union'], 'cyan')]
        fig_rows.append(dict(bg=step_qc._data(t1), overlays=overlays, focus=expert,
                             label=f'{sub} {ses} · expert = red · LINDA with HD-BET mask = yellow · '
                                   f'LINDA with HD-BET+SynthStrip mask = cyan'))
json.dump(rows, open(root / 'linda_scores.json', 'w'), indent=1)
print(f"{'session':24s} {'expert':>7s} {'cavity':>7s} | {'Dice':>5s} {'sens':>5s} {'prec':>5s} {'FP ml':>6s} {'cav':>5s} | "
      f"{'Dice':>5s} {'sens':>5s} {'prec':>5s} {'FP ml':>6s} {'cav':>5s}")
print(' ' * 41 + '| LINDA + HD-BET mask              | LINDA + HD-BET OR SynthStrip mask')
fmt = lambda r: (f"{r['dice']:5.3f} {r['sensitivity']:5.3f} {r['precision']:5.3f} {r['false_positive_ml']:6.1f} "
                 f"{r['cavity_detected_frac'] if r['cavity_detected_frac'] is not None else float('nan'):5.2f}") if r else ' ' * 31 + 'missing'
for r in rows:
    print(f"{r['subject'] + ' ' + r['session']:24s} {r['expert_ml']:7.1f} {r['expert_outside_hdbet_ml']:7.1f} | "
          f"{fmt(r['hdbet1_fast'])} | {fmt(r['union'])}")
both = [r for r in rows if r['hdbet1_fast'] and r['union']]
for k in ('dice', 'sensitivity', 'precision', 'false_positive_ml'):
    a = np.array([r['hdbet1_fast'][k] for r in both]); b = np.array([r['union'][k] for r in both])
    print(f'{k:18s} HD-BET median {np.median(a):.3f}  union median {np.median(b):.3f}  '
          f'median paired difference {np.median(b - a):+.3f}  (n={len(both)})')
if fig_rows:
    step_qc.figure(fig_rows, 'LINDA lesion with each brain mask', root / 'linda_comparison.png')
    print('figure:', root / 'linda_comparison.png')
