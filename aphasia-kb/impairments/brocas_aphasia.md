---
schema_version: 2.3
id: brocas_aphasia
name: Broca's aphasia
kind: impairment
status: approved
created_by: agent:claude-opus-4-7
created_on: 2026-05-01
short_definition: Non-fluent aphasia syndrome with effortful, halting speech, agrammatism,
  relatively preserved auditory comprehension, and impaired repetition. Classically
  associated with damage to left posterior inferior frontal cortex.
assessment:
- Western Aphasia Battery (WAB / WAB-R)
- Boston Diagnostic Aphasia Examination (BDAE)
findings:
- id: f1
  target: left_anterior_arcuate_fasciculus
  target_kind: region
  claim: Damage to the anterior segment of the left arcuate fasciculus is the strongest
    predictor of Broca's aphasia in a multivariate (SVM) classification of 98 chronic
    stroke aphasia patients (predictive relevance Z = 3.2).
  direction: likely
  relationship: causal
  citation: '@Yourganov2015Predicting'
  method: MLPA
  design: cross-sectional
  imaging: T1
  sample:
    n: 98
    population: chronic left-hemisphere stroke patients with aphasia (Broca's n=33;
      Wernicke's n=7; conduction n=13; global n=10; anomic n=35)
    time_post_onset: '>=6 months post-stroke; mean 40.1 months (SD 49.6, range 6–276)'
    age_range: mean 58 years (SD 11.9, range 31–80)
    handedness: all right-handed
    language: English (recruited in South Carolina, USA)
    recruitment: referrals from local neurologists and print/radio advertisements;
      behavioural assessment May 2007–Oct 2014 at the University of South Carolina.
    inclusion_criteria: right-handed; chronic left-hemisphere stroke; aphasia present
    exclusion_criteria: absence of aphasia; MRI contraindications; apraxia-of-speech-driven
      deficit; bilateral lesion; multiple sclerosis; transcortical motor aphasia (one
      such patient excluded for sample-size reasons).
  statistics:
    threshold: binomial-distribution test of test-set classification accuracy vs majority-class
      chance, FDR-corrected (p<0.05)
    cluster_extent: null
    effect_size: predictive relevance (weighted Z-score across pairwise contrasts)
      = 3.2 (Table 3)
    ci_95: not_reported
    p_value: not_reported per-region
  confounders_controlled:
  - balanced training set via resampling (handles unequal class sizes)
  - 8-fold cross-validation for SVM hyperparameter (C) optimization
  - lesion-volume effect partially absorbed by per-region damage proportion (vs raw
    voxels)
  confounders_not_controlled:
  - age and time-since-stroke (range 6–276 months — wide)
  - lesion volume not regressed out as a covariate
  - WAB-defined aphasia types (categorical; thresholding subjective)
  region_definition:
    kind: tract
    atlas: AALCTS (custom union of AAL grey-matter and Catani–Thiebaut de Schotten
      white-matter atlases; CTS arcuate split into anterior, long, and posterior segments)
    description: Anterior segment of arcuate fasciculus (CTS atlas; corresponds to
      fronto-parietal connection between IFG and inferior parietal cortex). Lesion
      damage measured as proportion of voxels lesioned in the tract after enantiomorphic
      normalization (SPM12) to MNI space.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: MP-RAGE
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 2250
      TI_ms: 900
      TE_ms: 4.52
      notes: First 25 patients used 160-slice sequence (TI=900, TE=4.52); subsequent
        72 patients used 192-slice sequence (TI=925, TE=4.15) with GRAPPA=2.
    - modality: T2
      sequence: 3D-SPACE
      TR_ms: 2800
      TE_ms: 402
      notes: Lesions were manually drawn on the T2 image by a trained neurologist;
        resliced to T1 native space; smoothed (3mm FWHM).
    preprocessing_pipeline: Enantiomorphic normalization (Nachev et al., 2008) using
      SPM12 unified segmentation + Clinical Toolbox (Rorden et al., 2012); lesion
      binarized at 50% probability after warping.
    reference_space: MNI152
    atlases_used:
    - Speculative Brodmann (82 areas)
    - JHU/Faria 2012 (189 areas, grey + white matter)
    - AAL (Tzourio-Mazoyer 2002; 116 grey-matter areas)
    - Catani–Thiebaut de Schotten 2008 (CTS; 34 white-matter tracts)
    - AALCTS (custom union of AAL + CTS; 150 areas; best-performing for most contrasts)
  replications:
  - '@Marchina2011'
  - '@Fridriksson2018'
  contradictions: []
  author_limitations:
  - Wernicke's group small (n=7) — limits sensitivity for any contrast involving it.
  - Broca's vs global aphasia could not be classified above chance (extensive overlap
    in lesion patterns).
  - WAB-based aphasia type may not match clinical impression for borderline cases.
  - Atlas-based parcellation has lower spatial resolution than voxel-wise approaches.
  - CTS atlas built from 12 healthy patients at 1.5T — applicability to chronic stroke
    is approximate.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results page 11–12 (narrative); Table 3 (page 24); Methods 2.3
      (page 7); Methods 2.2 (page 6–7)
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2018 — both papers from the same University
      of South Carolina aphasia registry / lab (Fridriksson + Rorden); the Yourganov
      2015 cohort (n=98, 2007–2014 enrolment) is plausibly a subset of the Fridriksson
      2018 cohort (n=132); flag for downstream double-counting risk in interpret_overlap().
  source_passages:
  - section: Results
    page: 12
    supports: claim
    quote: Broca's aphasia is strongly associated with damage to pars opercularis
      of the inferior frontal gyrus, corresponding to Brodmann area 44 and generally
      considered a part of Broca's area. Its posterior neighbour, rolandic operculum,
      also has high predictive relevance. The most relevant white-matter tract is
      the arcuate fasciculus, particularly the long and anterior segments.
  - section: Methods 2.1 — Participants
    page: 6
    supports: sample
    quote: 'Of the 98 participants whose data constituted the final study sample,
      5 aphasia types were observed: Anomic aphasia: 35 patients; Broca''s aphasia:
      33 patients; Wernicke''s aphasia: 7 patients; conduction aphasia: 13 patients;
      global aphasia: 10 patients.'
  - section: Methods 2.1 — Participants
    page: 6
    supports: sample
    quote: All patients were at least 6 months post-stroke, and the mean time since
      stroke onset was 40.1 months (SD= 49.6; range = 6–276).
  - section: Methods 2.4 — Classification
    page: 8
    supports: method
    quote: Support vector machines (SVMs) were used to predict the aphasia type from
      brain damage.
  - section: Methods 2.2 — MRI data collection and preprocessing
    page: 6
    supports: imaging_details
    quote: Images were acquired on a Siemens Trio 3T scanner equipped with a 12-element
      head coil located at the University of South Carolina. These images utilized
      a T1-weighted MP-RAGE sequence with 1 mm isotropic voxels, a 256×256 matrix
      size, and a 9-degree flip angle.
  - section: Methods 2.3 — Segmentation
    page: 7
    supports: region_definition
    quote: 'To segment the brain and compute the damage to each brain area, we used
      five different atlases: Speculative Brodmann atlas; […] AAL atlas: 116 grey-matter
      areas (Tzourio-Mazoyer et al., 2001); An atlas of white-matter tracts (Catani
      & Thiebaut de Schotten, 2008) […]; A union of AAL and CTS atlases (AALCTS);
      150 areas.'
  - section: Methods 2.6 — Evaluation of significance
    page: 9
    supports: statistics
    quote: False discovery rate (Genovese et al., 2002) was used to correct for multiple
      comparisons.
  - section: Discussion
    page: 12
    supports: limitation
    quote: the classification accuracy for the pairing of the two non-fluent aphasia
      types (global versus Broca's aphasia) was at chance level. This poor result
      could be driven by the similarity in the patterns of brain damage in non-fluent
      aphasia.
- id: f2
  target: left_long_segment_arcuate_fasciculus
  target_kind: region
  claim: Damage to the long segment of the left arcuate fasciculus is among the strongest
    predictors of Broca's aphasia (predictive relevance Z = 2.85).
  direction: likely
  relationship: causal
  citation: '@Yourganov2015Predicting'
  method: MLPA
  design: cross-sectional
  imaging: T1
  sample:
    n: 98
    population: chronic left-hemisphere stroke patients with aphasia
    time_post_onset: '>=6 months post-stroke (mean 40.1 months)'
    age_range: mean 58 years (SD 11.9)
    handedness: all right-handed
    language: English
  statistics:
    threshold: binomial test, FDR-corrected
    effect_size: predictive relevance Z = 2.85 (Table 3)
  confounders_controlled:
  - balanced training via resampling
  - 8-fold CV for SVM hyperparameters
  confounders_not_controlled:
  - lesion volume
  - age / time post-stroke
  region_definition:
    kind: tract
    atlas: Catani–Thiebaut de Schotten 2008 (CTS); arcuate split into long, anterior,
      and posterior segments
    description: Long segment of the arcuate fasciculus — the direct fronto-temporal
      connection in the dual-pathway model.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM12); lesion binarized
      at 50% post-warp
    reference_space: MNI152
    atlases_used:
    - CTS
    - AALCTS
  replications:
  - '@Marchina2011'
  contradictions: []
  author_limitations:
  - CTS atlas built from 12 healthy patients at 1.5T.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 3 (Broca's column); Results page 12
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream
      double-counting risk in interpret_overlap().
  source_passages:
  - section: Results
    page: 12
    supports: claim
    quote: The most relevant white-matter tract is the arcuate fasciculus, particularly
      the long and anterior segments.
  - section: Methods 2.3 — Segmentation
    page: 7
    supports: region_definition
    quote: An atlas of white-matter tracts (Catani & Thiebaut de Schotten, 2008),
      which we refer to as CTS (Catani - Thiebaut de Schotten) atlas for the sake
      of brevity; 34 areas
  - section: Methods 2.6
    page: 9
    supports: statistics
    quote: False discovery rate (Genovese et al., 2002) was used to correct for multiple
      comparisons.
  - section: Methods 2.1 — Participants
    page: 6
    supports: sample
    quote: Of the 98 participants whose data constituted the final study sample, 5
      aphasia types were observed
  - section: Methods 2.4
    page: 8
    supports: method
    quote: Support vector machines (SVMs) were used to predict the aphasia type from
      brain damage.
  - section: Methods 2.2
    page: 6
    supports: imaging_details
    quote: Images were acquired on a Siemens Trio 3T scanner equipped with a 12-element
      head coil located at the University of South Carolina.
  - section: Discussion
    page: 13
    supports: limitation
    quote: 'the differences in classification accuracy between atlases were not significant
      (Friedman test for column effects: p = 0.355; Wilcoxon signed-rank test between
      CTS and AALCTS atlases: p = 0.106).'
- id: f3
  target: ho-cort_44
  target_kind: region
  claim: Damage to the left inferior frontal gyrus pars opercularis (Brodmann area
    44) is a strong predictor of Broca's aphasia (predictive relevance Z = 2.45).
  direction: likely
  relationship: causal
  citation: '@Yourganov2015Predicting'
  method: MLPA
  design: cross-sectional
  imaging: T1
  sample:
    n: 98
    population: chronic left-hemisphere stroke patients with aphasia
    time_post_onset: '>=6 months post-stroke (mean 40.1 months)'
    age_range: mean 58 years (SD 11.9)
    handedness: all right-handed
    language: English
  statistics:
    threshold: binomial test, FDR-corrected
    effect_size: predictive relevance Z = 2.45 (Table 3)
  confounders_controlled:
  - balanced training via resampling
  - 8-fold CV
  confounders_not_controlled:
  - lesion volume
  - age / time post-stroke
  region_definition:
    kind: atlas
    atlas: AALCTS (AAL grey-matter component); HarvardOxford-cort-maxprob-thr25-2mm
      index 44 in the canonical KB
    description: Left IFG pars opercularis as defined by AAL; corresponds to the canonical
      KB's `ho-cort_44` (HarvardOxford index 44).
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM12)
    reference_space: MNI152
    atlases_used:
    - AAL
    - AALCTS
  replications:
  - '@Mirman2015'
  - '@Fridriksson2018'
  contradictions: []
  author_limitations:
  - Damage limited to Broca's area alone does not produce Broca's aphasia (Damasio
    1992; Fridriksson 2014); the finding is one component of a multivariate signature.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 3 (Broca's); Discussion page 12
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream
      double-counting risk in interpret_overlap().
    - target uses legacy id `ho-cort_44` rather than the new `left_ifg_pars_opercularis`
      because the canonical entry already exists at `regions/ho-cort_44.md`.
  source_passages:
  - section: Results
    page: 12
    supports: claim
    quote: Broca's aphasia is strongly associated with damage to pars opercularis
      of the inferior frontal gyrus, corresponding to Brodmann area 44 and generally
      considered a part of Broca's area.
  - section: Methods 2.1 — Participants
    page: 6
    supports: sample
    quote: Of the 98 participants whose data constituted the final study sample, 5
      aphasia types were observed
  - section: Methods 2.4
    page: 8
    supports: method
    quote: Support vector machines (SVMs) were used to predict the aphasia type from
      brain damage.
  - section: Methods 2.2
    page: 6
    supports: imaging_details
    quote: Images were acquired on a Siemens Trio 3T scanner equipped with a 12-element
      head coil located at the University of South Carolina.
  - section: Methods 2.6
    page: 9
    supports: statistics
    quote: False discovery rate (Genovese et al., 2002) was used to correct for multiple
      comparisons.
  - section: Discussion
    page: 12
    supports: limitation
    quote: Damage to these areas has previously been reported as critical lesion locations
      associated with Broca's aphasia; moreover, Broca's aphasia is not present when
      damage is limited to Broca's area or to the basal ganglia (Damasio, 1992; Alexander
      et al., 1987, Mohr et al., 1978).
