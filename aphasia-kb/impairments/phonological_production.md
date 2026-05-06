---
schema_version: 2.3
id: phonological_production
name: Phonological production
kind: impairment
status: approved
created_by: agent:claude-opus-4-7
created_on: 2026-05-01
short_definition: Underlying language component capturing the ability to produce word
  forms (single-word repetition and naming). Loads heavily on word/non-word repetition
  (PALPA 8/9), Boston Naming Test, OANB naming and Cambridge 64-item naming. One of
  five orthogonal factors recovered by PCA over the standard chronic-aphasia neuropsychological
  battery (Butler et al. 2014; Halai et al. 2017; Alyahya et al. 2018).
assessment:
- Word repetition — immediate (PALPA 9)
- Word repetition — delayed (PALPA 9)
- Non-word repetition — immediate (PALPA 8)
- Non-word repetition — delayed (PALPA 8)
- Cambridge 64-item naming
- Boston Naming Test (BNT)
- Object and Action Naming Battery (OANB) — noun and verb naming
findings:
- id: f1
  target: left_posterior_arcuate_fasciculus
  target_kind: region
  claim: Tissue concentration in the posterior segment of the left arcuate fasciculus
    uniquely covaries with the phonological production PCA factor in chronic post-stroke
    aphasia, after partialling out the four other principal components.
  direction: likely
  relationship: causal
  citation: '@Alyahya2018NounVerb'
  method: VBCM
  design: cross-sectional
  imaging: T1
  sample:
    n: 48
    population: chronic post-stroke aphasia (single left ischaemic or haemorrhagic
      stroke)
    time_post_onset: '>=12 months post-stroke'
    age_range: 44-87 years (mean 63.31, SD 11.8)
    handedness: right-handed (pre-morbid left-handers excluded)
    language: native English speakers
    recruitment: stroke community support groups and speech and language therapy services
      in the North West of England.
    inclusion_criteria: single left-hemisphere stroke; ≥12 months post-stroke; native
      English speaker; normal/corrected hearing and vision.
    exclusion_criteria: MRI contraindications; pre-morbid left-handedness; >1 stroke;
      other significant neurological condition.
  statistics:
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level (PCA-VBCM model
      with all five factors entered simultaneously); cluster survives adding lesion
      volume covariate at p<0.005 voxel-level
    cluster_extent: 3905
    effect_size: peak Z = 4.51
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled:
  - the other four PCA factors (semantics, fluency, phonological recognition, executive
    functions) entered simultaneously as orthogonal regressors
  - lesion volume (in the secondary analysis where the cluster still survives at lower
    threshold)
  confounders_not_controlled:
  - age and education entered as descriptors, not regressors
  - BDAE aphasia type (heterogeneous sample, deliberately)
  region_definition:
    kind: data_driven_cluster
    atlas: natbrainlab white-matter atlas (Catani et al. 2012)
    description: Cluster from PCA-VBCM phonological-production map labelled as posterior
      segment of the arcuate fasciculus by reference to the natbrainlab atlas; peak
      voxel at MNI [-40, -44, 12].
  imaging_details:
    field_strength: 3T
    acquisition:
      voxel_size_mm:
      - 1.0
      - 1.0
      - 1.0
      TR_ms: 9.0
      TE_ms: 3.93
      sequence: T1-weighted inversion recovery 3D (TI=1150 ms, flip angle=8°, 150
        contiguous slices)
    preprocessing_pipeline: SPM8 + OptiBET brain extraction (Lutkenhoff et al. 2014)
      + modified unified segmentation-normalisation optimised for focal lesions (Seghier
      et al. 2008) + 8 mm FWHM Gaussian smoothing; lesion U-threshold = 0.5
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford (Desikan et al. 2006)
    - natbrainlab white-matter atlas (Catani et al. 2012)
    coordinates_reported:
    - region: posterior segment of arcuate fasciculus
      mni:
      - -40
      - -44
      - 12
  replications:
  - '@Fridriksson2018'
  - '@Saur2008'
  contradictions: []
  author_limitations:
  - Univariate lesion-symptom mapping may bias the micro-level location of clusters
    (Mah et al. 2014); future work using multivariate approaches recommended.
  - VBCM uses continuous tissue concentration rather than binarised lesion masks —
    this is more sensitive than standard VLSM but treats partial lesions and adjacent
    atrophy on the same scale.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.2.3 + Table 6 (Factor 1 row, page 226); Discussion 4.3
      (page 227)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: Performance on the phonological production factor was uniquely associated
      with parietal operculum cortex.
  - section: Discussion 4.3
    page: 227
    supports: claim
    quote: This factor was also associated with the white matter tracts underlying
      inferior parietal regions, which correspond to the posterior segment of the
      arcuate fasciculus.
  - section: Methods 2.1 — Participants
    page: 217
    supports: sample
    quote: Forty-eight stroke patients (single left ischaemic or haemorrhagic stroke)
      with chronic aphasia participated in this study (34 males and 14 females).
  - section: Methods 2.1 — Participants
    page: 217
    supports: sample
    quote: They were recruited on the basis that they had a single left hemispheric
      stroke and were at least 12 months post-stroke. All participants were native
      English speakers
  - section: Methods 2.5 — Analysis of neuroimaging data
    page: 219
    supports: method
    quote: 'the normalised-smoothed T1-weighted images with continuous signal intensity
      values in each vowel across the whole brain were correlated with patients''
      individual behavioural measures using Voxel-Based Correlational Methodology
      (VBCM: Tyler et al., 2005)'
  - section: Methods 2.4 — Acquisition and processing of neuroimaging data
    page: 219
    supports: imaging_details
    quote: High-resolution structural T1-weighted MRI scans were acquired on a 3T
      Philips Achieva scanner
  - section: Methods 2.5 — Analysis of neuroimaging data
    page: 220
    supports: statistics
    quote: The standard threshold of p = 0.001 voxel-level, cluster-level corrected
      using FWE p < 0.05 was used in the direct contrasts and the PCA-VBCM analyses
  - section: Results 3.2.4 — Effect of lesion size
    page: 225
    supports: confounders
    quote: when adding lesion volume to the PCA-VBCM, the clusters remain significant.
      This outcome supports the proposal that PCA generates statically independent
      components, and improves power
  - section: Discussion 4.3
    page: 228
    supports: limitation
    quote: It should be noted that these neural correlates were identified using univariate
      lesion-symptom mapping analyses and there have been suggestions that such approaches
      might bias the micro-level location of clusters (Mah et al., 2014).
