---
schema_version: 2.7
id: age
name: Age at stroke
kind: predictor
predictor_type: demographic
short_definition: The age of the patient at the time of stroke onset.
units: years
typical_range: not_reported
direction_of_severity: not_applicable
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Younger age is associated with a greater degree of language recovery following acute stroke.
  direction: likely
  relationship: correlational
  citation: '@Laska2001'
  method: behavioral_only
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 119
    population: acute stroke patients with aphasia
    time_post_onset: acute stage to 18 months
    phase: longitudinal
    age_range: mean 78.6 (consecutive group), range 34-99
    handedness: not_reported
    language: Swedish
    cohort: not_reported
  statistics:
    threshold: P < 0.01
    effect_size: not_reported
  confounders_controlled:
  - gender
  - severity of stroke
  - aetiology
  - previous stroke
  - type of aphasia
  - lesion side
  - lesion volume
  - fluency
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioral predictor
  author_limitations:
  - The study used a combination of different aphasia tests which may introduce variability.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 418
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 6
    quote: However, in a multivariate regression analysis including the above variables, only age showed
      a signi®cant relation (P < 0.01), i.e. the younger the patient, the higher the degree of recovery.
    supports: claim
  - section: Study design and patients
    page: 2
    quote: In this way, 106 consecutive, unselected patients with acute stroke were included. Among these,
      36 patients with aphasia were iden-tified. [...] another 83 aphasics were iden-tified, yielding
      a total of 119 aphasic patients.
    supports: sample
  - section: Statistical methods
    page: 3
    quote: For multivariate regression ana-lyses, multivariate analysis of variance was used.
    supports: method
  - section: Discussion
    page: 8
    quote: Our results show that younger patients had a higher recovery rate, which is in agreement with
      others.
    supports: claim
  - section: Discussion
    page: 8
    quote: A combination of different and adjusted aphasia tests provided the possibility to assess almost
      all acute aphasic patients.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
Finding f1 describes the longitudinal association between age and the degree of recovery (measured by ANELT) in a cohort of 119 acute aphasic patients.
