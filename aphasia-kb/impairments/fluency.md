---
schema_version: 2.3
id: fluency
name: Fluency (speech fluency)
kind: impairment
status: approved
created_by: agent:claude-opus-4-7
created_on: 2026-05-01
short_definition: 'Underlying language component capturing connected-speech fluency:
  words per minute, mean length of utterance, and number of tokens in spontaneous
  speech. One of five orthogonal factors recovered by PCA over the standard chronic-aphasia
  neuropsychological battery (Butler et al. 2014; Halai et al. 2017; Alyahya et al.
  2018). Distinct from the BDAE/WAB clinical fluency dichotomy, which is a binary
  syndromic classification.'
assessment:
- Words per minute (Cookie theft picture description)
- Mean length of utterance (Cookie theft)
- Number of tokens (Cookie theft)
- Backward digit span (loads partially)
findings:
- id: f1
  target: left_anterior_arcuate_fasciculus
  target_kind: region
  claim: Tissue concentration in the anterior segment of the left arcuate fasciculus
    uniquely covaries with the fluency PCA factor in chronic post-stroke aphasia,
    after partialling out the four other principal components.
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
      did NOT survive lesion-volume covariate
    cluster_extent: 6008
    effect_size: peak Z = 3.30
  confounders_controlled:
  - other four PCA factors (phonological production, semantics, phonological recognition,
    executive function) entered simultaneously
  confounders_not_controlled:
  - lesion volume — fluency factor correlated strongly with lesion volume (r=0.59,
    p<0.0001) and the cluster did NOT survive when this was partialled out
  - age, education, BDAE aphasia type
  region_definition:
    kind: tract
    atlas: natbrainlab white-matter atlas (Catani et al. 2012)
    description: Anterior segment of arcuate fasciculus (sometimes referred to as
      the 'long anterior segment' or arcuate-direct in dual-stream models); peak MNI
      [-37, -19, 25].
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
    - region: anterior segment of arcuate fasciculus
      mni:
      - -37
      - -19
      - 25
  replications:
  - '@Marchina2011'
  contradictions: []
  author_limitations:
  - Fluency cluster did NOT survive lesion-volume control — interpretation as fluency-specific
    is weakened.
  - Univariate VBCM may bias micro-level localization (Mah et al. 2014).
  - Discussion notes the fluency factor is also tied to the 'frontal aslant tract'
    (Catani 2013, Halai 2017), which the natbrainlab atlas does not resolve from the
    arcuate; the cluster may include frontal-aslant fibres labelled as 'arcuate' here.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 3 (page 226); Results 3.2.4 (page 225 — does not
      survive lesion volume); Discussion 4.3 (page 228 — frontal aslant tract reference)
    confidence: high
    flags:
    - Discussion emphasises a frontal aslant tract interpretation that this VBCM analysis
      cannot resolve from anterior-arcuate due to atlas limitations — flag for follow-up
      with a higher-resolution tract atlas.
    - When promoting this finding, add 'frontal_aslant_tract' (or 'left_frontal_aslant_tract'
      under the new prefix convention) to the canonical 'left_anterior_arcuate_fasciculus'
      region entry's 'aliases:' list — the natbrainlab atlas conflates these two fibre
      systems, and the paper's Discussion (Catani 2013, Halai 2017, Rojkova 2015)
      prefers the FAT label.
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: Performance on the fluency factor was uniquely associated with left frontal
      and partial regions involving the anterior supramarginal gyrus, central opercular
      cortex, pre- and post-central gyri, posterior parahippocampal gyrus, planum
      polare, parietal operculum cortex and the white matter tracts corresponding
      to frontal aslant tract, cortico-spinal tract, and internal capsule.
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
    page: 226
    supports: confounders
    quote: there were no significant clusters remaining for the fluency factor (correlation
      with lesion volume r = 0.59, p < 0.0001).
  - section: Discussion 4.3
    page: 228
    supports: limitation
    quote: the fluency factor was also associated with white matter tracts most likely
      corresponding to the frontal aslant tract that connects the medial superior
      portion of the frontal lobe to the inferior-lateral frontal region (Rojkova
      et al., 2015).
