---
schema_version: 2.7
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
kind: predictor
predictor_type: behavioural
short_definition: Overall measure of aphasia severity.
assessment:
- Western Aphasia Battery-Revised Aphasia Quotient
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Higher pretreatment linguistic cognitive function (including WAB-R subscales) significantly predicts
    higher potential maximal gain (PMG) after language therapy.
  direction: likely
  relationship: correlational
  citation: '@Gilmore2019'
  method: behavioral_only
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  instrument: WAB-R
  score_band: all severities
  interpretation: Higher baseline linguistic ability correlates with better therapy outcomes.
  sample:
    n: 67
    population: persons with poststroke aphasia
    time_post_onset: mean 53.58 months (SD 47.78)
    phase: chronic
    age_range: mean 60.90 (SD 12.55)
    handedness: not_reported
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: P < .01
    effect_size: b = .49
    p_value: '.01'
  confounders_controlled:
  - age
  - treatment type
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Behavioural predictor; no specific brain region targeted.
  author_limitations:
  - ' The findings may have been affected by sample size (ie, under-powered principal components analyses),
    especially in study 2 (n=27).'
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results - Study 1, page 3
    confidence: high
    flags: []
  source_passages:
  - section: Results - Study 1
    page: 3
    quote: The linguistic (b=.49, standard error [SE]=.16, t=3.08, P<.01) and the nonlinguistic cognitive
      components (b=.42, SE=.10, t=4.07, P<.001) were both significant
    supports: claim
  - section: Methods - Study 1
    page: 2
    quote: Sixty-seven persons with poststroke aphasia (44 men; mean age=60.90; mean months post onset=53.58)
      were included in this study
    supports: sample
  - section: Results - Study 1
    page: 3
    quote: backward elimination linear regression with age and treatment type (ie, naming or sentence
      comprehension).
    supports: confounders
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
units: varies by instrument — see `instrument` field on each finding
direction_of_severity: lower_is_worse
---
