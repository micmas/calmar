---
schema_version: 2.7
id: time_post_onset
name: Time post-stroke onset
kind: predictor
predictor_type: clinical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
short_definition: Time elapsed since the stroke event.
units: months
findings:
- id: f1
  target: anomic_aphasia
  target_kind: impairment
  claim: Time post-stroke at first assessment does not predict the direction of language recovery or decline
    in chronic aphasia.
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
    cohort: PLORAS
  statistics:
    threshold: P < 0.05
    effect_size: t = 0.48
    p_value: '0.64'
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Time post-stroke at T1.
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
    quote: There were no significant differences between the 'improvers' and 'decliners' in terms of...
      time post-stroke at T1 (t = 0.48, P = 0.64) or T2 (t = 0.61, P = 0.55)...
    supports: claim
  - section: Materials and methods
    page: 3
    quote: 'Summary details of the 28 patients who met these criteria are as follows: 10 females; mean/standard
      deviation (SD) of age at stroke onset = 51.7/10.4 years...'
    supports: sample
  - section: Results
    page: 8
    quote: There were no significant differences between the 'improvers' and 'decliners' in terms of...
      time post-stroke at T1 (t = 0.48, P = 0.64) or T2 (t = 0.61, P = 0.55)...
    supports: statistics
  - section: Discussion
    page: 9
    quote: The distinction between improvers and decliners might reflect some more subtle (e.g. more multivariate)
      distinction between the patients...
    supports: limitation
  - section: added by backfill
    page: 2
    quote: Our patient data were extracted from our PLORAS database (Seghier et al., 2016)
    supports: sample
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
direction_of_severity: not_applicable
---
# Time Post Onset

Time post-stroke was not a significant predictor of the direction of language change in this chronic cohort.
