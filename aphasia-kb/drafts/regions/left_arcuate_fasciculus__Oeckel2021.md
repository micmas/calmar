---
schema_version: 2.7
id: left_arcuate_fasciculus
name: Left arcuate fasciculus
kind: tract
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: aphasia
  target_kind: impairment
  claim: Lesions of the left arcuate fasciculus (>15% overlap) were not significantly associated with
    the occurrence of aphasia in acute stroke patients without cortical language area lesions.
  direction: no_effect
  relationship: causal
  citation: '@Oeckel2021'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 123
    population: acute left-hemispheric stroke patients without lesions of language-related cortical areas
    time_post_onset: <10 days
    phase: acute
    age_range: < 90 years
    handedness: not_reported
    language: German native speaker
    cohort: not_reported
  statistics:
    threshold: P = 0.25
    effect_size: OR 0.30
    ci_95: '[0.04, 2.35]'
  confounders_controlled:
  - extreme capsule lesions
  - stroke volume
  - age
  - gender
  confounders_not_controlled: []
  region_definition:
    kind: tract
    description: Arcuate fascicle (AF) quantified via global fibre tractography and slice-plane overlap
      percentage.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: DTI
      sequence: diffusion-sensitive single-shot spin-echo echo-planar imaging
      voxel_size_mm:
      - 2
      - 2
      - 2
      TR_ms: 11800
      TE_ms: 96
      n_directions: 61
      b_values:
      - 0
      - 1000
    preprocessing_pipeline: MATLAB-based in-house toolbox for fibre tracking
    reference_space: not_reported
    atlases_used:
    - Stanford atlas of functional regions of interest
  author_limitations:
  - The size of the study cohort of 123 stroke patients including 18 (14.6%) with aphasia may be considered
    as a study limitation.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 8
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: In contrast, stroke lesions of >15% in the arcuate fascicle were not associated with aphasia.
    supports: claim
  - section: Results
    page: 8
    quote: 'AF lesions of more than 15% were not associated with aphasia (OR = 0.30, 95% confidence interval:
      0.04-2.35, P = 0.25)'
    supports: statistics
  - section: Discussion
    page: 8
    quote: Lesions in the AF were not associated with aphasia as defined by the Token Test.
    supports: claim
  - section: added by backfill
    page: 1
    quote: The study cohort consisted of 123 patients with acute left-hemispheric stroke without a lesion
      of language-related cortical areas of the Stanford atlas of functional regions of interest.
    supports: method
  - section: added by backfill
    page: 5
    quote: Stroke volume, age and gender were covariates.
    supports: method
  lesion_mapping:
    analysis: region_based
    n_analysed: 123
    min_lesion_overlap: '>15%'
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
