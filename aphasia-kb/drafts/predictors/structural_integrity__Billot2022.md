---
schema_version: 2.3
id: structural_integrity
name: Brain Structural Integrity
kind: predictor
predictor_type: imaging_metric
short_definition: Measures of anatomic integrity including percentage of spared gray/white matter and
  fractional anisotropy.
units: percentage / FA value
typical_range: not_reported
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
findings:
- id: f1
  target: rehabilitation_response
  target_kind: prognosis
  claim: Structural integrity (fractional anisotropy and percentage of spared gray matter) contributes
    to the optimal prediction of responsiveness to language rehabilitation.
  direction: likely
  relationship: responder
  citation: '@Billot2022'
  method: MLPA
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 55
    population: chronic left-hemisphere stroke aphasia
    time_post_onset: mean 59.0 months
    age_range: mean 58.8 years
    handedness: not_reported
    language: not_reported
    phase: chronic
  statistics:
    threshold: P < 0.001
    effect_size: Multimodal F1 = 0.94
    p_value: < 0.001
  confounders_controlled:
  - demographics
  - behavioral scores
  - functional imaging
  confounders_not_controlled: []
  region_definition:
    kind: atlas
    description: Percentage spared in 69 AAL gray matter regions and 36 BCBToolKit white matter tracts.
  imaging_details:
    field_strength: 3T
    reference_space: MNI152
    atlases_used:
    - AAL
    - BCBToolKit
    preprocessing_pipeline: ADPP + Automated Fiber Quantification
  author_limitations:
  - Small sample size may lead to less accurate results when using machine learning models on neuroimaging
    data.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1609
    confidence: high
    flags:
    - target_id rehabilitation_response is forward-looking
  source_passages:
  - section: Results
    page: 1
    quote: The best prediction performance was achieved by a support vector machine model trained on aphasia
      severity, demographics, measures of anatomic integrity and resting-state functional connectivity
      (F1=0.94).
    supports: claim
  - section: Results
    page: 1
    quote: This model resulted in a significantly superior prediction performance compared with support
      vector machine models trained on all feature sets (F1=0.82, P<0.001) or a single feature set (F1
      range=0.68-0.84, P<0.001).
    supports: statistics
  - section: Limitations
    page: 7
    quote: Previous studies demonstrated that small sample sizes can lead to less accurate results when
      using machine learning models on neuroimaging data to predict behavior.
    supports: limitation
---
Finding f1 describes the role of structural integrity (FA and spared tissue) as a component of the optimal multimodal prediction model.
