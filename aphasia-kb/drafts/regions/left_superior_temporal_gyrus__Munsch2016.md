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
  target: severity_metric
  target_kind: predictor
  claim: Damage to the left superior temporal gyrus is associated with worse global cognitive outcome
    (MoCA) at 3 months post-stroke.
  direction: likely
  relationship: causal
  citation: '@Munsch2016'
  method: VLSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 215
    population: patients with suspected supratentorial ischemic stroke
    time_post_onset: 3 months
    phase: chronic
    age_range: older than 18 years
    handedness: not_reported
    language: not_reported
  statistics:
    threshold: FDR P < 0.05
    effect_size: not_reported
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: atlas
    atlas: Automated Anatomic Labeling
    description: Left superior temporal cortex identified as eloquent for MoCA via VLSM.
  imaging_details:
    field_strength: 3T
    acquisition:
      sequence: 3D inversion recovery-prepared fast spoiled gradient-echo
      voxel_size_mm:
      - 1
      - 1
      - 1
    preprocessing_pipeline: SPM8 registration to MNI152
    reference_space: MNI152
    atlases_used:
    - Automated Anatomic Labeling
    - Brodmann
    - JHU-WhiteMatter-labels-1mm
  author_limitations:
  - Only few voxels remained eloquent after false discovery rate correction.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 69
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 69
    quote: VLSM analysis on MoCA highlighted an even stronger left lateralization with a predominance
      of not only the prefrontal, cingulate, peri-insular, middle, and superior temporal cortex...
    supports: claim
  - section: Material and Methods
    page: 68
    quote: The eloquent regions were identified using the Automated Anatomic Labeling, Brodmann, and JHU-WhiteMatter-labels-1mm
      atlases available in the MRIcron software package.
    supports: region_definition
  - section: MRI Protocol
    page: 67
    quote: MRI examinations were performed on a 3-T Discovery MR750w scanner... The 3D T1-weighed sequence
      was a 3D inversion recovery-prepared fast spoiled gradient-echo... slice thickness, 1 mm.
    supports: imaging_details
  - section: Discussion
    page: 71
    quote: Regarding our VLSM maps, only few voxels remained eloquent after false discovery rate correction...
    supports: limitation
---
