---
schema_version: 2.3
id: bilateral_middle_frontal_gyrus_recovery
name: Bilateral Middle Frontal Gyrus and Right Temporo-Occipital MTG — Fluency Recovery
kind: classical
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
hemisphere: bilateral
aliases:
- bilateral MFG
- right temporo-occipital MTG
- right supramarginal gyrus
notes: 'Stefaniak et al. (2022, Brain) — longitudinal fMRI study of multidimensional
  aphasia recovery.

  n=26 individuals with mild-moderate aphasia following left hemispheric infarct.

  Scanned at 2 weeks (T1) and 4 months (T2) post-stroke.

  Task: overt speech production (Speech+Count > Rest).

  Analysis: mass univariate SPM, voxelwise activation change correlated with PC score
  change,

  controlled for baseline PC score (proportional recovery confound).

  Three orthogonal PCA components: PC1=fluency, PC2=semantic/executive, PC3=phonology.

  Citation key: @Stefaniak2022

  Journal: Brain 2022;145:1354-1367. DOI: 10.1093/brain/awab377

  This file contains 4 findings: f1 (fluency longitudinal), f2 (semantic/executive
  longitudinal),

  f3 (phonology longitudinal), f4 (fluency cross-sectional at T1).

  '
findings:
- id: f1
  target: fluency_recovery
  target_kind: impairment
  claim: Increasing activation in bilateral middle frontal gyri and right temporo-occipital
    MTG between 2 weeks and 4 months post-stroke is positively associated with fluency
    component recovery, even after controlling for baseline fluency severity.
  direction: likely
  relationship: recruitment
  citation: '@Stefaniak2022'
  method: fMRI_activation
  design: longitudinal
  imaging: fMRI
  sample:
    n: 26
    population: adults with mild-moderate aphasia following left hemispheric infarct
    time_post_onset: 2 weeks (T1) and 4 months (T2) post-stroke
    age_range: mean 59.0 years (SD 11.0)
    handedness: not_reported
    language: English (premorbidly fluent)
    recruitment: Recruited from acute stroke wards; previous publications used same
      dataset (Geranmayeh et al. 2016, 2017).
    inclusion_criteria: Left hemisphere infarct; language difficulties at stroke onset;
      premorbidly fluent English; no previous stroke with aphasia.
    exclusion_criteria: Previous stroke resulting in aphasia; other neurological condition.
  statistics:
    threshold: voxel-wise cluster-forming p < 0.005 (uncorrected), cluster-level p
      < 0.05 FWE corrected
    cluster_extent: not_reported
    effect_size: 'Before baseline control — left MFG: beta=0.29 P=0.0003; right temporo-occipital
      MTG: beta=0.16 P=0.04; right MFG: beta=0.30 P=0.0001. After baseline PC1 control
      — bilateral vmPFC: beta=0.38 P=0.0001; right temporo-occipital MTG: beta=0.23
      P=0.003'
    ci_95: not_reported
    p_value: P=0.0003 (left MFG); P=0.04 (right MTG); P=0.0001 (right MFG)
  confounders_controlled:
  - baseline fluency score (T1 PC1) included as covariate in robust regression — controls
    for proportional recovery confound
  - lesion volume (included in robust regression)
  - years of education (included in robust regression)
  - age (included in robust regression)
  - analyses restricted to grey matter voxels in which no patient had a lesion
  confounders_not_controlled:
  - stroke etiology (all ischemic left hemisphere; not further stratified)
  - specific lesion location (controlled by lesion-free mask but not explicit covariate)
  - head motion in fMRI (6 rigid-body motion parameters only)
  region_definition:
    kind: data_driven_cluster
    atlas: Harvard-Oxford cortical atlas; AAL for subcortical
    description: 'Clusters from SPM mass univariate analysis of activation change
      (T2 minus T1 contrast image) regressed on PC1 fluency change. Bilateral MFG:
      lateral prefrontal; right temporo-occipital MTG: posterior middle temporal gyrus
      adjacent to supramarginal gyrus.'
  imaging_details:
    field_strength: not_reported
    acquisition:
      sequence: Sparse fMRI design (EPI volumes between overt speech); T1-weighted
        structural
      voxel_size_mm: not_reported
      TR_ms: not_reported
      TE_ms: not_reported
    modalities:
    - modality: fMRI_task_activation
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford (cortical)
    - AAL (subcortical)
    preprocessing_pipeline: 'FSL + SPM12: realign, brain-extract, smooth, coregister,
      normalize; fixed-effect first-level GLM with 6 rigid-body motion regressors
      of no-interest'
    task:
      name: Overt speech production (sparse fMRI)
      description: Sparse fMRI design with EPI volumes acquired between overt speech
        responses; participants produced speech and counted aloud in alternating blocks
      contrasts:
      - Speech+Count > Rest
      baseline: Rest
  replications: []
  contradictions: []
  author_limitations:
  - Small sample (n=26 mild-moderate aphasia); findings should be replicated in independent
    sample.
  - Left hemisphere mostly excluded from analysis (lesion-free mask); may miss left
    hemisphere correlates.
  - Single fMRI contrast cannot distinguish fluency vs. phonology vs. semantics contributions.
  - Bilateral MFG not activated in controls — role as spare capacity vs. compensation
    unclear.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results — Activation change positively associated with fluency
      improvement; Discussion
    confidence: high
    flags:
    - Dataset previously used in Geranmayeh et al. 2016 (Neurology) and 2017 (Brain)
      for single-measure analyses; current PCA analyses are entirely new.
    - Bilateral MFG and right MTG findings are robust pre- and post-baseline-control.
    - Uncorrected cluster-forming threshold (p<0.005) with FWE at cluster level —
      standard SPM but not permutation testing.
  source_passages:
  - section: Abstract
    page: 1
    supports: claim
    quote: fluency recovery was associated with increasing activation in bilateral
      middle frontal gyri and right temporo-occipital middle temporal gyrus
  - section: Results — Activation change positively associated with fluency improvement
    page: 6
    supports: statistics
    quote: cluster 1 beta = 0.29, P = 0.0003; cluster 2 beta = 0.16, P = 0.04; cluster
      3 beta = 0.30, P = 0.0001
  - section: Results — Activation change positively associated with fluency improvement
    page: 6
    supports: statistics
    quote: cluster 1 beta = 0.38, P = 0.0001; cluster 2 beta = 0.23, P = 0.003
  - section: Methods — Participants
    page: 3
    supports: sample
    quote: Twenty-six patients had a full battery of language test data available
      and were included in this analysis
  - section: Methods — Statistical analysis
    page: 3
    supports: method
    quote: We used varimax-rotated PCA to reduce the patients' scores across all 16
      neuropsychological tests, to a smaller number of principal components
  - section: Methods — Functional MRI second-level analysis
    page: 4
    supports: imaging_details
    quote: Statistical thresholding used a voxel-wise cluster forming threshold of
      P < 0.005 (uncorrected) and a cluster-level threshold of P < 0.05 after familywise
      error correction
