---
schema_version: 2.3
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
aliases:
- severity
- aphasia severity
- baseline severity
- severity metric
- WAB-AQ
- WAB AQ
- Aphasia Quotient
- Western Aphasia Battery Aphasia Quotient
- BDAE severity
- CAT severity
- AAT severity
- aphasia severity rating
- severity at intake
- pre-treatment severity
- initial aphasia severity
kind: predictor
predictor_type: behavioural
short_definition: Standardised score of overall aphasia severity. The exact instrument
  varies across studies (WAB-AQ, BDAE, CAT, AAT, Aphasia Severity Rating Scale, etc.);
  this entry holds findings from any of them and disambiguates per-finding via the
  `instrument` field.
assessment:
- WAB-R Aphasia Quotient (WAB-AQ, 0–100)
- BDAE Severity Rating (0–5)
- Comprehensive Aphasia Test (CAT)
- Aachen Aphasia Test (AAT)
- Aphasia Severity Rating Scale (ASRS, 0–5)
- Token Test
units: varies by instrument — see `instrument` field on each finding
typical_range: WAB-AQ 0–100 (cut-off ~93.8); BDAE 0–5 (5 = no aphasia)
direction_of_severity: lower_is_worse
status: approved
reviewer: human:michele
reviewed_on: 2026-05-01
created_by: human:michele
created_on: 2026-05-01
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  instrument: WAB-R AQ (0–100; continuous regression target)
  score_band: full severity range including very severe (<20); majority moderate-to-mild
  interpretation: Multimodal SVR combining resting-state functional connectivity and
    structural integrity (percent spared white matter) with demographics achieves
    significantly better WAB-R AQ prediction than any single-modality model (r=0.73,
    RMSE=15.82), demonstrating that aphasia severity reflects both functional network
    disruption and structural damage beyond lesion location and volume alone.
  claim: A multimodal SVR model combining demographics, percent spared white matter,
    and resting-state fMRI functional connectivity significantly outperforms any single-modality
    model for predicting WAB-R AQ in post-stroke aphasia, achieving r=0.73 and RMSE=15.82
    in 11-fold nested cross-validation.
  direction: likely
  relationship: correlational
  citation: '@Hu2025'
  method: computational_model
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 76
    population: post-stroke aphasia; left hemisphere strokes
    time_post_onset: not_reported
    age_range: 35–80 years
    handedness: not_reported
    language: not_reported
    recruitment: Boston University Center for Brain Recovery (Kiran lab); two cohorts
      combined.
    inclusion_criteria: post-stroke aphasia; ages 35–80; at least high school education;
      eligible for MRI; able to perform MRI tasks; complete multimodal neuroimaging
      data.
    exclusion_criteria: ineligible for MRI; comorbid neurological conditions; unable
      to perform MRI tasks; incomplete neuroimaging data.
  statistics:
    threshold: two-tailed Wilcoxon signed-rank tests comparing optimal vs single-modality
      models; α=0.05; primary metric RMSE
    effect_size: 'optimal SVR (DM+PSW+rsFMRI-FC): r=0.73 (SD=0.13), RMSE=15.82 (SD=5.21);
      rsFMRI-FC alone: r=0.70 (SD=0.13), RMSE=16.38 (SD=5.57)'
    ci_95: not_reported
    p_value: optimal model significantly outperforms single-modality rsFMRI-FC model
      (p<0.05; exact p not reported)
  confounders_controlled:
  - 11-fold outer cross-validation with 100 inner validation-training folds for hyperparameter
    tuning
  - Recursive Feature Elimination (RFE) applied within inner folds only (no data leakage)
  - class-weighted loss not applicable to regression (SVR minimises hinge loss)
  confounders_not_controlled:
  - sex (more male than female participants — potential bias)
  - age (range 35–80; not explicitly covaried)
  - pipeline mismatch between Cohort 1 (ITK-SNAP) and Cohort 2 (MRIcron) for lesion
    segmentation and DTI preprocessing
  - severe aphasia patients (WAB-AQ <20) poorly predicted — SVR insensitive to minority
    subgroup
  region_definition:
    kind: not_reported
    description: No single region anchor — features derived from atlas-based parcellations
      (AAL3 for GM/rsfMRI ROIs; BCBToolkit for WM tracts; ICBM152 for DTI tractography).
      Feature selection applied at predictor (modality) level, not at individual region
      level for the primary finding.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: MEMPRAGE
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 2530
      TE_ms: 1.69
    - modality: T2
      sequence: T2-SPACE FLAIR
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 6000
      TE_ms: 456
    - modality: DTI
      voxel_size_mm:
      - 2
      - 2
      - 2
      TR_ms: 3100
      TE_ms: 80.8
      n_directions: not_reported
      b_values: not_reported
    - modality: rsfMRI
      sequence: EPI
      voxel_size_mm: not_reported
      TR_ms: not_reported
      TE_ms: not_reported
    preprocessing_pipeline: 'Structural: T1 MEMPRAGE + T2-SPACE FLAIR; lesion segmentation
      semi-automated (Cohort 1: ITK-SNAP) or manual (Cohort 2: MRIcron). Percent spared
      GM/WM: AAL3 (83 LH GM regions) + BCBToolkit Tractotron (36 WM tracts). DTI:
      atlas-based tractography (ICBM152_adult via DSI Studio); FA extracted per tract.
      rsfMRI: CONN toolbox preprocessing (realignment, MNI normalization, band-pass
      filtering 0.01–0.1 Hz, regression of WM/CSF/motion); ROI-to-ROI FC matrix (50
      AAL3 ROIs, Fisher-z transformed, 625 intrahemispheric + homologous connections).'
    reference_space: MNI152
    atlases_used:
    - AAL3 (Automated Anatomical Labelling Atlas 3; Rolls et al. 2020)
    - BCBToolkit Tractotron (36 WM tracts)
    - ICBM152_adult (for DTI tractography)
    coordinates_reported: []
  replications:
  - '@Kristinsson2025'
  contradictions: []
  author_limitations:
  - Small sample size (n=76) relative to number of features; addressed via nested
    cross-validation and supervised feature selection.
  - Greater proportion of male participants may bias results.
  - Pipeline mismatch between Cohort 1 and Cohort 2 for lesion segmentation and DTI
    preprocessing introduces variability.
  - SVR poorly predicts severe aphasia (WAB-AQ <20) — minority class problem.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results — Model performance (pages 7–9)
    confidence: high
    flags:
    - Boston University CBR (Kiran lab) cohort — distinct from USC/MUSC and PLORAS
      cohorts; no overlap risk.
    - Pipeline mismatch between Cohort 1 (ITK-SNAP) and Cohort 2 (MRIcron) lesion
      segmentation is a reported limitation.
    - SVR poorly predicts severe aphasia (WAB-AQ <20) — minority subgroup underrepresented.
  source_passages:
  - section: Abstract
    page: 1
    quote: The SVR model outperformed RF, achieving an average root mean square error
      (RMSE) of 16.38 ± 5.57, Pearson's correlation coefficient (r) of 0.70 ± 0.13,
      and mean absolute error (MAE) of 12.67 ± 3.27
    supports: statistics
  - section: Results (Table 2)
    page: 8
    quote: DM PSW rsFMRI-FC
    supports: statistics
  - section: Abstract
    page: 1
    quote: The statistically significant difference in performance between the model
      using only single modality and the optimal multi-modal SVR/RF model (which included
      both resting-state connectivity and structural information) underscores that
      aphasia severity is influenced by factors beyond lesion location and volume
    supports: claim
  - section: Methods — Participants
    page: 3
    quote: between the ages of 35 and 80 years, and had received at least a high school
      education
    supports: sample
  - section: Methods — MRI acquisition
    page: 3
    quote: Images were acquired using Siemens 3.0T Prisma scanners. Structural images
      were acquired for all participants using the T1 MEMPRAGE (176 sagittal slices,
      1 mm × 1 mm × 1 mm voxel size, TR = 2530 ms, TE1 = 1.69 ms, TI = 1100 ms, flip
      angle = 7°) sequence
    supports: imaging_details
  - section: Limitations
    page: 11
    quote: our research faces limitations due to the small sample size of multimodal
      imaging data, despite adequately representing aphasia patient heterogeneity,
      and the greater number of male compared to female participants, which could
      bias the results
    supports: limitation
