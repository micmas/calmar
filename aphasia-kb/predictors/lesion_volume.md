---
schema_version: 2.3
id: lesion_volume
name: Total lesion volume
aliases:
- lesion volume
- lesion size
- infarct volume
- total infarct volume
kind: predictor
predictor_type: imaging_metric
short_definition: Total volume of structural damage on the patient's lesion mask,
  typically reported in millilitres (cubic centimetres) of T1- or FLAIR-defined tissue
  loss.
units: ml (cc)
typical_range: <1 ml (lacunar) to >300 ml (large MCA territory)
direction_of_severity: higher_is_worse
status: approved
reviewer: human:michele
reviewed_on: 2026-05-01
created_by: human:michele
created_on: 2026-05-01
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  instrument: Object and Action Naming Battery (OANB) — single-word naming and picture-to-word
    matching
  score_band: raw counts 0–32 per test (lower = more severe)
  interpretation: Total lesion volume is strongly correlated with single-word naming
    and comprehension performance in chronic post-stroke aphasia, accounting for a
    substantial portion of inter-individual variance regardless of lesion location.
  claim: Total lesion volume strongly correlates with single-word verb naming, noun
    naming, verb picture-to-word matching, and noun picture-to-word matching in chronic
    post-stroke aphasia (Pearson r = .56–.67, p<.0001 for all four measures).
  direction: likely
  relationship: correlational
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
    threshold: Pearson product-moment correlation, p<.0001 for all four behavioural
      measures
    effect_size: verb naming r=.65; verb picture-to-word matching r=.67; noun naming
      r=.62; noun picture-to-word matching r=.56
    ci_95: not_reported
    p_value: <.0001
  confounders_controlled:
  - no covariates — direct Pearson correlation
  confounders_not_controlled:
  - age (range 44–87 years)
  - education (range 9–19 years)
  - time post-stroke (range 12–280 months)
  - BDAE aphasia type
  region_definition:
    kind: data_driven_cluster
    description: Lesion volume measured as voxel count on the binarized lesion mask
      produced by Seghier et al. 2008's automated lesion identification pipeline (U-threshold
      = 0.5).
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
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008 unified segmentation-normalisation;
      lesion U-threshold 0.5; volume measured in MNI152 normalised space at 2 mm³
      resolution
    reference_space: MNI152
    atlases_used: []
  replications:
  - '@Yourganov2015Predicting'
  contradictions: []
  author_limitations:
  - Lesion volume measured in MNI-normalised space (warping inflates apparent volume
    relative to native space).
  - Automated lesion identification (Seghier 2008) detects abnormal-tissue-class voxels
    — captures gliosis and atrophy alongside the primary lesion.
  - U-threshold of 0.5 was used (vs. default 0.3) — different from many other groups'
    pipelines.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.2.4 (page 225)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.4 — Effect of lesion size
    page: 225
    supports: claim
    quote: 'lesion volume correlated with behavioural performance on all four measures
      (verb naming: r = 0.65, verb picture-to-word matching: r = 0.67, noun naming:
      r = 0.62, and noun picture-to-word matching: r = 0.56, p < 0.0001).'
  - section: Methods 2.1 — Participants
    page: 217
    supports: sample
    quote: Forty-eight stroke patients (single left ischaemic or haemorrhagic stroke)
      with chronic aphasia participated in this study (34 males and 14 females).
  - section: Methods 2.4 — Acquisition and processing of neuroimaging data
    page: 219
    supports: imaging_details
    quote: Each patient's lesion was automatically identified using a fully automated
      method based on fuzzy clustering (Seghier et al., 2008). The default parameters
      were used aside from the lesion definition 'U-threshold', which was set to 0.5
      rather than 0.3 to create a binary lesion image.
  - section: Methods 2.5
    page: 220
    supports: method
    quote: each patient's lesion volume (proxy of neurological severity) obtained
      from the output of the automated lesion identification procedure (Seghier et
      al., 2008) was entered as a covariate in subsequent VBCM analyses
  - section: Methods 2.5
    page: 220
    supports: confounders
    quote: by partialling out lesion volume there is a high risk for type II error.
      Hence, all VBCM analyses were performed and reported in this paper once with
      the behaviours of interest only and once with a correction for lesion volume.
  - section: Discussion 4.2
    page: 227
    supports: limitation
    quote: It must be noted that lesion-symptom mapping performed on a single noun
      or verb tests should be treated with some caution, due to their high correlation
      with lesion volume.
