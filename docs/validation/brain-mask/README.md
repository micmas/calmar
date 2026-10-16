# Brain mask for LINDA: HD-BET alone vs HD-BET OR SynthStrip

Decision (2026-10-12): `BRAIN_MASK = "hdbet"` is the default. The union with
SynthStrip is applied **per participant** by the skull-strip repair, when QC
shows that the brain mask left a CSF-filled lesion cavity outside.

Dataset: ds004884 1.0.2 (chronic stroke, expert lesion masks). Tools: `hdbet/1.0.0`,
`synthstrip/7.4.1`, `linda/0.5.1` (seed 1729, one thread).

## 1. Where the masks put the expert lesion (36 sessions)

`src/analysis_40_compare_brain_extraction.sh`, summarised by `scripts/summarize.py`
and `scripts/hybrids.py` → `mask_metrics.json`, `hybrids.json`, `worst_cases.png`,
`hybrid_worst_cases.png`.

| Brain mask | Sessions with >5% of the lesion outside | Worst | Extra volume beyond HD-BET and the lesion (median) |
|---|---|---|---|
| HD-BET fast | 12 / 36 | 35% | 0 ml |
| HD-BET fast + morphological closing | 11 | 34% | 11 ml |
| HD-BET accurate | 11 | 34% | 25 ml |
| SynthStrip, with CSF | 3 | 10% | 163 ml |
| HD-BET OR SynthStrip (union) | 2 | 7% | 163 ml |

HD-BET follows surviving tissue, so a chronic infarct cavity that opens onto the
brain surface falls outside its mask. The union keeps it, at the price of a CSF
rim of ~160 ml around the whole brain.

## 2. What LINDA does with each mask (8 sessions)

`src/analysis_41_linda_brain_mask_comparison.sh` (Slurm array, 16 LINDA runs),
scored by `scripts/score_linda.py` → `linda_scores.json`, `linda_comparison.png`
(expert red, LINDA with HD-BET yellow, LINDA with the union cyan). Four sessions
have 12–59 ml of the expert lesion outside HD-BET (among the largest of the 36)
and four have almost none, so the set over-represents the case the union is for.

| Median of 8 | HD-BET | Union |
|---|---|---|
| Dice | 0.607 | 0.589 |
| Sensitivity | 0.76 | 0.86 |
| Precision | 0.53 | 0.44 |
| False positives | 45 ml | 84 ml |

| Session | Expert lesion | Outside HD-BET | Dice HD-BET → union | False positives |
|---|---|---|---|---|
| sub-M2045 ses-381 | 269 ml | 59 ml (22%) | 0.729 → **0.771** | 52 → 79 ml |
| sub-M2029 ses-180 | 154 ml | 42 ml (27%) | 0.607 → **0.695** | 38 → 49 ml |
| sub-M2051 ses-284 | 131 ml | 25 ml (19%) | 0.607 → 0.569 | 81 → 159 ml |
| sub-M2037 ses-275 | 36 ml | 12 ml (34%) | 0.406 → 0.358 | 24 → 88 ml |
| sub-M2018 ses-341 | 47 ml | 2 ml | 0.436 → 0.411 | 96 → 110 ml |
| sub-M2061 ses-252 | 83 ml | 1 ml | 0.750 → 0.748 | 29 → 36 ml |
| sub-M2120 ses-749 | 42 ml | 0.3 ml | 0.602 → 0.493 | 37 → 67 ml |
| sub-M2001 ses-1076 | 150 ml | 0.2 ml | 0.665 → 0.610 | 118 → 163 ml |

With the union, LINDA labels the cavity (55–90% of the expert lesion outside
HD-BET, against 4–53% with HD-BET), but it also labels CSF next to the lesion
that the expert did not. The figure shows the cyan outline spreading into that CSF.

### Caveat: LINDA's sensitivity to numerical noise

The pipeline's LINDA step later re-ran sub-M2051 ses-284 with the identical HD-BET
mask, seed and one thread (Slurm job 39, 2026-10-13). The one difference was
`OPENBLAS_NUM_THREADS=1`, which the comparison script did not set. Its lesion was
222 ml instead of 174 ml, with Dice 0.87 between the two runs; round 1 already
differed. So, for this participant, a purely numerical difference moved LINDA as
much as the choice of brain mask did. The per-session differences above (Dice
−0.11 to +0.09) are of the same order, and the "~40 ml" rule below is tentative.
The comparison script now sets `OPENBLAS_NUM_THREADS=1`; repeating the comparison
(ideally twice) would separate the mask effect from this noise.

## When the union helps

Only when a **large** cavity, roughly 40 ml or more, lies outside the HD-BET
mask: sub-M2045 and sub-M2029 above, both with big cortical infarcts whose
resorbed cortex is continuous with the CSF over the brain. When the part outside
is small (sub-M2037, 12 ml) or moderate with a lot of nearby sulcal CSF
(sub-M2051, 25 ml), the extra false positives outweigh the gain. With nothing
outside, the union only adds false positives. This rule rests on 8 sessions and one LINDA run per mask (see the caveat above).

In QC this case looks like: on the skull-strip stage, a dark CSF-filled cavity
in the lesion territory lies outside the brain-mask outline, and on the LINDA
stage the red lesion outline stops at the brain-mask edge. Tag the skull strip
`lesion_excluded_by_strip`, mark the participant for repair and run the skull-strip repair. With
`REPAIR_BRAIN_MASK = "auto"`, a participant with that tag gets the union mask
(SynthStrip runs first if needed) and LINDA is recomputed with it; the method is
recorded in `<T1>_desc-<mode>_brain_mask.json`. Rate the new LINDA output: if it
now spreads into sulcal CSF, the union did not help this participant.

## Reproduce

The raw runs (masks and LINDA outputs, ~2.5 GB) are not tracked. Regenerate them
with the two Slurm scripts above, then run the scripts here from the project root
with `CALMAR_BRAIN_MASK_RUNS=<their output folder>` (default
`notes/review-20261009/brain-extraction`).