- id: f2
  target: severity_metric
  target_kind: predictor
  instrument: WAB-R AQ (0–100; continuous)
  score_band: full range
  interpretation: Feature selection across 11 outer cross-validation folds consistently
    identifies resting-state functional connectivity (particularly bilateral language
    network and interhemispheric connections) and left hemisphere white matter tract
    integrity (left arcuate fasciculus posterior segment, fronto-insular tract) as
    the most important predictors of WAB-R AQ. These findings underscore the complementary
    role of functional network integrity and structural white matter preservation
    in predicting aphasia severity.
  claim: Resting-state fMRI functional connectivity (selected in all top-10 SVR models)
    and left arcuate fasciculus posterior segment / fronto-insular tract integrity
    (selected in all 11 outer folds) are the most consistently selected features for
    WAB-R AQ prediction, with bilateral language network connectivity and interhemispheric
    connections emerging as key functional predictors.
  direction: likely
  relationship: correlational
  citation: '@Hu2025'
  method:
  - computational_model
  - fMRI_FC
  - DTI
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 76
    population: post-stroke aphasia; left hemisphere strokes
    time_post_onset: not_reported
    age_range: 35–80 years
    handedness: not_reported
    language: not_reported
    recruitment: Boston University Center for Brain Recovery.
    inclusion_criteria: post-stroke aphasia; ages 35–80; complete multimodal imaging.
    exclusion_criteria: ineligible for MRI; comorbid neurological conditions; incomplete
      imaging.
  statistics:
    threshold: 'feature selection frequency: selected in all 11/11 outer folds = maximum
      consistency; SHAP value for rsFMRI-FC = 3.65 (highest of all 7 predictor classes)'
    effect_size: rsFMRI-FC SHAP value = 3.65 (SVR model); left arcuate posterior +
      fronto-insular tract selected 11/11 outer folds; left arcuate FA + left uncinate
      FA selected 11/11 folds
    ci_95: not_reported
    p_value: not_reported (feature selection frequencies, not inferential tests)
  confounders_controlled:
  - RFE applied within inner cross-validation folds to prevent feature selection from
    accessing test data
  confounders_not_controlled:
  - feature importance derived from RFE + SHAP — explanatory, not causal
  - pipeline mismatch between cohorts for DTI preprocessing
  region_definition:
    kind: data_driven_cluster
    description: 'rsFMRI-FC features: ROI-to-ROI functional connectivity among 50
      pre-selected AAL3 ROIs spanning language, default mode, dorsal attention, and
      salience networks; 625 Fisher-z values retained after excluding non-homologous
      interhemispheric pairs. Most frequently selected FC connections involved bilateral
      language network and homologous interhemispheric pairs. PSW features: left arcuate
      fasciculus posterior segment (Fronto Insular Tract 5 left) selected 11/11 folds.
      FA features: left arcuate fasciculus and left uncinate fasciculus selected 11/11
      folds; left IFOF and left ILF selected 10/11 folds.'
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: rsfMRI
      sequence: EPI
      voxel_size_mm: not_reported
      TR_ms: not_reported
    - modality: DTI
      voxel_size_mm:
      - 2
      - 2
      - 2
      TR_ms: 3100
      TE_ms: 80.8
      n_directions: not_reported
    preprocessing_pipeline: 'rsfMRI: CONN toolbox; MNI normalization; band-pass filter
      0.01–0.1 Hz; WM/CSF/motion regression; 50 AAL3 ROI-to-ROI FC matrix (Fisher-z).
      DTI: DSI Studio; atlas-based tractography (ICBM152_adult); typology-informed
      pruning; FA extracted per tract.'
    reference_space: MNI152
    atlases_used:
    - AAL3
    - BCBToolkit Tractotron
    - ICBM152_adult
    coordinates_reported: []
  replications:
  - '@Marchina2011'
  contradictions: []
  author_limitations:
  - Feature selection frequencies indicate consistency, not causal importance.
  - Pipeline mismatch between cohorts for DTI preprocessing may have weakened FA predictor
    contribution.
  - rsFMRI-FC is a high-dimensional predictor (625 features) subject to overfitting
    despite RFE.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results — Resting-state functional connectivity; Results (Table
      3) (pages 9–10)
    confidence: high
    flags:
    - Feature selection frequencies (11/11 outer folds) are consistency indicators,
      not inferential statistics.
    - Pipeline mismatch between cohorts for DTI preprocessing may weaken FA predictor
      contribution.
  source_passages:
  - section: Results — Resting-state functional connectivity
    page: 9
    quote: FC emerges as a crucial feature
    supports: claim
  - section: Results — Resting-state functional connectivity
    page: 9
    quote: rsFMRI-FC has the highest SHAP value of 3.65
    supports: statistics
  - section: Results (Table 3)
    page: 9
    quote: SVR PSW Fronto insular tract5
    supports: statistics
  - section: Results (Table 3)
    page: 9
    quote: SVR FA Left arcuate fasciculus
    supports: statistics
  - section: Discussion — Features important to aphasia severity
    page: 10
    quote: selected rsFMRI-FC features for SVR models revealed
    supports: claim
  - section: Methods — MRI acquisition
    page: 3
    quote: DTI sequence was also completed
    supports: imaging_details
  - section: Limitations
    page: 11
    quote: data from Cohort 1 and Cohort 2 were processed using different pipelines
      for both lesion segmentation and DTI preprocessing
    supports: limitation
