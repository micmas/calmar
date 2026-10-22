---
schema_version: 2.6
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
kind: predictor
predictor_type: behavioural
short_definition: A measure of the severity of language impairment.
assessment:
- neuropsychological tests (language domain)
units: z-score
typical_range: 0 = healthy (mean of controls)
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: The severity of acute impairment is a strong predictor of the amount of behavioural recovery
    across all domains, including language.
  direction: likely
  relationship: correlational
  citation: '@Ramsey2017'
  method: behavioral_only
  design: longitudinal
  evidence_quality: cohort
  strength: strong
  sample:
    n: 132
    population: first-time stroke patients with heterogeneous lesions
    time_post_onset: approximately two weeks after their stroke
    phase: longitudinal
    age_range: mean 54 (s.d. 11)
    handedness: not_reported
    language: not_reported
  statistics:
    threshold: P < 0.001
    effect_size: r ≈ 0.5–0.9
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioural-only finding
  author_limitations:
  - The behavioural battery was a trade-off between completeness and feasibility.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 2
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 2
    quote: In agreement with other studies, we found that the severity of acute impairment was highly
      predictive of the amount of behavioural recovery.
    supports: claim
  - section: Results
    page: 2
    quote: In each domain, the correlation between acute impairment and the change in impairment (chronic
      minus sub-acute) was high (correlation coefficient, r ≈ 0.5–0.9) and highly significant (P < 0.001)
    supports: statistics
  - section: Discussion
    page: 6
    quote: Another limitation is that the behavioural battery was a trade-off between completeness and
      feasibility.
    supports: limitation
---
