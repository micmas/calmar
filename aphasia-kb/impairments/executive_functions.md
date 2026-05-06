---
schema_version: 2.3
id: executive_functions
name: Executive functions
kind: impairment
status: approved
created_by: agent:claude-opus-4-7
created_on: 2026-05-01
short_definition: Underlying cognitive component capturing non-linguistic executive
  control — rule anticipation and visuospatial reasoning. Loads heavily on the Brixton
  Spatial Anticipation Test and Raven's Coloured Progressive Matrices. One of five
  orthogonal factors recovered by PCA over the standard chronic-aphasia neuropsychological
  battery (Butler et al. 2014; Halai et al. 2017; Alyahya et al. 2018). Conceptually
  closer to a fluid-intelligence / cognitive-control construct than to language per
  se.
assessment:
- Brixton Spatial Anticipation Test (Burgess and Shallice 1997)
- Raven's Coloured Progressive Matrices (Raven 1962)
- Type-token ratio (negatively loaded fluency measure)
findings:
- id: f1
  target: left_superior_frontal_gyrus
  target_kind: region
  claim: Tissue concentration in the left superior frontal gyrus covaries with the
    executive function PCA factor in chronic post-stroke aphasia, but only at a relaxed
    statistical threshold (p<0.005 voxel-level).
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
      English speaker.
    exclusion_criteria: MRI contraindications; pre-morbid left-handedness; >1 stroke;
      other significant neurological condition.
  statistics:
    threshold: p<0.005 voxel-level (LOWER than standard p<0.001), FWE-corrected p<0.05
      cluster-level (Factor 5 did not survive at standard threshold; Table 6 footnote);
      cluster survives lesion-volume covariate
    cluster_extent: 1085
    effect_size: peak Z = 3.65
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume (Factor 5 r=0.14, p=0.33 with lesion volume; cluster survives)
  confounders_not_controlled:
  - age, education, BDAE aphasia type
  - lower threshold required — increased false-positive risk
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Left superior frontal gyrus; peak MNI [-22, 20, 52]. Threshold lowered
      to p<0.005 because no clusters survived at the standard p<0.001.
  imaging_details:
    field_strength: 3T
    acquisition:
      voxel_size_mm:
      - 1.0
      - 1.0
      - 1.0
      TR_ms: 9.0
      TE_ms: 3.93
      sequence: T1-weighted inversion recovery 3D
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008 unified segmentation-normalisation
      + 8 mm FWHM smoothing
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford (Desikan et al. 2006)
    - natbrainlab white-matter (Catani et al. 2012)
    coordinates_reported:
    - region: superior frontal gyrus
      mni:
      - -22
      - 20
      - 52
  replications: []
  contradictions: []
  author_limitations:
  - Univariate VBCM may bias micro-level localization (Mah et al. 2014).
  - Factor 5 explained the least behavioural variance (4.6%) and required a relaxed
    threshold to recover any cluster — interpretation should be cautious.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 5 (page 226 footnote); Results 3.2.3 (page 223);
      Discussion 4.3 (page 228)
    confidence: high
    flags:
    - Factor 5 required a relaxed threshold to produce significant clusters — strength
      flagged as weak.
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: There were no significant clusters identified for executive function factor.
      This factor, however, correlated with left frontal regions at a slightly lower
      threshold (p = 0.005 voxel-level, cluster corrected using FWE p < 0.05). This
      cluster included the left superior frontal gyrus, paracingulate gyrus, supplementary
      motor cortex and pre-central gyrus.
  - section: Discussion 4.3
    page: 228
    supports: claim
    quote: the executive function factor, which explained the least behavioural variance,
      did not uniquely correlate with any brain regions, unless the statistical threshold
      was reduced. At a lower threshold, this factor was associated with left frontal
      regions, which have been implicated with executive processing in both fMRI studies
      on healthy participants and in aphasia (Duncan and Owen, 2000; Lacey et al.,
      2017).
  - section: Methods 2.1 — Participants
    page: 217
    supports: sample
    quote: Forty-eight stroke patients (single left ischaemic or haemorrhagic stroke)
      with chronic aphasia participated in this study (34 males and 14 females).
  - section: Methods 2.5 — Analysis of neuroimaging data
    page: 219
    supports: method
    quote: 'the normalised-smoothed T1-weighted images with continuous signal intensity
      values in each vowel across the whole brain were correlated with patients''
      individual behavioural measures using Voxel-Based Correlational Methodology
      (VBCM: Tyler et al., 2005)'
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
  - section: Results 3.2.4
    page: 225
    supports: confounders
    quote: Three of the five components did not significantly correlate with lesion
      volume [phonological production (r = 0.22, p = 0.12); phonological recognition
      (r = 0.18, p = 0.21); and executive function (r = 0.14, p = 0.33)]
  - section: Discussion 4.3
    page: 228
    supports: limitation
    quote: It should be noted that these neural correlates were identified using univariate
      lesion-symptom mapping analyses and there have been suggestions that such approaches
      might bias the micro-level location of clusters (Mah et al., 2014).