- id: f3
  target: severity_metric
  target_kind: predictor
  instrument: 'WAB-R Aphasia Quotient (binary: severe WAB-AQ <50 vs non-severe ≥50)'
  score_band: severe = WAB-AQ <50 (35% of sample); non-severe = WAB-AQ ≥50
  interpretation: 3D CNN trained on whole-brain morphometry (tissue volumes + lesion
    anatomy) classifies severe vs non-severe chronic aphasia with significantly better
    accuracy than classical machine learning (SVM), demonstrating that distributed
    three-dimensional morphometry patterns beyond the lesion independently predict
    aphasia severity.
  claim: A 3D convolutional neural network applied to whole-brain morphometry (tissue
    volumes from T1/T2) and lesion anatomy predicts severe post-stroke aphasia (WAB-AQ
    <50) with significantly higher balanced accuracy and F1 score than support vector
    machines, achieving median balanced accuracy of 77% and F1 of 0.70 in chronic
    stroke patients.
  direction: likely
  relationship: correlational
  citation: '@Teghipco2024'
  method: computational_model
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 231
    population: chronic post-stroke aphasia; left hemisphere stroke
    time_post_onset: chronic (time post-stroke not precisely reported; imaging within
      10 days of WAB-R evaluation)
    age_range: not_reported
    handedness: not_reported
    language: not_reported
    recruitment: University of South Carolina and Medical University of South Carolina
      (Siemens 3T Prisma).
    inclusion_criteria: post-stroke aphasia; left hemisphere stroke; WAB-R assessment
      available.
    exclusion_criteria: not_reported
  statistics:
    threshold: paired t-test across 20 repeats of cross-validation (stratified, nested)
    effect_size: CNN F1 M=0.70, SD=0.01; balanced accuracy M=0.77, SD=0.01; Cohen's
      d=2.24 (CNN vs linear SVM on F1)
    ci_95: not_reported
    p_value: 'CNN vs SVM F1: t(19)=-10, p=5.26e-9; balanced accuracy: t(19)=-9.8,
      p=7.28e-9'
  confounders_controlled:
  - cross-validation stratified by WAB-R aphasia category (very severe/severe/moderate/mild)
  - 20 repeats of cross-validation to capture data-partitioning noise
  - enantiomorphic healing to control for normalization artefacts from large lesions
  confounders_not_controlled:
  - age (not reported as a covariate)
  - sex (not covaried)
  - time post-stroke (not covaried)
  - lesion volume (included as a morphometric feature, not as a covariate to be controlled)
  region_definition:
    kind: data_driven_cluster
    description: No single region anchor — whole-brain 8mm downsampled morphometric
      map (grey matter, white matter, CSF, lesion) in MNI152 space used as CNN input.
      Region importance assessed via Grad-CAM++ saliency maps and SHAP values averaged
      across 20 cross-validation repeats.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: MPRAGE
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 2250
      TE_ms: 4.11
    - modality: T2
      sequence: 3D SPACE
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 3200
      TE_ms: 567
    preprocessing_pipeline: Lesion manually segmented on T2 in MRIcron; resampled
      to T1 using nii_preprocess + SPM8; enantiomorphic healing (intact contralateral
      tissue fills lesion boundary). Healed T1 segmented into WM/GM/CSF using FAST;
      normalized to MNI152 2mm with fsl_anat/FNIRT; tissue + lesion maps merged into
      ordinal morphometric map; downsampled to 8mm voxels; scaled to [-1,1].
    reference_space: MNI152
    atlases_used: []
    coordinates_reported: []
  replications: []
  contradictions: []
  author_limitations:
  - Sample size modest by deep learning standards — patterns consistent across cross-validation
    repeats but replication in larger independent samples needed.
  - Cross-sectional design using chronic data — cannot model recovery trajectory;
    longitudinal data would be needed for clinical deployment.
  - CNN complexity precludes human-interpretable explanation of exactly which feature
    combinations drive predictions.
  - Preprocessing was semi-automated; higher-quality automated pipelines may be needed
    for clinical deployment.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results — Evaluating the quality of CNN model predictions (pages
      7–9)
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2018, @Yourganov2015Predicting, @Kristinsson2025
      (same USC/MUSC Aphasia Lab infrastructure); flag for double-counting.
  source_passages:
  - section: Abstract
    page: 1
    quote: CNNs achieve higher balanced accuracy and F1 scores, even when SVMs are
      nonlinear or integrate linear or nonlinear dimensionality reduction
    supports: claim
  - section: Results — Evaluating the quality of CNN model predictions against classical
      machine learning
    page: 7
    quote: worse F1 scores (M = 0.65, SD = 0.02) compared to CNNs
    supports: statistics
  - section: Results — Evaluating the quality of CNN model predictions against classical
      machine learning
    page: 7
    quote: SVMs mean accuracy was worse (M = 0.73, SD = 0.01) than CNNs (M = 0.77,
      SD = 0.01), t(19) = −9.8, p = 7.28e−9, Cohen's d = −2.2
    supports: statistics
  - section: Methods — Imaging data
    page: 3
    quote: Magnetic Resonance Imaging (MRI) was performed at the University of South
      Carolina or Medical University of South Carolina using a Siemen's 3T Prisma
      (upgraded from Trio to FIT in 2016) equipped with a 20-channel RF receiver head/neck
      coil
    supports: imaging_details
  - section: Methods — Image preprocessing
    page: 3
    quote: Healed T1 scans were segmented (binary) into volumes containing white matter,
      gray matter, and cerebrospinal fluid using FAST
    supports: imaging_details
  - section: Methods — Image preprocessing
    page: 3
    quote: The same healed T1 scans were normalized to the MNI152 (2 mm) template
      distributed with FMRIB Software Library (FSL) using the fsl_anat pipeline
    supports: imaging_details
  - section: Abstract
    page: 1
    quote: we test whether deep learning with Convolutional Neural Networks (CNNs)
      on whole brain morphometry (i.e., segmented tissue volumes) and lesion anatomy
      better predicts chronic stroke individuals with severe aphasia (N = 231)
    supports: sample
  - section: Discussion
    page: 11
    quote: in modest samples of chronic stroke patients, deep learning can be effective
    supports: limitation
