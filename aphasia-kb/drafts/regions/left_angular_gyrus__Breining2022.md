---
schema_version: 2.3
id: left_angular_gyrus
name: "Left Angular Gyrus"
kind: classical
hemisphere: left
aliases:
  - "left AG"
  - "Brodmann area 39 (left)"
status: draft
created_by: "agent:claude-sonnet-4-6"
created_on: 2026-05-06

findings:
  - id: f1
    target: object_naming
    target_kind: impairment
    claim: >
      Greater damage to the left angular gyrus is independently associated with worse
      object naming (BNT) performance in acute left hemisphere stroke.
    direction: likely
    relationship: causal
    citation: "@Breining2022"

    method: MLPA
    design: cross-sectional
    imaging: multimodal

    sample:
      n: 37
      population: "acute left hemisphere stroke patients"
      time_post_onset: "acute (scan obtained 0–12 days post-stroke, mean 2.2 days; assessment 0–12 days, mean scan-assessment interval −1.5 days)"
      age_range: "mean 56.5 ± 13.4 years; range 28–87"
      handedness: not_reported
      language: "English-speaking (Johns Hopkins)"
      recruitment: "Department of Neurology, Johns Hopkins School of Medicine"
      inclusion_criteria: "acute left hemisphere stroke; unilateral left hemisphere stroke (right hemisphere ROIs excluded due to no lesions)"
      exclusion_criteria: "bilateral lesions; right hemisphere ROIs had no lesions in any participant"

    statistics:
      threshold: "LASSO regression with leave-one-out cross-validation (λ minimizing mean cross-validated error); inference via post-LASSO t-test"
      cluster_extent: not_reported
      effect_size: "LASSO value = −0.524; adjusted coefficient = −0.555"
      ci_95: not_reported
      p_value: "p < .001 (independent significant predictor of BNT performance)"

    confounders_controlled:
      - "total lesion volume (entered as covariate in LASSO model)"
      - "LASSO regularization to address multicollinearity between adjacent regions"
    confounders_not_controlled:
      - "age"
      - "education"
      - "sex"
      - "time post-onset (narrow acute window but not formally covaried)"

    region_definition:
      kind: atlas
      atlas: "MRICloud multi-atlas pipeline (289 ROI parcellation)"
      description: "Automated segmentation of DWI-traced acute lesion map overlaid onto MRICloud-segmented T1 structural image; percentage of each of 13 left hemisphere ROIs damaged calculated. Left angular gyrus is one of 13 ROIs with lesions in ≥5 participants."

    imaging_details:
      field_strength: not_reported
      modalities:
        - modality: DWI
          sequence: "diffusion-weighted imaging (DWI)"
          description: "Areas of dense ischemia (bright DWI, dark ADC) manually traced by technicians blinded to behavior"
        - modality: T1
          sequence: "MPRAGE"
          description: "T1 anatomical; lesioned tissue replaced with undamaged right hemisphere tissue; segmented via MRICloud"
      preprocessing_pipeline: "MRICloud automated segmentation (289 ROIs via large deformation diffeomorphic mapping + multi-atlas fusion); lesion co-registered to T1 via SPM12; lesioned tissue replaced with right hemisphere mirror; MRICloud pipeline applied; lesion map overlaid to calculate %ROI damaged"
      reference_space: "MNI152"
      atlases_used:
        - "MRICloud multi-atlas parcellation (289 ROIs)"
      coordinates_reported: []

    replications: []
    contradictions: []

    author_limitations:
      - "Small neuroimaging sample (n=37 acute stroke with imaging); LASSO may overfit with many predictors relative to sample size."
      - "LASSO eliminates highly correlated variables — regions important for naming may not have been selected due to correlation with left angular gyrus."
      - "Picture naming of actions involves objects in the image, potentially conflating object and action processing."
      - "White matter tracts were not assessed."
      - "Static picture stimuli for action naming cannot fully capture the temporal nature of actions."

    evidence_quality: cohort
    strength: moderate

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results – Neuroimaging results (pp. 747–748, Table 5); Methods – Acute stroke neuroimaging (pp. 743–744)"
      confidence: high
      flags:
        - "PPA data NOT extracted per extraction rules (non-stroke etiology); only acute stroke findings are in this draft"
        - "Method coded as MLPA (LASSO is a form of multivariate lesion-symptom mapping) rather than VLSM"
        - "ROI-based LASSO, not voxel-wise — region boundaries determined by MRICloud atlas, not data-driven clusters"
        - "forward-looking target ID: object_naming (check if impairment ID exists in KB)"

    source_passages:
      - section: "Results – Neuroimaging results"
        page: 748
        supports: claim
        quote: >
          For the model of object naming, we found that larger percentage of tissue lesioned
          in the left angular gyrus and left middle temporal gyrus were associated with worse
          performance on the BNT. Greater damage to the left angular gyrus independently
          predicted object naming performance (p < .001).
      - section: "Methods – Acute stroke"
        page: 743
        supports: sample
        quote: >
          Participants (N = 138 PPA, N = 37 acute stroke) completed the BNT and HANA.
          A subset of participants (N = 31 PPA, N = 37 acute stroke) provided neuroimaging data.
      - section: "Methods – Acute stroke"
        page: 743
        supports: imaging_details
        quote: >
          Technicians blinded to the behavioural results used MRIcron to trace areas of
          tissue disfunction, defined as areas of dense ischemia/infarct that were bright on
          DWI maps but dark on apparent diffusion coefficient (ADC) maps. Traced lesions were
          coregistered to T1 scans using SPM12. Lesioned tissue was replaced with tissue from
          the undamaged right hemisphere.
      - section: "Results – Neuroimaging results (Table 5)"
        page: 749
        supports: statistics
        quote: >
          Left angular gyrus −0.524 −0.555 <.001* −0.405 −0.487 0.728
      - section: "Methods – Relating neuroimaging and behavioural data"
        page: 744
        supports: method
        quote: >
          Least Absolute Shrinkage and Selection Operator (LASSO) regression was used to
          evaluate which ROIs were related to behaviour on object and action naming. LASSO
          regression with standardised features was instantiated with the glmnet package in R,
          using leave-one-out cross-validation to select the λ value that resulted in the
          minimum mean cross validated error.
      - section: "Discussion – Limitations"
        page: 752
        supports: limitation
        quote: >
          Another important limitation is the sample size that was included in the
          neuroimaging analysis. Although behavioural data were available for a relatively
          sizable sample of participants with PPA, contemporaneous neuroimaging data were
          not available for many of the participants. Similarly, the sample size was
          relatively small for the acute stroke participants.

  - id: f2
    target: action_naming
    target_kind: impairment
    claim: >
      Greater damage to the left angular gyrus is associated with worse action naming
      (HANA) performance in acute left hemisphere stroke; the effect is not independently
      statistically significant but the region appears in the LASSO-selected model.
    direction: mixed
    relationship: causal
    citation: "@Breining2022"

    method: MLPA
    design: cross-sectional
    imaging: multimodal

    sample:
      n: 37
      population: "acute left hemisphere stroke patients"
      time_post_onset: "acute (mean scan 2.2 days post-stroke)"
      age_range: "mean 56.5 ± 13.4 years"
      handedness: not_reported
      language: "English-speaking"
      recruitment: "Johns Hopkins Department of Neurology"
      inclusion_criteria: "acute left hemisphere stroke"
      exclusion_criteria: "bilateral lesions; right hemisphere regions not assessed (no lesions)"

    statistics:
      threshold: "LASSO regression with leave-one-out cross-validation"
      cluster_extent: not_reported
      effect_size: "LASSO value = −0.405; adjusted coefficient = −0.487"
      ci_95: not_reported
      p_value: "p = .728 (not independently significant)"

    confounders_controlled:
      - "total lesion volume (covariate in model; significant for action naming LASSO: LASSO value=−0.225, p=.072 trend)"
    confounders_not_controlled:
      - "age, education, sex, time post-onset"

    region_definition:
      kind: atlas
      atlas: "MRICloud multi-atlas pipeline (289 ROI parcellation)"
      description: "Same automated segmentation pipeline as f1; 13 left hemisphere ROIs used for acute stroke analyses"

    imaging_details:
      field_strength: not_reported
      acquisition:
        sequence: "DWI + MPRAGE T1"
      preprocessing_pipeline: "SPM12 co-registration; MRICloud automated parcellation; lesion overlay to calculate %ROI damaged"
      reference_space: "MNI152"
      atlases_used:
        - "MRICloud multi-atlas parcellation"
      coordinates_reported: []

    replications: []
    contradictions: []

    author_limitations:
      - "Small sample; LASSO may overfit."
      - "Left angular gyrus selected for action naming model but not independently significant (p=.728)."
      - "Left insula and total lesion volume were the model components associated with action naming (insula LASSO value=−0.015, not independently significant either)."

    evidence_quality: cohort
    strength: weak

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results – Neuroimaging results (Table 5, p.749)"
      confidence: high
      flags:
        - "PPA data NOT extracted (non-stroke etiology)"
        - "Left angular gyrus appears in LASSO action naming model with negative coefficient (LASSO=−0.405, more damage = worse performance) but is NOT independently significant (p=.728); direction coded `mixed` because the model selects the region but the coefficient does not reach individual significance"
        - "Left insula also selected by LASSO for action naming (LASSO value=−0.015, p=.92) — forward-looking: consider separate draft for left_insula__Breining2022 if desired"

    source_passages:
      - section: "Results – Neuroimaging results"
        page: 748
        supports: claim
        quote: >
          For the model of action naming, we found that larger percentage of tissue lesioned
          in the left angular gyrus and left insula were associated with worse performance
          on the HANA, as was larger total lesion volume. None of the covariates were
          independent, statistically significant predictors of action naming in acute stroke.
      - section: "Results – Neuroimaging results (Table 5)"
        page: 749
        supports: statistics
        quote: >
          Left angular gyrus −0.524 −0.555 <.001* −0.405 −0.487 0.728

source: extracted
notes: |
  PPA EXCLUSION: This paper includes both acute stroke (N=37 with imaging) and primary progressive
  aphasia (N=31 with imaging, N=138 behaviorally). Per extraction rules, PPA is a non-stroke
  etiology and is excluded from this draft. Only the acute stroke findings (Table 5) are extracted.
  This is documented in provenance.flags on both findings.

  The paper also reports left middle temporal gyrus associated with object naming only (LASSO
  value=−0.121, p=.397, not independently significant) and left insula + total lesion volume
  associated with action naming only. These are not independently statistically significant
  findings and are partially covered in f2 notes above. If desired, a separate draft for
  left_middle_temporal_gyrus__Breining2022 and left_insula__Breining2022 could be added.

  Method coded as MLPA (multivariate lesion-symptom — LASSO regression) rather than VLSM
  (univariate). The MRICloud ROI pipeline is atlas-based not voxel-wise.

  Citation info verified from paper: Aphasiology. 2022, Vol. 36, No. 6, 732–760.
  DOI: 10.1080/02687038.2021.1907291
---
