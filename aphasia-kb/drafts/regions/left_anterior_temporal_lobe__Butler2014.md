---
schema_version: 2.7
id: left_anterior_temporal_lobe
name: Left Anterior Temporal Lobe
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: Damage to the left anterior temporal lobe, specifically the anterior middle temporal gyrus and
    temporal stem, is associated with impaired semantic processing in chronic stroke.
  direction: likely
  relationship: causal
  citation: '@Butler2014'
  method: VBCM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 31
    population: chronic stroke aphasia
    time_post_onset: '>= 12 months'
    age_range: not_reported
    handedness: all right-handed
    language: English first language
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: P = 0.001 voxel-level, P < 0.001 FWE corrected cluster-level
    effect_size: not_reported
  confounders_controlled:
  - lesion volume
  - other PCA factors
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Cluster in the left hemisphere anterior temporal lobe overlapping with anterior MTG and
      temporal stem (including dorsal edges of ITG and fusiform gyrus).
  imaging_details:
    field_strength: 3T
    acquisition:
      voxel_size_mm:
      - 1
      - 1
      - 1
      sequence: T1-weighted inversion recovery
    preprocessing_pipeline: modified unified segmentation-normalization procedure (Seghier et al. 2008)
      implemented in SPM8
    reference_space: MNI152
    atlases_used: []
  author_limitations:
  - Automated lesion identification may be affected by abnormal ventricle shape in large lesions.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 8
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 8
    quote: Performance on the semantic factor was uniquely related to a cluster of voxels in the left
      hemisphere anterior temporal lobe (Fig. 5B). The cluster overlapped with the anterior middle temporal
      gyrus and the temporal stem (including the dorsal edges of the inferior temporal gyrus and fusiform
      gyrus).
    supports: claim
  - section: Materials and methods
    page: 3
    quote: Participants were included if they had chronic stroke aphasia... and were at least 12 months
      post-stroke at time of scanning and assessment (n = 31).
    supports: sample
  - section: Results
    page: 6
    quote: Results are thresholded at P = 0.001 voxel-level, P < 0.001 family-wise error (FWE) corrected
      cluster-level.
    supports: statistics
  - section: Materials and methods
    page: 5
    quote: It is therefore likely to be affected by the abnormal shape of the ventricles in patients with
      large lesions, and hence is used with the caveat that periventricular results are treated with caution
      (Geva et al., 2012).
    supports: limitation
  - section: added by backfill
    page: not_reported
    quote: The first analysis used the three continuous multidimensional predictors of the PCA factor
      scores, which are necessarily uncorrelated (orthogonal) with one another.
    supports: method
  - section: added by backfill
    page: 10
    quote: including lesion volume in the VBCM model with the independent PCA factor scores did not alter
      the pattern of results obtained
    supports: method
  lesion_mapping:
    analysis: univariate
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
Finding f1: Butler et al. (2014) found that the semantic factor uniquely correlated with a cluster in the left anterior temporal lobe.
