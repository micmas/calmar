---
schema_version: 2.7
id: right_arcuate_fasciculus
name: Right Arcuate Fasciculus
kind: tract
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: right
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: The volume of the long segment of the right arcuate fasciculus is a positive predictor of language
    recovery (WAB-R AQ) 6 months post-stroke.
  direction: likely
  relationship: correlational
  citation: '@Forkel2014'
  method: tractography
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 16
    population: left hemisphere stroke patients with aphasia
    time_post_onset: baseline within 2 weeks; follow-up at 6 months
    age_range: 28-87 years (mean 60)
    handedness: all right-handed
    language: native English speaker
    phase: longitudinal
    cohort: not_reported
  statistics:
    threshold: P = 0.020
    effect_size: beta = 0.730
    p_value: 0.02
  confounders_controlled:
  - age
  - sex
  - lesion size
  confounders_not_controlled: []
  region_definition:
    kind: manual_ROI
    description: Long segment of the arcuate fasciculus defined as streamlines passing through both frontal
      and temporal regions of interest.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: DTI
      sequence: spin echo, single shot EPI
      voxel_size_mm:
      - 2.4
      - 2.4
      - 2.4
      n_directions: 60
      b_values:
      - 1500
    preprocessing_pipeline: ExploreDTI for eddy current and motion correction; RESTORE for outlier exclusion;
      non-linear least squares tensor estimation
    reference_space: native
    atlases_used: []
  author_limitations:
  - DTI algorithms are prone to false positives (non-existing tracts) and false negatives.
  - The sample was a selected group able to tolerate long MRI scans in the acute stage, potentially possessing
    higher plasticity than the general population.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 2032
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 1
    quote: For the right hemisphere, age [beta = -0.678, t(-3.087), P = 0.010] and volume of the long
      segment of the arcuate fasciculus [beta = 0.730, t(2.732), P = 0.020] were predictors of longitudinal
      aphasia severity.
    supports: claim
  - section: Materials and methods
    page: 1
    quote: Sixteen patients (10 males; mean age 60 +/- 17 years, range 28-87 years) underwent post stroke
      language assessment with the Revised Western Aphasia Battery and neuroimaging scanning within a
      fortnight from symptoms onset.
    supports: sample
  - section: Materials and methods
    page: 3
    quote: Diffusion tensor imaging data were acquired using a spin echo, single shot EPI pulse sequence...
      combined together for a total of 60 directions and seven non-diffusion weighted volumes... voxel
      size was 2.4 x 2.4 x 2.4 mm.
    supports: imaging_details
  - section: Materials and methods
    page: 4
    quote: All streamlines passing through both frontal and temporal regions of interest were considered
      as belonging to the long segment of the arcuate fasciculus.
    supports: region_definition
  - section: Discussion
    page: 11
    quote: Current diffusion tensor imaging algorithms are prone to implicit limitations, including generating
      the presence of false positives (i.e. non-existing tracts) and false negatives (i.e. absence of
      truly existing tracts)
    supports: limitation
  - section: Discussion
    page: 11
    quote: our observations reflect results derived from a selected group of patients that were able to
      tolerate a 45-min MRI scanning session in the acute stage of stroke.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
# Right Arcuate Fasciculus

This entry describes the right hemisphere arcuate fasciculus, specifically its role as a structural predictor of recovery following left-hemisphere stroke.
