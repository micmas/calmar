---
schema_version: 2.3
id: left_parietal_association_cortex
name: Left Parietal Association Cortex
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: Damage to the left parietal association cortex contributes significantly to impaired auditory
    comprehension.
  direction: likely
  relationship: causal
  citation: '@Bates2003'
  method: VLSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 101
    population: left-hemisphere-damaged aphasic patients
    time_post_onset: at least one year after stroke
    age_range: not_reported
    handedness: not_reported
    language: native English speakers
    phase: not_reported
  statistics:
    threshold: P = 0.05 (controlling the expected proportion of false positives)
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: data_driven_cluster
    description: Voxel-based lesion-symptom mapping cluster for auditory comprehension.
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
    flags:
    - target mapped to semantics as proxy for auditory comprehension
  source_passages:
  - section: Results
    page: 2
    quote: Auditory comprehension was most affected by lesions in the middle temporal gyrus (MTG), with
      significant contributions also seen in... parietal association cortex
    supports: claim
  - section: Figure 1 caption
    page: 2
    quote: Only voxels that were significant at P = 0.05 (controlling the expected proportion of false
      positives) are shown.
    supports: statistics
---
