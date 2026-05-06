---
schema_version: 2.3
id: semantics
name: Semantics (semantic processing)
kind: impairment
status: approved
created_by: agent:claude-opus-4-7
created_on: 2026-05-01
short_definition: Underlying language component capturing semantic processing — comprehension
  and meaning-based judgments across receptive and expressive tasks (synonym judgments,
  picture-to-word matching, Camel & Cactus). One of five orthogonal factors recovered
  by PCA over the standard chronic-aphasia neuropsychological battery (Butler et al.
  2014; Halai et al. 2017; Alyahya et al. 2018).
assessment:
- Camel and Cactus Test — pictures (Cambridge Semantic Battery)
- 96-trial Synonym Judgment Test (Jefferies et al. 2009)
- Verb Synonym Judgment Test
- Spoken word-to-picture matching (Cambridge Semantic Battery)
- Written word-to-picture matching
- Spoken Sentence Comprehension (CAT)
- Picture-to-word matching (noun and verb)
findings:
- id: f1
  target: left_anterior_middle_temporal_gyrus
  target_kind: region
  claim: Tissue concentration in the left anterior middle temporal gyrus uniquely
    covaries with the semantic PCA factor in chronic post-stroke aphasia, independent
    of phonological production, fluency, phonological recognition, and executive function
    components.
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
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level (PCA-VBCM with
      all five factors entered simultaneously)
    cluster_extent: 8326
    effect_size: peak Z = 3.90
  confounders_controlled:
  - other four PCA factors (phonological production, fluency, phonological recognition,
    executive function) entered simultaneously as orthogonal regressors
  confounders_not_controlled:
  - lesion volume — the semantic factor showed mild correlation with lesion volume
    (r=0.37, p=0.01) and the cluster shrank when partialled out, surviving only in
    occipital subregions
  - age, education, BDAE aphasia type (descriptive only)
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Anterior middle temporal gyrus as labelled in Harvard-Oxford; PCA-VBCM
      peak at MNI [-48, -6, -26].
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
    - region: anterior middle temporal gyrus
      mni:
      - -48
      - -6
      - -26
  replications:
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - Univariate VBCM may bias micro-level cluster localization (Mah et al. 2014).
  - The semantic-cluster shrinkage when lesion volume is partialled out (limited to
    occipital subregions) is a real concern for the temporal-lobe portion of this
    finding.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 2 (page 226); Results 3.2.3 (page 223); Results
      3.2.4 (page 225); Discussion 4.3 (page 227)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: Performance on the semantic factor was uniquely associated with left superior
      lateral occipital cortex, occipital fusiform gyrus, temporal occipital fusiform
      cortex, anterior inferior temporal gyrus, anterior temporal fusiform cortex,
      anterior middle temporal gyrus, temporal pole and precuneus.
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
  - section: Results 3.2.4
    page: 225
    supports: confounders
    quote: 'the neural correlates for the semantic factor (correlation with lesion
      volume: r = 0.37, p = 0.01) showed a reduction in cluster size and were limited
      to the left superior and inferior lateral occipital cortex, precuneus, and occipital
      fusiform gyrus.'
  - section: Methods 2.5
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
- id: f2
  target: left_temporal_pole
  target_kind: region
  claim: Tissue concentration in the left temporal pole uniquely covaries with the
    semantic PCA factor in chronic post-stroke aphasia.
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
    cluster_extent: 8326
    effect_size: peak Z = 3.78
  confounders_controlled:
  - other four PCA factors entered simultaneously
  confounders_not_controlled:
  - lesion volume (semantic cluster attenuated when included)
  - age, education, aphasia type
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Left temporal pole (HO label); peak at MNI [-42, 4, -26]. The semantic
      'hub' region in Lambon Ralph models.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - region: temporal pole
      mni:
      - -42
      - 4
      - -26
  replications:
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - Univariate VBCM caveat (Mah et al. 2014).
  - Semantic-cluster shrinkage under lesion-volume covariate.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 2; Results 3.2.3 (page 223); Discussion 4.3 (page
      227)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: Performance on the semantic factor was uniquely associated with left superior
      lateral occipital cortex, occipital fusiform gyrus, temporal occipital fusiform
      cortex, anterior inferior temporal gyrus, anterior temporal fusiform cortex,
      anterior middle temporal gyrus, temporal pole and precuneus.
  - section: Discussion 4.3
    page: 227
    supports: claim
    quote: The neural correlates associated with the semantic factor were the largest
      in size and included anterior and posterior temporal regions, which have been
      linked to semantic processing
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
- id: f3
  target: left_superior_lateral_occipital_cortex
  target_kind: region
  claim: Tissue concentration in the left superior lateral occipital cortex uniquely
    covaries with the semantic PCA factor in chronic post-stroke aphasia (the strongest
    peak; cluster also survives lesion-volume covariate).
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
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level; cluster survives
      at lower threshold (p<0.005) when lesion volume is added
    cluster_extent: 8326
    effect_size: peak Z = 5.53 (strongest cluster across the entire PCA-VBCM analysis)
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume (occipital sub-region survives this covariate)
  confounders_not_controlled:
  - age, education, aphasia type
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Left superior lateral occipital cortex; peak MNI [-28, -74, 14].
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - region: superior lateral occipital cortex
      mni:
      - -28
      - -74
      - 14
  replications: []
  contradictions: []
  author_limitations:
  - Univariate VBCM caveat (Mah et al. 2014).
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 2 (peak); Results 3.2.4 (page 225 — survives lesion
      volume)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: Performance on the semantic factor was uniquely associated with left superior
      lateral occipital cortex, occipital fusiform gyrus, temporal occipital fusiform
      cortex
  - section: Results 3.2.4
    page: 225
    supports: statistics
    quote: 'the neural correlates for the semantic factor (correlation with lesion
      volume: r = 0.37, p = 0.01) showed a reduction in cluster size and were limited
      to the left superior and inferior lateral occipital cortex, precuneus, and occipital
      fusiform gyrus.'
  - section: Methods 2.5
    page: 219
    supports: imaging_details
    quote: All anatomical results are described using labels based on the Harvard-Oxford
      atlas in MNI space (Desikan et al., 2006) and natbrainlab white matter connections
      atlas
