---
schema_version: 2.3
id: lesion_volume
name: Total lesion volume
kind: predictor
predictor_type: imaging_metric
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
short_definition: Total volume of the brain lesion.
units: cm3
findings:
- id: f1
  target: anomic_aphasia
  target_kind: impairment
  claim: Lesion volume does not predict the direction of language recovery or decline in chronic aphasia.
  direction: no_effect
  relationship: correlational
  citation: '@Hope2017'
  method: behavioral_only
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 28
    population: right-handed left-hemisphere stroke patients
    time_post_onset: T1 > 1 year
    age_range: mean 51.7 years
    handedness: all right-handed
    language: English
    phase: chronic
  statistics:
    threshold: P < 0.05
    effect_size: t = 0.40
    p_value: '0.69'
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Global lesion volume.
  author_limitations:
  - The distinction between improvers and decliners might reflect subtle multivariate distinctions or
    variable patterns of everyday language use.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1725
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 8
    quote: There were no significant differences between the 'improvers' and 'decliners' in terms of age
      at stroke onset (t = 0.86, df = 22, P = 0.40), time post-stroke at T1 (t = 0.48, P = 0.64) or T2
      (t = 0.61, P = 0.55), or lesion volume (t = 0.40, P = 0.69)...
    supports: claim
  - section: Materials and methods
    page: 3
    quote: 'Summary details of the 28 patients who met these criteria are as follows: 10 females; mean/standard
      deviation (SD) of age at stroke onset = 51.7/10.4 years...'
    supports: sample
  - section: Results
    page: 8
    quote: There were no significant differences between the 'improvers' and 'decliners' in terms of...
      lesion volume (t = 0.40, P = 0.69)...
    supports: statistics
  - section: Discussion
    page: 9
    quote: The distinction between improvers and decliners might reflect some more subtle (e.g. more multivariate)
      distinction between the patients...
    supports: limitation
direction_of_severity: higher_is_worse
---
# Lesion Volume

Lesion volume was not found to be a significant predictor of the direction of language change in this chronic cohort.
