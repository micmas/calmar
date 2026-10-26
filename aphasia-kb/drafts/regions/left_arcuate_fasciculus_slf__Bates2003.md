---
schema_version: 2.7
id: left_arcuate_fasciculus_slf
name: Left Arcuate Fasciculus and Superior Longitudinal Fascicle (Dorsal Language Pathway)
kind: tract
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: fluency
  target_kind: impairment
  claim: Damage to the left arcuate/superior longitudinal fasciculus in parietal white matter is associated
    with reduced speech fluency.
  direction: likely
  relationship: causal
  citation: '@Bates2003'
  method: VLSM
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 101
    population: left-hemisphere-damaged aphasic patients
    time_post_onset: at least one year after stroke
    age_range: not_reported
    handedness: not_reported
    language: native English speakers
    phase: not_reported
    cohort: not_reported
  statistics:
    threshold: P = 0.05 (controlling the expected proportion of false positives)
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: data_driven_cluster
    description: Voxel-based lesion-symptom mapping peak in parietal white matter.
  imaging_details:
    reference_space: other
    atlases_used: []
    preprocessing_pipeline: Lesions reconstructed onto templates by a board-certified neurologist.
  author_limitations:
  - An area may emerge as relevant either because it has a direct causal role or because of a diaschitic
    effect.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 449
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 2
    quote: Fluency was most affected by lesions in the insula... and in the arcuate/superior longitudinal
      fasciculus in parietal white matter
    supports: claim
  - section: Figure 1 caption
    page: 2
    quote: Only voxels that were significant at P = 0.05 (controlling the expected proportion of false
      positives) are shown.
    supports: statistics
  - section: added by backfill
    page: 1
    quote: We applied VLSM to measures of speech fluency and language comprehension in 101 left-hemisphere-damaged
      aphasic patients
    supports: method
  lesion_mapping:
    analysis: univariate
    n_analysed: 101
    min_lesion_overlap: not_reported
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