- id: f4
  target: left_rolandic_operculum
  target_kind: region
  claim: Damage to the left rolandic operculum (the cortex superior and posterior
    to pars opercularis) is a strong predictor of Broca's aphasia (predictive relevance
    Z = 2.2).
  direction: likely
  relationship: causal
  citation: '@Yourganov2015Predicting'
  method: MLPA
  design: cross-sectional
  imaging: T1
  sample:
    n: 98
    population: chronic left-hemisphere stroke patients with aphasia
    time_post_onset: '>=6 months post-stroke (mean 40.1 months)'
    age_range: mean 58 years (SD 11.9)
    handedness: all right-handed
    language: English
  statistics:
    threshold: binomial test, FDR-corrected
    effect_size: predictive relevance Z = 2.2 (Table 3)
  confounders_controlled:
  - balanced training via resampling
  - 8-fold CV
  confounders_not_controlled:
  - lesion volume
  - age / time post-stroke
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left rolandic operculum as defined by AAL — the cortex along the
      central sulcus at the level of the operculum, posterior neighbour of pars opercularis.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM12)
    reference_space: MNI152
    atlases_used:
    - AAL
    - AALCTS
  replications: []
  contradictions: []
  author_limitations:
  - Atlas-based parcellation has lower spatial resolution than voxel-wise approaches.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 3; Results page 12
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream
      double-counting risk in interpret_overlap().
  source_passages:
  - section: Results
    page: 12
    supports: claim
    quote: Its posterior neighbour, rolandic operculum, also has high predictive relevance.
  - section: Methods 2.1 — Participants
    page: 6
    supports: sample
    quote: Of the 98 participants whose data constituted the final study sample, 5
      aphasia types were observed
  - section: Methods 2.4
    page: 8
    supports: method
    quote: Support vector machines (SVMs) were used to predict the aphasia type from
      brain damage.
  - section: Methods 2.2
    page: 6
    supports: imaging_details
    quote: Images were acquired on a Siemens Trio 3T scanner equipped with a 12-element
      head coil located at the University of South Carolina.
  - section: Methods 2.6
    page: 9
    supports: statistics
    quote: False discovery rate (Genovese et al., 2002) was used to correct for multiple
      comparisons.
