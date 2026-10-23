---
schema_version: 2.6
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
kind: predictor
predictor_type: behavioural
short_definition: A general measure of aphasia severity or functional communication ability.
assessment:
- ASRS
- ScreeLing
units: score
typical_range: ASRS 0-5; ScreeLing 0-24 per component
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Initial severity of phonological impairment is the strongest linguistic predictor of good functional
    verbal communication outcome at 1 year post-stroke.
  direction: likely
  relationship: correlational
  citation: '@ElHachioui2013'
  method: behavioral_only
  design: longitudinal
  strength: strong
  evidence_quality: cohort
  instrument: ScreeLing (Phonology)
  score_band: baseline score
  interpretation: Higher initial phonology scores predict better 1-year functional outcome.
  sample:
    n: 130
    population: adult Dutch native/near-native speakers with aphasia due to a first-ever stroke
    time_post_onset: mean of 4 days (T1)
    phase: acute
    age_range: 19-96 years
    handedness: 86% right-handed
    language: Dutch
  statistics:
    threshold: p=0.003
    effect_size: OR 1.31 (95% CI 1.15 to 1.51)
    p_value: 0.003
  confounders_controlled:
  - age
  - Barthel Index score
  - educational level
  - stroke subtype
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Behavioural predictor based on ScreeLing phonology score.
  author_limitations:
  - The three core linguistic components were not examined extensively but with a screening tool.
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
    quote: In multivariable analysis, these variables explained 46.5% of the variance, with phonology
      being the only signiﬁcant predictor (p=0.003).
    supports: claim
  - section: Methods - Patients
    page: 310
    quote: Adult Dutch native/near-native speakers who could complete language tests between 2 and 14
      days after stroke were eligible for inclusion.
    supports: sample
  - section: Statistical analysis
    page: 312
    quote: The first step was to investigate the inﬂuence of the linguistic variables (ie, semantics,
      phonology and syntax scores) with univariable logistic regression analyses.
    supports: method
  - section: Table 2
    page: 313
    quote: Phonology score at T1... OR for good outcome (95% CI) 1.31 (1.15 to 1.51)
    supports: statistics
  - section: Discussion
    page: 313
    quote: First, we had to dichotomise our outcome variable because in the more severe categories of
      the ASRS we lacked adequate numbers of patients...
    supports: limitation
  - section: Discussion
    page: 313
    quote: Second, the three core linguistic components were not examined extensively but with a screening
      tool.
    supports: limitation
---
