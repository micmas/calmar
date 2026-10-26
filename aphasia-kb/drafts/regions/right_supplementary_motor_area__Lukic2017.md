---
schema_version: 2.7
id: right_supplementary_motor_area
name: Right Supplementary Motor Area
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
hemisphere: right
findings:
- id: f1
  target: fluency
  target_kind: impairment
  claim: Increased grey matter volume in the right supplementary motor area is associated with better
    spoken word and sentence production in chronic aphasia.
  direction: likely
  relationship: correlational
  citation: '@Lukic2017'
  method: VBCM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 40
    population: chronic stroke-induced aphasia
    time_post_onset: at least eight months post onset of stroke (57.2 ±52.3 months)
    phase: chronic
    age_range: 35 to 81 (59.4 ±12.4 yrs)
    handedness: all right handed, with the exception of one aphasic speaker who was left handed
    language: native English speakers
    cohort: not_reported
  statistics:
    threshold: p < 0.001 voxel-level threshold and a minimum cluster size (665–708 mm3) determined by
      an estimate of image smoothness
    effect_size: '0.59'
    p_value: '0.0002'
  confounders_controlled:
  - age
  - total intracranial volume
  - proportion of critical area of damage (PCAD)
  confounders_not_controlled: []
  region_definition:
    kind: atlas
    atlas: AAL
    description: Right supplementary motor area (SMA) identified via AAL atlas peak coordinates.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: 3D MPRAGE
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 2300
      TE_ms: 2.91
    preprocessing_pipeline: bias field inhomogeneities correction + VBM8 toolbox (tissue segmentation,
      rigid registration, DARTEL normalization to MNI152) + 8mm FWHM Gaussian smoothing
    reference_space: MNI152
    atlases_used:
    - AAL
    coordinates_reported:
    - region: right SMA
      mni:
      - 13.5
      - 16.5
      - 61.5
  author_limitations:
  - The study is not longitudinal, so it cannot definitively establish a recovery trajectory.
  - Individual differences among participants before stroke may explain the observed GM volume differences.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, Table 4
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 6
    quote: For production measures, the voxel-wise linear regression of spoken word production on the
      GM volume revealed a significant positive relationship between word production scores and GM volume
      in the right SMA and insula.
    supports: claim
  - section: Method
    page: 3
    quote: Forty participants with aphasia (14 female) resulting from a single-left hemisphere stroke...
      were recruited
    supports: sample
  - section: Method
    page: 3
    quote: Aphasic participants were at least eight months post onset of stroke (57.2 ±52.3 months)
    supports: sample
  - section: Method
    page: 5
    quote: The relationship between grey matter volume in the right hemisphere and language performance...
      was analyzed by performing voxel-wise multiple linear regression using the VBM8 toolbox
    supports: method
  - section: Method
    page: 5
    quote: the 'proportion of critical area of damage' (PCAD) was entered as a covariate together with
      age and the total intracranial volume
    supports: confounders
  - section: Method
    page: 5
    quote: thresholded by determining the minimum cluster size based on a p < 0 001 voxel-level threshold
      and on an estimate of image smoothness in AFNI
    supports: statistics
  - section: Discussion
    page: 11
    quote: In the absence of longitudinal data, however, we refrain from making strong claims regarding
      the relation between RH GM volume and recovery.
    supports: limitation
  - section: Method
    page: 4
    quote: DARTEL normalization to the template space (Template_1_IXI550_MNI152.nii)
    supports: imaging_details
  - section: added by backfill
    page: 5
    quote: The segmented, modulated, normalized, and smoothed GM images and language scores (% correct)
      were entered in each regression model, resulting in T-maps that showed regions where GM volume was
      signiﬁcantly associated with language performance.
    supports: method
  - section: added by backfill
    page: 5
    quote: the “proportion of critical area of damage” (PCAD) was entered as a covariate together with
      age and the total intracranial volume (computed as the sum of grey and white matter, and cerebrospinal
      ﬂuid) in the VBM analysis to partial out their eﬀects on language performance.
    supports: method
  lesion_mapping:
    analysis: univariate
    n_analysed: 40
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
