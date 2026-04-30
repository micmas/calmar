# LINDA QC rubric

Reference for rating LINDA pipeline outputs at each stage. The same
definitions are loaded by `linda_qc.py` so the notebook UI and this
document stay in sync — if you change one, regenerate the other.

> **Where the ratings go.** Each rating is saved as a sidecar JSON next
> to the lesion mask: `Lesion_in_MNI.qc.json`. The sidecar's `stages`
> dict carries one rating per pipeline stage (skull strip, registration,
> lesion). The notebook aggregates every sidecar into `qc_summary.csv`.

## The two stages

LINDA's pipeline runs:

```
T1w → N4 bias correction → SKULL STRIP → MNI REGISTRATION → LESION PREDICTION
```

A failure at an earlier stage propagates downstream — you cannot get a
trustworthy lesion mask from a poor skull strip. The QC widget walks
through two stages:

1. **Skull strip / brain extraction** — is the brain mask
   (`BrainMask.nii.gz`) clean? If not, **re-strip with HD-BET** and
   re-run before evaluating the lesion. The QC widget has a one-click
   button for this.
2. **Lesion mask** — the LINDA output proper. Rate this once the
   skull strip is good.

> **Why no registration QC?** Visual QC of MNI registration is
> genuinely hard without specialized tools (template overlays with
> edge highlighting, checkerboards, NMI metrics). The most
> consequential registration failure — the lesion getting warped
> across an anatomical boundary — is usually catchable by inspecting
> the lesion in MNI space (e.g., contralateral hemisphere when the
> stroke was clinically left-sided), so it gets covered by the lesion
> stage's `wrong_hemisphere` and `false_positive_cluster` tags.
> The registration vocabulary is preserved as comments in
> `linda_qc.py` if you want to re-enable it later.

**Workflow tip:** judge skull strip first. If it's a 3, fix it before
rating the lesion. The chip row at the top of the widget shows your
current ratings for both stages at a glance.

---

## Stage 1 — Skull strip / brain extraction

### Ratings

- **1 — Good.** Brain mask cleanly excludes skull and scalp and
  includes all of cortex, cerebellum, and brainstem. Usable as-is.
- **2 — Acceptable.** Minor issues: small bits of dura/scalp included,
  or thin slivers of cortex excluded — fixable by morphology or a
  single round of HD-BET. Lesion QC can usually proceed.
- **3 — Poor.** Major issues: large extracranial regions included,
  brain tissue excluded, or cerebellum/brainstem dropped. **Re-strip
  with HD-BET and re-run LINDA before evaluating downstream stages —
  they are not trustworthy until this is fixed.**

### Tags

- `brain_under_stripped` — Skull, scalp, dura, or eyes are still
  inside the brain mask. *Tiebreaker:* thin meningeal tissue is
  typically rating-2; large dural inclusions are rating-3.
- `brain_over_stripped` — Brain tissue (cortex, white matter) is
  outside the brain mask. *Tiebreaker:* superficial cortex is the most
  commonly mis-excluded region.
- `cerebellum_dropped` — Cerebellum (or part of it) is excluded.
  Common with template-based stripping; HD-BET / SynthStrip usually
  fix this.
- `brainstem_dropped` — Brainstem is excluded. Often co-occurs with
  `cerebellum_dropped`.
- `lesion_excluded_by_strip` — **The most consequential failure mode
  for chronic stroke data.** The lesion area itself is outside the
  brain mask because the cyst has CSF intensity and the stripper
  treated it as extracranial space. Re-strip with HD-BET (which is
  more lesion-tolerant) is the right move.
- `asymmetric_strip` — One hemisphere is stripped more aggressively
  than the other. Often a sign that the registration template doesn't
  fit; deep-learning methods are more robust.
- `other` — Describe in Notes.

### Repair

The QC widget exposes two buttons on this stage:

- **Re-strip with HD-BET** — Runs HD-BET (or SynthStrip as fallback)
  on the original T1w. Saves to `_hdbet_work/`.
