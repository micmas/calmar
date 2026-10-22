---
schema_version: 2.3
id: left_middle_temporal_gyrus
name: Left Middle Temporal Gyrus (Ventral Stream Node)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: Damage to the left posterior middle temporal gyrus and underlying white matter is associated
    with deficits in word-level language comprehension.
  direction: likely
  relationship: causal
  citation: '@Dronkers2004'
  method: VLSM
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 64
    population: chronic left hemisphere stroke patients
    time_post_onset: mean 4.8 years (range 1-20.5)
    age_range: 31-80 years (mean 61.5)
    handedness: all right-handed
    language: monolingual, native English speakers
    phase: chronic
  statistics:
    threshold: Bonferroni correction (t > 4.7)
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: data_driven_cluster
    description: VLSM-defined cluster in the posterior middle temporal gyrus and underlying white matter
      (Slices 3-6).
  imaging_details:
    field_strength: not_reported
    acquisition:
      voxel_size_mm:
      - 0.5
      - 0.5
      - 0.5
      sequence: not_reported
    preprocessing_pipeline: Manual reconstruction onto 11 standard templates based on the atlas of DeArmond,
      Fusco, and Dewey (1976).
    reference_space: Talairach
    atlases_used:
    - DeArmond, Fusco, and Dewey (1976)
    coordinates_reported: []
  author_limitations:
  - Brain regions cannot easily be separated from each other in lesion analysis.
  - Possibility of diaschitic effects where injuries to one area cause dysfunction in remote, non-lesioned
    areas.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 15
    confidence: high
    flags:
    - coordinates in Table 3 are in an unfamiliar format and were omitted
  source_passages:
  - section: Abstract
    page: 1
    quote: Results indicated that lesions to five left hemisphere brain regions affected performance on
      the CYCLE-R, including the posterior middle temporal gyrus and underlying white matter...
    supports: claim
  - section: Methods - Participants
    page: 4
    quote: Sixty-four left hemisphere-injured (LH) chronic stroke patients... All were right-handed, monolingual,
      native English speakers...
    supports: sample
  - section: Methods - VLSM
    page: 10
    quote: T-tests were then performed at each eligible voxel with the CYCLE-R score as the dependent
      variable...
    supports: method
  - section: Results - VLSM of overall CYCLE performance
    page: 14
    quote: T-values ranged from 21.4 to 6.3 (one-tailed), with those over 4.7... being statistically significant
      after Bonferroni correction...
    supports: statistics
  - section: Discussion
    page: 21
    quote: One caveat to any study that attempts to map cognitive functions is that brain regions cannot
      easily be separated from each other.
    supports: limitation
  - section: Discussion
    page: 21
    quote: Furthermore, lesion studies may suffer from the possibility of diaschitic effects such that
      injuries to one area can cause dysfunction in remote, non-lesioned areas.
    supports: limitation
---
