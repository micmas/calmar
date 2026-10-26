---
schema_version: 2.7
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
kind: predictor
predictor_type: behavioural
short_definition: A quantitative measure of overall aphasia severity, typically using the Aphasia Quotient
  (AQ).
assessment:
- WAB-AQ
- WAB-R AQ
units: score 0–100
typical_range: 0–100 (lower = more severe)
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: A multimodal neuroimaging model (combining fMRI, FA, CBF, and lesion-load) predicts aphasia severity
    (WAB-AQ) more accurately than any single-modality model or lesion volume alone.
  direction: likely
  relationship: correlational
  citation: '@Kristinsson2021'
  method: MLPA
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 116
    population: chronic left-hemisphere stroke
    time_post_onset: mean 39.4 months
    age_range: mean 58.5 ± 10.9 years
    handedness: not_reported
    language: not_reported
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: p < .05
    effect_size: r = .67 (multimodal) vs .20–.58 (single-modality)
    p_value: <.001–.022
  confounders_controlled:
  - sex
  - age
  - time post-stroke
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Multimodal features preselected via univariate regression across 150 AALCTS ROIs.
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - AALCTS
    modalities:
    - modality: fMRI
      sequence: T2* EPI
      voxel_size_mm:
      - 3.25
      - 3.25
      - 3.2
      TR_ms: 10000
      TE_ms: 30
      volumes: 60
    - modality: DTI
      sequence: Bipolar/Monopolar
      voxel_size_mm:
      - 2.0
      - 2.0
      - 2.0
    - modality: ASL
      sequence: PASL/pCASL
  author_limitations:
  - The study did not validate the prediction accuracy of the models in an independent sample.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, Table 6
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2018, @Yourganov2015Predicting (USC/MUSC Aphasia Lab); flag for
      downstream double-counting risk in interpret_overlap().
  source_passages:
  - section: Results
    page: 11
    quote: 'The multimodal prediction model was more accurate than any single-modality model in predicting
      all six language measures (Figure 2): WAB-AQ (r = .67; single-modality models: .20–.58; Figure 3)'
    supports: claim
  - section: Results
    page: 12
    quote: 'the multimodal prediction model was significantly more accurate than any single-modality and
      the lesion-volume model in predicting WAB-AQ (p-value range: <.001–.022)'
    supports: statistics
  - section: Method
    page: 6
    quote: For each individual, and for each map (lesion-load, CBF, fMRI, FA), we computed the average
      signal intensity in each of 150 areas based on the AALCTS atlas.
    supports: region_definition
  - section: Discussion
    page: 14
    quote: Last, we did not validate the prediction accuracy of our models in an independent sample of
      persons with aphasia.
    supports: limitation
  - section: added by backfill
    page: not_reported
    quote: we constructed data-driven multivariate prediction models for language measures.
    supports: method
  - section: added by backfill
    page: 8
    quote: As our preliminary data analysis (see Section 2.4.1. and Results) found that lesion volume
      differed depending on sex, we included sex as a covariate in the preselection analyses
    supports: method
  - section: added by backfill
    page: 8
    quote: Features were retained if they had a p-value <.05 after applying the Benjamini–Hochberg correction
      for multiple comparisons
    supports: method
  lesion_mapping:
    analysis: multivariate
    n_analysed: 116
    min_lesion_overlap: not_reported
    lesion_volume_correction: covariate
    multiple_comparisons: fdr
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
---
