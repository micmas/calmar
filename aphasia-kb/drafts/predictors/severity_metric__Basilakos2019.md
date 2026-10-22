---
schema_version: 2.3
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
kind: predictor
predictor_type: behavioural
short_definition: Overall aphasia severity as measured by a standardized battery.
assessment:
- WAB-R Aphasia Quotient
units: score 0-100
typical_range: 0-100 (lower = more severe)
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-19
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Higher initial aphasia severity (higher WAB-AQ) predicts a greater decline in language abilities
    over time in chronic aphasia.
  direction: likely
  relationship: correlational
  citation: '@Basilakos2019'
  method: behavioral_only
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 35
    population: chronic left-hemisphere stroke
    time_post_onset: mean 36.3 +/- 40.8 months at initial evaluation
    age_range: mean 55.8 +/- 9.1 years
    handedness: premorbidly right-handed
    language: not_reported
    phase: chronic
  statistics:
    threshold: P < .05
    effect_size: t = -2.6, P = .014
    p_value: 0.014
  confounders_controlled:
  - leukoaraiosis severity
  - stroke age
  - time post-stroke at follow-up assessment
  confounders_not_controlled:
  - diabetes
  - atherosclerotic disease
  - hypertension
  - age
  - external treatment
  instrument: WAB-AQ
  score_band: all severities
  interpretation: Overall aphasia severity
  region_definition:
    kind: not_reported
    description: Behavioural-only predictor finding based on initial WAB-AQ score.
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  author_limitations:
  - The sample size was relatively small.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 7
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2018, @Yourganov2015Predicting (USC/MUSC Aphasia Lab)
  source_passages:
  - section: Results
    page: 7
    quote: higher initial AQ scores... predicted decline in AQ at follow-up
    supports: claim
  - section: Results
    page: 7
    quote: for every 1-unit increase in initial AQ, follow-up AQ decreased by 0.22 (t = -2.6, P = .014).
    supports: statistics
  - section: Materials and Methods - Participants
    page: 2
    quote: 'N = 35 participants (9 females; age at stroke: M = 55.5 +/- 10 years, range = 31-71 years)
      in the chronic stage of recovery after a single-event left hemisphere stroke'
    supports: sample
  - section: Materials and Methods - Statistical Methods
    page: 6
    quote: Initial AQ was also used as a predictor in this analysis, alongside stroke age and time post-stroke
      at follow-up assessment
    supports: method
  - section: Limitations
    page: 10
    quote: First, the sample size was relatively small
    supports: limitation
---
# Findings on the predictive value of initial aphasia severity for long-term decline.
