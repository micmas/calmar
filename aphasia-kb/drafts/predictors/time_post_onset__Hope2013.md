---
schema_version: 2.6
id: time_post_onset
name: Time post-stroke onset
kind: predictor
predictor_type: clinical
short_definition: The duration of time elapsed since the onset of the stroke.
units: months
typical_range: not_reported
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Time post-stroke is the most significant single predictor of speech production recovery when
    combined with lesion damage.
  direction: likely
  relationship: correlational
  citation: '@Hope2013'
  method: MLPA
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 270
    population: stroke patients
    time_post_onset: from less than a month to more than 30 years
    phase: mixed
    age_range: 20 to 90 years
    handedness: not_reported
    language: English
  statistics:
    threshold: p < 0.001
    effect_size: R2 = 0.59
  confounders_controlled:
  - lesion volume
  - lesion site (35 regions)
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Temporal variable representing time since stroke.
  imaging_details:
    reference_space: MNI152
    atlases_used: []
  author_limitations:
  - The system systematically under-estimates the severity of impairments for the most impaired patients.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, Section 3.5
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 5
    quote: The best subset included 37 relevant predictors (R2 = 0.59, F = 38.38, p < 0.001), including
      time post-stroke (the most significant, single predictor)
    supports: claim
  - section: Method
    page: 2
    quote: This selection process left us with data from 270 patients
    supports: sample
  - section: Discussion
    page: 8
    quote: our preferred predictor configuration systematically under-estimates the severity of the impairments
      suffered by the most impaired patients
    supports: limitation
---
