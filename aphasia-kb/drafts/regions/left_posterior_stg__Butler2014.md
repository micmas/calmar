---
schema_version: 2.3
id: left_posterior_stg
name: Left Posterior Superior Temporal Gyrus
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: phonological_production
  target_kind: impairment
  claim: Damage to left posterior perisylvian regions, including the posterior superior temporal gyrus,
    middle temporal gyrus, and Heschl's gyrus, is associated with impaired phonological processing in
    chronic stroke.
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
  statistics:
    threshold: P = 0.001 voxel-level, P < 0.001 FWE corrected cluster-level
    effect_size: not_reported
  confounders_controlled:
  - lesion volume
  - other PCA factors (semantics, executive-cognition)
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Cluster containing primary auditory cortex (BA 41, 42), mid to posterior MTG, STG, STS,
      posterior insula, Heschl's gyrus, and planum temporale.
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
  - Automated lesion identification may be affected by abnormal ventricle shape in large lesions, making
    periventricular results less reliable.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 8
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 8
    quote: 'Performance on the phonological factor was uniquely correlated with voxels across a number
      of left hemisphere regions, principally a cluster containing: primary auditory cortex (Brodmann
      areas 41 and 42); mid to posterior middle and superior temporal gyri; superior temporal sulcus;
      and posterior portions of the insula, Heschl''s gyrus and the planum temporale.'
    supports: claim
  - section: Materials and methods
    page: 3
    quote: Participants were included if they had chronic stroke aphasia... and were at least 12 months
      post-stroke at time of scanning and assessment (n = 31).
    supports: sample
  - section: Materials and methods
    page: 1
    quote: The use of principle components analysis rendered participants' scores on these three factors
      orthogonal and therefore ideal for use as simultaneous continuous predictors in a voxel-based correlational
      methodology analysis of high resolution structural scans.
    supports: method
  - section: Results
    page: 6
    quote: Results are thresholded at P = 0.001 voxel-level, P < 0.001 family-wise error (FWE) corrected
      cluster-level.
    supports: statistics
  - section: Materials and methods
    page: 4
    quote: High resolution structural T1-weighted MRI scans were acquired on a 3.0 T Philips Achieva scanner...
      acquired voxel size 1.0 x 1.0 x 1.0 mm3
    supports: imaging_details
  - section: Materials and methods
    page: 4
    quote: Participants' MRI scans were normalized and segmented using a modified unified segmentation-normalization
      procedure optimized for lesioned brains (Seghier et al., 2008) implemented in Statistical Parametric
      Mapping (SPM) 8
    supports: imaging_details
  - section: Materials and methods
    page: 5
    quote: It is therefore likely to be affected by the abnormal shape of the ventricles in patients with
      large lesions, and hence is used with the caveat that periventricular results are treated with caution
      (Geva et al., 2012).
    supports: limitation
---
Finding f1: Butler et al. (2014) used PCA to isolate a phonological factor and found it uniquely correlated with a left posterior perisylvian cluster including the pSTG and Heschl's gyrus.
