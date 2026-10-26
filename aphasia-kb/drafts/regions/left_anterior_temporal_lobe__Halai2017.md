---
schema_version: 2.7
id: left_anterior_temporal_lobe
name: Left Anterior Temporal Lobe
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
hemisphere: left
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: Damage to the left anterior temporal lobe is uniquely associated with impaired semantic ability
    in chronic post-stroke aphasia.
  direction: likely
  relationship: causal
  citation: '@Halai2017'
  method: VBCM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 31
    population: chronic post-stroke aphasia
    time_post_onset: at least 12 months
    phase: chronic
    age_range: not_reported
    handedness: all right-handed
    language: native English speakers
    cohort: not_reported
  statistics:
    threshold: p < .005 voxel-level, p <= .001 family-wise error (FWE)-corrected cluster-level
    effect_size: not_reported
    p_value: not_reported
  confounders_controlled:
  - lesion volume
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: VBCM cluster uniquely correlating with the semantic factor score.
  imaging_details:
    field_strength: 3.0 T
    acquisition:
      voxel_size_mm:
      - 1.0
      - 1.0
      - 1.0
      TR_ms: 9.0
      TE_ms: 3.93
      sequence: T1-weighted inversion recovery
    preprocessing_pipeline: SPM8 modified unified segmentation-normalisation (Seghier et al., 2008) +
      8mm FWHM Gaussian kernel
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
  author_limitations:
  - The factor solution is always dependent on the tests included in the decomposition.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 10
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 10
    quote: Performance on the semantic factor was uniquely related to a cluster in the left hemisphere
      anterior temporal lobe (ATL; see Fig. 3A).
    supports: claim
  - section: Methods - Participants
    page: 4
    quote: Thirty one chronic stroke patients... All patients were at least 12 months post-stroke at the
      time of scanning and assessment
    supports: sample
  - section: Methods - Analysis of neuroimaging data
    page: 6
    quote: We used the T1-weighted images... and correlated these with individual measures or PCA factor
      scores using a voxel-based correlational methodology (VBCM)
    supports: method
  - section: Results
    page: 9
    quote: Results are thresholded at p < .005 voxel-level, p <= .001 family-wise error (FWE)-corrected
      cluster-level.
    supports: statistics
  - section: Methods - Analysis of neuroimaging data
    page: 6
    quote: In order to ensure that the results were not merely attributable to lesion size... this was
      entered as a covariate in each VBCM.
    supports: confounders
  - section: Discussion
    page: 13
    quote: One thing that must be kept in mind when using PCA is that the factor solution is always dependent
      on the tests included in the decomposition.
    supports: limitation
  - section: Methods - Acquisition of neuroimaging data
    page: 5
    quote: High-resolution structural T1-weighted MRI scans were acquired on a 3.0 T Philips Achieva scanner
    supports: imaging_details
  - section: added by backfill
    page: 6
    quote: the participants' factor scores from the omnibus PCA of the entire neuropsychological test
      battery and speech measures were entered into a VBCM analysis.
    supports: method
  - section: added by backfill
    page: 6
    quote: In order to ensure that the results were not merely attributable to lesion size, each participants'
      lesion volume was calculated from the lesion identiﬁed by the automated lesion identiﬁcation method
      (Seghier et al., 2008) and this was entered as a covariate in each VBCM.
    supports: method
  lesion_mapping:
    analysis: multivariate
    n_analysed: 31
    min_lesion_overlap: not_reported
    lesion_volume_correction: covariate
    multiple_comparisons: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
---