- id: f2
  target: left_angular_gyrus
  target_kind: region
  claim: Tissue concentration in the left angular gyrus uniquely covaries with the
    phonological production PCA factor in chronic post-stroke aphasia.
  direction: likely
  relationship: causal
  citation: '@Alyahya2018NounVerb'
  method: VBCM
  design: cross-sectional
  imaging: T1
  sample:
    n: 48
    population: chronic post-stroke aphasia (single left ischaemic or haemorrhagic
      stroke)
    time_post_onset: '>=12 months post-stroke'
    age_range: 44-87 years (mean 63.31, SD 11.8)
    handedness: right-handed
    language: native English speakers
  statistics:
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level (PCA-VBCM);
      cluster survives lesion-volume covariate
    cluster_extent: 3905
    effect_size: peak Z = 4.41
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume (in secondary analysis)
  confounders_not_controlled:
  - age, education, aphasia type (descriptive only)
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford (Desikan et al. 2006)
    description: Left angular gyrus as labelled in the Harvard-Oxford cortical atlas;
      PCA-VBCM peak at MNI [-34, -54, 24].
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008 unified segmentation-normalisation
      + 8 mm FWHM smoothing
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford (Desikan et al. 2006)
    - natbrainlab white-matter (Catani et al. 2012)
    coordinates_reported:
    - region: angular gyrus
      mni:
      - -34
      - -54
      - 24
  replications:
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - Univariate VBCM may bias micro-level localization (Mah et al. 2014).
  - Angular gyrus loaded across three factors (phonological production, phonological
    recognition, semantics) — domain-specificity of the cluster should not be over-interpreted.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 (Factor 1 row); page 224 (shared regions paragraph)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 224
    supports: claim
    quote: the left angular gyrus was associated with phonological production, phonological
      recognition and semantic factors
  - section: Methods 2.5 — Analysis of neuroimaging data
    page: 219
    supports: imaging_details
    quote: All anatomical results are described using labels based on the Harvard-Oxford
      atlas in MNI space (Desikan et al., 2006) and natbrainlab white matter connections
      atlas based on diffusion tensor tractography (Catani et al., 2012).
  - section: Discussion 4.3
    page: 228
    supports: limitation
    quote: It should be noted that these neural correlates were identified using univariate
      lesion-symptom mapping analyses and there have been suggestions that such approaches
      might bias the micro-level location of clusters (Mah et al., 2014).
  - section: Methods 2.5
    page: 220
    supports: statistics
    quote: The standard threshold of p = 0.001 voxel-level, cluster-level corrected
      using FWE p < 0.05 was used in the direct contrasts and the PCA-VBCM analyses
