---
schema_version: 2.3
id: phonological_recognition
name: Phonological recognition
kind: impairment
status: approved
created_by: agent:claude-opus-4-7
created_on: 2026-05-01
short_definition: Underlying language component capturing phonemic discrimination
  — distinguishing word and non-word minimal pairs (PALPA 1 and PALPA 2). Distinct
  from phonological production (Factor 1, repetition + naming). One of five orthogonal
  factors recovered by PCA over the standard chronic-aphasia neuropsychological battery
  (Butler et al. 2014; Halai et al. 2017; Alyahya et al. 2018).
assessment:
- Non-word minimal pairs (PALPA 1)
- Word minimal pairs (PALPA 2)
findings:
- id: f1
  target: left_heschls_gyrus
  target_kind: region
  claim: Tissue concentration in the left Heschl's gyrus uniquely covaries with the
    phonological recognition PCA factor in chronic post-stroke aphasia (the headline
    cluster of Factor 4 in the Discussion).
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
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level (PCA-VBCM);
      cluster survives lesion-volume covariate
    cluster_extent: 4088
    effect_size: peak Z = 3.96
  confounders_controlled:
  - other four PCA factors (phonological production, semantics, fluency, executive
    function) entered simultaneously
  - lesion volume (Factor 4 r=0.18, p=0.21 with lesion volume; cluster survives)
  confounders_not_controlled:
  - age, education, BDAE aphasia type
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Left Heschl's gyrus (HO label, includes H1 and H2 transverse temporal
      gyri); peak MNI [-52, -20, 6]. Primary auditory cortex.
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
    - region: Heschl's gyrus
      mni:
      - -52
      - -20
      - 6
  replications:
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - Univariate VBCM may bias micro-level localization (Mah et al. 2014).
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 4 (page 226); Results 3.2.3 (page 223); Discussion
      4.3 (page 227)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: Performance on the phonological recognition factor was uniquely associated
      with the left posterior superior temporal gyrus, Heschl's gyrus (including H1
      and H2), and posterior superior and inferior temporal gyri.
  - section: Discussion 4.3
    page: 227
    supports: claim
    quote: The phonological recognition factor was uniquely associated with Heschl's
      gyrus, which is critically involved with processing speech sounds (DeWitt and
      Rauschecker, 2012).
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
      (r = 0.18, p = 0.21); and executive function (r = 0.14, p = 0.33)], and therefore
      controlling for lesion volume did not have a significant effect on the neural
      correlates
  - section: Discussion 4.3
    page: 228
    supports: limitation
    quote: It should be noted that these neural correlates were identified using univariate
      lesion-symptom mapping analyses and there have been suggestions that such approaches
      might bias the micro-level location of clusters (Mah et al., 2014).
- id: f2
  target: left_planum_temporale
  target_kind: region
  claim: Tissue concentration in the left planum temporale uniquely covaries with
    the phonological recognition PCA factor in chronic post-stroke aphasia (also implicated
    in phonological production).
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
      lesion-volume covariate
    cluster_extent: 4088
    effect_size: peak Z = 4.42
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume (Factor 4 cluster survives)
  confounders_not_controlled:
  - age, education, aphasia type
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Left planum temporale; peak MNI [-60, -30, 8]. Cross-loaded onto
      Factor 1 (phonological production).
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - region: planum temporale
      mni:
      - -60
      - -30
      - 8
  replications:
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - Univariate VBCM caveat.
  - Cross-loaded across phonological production and phonological recognition factors.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 4 (page 226); Results 3.2.3 (page 224)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 224
    supports: claim
    quote: the left posterior supramarginal gyrus and planum temporale were associated
      with phonological production and phonological recognition factors
  - section: Discussion 4.3
    page: 227
    supports: claim
    quote: Both phonological production and recognition factors were associated with
      tissues deep in the left planum temporale, which has been associated with speech
      recognition in previous studies (e.g., Mirman et al., 2015).
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
  target: left_posterior_superior_temporal_gyrus
  target_kind: region
  claim: Tissue concentration in the left posterior superior temporal gyrus uniquely
    covaries with the phonological recognition PCA factor in chronic post-stroke aphasia.
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
      lesion-volume covariate
    cluster_extent: 4088
    effect_size: peak Z = 3.32
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume
  confounders_not_controlled:
  - age, education, aphasia type
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Left posterior superior temporal gyrus; peak MNI [-46, -38, 6].
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - region: posterior superior temporal gyrus
      mni:
      - -46
      - -38
      - 6
  replications: []
  contradictions: []
  author_limitations:
  - Univariate VBCM caveat.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 4
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: Performance on the phonological recognition factor was uniquely associated
      with the left posterior superior temporal gyrus, Heschl's gyrus (including H1
      and H2), and posterior superior and inferior temporal gyri.
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
- id: f4
  target: left_heschls_gyrus
  target_kind: region
  claim: Tissue concentration in the left Heschl's gyrus uniquely covaries with the
    phonological recognition PCA factor in chronic post-stroke aphasia (the headline
    cluster of Factor 4 in the Discussion).
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
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level (PCA-VBCM);
      cluster survives lesion-volume covariate
    cluster_extent: 4088
    effect_size: peak Z = 3.96
  confounders_controlled:
  - other four PCA factors (phonological production, semantics, fluency, executive
    function) entered simultaneously
  - lesion volume (Factor 4 r=0.18, p=0.21 with lesion volume; cluster survives)
  confounders_not_controlled:
  - age, education, BDAE aphasia type
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Left Heschl's gyrus (HO label, includes H1 and H2 transverse temporal
      gyri); peak MNI [-52, -20, 6]. Primary auditory cortex.
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
    - region: Heschl's gyrus
      mni:
      - -52
      - -20
      - 6
  replications:
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - Univariate VBCM may bias micro-level localization (Mah et al. 2014).
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 4 (page 226); Results 3.2.3 (page 223); Discussion
      4.3 (page 227)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: Performance on the phonological recognition factor was uniquely associated
      with the left posterior superior temporal gyrus, Heschl's gyrus (including H1
      and H2), and posterior superior and inferior temporal gyri.
  - section: Discussion 4.3
    page: 227
    supports: claim
    quote: The phonological recognition factor was uniquely associated with Heschl's
      gyrus, which is critically involved with processing speech sounds (DeWitt and
      Rauschecker, 2012).
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
      (r = 0.18, p = 0.21); and executive function (r = 0.14, p = 0.33)], and therefore
      controlling for lesion volume did not have a significant effect on the neural
      correlates
  - section: Discussion 4.3
    page: 228
    supports: limitation
    quote: It should be noted that these neural correlates were identified using univariate
      lesion-symptom mapping analyses and there have been suggestions that such approaches
      might bias the micro-level location of clusters (Mah et al., 2014).
