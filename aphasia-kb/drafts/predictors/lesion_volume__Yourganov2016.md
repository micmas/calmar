---
schema_version: 2.3
id: lesion_volume
name: Total lesion volume
kind: predictor
predictor_type: imaging_metric
short_definition: The total volume of the stroke lesion measured in voxels.
units: voxels
typical_range: not_reported
direction_of_severity: higher_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Overall lesion size is a significant predictor of WAB scores, including fluency, auditory comprehension,
    repetition, naming, and the aphasia quotient.
  direction: likely
  relationship: correlational
  citation: '@Yourganov2016'
  method: behavioral_only
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 90
    population: chronic left-hemisphere stroke aphasia
    time_post_onset: mean 42.8 months
    age_range: mean 58.8 years
    handedness: not_reported
    language: not_reported
    phase: chronic
  statistics:
    threshold: p < 0.000005
    effect_size: r = 0.5698 to 0.6971
  confounders_controlled: []
  confounders_not_controlled: []
  author_limitations: []
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 5
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 4
    quote: The accuracy of predicting WAB scores from the lesion size was significantly better than chance,
      as demonstrated in Table 3.
    supports: claim
  - section: Results
    page: 5
    quote: This table lists Pearson's correlation coefficient between actual and predicted WAB scores
      (fluency, auditory comprehension, repetition, naming, and AQ) and the associated p value.
    supports: statistics
  region_definition:
    kind: not_reported
---
Findings from Yourganov 2016 regarding the predictive value of total lesion volume.
