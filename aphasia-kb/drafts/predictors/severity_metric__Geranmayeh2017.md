---
schema_version: 2.6
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
kind: predictor
predictor_type: behavioural
short_definition: A measure of overall aphasia severity or language performance.
assessment:
- in-scanner language measure (AICW)
- Comprehensive Aphasia Test (CAT)
units: raw score
typical_range: not_reported
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Initial language performance (measured by in-scanner AICW) is a significant predictor of language
    outcome at 4 months and language recovery over time.
  direction: likely
  relationship: correlational
  citation: '@Geranmayeh2017'
  method: behavioral_only
  design: longitudinal
  strength: strong
  evidence_quality: cohort
  instrument: in-scanner language measure (AICW)
  score_band: all severities
  interpretation: Initial performance serves as a baseline for predicting recovery trajectory.
  sample:
    n: 27
    population: left hemisphere stroke
    time_post_onset: ≈2 weeks
    phase: early_subacute
    age_range: 59 ± 11 years
    handedness: not_reported
    language: English
  statistics:
    threshold: P < 0.05
    effect_size: beta = 0.767 (outcome), beta = -0.813 (recovery)
    p_value: P = 0.002
  confounders_controlled:
  - lesion volume
  - age
  confounders_not_controlled: []
  author_limitations:
  - The early language performance... [is] a marker of initial aphasic stroke severity... in keeping with
    previous studies.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1952
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 6
    quote: Only early language measure performance (beta = 0.767, P = 0.002) and age (beta = -0.257, P
      = 0.047) were the overall significant predictors of language outcome at 4 months after stroke.
    supports: claim
  - section: Results
    page: 6
    quote: Again, only early language performance (beta = -0.813, P = 0.002) and age (beta = -0.306, P
      = 0.047) were the overall significant predictors of language recovery over time.
    supports: statistics
  - section: Participants
    page: 2
    quote: Twenty-seven participants were scanned at two time points; first in the early phase after the
      stroke [15 ± 7.6 days]
    supports: sample
  region_definition:
    kind: not_reported
---

Initial language performance is a robust predictor of both final outcome and the amount of recovery over time.
