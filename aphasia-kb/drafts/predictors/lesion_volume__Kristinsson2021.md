---
schema_version: 2.7
id: lesion_volume
name: Total lesion volume
kind: predictor
predictor_type: imaging_metric
short_definition: The total volume of brain tissue damaged by stroke, typically measured in cubic centimeters
  (cm3).
units: cm3
typical_range: 2.09–472.38 cm3
direction_of_severity: higher_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Total lesion volume is significantly associated with overall aphasia severity and specific language
    functions in chronic stroke.
  direction: likely
  relationship: causal
  citation: '@Kristinsson2021'
  method: behavioral_only
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 116
    population: chronic left-hemisphere stroke
    time_post_onset: 'mean 39.4 months (range: 5.6–237.1 months)'
    age_range: 'mean 58.5 ± 10.9 years (range: 29–81 years)'
    handedness: not_reported
    language: not_reported
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: p < .001
    effect_size: 'WAB-AQ estimate: −0.184'
    p_value: < 2E−16
  confounders_controlled:
  - sex
  - age
  - time post-stroke
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Global lesion volume calculation
  author_limitations:
  - The study did not validate the prediction accuracy of the models in an independent sample.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, Table 4
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 10
    quote: The only significant association was found between lesion volume and all language measures
      (all p-values <.001).
    supports: claim
  - section: Method
    page: 1
    quote: a total of 116 participants were included for data analysis.
    supports: sample
  - section: Method
    page: 3
    quote: 'The mean sample age was 58.5 ± 10.9 years (range: 29–81 years)... and mean time poststroke
      was 39.4 months (range: 5.6–237.1 months).'
    supports: sample
  - section: Results
    page: 10
    quote: Table 4
    supports: statistics
  - section: Discussion
    page: 14
    quote: Last, we did not validate the prediction accuracy of our models in an independent sample of
      persons with aphasia.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
