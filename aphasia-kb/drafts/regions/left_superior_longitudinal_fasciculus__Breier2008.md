---
schema_version: 2.3
id: left_superior_longitudinal_fasciculus
name: Left Superior Longitudinal Fasciculus
kind: tract
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: phonological_production
  target_kind: impairment
  claim: Reduced integrity of the left superior longitudinal fasciculus is associated with impaired speech
    repetition in chronic stroke patients.
  direction: likely
  relationship: correlational
  citation: '@Breier2008'
  method: DTI
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 20
    population: chronic left-hemisphere stroke
    time_post_onset: mean 22 months
    age_range: 38-77 years
    handedness: all premorbidly right handed
    language: not_reported
    phase: chronic
  statistics:
    threshold: P < 0.017
    effect_size: F[1,18] = 15.51
    p_value: '0.001'
  confounders_controlled:
  - cortical damage to Broca area
  - white matter disease
  confounders_not_controlled:
  - poststroke reorganization
  region_definition:
    kind: manual_ROI
    description: FA values obtained as it runs anteroposterior, deep to the shoulder of the Sylvian fissure.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: DTI
      sequence: single-shot spin-echo diffusion sensitized echo-planar imaging (EPI)
      voxel_size_mm:
      - 3
      - 3
      - 3
      TR_ms: 6100
      TE_ms: 84
      n_directions: 21
      b_values:
      - 1000
    preprocessing_pipeline: not_reported
    reference_space: not_reported
    atlases_used:
    - Mori et al. 2005
  author_limitations:
  - FA decreases may be non-specific.
  - Use of standard rectangular rather than tailored irregular ROIs.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 484
    confidence: high
    flags:
    - 'new_region_id: left_superior_longitudinal_fasciculus'
  source_passages:
  - section: Results
    page: 3
    quote: For the SLF, only the relationship between the FA value and repetition was significant (F[1,18]
      15.51; P 0.001).
    supports: claim
  - section: Methods - DTI Analyses
    page: 2
    quote: We obtained FA values for the SLF as it runs anteroposterior, deep to the shoulder of the Sylvian
      fissure.
    supports: region_definition
---
Findings from Breier 2008 regarding the left superior longitudinal fasciculus and its correlation with repetition.