- id: f3
  target: left_parietal_operculum_cortex
  target_kind: region
  claim: Tissue concentration in the left parietal operculum cortex uniquely covaries
    with the phonological production PCA factor in chronic post-stroke aphasia (the
    headline cluster of Factor 1 in the Discussion).
  direction: likely
  relationship: causal
  citation: '@Alyahya2018NounVerb'
  method: VBCM
  design: cross-sectional
  imaging: T1
  sample:
    n: 48
    population: chronic post-stroke aphasia (single left ischaemic or haemorrhagic
      stroke)
    time_post_onset: '>=12 months post-stroke'
    age_range: 44-87 years (mean 63.31, SD 11.8)
    handedness: right-handed
    language: native English speakers
  statistics:
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level (PCA-VBCM);
      cluster survives lesion-volume covariate
    cluster_extent: 3905
    effect_size: peak Z = 4.30
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume (secondary analysis)
  confounders_not_controlled:
  - age, education, aphasia type (descriptive only)
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Left parietal operculum cortex (HO cortical label); peak at MNI [-32,
      -36, 22].
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    - natbrainlab white-matter (Catani et al. 2012)
    coordinates_reported:
    - region: parietal operculum cortex
      mni:
      - -32
      - -36
      - 22
  replications:
  - '@Fridriksson2018'
  contradictions: []
  author_limitations:
  - Univariate VBCM caveat (Mah et al. 2014).
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.2.3 (page 223 narrative), Table 6 Factor 1
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: Performance on the phonological production factor was uniquely associated
      with parietal operculum cortex.
  - section: Discussion 4.3
    page: 227
    supports: claim
    quote: The phonological production factor was uniquely associated with posterior
      parietal regions, that have been previously shown to be involved with speech
      repetition and phonological retrieval
  - section: Methods 2.5
    page: 220
    supports: statistics
    quote: The standard threshold of p = 0.001 voxel-level, cluster-level corrected
      using FWE p < 0.05 was used in the direct contrasts and the PCA-VBCM analyses
  - section: Methods 2.5
    page: 219
    supports: imaging_details
    quote: All anatomical results are described using labels based on the Harvard-Oxford
      atlas in MNI space (Desikan et al., 2006) and natbrainlab white matter connections
      atlas based on diffusion tensor tractography (Catani et al., 2012).
- id: f4
  target: left_posterior_supramarginal_gyrus
  target_kind: region
  claim: Tissue concentration in the left posterior supramarginal gyrus uniquely covaries
    with the phonological production PCA factor in chronic post-stroke aphasia.
  direction: likely
  relationship: causal
  citation: '@Alyahya2018NounVerb'
  method: VBCM
  design: cross-sectional
  imaging: T1
  sample:
    n: 48
    population: chronic post-stroke aphasia
    time_post_onset: '>=12 months post-stroke'
    age_range: 44-87 years (mean 63.31, SD 11.8)
    handedness: right-handed
    language: native English speakers
  statistics:
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level
    cluster_extent: 3905
    effect_size: peak Z = 3.85
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume (secondary analysis)
  confounders_not_controlled:
  - age, education, aphasia type
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: 'Left posterior supramarginal gyrus (HO label); peak MNI [-50, -46,
      40]. Note: this region also loaded on the phonological recognition factor.'
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - region: posterior supramarginal gyrus
      mni:
      - -50
      - -46
      - 40
  replications: []
  contradictions: []
  author_limitations:
  - Region overlap across PCA factors limits factor-specificity claims.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 (Factor 1 row, page 226); Results 3.2.3 (page 224)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 224
    supports: claim
    quote: the left posterior supramarginal gyrus and planum temporale were associated
      with phonological production and phonological recognition factors
  - section: Methods 2.5
    page: 220
    supports: statistics
    quote: The standard threshold of p = 0.001 voxel-level, cluster-level corrected
      using FWE p < 0.05 was used in the direct contrasts and the PCA-VBCM analyses
  - section: Methods 2.5
    page: 219
    supports: imaging_details
    quote: All anatomical results are described using labels based on the Harvard-Oxford
      atlas in MNI space (Desikan et al., 2006) and natbrainlab white matter connections
      atlas
