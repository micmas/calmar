---
schema_version: 2.6
id: left_ifg_pars_opercularis
name: Left IFG Pars Opercularis (Broca's area, dorsal stream hub)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
hemisphere: left
findings:
- id: f1
  target: phonological_production
  target_kind: impairment
  claim: Damage to the left inferior frontal gyrus pars opercularis is associated with increased phonological
    errors during object naming.
  direction: likely
  relationship: causal
  citation: '@Schwartz2012'
  method: VLSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 106
    population: individuals with diverse profiles of aphasia
    time_post_onset: median months post-onset = 21.5; mean (SD) = 50.6 (66.6)
    phase: chronic
    age_range: mean 58 years (range 26-79 years)
    handedness: premorbid right handedness
    language: English as primary language
  statistics:
    threshold: FDR q = 0.01
    effect_size: t = 4.46
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lesion size
  region_definition:
    kind: data_driven_cluster
    description: Small cluster in the inferior frontal gyrus pars opercularis identified via VLSM.
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
    - region: inferior frontal gyrus
      mni:
      - -61
      - -3
      - 4
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
    quote: Additionally, there was a small cluster in the inferior frontal gyrus pars opercularis and
      rare voxels in pars triangularis; the peak t-value (t = 4.46) in inferior frontal gyrus was at MNI
      coordinates x = -61, y = -3, z = 4.
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
---
