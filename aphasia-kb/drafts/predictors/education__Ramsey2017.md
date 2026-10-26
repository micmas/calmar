---
schema_version: 2.7
id: education
name: Education
kind: predictor
predictor_type: demographic
short_definition: Number of years of formal education.
units: years
typical_range: not_reported
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Higher levels of education predict better chronic language outcomes, even after accounting for
    initial deficit severity.
  direction: likely
  relationship: correlational
  citation: '@Ramsey2017'
  method: behavioral_only
  design: longitudinal
  evidence_quality: cohort
  strength: moderate
  sample:
    n: 132
    population: first-time stroke patients with heterogeneous lesions
    time_post_onset: approximately two weeks after their stroke
    phase: longitudinal
    age_range: mean 54 (s.d. 11)
    handedness: not_reported
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: P < 0.005
    effect_size: beta = 0.182
  confounders_controlled:
  - sub-acute score
  - lesion size
  - age
  - therapy
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioural-only finding
  author_limitations:
  - The behavioural battery was a trade-off between completeness and feasibility.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 3
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 3
    quote: Additionally, lesion size and education were predictors of chronic language scores
    supports: claim
  - section: Table 2
    page: 6
    quote: Education (yr) 0.182**
    supports: statistics
  - section: Discussion
    page: 6
    quote: Another limitation is that the behavioural battery was a trade-off between completeness and
      feasibility.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
