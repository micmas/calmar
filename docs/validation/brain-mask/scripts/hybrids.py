"""Score hybrid masks built from the comparison outputs (no new tool runs).

union        = HD-BET 1 fast  OR  SynthStrip (brain + CSF)
cavity_rN    = HD-BET 1 fast  OR  (SynthStrip  AND  close_cavities(HD-BET 1 fast, N mm))
               i.e. SynthStrip's extra voxels are accepted only inside concavities of the HD-BET brain.
"""
import json, os, sys
from pathlib import Path
sys.path.insert(0, '.')
import nibabel as nib, numpy as np
from nibabel.processing import resample_from_to
from calmar.brainmask import close_cavities, save_like
from calmar import step_qc

root = Path(os.environ.get('CALMAR_BRAIN_MASK_RUNS', 'notes/review-20261009/brain-extraction'))
entries = {(e['subject'], e['session']): e for e in json.load(open(root / 'participants.json'))}
out = []
for (sub, ses), e in sorted(entries.items()):
    d = root / 'runs' / f'{sub}_{ses}'
    if not (d / 'metrics.json').exists():
        continue
    t1 = nib.load(e['t1w']); z = t1.header.get_zooms()[:3]; vox = float(np.prod(z)) / 1000
    def on_t1(p):
        img = nib.load(p)
        if img.shape[:3] != t1.shape[:3] or not np.allclose(img.affine, t1.affine, atol=1e-3):
            img = resample_from_to(img, t1, order=0)
        return np.asarray(img.dataobj).reshape(t1.shape[:3]) > .5
    expert, base, ss = on_t1(e['expert']), on_t1(e['hdbet_fast']), on_t1(d / 'synthstrip_csf_mask.final.nii.gz')
    masks = {'union': base | ss}
    for r in (10, 15):
        masks[f'cavity_r{r}'] = base | (ss & close_cavities(base, z, radius_mm=r))
    for name, m in masks.items():
        save_like(m, t1, d / f'{name}_mask.final.nii.gz')
    row = {'subject': sub, 'session': ses, 'masks': {}}
    for name, m in masks.items():
        row['masks'][name] = {'lesion_outside_frac': round(float((expert & ~m).sum() / max(expert.sum(), 1)), 4),
                              'added_beyond_hdbet_and_lesion_ml': round(float((m & ~base & ~expert).sum() * vox), 1),
                              'volume_ml': round(m.sum() * vox, 1)}
    row['masks'].update(json.load(open(d / 'metrics.json'))['masks'])
    out.append(row)
json.dump(out, open(root / 'hybrids.json', 'w'), indent=1)
names = list(out[0]['masks'])
print(f'{len(out)} sessions')
print(f"{'method':20s} {'outside med':>11s} {'mean':>6s} {'max':>6s} {'n>5%':>5s} {'n>1%':>5s} {'added med':>9s} {'max':>6s}")
for n in names:
    lo = np.array([r['masks'][n]['lesion_outside_frac'] for r in out]); add = np.array([r['masks'][n]['added_beyond_hdbet_and_lesion_ml'] for r in out])
    print(f'{n:20s} {np.median(lo):11.4f} {lo.mean():6.3f} {lo.max():6.3f} {(lo>.05).sum():5d} {(lo>.01).sum():5d} {np.median(add):9.1f} {add.max():6.1f}')
worst = sorted(out, key=lambda r: -r['masks']['hdbet1_fast']['lesion_outside_frac'])[:4]
print('worst:', [(r['subject'], {k: r['masks'][k]['lesion_outside_frac'] for k in ('hdbet1_fast', 'synthstrip_csf', 'cavity_r10', 'cavity_r15', 'union')}) for r in worst])
rows = []
for r in worst:
    e = entries[(r['subject'], r['session'])]; d = root / 'runs' / f"{r['subject']}_{r['session']}"
    anat = step_qc._load(e['t1w'])
    ex = step_qc._data(step_qc._load(e['expert'], anat))
    ov = [(step_qc._data(step_qc._load(e['hdbet_fast'], anat)), 'yellow'),
          (step_qc._data(step_qc._load(d / 'synthstrip_csf_mask.final.nii.gz', anat)), 'cyan'),
          (step_qc._data(step_qc._load(d / 'cavity_r15_mask.final.nii.gz', anat)), 'lime'), (ex, 'red')]
    rows.append(dict(bg=step_qc._data(anat), overlays=ov, focus=ex,
                     label=f"{r['subject']} {r['session']} · expert lesion = red · HD-BET 1 fast = yellow · SynthStrip+CSF = cyan · hybrid (cavity r15) = green"))
step_qc.figure(rows, 'Hybrid brain mask on the largest cavities', root / 'hybrid_worst_cases.png')
