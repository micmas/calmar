---
schema_version: 2.7
id: leukoaraiosis
name: Leukoaraiosis
kind: predictor
predictor_type: imaging_metric
short_definition: Presence and severity of pathological white matter hyperintensities (WMHs) in the periventricular
  and deep white matter.
assessment:
- Fazekas scale
units: Fazekas total score (0-6)
typical_range: 0-6 (higher = more severe)
direction_of_severity: higher_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-19
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: More severe leukoaraiosis at initial evaluation predicts a decline in language abilities (WAB-AQ)
    over time in chronic aphasia.
  direction: likely
  relationship: correlational
  citation: '@Basilakos2019'
  method: LSM
  design: longitudinal
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
    cohort: not_reported
  statistics:
    threshold: P < .05
    effect_size: t = -2.3, P = .028; odds of decline 4.3 (95% CI = 1.2-14.7, P = .017)
    p_value: 0.028
  confounders_controlled:
  - initial aphasia severity
  - stroke age
  - time post-stroke at follow-up assessment
  confounders_not_controlled:
  - diabetes
  - atherosclerotic disease
  - hypertension
  - age
  - external treatment
  region_definition:
    kind: not_reported
    description: Global leukoaraiosis severity rated on the right hemisphere using the Fazekas scale (sum
      of PVH and DWMH scores).
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: MP-RAGE
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 2250
      TI_ms: 925
      TE_ms: 4.11
    - modality: T2
      sequence: SPACE
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 3200
      TE_ms: 212
    preprocessing_pipeline: SPM12 unified segmentation-normalization
    reference_space: MNI152
    atlases_used: []
  author_limitations:
  - The sample size was relatively small.
  - Unable to control for factors that may have influenced the presence and severity of leukoaraiosis
    (eg, diabetes, atherosclerotic disease, hypertension, age).
  - Male dominated sample (approximately a 3:1 ratio of males:females).
  - Unable to control for treatment that individuals may have received in acute inpatient or outpatient
    rehabilitation settings outside of our lab.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, pages 723-724
    confidence: high
    flags:
    - new predictor id
    - cohort overlaps with @Fridriksson2018, @Yourganov2015Predicting (USC/MUSC Aphasia Lab)
    - leukoaraiosis rated on right hemisphere due to symmetry assumption
  source_passages:
  - section: Abstract
    page: 1
    quote: Leukoaraiosis severity and initial aphasia severity significantly predicted decline in language
      abilities at follow-up, accounting for approximately one-third of the variance (adjusted R2 = 0.33).
    supports: claim
  - section: Results
    page: 7
    quote: Specifically, for every 1-point increase in Fazekas score, AQ decreased by 2.6 points (t =
      -2.3, P = .028)
    supports: statistics
  - section: Results
    page: 7
    quote: for every 1-point increase in Fazekas score, the odds of decline was 4.3, 95% CI = 1.2-14.7
      (beta = 1.48, P = .017).
    supports: statistics
  - section: Materials and Methods - Participants
    page: 2
    quote: 'N = 35 participants (9 females; age at stroke: M = 55.5 +/- 10 years, range = 31-71 years)
      in the chronic stage of recovery after a single-event left hemisphere stroke'
    supports: sample
  - section: Materials and Methods - Statistical Methods
    page: 4
    quote: A series of regression analyses ('Enter' method in SPSS) was then used to evaluate our 2 lines
      of inquiry.
    supports: method
  - section: Materials and Methods - Neuroimaging
    page: 2
    quote: T1- and T2-weighted images were acquired on a Siemens Trio 3T scanner... T1-weigthed imaging
      utilized an MP-RAGE sequence with 1 mm isotropic voxels... T2-weighted scans were acquired using
      a 3-dimensional T2-weighted SPACE sequence... with a resolution of 1 mm3
    supports: imaging_details
  - section: Limitations
    page: 10
    quote: First, the sample size was relatively small
    supports: limitation
  - section: added by backfill
    page: 2
    quote: This is a retrospective study including multi–time point assessment of N = 35 participants
    supports: method
  - section: added by backfill
    page: 5
    quote: Again, lesion volume and leukoaraiosis severity were entered as predictors, this time predicting
      the raw change in AQ from initial to follow-up assessment.
    supports: method
  lesion_mapping:
    analysis: not_reported
    n_analysed: 35
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
# Findings on the role of leukoaraiosis in chronic aphasia prognosis.