- id: f2
  target: semantic_executive_recovery
  target_kind: impairment
  claim: Decreasing activation in bilateral anterior temporal lobes between 2 weeks
    and 4 months post-stroke is associated with better semantic/executive recovery
    — a finding revealed only after controlling for baseline semantic/executive severity.
  direction: likely
  relationship: recruitment
  citation: '@Stefaniak2022'
  method: fMRI_activation
  design: longitudinal
  imaging: fMRI
  sample:
    n: 26
    population: adults with mild-moderate aphasia following left hemispheric infarct
    time_post_onset: 2 weeks (T1) and 4 months (T2) post-stroke
    age_range: mean 59.0 years (SD 11.0)
    handedness: not_reported
    language: English (premorbidly fluent)
    recruitment: Same cohort as f1.
    inclusion_criteria: Left hemisphere infarct; language difficulties at stroke onset.
    exclusion_criteria: Previous stroke with aphasia; other neurological condition.
  statistics:
    threshold: voxel-wise cluster-forming p < 0.005 (uncorrected), cluster-level p
      < 0.05 FWE
    cluster_extent: not_reported
    effect_size: 'Left ATL cluster (temporal pole, frontal medial, frontal pole):
      beta=-0.22 P=2.5e-7; Right ATL cluster (temporal pole, anterior MTG, posterior
      inferior temporal): beta=-0.28 P=8.0e-5'
    ci_95: not_reported
    p_value: P=2.5e-7 (left ATL); P=8.0e-5 (right ATL)
  confounders_controlled:
  - baseline semantic/executive score (T1 PC2) — critical covariate; without this
    NO clusters were found
  - lesion volume, years of education, age (robust regression)
  confounders_not_controlled:
  - specific semantic task demands (single Speech+Count>Rest contrast)
  region_definition:
    kind: data_driven_cluster
    atlas: Harvard-Oxford cortical atlas
    description: 'Bilateral ATL clusters. Left: temporal pole, frontal medial cortex,
      frontal pole. Right: temporal pole, anterior MTG, posterior inferior temporal
      gyrus. These are core regions of the bilateral semantic network hub (Lambon
      Ralph et al. 2017).'
  imaging_details:
    field_strength: not_reported
    acquisition:
      sequence: Sparse fMRI; same as f1
      voxel_size_mm: not_reported
      TR_ms: not_reported
      TE_ms: not_reported
    modalities:
    - modality: fMRI_task_activation
    reference_space: MNI152
    atlases_used: []
    software: FSL + SPM12
  replications: []
  contradictions: []
  author_limitations:
  - No clusters found before baseline control — this finding would have been missed
    in conventional analysis (false-negative).
  - 'Negative association may reflect efficiency: poorer recovery requires higher
    ATL activation to perform the task.'
  - Left hemisphere mask excludes much of left ATL.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results — Activation change negatively associated with semantic/executive
      change; Discussion
    confidence: high
    flags:
    - 'Key methodological finding: baseline-PC2 control revealed bilateral ATL clusters
      entirely absent without control — demonstrates importance of proportional-recovery
      confound adjustment.'
  source_passages:
  - section: Abstract
    page: 1
    supports: claim
    quote: semantic/executive recovery was associated with reducing activation in
      bilateral anterior temporal lobes
  - section: Results — Activation change negatively associated with semantic/executive
      change
    page: 6
    supports: statistics
    quote: cluster 1 beta = –0.22, P = 2.5  10–7; cluster 2 beta = –0.28, P = 8.0  10–5
  - section: Discussion
    page: 9
    supports: claim
    quote: no regions were associated with semantic/executive change before controlling
      for T1 score, yet bilateral ATL clusters were negatively associated with semantic/executive
      recovery after controlling for T1 score
