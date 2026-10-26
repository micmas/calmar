---
schema_version: 2.7
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
kind: predictor
predictor_type: behavioural
short_definition: A general measure of aphasia severity or specific phonological ability.
assessment:
- Phonological Composite (PC) score
units: percent correct
typical_range: 0-100%
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
findings:
- id: f1
  target: phonological_dyslexia
  target_kind: impairment
  claim: General phonological ability (PC score) is a strong predictor of reading accuracy in patients
    with perisylvian lesions.
  direction: likely
  relationship: correlational
  citation: '@Rapcsak2009'
  method: behavioral_only
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  instrument: Phonological Composite (PC) score
  score_band: all severities
  interpretation: Higher general phonological ability correlates with better reading accuracy.
  sample:
    n: 22
    population: perisylvian patients who completed the full phonological battery
    time_post_onset: subacute or chronic stage
    age_range: 40-78 years
    handedness: not_reported
    language: not_reported
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: one-tailed p-value
    effect_size: R^2 = 66.9%
    p_value: <.0001
  confounders_controlled: []
  confounders_not_controlled: []
  author_limitations:
  - Retrospective nature of the investigation; not all participants completed all tasks.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 583
    confidence: high
    flags:
    - target_id phonological_dyslexia is forward-looking
  source_passages:
  - section: Results
    page: 9
    quote: Overall, PC scores proved to be powerful predictors of written language performance, accounting
      for 66.9% of the variance in reading accuracy [F(1,20) = 40.397, p < .0001]
    supports: claim
  - section: Methods
    page: 4
    quote: a subset of 25 patients and 17 controls were evaluated with a phonological battery... Percent
      correct performance on all six subtests of the phonological battery was computed individually and
      then averaged to derive a phonological composite (PC) score
    supports: method
  - section: Discussion
    page: 588
    quote: Due to the retrospective nature of this investigation, we were unable to ensure that all participants
      receive testing with the same materials or that they complete all relevant language tasks
    supports: limitation
  region_definition:
    kind: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
