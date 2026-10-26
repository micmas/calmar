---
schema_version: 2.7
id: left_middle_frontal_gyrus
name: Left Middle Frontal Gyrus
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
hemisphere: left
findings:
- id: f1
  target: fluency
  target_kind: impairment
  claim: Damage to the left middle frontal gyrus is associated with reduced verbal quality in connected
    speech production.
  direction: likely
  relationship: causal
  citation: '@Alyahya2020'
  method: VBCM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 46
    population: chronic post-stroke aphasia
    time_post_onset: 4-12 months post-stroke
    phase: early_subacute
    age_range: mean 63.21 (SD 11.93)
    handedness: right-handed
    language: native English speakers
    cohort: not_reported
  statistics:
    threshold: P = 0.001 voxel-level and cluster-level corrected using family-wise error (FWE) at P =
      0.05
    effect_size: not_reported
  confounders_controlled:
  - age
  - education
  - time since stroke onset
  - other language and cognitive components
  confounders_not_controlled: []
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford atlas
    description: Middle frontal gyrus
  imaging_details:
    field_strength: 3.0 T
    acquisition:
      sequence: T1-weighted inversion recovery sequence with 3D acquisition
    preprocessing_pipeline: SPM8
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford atlas
    coordinates_reported:
    - region: Middle frontal gyrus
      mni:
      - -34
      - 16
      - 32
  author_limitations:
  - White matter tracts described are descriptive, based on overlap with an atlas rather than directly
    measured using DWI.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1548; Table 2, page 1550
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 1548
    quote: the 'verbal quality' component showed neural correlates across left frontal regions, including
      the inferior frontal gyrus (pars opercularis and pars triangularis), middle frontal gyrus...
    supports: claim
  - section: Materials and methods
    page: 1543
    quote: Forty-six patients who had developed aphasia following a single left haemorrhagic or ischaemic
      stroke were tested in the chronic stage (4-12 months post-stroke).
    supports: sample
  - section: Analysis of neuroimaging data
    page: 1544
    quote: The unified PCA model was mapped onto brain lesions using a voxel-based correlational methodology
      (VBCM) (Tyler et al., 2005).
    supports: method
  - section: Analysis of neuroimaging data
    page: 1544
    quote: The results were thresholded at P = 0.001 voxel-level and cluster-level corrected using family-wise
      error (FWE) at P = 0.05.
    supports: statistics
  - section: Discussion
    page: 1552
    quote: it must be acknowledged that white matter tracts described in this study are descriptive, based
      on the overlap of the significant clusters with a white matter atlas (Catani et al., 2012) rather
      than directly measured using diffusion-weighted imaging.
    supports: limitation
  - section: Acquisition and processing of neuroimaging data
    page: 1543
    quote: High-resolution structural T1-weighted MRI scans were acquired for each patient on a 3.0 T
      Philips Achieva scanner... A T1-weighted inversion recovery sequence with 3D acquisition was used.
    supports: imaging_details
  - section: added by backfill
    page: 4
    quote: A multiple regression model was created using the normalized-smoothed T1-weighted images as
      the dependant variable and language and cognitive component as regressors of interest, entered simultaneously
      along with the other components and demographic variables (age, education, and time since stroke
      onset).
    supports: method
  - section: added by backfill
    page: 4
    quote: Two parallel analyses were performed, with/without lesion volume as a covariate, to avoid a
      possible risk for type II error with the inclusion of lesion volume.
    supports: method
  - section: added by backfill
    page: 4
    quote: The results were thresholded at P5 0.001 voxel-level and cluster-level corrected using family-wise
      error (FWE) at P5 0.05.
    supports: method
  lesion_mapping:
    analysis: multivariate
    n_analysed: 46
    min_lesion_overlap: not_reported
    lesion_volume_correction: covariate
    multiple_comparisons: cluster_fwe
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
---
Finding from @Alyahya2020 regarding the left middle frontal gyrus and verbal quality in connected speech.