- id: f3
  target: phonology_recovery
  target_kind: impairment
  claim: Decreasing activation in bilateral precentral gyri, dorso-medial frontal
    poles, and precuneus between 2 weeks and 4 months is associated with better phonology
    recovery, particularly in patients with low baseline phonological ability.
  direction: likely
  relationship: recruitment
  citation: '@Stefaniak2022'
  method: fMRI_activation
  design: longitudinal
  imaging: fMRI
  sample:
    n: 26
    population: adults with mild-moderate aphasia following left hemispheric infarct
    time_post_onset: 2 weeks (T1) and 4 months (T2) post-stroke
    age_range: mean 59.0 years (SD 11.0)
    handedness: not_reported
    language: English (premorbidly fluent)
    recruitment: Same cohort as f1.
    inclusion_criteria: Left hemisphere infarct; language difficulties at stroke onset.
    exclusion_criteria: Previous stroke with aphasia; other neurological condition.
  statistics:
    threshold: voxel-wise cluster-forming p < 0.005 (uncorrected), cluster-level p
      < 0.05 FWE
    cluster_extent: not_reported
    effect_size: 'Bilateral precentral/MFG/SFG (before control): beta=-0.27 P=8.3e-5;
      significant T1-PC3 x activation interaction P=0.0009. After baseline control:
      vmPFC beta=-0.28 P=0.0001; precuneus beta=-0.15 P=0.0002; frontal poles/midline
      SFG beta=-0.13 P=0.0006'
    ci_95: not_reported
    p_value: P=0.0001 (vmPFC); P=0.0002 (precuneus)
  confounders_controlled:
  - baseline phonology score (T1 PC3)
  - lesion volume, years of education, age (robust regression)
  confounders_not_controlled:
  - significant T1 PC3 x activation interaction means finding is moderated by baseline
    severity — not a simple main effect
  region_definition:
    kind: data_driven_cluster
    atlas: Harvard-Oxford cortical atlas; AAL subcortical
    description: 'Before baseline control: bilateral precentral gyrus, MFG, superior
      frontal gyrus. After baseline control: bilateral frontal poles and midline SFG;
      ventromedial prefrontal cortex (vmPFC — overlapping with fluency f1 cluster,
      opposing sign); precuneus (task-negative DMN region).'
  imaging_details:
    field_strength: not_reported
    acquisition:
      sequence: Sparse fMRI; same as f1
      voxel_size_mm: not_reported
      TR_ms: not_reported
      TE_ms: not_reported
    modalities:
    - modality: fMRI_task_activation
    reference_space: MNI152
    atlases_used: []
    software: FSL + SPM12
  replications: []
  contradictions: []
  author_limitations:
  - PC3 phonology scores did not significantly improve at group level (Wilcoxon P=0.38),
    reducing confidence in recovery imaging correlates.
  - Interaction with baseline PC3 means the negative association is specific to patients
    with low baseline phonological ability.
  - vmPFC cluster has opposing sign for fluency (positive) vs. phonology (negative)
    — antagonistic trade-off between fluency and phonology recovery.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results — Activation change negatively associated with phonology
      change; Discussion
    confidence: medium
    flags:
    - PC3 phonology did not significantly improve at group level (P=0.38) — findings
      for phonology recovery correlates are tentative.
    - vmPFC is a SHARED cluster with f1 (fluency), positively for fluency and negatively
      for phonology — captures an anti-correlated trade-off.
    - Multiple significant baseline x activation interactions complicate interpretation.
  source_passages:
  - section: Abstract
    page: 1
    supports: claim
    quote: phonology recovery was associated with reducing activation in bilateral
      precentral gyri, dorso-medial frontal poles and the precuneus
  - section: Results — Activation change negatively associated with phonology change
    page: 7
    supports: statistics
    quote: mean activation change extracted from cluster 2 was negatively associated
      with PC3 change both before and after including T1 PC3 score, and even after
      including lesion volume, years of education and age (beta = –0.28, P = 0.0001
  - section: Results — PCA
    page: 5
    supports: limitation
    quote: PC3 scores were not significantly better at T2 than T1 [median 0.21 (IQR
      1.07) at T1 versus 0.26 (0.59) at T2; Wilcoxon signed-rank test, z = 0.88, P
      = 0.38]
  - section: Discussion
    page: 9
    supports: claim
    quote: activation change in the ventromedial prefrontal cortex, dorso-medial frontal
      poles and precuneus was negatively correlated with phonological recovery
- id: f4
  target: fluency
  target_kind: impairment
  claim: At 2 weeks post-stroke, activation in the right posterior supramarginal gyrus,
    insular cortex, and temporo-occipital MTG is positively associated with concurrent
    fluency score, suggesting early right hemisphere compensatory recruitment.
  direction: likely
  relationship: recruitment
  citation: '@Stefaniak2022'
  method: fMRI_activation
  design: cross-sectional
  imaging: fMRI
  sample:
    n: 26
    population: adults with mild-moderate aphasia at 2 weeks post-stroke
    time_post_onset: 2 weeks post-stroke (T1 only)
    age_range: mean 59.0 years (SD 11.0)
    handedness: not_reported
    language: English (premorbidly fluent)
    recruitment: Same cohort as f1.
    inclusion_criteria: Left hemisphere infarct; language difficulties at stroke onset.
    exclusion_criteria: Previous stroke with aphasia; other neurological condition.
  statistics:
    threshold: voxel-wise cluster-forming p < 0.005 (uncorrected), cluster-level p
      < 0.05 FWE
    cluster_extent: not_reported
    effect_size: beta=0.54 P=7.1e-5 (unadjusted); beta=0.51 P=0.0004 (with lesion
      volume, education, age)
    ci_95: not_reported
    p_value: P=7.1e-5
  confounders_controlled:
  - lesion volume, years of education, age (robust regression)
  confounders_not_controlled:
  - baseline severity not controlled (this is concurrent cross-sectional correlation,
    not change score)
  - no semantic/executive or phonology cross-sectional correlates found
  region_definition:
    kind: data_driven_cluster
    atlas: Harvard-Oxford cortical atlas
    description: 'Single cluster: right posterior supramarginal gyrus, insular cortex,
      and temporo-occipital MTG. Similar to the right temporo-occipital MTG cluster
      in f1 (longitudinal fluency recovery).'
  imaging_details:
    field_strength: not_reported
    acquisition:
      sequence: Sparse fMRI; same as f1
      voxel_size_mm: not_reported
      TR_ms: not_reported
      TE_ms: not_reported
    modalities:
    - modality: fMRI_task_activation
    reference_space: MNI152
    atlases_used: []
    software: FSL + SPM12
  replications: []
  contradictions: []
  author_limitations:
  - Cross-sectional correlation at T1 — causal direction cannot be established.
  - No semantic/executive or phonology cross-sectional correlates found at T1.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results — Activation positively associated with fluency at 2 weeks
      post-stroke
    confidence: high
    flags:
    - 'Convergent evidence: same right temporo-occipital MTG region identified both
      cross-sectionally at T1 (f4) and longitudinally as predictor of recovery (f1).'
  source_passages:
  - section: Results — Activation positively associated with fluency at 2 weeks post-stroke
    page: 6
    supports: claim
    quote: T1 activation in a cluster in the right posterior supramarginal gyrus,
      insular cortex and temporo-occipital middle temporal gyrus (MTG) was positively
      associated with T1 fluency (PC1) score
  - section: Results — Activation positively associated with fluency at 2 weeks post-stroke
    page: 6
    supports: statistics
    quote: Mean activation extracted from this cluster was significantly positively
      associated with T1 PC1 score (beta = 0.54, P = 7.1  10–5), even after including
      lesion volume, years of education and age (beta = 0.51, P = 0.0004)
reviewer: michele
reviewed_on: '2026-05-06'
---
# Bilateral MFG / Right Temporo-Occipital MTG — Stefaniak 2022

Stefaniak et al. (2022, Brain) longitudinal fMRI study (n=26, 2wks and 4mths post-stroke).
Four findings: f1 fluency longitudinal, f2 semantic/executive longitudinal, f3 phonology longitudinal, f4 fluency cross-sectional (T1).
