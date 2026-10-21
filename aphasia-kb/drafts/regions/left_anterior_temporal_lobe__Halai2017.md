---
schema_version: 2.3
id: left_anterior_temporal_lobe
name: Left Anterior Temporal Lobe
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: Damage to the left anterior temporal lobe is associated with impaired semantic ability in chronic
    stroke.
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
    time_post_onset: '>= 12 months'
    age_range: not_reported
    handedness: all right-handed
    language: native English
    phase: chronic
  statistics:
    threshold: p < .005 voxel-level, p <= .001 FWE-corrected cluster-level
    effect_size: not_reported
  confounders_controlled:
  - lesion volume
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: VBCM cluster in the left hemisphere anterior temporal lobe (ATL).
  imaging_details:
    field_strength: 3T
    acquisition:
      voxel_size_mm:
      - 1
      - 1
      - 1
      sequence: T1-weighted inversion recovery
    preprocessing_pipeline: SPM8 modified unified segmentation-normalisation (Seghier et al. 2008) + 8mm
      FWHM Gaussian kernel
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
  author_limitations:
  - the factor solution is always dependent on the tests included in the decomposition
  - future studies will need to augment the range of assessments in order to capture other key features...
    including syntactic processing, speech errors, written language processing, etc.
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
      anterior temporal lobe (ATL...)
    supports: claim
  - section: Methods
    page: 4
    quote: Thirty one chronic stroke patients... were recruited... All patients were at least 12 months
      post-stroke at the time of scanning and assessment...
    supports: sample
  - section: Results
    page: 9
    quote: Results are thresholded at p < .005 voxel-level, p <= .001 family-wise error (FWE)-corrected
      cluster-level.
    supports: statistics
  - section: Discussion
    page: 13
    quote: One thing that must be kept in mind when using PCA is that the factor solution is always dependent
      on the tests included in the decomposition.
    supports: limitation
---
