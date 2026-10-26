---
schema_version: 2.7
id: age
name: Age at stroke
aliases:
- age
- age at stroke
- age at onset
- patient age
kind: predictor
predictor_type: demographic
short_definition: Patient age in years at the time of the stroke event (or, if not
  reported, age at the imaging session).
units: years
typical_range: 30–85 yrs (most aphasia studies)
direction_of_severity: higher_is_worse
status: approved
reviewer: human:michele
reviewed_on: 2026-05-01
created_by: human:michele
created_on: 2026-05-01
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Older age at stroke onset is associated with long-term decline in aphasia
    severity in chronic stroke survivors.
  direction: unlikely
  relationship: correlational
  citation: '@Johnson2019'
  method: behavioral_only
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 39
    population: chronic left-hemisphere ischemic stroke
    time_post_onset: mean 38.0 months (range 6.0-224.0)
    phase: chronic
    age_range: mean 54.7 (SD 9.8)
    handedness: not_reported
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: p < .05
    effect_size: -1.51 points (WAB-AQ decrease per year)
    p_value: 0.04
  confounders_controlled:
  - sex
  - education
  - time poststroke of WAB testing
  - aphasia type
  - days of exercise per week poststroke
  - use of antidepressants
  - presence of diabetes
  - number of hours of participation in aphasia treatment studies
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioral-only predictor
  author_limitations:
  - The study used a convenience sample from an archival database.
  - Results should be interpreted with caution until replication with a larger sample.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 643
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 641
    quote: older stroke age was associated with long-term decline (p = .04).
    supports: claim
  - section: Participants
    page: 640
    quote: Thirty-nine individuals (13 women, 26 men) with a mean age of 54.7 years
      (SD = 9.8) at the time of stroke met the inclusion criteria.
    supports: sample
  - section: Statistical Analyses
    page: 641
    quote: To accommodate the variation between and within subjects, linear mixed-effects
      models (LMEs) were used to predict changes in WAB-AQ based on demographic information
    supports: method
  - section: Results
    page: 643
    quote: The results reveal that, for every year increase in age at stroke, WAB-AQ
      decreased by 1.51 points
    supports: statistics
  - section: Results
    page: 643
    quote: Although these group differences are not statistically significant, results
      should be interpreted with caution until replication with a larger sample of
      participants.
    supports: limitation
  review:
    reviewer: model:gemma4:26b
    reviewed_on: '2026-10-22'
    tier: A
    extractor: agent:ollama-extract-cli/gemma4:31b-it-q8_0
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
notes: Starter entry for schema v2.3. Age is one of the most consistent predictors
  of recovery, with younger patients typically showing better spontaneous recovery
  and stronger therapy response. The relationship is not strictly linear — children
  have markedly different recovery profiles (greater plasticity, different lesion-symptom
  relationships) and very young adults show recovery patterns distinct from older
  adults. Future findings should be careful about whether they're modelling age linearly
  or by cohort.
last_reviewed: '2026-10-22'
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