- id: f4
  target: severity_metric
  target_kind: predictor
  instrument: 'WAB-R Aphasia Quotient (binary: severe <50 vs non-severe ≥50)'
  score_band: severe = WAB-AQ <50; non-severe = WAB-AQ ≥50
  interpretation: Right hemisphere morphometry is the strongest CNN-identified predictor
    of severe aphasia; left hemisphere morphometry predicts non-severe aphasia. Saliency
    maps show significantly higher Grad-CAM++ attention to all right hemisphere regions
    for severe predictions and to all left hemisphere regions for non-severe predictions,
    indicating that distributed contralateral morphometry patterns are key to classifying
    severe aphasia beyond lesion location.
  claim: CNN saliency maps reveal that right hemisphere morphometry is significantly
    more predictive of severe aphasia (WAB-AQ <50) while left hemisphere morphometry
    is more predictive of non-severe aphasia, with distinct subgroups showing individualized
    patterns implicating language, attention, and aging networks beyond the canonical
    language system.
  direction: likely
  relationship: correlational
  citation: '@Teghipco2024'
  method: computational_model
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 231
    population: chronic post-stroke aphasia; left hemisphere stroke
    time_post_onset: chronic
    age_range: not_reported
    handedness: not_reported
    language: not_reported
    recruitment: University of South Carolina and Medical University of South Carolina.
    inclusion_criteria: post-stroke aphasia; left hemisphere stroke; WAB-R available.
    exclusion_criteria: not_reported
  statistics:
    threshold: two-sample t-tests on ROI-normalized saliency; p<0.0001 for all left
      and right hemisphere ROI comparisons
    effect_size: not_reported (significant for all ROIs; exact values in supplementary)
    ci_95: not_reported
    p_value: <0.0001 for all left and right hemisphere regions
  confounders_controlled:
  - ROI saliency maps normalised to sum to 1 (removes absolute-saliency confound)
  confounders_not_controlled:
  - lesion size (correlated with severity — SVMs showed this, CNN went beyond it)
  - age (not explicitly modelled as covariate)
  region_definition:
    kind: data_driven_cluster
    description: Regions of interest defined as lesion, perilesional, extralesional,
      and their right-hemisphere homologs. Grad-CAM++ saliency maps from CNN averaged
      across cross-validation repeats, then compared between severe and non-severe
      predictions using two-sample t-tests. Subtype clustering (consensus clustering
      of saliency maps) revealed 7 severe and 6 non-severe subgroups with distinct
      morphometry patterns.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: MPRAGE
      voxel_size_mm:
      - 1
      - 1
      - 1
    - modality: T2
      sequence: 3D SPACE
      voxel_size_mm:
      - 1
      - 1
      - 1
    preprocessing_pipeline: Same as f1 — enantiomorphic healing, FAST segmentation,
      FNIRT/MNI152 normalization, 8mm downsampling. Saliency maps computed via Grad-CAM++
      on last convolutional layer across 20 cross-validation repeats.
    reference_space: MNI152
    atlases_used: []
    coordinates_reported: []
  replications: []
  contradictions: []
  author_limitations:
  - Saliency maps from different explainability methods (Grad-CAM++ vs SHAP) highlighted
    different features — incontrovertible feature importance is difficult to determine.
  - Subtype clustering exploratory — cluster membership not independently validated.
  - Meta-analytic decoding of saliency maps is indirect and relies on Neurosynth associations.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results — ROI analysis; Discussion — Subtyping (pages 9–14)
    confidence: high
    flags:
    - Saliency-based findings are exploratory — cluster membership not independently
      validated.
    - cohort overlaps with @Fridriksson2018, @Yourganov2015Predicting, @Kristinsson2025.
  source_passages:
  - section: Results — Evaluating the quality of CNN model predictions (ROI analysis)
    page: 9
    quote: higher in all left hemisphere regions for
    supports: claim
  - section: Results — Evaluating the quality of CNN model predictions (ROI analysis)
    page: 9
    quote: saliency was significantly higher in all right hemisphere regions for severe
      predictions (all p < 0.0001)
    supports: statistics
  - section: Discussion
    page: 13
    quote: Attention to right hemisphere morphometry is consistent with contemporary
      models of aphasia recovery, which tend to emphasize worsening aphasia as damage
      spills out of core language regions and into non-language left and right hemisphere
      regions
    supports: claim
  - section: Discussion
    page: 14
    quote: Subgroups emphasized different subsystems, including semantics when anterior
      temporal pole
    supports: claim
  - section: Abstract
    page: 1
    quote: we test whether deep learning with Convolutional Neural Networks (CNNs)
      on whole brain morphometry (i.e., segmented tissue volumes) and lesion anatomy
      better predicts chronic stroke individuals with severe aphasia (N = 231)
    supports: sample
  - section: Discussion
    page: 12
    quote: CNNs can be successfully deployed outside their current niche
    supports: limitation
