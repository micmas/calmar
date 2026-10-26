---
schema_version: 2.7
id: left_anterior_arcuate_fasciculus
name: Left anterior arcuate fasciculus
kind: tract
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: fluency
  target_kind: impairment
  claim: Damage to the anterior segment of the left arcuate fasciculus is a robust predictor of impaired
    speech fluency in aphasia.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2013'
  method: VBCM
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 64
    population: chronic left hemisphere stroke
    time_post_onset: mean 39.86 months (SD 49.24)
    age_range: mean 61.6 years (SD 12.27)
    handedness: not_reported
    language: not_reported
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: Bonferroni corrected P < 0.002
    effect_size: R2 = 0.40
    p_value: '0.0001'
  confounders_controlled:
  - lesion size
  confounders_not_controlled:
  - agrammatism
  region_definition:
    kind: atlas
    atlas: Catani et al. (2012) white matter atlas
    description: Anterior segment of the arcuate fasciculus (ASAF) defined by a probability threshold
      of 0.50.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: MP-RAGE
      voxel_size_mm:
      - 2
      - 2
      - 2
    - modality: T2
      sequence: 3D SPACE
      voxel_size_mm:
      - 1
      - 1
      - 1
    preprocessing_pipeline: SPM8 + cost-function masking + normalization to 2mm ICBM template
    reference_space: MNI152
    atlases_used:
    - Catani et al. (2012)
  author_limitations:
  - Lack of explicit measures of patients' ability to initiate or to maintain fluent speech.
  - Data set does not include a detailed measure of agrammatism.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 3454
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 4
    quote: The primary region of interest analysis (using stepwise regression) revealed that speech fluency
      ratings on the WAB are best predicted by damage to the ASAF, P = 0.0001, R2 = 0.40
    supports: claim
  - section: Materials and methods
    page: 3
    quote: Out of 76 patients included in the database, data from 64 patients... who had incurred a single
      left hemisphere stroke... resulting in chronic aphasia... were included
    supports: sample
  - section: Discussion
    page: 8
    quote: The study is also limited by its lack of explicit measures of patients' ability to initiate
      or to maintain fluent speech.
    supports: limitation
  - section: added by backfill
    page: 4
    quote: The cortical regions and white matter tracts comprised a neuroanatomical model where the mean
      intensity value in each region of interest, as well as lesion size, was entered into a stepwise
      regression analysis to predict the speech and language measures (Fig. 2).
    supports: method
  - section: added by backfill
    page: not_reported
    quote: 'To control for multiple comparisons, the stepwise regression analyses were Bonferroni corrected
      where P = 0.05 was divided by the number of predictors: 21 regions of interest and one factor for
      lesion size (for 22 total predictors).'
    supports: method
  - section: added by backfill
    page: 3
    quote: Out of 76 patients included in the database, data from 64 patients (29 females) who had incurred
      a single left hemisphere stroke (60 ischaemic; four haemorrhagic) resulting in chronic aphasia (46
      months post-stroke) were included in this research (Supplementary material).
    supports: method
  lesion_mapping:
    analysis: region_based
    n_analysed: 64
    min_lesion_overlap: not_reported
    lesion_volume_correction: covariate
    multiple_comparisons: bonferroni
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
---
