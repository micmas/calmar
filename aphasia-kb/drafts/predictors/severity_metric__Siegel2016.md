---
schema_version: 2.6
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
kind: predictor
predictor_type: behavioural
short_definition: A composite measure of language impairment following stroke.
assessment:
- neuropsychological battery (PCA-derived language component)
units: z-normalized score
typical_range: mean = 0, SD = 1 (lower score indicating greater deficit)
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Language deficits in stroke patients are predicted with similar accuracy by both focal lesion
    topography and resting-state functional connectivity.
  direction: likely
  relationship: correlational
  citation: '@Siegel2016'
  method:
  - LSM
  - rs_fMRI
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 98
    population: subacute stroke patients
    time_post_onset: 1-2 wk after stroke
    phase: early_subacute
    age_range: mean 52.8 y (range 22-77)
    handedness: 119 right handed
    language: not_reported
  statistics:
    threshold: permutation tests
    effect_size: lesion r2 = 64.6%, FC r2 = 51.1%
    p_value: lesion P < 1e-4, FC P < 1e-4
  confounders_controlled:
  - head motion
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Comparison of whole-brain lesion maps vs. whole-brain FC matrices.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: MP-RAGE
      voxel_size_mm:
      - 1.0
      - 1.0
      - 1.0
    - modality: fMRI
      sequence: gradient echo EPI
      voxel_size_mm:
      - 4.0
      - 4.0
      - 4.0
      TR_ms: 2000
      TE_ms: 27
      volumes: 128
    preprocessing_pipeline: FSL FNIRT registration + FreeSurfer surface projection + global signal regression
      + CompCor
    reference_space: MNI152
    atlases_used:
    - Gordon et al. 2016 parcellation
  author_limitations:
  - The accuracy of brain network models depends in part on the brain regions used in the models.
  - Data from the cerebellum and basal ganglia were not included in this parcellation.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 3
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 3
    quote: language (n = 98, lesion P < 1 x 10-4, FC P < 1 x 10-4)
    supports: statistics
  - section: Results
    page: 4
    quote: language was equally predicted by both inputs (Attention -lesion = 32.3%, FC = 45.0%, P = 0.074;
      Language -lesion = 64.6%, FC = 51.1%, P = 0.21).
    supports: claim
  - section: Experimental Procedures
    page: 7
    quote: First-time stroke patients were recruited... time of enrollment < 2 wk poststroke onset.
    supports: sample
  - section: Experimental Procedures
    page: 8
    quote: All imaging was performed using a Siemens 3T Tim-Trio scanner... Resting state functional scans
      were acquired with a gradient echo EPI sequence (TR = 2,000 msec, TE = 27 msec, 32 contiguous 4-mm
      slices, 4 x 4 mm in-plane resolution)
    supports: imaging_details
  - section: Caveats/Limitations
    page: 7
    quote: However, data from the cerebellum and basal ganglia were not included in this parcellation.
    supports: limitation
---