- id: f5
  target: severity_metric
  target_kind: predictor
  instrument: CAT spoken picture description (aphasic vs non-aphasic binary)
  score_band: 'binary: aphasic vs non-aphasic'
  interpretation: Three tabular clinical features — initial aphasia severity, left
    hemisphere lesion size, and time post-stroke (recovery time) — each independently
    and significantly predict post-stroke spoken language recovery; together they
    achieve balanced accuracy of 0.813 in a logistic regression model, with initial
    severity and recovery time incrementally adding predictive value beyond lesion
    size alone.
  claim: Initial aphasia severity, left hemisphere lesion size, and recovery time
    are each independently significant predictors of post-stroke spoken picture description
    ability; logistic regression combining all three achieves balanced accuracy of
    0.813 in stroke survivors assessed months to years post-stroke.
  direction: likely
  relationship: correlational
  citation: '@White2024'
  method: computational_model
  design: cross-sectional
  imaging: T1
  sample:
    n: 758
    population: stroke survivors (bilateral, left-sided, or right-sided strokes) from
      the PLORAS database
    time_post_onset: months to years post-stroke; matched for recovery time across
      5 groups
    age_range: mean age at stroke 56.1 years
    handedness: not_reported
    language: English speaking
    recruitment: PLORAS database (Predicting Language Outcome and Recovery After Stroke;
      Seghier et al. 2016), UCL Wellcome Centre for Human Neuroimaging.
    inclusion_criteria: English-speaking stroke survivors; MRI and tabular data available;
      spoken picture description score collected.
    exclusion_criteria: not_reported
  statistics:
    threshold: 'logistic regression; all three tabular features statistically significant
      (p<0.001); note: high degrees of freedom inflates p-values'
    effect_size: 'balanced accuracy: lesion size alone 0.678; + initial severity 0.757;
      + recovery time 0.813'
    ci_95: not_reported
    p_value: <0.001 for all three tabular features in logistic regression
  confounders_controlled:
  - five-group matched partition (matched for recovery time, initial severity, left
    lesion size, and spoken description score)
  - lock-box test set (fifth group) held out until final evaluation
  confounders_not_controlled:
  - age (mean 56.1 years; not covaried)
  - sex (male:female ratio 2.3:1; not covaried)
  - stroke laterality (bilateral, left, or right included; analyses focused on left
    lesion size)
  - aphasia type (not specified)
  region_definition:
    kind: not_reported
    description: Behavioural-only logistic regression finding — no specific brain
      region anchored. Left lesion size was quantified as the count of damaged voxels
      in the left hemisphere binary lesion image (ALI automated lesion identification;
      Seghier et al. 2008), not region-specific.
  imaging_details:
    field_strength: 1.5T and 3T
    acquisition:
      sequence: T1 MPRAGE (1 mm isotropic); repetition time/echo time/inversion time
        = 12.24/3.56/530 ms at 1.5T and 7.92/2.48/910 ms at 3T
      voxel_size_mm:
      - 1
      - 1
      - 1
    preprocessing_pipeline: SPM (Penny et al. 2011); spatial normalization to MNI
      using unified segmentation (Ashburner & Friston 2005; Crinion et al. 2007) optimized
      for focal brain lesions via an extra lesioned-tissue class (Seghier et al. 2008;
      ALI approach). Left lesion size = number of damaged voxels in left hemisphere
      binary lesion image.
    reference_space: MNI152
    atlases_used: []
    coordinates_reported: []
  replications: []
  contradictions: []
  author_limitations:
  - Initial severity assessed by patient report (not a standardised battery score),
    introducing measurement variability.
  - Only one coarse imaging variable (lesion size) included in the logistic regression
    baseline — spatial patterns not captured.
  - High degrees of freedom in logistic regression inflates statistical significance
    — p<0.001 thresholds should be interpreted cautiously.
  - MRI data restricted to research-quality scanners — may not generalize to clinical
    scans.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results (pages 7–8)
    confidence: high
    flags:
    - PLORAS cohort (UCL) is distinct from USC/MUSC and Boston University cohorts
      — no overlap with other extracted papers.
    - Initial severity measured by patient self-report, not standardised battery —
      introduces measurement variability.
  source_passages:
  - section: Results
    page: 7
    quote: If the logistic regression was run just with 'left lesion size' as the
      independent variable, the balanced accuracies dropped to 0.678/0.694 (all patients/patients
      with initial severity severe and moderate). Adding 'initial severity' increased
      the balanced accuracies to 0.757/0.706; further adding 'recovery time' gave
      balanced accuracies of 0.813/0.780
    supports: statistics
  - section: Results
    page: 7
    quote: All three tabular features were statistically significant (p < 0.001) although,
      these significant findings are, to some extent, carried by the very high degrees
      of freedom associated with these tests
    supports: statistics
  - section: Methods — Dataset
    page: 3
    quote: The participants were 758 S survivors from the PLORAS database (Seghier
      et al., 2016). The male to female ratio was 2.3:1, and the average age at stroke
      was 56.1
    supports: sample
  - section: Methods — Dataset
    page: 3
    quote: 'Three PLORAS tabular features were identified a priori as being of prognostic
      relevance to recovery from aphasia: (i) Initial severity of aphasia after stroke;
      (ii) Left hemisphere lesion size; (iii) Recovery time'
    supports: method
  - section: Limitations
    page: 10
    quote: MRI data was restricted to research quality scanners
    supports: limitation
