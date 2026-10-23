---
schema_version: 2.6
id: age
name: Age at stroke
kind: predictor
predictor_type: demographic
short_definition: The age of the patient at the time of stroke or assessment.
units: years
typical_range: not_reported
direction_of_severity: higher_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
findings:
- id: f1
  target: affective_receptive_aprosodia
  target_kind: impairment
  claim: Older age is an independent predictor of impairment in overall emotional prosody identification
    in acute right hemisphere stroke.
  direction: likely
  relationship: correlational
  citation: '@Sheppard2020'
  method: RLSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 23
    population: acute right hemisphere ischemic stroke
    time_post_onset: within 5 days of stroke
    phase: acute
    age_range: mean 55.09 years, SD 17.22
    handedness: all right-handed
    language: premorbid fluent speakers of English
  statistics:
    threshold: p < 0.05
    effect_size: p = 0.009
    p_value: 0.009
  confounders_controlled:
  - education
  - lesion volume
  - percent damage to ventral stream regions
  confounders_not_controlled: []
  author_limitations:
  - Small sample size for longitudinal follow-up.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page e1015
    confidence: high
    flags:
    - imaging_details.reference_space not extracted by the model — set to not_reported; verify against
      the paper
  source_passages:
  - section: Results
    page: 4
    quote: Individual predictors of overall emotion identification impairment were older age (p = 0.009)
      and greater damage to posterior STG (p = 0.038)
    supports: claim
  - section: Methods
    page: 2
    quote: We enrolled 23 patients (mean age 55.09 years, SD 17.22) with acute RH ischemic stroke... At
      the acute time point, 23 patients were tested within 5 days of stroke.
    supports: sample
  - section: Statistical analysis
    page: 3
    quote: 'Multivariable linear regression was used to identify the independent predictors of overall
      emotional prosody identification impairment... The following independent variables were entered
      into the initial model: percent damage to each of 7 regions of interest... overall lesion volume,
      age, and education.'
    supports: method
  - section: Results
    page: 4
    quote: The model for overall emotion identification was significant, F10,10 = 3.15, p = 0.043... Individual
      predictors of overall emotion identification impairment were older age (p = 0.009)
    supports: statistics
  - section: Discussion
    page: 5
    quote: The finding that older age was an individual predictor of impaired emotion identification was
      not surprising given that both pitch identification and emotion identification skills decline as
      individuals age even in neurologically unimpaired adults
    supports: claim
  - section: Discussion
    page: 6
    quote: There were a relatively small number of participants with longitudinal data at both the acute
      and chronic stages
    supports: limitation
  region_definition:
    kind: not_reported
  imaging_details:
    reference_space: not_reported
    atlases_used: []
---

Finding f1 identifies age as a demographic predictor of emotional prosody identification impairment.