- id: f2
  target: left_central_opercular_cortex
  target_kind: region
  claim: Tissue concentration in the left central opercular cortex uniquely covaries
    with the fluency PCA factor in chronic post-stroke aphasia (the strongest peak
    in the fluency cluster).
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
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level; did NOT survive
      lesion-volume covariate
    cluster_extent: 6008
    effect_size: peak Z = 4.78
  confounders_controlled:
  - other four PCA factors entered simultaneously
  confounders_not_controlled:
  - lesion volume (cluster did not survive)
  - age, education, aphasia type
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Left central opercular cortex (HO label); peak MNI [-66, -6, 8].
      The lesion-overlap maximum across the whole cohort fell in this region (40 patients
      with damage at MNI -38, -9, 24).
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - region: central opercular cortex
      mni:
      - -66
      - -6
      - 8
  replications: []
  contradictions: []
  author_limitations:
  - Did not survive lesion-volume control.
  - This region is also the lesion-overlap maximum for the cohort, so the finding
    may be partially driven by the spatial distribution of MCA strokes (Phan et al.
    2005).
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 3 peak; Figure 1 caption (lesion overlap)
    confidence: high
    flags:
    - lesion-overlap confound — same coordinate region as the cohort's overlap maximum.
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: Performance on the fluency factor was uniquely associated with left frontal
      and partial regions involving the anterior supramarginal gyrus, central opercular
      cortex, pre- and post-central gyri
  - section: Methods 2.4 — Acquisition and processing
    page: 219
    supports: confounders
    quote: 'Colour scale indicates number of patients with a lesion in that voxel
      (threshold = 1–40). The maximum number of patients who had a lesion in one voxel
      was 40 (MNI coordinate: −38, −9, 24; central opercular cortex).'
  - section: Results 3.2.4
    page: 226
    supports: limitation
    quote: there were no significant clusters remaining for the fluency factor (correlation
      with lesion volume r = 0.59, p < 0.0001).
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
  target: left_pre_central_gyrus
  target_kind: region
  claim: Tissue concentration in the left pre-central gyrus uniquely covaries with
    the fluency PCA factor in chronic post-stroke aphasia.
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
    threshold: p<0.001 voxel-level, FWE-corrected p<0.05 cluster-level; did NOT survive
      lesion-volume covariate
    cluster_extent: 6008
    effect_size: peak Z = 3.58
  confounders_controlled:
  - other four PCA factors entered simultaneously
  confounders_not_controlled:
  - lesion volume
  - age, education, aphasia type
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: 'Left pre-central gyrus; peak MNI [-50, -4, 40]. Note: pre-central
      gyrus also loaded weakly on Factor 5 (executive functions) at lower threshold.'
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - region: pre-central gyrus
      mni:
      - -50
      - -4
      - 40
  replications: []
  contradictions: []
  author_limitations:
  - Did not survive lesion-volume control.
  - Region cross-loaded onto executive-function factor at lower threshold.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 6 Factor 3
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.3
    page: 223
    supports: claim
    quote: Performance on the fluency factor was uniquely associated with left frontal
      and partial regions involving the anterior supramarginal gyrus, central opercular
      cortex, pre- and post-central gyri, posterior parahippocampal gyrus, planum
      polare, parietal operculum cortex
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

  fluency PCA factor (Factor 3: 7.8% variance) is associated with a

  6008-voxel cluster spanning left frontal and parietal regions

  including central opercular cortex, pre- and post-central gyri, and

  the anterior segment of the arcuate fasciculus. Three peak findings

  recorded.


  Loadings (Table 4) used to interpret this factor as "fluency":

  word-per-minute (.837), mean length of utterance (.828), number of

  tokens (.811), backward digit span (.511). All three primary

  loadings derived from coding spontaneous speech in the BDAE Cookie

  Theft picture description task.


  CRITICAL CAVEAT: the fluency cluster did NOT survive when lesion

  volume was added as a covariate (correlation with lesion volume:

  r=0.59, p<0.0001). The fluency factor is the most lesion-volume-

  confounded of the five PCA factors. Promotion of these findings

  should reflect that lesion-volume independence has not been

  demonstrated.


  Discussion (page 228) emphasises that the relevant white-matter tract

  is most likely the frontal aslant tract (Catani 2013, Rojkova 2015,

  Halai 2017) rather than the arcuate per se. The natbrainlab atlas

  used here does not resolve the frontal aslant from the anterior

  arcuate, so the f1 finding may include both fibre systems.'
reviewer: michele
reviewed_on: '2026-05-06'
---
# Fluency (speech fluency)

## Component definition

Connected-speech fluency, operationalised as words per minute, mean
length of utterance, and number of tokens in the BDAE Cookie Theft
picture description task. This is a continuous measure of speech
production rate, distinct from the BDAE/WAB clinical fluency
dichotomy (which is a binary syndromic classification).

## Lesion correlates (per Alyahya 2018 NounVerb)

PCA-VBCM identifies a 6008-voxel cluster with peaks in:

  - Central opercular cortex (Z=4.78)
  - Post-central gyrus (Z=4.48)
  - Pre-central gyrus (Z=3.58)
  - Anterior segment of arcuate fasciculus (Z=3.30)

The cluster does NOT survive lesion-volume covariate. The Discussion
attributes the fluency white-matter finding to the frontal aslant
tract (FAT) on theoretical grounds, but the natbrainlab atlas used
in this paper does not separate FAT from anterior-arcuate.

## Notes for next extraction round

  - Add left_anterior_arcuate_fasciculus, left_central_opercular_cortex,
    left_pre_central_gyrus, post_central_gyrus as region entries before
    re-extracting on the region side.
  - Consider creating a frontal_aslant_tract region entry given the
    Discussion's emphasis on FAT.
  - Findings here should be flagged as "lesion-volume confounded"
    when used in interpret_overlap downstream.
