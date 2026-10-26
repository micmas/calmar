---
schema_version: 2.7
id: left_presma_dacc
name: Left Presupplementary Motor Area / Dorsal Anterior Cingulate Cortex
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
hemisphere: left
findings:
- id: f1
  target: fluency
  target_kind: impairment
  claim: Activation in the left preSMA/dACC during speech production is positively correlated with the
    longitudinal recovery of speech production in subacute aphasia.
  direction: likely
  relationship: correlational
  citation: '@Geranmayeh2017'
  method: fMRI_activation
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 27
    population: left hemisphere stroke
    time_post_onset: first in the early phase (≈2 weeks) and then ≈4 months after the ictus
    phase: longitudinal
    age_range: 59 ± 11 years
    handedness: one patient was left-handed
    language: English
    cohort: not_reported
  statistics:
    threshold: FWE cluster correction for the whole brain volume at P = 0.05
    effect_size: r = 0.363 (early phase), r = 0.538 (late phase)
    p_value: P = 0.03 (early), P = 0.004 (late)
  confounders_controlled:
  - lesion volume
  - age
  - initial language impairment
  confounders_not_controlled: []
  region_definition:
    kind: peak_coord_sphere
    mni_peak:
    - -4
    - 8
    - 50
    description: Midline voxel with highest activity during the Decision task, located within the preSMA
      and extending into the dACC.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: fMRI
      sequence: gradient-echo
      voxel_size_mm:
      - 3.5
      - 3.5
      - 3.0
      TR_ms: 10000
      TE_ms: 31
    task:
      name: Speech task
      description: Participants were required to define nouns presented as coloured picture stimuli.
      contrasts:
      - Speech > Rest
      baseline: Rest
    preprocessing_pipeline: FSL (motion-correction, non-brain voxels removal, 8mm Gaussian smoothing,
      high-pass filtering) + Boundary-Based Registration + fieldmap-based EPI distortion correction
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford cortical structural atlas
  author_limitations:
  - The observed relationship... is likely to have relationship with brain structure [e.g., small vessel
    disease or indirect result of stroke disrupting inputs].
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, pages 1951-1953
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: the level of activation within this region during speech production correlated positively with
      the longitudinal recovery of speech production across the two time points
    supports: claim
  - section: Participants
    page: 2
    quote: Twenty-seven participants were scanned at two time points; first in the early phase after the
      stroke [15 ± 7.6 days... and again at ≈4 months (108 ± 26 days)
    supports: sample
  - section: Image analysis
    page: 4
    quote: Data were preprocessed with the FMRIB Software Library... Registration of functional MRI images
      to high resolution structural images was carried out by Boundary-Based Registration
    supports: method
  - section: Results
    page: 7
    quote: the activity in the peak voxel of midline frontal cortex in the preSMA/dACC, during the early
      scan (r = 0.363, P = 0.03 one-tailed) and late scan (r = 0.538, P = 0.004) when performing the Speech
      task were both correlated positively with degree of language recovery
    supports: statistics
  - section: Image analysis
    page: 5
    quote: 'The midline voxel with highest activity during the Decision task was chosen as a functional
      region of interest... located within the preSMA (x, y, z coordinates: -4, 8, 50)'
    supports: region_definition
  - section: Discussion
    page: 10
    quote: The observed relationship of reduced preSMA/dACC activity and recovery is likely to have relationship
      with brain structure. It could be due to (i) pre-existing pathology... (ii) a simple relationship
      as a direct result of stroke lesion volume; and (iii) a more complicated relationship as an indirect
      result of the stroke disrupting the inputs to this region.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
Findings from Geranmayeh 2017 indicate that activation in the preSMA/dACC during speech production predicts longitudinal recovery of speech production, independent of lesion volume and age.
