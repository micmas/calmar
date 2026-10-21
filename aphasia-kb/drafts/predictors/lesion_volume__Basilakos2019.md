---
schema_version: 2.3
id: lesion_volume
name: Lesion Volume
kind: predictor
predictor_type: imaging_metric
short_definition: The total volume of the stroke lesion.
assessment:
- manual T2 tracing
units: cm3
typical_range: not_reported
direction_of_severity: higher_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-19
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Larger lesion volume is associated with more severe initial aphasia (lower WAB-AQ) in chronic
    stroke.
  direction: likely
  relationship: causal
  citation: '@Basilakos2019'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 35
    population: chronic left-hemisphere stroke
    time_post_onset: mean 36.3 +/- 40.8 months at initial evaluation
    age_range: mean 55.8 +/- 9.1 years
    handedness: premorbidly right-handed
    language: not_reported
    phase: chronic
  statistics:
    threshold: P < .001
    effect_size: t = -4.3, P = .001
    p_value: 0.001
  confounders_controlled:
  - time poststroke at evaluation
  confounders_not_controlled:
  - diabetes
  - atherosclerotic disease
  - hypertension
  - age
  region_definition:
    kind: not_reported
    description: Total lesion volume obtained from manually traced T2-MRIs normalized to MNI space.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: MP-RAGE
      voxel_size_mm:
      - 1
      - 1
      - 1
    - modality: T2
      sequence: SPACE
      voxel_size_mm:
      - 1
      - 1
      - 1
    preprocessing_pipeline: SPM12 unified segmentation-normalization
    reference_space: MNI152
    atlases_used: []
  author_limitations:
  - The sample size was relatively small.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 7
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2018, @Yourganov2015Predicting (USC/MUSC Aphasia Lab)
  source_passages:
  - section: Results
    page: 7
    quote: Larger lesions were associated with more severe aphasia at initial evaluation (t = -4.3, P
      = .001)
    supports: claim
  - section: Materials and Methods - Participants
    page: 2
    quote: 'N = 35 participants (9 females; age at stroke: M = 55.5 +/- 10 years, range = 31-71 years)
      in the chronic stage of recovery after a single-event left hemisphere stroke'
    supports: sample
  - section: Materials and Methods - Predictor Variables Obtained From Neuroimaging
    page: 3
    quote: Lesion volume, obtained from the normalized lesion maps, was used to determine the spatial
      extent of the stroke lesion, where lesion volume (in cm3) was used as a predictor variable in regression
      models.
    supports: method
  - section: Limitations
    page: 10
    quote: First, the sample size was relatively small
    supports: limitation
---
# Findings on the relationship between lesion volume and initial aphasia severity.
