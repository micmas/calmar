---
schema_version: 2.7
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
kind: predictor
predictor_type: behavioural
short_definition: A measure of overall aphasia severity, typically using the Aphasia Quotient (AQ).
assessment:
- WAB-AQ
- WAB-R AQ
units: score 0-100
typical_range: 0-100 (lower = more severe)
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: A greater number of cumulative aphasia treatment hours significantly predicts improvement in
    aphasia severity in chronic stroke survivors.
  direction: likely
  relationship: correlational
  citation: '@Johnson2019'
  method: behavioral_only
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 39
    population: chronic left-hemisphere ischemic stroke
    time_post_onset: mean 38.0 months (range 6.0-224.0)
    phase: chronic
    age_range: mean 54.7 (SD 9.8)
    handedness: not_reported
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: p < .05
    effect_size: 0.07 points (WAB-AQ increase per hour)
    p_value: 0.03
  confounders_controlled:
  - age at stroke onset
  - age at WAB testing
  - sex
  - education
  - time poststroke of WAB testing
  - aphasia type
  - days of exercise per week poststroke
  - use of antidepressants
  - presence of diabetes
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioral-only predictor
  author_limitations:
  - The number of treatment hours only reflected hours received while participating in research studies
    in the authors' laboratory, likely underestimating total treatment.
  - The study used a convenience sample from an archival database.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 643
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 641
    quote: A greater number of aphasia treatment hours significantly predicted language improvement (p
      = .03)
    supports: claim
  - section: Participants
    page: 640
    quote: Thirty-nine individuals (13 women, 26 men) with a mean age of 54.7 years (SD = 9.8) at the
      time of stroke met the inclusion criteria.
    supports: sample
  - section: Statistical Analyses
    page: 641
    quote: To accommodate the variation between and within subjects, linear mixed-effects models (LMEs)
      were used to predict changes in WAB-AQ
    supports: method
  - section: Results
    page: 643
    quote: for every additional hour of aphasia treatment, WAB-AQ increased 0.07 points on average.
    supports: statistics
  - section: Limitations
    page: 646
    quote: the factor 'therapy hours' only reflected the number of treatment hours a participant received
      while participating in a research study in our laboratory.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
Johnson et al. (2019) found that cumulative treatment hours in the chronic phase are positively associated with improvements in WAB-AQ.