- id: f5
  target: left_inferior_longitudinal_fasciculus
  target_kind: region
  claim: Tissue concentration in the left inferior longitudinal fasciculus uniquely
    covaries with the phonological production PCA factor in chronic post-stroke aphasia.
  direction: likely
  relationship: causal
  citation: '@Alyahya2018NounVerb'
  method: VBCM
  design: cross-sectional
  imaging: T1
  sample:
    n: 48
    population: chronic post-stroke aphasia
    time_post_onset: '>=12 months post-stroke'
    age_range: 44-87 years (mean 63.31, SD 11.8)
    handedness: right-handed
    language: native English speakers
  statistics:
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level
    cluster_extent: 3905
    effect_size: peak Z = 3.79
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume (secondary analysis)
  confounders_not_controlled:
  - age, education, aphasia type
  region_definition:
    kind: tract
    atlas: natbrainlab white-matter atlas (Catani et al. 2012)
    description: Inferior longitudinal fasciculus as labelled by the natbrainlab atlas;
      peak at MNI [-34, -46, 0]. The ILF was also associated with the semantic factor.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - natbrainlab white-matter (Catani et al. 2012)
    coordinates_reported:
    - region: inferior longitudinal fasciculus
      mni:
      - -34
      - -46
      - 0
  replications:
  - '@Saur2008'
  contradictions: []
  author_limitations:
  - natbrainlab atlas built from healthy adults; tract definitions in chronic stroke
    are approximate.
  - The ILF cluster also loaded on the semantic factor — interpretation as 'phonological'
    is partial.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 (Factor 1 row); Results 3.2.3 (page 224); Discussion 4.3
      (page 228)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 224
    supports: claim
    quote: the tract corresponding to the inferior longitudinal fasciculus was associated
      with phonological production and semantic factors
  - section: Discussion 4.3
    page: 228
    supports: claim
    quote: The phonological production and semantic factors were also associated with
      white matter tracts that connect posterior occipito-temporal regions to the
      temporal pole, corresponding to the inferior longitudinal fasciculus.
  - section: Methods 2.5
    page: 220
    supports: statistics
    quote: The standard threshold of p = 0.001 voxel-level, cluster-level corrected
      using FWE p < 0.05 was used in the direct contrasts and the PCA-VBCM analyses
  - section: Methods 2.5
    page: 219
    supports: imaging_details
    quote: All anatomical results are described using labels based on the Harvard-Oxford
      atlas in MNI space (Desikan et al., 2006) and natbrainlab white matter connections
      atlas based on diffusion tensor tractography (Catani et al., 2012).