- id: f2
  target: fluency
  target_kind: impairment
  claim: Total lesion volume strongly predicts the fluency PCA factor in chronic post-stroke
    aphasia (r=.59, p<.0001), and adding lesion volume as a covariate eliminates all
    significant lesion-symptom clusters for this factor.
  direction: likely
  relationship: correlational
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
    threshold: Pearson product-moment correlation, p<.0001
    effect_size: r = 0.59
    p_value: <.0001
  confounders_controlled: []
  confounders_not_controlled:
  - age, education, time post-stroke, BDAE type
  region_definition:
    kind: data_driven_cluster
    description: Lesion volume in MNI-normalised binarized mask. Fluency PCA factor
      derived from words-per-minute, mean length of utterance, number of tokens (Cookie
      Theft picture description) and backward digit span.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used: []
  replications: []
  contradictions: []
  author_limitations:
  - Strongest lesion-volume confound across the five PCA factors — fluency findings
    need explicit lesion-volume control.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.2.4 (pages 225–226)
    confidence: high
    flags:
    - target id 'fluency' is the impairment id created in drafts/impairments/fluency__Alyahya2018NounVerb.md
      from this same paper.
  source_passages:
  - section: Results 3.2.4
    page: 226
    supports: claim
    quote: there were no significant clusters remaining for the fluency factor (correlation
      with lesion volume r = 0.59, p < 0.0001).
  - section: Methods 2.5
    page: 220
    supports: method
    quote: each patient's lesion volume (proxy of neurological severity) obtained
      from the output of the automated lesion identification procedure (Seghier et
      al., 2008) was entered as a covariate in subsequent VBCM analyses
  - section: Methods 2.4
    page: 219
    supports: imaging_details
    quote: Each patient's lesion was automatically identified using a fully automated
      method based on fuzzy clustering (Seghier et al., 2008). The default parameters
      were used aside from the lesion definition 'U-threshold', which was set to 0.5
      rather than 0.3 to create a binary lesion image.
  - section: Methods 2.5
    page: 220
    supports: statistics
    quote: by partialling out lesion volume there is a high risk for type II error.
      Hence, all VBCM analyses were performed and reported in this paper once with
      the behaviours of interest only and once with a correction for lesion volume.
- id: f3
  target: phonological_production
  target_kind: impairment
  claim: Total lesion volume does NOT significantly correlate with the phonological
    production PCA factor in chronic post-stroke aphasia (r=.22, p=.12); the lesion-symptom
    cluster for this factor is robust to lesion-volume control.
  direction: no_effect
  relationship: correlational
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
    threshold: Pearson product-moment correlation; null finding at p=.12
    effect_size: r = 0.22
    p_value: '.12'
  confounders_controlled: []
  confounders_not_controlled:
  - age, education, time post-stroke, BDAE type
  region_definition:
    kind: data_driven_cluster
    description: Lesion volume in MNI-normalised binarized mask. Phonological production
      PCA factor primarily indexed by repetition and naming.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used: []
  replications: []
  contradictions: []
  author_limitations: []
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.2.4 (page 225)
    confidence: high
    flags:
    - Useful negative finding — establishes that the phonological_production lesion
      map (Factor 1) is independent of total lesion volume. Reviewers should preserve
      this when promoting Factor 1 region findings.
  source_passages:
  - section: Results 3.2.4
    page: 225
    supports: claim
    quote: Three of the five components did not significantly correlate with lesion
      volume [phonological production (r = 0.22, p = 0.12); phonological recognition
      (r = 0.18, p = 0.21); and executive function (r = 0.14, p = 0.33)], and therefore
      controlling for lesion volume did not have a significant effect on the neural
      correlates identified from the previous analysis
  - section: Methods 2.5
    page: 220
    supports: statistics
    quote: by partialling out lesion volume there is a high risk for type II error.
      Hence, all VBCM analyses were performed and reported in this paper once with
      the behaviours of interest only and once with a correction for lesion volume.
  - section: Methods 2.5
    page: 220
    supports: method
    quote: each patient's lesion volume (proxy of neurological severity) obtained
      from the output of the automated lesion identification procedure (Seghier et
      al., 2008) was entered as a covariate in subsequent VBCM analyses
  - section: Methods 2.4
    page: 219
    supports: imaging_details
    quote: Each patient's lesion was automatically identified using a fully automated
      method based on fuzzy clustering (Seghier et al., 2008). The default parameters
      were used aside from the lesion definition 'U-threshold', which was set to 0.5
      rather than 0.3 to create a binary lesion image.