- id: f6
  target: severity_metric
  target_kind: predictor
  instrument: CAT spoken picture description (aphasic vs non-aphasic binary)
  score_band: 'binary: aphasic vs non-aphasic'
  interpretation: Combining MRI ROI features with symbolic tabular data in a ResNet-18
    CNN (Hybrid ROI model) achieves the highest balanced accuracy of approximately
    0.85, significantly outperforming logistic regression with tabular data alone
    (balanced accuracy 0.813), demonstrating that spatial MRI information provides
    an incremental but significant predictive gain for post-stroke language recovery.
  claim: A ResNet-18 CNN trained on hybrid images combining MRI ROIs with symbolic
    tabular representations (initial severity, lesion size, recovery time) achieves
    the highest classification accuracy for post-stroke spoken language recovery in
    the PLORAS cohort, significantly outperforming logistic regression and all other
    CNN architectures (balanced accuracy ~0.85, statistically significant improvement
    over baseline).
  direction: likely
  relationship: correlational
  citation: '@White2024'
  method: computational_model
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 758
    population: stroke survivors from the PLORAS database
    time_post_onset: months to years post-stroke
    age_range: mean age at stroke 56.1 years
    handedness: not_reported
    language: English speaking
    recruitment: PLORAS database; UCL Wellcome Centre for Human Neuroimaging.
    inclusion_criteria: English-speaking stroke survivors; MRI and tabular data available.
    exclusion_criteria: not_reported
  statistics:
    threshold: FDR-corrected paired comparison; 20 random seed repeats per model
    effect_size: balanced accuracy improvement ~0.04 over logistic regression baseline
      (from ~0.813 to ~0.85); statistically significant (FDR corrected; see appendix
      A2)
    ci_95: not_reported
    p_value: FDR-corrected significant (exact p not reported in main text)
  confounders_controlled:
  - single lock-box test set (fifth group) accessed only once after all hyperparameter
    tuning
  - five-group matched partition design
  - 20 random seed repeats to capture variability
  confounders_not_controlled:
  - age, sex, stroke laterality (not covaried)
  - single lock-box only used once — multiple-algorithm comparison inflates best-model
    accuracy
  region_definition:
    kind: data_driven_cluster
    description: ROI images derived from MRI using CLEAR Image explainable AI (perturbation-based;
      Brainnetome atlas ROIs). Hybrid ROI images stitch MRI ROI features with symbolic
      pixel representations of tabular data (initial severity, left lesion size, recovery
      time). CLEAR Image feature importance identifies key ROIs; exact ROI identities
      not reported as primary finding — model designed to identify combinations rather
      than dominant individual regions.
  imaging_details:
    field_strength: 1.5T and 3T
    acquisition:
      sequence: T1 MPRAGE; 1 mm isotropic
      voxel_size_mm:
      - 1
      - 1
      - 1
    preprocessing_pipeline: 'SPM unified segmentation + ALI lesion identification;
      spatial normalization to MNI. Stitched MRI: 64 MRI slices downsized to 256×256
      images. ROI images: parcellated via brain atlas into regions of interest. Hybrid
      ROI images: ROI features combined with symbolic pixel representations of tabular
      data. ResNet-18 pretrained on ImageNet, fine-tuned with 4-fold cross-validation
      (lock-box held out).'
    reference_space: MNI152
    atlases_used:
    - Brainnetome (for ROI parcellation; implied by CLEAR Image method)
    coordinates_reported: []
  replications: []
  contradictions: []
  author_limitations:
  - Explainable AI methods (CLEAR Image, Grad-CAM, LIME) differ in their feature importance
    explanations — incontrovertible feature importance is difficult to determine.
  - Study does not explain which combination of damage drives predictions — focuses
    on classification accuracy, not mechanistic insight.
  - Dataset is small by machine learning standards — deep learning benefits may increase
    with larger samples.
  - 'Single lock-box approach: choosing best algorithm from multiple on same lock-box
    inflates accuracy estimate.'
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results (pages 7–8); Methods — Dataset (pages 3–4)
    confidence: high
    flags:
    - Single lock-box test set evaluated by multiple algorithms — best-model accuracy
      may be optimistically inflated.
    - PLORAS cohort (UCL) is distinct from USC/MUSC and Boston University cohorts
      — no overlap with other extracted papers.
  source_passages:
  - section: Results
    page: 7
    quote: The best results came from using the ResNet-18 with the Hybrid ROI images,
      improving balanced accuracy by approximately 0.04 compared to the baseline logistic
      regression
    supports: claim
  - section: Results
    page: 7
    quote: This difference was also statistically significant (false discovery rate
      corrected for multiple comparisons); see appendix A2
    supports: statistics
  - section: Methods — Dataset
    page: 3
    quote: The participants were 758 S survivors from the PLORAS database (Seghier
      et al., 2016). The male to female ratio was 2.3:1, and the average age at stroke
      was 56.1
    supports: sample
  - section: Methods — Dataset
    page: 4
    quote: 'isotropic voxels: repetition time/echo time/inversion time = 12.24/3.56/530
      ms and 7.92/2.48/910 ms at 1.5 T and 3 T, respectively'
    supports: imaging_details
  - section: Discussion
    page: 8
    quote: we are not claiming to have established that deep learning substantially
      outperforms more traditional methods
    supports: limitation
  - section: Limitations
    page: 10
    quote: MRI data was restricted to research quality scanners
    supports: limitation
