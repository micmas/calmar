---
schema_version: 2.3
id: left_supramarginal_gyrus
name: Left Supramarginal Gyrus
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: phonological_production
  target_kind: impairment
  claim: Damage to the left supramarginal gyrus is associated with increased phonological errors in object
    naming.
  direction: likely
  relationship: causal
  citation: '@Schwartz2012'
  method: VLSM
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 106
    population: chronic left-hemisphere stroke aphasia
    age_range: mean 58 (range 26-79)
    handedness: premorbid right-handed
    language: English
    phase: not_reported
  statistics:
    threshold: FDR q = 0.01
    effect_size: t = 4.82
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: data_driven_cluster
    description: Voxel-based cluster in the supramarginal gyrus.
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - AAL
    preprocessing_pipeline: Symmetric diffeomorphic registration (ANTS) to MNI Colin27
    coordinates_reported:
    - region: supramarginal gyrus
      mni:
      - -45
      - -30
      - 26
  author_limitations:
  - Spatial coherence problem limits the ability to detect differences between positively correlated regions.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 3804
    confidence: high
    flags:
    - 'new_id: left_supramarginal_gyrus created as it is distinct from left_supramarginal_gyrus_premotor'
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
  - section: Discussion
    page: 13
    quote: the spatial coherence problem sets limits on what VLSM can tell about interregional differences
    supports: limitation
---