- **Re-strip + re-run LINDA** — Runs the brain extractor *and* re-runs
  LINDA on the brain-extracted T1. The original LINDA outputs are
  preserved in `_linda_original/`.

For HD-BET to be available on Neurodesk, load the module first:

```python
import module
await module.load('hdbet/<version>')
```

---

## Stage 2 — Lesion mask

Only rate carefully once the skull strip stage is at least a 2.

### Ratings (1 / 2 / 3)

The rating answers one question: **what does this mask need next?**

### 1 — Good

> Mask faithfully represents the lesion. Borders match within ~2–3
> voxels of what you would draw by hand. No clusters of false
> positives. Native and MNI versions both look correct. **Usable for
> analysis as-is.**

If you'd be willing to compute atlas overlap on this mask without
touching it, it's a 1.

### 2 — Acceptable

> Minor issues only. Some boundary inaccuracy or 1–2 small
> false-positive clusters that can be cleaned with deterministic
> post-processing (threshold, morphology, hemisphere clip). The core
> lesion is correctly identified. **Usable after Tier-1 fixes.**

If a slider tweak in the deterministic-ops cell would make it usable,
it's a 2.

### 3 — Poor

> Substantial issues. Examples: a sub-region of the true lesion is
> missed entirely, large false-positive clusters in healthy tissue,
> lesion in the wrong hemisphere, or a pipeline-stage failure
> (registration off, skull-strip bled). **Needs manual painting (Tier
> 2 / Tier 3) or a re-run with a manual seed.**

If you would not trust this mask without painting or re-running, it's
a 3.

---

## Issue tags

Tags are organized by **what kind of error** is happening, not by
where it is in the brain. Many tags can co-occur on one mask. The
"tiebreaker" line for each tag is the rule to use when an adjacent tag
feels close.

### Coverage errors

These are about whole **components** (regions) being missed or extra.

#### `lesion_missed_partly`
A sub-region of the true lesion is **entirely outside the mask** —
not just shrunk borders.
*Tiebreaker:* if the missed area would need painting in or a regional
re-run, use this; if just lowering the threshold or a morphological
close would catch it, use `boundary_too_tight` instead.

#### `false_positive_cluster`
One or more **separate clusters** of "lesion" appear in tissue that is
not lesioned.
*Tiebreaker:* if the extra voxels are *adjacent* to the true lesion,
that's `boundary_too_loose`, not this.

### Boundary errors

These are about the **edge** of an otherwise-correctly-identified
lesion.

#### `boundary_too_tight`
True lesion is identified, but the borders shrink in by a few voxels
everywhere — fixable by a lower threshold or a morphological close.
*Tiebreaker:* use `lesion_missed_partly` if a whole sub-region is gone.

#### `boundary_too_loose`
True lesion is identified, but borders extend a few voxels past the
true edge everywhere — fixable by a higher threshold or a
morphological open.
*Tiebreaker:* use `false_positive_cluster` if the extra voxels are a
separate, non-adjacent blob.

### Tissue-class confusions

These are about **where** false positives land, not how big they are.
Use them in addition to a coverage tag (e.g. `false_positive_cluster`
+ `csf_included`).

#### `csf_included`
Ventricles, sulci, or other CSF spaces are flagged as lesion. A common
LINDA failure mode in chronic stroke where the cyst itself has CSF
intensity.
*Tiebreaker:* use this when the false positives are *specifically* in
CSF.

#### `extracranial_included`
Skull, scalp, or air outside the brain is flagged as lesion.
*Tiebreaker:* often co-occurs with `skull_strip_failed`, which is the
upstream cause.

### Topology issues

These are about **how the mask is connected**, even when the voxels
are mostly right.

#### `lesion_fragmented`
True lesion is one connected region, but the mask shows it as
multiple disconnected blobs.
*Fix:* morphological close or "keep N largest components".

