---
schema_version: 2.3
id: lesion_volume
name: "Total lesion volume"
aliases:
  - lesion volume
  - lesion size
  - infarct volume
  - total infarct volume
kind: predictor
predictor_type: imaging_metric
short_definition: >-
  Total volume of structural damage on the patient's lesion mask, typically
  reported in millilitres (cubic centimetres) of T1- or FLAIR-defined tissue
  loss.
units: "ml (cc)"
typical_range: "<1 ml (lacunar) to >300 ml (large MCA territory)"
direction_of_severity: higher_is_worse
status: approved
reviewer: human:michele
reviewed_on: 2026-05-01
created_by: human:michele
created_on: 2026-05-01
findings: []
notes: >-
  Starter entry for schema v2.3. Lesion volume is the single most-controlled-for
  covariate in lesion-symptom mapping. Findings here should be reserved for
  *predictive* claims (volume → severity / recovery / therapy response), not
  the trivial "bigger lesion = more damage" tautology. Be careful to track
  whether a paper measures volume in native or MNI space — ratios change
  with normalisation.
---

# Total lesion volume

Total lesion volume is the simplest possible imaging metric and one of
the most robust predictors of aphasia outcome — but it is also the one
most prone to acting as a confound rather than a signal. A useful
finding here is one where volume is shown to predict an outcome
*independently of* lesion location, or one where the predictive
validity of a regional finding holds *after controlling for* total
volume.

Common pitfalls to flag in the `provenance.flags` of any finding under
this entry:

- Volume measured in native vs. normalised space (MNI volumes are
  systematically larger after warping)
- Acute vs. chronic measurement (acute oedema inflates apparent
  volume; chronic atrophy can shrink it)
- Whether white-matter hyperintensities, microbleeds, or old strokes
  are included or excluded
- The threshold used to binarise the lesion (manual tracing vs.
  intensity threshold vs. atlas-based segmentation)