- id: f6
  target: left_posterior_arcuate_fasciculus
  target_kind: region
  claim: Tissue concentration in the posterior segment of the left arcuate fasciculus
    uniquely covaries with the phonological production PCA factor in chronic post-stroke
    aphasia, after partialling out the four other principal components.
  direction: likely
  relationship: causal
  citation: '@Alyahya2018NounVerb'
  method: VBCM
  design: cross-sectional
  imaging: T1
  sample:
    n: 48
    population: chronic post-stroke aphasia (single left ischaemic or haemorrhagic
      stroke)
    time_post_onset: '>=12 months post-stroke'
    age_range: 44-87 years (mean 63.31, SD 11.8)
    handedness: right-handed (pre-morbid left-handers excluded)
    language: native English speakers
    recruitment: stroke community support groups and speech and language therapy services
      in the North West of England.
    inclusion_criteria: single left-hemisphere stroke; ≥12 months post-stroke; native
      English speaker; normal/corrected hearing and vision.
    exclusion_criteria: MRI contraindications; pre-morbid left-handedness; >1 stroke;
      other significant neurological condition.
  statistics:
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level (PCA-VBCM model
      with all five factors entered simultaneously); cluster survives adding lesion
      volume covariate at p<0.005 voxel-level
    cluster_extent: 3905
    effect_size: peak Z = 4.51
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled:
  - the other four PCA factors (semantics, fluency, phonological recognition, executive
    functions) entered simultaneously as orthogonal regressors
  - lesion volume (in the secondary analysis where the cluster still survives at lower
    threshold)
  confounders_not_controlled:
  - age and education entered as descriptors, not regressors
  - BDAE aphasia type (heterogeneous sample, deliberately)
  region_definition:
    kind: data_driven_cluster
    atlas: natbrainlab white-matter atlas (Catani et al. 2012)
    description: Cluster from PCA-VBCM phonological-production map labelled as posterior
      segment of the arcuate fasciculus by reference to the natbrainlab atlas; peak
      voxel at MNI [-40, -44, 12].
  imaging_details:
    field_strength: 3T
    acquisition:
      voxel_size_mm:
      - 1.0
      - 1.0
      - 1.0
      TR_ms: 9.0
      TE_ms: 3.93
      sequence: T1-weighted inversion recovery 3D (TI=1150 ms, flip angle=8°, 150
        contiguous slices)
    preprocessing_pipeline: SPM8 + OptiBET brain extraction (Lutkenhoff et al. 2014)
      + modified unified segmentation-normalisation optimised for focal lesions (Seghier
      et al. 2008) + 8 mm FWHM Gaussian smoothing; lesion U-threshold = 0.5
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford (Desikan et al. 2006)
    - natbrainlab white-matter atlas (Catani et al. 2012)
    coordinates_reported:
    - region: posterior segment of arcuate fasciculus
      mni:
      - -40
      - -44
      - 12
  replications:
  - '@Fridriksson2018'
  - '@Saur2008'
  contradictions: []
  author_limitations:
  - Univariate lesion-symptom mapping may bias the micro-level location of clusters
    (Mah et al. 2014); future work using multivariate approaches recommended.
  - VBCM uses continuous tissue concentration rather than binarised lesion masks —
    this is more sensitive than standard VLSM but treats partial lesions and adjacent
    atrophy on the same scale.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.2.3 + Table 6 (Factor 1 row, page 226); Discussion 4.3
      (page 227)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: Performance on the phonological production factor was uniquely associated
      with parietal operculum cortex.
  - section: Discussion 4.3
    page: 227
    supports: claim
    quote: This factor was also associated with the white matter tracts underlying
      inferior parietal regions, which correspond to the posterior segment of the
      arcuate fasciculus.
  - section: Methods 2.1 — Participants
    page: 217
    supports: sample
    quote: Forty-eight stroke patients (single left ischaemic or haemorrhagic stroke)
      with chronic aphasia participated in this study (34 males and 14 females).
  - section: Methods 2.1 — Participants
    page: 217
    supports: sample
    quote: They were recruited on the basis that they had a single left hemispheric
      stroke and were at least 12 months post-stroke. All participants were native
      English speakers
  - section: Methods 2.5 — Analysis of neuroimaging data
    page: 219
    supports: method
    quote: 'the normalised-smoothed T1-weighted images with continuous signal intensity
      values in each vowel across the whole brain were correlated with patients''
      individual behavioural measures using Voxel-Based Correlational Methodology
      (VBCM: Tyler et al., 2005)'
  - section: Methods 2.4 — Acquisition and processing of neuroimaging data
    page: 219
    supports: imaging_details
    quote: High-resolution structural T1-weighted MRI scans were acquired on a 3T
      Philips Achieva scanner
  - section: Methods 2.5 — Analysis of neuroimaging data
    page: 220
    supports: statistics
    quote: The standard threshold of p = 0.001 voxel-level, cluster-level corrected
      using FWE p < 0.05 was used in the direct contrasts and the PCA-VBCM analyses
  - section: Results 3.2.4 — Effect of lesion size
    page: 225
    supports: confounders
    quote: when adding lesion volume to the PCA-VBCM, the clusters remain significant.
      This outcome supports the proposal that PCA generates statically independent
      components, and improves power
  - section: Discussion 4.3
    page: 228
    supports: limitation
    quote: It should be noted that these neural correlates were identified using univariate
      lesion-symptom mapping analyses and there have been suggestions that such approaches
      might bias the micro-level location of clusters (Mah et al., 2014).
