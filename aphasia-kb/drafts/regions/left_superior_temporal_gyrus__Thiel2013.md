---
schema_version: 2.3
id: left_superior_temporal_gyrus
name: Left Superior Temporal Gyrus (Dorsal Stream Node)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Increased recruitment of left-hemispheric language networks (measured by activation volume index)
    is positively correlated with global language recovery after inhibitory rTMS to the right IFG.
  direction: likely
  relationship: correlational
  citation: '@Thiel2013'
  method:
  - TMS
  - fMRI_activation
  design: RCT
  strength: moderate
  evidence_quality: RCT
  sample:
    n: 24
    population: subacute poststroke aphasia
    time_post_onset: average 5.4-7.2 weeks
    age_range: mean 69.8-71.2 years
    handedness: all right handed
    language: German
    phase: early_subacute
  statistics:
    threshold: P=0.015
    effect_size: r2=0.25
    p_value: 0.015
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Left-hemispheric activation volume (AV) of all suprathreshold voxels (Z>2) during verb
      generation.
  author_limitations:
  - The study was underpowered to detect a specific aphasia type and treatment interaction.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 2242
    confidence: high
    flags:
    - target is a general left-hemisphere network index, but mapped to STG as part of the language network
  source_passages:
  - section: Results
    page: 1
    quote: There was a moderate but significant linear relationship between activation volume index change
      and global Aachen Aphasia Test score change (r2=0.25; P=0.015).
    supports: claim
  - section: Methods
    page: 2
    quote: Z-score images were thresholded at Z>2, and activation volumes (AV) of all suprathreshold voxels
      were calculated for each hemisphere using the 3D tool.
    supports: method
  - section: Discussion
    page: 5
    quote: Results of the linear regression analysis suggest that this change in interhemispheric balance
      as measured with the AVI explains ≈25% of the observed variability of our primary outcome variable.
    supports: statistics
  - section: Discussion
    page: 5
    quote: however, the study was underpowered to detect a specific aphasia type and treatment interaction
    supports: limitation
  imaging_details:
    field_strength: not_reported
    modalities:
    - modality: PET
      sequence: O-15-water
      voxel_size_mm:
      - 2.2
      - 2.2
      - 3.125
      notes: CTI/Siemens ECAT EXACT HR scanner
    - modality: T1
      sequence: not_reported
    preprocessing_pipeline: Spatially normalized to MNI space using SPM8
    reference_space: MNI152
    atlases_used: []
    task:
      name: Verb generation
      description: Patients generated one semantically matching verb to each presented high-frequency
        German noun.
      contrasts:
      - Verb generation > Baseline
      baseline: Eyes closed and no auditory input
---
This finding links the shift of activation back to the left hemisphere (measured via AVI) to clinical improvement following right-hemisphere inhibition.