notes: "This is the umbrella entry for *any* finding about how aphasia severity predicts\
  \ an outcome. Different studies use different instruments (WAB-AQ, BDAE severity,\
  \ CAT, AAT, …); rather than fragmenting the literature into one predictor entry\
  \ per instrument — which would also fragment the user's prognostic query when their\
  \ patient was tested with a different battery — we keep one entry and tag each finding\
  \ with its `instrument`, `score_band`, and a plain-language `interpretation`.\n\
  When extracting:\n  * Use this entry whenever the paper reports overall aphasia\
  \ severity\n    as a predictor of an outcome, regardless of instrument.\n  * On\
  \ each finding, fill `instrument` (e.g. \"WAB-AQ\", \"BDAE severity\"),\n    `score_band`\
  \ (e.g. \"WAB-AQ 50–75 (moderate)\"), and\n    `interpretation` (one sentence in\
  \ plain language).\n  * If the paper used a *subscale* of a battery (e.g. WAB Naming,\
  \ BDAE\n    Auditory Comprehension) and that subscale is the *predictor*, this\n\
  \    entry is fine — but consider whether a more specific predictor\n    entry (e.g.\
  \ `naming_score`) would be more accurate.\n\nWhen querying (`interpret_predictors`):\n\
  \  * The user supplies the patient's measured value and the instrument\n    that\
  \ produced it. The interpreter matches findings by\n    `severity_metric`, then\
  \ optionally filters / weights by matching\n    `instrument` (preferring exact-instrument\
  \ matches)."