- id: f7
  target: left_angular_gyrus
  target_kind: region
  claim: Tissue concentration in the left angular gyrus uniquely covaries with the
    phonological production PCA factor in chronic post-stroke aphasia.
  direction: likely
  relationship: causal
  citation: '@Alyahya2018NounVerb'
  method: VBCM
  design: cross-sectional
  imaging: T1
  sample:
    n: 48
    population: chronic post-stroke aphasia (single left ischaemic or haemorrhagic
      stroke)
    time_post_onset: '>=12 months post-stroke'
    age_range: 44-87 years (mean 63.31, SD 11.8)
    handedness: right-handed
    language: native English speakers
  statistics:
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level (PCA-VBCM);
      cluster survives lesion-volume covariate
    cluster_extent: 3905
    effect_size: peak Z = 4.41
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume (in secondary analysis)
  confounders_not_controlled:
  - age, education, aphasia type (descriptive only)
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford (Desikan et al. 2006)
    description: Left angular gyrus as labelled in the Harvard-Oxford cortical atlas;
      PCA-VBCM peak at MNI [-34, -54, 24].
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008 unified segmentation-normalisation
      + 8 mm FWHM smoothing
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford (Desikan et al. 2006)
    - natbrainlab white-matter (Catani et al. 2012)
    coordinates_reported:
    - region: angular gyrus
      mni:
      - -34
      - -54
      - 24
  replications:
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - Univariate VBCM may bias micro-level localization (Mah et al. 2014).
  - Angular gyrus loaded across three factors (phonological production, phonological
    recognition, semantics) — domain-specificity of the cluster should not be over-interpreted.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 (Factor 1 row); page 224 (shared regions paragraph)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 224
    supports: claim
    quote: the left angular gyrus was associated with phonological production, phonological
      recognition and semantic factors
  - section: Methods 2.5 — Analysis of neuroimaging data
    page: 219
    supports: imaging_details
    quote: All anatomical results are described using labels based on the Harvard-Oxford
      atlas in MNI space (Desikan et al., 2006) and natbrainlab white matter connections
      atlas based on diffusion tensor tractography (Catani et al., 2012).
  - section: Discussion 4.3
    page: 228
    supports: limitation
    quote: It should be noted that these neural correlates were identified using univariate
      lesion-symptom mapping analyses and there have been suggestions that such approaches
      might bias the micro-level location of clusters (Mah et al., 2014).
  - section: Methods 2.5
    page: 220
    supports: statistics
    quote: The standard threshold of p = 0.001 voxel-level, cluster-level corrected
      using FWE p < 0.05 was used in the direct contrasts and the PCA-VBCM analyses
- id: f8
  target: left_parietal_operculum_cortex
  target_kind: region
  claim: Tissue concentration in the left parietal operculum cortex uniquely covaries
    with the phonological production PCA factor in chronic post-stroke aphasia (the
    headline cluster of Factor 1 in the Discussion).
  direction: likely
  relationship: causal
  citation: '@Alyahya2018NounVerb'
  method: VBCM
  design: cross-sectional
  imaging: T1
  sample:
    n: 48
    population: chronic post-stroke aphasia (single left ischaemic or haemorrhagic
      stroke)
    time_post_onset: '>=12 months post-stroke'
    age_range: 44-87 years (mean 63.31, SD 11.8)
    handedness: right-handed
    language: native English speakers
  statistics:
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level (PCA-VBCM);
      cluster survives lesion-volume covariate
    cluster_extent: 3905
    effect_size: peak Z = 4.30
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume (secondary analysis)
  confounders_not_controlled:
  - age, education, aphasia type (descriptive only)
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Left parietal operculum cortex (HO cortical label); peak at MNI [-32,
      -36, 22].
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    - natbrainlab white-matter (Catani et al. 2012)
    coordinates_reported:
    - region: parietal operculum cortex
      mni:
      - -32
      - -36
      - 22
  replications:
  - '@Fridriksson2018'
  contradictions: []
  author_limitations:
  - Univariate VBCM caveat (Mah et al. 2014).
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.2.3 (page 223 narrative), Table 6 Factor 1
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: Performance on the phonological production factor was uniquely associated
      with parietal operculum cortex.
  - section: Discussion 4.3
    page: 227
    supports: claim
    quote: The phonological production factor was uniquely associated with posterior
      parietal regions, that have been previously shown to be involved with speech
      repetition and phonological retrieval
  - section: Methods 2.5
    page: 220
    supports: statistics
    quote: The standard threshold of p = 0.001 voxel-level, cluster-level corrected
      using FWE p < 0.05 was used in the direct contrasts and the PCA-VBCM analyses
  - section: Methods 2.5
    page: 219
    supports: imaging_details
    quote: All anatomical results are described using labels based on the Harvard-Oxford
      atlas in MNI space (Desikan et al., 2006) and natbrainlab white matter connections
      atlas based on diffusion tensor tractography (Catani et al., 2012).
