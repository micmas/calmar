---
schema_version: 2.6
id: left_rostral_anterior_cingulate_cortex
name: Left Rostral Anterior Cingulate Cortex
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
hemisphere: left
findings:
- id: f1
  target: executive_functions
  target_kind: impairment
  claim: Damage to the left rostral anterior cingulate cortex is associated with impaired response and
    set switching, as measured by the Trail-Making Test and Wisconsin Card Sorting Test.
  direction: likely
  relationship: causal
  citation: '@Glascher2012'
  method: VLSM
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 344
    population: individuals with focal lesions
    time_post_onset: not_reported
    phase: not_reported
    age_range: not_reported
    handedness: mostly right-handed (317 of 344)
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: P < 0.05 (FDR)
    effect_size: not_reported
  confounders_controlled:
  - verbal abilities
  - spatial abilities
  - verbal memory
  - spatial memory
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Focal region of left rostral ACC identified via VLSM associated with TMT and WCST performance.
  imaging_details:
    reference_space: not_reported
    atlases_used: []
    preprocessing_pipeline: Manual slice-by-slice tracing onto a reference brain
  author_limitations:
  - Findings are relative to the particular tasks for which data were available.
  - Power was greatest in regions with the densest lesion overlaps (PFC).
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 2
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 2
    quote: Significantly lower performances on the TMT and WCST were associated with damage to the ACC.
      Lower performance on the TMT was associated with damage to a focal region of left rostral ACC, whereas
      lower performance on the WCST was associated with damage to a slightly more anterior region of the
      ACC...
    supports: claim
  - section: Materials and Methods
    page: 6
    quote: The 344 participants were drawn from the Patient Registry of the Department of Neurology at
      the University of Iowa Hospitals and Clinics.
    supports: sample
  - section: Materials and Methods
    page: 6
    quote: We used nonparametric voxel-based lesion-symptom mapping (VLSM) (28) to map out significant
      lesion-deficit relationships.
    supports: method
  - section: Materials and Methods
    page: 6
    quote: We used a threshold of 5% FDR to control for multiple comparisons.
    supports: statistics
  - section: Materials and Methods
    page: 6
    quote: Performance scores indexing verbal skills, visual-spatial reasoning, and both verbal and visual
      memory were derived from additional neuropsychological tests and used as covariates to partial out
      their effects...
    supports: confounders
  - section: Materials and Methods
    page: 6
    quote: The visible lesion of each patient's MRI or CT scan was traced manually slice by slice on corresponding
      regions of a reference brain by a neuroanatomical expert.
    supports: imaging_details
  - section: Discussion
    page: 5
    quote: our results are relative to the particular tasks for which data were available, and different
      neuropsychological measures might produce somewhat different anatomical results.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    unresolved:
    - lesion_mapping
---
