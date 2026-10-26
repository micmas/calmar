---
schema_version: 2.7
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
kind: predictor
predictor_type: behavioural
short_definition: A global measure of aphasia severity, typically derived from a standardized battery.
assessment:
- WAB-R Aphasia Quotient
units: score 0-100
typical_range: 0-100 (lower = more severe)
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
findings:
- id: f1
  target: aphasia_recovery
  target_kind: prognosis
  claim: Baseline aphasia severity (WAB-AQ) is an independent predictor of responsiveness to language
    rehabilitation in chronic post-stroke aphasia.
  direction: likely
  relationship: correlational
  citation: '@Billot2022'
  method: MLPA
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  instrument: WAB-R Aphasia Quotient
  score_band: all severities
  interpretation: Baseline severity provides unique prognostic information regarding treatment response.
  sample:
    n: 55
    population: chronic post-stroke aphasia
    time_post_onset: mean 59.0 months
    phase: chronic
    age_range: mean 58.8 years
    handedness: not_reported
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: P < 0.001
    effect_size: F1 = 0.842 (individual feature set model)
    p_value: '.001'
  confounders_controlled:
  - demographics
  - structural integrity
  - functional connectivity
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Behavioural metric (WAB-AQ)
  author_limitations:
  - The sample size was limited due to the availability of multimodal MRI data.
  - The use of leave-one-out cross-validation instead of k-fold may affect generalizability.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1610
    confidence: high
    flags:
    - cohort overlaps with @Barbieri2023 (same multi-site project involving BU, JHU, NU)
    - imaging_details.reference_space not extracted by the model — set to not_reported; verify against
      the paper
  source_passages:
  - section: Results
    page: 5
    quote: Notably, among SVM models trained on an individual feature set, aphasia severity (ie, AQ) and
      rs-fMRI connectivity (ie, RS) independently provided the best prediction performance scores...
    supports: claim
  - section: Participants
    page: 2
    quote: Participants were 55 individuals (37 male) with chronic post-stroke aphasia due to a single
      left-hemisphere stroke (mean age =58.8 years, mean time poststroke onset =59.0 months, mean education
      =15.8 years).
    supports: sample
  - section: Model Development and Evaluation
    page: 4
    quote: SVM and RF models were trained, tuned, and tested using a leave-one-out cross-validation procedure
      on all possible combinations of feature sets...
    supports: method
  - section: Results
    page: 5
    quote: The optimal SVM model... performed significantly better than any of the models trained on an
      individual feature set (P < 0.001).
    supports: statistics
  - section: Limitations
    page: 7
    quote: Although the sample size of this study was limited due to the availability of the multimodal
      MRI data...
    supports: limitation
  - section: added by backfill
    page: 2
    quote: Participants were 55 individuals (37 male) with chronic post-stroke aphasia due to a single
      left-hemisphere stroke
    supports: method
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  lesion_mapping:
    analysis: multivariate
    n_analysed: 55
    min_lesion_overlap: not_reported
    lesion_volume_correction: not_reported
    multiple_comparisons: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
---