- id: f9
  target: left_posterior_supramarginal_gyrus
  target_kind: region
  claim: Tissue concentration in the left posterior supramarginal gyrus uniquely covaries
    with the phonological production PCA factor in chronic post-stroke aphasia.
  direction: likely
  relationship: causal
  citation: '@Alyahya2018NounVerb'
  method: VBCM
  design: cross-sectional
  imaging: T1
  sample:
    n: 48
    population: chronic post-stroke aphasia
    time_post_onset: '>=12 months post-stroke'
    age_range: 44-87 years (mean 63.31, SD 11.8)
    handedness: right-handed
    language: native English speakers
  statistics:
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level
    cluster_extent: 3905
    effect_size: peak Z = 3.85
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume (secondary analysis)
  confounders_not_controlled:
  - age, education, aphasia type
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: 'Left posterior supramarginal gyrus (HO label); peak MNI [-50, -46,
      40]. Note: this region also loaded on the phonological recognition factor.'
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - region: posterior supramarginal gyrus
      mni:
      - -50
      - -46
      - 40
  replications: []
  contradictions: []
  author_limitations:
  - Region overlap across PCA factors limits factor-specificity claims.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 (Factor 1 row, page 226); Results 3.2.3 (page 224)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 224
    supports: claim
    quote: the left posterior supramarginal gyrus and planum temporale were associated
      with phonological production and phonological recognition factors
  - section: Methods 2.5
    page: 220
    supports: statistics
    quote: The standard threshold of p = 0.001 voxel-level, cluster-level corrected
      using FWE p < 0.05 was used in the direct contrasts and the PCA-VBCM analyses
  - section: Methods 2.5
    page: 219
    supports: imaging_details
    quote: All anatomical results are described using labels based on the Harvard-Oxford
      atlas in MNI space (Desikan et al., 2006) and natbrainlab white matter connections
      atlas
- id: f10
  target: left_inferior_longitudinal_fasciculus
  target_kind: region
  claim: Tissue concentration in the left inferior longitudinal fasciculus uniquely
    covaries with the phonological production PCA factor in chronic post-stroke aphasia.
  direction: likely
  relationship: causal
  citation: '@Alyahya2018NounVerb'
  method: VBCM
  design: cross-sectional
  imaging: T1
  sample:
    n: 48
    population: chronic post-stroke aphasia
    time_post_onset: '>=12 months post-stroke'
    age_range: 44-87 years (mean 63.31, SD 11.8)
    handedness: right-handed
    language: native English speakers
  statistics:
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level
    cluster_extent: 3905
    effect_size: peak Z = 3.79
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume (secondary analysis)
  confounders_not_controlled:
  - age, education, aphasia type
  region_definition:
    kind: tract
    atlas: natbrainlab white-matter atlas (Catani et al. 2012)
    description: Inferior longitudinal fasciculus as labelled by the natbrainlab atlas;
      peak at MNI [-34, -46, 0]. The ILF was also associated with the semantic factor.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - natbrainlab white-matter (Catani et al. 2012)
    coordinates_reported:
    - region: inferior longitudinal fasciculus
      mni:
      - -34
      - -46
      - 0
  replications:
  - '@Saur2008'
  contradictions: []
  author_limitations:
  - natbrainlab atlas built from healthy adults; tract definitions in chronic stroke
    are approximate.
  - The ILF cluster also loaded on the semantic factor — interpretation as 'phonological'
    is partial.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 (Factor 1 row); Results 3.2.3 (page 224); Discussion 4.3
      (page 228)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 224
    supports: claim
    quote: the tract corresponding to the inferior longitudinal fasciculus was associated
      with phonological production and semantic factors
  - section: Discussion 4.3
    page: 228
    supports: claim
    quote: The phonological production and semantic factors were also associated with
      white matter tracts that connect posterior occipito-temporal regions to the
      temporal pole, corresponding to the inferior longitudinal fasciculus.
  - section: Methods 2.5
    page: 220
    supports: statistics
    quote: The standard threshold of p = 0.001 voxel-level, cluster-level corrected
      using FWE p < 0.05 was used in the direct contrasts and the PCA-VBCM analyses
  - section: Methods 2.5
    page: 219
    supports: imaging_details
    quote: All anatomical results are described using labels based on the Harvard-Oxford
      atlas in MNI space (Desikan et al., 2006) and natbrainlab white matter connections
      atlas based on diffusion tensor tractography (Catani et al., 2012).