- id: f5
  target: left_superior_temporal_gyrus
  target_kind: region
  claim: Damage to the left superior temporal gyrus contributes to Broca's aphasia
    classification in this multivariate model (predictive relevance Z = 1.99) — consistent
    with the view that classical Broca's requires damage extending into Wernicke's-area
    territory.
  direction: likely
  relationship: causal
  citation: '@Yourganov2015Predicting'
  method: MLPA
  design: cross-sectional
  imaging: T1
  sample:
    n: 98
    population: chronic left-hemisphere stroke patients with aphasia
    time_post_onset: '>=6 months post-stroke (mean 40.1 months)'
    age_range: mean 58 years (SD 11.9)
    handedness: all right-handed
    language: English
  statistics:
    threshold: binomial test, FDR-corrected
    effect_size: predictive relevance Z = 1.99 (Table 3)
  confounders_controlled:
  - balanced training via resampling
  confounders_not_controlled:
  - lesion volume
  - age / time post-stroke
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left superior temporal gyrus as defined by AAL.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM12)
    reference_space: MNI152
    atlases_used:
    - AAL
    - AALCTS
  replications:
  - '@Fridriksson2018'
  contradictions: []
  author_limitations:
  - STG is also predictive of Wernicke's and global aphasia — finding is non-specific
    to Broca's.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 3
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream
      double-counting risk in interpret_overlap().
  source_passages:
  - section: Discussion
    page: 12
    supports: claim
    quote: we found that damage to supramarginal and Heschl's gyri predicts Broca's
      aphasia, consistent with Fridriksson et al. (2014).
  - section: Methods 2.1 — Participants
    page: 6
    supports: sample
    quote: Of the 98 participants whose data constituted the final study sample, 5
      aphasia types were observed
  - section: Methods 2.4
    page: 8
    supports: method
    quote: Support vector machines (SVMs) were used to predict the aphasia type from
      brain damage.
  - section: Methods 2.2
    page: 6
    supports: imaging_details
    quote: Images were acquired on a Siemens Trio 3T scanner equipped with a 12-element
      head coil located at the University of South Carolina.
  - section: Methods 2.6
    page: 9
    supports: statistics
    quote: False discovery rate (Genovese et al., 2002) was used to correct for multiple
      comparisons.