- id: f4
  target: severity_metric
  target_kind: predictor
  instrument: Object and Action Naming Battery (OANB) — single-word naming and picture-to-word
    matching
  score_band: raw counts 0–32 per test (lower = more severe)
  interpretation: Total lesion volume is strongly correlated with single-word naming
    and comprehension performance in chronic post-stroke aphasia, accounting for a
    substantial portion of inter-individual variance regardless of lesion location.
  claim: Total lesion volume strongly correlates with single-word verb naming, noun
    naming, verb picture-to-word matching, and noun picture-to-word matching in chronic
    post-stroke aphasia (Pearson r = .56–.67, p<.0001 for all four measures).
  direction: likely
  relationship: correlational
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
    threshold: Pearson product-moment correlation, p<.0001 for all four behavioural
      measures
    effect_size: verb naming r=.65; verb picture-to-word matching r=.67; noun naming
      r=.62; noun picture-to-word matching r=.56
    ci_95: not_reported
    p_value: <.0001
  confounders_controlled:
  - no covariates — direct Pearson correlation
  confounders_not_controlled:
  - age (range 44–87 years)
  - education (range 9–19 years)
  - time post-stroke (range 12–280 months)
  - BDAE aphasia type
  region_definition:
    kind: data_driven_cluster
    description: Lesion volume measured as voxel count on the binarized lesion mask
      produced by Seghier et al. 2008's automated lesion identification pipeline (U-threshold
      = 0.5).
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
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008 unified segmentation-normalisation;
      lesion U-threshold 0.5; volume measured in MNI152 normalised space at 2 mm³
      resolution
    reference_space: MNI152
    atlases_used: []
  replications:
  - '@Yourganov2015Predicting'
  contradictions: []
  author_limitations:
  - Lesion volume measured in MNI-normalised space (warping inflates apparent volume
    relative to native space).
  - Automated lesion identification (Seghier 2008) detects abnormal-tissue-class voxels
    — captures gliosis and atrophy alongside the primary lesion.
  - U-threshold of 0.5 was used (vs. default 0.3) — different from many other groups'
    pipelines.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.2.4 (page 225)
    confidence: high
    flags: []
  source_passages:
  - section: Results 3.2.4 — Effect of lesion size
    page: 225
    supports: claim
    quote: 'lesion volume correlated with behavioural performance on all four measures
      (verb naming: r = 0.65, verb picture-to-word matching: r = 0.67, noun naming:
      r = 0.62, and noun picture-to-word matching: r = 0.56, p < 0.0001).'
  - section: Methods 2.1 — Participants
    page: 217
    supports: sample
    quote: Forty-eight stroke patients (single left ischaemic or haemorrhagic stroke)
      with chronic aphasia participated in this study (34 males and 14 females).
  - section: Methods 2.4 — Acquisition and processing of neuroimaging data
    page: 219
    supports: imaging_details
    quote: Each patient's lesion was automatically identified using a fully automated
      method based on fuzzy clustering (Seghier et al., 2008). The default parameters
      were used aside from the lesion definition 'U-threshold', which was set to 0.5
      rather than 0.3 to create a binary lesion image.
  - section: Methods 2.5
    page: 220
    supports: method
    quote: each patient's lesion volume (proxy of neurological severity) obtained
      from the output of the automated lesion identification procedure (Seghier et
      al., 2008) was entered as a covariate in subsequent VBCM analyses
  - section: Methods 2.5
    page: 220
    supports: confounders
    quote: by partialling out lesion volume there is a high risk for type II error.
      Hence, all VBCM analyses were performed and reported in this paper once with
      the behaviours of interest only and once with a correction for lesion volume.
  - section: Discussion 4.2
    page: 227
    supports: limitation
    quote: It must be noted that lesion-symptom mapping performed on a single noun
      or verb tests should be treated with some caution, due to their high correlation
      with lesion volume.
- id: f5
  target: fluency
  target_kind: impairment
  claim: Total lesion volume strongly predicts the fluency PCA factor in chronic post-stroke
    aphasia (r=.59, p<.0001), and adding lesion volume as a covariate eliminates all
    significant lesion-symptom clusters for this factor.
  direction: likely
  relationship: correlational
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
    threshold: Pearson product-moment correlation, p<.0001
    effect_size: r = 0.59
    p_value: <.0001
  confounders_controlled: []
  confounders_not_controlled:
  - age, education, time post-stroke, BDAE type
  region_definition:
    kind: data_driven_cluster
    description: Lesion volume in MNI-normalised binarized mask. Fluency PCA factor
      derived from words-per-minute, mean length of utterance, number of tokens (Cookie
      Theft picture description) and backward digit span.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used: []
  replications: []
  contradictions: []
  author_limitations:
  - Strongest lesion-volume confound across the five PCA factors — fluency findings
    need explicit lesion-volume control.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.2.4 (pages 225–226)
    confidence: high
    flags:
    - target id 'fluency' is the impairment id created in drafts/impairments/fluency__Alyahya2018NounVerb.md
      from this same paper.
  source_passages:
  - section: Results 3.2.4
    page: 226
    supports: claim
    quote: there were no significant clusters remaining for the fluency factor (correlation
      with lesion volume r = 0.59, p < 0.0001).
  - section: Methods 2.5
    page: 220
    supports: method
    quote: each patient's lesion volume (proxy of neurological severity) obtained
      from the output of the automated lesion identification procedure (Seghier et
      al., 2008) was entered as a covariate in subsequent VBCM analyses
  - section: Methods 2.4
    page: 219
    supports: imaging_details
    quote: Each patient's lesion was automatically identified using a fully automated
      method based on fuzzy clustering (Seghier et al., 2008). The default parameters
      were used aside from the lesion definition 'U-threshold', which was set to 0.5
      rather than 0.3 to create a binary lesion image.
  - section: Methods 2.5
    page: 220
    supports: statistics
    quote: by partialling out lesion volume there is a high risk for type II error.
      Hence, all VBCM analyses were performed and reported in this paper once with
      the behaviours of interest only and once with a correction for lesion volume.