- id: f2
  target: left_paracingulate_gyrus
  target_kind: region
  claim: Tissue concentration in the left paracingulate gyrus covaries with the executive
    function PCA factor in chronic post-stroke aphasia (relaxed threshold).
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
    threshold: p<0.005 voxel-level (relaxed), FWE-corrected p<0.05 cluster-level
    cluster_extent: 1085
    effect_size: peak Z = 3.36
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume
  confounders_not_controlled:
  - age, education, aphasia type
  - relaxed threshold
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Left paracingulate gyrus; peak MNI [-6, 30, 32].
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - region: paracingulate gyrus
      mni:
      - -6
      - 30
      - 32
  replications: []
  contradictions: []
  author_limitations:
  - Relaxed threshold; weak factor explained least variance (4.6%).
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 5
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: This cluster included the left superior frontal gyrus, paracingulate gyrus,
      supplementary motor cortex and pre-central gyrus.
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
- id: f3
  target: left_supplementary_motor_area
  target_kind: region
  claim: Tissue concentration in the left supplementary motor area covaries with the
    executive function PCA factor in chronic post-stroke aphasia (relaxed threshold).
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
    threshold: p<0.005 voxel-level (relaxed), FWE-corrected p<0.05 cluster-level
    cluster_extent: 1085
    effect_size: peak Z = 3.27
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume
  confounders_not_controlled:
  - age, education, aphasia type
  - relaxed threshold
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Left supplementary motor area; peak MNI [-10, -8, 52].
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - region: supplementary motor area
      mni:
      - -10
      - -8
      - 52
  replications: []
  contradictions: []
  author_limitations:
  - Relaxed threshold.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 5
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: This cluster included the left superior frontal gyrus, paracingulate gyrus,
      supplementary motor cortex and pre-central gyrus.
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
source: agent_draft
last_reviewed: null
notes: 'First-extraction draft from Alyahya et al. 2018 (NounVerb). The

  executive function PCA factor (Factor 5: 4.6% variance — the smallest

  factor) did NOT yield significant clusters at the standard

  p<0.001 voxel threshold. Authors relaxed the threshold to p<0.005

  voxel-level, FWE p<0.05 cluster-level, recovering a 1085-voxel

  cluster in left superior frontal cortex. Three peak findings

  recorded with strength flagged as ''weak''.


  Loadings (Table 4) used to interpret this factor as "executive

  functions": Raven''s Coloured Progressive Matrices (.549), Brixton

  spatial anticipation test (.526), type-token ratio (-.591;

  negatively loaded). Visuospatial reasoning + verbal-diversity

  measures.


  Factor 5 has the lowest correlation with lesion volume (r=0.14,

  p=0.33), so the cluster IS robust to lesion-volume covariate at the

  relaxed threshold. The interpretation in the paper aligns this with

  generic prefrontal cognitive control (Duncan and Owen 2000), not a

  language-specific finding.'
reviewer: michele
reviewed_on: '2026-05-06'
---
# Executive functions

## Component definition

Executive functions in this paper means the non-linguistic cognitive
control component recovered by PCA — primarily fluid-reasoning and
rule-anticipation tasks (Raven's, Brixton). It is the smallest of the
five factors (4.6% of variance) and the only one that did not yield
significant lesion correlates at the standard threshold.

## Lesion correlates (per Alyahya 2018 NounVerb)

At a relaxed threshold (p<0.005 voxel-level, FWE-cluster p<0.05) a
1085-voxel left frontal cluster emerges:

  - Superior frontal gyrus (Z=3.65)
  - Paracingulate gyrus (Z=3.36)
  - Supplementary motor area (Z=3.27)
  - Pre-central gyrus (Z=2.96, also loaded on Factor 3)

The Discussion (page 228) interprets this as consistent with
prefrontal cognitive-control regions (Duncan & Owen 2000).

## Notes for next extraction round

  - Findings here have `strength: weak` because they required a
    relaxed threshold. Reviewers should consider whether Factor 5 is
    even worth promoting given it captures only 4.6% of variance and
    primarily indexes non-language cognition.
  - Add left_superior_frontal_gyrus, left_paracingulate_gyrus,
    left_supplementary_motor_area as region entries before re-extracting.
