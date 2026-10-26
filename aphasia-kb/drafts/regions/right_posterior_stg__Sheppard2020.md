---
schema_version: 2.7
id: right_posterior_stg
name: Right Posterior Superior Temporal Gyrus
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
hemisphere: right
findings:
- id: f1
  target: affective_receptive_aprosodia
  target_kind: impairment
  claim: Damage to the right posterior superior temporal gyrus is an independent predictor of impairment
    in overall emotional prosody identification in acute stroke.
  direction: likely
  relationship: causal
  citation: '@Sheppard2020'
  method: RLSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 23
    population: acute right hemisphere ischemic stroke
    time_post_onset: within 5 days of stroke
    phase: acute
    age_range: mean 55.09 years, SD 17.22
    handedness: all right-handed
    language: premorbid fluent speakers of English
    cohort: not_reported
  statistics:
    threshold: p < 0.05
    effect_size: p = 0.038
    p_value: 0.038
  confounders_controlled:
  - age
  - education
  - lesion volume
  confounders_not_controlled: []
  region_definition:
    kind: manual_ROI
    description: Right posterior superior temporal gyrus traced using MRIcron and coregistered to the
      Johns Hopkins University atlas.
  imaging_details:
    field_strength: 3.0T
    acquisition:
      voxel_size_mm:
      - 2
      - 2
      - 2
      sequence: DWI
    preprocessing_pipeline: MRIcron tracing + SPM12 coregistration to Johns Hopkins University atlas
    reference_space: other
    atlases_used:
    - Johns Hopkins University atlas
  author_limitations:
  - Relatively small number of participants with longitudinal data prevented brain-behavior mapping in
    chronic patients.
  - Only 1 of 9 chronic patients had a lesion in posterior STG, preventing determination of its role in
    chronic deficits.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page e1015
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 4
    quote: Individual predictors of overall emotion identification impairment were older age (p = 0.009)
      and greater damage to posterior STG (p = 0.038)
    supports: claim
  - section: Methods
    page: 2
    quote: We enrolled 23 patients (mean age 55.09 years, SD 17.22) with acute RH ischemic stroke... At
      the acute time point, 23 patients were tested within 5 days of stroke.
    supports: sample
  - section: Statistical analysis
    page: 3
    quote: 'Multivariable linear regression was used to identify the independent predictors of overall
      emotional prosody identification impairment... The following independent variables were entered
      into the initial model: percent damage to each of 7 regions of interest... overall lesion volume,
      age, and education.'
    supports: method
  - section: Results
    page: 4
    quote: The model for overall emotion identification was significant, F10,10 = 3.15, p = 0.043... Individual
      predictors of overall emotion identification impairment were older age (p = 0.009) and greater damage
      to posterior STG (p = 0.038)
    supports: statistics
  - section: Methods
    page: 2
    quote: Scans were acquired clinically within 48 hours of admission on a 3.0T Siemens (Munich, Germany)
      Trio scanner. Whole-brain DWI had 40 slices with a 2.0 mm3 voxel size.
    supports: imaging_details
  - section: Methods
    page: 2
    quote: These areas of tissue dysfunction were traced using MRIcron software and were coregistered
      to the Johns Hopkins University atlas using SPM12
    supports: region_definition
  - section: Discussion
    page: 6
    quote: There were a relatively small number of participants with longitudinal data at both the acute
      and chronic stages, which prevented us from conducting brain-behavior mapping in chronic patients.
    supports: limitation
  - section: added by backfill
    page: 1
    quote: Multivariable linear regression was used to identify the independent predictors of overall
      emotional prosody identification impairment
    supports: method
  - section: added by backfill
    page: 3
    quote: Only regions from the proposed ventral stream where at least 2 participants had damage were
      included in the analysis
    supports: method
  - section: added by backfill
    page: 3
    quote: 'The following independent variables were entered into the initial model: percent damage to
      each of 7 regions of interest (posterior STG, STG, temporal pole, IFG pars orbitalis, lateral OFC,
      amygdala, sagittal stratum), overall lesion volume, age, and education.'
    supports: method
  lesion_mapping:
    analysis: multivariate
    n_analysed: 23
    min_lesion_overlap: '>= 2 patients'
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
Finding f1 describes the causal link between right posterior STG damage and overall emotional prosody identification impairment in acute stroke patients.