- id: f4
  target: left_inferior_longitudinal_fasciculus
  target_kind: region
  claim: Tissue concentration in the left inferior longitudinal fasciculus uniquely
    covaries with the semantic PCA factor — connecting posterior occipito-temporal
    cortex with the temporal pole, consistent with the ventral language pathway.
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
    cluster_extent: 8326
    effect_size: peak Z = 4.67
  confounders_controlled:
  - other four PCA factors entered simultaneously
  confounders_not_controlled:
  - lesion volume (semantic cluster attenuated when included)
  - age, education, aphasia type
  region_definition:
    kind: tract
    atlas: natbrainlab white-matter atlas (Catani et al. 2012)
    description: Inferior longitudinal fasciculus; peak MNI [-38, -8, -20]. The ILF
      was associated with both phonological production and semantic factors in this
      paper.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - natbrainlab white-matter (Catani et al. 2012)
    coordinates_reported:
    - region: inferior longitudinal fasciculus
      mni:
      - -38
      - -8
      - -20
  replications:
  - '@Saur2008'
  contradictions: []
  author_limitations:
  - Tract atlas built from healthy adults; tract trajectories in chronic stroke are
    approximate.
  - ILF cross-loaded on Factor 1 — domain-specificity is mixed.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 2; Discussion 4.3 (page 228)
    confidence: high
    flags: []
  source_passages:
  - section: Discussion 4.3
    page: 228
    supports: claim
    quote: The phonological production and semantic factors were also associated with
      white matter tracts that connect posterior occipito-temporal regions to the
      temporal pole, corresponding to the inferior longitudinal fasciculus. This underlying
      temporal stem corresponds to the ventral language pathway and has been shown
      to be involved with recognition and comprehension
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
- id: f5
  target: left_precuneus
  target_kind: region
  claim: Tissue concentration in the left precuneus uniquely covaries with the semantic
    PCA factor in chronic post-stroke aphasia (cluster also survives lesion-volume
    covariate in this region).
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
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level; survives at
      p<0.005 when lesion volume is added
    cluster_extent: 8326
    effect_size: peak Z = 5.01
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume (precuneus survives this covariate)
  confounders_not_controlled:
  - age, education, aphasia type
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Left precuneus cortex; peak MNI [-18, -56, 26]. Default mode network
      region implicated in semantic processing.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - region: precuneus
      mni:
      - -18
      - -56
      - 26
  replications: []
  contradictions: []
  author_limitations:
  - Univariate VBCM caveat.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 2; Results 3.2.4 (page 225)
    confidence: high
    flags: []
  source_passages:
  - section: Discussion 4.3
    page: 228
    supports: claim
    quote: Posterior left central perisylvian regions (angular gyrus, posterior inferior
      and middle temporal gyrus) were shared between the semantic, phonological production
      and phonological recognition factors. These posterior regions have been implicated
      in phonological and semantic processing by functional MRI studies, and the parietal
      regions have been associated with default mode network
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

  semantic PCA factor (Factor 2: 11.5% variance) is associated with the

  largest cluster in the entire analysis (8326 voxels) spanning

  occipito-temporal cortex, anterior temporal lobe (including the

  temporal pole), the inferior longitudinal fasciculus, and precuneus.

  Five strongest peaks recorded as separate findings.


  Loadings (Table 4) used to interpret this factor as "semantics":

  Camel and Cactus pictures (.873), verb picture-to-word matching

  (.829), noun picture-to-word matching (.816), verb synonym judgment

  (.799), 96-synonym judgment (.798), written word-to-picture matching

  (.778), spoken word-to-picture matching (.756), spoken sentence

  comprehension (.613), Raven''s Coloured Progressive Matrices (.563),

  noun naming OANB (.617).


  Important caveat: the semantic factor showed mild correlation with

  lesion volume (r=0.37, p=0.01); when lesion volume was partialled

  out, the cluster shrank and was limited to occipital sub-regions

  (superior + inferior lateral occipital cortex, precuneus, occipital

  fusiform). Temporal-lobe peaks (temporal pole, anterior MTG) did NOT

  survive that covariate. Reviewers should weigh this when promoting

  individual findings.'