- id: f6
  target: phonological_production
  target_kind: impairment
  claim: Total lesion volume does NOT significantly correlate with the phonological
    production PCA factor in chronic post-stroke aphasia (r=.22, p=.12); the lesion-symptom
    cluster for this factor is robust to lesion-volume control.
  direction: no_effect
  relationship: correlational
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
    threshold: Pearson product-moment correlation; null finding at p=.12
    effect_size: r = 0.22
    p_value: '.12'
  confounders_controlled: []
  confounders_not_controlled:
  - age, education, time post-stroke, BDAE type
  region_definition:
    kind: data_driven_cluster
    description: Lesion volume in MNI-normalised binarized mask. Phonological production
      PCA factor primarily indexed by repetition and naming.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 + OptiBET + Seghier 2008
    reference_space: MNI152
    atlases_used: []
  replications: []
  contradictions: []
  author_limitations: []
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.2.4 (page 225)
    confidence: high
    flags:
    - Useful negative finding — establishes that the phonological_production lesion
      map (Factor 1) is independent of total lesion volume. Reviewers should preserve
      this when promoting Factor 1 region findings.
  source_passages:
  - section: Results 3.2.4
    page: 225
    supports: claim
    quote: Three of the five components did not significantly correlate with lesion
      volume [phonological production (r = 0.22, p = 0.12); phonological recognition
      (r = 0.18, p = 0.21); and executive function (r = 0.14, p = 0.33)], and therefore
      controlling for lesion volume did not have a significant effect on the neural
      correlates identified from the previous analysis
  - section: Methods 2.5
    page: 220
    supports: statistics
    quote: by partialling out lesion volume there is a high risk for type II error.
      Hence, all VBCM analyses were performed and reported in this paper once with
      the behaviours of interest only and once with a correction for lesion volume.
  - section: Methods 2.5
    page: 220
    supports: method
    quote: each patient's lesion volume (proxy of neurological severity) obtained
      from the output of the automated lesion identification procedure (Seghier et
      al., 2008) was entered as a covariate in subsequent VBCM analyses
  - section: Methods 2.4
    page: 219
    supports: imaging_details
    quote: Each patient's lesion was automatically identified using a fully automated
      method based on fuzzy clustering (Seghier et al., 2008). The default parameters
      were used aside from the lesion definition 'U-threshold', which was set to 0.5
      rather than 0.3 to create a binary lesion image.
notes: Starter entry for schema v2.3. Lesion volume is the single most-controlled-for
  covariate in lesion-symptom mapping. Findings here should be reserved for *predictive*
  claims (volume → severity / recovery / therapy response), not the trivial "bigger
  lesion = more damage" tautology. Be careful to track whether a paper measures volume
  in native or MNI space — ratios change with normalisation.
last_reviewed: '2026-05-06'
---
# Total lesion volume

Total lesion volume is the simplest possible imaging metric and one of
the most robust predictors of aphasia outcome — but it is also the one
most prone to acting as a confound rather than a signal. A useful
finding here is one where volume is shown to predict an outcome
*independently of* lesion location, or one where the predictive
validity of a regional finding holds *after controlling for* total
volume.

Common pitfalls to flag in the `provenance.flags` of any finding under
this entry:

- Volume measured in native vs. normalised space (MNI volumes are
  systematically larger after warping)
- Acute vs. chronic measurement (acute oedema inflates apparent
  volume; chronic atrophy can shrink it)
- Whether white-matter hyperintensities, microbleeds, or old strokes
  are included or excluded
- The threshold used to binarise the lesion (manual tracing vs.
  intensity threshold vs. atlas-based segmentation)