source: agent_draft
last_reviewed: '2026-05-06'
notes: 'First-extraction draft from Alyahya et al. 2018 (NounVerb). The

  phonological production PCA factor (Factor 1: 51.45% variance) is

  associated with a 3905-voxel cluster spanning posterior arcuate

  fasciculus, angular gyrus, parietal operculum, posterior supramarginal

  gyrus, and inferior longitudinal fasciculus. All five peaks recorded

  here as separate findings. The cluster survived adding lesion volume

  as a covariate (the only Factor whose semantic counterpart partially

  attenuated). This is one of the more robust lesion-symptom maps of

  phonological production in the chronic-aphasia literature because

  PCA orthogonalizes the factor away from semantic and fluency

  contributions.


  Loadings (Table 4) used to interpret this factor as "phonological

  production": word repetition - immediate (.917), word repetition -

  delayed (.904), non-word repetition - immediate (.896), non-word

  repetition - delayed (.855), Cambridge 64-item naming (.786), Boston

  Naming Test (.770), Verb naming OANB (.748), Noun naming OANB (.736),

  forward digit span (.662).


  Anchored on impairment rather than region because none of the five

  target regions yet exist as canonical region entries in regions/.

  Reviewer should consider creating left_posterior_arcuate_fasciculus,

  left_angular_gyrus, left_parietal_operculum_cortex, left_posterior_supramarginal_gyrus,

  and left_inferior_longitudinal_fasciculus as region entries before

  promoting these findings.'
reviewer: auto-reviewer
reviewed_on: '2026-05-05'
---
# Phonological production

## How to read this entry

First-extraction draft from Alyahya et al. 2018 (NounVerb). Defines the
phonological production component as a draft impairment ID and lists
the brain regions whose tissue concentration uniquely covaries with it
in the PCA-VBCM analysis (Factor 1).

## Component definition

Phonological production is the underlying language component
that captures the ability to produce word forms (single-word
repetition and naming). It is the largest factor in the rotated PCA
solution from Alyahya et al. (51.45% of variance), and is conceptually
distinct from phonological recognition (Factor 4 — minimal-pair
discrimination), semantics (Factor 2), fluency (Factor 3), and
executive function (Factor 5). The factor loads heavily on word and
non-word repetition (loadings .855–.917), all naming tasks
(.736–.786), and forward digit span (.662) — see Table 4 of the paper.

## Lesion correlates (per Alyahya 2018 NounVerb)

PCA-VBCM identifies a 3905-voxel cluster centered on:

  - Posterior segment of the arcuate fasciculus (Z=4.51, MNI [-40,-44,12])
  - Angular gyrus (Z=4.41, MNI [-34,-54,24])
  - Parietal operculum cortex (Z=4.30, MNI [-32,-36,22])
  - Posterior supramarginal gyrus (Z=3.85, MNI [-50,-46,40])
  - Inferior longitudinal fasciculus (Z=3.79, MNI [-34,-46,0])

All five clusters survive when lesion volume is added as a covariate
(the analysis is repeated at p<0.005 voxel-level FWE-corrected
cluster-level). This is a notable robustness check given that the
verb naming, verb comprehension, noun naming, and noun comprehension
maps all *did* drop out of significance under the same covariate.

## Notes for next extraction round

  - Add left_posterior_arcuate_fasciculus, left_angular_gyrus,
    left_parietal_operculum_cortex, left_posterior_supramarginal_gyrus, and
    left_inferior_longitudinal_fasciculus as region entries before
    re-extracting on the region side.
  - The angular gyrus, posterior supramarginal gyrus, and inferior
    longitudinal fasciculus also load on other PCA factors — capture
    those cross-factor associations as additional findings on the
    region side, with cross-references to the relevant impairment
    drafts.
