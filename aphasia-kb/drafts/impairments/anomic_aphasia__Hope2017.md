---
schema_version: 2.7
id: anomic_aphasia
name: Anomic aphasia
kind: impairment
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
short_definition: Aphasia characterized by difficulty in word retrieval (naming).
findings:
- id: f1
  target: anomic_aphasia
  target_kind: impairment
  claim: Longitudinal changes in spoken object naming in chronic aphasia reflect changes in word-finding
    processes rather than articulatory changes.
  direction: likely
  relationship: correlational
  citation: '@Hope2017'
  method: behavioral_only
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 28
    population: right-handed left-hemisphere stroke patients
    time_post_onset: T1 > 1 year; mean T1 50.7 months, mean T2 80.4 months
    age_range: mean 51.7 years (SD 10.4)
    handedness: all right-handed
    language: English first language
    phase: longitudinal
    cohort: PLORAS
  statistics:
    threshold: P < 0.05
    effect_size: r = 0.71 (spoken object vs written object naming)
    p_value: '0.001'
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Behavioural dissociation between word-retrieval and articulation tasks.
  author_limitations:
  - The relationship between impairment-based measures and day-to-day experiences of language use might
    be complex.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1724
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 8
    quote: The results are, however, consistent with the change in spoken object naming scores being a
      consequence of changes in word finding abilities (lower during auditory repetition than spoken object
      naming, spoken action naming and written object naming).
    supports: claim
  - section: Materials and methods
    page: 3
    quote: 'Summary details of the 28 patients who met these criteria are as follows: 10 females; mean/standard
      deviation (SD) of age at stroke onset = 51.7/10.4 years; mean/SD of time post-stroke when assessed
      = (T1) 50.7/43.7 months; (T2) 80.4/53.5 months...'
    supports: sample
  - section: Results
    page: 1724
    quote: '...we found changes in the spoken object naming scores were significantly correlated with
      changes in: (i) written object naming scores (r = 0.71, P = 0.001); and (ii) spoken action naming
      scores (r = 0.67, P = 0.001)... In contrast, the correlation between spoken object naming and auditory
      repetition scores was not significant (r = 0.04, P = 0.83).'
    supports: statistics
  - section: Discussion
    page: 10
    quote: the relationship between our impairment-based measures of language skill, and the patients'
      day-to-day experiences of language use, might be complex.
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
---
# Anomic Aphasia

Findings from Hope et al. (2017) suggest that longitudinal changes in naming in chronic aphasia are driven by word-retrieval mechanisms.
