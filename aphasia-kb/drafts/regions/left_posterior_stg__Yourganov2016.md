---
schema_version: 2.3
id: left_posterior_stg
name: Left Posterior Superior Temporal Gyrus
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: fluency
  target_kind: impairment
  claim: Damage to the left posterior superior temporal gyrus is a significant predictor of speech fluency
    in chronic aphasia.
  direction: likely
  relationship: causal
  citation: '@Yourganov2016'
  method: MLPA
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 90
    population: chronic left-hemisphere stroke aphasia
    time_post_onset: mean 42.8 months (range 6-276)
    age_range: mean 58.8 years (range 31-81)
    handedness: not_reported
    language: not_reported
    phase: chronic
  statistics:
    threshold: p < 0.05 with Bonferroni's correction
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: atlas
    atlas: Faria et al. (2012)
    description: Posterior part of the superior temporal gyrus
  imaging_details:
    field_strength: 3T
    acquisition:
      voxel_size_mm:
      - 1
      - 1
      - 1
      sequence: MP-RAGE
    preprocessing_pipeline: Enantiomorphic normalization using SPM12
    reference_space: MNI152
    atlases_used:
    - Faria et al. (2012)
  author_limitations:
  - The use of a linear SVR model may not capture non-linear relationships between brain damage and behavior.
  - Feature selection by discarding low-correlation features might miss variables that are predictive
    only in combination with others.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 5
    confidence: high
    flags:
    - cohort overlaps with @Yourganov2015Predicting (same USC/MUSC lab group)
  source_passages:
  - section: Results
    page: 5
    quote: For lesion-based analysis, the most important regions for predicting fluency scores were the
      precentral gyrus, opercular part of inferior frontal gyrus, and the posterior part of the superior
      temporal gyrus (PSTG)
    supports: claim
  - section: Materials and Methods
    page: 2
    quote: 90 individuals were included in the final data analyses. The mean +/- SD sample age was 58.8
      +/- 12.1 years (range, 31-81 years)... mean +/- SD time since stroke onset was 42.8 +/- 50 months
    supports: sample
  - section: Materials and Methods
    page: 4
    quote: The threshold for significance of correlation was 0.05 with Bonferroni's correction for multiple
      comparisons
    supports: statistics
  - section: Discussion
    page: 11
    quote: by discarding the features that were not highly correlated with a given behavioral score, we
      could potentially discard the features that might be predictive when used in combination with other
      features.
    supports: limitation
- id: f2
  target: auditory_comprehension
  target_kind: impairment
  claim: Damage to the left posterior superior temporal gyrus is a significant predictor of auditory comprehension
    in chronic aphasia.
  direction: likely
  relationship: causal
  citation: '@Yourganov2016'
  method: MLPA
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 90
    population: chronic left-hemisphere stroke aphasia
    time_post_onset: mean 42.8 months
    age_range: mean 58.8 years
    handedness: not_reported
    language: not_reported
    phase: chronic
  statistics:
    threshold: p < 0.05 with Bonferroni's correction
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: atlas
    atlas: Faria et al. (2012)
    description: Posterior part of the superior temporal gyrus
  imaging_details:
    field_strength: 3T
    reference_space: MNI152
    atlases_used:
    - Faria et al. (2012)
  author_limitations:
  - Feature selection by discarding low-correlation features might miss variables that are predictive
    only in combination with others.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 5
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 5
    quote: for predicting auditory comprehension scores, the PSTG, the triangular part of inferior frontal
      gyrus, the pole and the posterior part of the middle temporal gyrus, the amygdala, and the dorsal
      part of the middle frontal gyrus
    supports: claim
- id: f3
  target: speech_repetition
  target_kind: impairment
  claim: Damage to the left posterior superior temporal gyrus is a significant predictor of speech repetition
    in chronic aphasia.
  direction: likely
  relationship: causal
  citation: '@Yourganov2016'
  method: MLPA
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 90
    population: chronic left-hemisphere stroke aphasia
    time_post_onset: mean 42.8 months
    age_range: mean 58.8 years
    handedness: not_reported
    language: not_reported
    phase: chronic
  statistics:
    threshold: p < 0.05 with Bonferroni's correction
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: atlas
    atlas: Faria et al. (2012)
    description: Posterior part of the superior temporal gyrus
  imaging_details:
    field_strength: 3T
    reference_space: MNI152
    atlases_used:
    - Faria et al. (2012)
  author_limitations:
  - Feature selection by discarding low-correlation features might miss variables that are predictive
    only in combination with others.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 5
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 5
    quote: for predicting speech repetition scores, the posterior part of the superior and the middle
      temporal gyri
    supports: claim
- id: f4
  target: naming
  target_kind: impairment
  claim: Damage to the left posterior superior temporal gyrus is a significant predictor of naming in
    chronic aphasia.
  direction: likely
  relationship: causal
  citation: '@Yourganov2016'
  method: MLPA
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 90
    population: chronic left-hemisphere stroke aphasia
    time_post_onset: mean 42.8 months
    age_range: mean 58.8 years
    handedness: not_reported
    language: not_reported
    phase: chronic
  statistics:
    threshold: p < 0.05 with Bonferroni's correction
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: atlas
    atlas: Faria et al. (2012)
    description: Posterior part of the superior temporal gyrus
  imaging_details:
    field_strength: 3T
    reference_space: MNI152
    atlases_used:
    - Faria et al. (2012)
  author_limitations:
  - Feature selection by discarding low-correlation features might miss variables that are predictive
    only in combination with others.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 5
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 5
    quote: for predicting naming scores, the PSTG, the pole of the superior and middle temporal gyri,
      and the triangular part of the inferior frontal gyrus.
    supports: claim
---
Findings from Yourganov 2016 using multivariate SVR to predict WAB scores from lesion maps and connectomes.