- id: f6
  target: left_supramarginal_gyrus
  target_kind: region
  claim: Damage to the left supramarginal gyrus contributes to Broca's aphasia classification
    (predictive relevance Z = 1.66).
  direction: likely
  relationship: causal
  citation: '@Yourganov2015Predicting'
  method: MLPA
  design: cross-sectional
  imaging: T1
  sample:
    n: 98
    population: chronic left-hemisphere stroke patients with aphasia
    time_post_onset: '>=6 months post-stroke (mean 40.1 months)'
    age_range: mean 58 years (SD 11.9)
    handedness: all right-handed
    language: English
  statistics:
    threshold: binomial test, FDR-corrected
    effect_size: predictive relevance Z = 1.66 (Table 3)
  confounders_controlled:
  - balanced training via resampling
  confounders_not_controlled:
  - lesion volume
  - age / time post-stroke
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left supramarginal gyrus (combined; the AAL parcellation does not
      split anterior/posterior subdivisions).
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM12)
    reference_space: MNI152
    atlases_used:
    - AAL
    - AALCTS
  replications:
  - '@Fridriksson2018'
  contradictions: []
  author_limitations:
  - Discussion notes that this finding is consistent with Fridriksson et al. (2014),
    who reported that classical Broca's aphasia requires damage extending into Wernicke's-area
    territory.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 3; Discussion page 12
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream
      double-counting risk in interpret_overlap().
  source_passages:
  - section: Discussion
    page: 12
    supports: claim
    quote: we found that damage to supramarginal and Heschl's gyri predicts Broca's
      aphasia, consistent with Fridriksson et al. (2014).
  - section: Methods 2.1 — Participants
    page: 6
    supports: sample
    quote: Of the 98 participants whose data constituted the final study sample, 5
      aphasia types were observed
  - section: Methods 2.4
    page: 8
    supports: method
    quote: Support vector machines (SVMs) were used to predict the aphasia type from
      brain damage.
  - section: Methods 2.2
    page: 6
    supports: imaging_details
    quote: Images were acquired on a Siemens Trio 3T scanner equipped with a 12-element
      head coil located at the University of South Carolina.
  - section: Methods 2.6
    page: 9
    supports: statistics
    quote: False discovery rate (Genovese et al., 2002) was used to correct for multiple
      comparisons.
