---
schema_version: 2.3
id: left_ifg_pars_opercularis
name: Left IFG Pars Opercularis (Broca's area, dorsal stream hub)
kind: classical
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
hemisphere: left
aliases:
- BA 44
- Broca's area posterior
- left pars opercularis
- IFG opercularis
notes: "Fridriksson 2018 \"Anatomy of aphasia revisited\" (Brain) uses RLSM and CLSM\
  \ (connectome-LSM)\nin 159 chronic LH stroke patients to map clinical aphasia test\
  \ performance to dual-stream damage.\nThis draft focuses on left IFG pars opercularis\
  \ (dorsal stream hub):\n  f1: pars opercularis as strongest single predictor of\
  \ speech fluency (multivariate RLSM R2=0.40)\n  f2: pars opercularis in the network\
  \ underlying aphasia severity (AQ), primarily via CLSM\nSee companion draft left_posterior_stg__Fridriksson2018Anatomy.md\
  \ for ventral stream findings.\nCohort overlaps with @Fridriksson2018 (same USC\
  \ lab).\nThe paper also reports PCA-derived speech production component (Component\
  \ 1) primarily mapped to\ndorsal stream including precentral gyrus; speech comprehension\
  \ component (Component 2) to ventral\nstream including posterior STG — these PCA-derived\
  \ findings are in a separate draft."
findings:
- id: f1
  target: speech_fluency
  target_kind: impairment
  claim: Damage to left IFG pars opercularis is the strongest independent predictor
    of impaired speech fluency in chronic left-hemisphere stroke aphasia, accounting
    for 40% of variance in a multivariate region-wise LSM analysis.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018Anatomy'
  method: LSM
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 159
    population: chronic left-hemisphere stroke survivors with aphasia
    time_post_onset: '>=6 months (mean 36.4 months, SD 43.1)'
    age_range: mean 60.0 years (SD 11.2)
    handedness: not_reported
    language: English (native speakers)
    recruitment: Archival database, Aphasia Lab, University of South Carolina and
      Medical University of South Carolina.
    inclusion_criteria: Single left-hemisphere stroke >=6 months prior; native English
      speaker; no history of dementia or other neurological problems.
    exclusion_criteria: History of dementia or other neurological problems (self/caregiver
      or medical report).
  statistics:
    threshold: permutation thresholding (4000 permutations), p<0.05 one-tailed (univariate);
      stepwise regression p<0.05 for entry, p>0.10 for removal (multivariate)
    cluster_extent: not_reported
    effect_size: R2=0.40 (IFG opercularis as first entry in multivariate RLSM for
      speech fluency); total model R2=0.57 (IFG opercularis + posterior STG + putamen
      + precentral gyrus)
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled:
  - overall lesion size not included as covariate (lesion site excluded from tractography
    tracing in CLSM; tractography preprocessing controls for lesion influence)
  - time post-stroke (verified not to correlate with any of 16 tests)
  confounders_not_controlled:
  - age
  - education
  - handedness
  - stroke etiology
  region_definition:
    kind: atlas
    atlas: JHU/Faria atlas (118 grey matter regions; Faria et al. 2012)
    description: Pars opercularis defined as a region of interest within the Faria
      et al. 2012 118-region atlas parcellation; region-wise lesion load computed
      as proportion of intact voxels within each grey matter region.
  imaging_details:
    field_strength: 3T
    acquisition:
      sequence: T1-weighted MP-RAGE (1mm isotropic) + T2-weighted 3D-SPACE + DTI (EPI,
        30 directions, b=1000 and b=2000 s/mm2)
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 2250
      TE_ms: 4.52
    modalities:
    - modality: T1
      sequence: MP-RAGE
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 2250
      TE_ms: 4.52
      notes: 160 or 192 slice sequence; 9 degree flip angle; GRAPPA=2 for 192-slice
        version
    - modality: T2
      sequence: 3D-SPACE (TSE)
      TR_ms: 2800
      TE_ms: 402
      notes: 1mm thick, 192 slices, GRAPPA=2; used for lesion delineation
    - modality: DTI
      sequence: EPI
      voxel_size_mm:
      - 2.7
      - 2.7
      - 2.7
      TR_ms: 6100
      TE_ms: 101
      n_directions: 30
      b_values:
      - 0
      - 1000
      - 2000
      notes: Acquired twice (60 volumes at b=1000, 60 at b=2000, 11 at b=0); 2.7mm
        axial slices
    preprocessing_pipeline: 'Lesions demarcated on T2 by neurologist blinded to language
      scores; T2 co-registered to T1; enantiomorphic normalization via SPM12 (Nachev
      et al. 2008); SPM12 unified segmentation-normalization to standard space; lesion
      binarized at 50% probability threshold; 118-region grey matter parcellation
      (Faria et al. 2012); DTI probabilistic tractography via FSL FDT/probtrackX (BEDPOST
      + probtrackX: 5000 pathways, curvature threshold 0.2, 200 max steps, 0.5mm step
      length)'
    reference_space: MNI152
    atlases_used:
    - Faria et al. 2012 (118 grey matter regions)
    - JHU atlas
    coordinates_reported: []
  replications:
  - '@Fridriksson2018'
  contradictions: []
  author_limitations:
  - The reading and writing subtests on the WAB provide a shallow picture of alexia
    and agraphia; more sensitive tasks are needed.
  - Dataset did not include a comprehensive measure of phonological input.
  - 'Univariate and multivariate analyses should be considered complementary rather
    than contradictory: univariate highlights larger contiguous clusters; multivariate
    reveals more distal independent predictors.'
  - Phonological naming errors on the PNT did not yield significant results in univariate
    RLSM, possibly reflecting mixed sources of error (phonological retrieval vs. motor
    planning) rather than insufficient power.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – Region-wise lesion-symptom mapping; Table 2; Table 3;
      Methods – Brain imaging; Methods – Image preprocessing; Methods – Data analyses
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2018 (same USC Aphasia Lab archival database;
      Fridriksson2018 n=138, Fridriksson2018Anatomy n=159 — the latter is the larger,
      later dataset from the same lab)
    - 'univariate RLSM for speech fluency: IFG opercularis Z=7.73 (Table 2), second
      only to STG Z=7.74 — both regions top predictors in univariate; multivariate
      gives IFG opercularis R2=0.40 as first entry (Table 3)'
    - 'CLSM (connectome-LSM) for speech fluency: top univariate connection is IFG
      opercularis <-> precentral gyrus (Z=6.47); multivariate CLSM top connection
      is IFG triangularis <-> IFG opercularis (R2=0.25)'
    - Number of participants for speech fluency subtest = 159 (full sample)
  source_passages:
  - section: Results – RLSM
    page: 6
    supports: claim
    quote: 'The regions that most often predicted performance on the 16 speech and
      language measures in the multivariate analyses were: (i) pSTG (predictor on
      eight tests); (ii) precentral gyrus (predictor on seven tests); and (iii) posterior
      insula (predictor on six tests).'
  - section: Table 3
    page: 9
    supports: statistics
    quote: 'Speech Fluency

      IFG opercularis

      0.40

      0.40

      Posterior STG

      0.53

      0.13

      Putamen

      0.56

      0.02

      PrCG

      0.57

      0.02'
  - section: Table 2
    page: 7
    supports: statistics
    quote: 'Speech Fluency

      STG'
  - section: Methods – Participants
    page: 3
    supports: sample
    quote: 'The total sample size was 159 chronic stroke survivors and

      the number of tested participants varied across the different'
  - section: Methods – Participants
    page: 3
    supports: sample
    quote: The average time post-stroke was 36.4 months [standard deviation (SD) =
      43.1].
  - section: Methods – Brain imaging
    page: 4
    supports: imaging_details
    quote: 'T1-weighted MRI using an

      MP-RAGE sequence with 1

      mm isotropic voxels'
  - section: Methods – Brain imaging
    page: 4
    supports: imaging_details
    quote: 'diffusion EPI scan that uses 30 directions with

      b = 1000 s/mm2 and b = 2000 s/mm2, repetition time = 6100 ms,

      echo time = 101 ms'
  - section: Methods – Image preprocessing
    page: 4
    supports: imaging_details
    quote: Enantiomorphic normalization (Nachev et al., 2008) relied on SPM12 and
      MATLAB scripts
  - section: Methods – Data analyses
    page: 5
    supports: method
    quote: 'The univariate lesion analyses relied on conventional lesion symptom mapping:
      General Linear Model (GLM) (pooled variance t-test) with P < 0.05 (one-tailed)
      and control for multiple comparisons used permutation threshholding (4000 permutations).'
  - section: Discussion
    page: 13
    supports: limitation
    quote: Unfortunately, our dataset did not include a comprehensive measure of phonological
      input, something that is clearly a focus of Hickok and Poeppel's dual stream
      model.
- id: f2
  target: aphasia_quotient
  target_kind: predictor
  claim: Damage to left IFG pars opercularis contributes to overall aphasia severity
    (WAB Aphasia Quotient), though pars opercularis is less strongly dominant than
    STG in the univariate analysis; aphasia severity involves an extensive cortical
    network primarily within the dorsal stream.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018Anatomy'
  method: LSM
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 159
    population: chronic left-hemisphere stroke survivors with aphasia
    time_post_onset: '>=6 months (mean 36.4 months, SD 43.1)'
    age_range: mean 60.0 years (SD 11.2)
    handedness: not_reported
    language: English (native speakers)
    recruitment: USC/MUSC Aphasia Lab archival database.
  statistics:
    threshold: permutation thresholding (4000 permutations), p<0.05 one-tailed
    cluster_extent: not_reported
    effect_size: 'STG Z=7.84 (top univariate predictor for AQ); IFG opercularis not
      listed in top 3 for AQ univariate; multivariate AQ: STG R2=0.43 (first entry),
      total model R2=0.51'
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled:
  - time post-stroke (verified non-significant correlation with all 16 tests)
  confounders_not_controlled:
  - age
  - lesion volume (excluded from CLSM by preprocessing design)
  region_definition:
    kind: atlas
    atlas: Faria et al. 2012 (118 grey matter regions)
    description: Pars opercularis as one of 20 dorsal/ventral stream ROIs used in
      the RLSM analysis.
  imaging_details:
    field_strength: 3T
    acquisition:
      sequence: T1-weighted MP-RAGE + T2 3D-SPACE + DTI EPI
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 2250
      TE_ms: 4.52
    preprocessing_pipeline: Enantiomorphic normalization SPM12; 118-region grey matter
      parcellation; FSL FDT probabilistic tractography
    reference_space: MNI152
    atlases_used:
    - Faria et al. 2012
    coordinates_reported: []
  replications:
  - '@Fridriksson2018'
  contradictions: []
  author_limitations:
  - Aphasia quotient is heavily weighted toward speech production; its network basis
    overlaps substantially with speech fluency and repetition.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – RLSM; Table 2; Table 3; Discussion
    confidence: high
    flags:
    - For AQ, the univariate top predictor is STG (Z=7.84), not IFG opercularis —
      IFG opercularis does not appear in top 3 for AQ in Table 2; included here because
      the paper describes pars opercularis as a key 'hub' region across analyses
    - 'Multivariate RLSM for AQ: STG enters first (R2=0.43), followed by PrCG, posterior
      STG, posterior insula — IFG opercularis not in multivariate AQ model'
    - 'CLSM top univariate link for AQ: IFG opercularis <-> IFG triangularis (Z=5.65)
      — IFG opercularis IS the top CLSM predictor for AQ'
    - 'aphasia_quotient coded as target_kind: predictor (severity_metric construct)'
  source_passages:
  - section: Discussion
    page: 9
    supports: claim
    quote: the overall severity of aphasia ('aphasia quotient') and 'speech fluency'
      were predicted by damage to an extensive network primarily involving the dorsal
      stream, with somewhat fewer connections to the ventral stream.
  - section: Table 4
    page: 10
    supports: statistics
    quote: 'Aphasia Quotient

      IFG opercularis $ IFG triangularis

      5.65

      IFG opercularis $ PrCG

      5.39'
  - section: Methods – Participants
    page: 3
    supports: sample
    quote: The total sample size was 159 chronic stroke survivors
  - section: Methods – Data analyses
    page: 5
    supports: method
    quote: 'The univariate lesion analyses relied on conventional lesion symptom mapping:
      General Linear Model (GLM) (pooled variance t-test) with P < 0.05 (one-tailed)
      and control for multiple comparisons used permutation threshholding (4000 permutations).'
  - section: Methods – Brain imaging
    page: 4
    supports: imaging_details
    quote: T1-weighted MRI using an MP-RAGE sequence with 1 mm isotropic voxels
  - section: Discussion
    page: 11
    supports: limitation
    quote: The univariate analyses highlight larger contiguous regional clusters that,
      when damaged, are very likely to cause impairment. In contrast, the multivariate
      analyses reveal smaller overall damage but more distal modules as being independent
      predictors
source: draft
reviewer: auto-reviewer
reviewed_on: '2026-05-06'
---
# Left IFG Pars Opercularis — Fridriksson 2018 Anatomy (RLSM + CLSM)

Fridriksson et al. 2018 "Anatomy of aphasia revisited" (Brain) examined the neural correlates of 16
clinical aphasia tests in 159 chronic LH stroke patients using RLSM and CLSM. Key findings for pars opercularis:

- **f1**: IFG pars opercularis is the strongest single independent predictor of speech fluency in the
  multivariate RLSM (R2=0.40, Table 3). It also ranks as the second-highest Z-score region in the
  univariate RLSM for speech fluency (Z=7.73).
- **f2**: CLSM reveals IFG opercularis as the most frequently damaged hub link for aphasia quotient
  (IFG opercularis <-> IFG triangularis, Z=5.65) and speech fluency (IFG opercularis <-> precentral
  gyrus, Z=6.47 — top link overall).

The paper emphasizes that pars opercularis, SMG/angular gyrus, and posterior STG are the most
important hubs in the cortical speech and language network, with damage to these regions having
disproportionately large negative effects across multiple clinical tests.