last_reviewed: '2026-05-06'
---
# Aphasia severity metric (instrument-agnostic)

Aphasia severity is one of the most universally reported predictors in
the aphasia literature, but the field has not converged on a single
instrument. WAB-AQ dominates anglophone neuroscience papers; BDAE
severity ratings dominate older and clinical literature; CAT, AAT, and
the Token Test are more common in European and multilingual studies;
the Aphasia Severity Rating Scale appears in many therapy trials.

Putting all of these into a single `severity_metric` predictor entry
keeps the literature unified and lets a downstream interpreter answer
questions like *"my patient has a WAB-AQ of 65 — what does the
literature say about their prognosis?"* by:

1. Looking up findings on `severity_metric`.
2. Preferring findings whose `instrument` exactly matches the patient's
   instrument (WAB-AQ).
3. Falling back to findings on other instruments with a confidence
   penalty, so the user still sees the relevant evidence.

## Per-finding fields used by this entry

The optional v2.3 finding-level fields below are most useful inside
this entry (and any other predictor entry where the same construct can
be measured by multiple instruments):

| Field            | Example                                          |
|------------------|--------------------------------------------------|
| `instrument`     | `"WAB-AQ"`, `"BDAE severity"`, `"CAT"`, `"AAT"`  |
| `score_band`     | `"WAB-AQ 50–75 (moderate)"`, `"BDAE severity 2"` |
| `interpretation` | `"Moderate aphasia, intermediate prognosis"`     |

These three fields stay together — none is required, but if you fill
one, fill all three. They make per-finding filtering and per-patient
querying possible without forcing the schema to model every battery.