#### `multiple_lesions_one_missed`
Patient has multiple distinct lesions; the mask captured some but not
all.
*Tiebreaker:* use `lesion_missed_partly` only if the missed lesion
would anatomically continue a single captured lesion.

### Lateralization

#### `wrong_hemisphere`
Mask voxels appear in the contralesional (non-affected) hemisphere.
*Tiebreaker:* if only a few voxels, fix with a `hemisphere_clip` op;
if a large mirror-image lesion, suspect `registration_off`.

### Pipeline-stage failures

These are not about the lesion mask itself but about the
**preconditions** that produced it.

#### `skull_strip_failed`
The brain mask is poor — either excludes brain tissue or includes
scalp. Affects everything downstream.
*Tiebreaker:* if the skull-strip *looks* fine in the QC view but
extra-cranial voxels still got into the lesion, use
`extracranial_included` instead.

#### `registration_off`
MNI alignment is poor — the lesion is in the right place in native
space but in the wrong place in MNI.
*Tiebreaker:* compare the "Lesion (native)" view vs the "Lesion (MNI)"
view in the QC cell; if only the MNI version looks wrong, this is the
right tag.

### Catch-all

#### `other`
Something else — please describe in Notes.

---

## How tags map to ratings (rules of thumb)

The relationship is not strict — context matters — but these are
typical patterns:

| Tag pattern                                              | Typical rating |
|----------------------------------------------------------|----------------|
| No tags                                                  | 1              |
| `boundary_too_tight` only                                | 2              |
| `boundary_too_loose` only                                | 2              |
| `csf_included` only (small)                              | 2              |
| `lesion_fragmented` only                                 | 2              |
| `wrong_hemisphere` (a few voxels)                        | 2              |
| `extracranial_included` (small)                          | 2              |
| `lesion_missed_partly`                                   | 3              |
| `false_positive_cluster` (large)                         | 3              |
| `multiple_lesions_one_missed`                            | 3              |
| `wrong_hemisphere` (large mirror)                        | 3              |
| `skull_strip_failed` or `registration_off`               | 3              |

> **Heuristic:** if every tag on the mask is a Boundary or
> Tissue-confusion tag, it's almost certainly a 2. If any Coverage,
> Topology (large-scale), or Pipeline tag is present, it's likely a 3.

---

## How tags map to fixes (typical first move)

| Tag                            | First thing to try                                       |
|--------------------------------|----------------------------------------------------------|
| `boundary_too_tight`           | Tier 1: lower threshold; or morph_close radius 1         |
| `boundary_too_loose`           | Tier 1: raise threshold; or morph_open radius 1          |
| `lesion_fragmented`            | Tier 1: morph_close 1–2, or keep_N_largest=1             |
| `false_positive_cluster`       | Tier 1: keep_N_largest=1; or hemisphere_clip if applicable |
| `csf_included`                 | Tier 1: morph_open + raise threshold                     |
| `extracranial_included`        | Tier 1: hemisphere_clip is usually unhelpful — Tier 2/3  |
| `wrong_hemisphere` (small)     | Tier 1: hemisphere_clip                                   |
| `wrong_hemisphere` (large)     | Tier 3: re-check registration; consider re-run with seed |
| `lesion_missed_partly`         | Tier 2: paint the missing area; or re-run with seed      |
| `multiple_lesions_one_missed`  | Tier 2: paint the missed lesion; or re-run with seed     |
| `skull_strip_failed`           | Re-run with corrected skull-strip; LINDA cannot recover  |
| `registration_off`             | Re-run with manual seed in native space                  |

---

## When in doubt

1. Pick the **smallest** rating that requires the most-extensive fix.
   (A mask with one boundary issue *and* a missed sub-region is a 3
   because of the missed sub-region.)
2. Apply at least one tag from the most-relevant **category** above
   for any mask that isn't a 1.
3. Use `notes` to describe anything unusual; the agent reading the
   sidecar later will see them.
