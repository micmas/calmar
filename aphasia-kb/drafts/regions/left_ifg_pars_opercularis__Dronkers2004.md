---
schema_version: 2.3
id: left_ifg_pars_opercularis
name: Left IFG Pars Opercularis (Broca's area, dorsal stream hub)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: syntactic_processing
  target_kind: impairment
  claim: Damage to the left inferior frontal gyrus pars opercularis (BA44) was not found to significantly
    affect sentence comprehension on the CYCLE-R.
  direction: no_effect
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
    description: Brodmann's area 44 (Broca's area).
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
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: Lesions to Broca's and Wernicke's areas were not found to significantly alter language comprehension
      on this particular measure.
    supports: claim
  - section: Results - VLSM of overall CYCLE performance
    page: 15
    quote: Lesions in Brodmann's areas 44 and 45 (Broca's area) were not seen to contribute...
    supports: claim
  - section: Methods - Participants
    page: 4
    quote: Sixty-four left hemisphere-injured (LH) chronic stroke patients... All were right-handed, monolingual,
      native English speakers...
    supports: sample
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
---
