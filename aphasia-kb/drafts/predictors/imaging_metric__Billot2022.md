---
schema_version: 2.7
id: imaging_metric_rsfc
name: Resting-State Functional Connectivity
kind: predictor
predictor_type: imaging_metric
short_definition: Bivariate Fisher-transformed Pearson correlations between anatomic regions of interest
  during resting state.
units: Fisher-z correlation
typical_range: not_reported
direction_of_severity: not_applicable
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
findings:
- id: f1
  target: aphasia_recovery
  target_kind: prognosis
  claim: Resting-state functional connectivity (rs-fMRI) is a particularly strong independent predictor
    of responsiveness to language treatment in chronic aphasia.
  direction: likely
  relationship: correlational
  citation: '@Billot2022'
  method: MLPA
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
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
    effect_size: F1 = 0.812 (individual SVM model); F1 = 0.87 (best RF model)
    p_value: '.001'
  confounders_controlled:
  - aphasia severity
  - demographics
  - structural integrity
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Bivariate correlations between 50 bilateral AAL3 ROIs.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: fMRI
      sequence: gradient-echo T2*-weighted
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3
    preprocessing_pipeline: fMRIPrep version 1.4.1 + CONN toolbox
    reference_space: MNI152
    atlases_used:
    - Automated Anatomical Labeling atlas 3
  author_limitations:
  - The sample size was limited due to the availability of the multimodal MRI data.
  - The use of leave-one-out cross-validation instead of k-fold may affect generalizability.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1610
    confidence: high
    flags:
    - cohort overlaps with @Barbieri2023 (same multi-site project involving BU, JHU, NU)
  source_passages:
  - section: Conclusions
    page: 1
    quote: functional connectivity of the brain at rest after stroke is a particularly important predictor
      of responsiveness to treatment, both alone and combined with other patient-related factors.
    supports: claim
  - section: Results
    page: 5
    quote: Notably, among SVM models trained on an individual feature set, aphasia severity (ie, AQ) and
      rs-fMRI connectivity (ie, RS) independently provided the best prediction performance scores...
    supports: statistics
  - section: MRI Data Preprocessing
    page: 3
    quote: resting-state functional MRI (rs-fMRI) connectivity, involving the rs-fMRI data first preprocessed
      in fMRIPrep version 1.4.1... and then through the CONN toolbox to extract bivariate Fisher-transformed
      Pearson correlations between 50 bilateral anatomic regions of interest specified using the Automated
      Anatomical Labeling atlas 3...
    supports: imaging_details
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
