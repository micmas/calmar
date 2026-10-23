---
schema_version: 2.6
id: age
name: Age at stroke
kind: predictor
predictor_type: demographic
short_definition: Age of the patient at the time of stroke.
units: years
typical_range: 18-100
direction_of_severity: higher_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Older age is an independent predictor of poorer functional verbal communication outcome at 1
    year post-stroke.
  direction: likely
  relationship: correlational
  citation: '@ElHachioui2013'
  method: behavioral_only
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 130
    population: adult Dutch native/near-native speakers with aphasia due to a first-ever stroke
    time_post_onset: mean of 4 days (T1)
    phase: acute
    age_range: 19-96 years
    handedness: 86% right-handed
    language: Dutch
  statistics:
    threshold: p <= 0.20 (univariable)
    effect_size: OR 0.94 (0.89 to 0.99)
    p_value: not_reported
  confounders_controlled:
  - phonology score
  - Barthel Index score
  - educational level
  - stroke subtype
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Demographic predictor (age).
  author_limitations:
  - Outcome variable was dichotomised due to lack of patients in severe categories.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 312; Table 2
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 312
    quote: Age, Barthel Index score, educational level and stroke subtype were the other signiﬁcant independent
      predictors with a p value ≤0.20 in univariable logistic regression analyses (table 2).
    supports: claim
  - section: Methods - Patients
    page: 310
    quote: Adult Dutch native/near-native speakers who could complete language tests between 2 and 14
      days after stroke were eligible for inclusion.
    supports: sample
  - section: Table 2
    page: 313
    quote: Age at T1 (19-96 years)... OR for good outcome (95% CI) 0.94 (0.89 to 0.99)
    supports: statistics
  - section: Discussion
    page: 313
    quote: First, we had to dichotomise our outcome variable because in the more severe categories of
      the ASRS we lacked adequate numbers of patients...
    supports: limitation
---