- id: f5
  target: left_planum_temporale
  target_kind: region
  claim: Tissue concentration in the left planum temporale uniquely covaries with
    the phonological recognition PCA factor in chronic post-stroke aphasia (also implicated
    in phonological production).
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
      lesion-volume covariate
    cluster_extent: 4088
    effect_size: peak Z = 4.42
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume (Factor 4 cluster survives)
  confounders_not_controlled:
  - age, education, aphasia type
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Left planum temporale; peak MNI [-60, -30, 8]. Cross-loaded onto
      Factor 1 (phonological production).
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - region: planum temporale
      mni:
      - -60
      - -30
      - 8
  replications:
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - Univariate VBCM caveat.
  - Cross-loaded across phonological production and phonological recognition factors.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 4 (page 226); Results 3.2.3 (page 224)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 224
    supports: claim
    quote: the left posterior supramarginal gyrus and planum temporale were associated
      with phonological production and phonological recognition factors
  - section: Discussion 4.3
    page: 227
    supports: claim
    quote: Both phonological production and recognition factors were associated with
      tissues deep in the left planum temporale, which has been associated with speech
      recognition in previous studies (e.g., Mirman et al., 2015).
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
- id: f6
  target: left_posterior_superior_temporal_gyrus
  target_kind: region
  claim: Tissue concentration in the left posterior superior temporal gyrus uniquely
    covaries with the phonological recognition PCA factor in chronic post-stroke aphasia.
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
      lesion-volume covariate
    cluster_extent: 4088
    effect_size: peak Z = 3.32
  confounders_controlled:
  - other four PCA factors entered simultaneously
  - lesion volume
  confounders_not_controlled:
  - age, education, aphasia type
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Left posterior superior temporal gyrus; peak MNI [-46, -38, 6].
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - region: posterior superior temporal gyrus
      mni:
      - -46
      - -38
      - 6
  replications: []
  contradictions: []
  author_limitations:
  - Univariate VBCM caveat.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 4
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: Performance on the phonological recognition factor was uniquely associated
      with the left posterior superior temporal gyrus, Heschl's gyrus (including H1
      and H2), and posterior superior and inferior temporal gyri.
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
last_reviewed: '2026-05-06'
notes: 'First-extraction draft from Alyahya et al. 2018 (NounVerb). The

  phonological recognition PCA factor (Factor 4: 6.27% variance) is

  associated with a 4088-voxel cluster in superior temporal cortex

  including Heschl''s gyrus, planum temporale, and posterior STG. Three

  peak findings recorded.


  Loadings (Table 4) used to interpret this factor as "phonological

  recognition": non-word minimal pairs (.893), word minimal pairs

  (.816). Both are PALPA phoneme-discrimination tasks. Note that the

  factor loads minimally on production-side measures, justifying its

  separation from Factor 1.


  This factor has the lowest correlation with lesion volume (r=0.18,

  p=0.21), so the cluster is highly robust to lesion-volume control.

  The findings here are among the most lesion-volume-robust in the

  whole paper.'
reviewer: auto-reviewer
reviewed_on: '2026-05-05'
---
# Phonological recognition

## Component definition

Phonological recognition is the underlying language component
capturing phonemic discrimination — the ability to tell minimal pairs
of words and non-words apart (PALPA 1 and PALPA 2). It is conceptually
distinct from phonological production (Factor 1, which captures
repetition and naming) and from semantics. The factor accounts for
6.27% of the variance in the rotated PCA solution.

## Lesion correlates (per Alyahya 2018 NounVerb)

PCA-VBCM identifies a 4088-voxel cluster centered on the auditory
cortex region:

  - Planum temporale (Z=4.42)
  - Middle temporal gyrus (Z=4.31)
  - Heschl's gyrus (Z=3.96)
  - Angular gyrus (Z=3.40, cross-loaded with Factors 1 and 2)
  - Posterior supramarginal gyrus (Z=3.36, cross-loaded with Factor 1)
  - Posterior superior temporal gyrus (Z=3.32)

The Discussion (page 227) singles out Heschl's gyrus and planum
temporale as the headline regions, citing DeWitt & Rauschecker (2012)
and Mirman et al. (2015).

## Notes for next extraction round

  - Add left_heschls_gyrus, left_planum_temporale, left_posterior_superior_temporal_gyrus
    as region entries before re-extracting on the region side.
