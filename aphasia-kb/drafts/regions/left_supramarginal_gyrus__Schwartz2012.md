---
schema_version: 2.7
id: left_supramarginal_gyrus
name: Left Supramarginal Gyrus
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
hemisphere: left
findings:
- id: f1
  target: phonological_production
  target_kind: impairment
  claim: Damage to the left supramarginal gyrus is associated with increased phonological errors during
    object naming.
  direction: likely
  relationship: causal
  citation: '@Schwartz2012'
  method: VLSM
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 106
    population: individuals with diverse profiles of aphasia
    time_post_onset: median months post-onset = 21.5; mean (SD) = 50.6 (66.6)
    phase: chronic
    age_range: mean 58 years (range 26-79 years)
    handedness: premorbid right handedness
    language: English as primary language
    cohort: not_reported
  statistics:
    threshold: FDR q = 0.01
    effect_size: t = 4.82
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lesion size
  region_definition:
    kind: data_driven_cluster
    description: Cluster of significant voxels occupying the supramarginal gyrus identified via VLSM.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: MPRAGE
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 1620
      TE_ms: 3.87
    preprocessing_pipeline: Symmetric diffeomorphic registration (ANTS) to custom template, then to MNI
      Colin27
    reference_space: MNI152
    atlases_used:
    - AAL
    coordinates_reported:
    - region: supramarginal gyrus
      mni:
      - -45
      - -30
      - 26
  author_limitations:
  - Spatial coherence of lesion data may make it difficult to distinguish between joint and independent
    contributions of adjacent regions.
  - Poor lesion coverage in the inferior temporal and fusiform gyri prevents addressing those areas.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 6
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 6
    quote: A large number of significant voxels (2275 voxels; 16% of total) occupied the supramarginal
      gyrus; the maximal t-value in this cluster (t = 4.82) was at MNI coordinates x = -45, y = -30, z
      = 26.
    supports: claim
  - section: Materials and methods
    page: 3
    quote: Of the 142 individuals enrolled, 106 qualified for the current study.
    supports: sample
  - section: Materials and methods
    page: 3
    quote: Ninety-one (86%) were 46 months post-onset of aphasia; median months post-onset = 21.5; mean
      (SD) = 50.6 (66.6).
    supports: sample
  - section: Materials and methods
    page: 5
    quote: The resulting t-maps were thresholded to control the false discovery rate (FDR) (Genovese et
      al., 2002) at q = 0.01
    supports: statistics
  - section: Materials and methods
    page: 5
    quote: The structural scans were registered to a custom template... using a symmetric diffeomorphic
      registration algorithm (Avants et al., 2006) implemented in the Advanced Normalization Tools package...
      A single mapping from the custom intermediate template to the Montreal Neurological Institute (MNI)
      space 'Colin27' volume... was used
    supports: imaging_details
  - section: Discussion
    page: 13
    quote: 'the spatial coherence problem sets limits on what VLSM can tell about interregional differences:
      ''Even in the presence of good regional power, the power to detect differences between two regions
      may be low when the two regions are positively correlated'''
    supports: limitation
  - section: added by backfill
    page: 5
    quote: a t-test was performed at each voxel comparing scores on the dependent variable between patients
      with and without lesions in that voxel.
    supports: method
  lesion_mapping:
    analysis: univariate
    n_analysed: 106
    min_lesion_overlap: 10% of the sample
    lesion_volume_correction: not_reported
    multiple_comparisons: fdr
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
---
