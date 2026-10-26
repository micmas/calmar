# Sample-applicability warning fields

Status: proposal only. No aphasia-KB schema, validator, or entry is changed.
Maintainer approval is required before implementation.

## Goal

Extend the existing recovery-stage mismatch marker so each finding can also be
compared with the participant on stroke history, lesion laterality, imaging
modality, and age. These are applicability cautions, not exclusion rules and
not participant-level predictions.

## Proposed normalized sample fields

Add optional fields under each finding's `sample` block while retaining the
existing free-text fields for provenance:

| Field | Proposed values | Reason |
|---|---|---|
| `stroke_history` | `first_ever`, `recurrent`, `mixed`, `not_reported` | Separates explicitly first-ever cohorts from recurrent-stroke cohorts. “Mixed” means both were included; it must not be inferred from silence. |
| `lesion_laterality` | `left_unilateral`, `right_unilateral`, `unilateral_both_sides`, `bilateral`, `mixed`, `not_reported` | Distinguishes a cohort restricted to one hemisphere, unilateral cohorts containing both sides, explicitly bilateral cohorts, and samples containing both unilateral and bilateral cases. |
| `imaging_modalities` | list drawn from `T1`, `T2`, `FLAIR`, `DWI`, `ADC`, `DTI`, `fMRI`, `NCCT`, `CTA`, `CTP`, `PET`, `none`, `other`, `not_reported` | A list is needed because many studies are multimodal. This should describe imaging used for the finding, not every scan acquired. |
| `age_years` | object with optional numeric `min`, `max`, `mean`, `sd` plus `basis` = `range`, `summary_only`, or `not_reported` | Makes overlap checks possible without parsing prose such as “mean 75.4 (SD 11.0)”. A mean/SD must not be converted into a fabricated range. |

The current `sample.age_range` and `imaging_details.modalities` should remain
unchanged until migration is approved. A migration tool could prefill proposed
values only when text is unambiguous, mark their source as stated/inferred, and
send inferred records for review.

## Participant-side fields

The report needs explicit participant values from `participants.tsv` or route
metadata:

- `stroke_history`: `first_ever`, `recurrent`, or missing;
- `lesion_laterality`: computed from the reviewed lesion mask as left, right,
  bilateral, or missing, with a documented midline rule;
- `imaging_modality`: the actual lesion-defining modality (`T1`, `DWI/ADC`,
  `NCCT`, etc.), not merely every available scan; and
- `age_at_stroke`: already supported, with missing preserved.

## Warning logic

- Show **applicability matches** and **mismatches** separately; unknown study or
  participant data remain “not stated”, never a mismatch.
- First-ever versus recurrent and unilateral versus bilateral are exact
  comparisons. A `mixed` study sample is broad/uncertain, not an exact match.
- Modality mismatch is shown when the finding's lesion analysis used a
  different modality family. Multimodal findings match when the participant's
  modality is included but should still name the other modalities.
- Age matches only when a stated min/max contains the participant's age. A
  summary-only mean/SD supports descriptive context but no in/out-of-range
  judgement.
- Do not filter findings by default. Add concise indicators to each finding and
  a section summary analogous to the recovery-stage summary.

## Approval questions

1. Should these fields live directly in `sample`, or in a nested
   `sample.applicability` object to keep schema growth contained?
2. Should `imaging_modalities` duplicate normalized information from
   `imaging_details.modalities`, or should the latter become the single source?
3. Is lesion laterality best represented as one categorical field or as
   explicit inclusion flags for left-unilateral, right-unilateral, and
   bilateral cases?
4. Should inferred legacy values be reportable immediately with a visible
   provenance flag, or hidden until human review?
