---
schema_version: 2.3
id: age
name: "Age at stroke"
aliases:
  - age
  - age at stroke
  - age at onset
  - patient age
kind: predictor
predictor_type: demographic
short_definition: >-
  Patient age in years at the time of the stroke event (or, if not reported,
  age at the imaging session).
units: "years"
typical_range: "30–85 yrs (most aphasia studies)"
direction_of_severity: higher_is_worse
status: approved
reviewer: human:michele
reviewed_on: 2026-05-01
created_by: human:michele
created_on: 2026-05-01
findings: []
notes: >-
  Starter entry for schema v2.3. Age is one of the most consistent predictors
  of recovery, with younger patients typically showing better spontaneous
  recovery and stronger therapy response. The relationship is not strictly
  linear — children have markedly different recovery profiles (greater
  plasticity, different lesion-symptom relationships) and very young adults
  show recovery patterns distinct from older adults. Future findings should
  be careful about whether they're modelling age linearly or by cohort.
---

# Age at stroke

Age at stroke (sometimes reported as age at imaging or age at therapy)
is one of the most universally reported demographic variables in the
aphasia literature. It is consistently associated with both severity
and recovery, but the direction and shape of the relationship depends
on what is being predicted and on the age range sampled.

When linking a paper to this predictor, check whether age was treated as:

- a continuous variable (linear effect)
- a binary split (e.g. <65 vs ≥65)
- an interaction term (e.g. age × therapy intensity)
- a control variable only (no main-effect estimate reported)

Studies of paediatric aphasia and post-stroke aphasia in the very
elderly (>85) have meaningfully different findings and should typically
be flagged in `provenance.flags`.