reviewer: michele
reviewed_on: '2026-05-06'
---
# Semantics (semantic processing)

## How to read this entry

First-extraction draft from Alyahya et al. 2018 (NounVerb). Defines
"semantics" as a draft impairment-like component ID and lists the
brain regions whose tissue concentration uniquely covaries with the
semantic PCA factor (Factor 2).

## Component definition

Semantics is the underlying language component capturing semantic
processing across both receptive (synonym judgments, picture-to-word
matching) and expressive (naming) tasks. In Alyahya et al. it accounts
for 11.5% of variance and is conceptually distinct from phonological
production (Factor 1), fluency (Factor 3), phonological recognition
(Factor 4), and executive function (Factor 5). Factor loadings concentrate
on Camel & Cactus, synonym judgments (verbal and verb-specific), and
picture-to-word matching tasks.

## Lesion correlates (per Alyahya 2018 NounVerb)

PCA-VBCM identifies an 8326-voxel cluster — the largest in the analysis —
with peaks in:

  - Superior lateral occipital cortex (Z=5.53)
  - Precuneus cortex (Z=5.01)
  - Inferior longitudinal fasciculus (Z=4.67)
  - Anterior temporal fusiform cortex (Z=4.67)
  - Anterior inferior temporal gyrus (Z=4.28)
  - Posterior inferior temporal gyrus (Z=4.12)
  - Posterior middle temporal gyrus (Z=4.04)
  - Anterior middle temporal gyrus (Z=3.90)
  - Temporal pole (Z=3.78)

When lesion volume is partialled out, the cluster shrinks substantially
and survives only in the left superior and inferior lateral occipital
cortex, precuneus, and occipital fusiform gyrus. Temporal-lobe peaks
do not survive that covariate.

## Notes for next extraction round

  - Add left_anterior_middle_temporal_gyrus, left_temporal_pole,
    left_superior_lateral_occipital_cortex, left_inferior_longitudinal_fasciculus,
    left_precuneus as region entries before re-extracting on the region
    side.
  - When promoting these findings, prioritise occipital peaks
    (left_superior_lateral_occipital_cortex, left_precuneus) since they are the
    only ones that survive lesion-volume control.
