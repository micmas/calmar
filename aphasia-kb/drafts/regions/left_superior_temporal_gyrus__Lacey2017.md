---
schema_version: 2.6
id: left_superior_temporal_gyrus
name: Left Superior Temporal Gyrus (Dorsal Stream Node)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
hemisphere: left
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: Damage to the superior temporal cortex anterior to Heschl's gyrus is associated with comprehension
    deficits.
  direction: likely
  relationship: causal
  citation: '@Lacey2017'
  method: MLPA
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 38
    population: chronic left hemisphere stroke survivors
    time_post_onset: '>6 months'
    phase: chronic
    age_range: mean 62.97 (SD 12.41)
    handedness: mixed
    language: native English speakers
  statistics:
    threshold: P < .005 with a cluster threshold of 500 mm3
    effect_size: not_reported
  confounders_controlled:
  - lesion volume
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: SVR-LSM cluster in the superior temporal cortex anterior to Heschl's gyrus.
  imaging_details:
    field_strength: 3.0-T
    acquisition:
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 1900
      TE_ms: 2.56
      sequence: T1-weighted
    preprocessing_pipeline: VBM8 toolbox in SPM8 unified segmentation to MNI space
    reference_space: MNI152
    atlases_used: []
    coordinates_reported:
    - region: Superior temporal gyrus
      mni:
      - -46
      - -8
      - 0
  author_limitations:
  - The use of SVR-LSM vector weights does not necessarily correspond to the level of their importance
    to the cognitive process.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 446
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 446
    quote: Comprehension deficits were associated with lesions to the superior temporal cortex anterior
      to Heschl's gyrus.
    supports: claim
  - section: Methods
    page: 444
    quote: Thirty-eight native English speakers with chronic LH stroke (>6 months) participated in the
      study.
    supports: sample
  - section: Methods
    page: 444
    quote: Multivariate lesion-symptom mapping was carried out on each factor score using support vector
      regression–based lesion-symptom mapping (SVR-LSM)
    supports: method
  - section: Methods
    page: 445
    quote: the resulting P-map was thresholded at P < .005, with an arbitrary cluster threshold of 500
      mm3.
    supports: statistics
  - section: Methods
    page: 444
    quote: SVR-LSM provides a direct total lesion volume control (dTLVC) method to control relationships
      between total lesion size, stroke distribution, and factor scores.
    supports: confounders
  - section: Methods
    page: 444
    quote: High-resolution 3-dimensional T1-weighted magnetic resonance images were acquired on a 3.0-T
      Siemens TIM Trio scanner... voxel size = 1 mm3.
    supports: imaging_details
  - section: Methods
    page: 444
    quote: T1-weighted images were normalized to a standard older T1 brain template in Montreal Neurological
      Institute (MNI) space via the unified segmentation approach provided by the VBM8 toolbox in SPM8
    supports: imaging_details
  - section: Methods
    page: 444
    quote: Multivariate lesion-symptom mapping techniques must be interpreted with caution, because the
      vector weights do not necessarily correspond to the level of their importance to the cognitive process
      being studied.
    supports: limitation
---
