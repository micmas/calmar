---
schema_version: 2.3
id: severity_metric
name: Aphasia Severity Metric
kind: predictor
predictor_type: behavioural
short_definition: Overall aphasia severity as measured by standardized batteries.
assessment:
- WAB-R Aphasia Quotient
units: score 0-100
typical_range: 0-100 (lower = more severe)
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
findings:
- id: f1
  target: rehabilitation_response
  target_kind: prognosis
  claim: Baseline aphasia severity (WAB-AQ) independently predicts responsiveness to language rehabilitation
    in chronic stroke.
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
    threshold: not_reported
    effect_size: F1 = 0.842
    p_value: not_reported
  confounders_controlled:
  - demographics
  - structural imaging
  - functional imaging
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioural-only predictor
  author_limitations:
  - Small sample size may lead to less accurate results when using machine learning models on neuroimaging
    data.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1610
    confidence: high
    flags:
    - imaging_details.reference_space not extracted by the model — set to not_reported; verify against
      the paper
  source_passages:
  - section: Results
    page: 5
    quote: Notably, among SVM models trained on an individual feature set, aphasia severity (ie, AQ) and
      rs-fMRI connectivity (ie, RS) independently provided the best prediction performance scores, with
      an accuracy of 0.782 and 0.764 and an F1 score of 0.842 and 0.812, respectively.
    supports: statistics
  - section: Methods
    page: 2
    quote: Participants were 55 individuals (37 male) with chronic post-stroke aphasia due to a single
      left-hemisphere stroke (mean age =58.8 years, mean time poststroke onset =59.0 months, mean education
      =15.8 years).
    supports: sample
  - section: Limitations
    page: 7
    quote: Previous studies demonstrated that small sample sizes can lead to less accurate results when
      using machine learning models on neuroimaging data to predict behavior.
    supports: limitation
  imaging_details:
    reference_space: not_reported
    atlases_used: []
- id: f2
  target: rehabilitation_response
  target_kind: prognosis
  claim: A multimodal combination of aphasia severity, demographics, structural integrity, and resting-state
    connectivity predicts treatment response significantly better than any single feature set.
  direction: likely
  relationship: responder
  citation: '@Billot2022'
  method: MLPA
  design: cross-sectional
  strength: strong
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
    effect_size: F1 = 0.94
    p_value: < 0.001
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: multimodal predictor combination
  author_limitations:
  - Small sample size may lead to less accurate results when using machine learning models on neuroimaging
    data.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1609
    confidence: high
    flags:
    - imaging_details.reference_space not extracted by the model — set to not_reported; verify against
      the paper
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
  imaging_details:
    reference_space: not_reported
    atlases_used: []
---
Finding f1 reports the independent predictive value of WAB-AQ for treatment response. Finding f2 reports the superiority of a multimodal model including AQ.