- id: f7
  target: left_heschls_gyrus
  target_kind: region
  claim: Damage to the left Heschl's gyrus contributes to Broca's aphasia classification
    (predictive relevance Z = 1.35).
  direction: likely
  relationship: causal
  citation: '@Yourganov2015Predicting'
  method: MLPA
  design: cross-sectional
  imaging: T1
  sample:
    n: 98
    population: chronic left-hemisphere stroke patients with aphasia
    time_post_onset: '>=6 months post-stroke (mean 40.1 months)'
    age_range: mean 58 years (SD 11.9)
    handedness: all right-handed
    language: English
  statistics:
    threshold: binomial test, FDR-corrected
    effect_size: predictive relevance Z = 1.35 (Table 3)
  confounders_controlled:
  - balanced training via resampling
  confounders_not_controlled:
  - lesion volume
  - age / time post-stroke
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left Heschl's gyrus (transverse temporal gyrus; primary auditory
      cortex).
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM12)
    reference_space: MNI152
    atlases_used:
    - AAL
    - AALCTS
  replications:
  - '@Fridriksson2018'
  contradictions: []
  author_limitations:
  - Heschl's gyrus is also predictive of Wernicke's, conduction, and global aphasia
    — finding is non-specific to Broca's.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 3
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream
      double-counting risk in interpret_overlap().
  source_passages:
  - section: Discussion
    page: 12
    supports: claim
    quote: we found that damage to supramarginal and Heschl's gyri predicts Broca's
      aphasia, consistent with Fridriksson et al. (2014).
  - section: Methods 2.1 — Participants
    page: 6
    supports: sample
    quote: Of the 98 participants whose data constituted the final study sample, 5
      aphasia types were observed
  - section: Methods 2.4
    page: 8
    supports: method
    quote: Support vector machines (SVMs) were used to predict the aphasia type from
      brain damage.
  - section: Methods 2.2
    page: 6
    supports: imaging_details
    quote: Images were acquired on a Siemens Trio 3T scanner equipped with a 12-element
      head coil located at the University of South Carolina.
  - section: Methods 2.6
    page: 9
    supports: statistics
    quote: False discovery rate (Genovese et al., 2002) was used to correct for multiple
      comparisons.
