---
schema_version: 2.7
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
kind: predictor
predictor_type: behavioural
short_definition: A general measure of aphasia or global cognitive severity using standardized batteries.
assessment:
- WAB-R
- BNT
- MoCA
- NIHSS
units: score
typical_range: varies by instrument
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Initial NIHSS score is an independent predictor of poor functional outcome (mRS) at 3 months
    post-stroke.
  direction: likely
  relationship: correlational
  citation: '@Munsch2016'
  method: MLPA
  design: longitudinal
  strength: strong
  evidence_quality: cohort
  instrument: NIHSS
  score_band: not_reported
  interpretation: Higher initial NIHSS indicates worse functional prognosis.
  sample:
    n: 289
    population: patients with suspected supratentorial ischemic stroke
    time_post_onset: 24 to 72 hours
    phase: early_subacute
    age_range: older than 18 years
    handedness: not_reported
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: not_reported
    effect_size: beta = -0.320
    ci_95: '[-0.443, -0.196]'
    p_value: not_reported
  confounders_controlled:
  - age
  - stroke volume
  - stroke location
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioural-only predictor finding
  author_limitations:
  - The cohort contained mild ischemic stroke patients, potentially due to MRI tolerance in severe cases.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 69
    confidence: high
    flags:
    - imaging_details.reference_space not extracted by the model — set to not_reported; verify against
      the paper
  source_passages:
  - section: Results
    page: 69
    quote: In multivariate analysis, the association between stroke location and mRS did not persist,
      baseline NIHSS (beta=-0.320; 95% CI, -0.443 to -0.196) being the only independent predictor of functional
      outcome.
    supports: claim
  - section: Material and Methods
    page: 67
    quote: We prospectively recruited 428 consecutive patients presenting a suspected supratentorial ischemic
      stroke... imaged with structural magnetic resonance imaging (MRI) within 24 to 72 hours of a stroke.
    supports: sample
  - section: Discussion
    page: 71
    quote: Our cohort contained mild ischemic stroke patients. This might be because of the fact that
      severe stroke patients are less tolerant of the MRI procedure.
    supports: limitation
  - section: added by backfill
    page: 2
    quote: The 289 patients with complete data set were divided into 2 samples
    supports: method
  - section: added by backfill
    page: 1
    quote: We used multivariate logistic regression models to study the influence of stroke location (number
      of eloquent voxels from voxel-based lesion-symptom mapping maps), age, initial National Institutes
      of Health Stroke Scale and stroke volume on modified Rankin Scale and MoCA.
    supports: method
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  lesion_mapping:
    analysis: multivariate
    n_analysed: 289
    min_lesion_overlap: not_reported
    lesion_volume_correction: covariate
    multiple_comparisons: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
- id: f2
  target: prognosis
  target_kind: prognosis
  claim: Initial NIHSS score is an independent predictor of poor cognitive outcome (MoCA) at 3 months
    post-stroke.
  direction: likely
  relationship: correlational
  citation: '@Munsch2016'
  method: MLPA
  design: longitudinal
  strength: strong
  evidence_quality: cohort
  instrument: NIHSS
  score_band: not_reported
  interpretation: Higher initial NIHSS indicates worse cognitive prognosis.
  sample:
    n: 289
    population: patients with suspected supratentorial ischemic stroke
    time_post_onset: 24 to 72 hours
    phase: early_subacute
    age_range: older than 18 years
    handedness: not_reported
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: not_reported
    effect_size: beta = -0.158
    ci_95: '[-0.264, -0.051]'
    p_value: not_reported
  confounders_controlled:
  - age
  - stroke volume
  - stroke location
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioural-only predictor finding
  author_limitations:
  - The cohort contained mild ischemic stroke patients, potentially due to MRI tolerance in severe cases.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 69
    confidence: high
    flags:
    - imaging_details.reference_space not extracted by the model — set to not_reported; verify against
      the paper
  source_passages:
  - section: Results
    page: 69
    quote: In multivariate analysis, the association between stroke location and MoCA persisted... followed
      by baseline NIHSS (beta=-0.158; 95% CI, -0.264 to -0.051).
    supports: claim
  - section: Material and Methods
    page: 67
    quote: We prospectively recruited 428 consecutive patients presenting a suspected supratentorial ischemic
      stroke... imaged with structural magnetic resonance imaging (MRI) within 24 to 72 hours of a stroke.
    supports: sample
  - section: Discussion
    page: 71
    quote: Our cohort contained mild ischemic stroke patients. This might be because of the fact that
      severe stroke patients are less tolerant of the MRI procedure.
    supports: limitation
  - section: added by backfill
    page: 2
    quote: The 289 patients with complete data set were divided into 2 samples
    supports: method
  - section: added by backfill
    page: 1
    quote: We used multivariate logistic regression models to study the influence of stroke location (number
      of eloquent voxels from voxel-based lesion-symptom mapping maps), age, initial National Institutes
      of Health Stroke Scale and stroke volume on modified Rankin Scale and MoCA.
    supports: method
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  lesion_mapping:
    analysis: multivariate
    n_analysed: 289
    min_lesion_overlap: not_reported
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
