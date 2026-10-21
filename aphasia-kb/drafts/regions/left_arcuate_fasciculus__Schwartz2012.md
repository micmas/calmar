---
schema_version: 2.3
id: left_arcuate_fasciculus
name: Left Arcuate Fasciculus
kind: tract
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: phonological_production
  target_kind: impairment
  claim: Damage to the anterior portion of the left arcuate fasciculus is associated with increased phonological
    errors in object naming.
  direction: likely
  relationship: causal
  citation: '@Schwartz2012'
  method: VLSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 106
    population: chronic left-hemisphere stroke aphasia
    age_range: mean 58 (range 26-79)
    handedness: premorbid right-handed
    language: English
    phase: not_reported
  statistics:
    threshold: FDR q = 0.05
    effect_size: 29% overlap
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: tract
    description: Probabilistic arcuate fasciculus mask from JHU atlas thresholded at 0.8 probability.
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - JHU Probabilistic Atlas
    preprocessing_pipeline: Symmetric diffeomorphic registration (ANTS) to MNI Colin27
  author_limitations:
  - Analysis was exploratory and based on a probabilistic atlas rather than subject-specific DTI.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 3807
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 7
    quote: Of 10 582 voxels in the arcuate fasciculus mask, 29% (3077) overlapped with the t-map from
      the VLSM of phonological errors; the overlap was substantial in the anterior portion of the arcuate
      fasciculus
    supports: claim
  - section: Materials and methods
    page: 3
    quote: Of the 142 individuals enrolled, 106 qualified for the current study.
    supports: sample
  - section: Results
    page: 7
    quote: Not having collected diffusion tensor imaging data from these participants, we were unable
      to address this directly.
    supports: limitation
---