source: agent_draft
last_reviewed: null
notes: 'Re-extraction draft from Yourganov 2015 (predictive relevance > 1

  thresholds in Table 3). Seven findings recorded, covering all eight

  regions in Table 3''s Broca''s column except the "arcuate (combined)"

  entry (Z = 1.91) — that entry is a redundant aggregation of the

  anterior + long + posterior segments which are recorded as

  individual findings (f1 anterior, f2 long; the posterior segment

  appears in conduction_aphasia rather than Broca''s).


  Per the multi-paper consolidation rule (schema.md), the canonical

  `ho-cort_44.md` already carries a Fridriksson 2018 finding (`f1`).

  When promote.py runs, this draft''s f3 (the Yourganov IFG-pars-

  opercularis finding) gets appended to that file as `f2` (or whatever

  the next available id is). The cohort-overlap flag on f3 makes the

  shared-cohort relationship explicit so interpret_overlap() doesn''t

  double-count.


  Anchored on impairment because the paper is a multi-class syndrome-

  classification study; per-region claims are most naturally

  organized by syndrome label.'
reviewer: auto-reviewer
reviewed_on: '2026-05-05'
---
# Broca's aphasia

## Clinical definition

Broca's aphasia is a non-fluent aphasia syndrome characterized by
effortful, halting speech production, agrammatism, relatively
preserved single-word auditory comprehension, and impaired
repetition. Classically associated with damage to left posterior
inferior frontal cortex (Broca's area, BA 44/45) and the underlying
white matter, though modern lesion-symptom evidence shows damage
typically extends well beyond classical Broca's area.

## Lesion correlates (per Yourganov 2015)

Multivariate SVM classification of 98 chronic stroke patients across
five aphasia types identifies the following regions as most
predictive of Broca's aphasia, ranked by predictive relevance
(weighted Z-score across pairwise classifications):

  - Anterior segment of arcuate fasciculus (Z = 3.2) — f1
  - Long segment of arcuate fasciculus (Z = 2.85) — f2
  - IFG pars opercularis / `ho-cort_44` (Z = 2.45) — f3
  - Rolandic operculum (Z = 2.2) — f4
  - Superior temporal gyrus (Z = 1.99) — f5
  - Arcuate fasciculus (combined; Z = 1.91) — covered by f1 + f2
  - Supramarginal gyrus (Z = 1.66) — f6
  - Heschl's gyrus (Z = 1.35) — f7

The Discussion (page 12) notes that damage limited to Broca's area
alone does NOT produce Broca's aphasia (Damasio 1992; Alexander 1987;
Mohr 1978; Fridriksson 2014); the syndrome requires a multivariate
signature of damage spanning the IFG, adjacent motor cortex, the
arcuate fasciculus, and (often) extending to STG / SMG / Heschl's.

## Important caveat: Broca's vs global at chance

Broca's vs global aphasia could not be classified above chance with
any atlas (Table 1). The Discussion attributes this to lesion-pattern
similarity between the two non-fluent syndromes and notes that global
aphasia often resolves to Broca's during recovery (Pedersen 2003).
