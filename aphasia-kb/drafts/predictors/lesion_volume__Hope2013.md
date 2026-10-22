---
schema_version: 2.6
id: lesion_volume
name: Total lesion volume
kind: predictor
predictor_type: imaging_metric
short_definition: The total volume of brain tissue damaged by a stroke, typically measured in voxels or
  milliliters.
units: voxels
typical_range: not_reported
direction_of_severity: higher_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Total lesion volume, combined with demographic data, significantly improves the prediction of
    speech production scores in stroke patients.
  direction: likely
  relationship: correlational
  citation: '@Hope2013'
  method: MLPA
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 270
    population: stroke patients
    time_post_onset: from less than a month to more than 30 years
    phase: mixed
    age_range: 20 to 90 years (mean = 61.27; SD = 12.21)
    handedness: 242 right handed
    language: English as a first language
  statistics:
    threshold: p < 0.001
    effect_size: R2 = 0.35
  confounders_controlled:
  - time elapsed since stroke
  - age at stroke
  - handedness
  - gender
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Total number of lesioned voxels across the brain.
  imaging_details:
    field_strength: 1.5T or 3T
    preprocessing_pipeline: SPM unified segmentation optimized for focal brain lesions
    reference_space: MNI152
    atlases_used: []
  author_limitations:
  - The system systematically under-estimates the severity of impairments for the most impaired patients.
  - Pooling scans from acute and chronic phases may introduce noise due to lesion evolution.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, Section 3.2
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 4
    quote: As expected, access to this kind of information (alongside the demographic predictors used
      previously) did improve the predictions (R2 = 0.35, F = 144.73, p < 0.001)
    supports: claim
  - section: Method
    page: 2
    quote: This selection process left us with data from 270 patients
    supports: sample
  - section: Method
    page: 3
    quote: We employed GPR to learn the associations between predictors (patient demographic and lesion
      data), and output (speech production scores)
    supports: method
  - section: Discussion
    page: 8
    quote: our preferred predictor configuration systematically under-estimates the severity of the impairments
      suffered by the most impaired patients
    supports: limitation
  - section: Discussion
    page: 8
    quote: One criticism of the system described here is that it pools scans taken both soon after stroke
      (within the first month), and many years later (30 years or more).
    supports: limitation
---
