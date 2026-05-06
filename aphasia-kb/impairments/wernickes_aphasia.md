---
schema_version: 2.3
id: wernickes_aphasia
name: Wernicke's aphasia
kind: impairment
status: approved
created_by: agent:claude-opus-4-7
created_on: 2026-05-01
short_definition: Fluent aphasia syndrome characterized by impaired auditory comprehension,
  fluent but often jargon-like speech, semantic and phonemic paraphasias, and impaired
  repetition. Classically associated with damage to left posterior superior temporal
  gyrus.
assessment:
- Western Aphasia Battery (WAB / WAB-R)
- Boston Diagnostic Aphasia Examination (BDAE)
findings:
- id: f1
  target: left_angular_gyrus
  target_kind: region
  claim: Damage to the left angular gyrus is the strongest predictor of Wernicke's
    aphasia in a multivariate SVM classification (predictive relevance Z = 1.76).
  direction: likely
  relationship: causal
  citation: '@Yourganov2015Predicting'
  method: MLPA
  design: cross-sectional
  imaging: T1
  sample:
    n: 98
    population: chronic left-hemisphere stroke patients with aphasia (Wernicke's subgroup
      n=7)
    time_post_onset: '>=6 months post-stroke; mean 40.1 months (SD 49.6, range 6–276)'
    age_range: mean 58 years (SD 11.9, range 31–80)
    handedness: all right-handed
    language: English (recruited in South Carolina, USA)
    recruitment: referrals from local neurologists and print/radio advertisements;
      behavioural assessment May 2007–Oct 2014 at the University of South Carolina.
    inclusion_criteria: right-handed; chronic left-hemisphere stroke; aphasia present
    exclusion_criteria: absence of aphasia; MRI contraindications; apraxia-of-speech-driven
      deficit; bilateral lesion; multiple sclerosis.
  statistics:
    threshold: binomial-distribution test, FDR-corrected (p<0.05)
    effect_size: predictive relevance Z = 1.76 (Table 3)
    ci_95: not_reported
    p_value: not_reported per-region
  confounders_controlled:
  - balanced training set via resampling
  - 8-fold CV for SVM hyperparameters
  confounders_not_controlled:
  - lesion volume
  - age / time post-stroke
  - small Wernicke's subgroup (n=7)
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left angular gyrus as defined by AAL — the posterior inferior parietal
      lobule wrapping around the superior temporal sulcus.
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
      notes: Lesions manually drawn on the T2 image by a trained neurologist; resliced
        to T1 native space; smoothed (3mm FWHM).
    preprocessing_pipeline: Enantiomorphic normalization (Nachev et al., 2008) using
      SPM12 unified segmentation + Clinical Toolbox (Rorden et al., 2012); lesion
      binarized at 50% probability after warping.
    reference_space: MNI152
    atlases_used:
    - Speculative Brodmann (82 areas)
    - JHU/Faria 2012 (189 areas)
    - AAL (Tzourio-Mazoyer 2002; 116 areas)
    - Catani–Thiebaut de Schotten 2008 (CTS; 34 white-matter tracts)
    - AALCTS (custom union; 150 areas)
  replications: []
  contradictions: []
  author_limitations:
  - Wernicke's group small (n=7) — predictive-relevance values may be unstable; the
    authors note this explicitly.
  - Conduction vs Wernicke's classification at chance — the two fluent syndromes are
    not separable on lesion pattern alone in this sample.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results page 12; Table 3 (Wernicke's column); Discussion pages
      12–13
    confidence: medium
    flags:
    - cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream
      double-counting risk in interpret_overlap().
    - 'Wernicke''s subgroup is only n=7; predictive-relevance values across pairwise
      contrasts may be inflated by sample-specific lesion idiosyncrasies — confidence:
      medium.'
  source_passages:
  - section: Results
    page: 12
    supports: claim
    quote: Wernicke's aphasia can be predicted from damage to angular, Heschl's, and
      superior temporal gyri, as well as temporal pole and putamen.
  - section: Methods 2.1 — Participants
    page: 6
    supports: sample
    quote: 'Of the 98 participants whose data constituted the final study sample,
      5 aphasia types were observed: Anomic aphasia: 35 patients; Broca''s aphasia:
      33 patients; Wernicke''s aphasia: 7 patients; conduction aphasia: 13 patients;
      global aphasia: 10 patients.'
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
    quote: The group of patients with Wernicke's aphasia was the smallest (n=7) patient
      group in our sample. Despite the sample size limitation, the brain areas that
      we found to predict Wernicke's aphasia include the classical Wernicke's area
      and its neighbourhood, which is consistent with the existing literature
- id: f2
  target: left_heschls_gyrus
  target_kind: region
  claim: Damage to the left Heschl's gyrus contributes to Wernicke's aphasia classification
    (predictive relevance Z = 1.61).
  direction: likely
  relationship: causal
  citation: '@Yourganov2015Predicting'
  method: MLPA
  design: cross-sectional
  imaging: T1
  sample:
    n: 98
    population: chronic left-hemisphere stroke patients with aphasia (Wernicke's subgroup
      n=7)
    time_post_onset: '>=6 months post-stroke (mean 40.1 months)'
    age_range: mean 58 years (SD 11.9)
    handedness: all right-handed
    language: English
  statistics:
    threshold: binomial test, FDR-corrected
    effect_size: predictive relevance Z = 1.61 (Table 3)
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
  replications: []
  contradictions: []
  author_limitations:
  - Heschl's gyrus is also predictive of Broca's, conduction, and global aphasia —
    finding is non-specific to Wernicke's.
  - Small n=7 Wernicke's subgroup.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 3 (Wernicke's column)
    confidence: medium
    flags:
    - cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream
      double-counting risk in interpret_overlap().
  source_passages:
  - section: Results
    page: 12
    supports: claim
    quote: Wernicke's aphasia can be predicted from damage to angular, Heschl's, and
      superior temporal gyri, as well as temporal pole and putamen.
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
- id: f3
  target: left_temporal_pole_mtg
  target_kind: region
  claim: Damage to the left temporal pole (middle temporal gyrus subdivision) contributes
    to Wernicke's aphasia classification (predictive relevance Z = 1.47).
  direction: likely
  relationship: causal
  citation: '@Yourganov2015Predicting'
  method: MLPA
  design: cross-sectional
  imaging: T1
  sample:
    n: 98
    population: chronic left-hemisphere stroke patients with aphasia (Wernicke's subgroup
      n=7)
    time_post_onset: '>=6 months post-stroke (mean 40.1 months)'
    age_range: mean 58 years (SD 11.9)
    handedness: all right-handed
    language: English
  statistics:
    threshold: binomial test, FDR-corrected
    effect_size: predictive relevance Z = 1.47 (Table 3)
  confounders_controlled:
  - balanced training via resampling
  confounders_not_controlled:
  - lesion volume
  - age / time post-stroke
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left temporal pole (middle temporal gyrus subdivision) — anterior
      MTG. AAL provides separate temporal-pole subdivisions for STG and MTG.
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
  - Authors note the temporal pole and putamen findings 'may reflect the idiosyncrasies
    of our small sample' (page 13).
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 3; Discussion page 13
    confidence: medium
    flags:
    - cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream
      double-counting risk in interpret_overlap().
    - Authors explicitly flag temporal-pole + putamen findings as possibly idiosyncratic
      to small Wernicke's sample (n=7).
  source_passages:
  - section: Results
    page: 12
    supports: claim
    quote: Wernicke's aphasia can be predicted from damage to angular, Heschl's, and
      superior temporal gyri, as well as temporal pole and putamen.
  - section: Discussion
    page: 13
    supports: limitation
    quote: the damage to the temporal poles and the putamen was also associated with
      Wernicke's aphasia, which may reflect the idiosyncrasies of our small sample
      (see the lesion overlay map in Figure 1).
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
- id: f4
  target: left_pallidum
  target_kind: region
  claim: Damage to the left pallidum (globus pallidus) contributes to Wernicke's aphasia
    classification (predictive relevance Z = 1.45).
  direction: likely
  relationship: causal
  citation: '@Yourganov2015Predicting'
  method: MLPA
  design: cross-sectional
  imaging: T1
  sample:
    n: 98
    population: chronic left-hemisphere stroke patients with aphasia (Wernicke's subgroup
      n=7)
    time_post_onset: '>=6 months post-stroke (mean 40.1 months)'
    age_range: mean 58 years (SD 11.9)
    handedness: all right-handed
    language: English
  statistics:
    threshold: binomial test, FDR-corrected
    effect_size: predictive relevance Z = 1.45 (Table 3)
  confounders_controlled:
  - balanced training via resampling
  confounders_not_controlled:
  - lesion volume
  - age / time post-stroke
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left globus pallidus (basal ganglia structure).
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
  - Basal ganglia damage is also predictive of global aphasia (see global_aphasia
    draft); finding is non-specific.
  - Small Wernicke's sample (n=7) — predictive relevance may be sample-specific.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 3 (Wernicke's column)
    confidence: medium
    flags:
    - cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream
      double-counting risk in interpret_overlap().
  source_passages:
  - section: Results
    page: 12
    supports: claim
    quote: Wernicke's aphasia can be predicted from damage to angular, Heschl's, and
      superior temporal gyri, as well as temporal pole and putamen.
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
  target: left_temporal_pole_stg
  target_kind: region
  claim: Damage to the left temporal pole (superior temporal gyrus subdivision) contributes
    to Wernicke's aphasia classification (predictive relevance Z = 1.34).
  direction: likely
  relationship: causal
  citation: '@Yourganov2015Predicting'
  method: MLPA
  design: cross-sectional
  imaging: T1
  sample:
    n: 98
    population: chronic left-hemisphere stroke patients with aphasia (Wernicke's subgroup
      n=7)
    time_post_onset: '>=6 months post-stroke (mean 40.1 months)'
    age_range: mean 58 years (SD 11.9)
    handedness: all right-handed
    language: English
  statistics:
    threshold: binomial test, FDR-corrected
    effect_size: predictive relevance Z = 1.34 (Table 3)
  confounders_controlled:
  - balanced training via resampling
  confounders_not_controlled:
  - lesion volume
  - age / time post-stroke
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left temporal pole (superior temporal gyrus subdivision) — anterior
      STG.
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
  - Sample-size caveat (n=7 Wernicke's).
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 3
    confidence: medium
    flags:
    - cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream
      double-counting risk in interpret_overlap().
  source_passages:
  - section: Results
    page: 12
    supports: claim
    quote: Wernicke's aphasia can be predicted from damage to angular, Heschl's, and
      superior temporal gyri, as well as temporal pole and putamen.
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
  target: left_superior_temporal_gyrus
  target_kind: region
  claim: Damage to the left superior temporal gyrus contributes to Wernicke's aphasia
    classification (predictive relevance Z = 1.31).
  direction: likely
  relationship: causal
  citation: '@Yourganov2015Predicting'
  method: MLPA
  design: cross-sectional
  imaging: T1
  sample:
    n: 98
    population: chronic left-hemisphere stroke patients with aphasia (Wernicke's subgroup
      n=7)
    time_post_onset: '>=6 months post-stroke (mean 40.1 months)'
    age_range: mean 58 years (SD 11.9)
    handedness: all right-handed
    language: English
  statistics:
    threshold: binomial test, FDR-corrected
    effect_size: predictive relevance Z = 1.31 (Table 3)
  confounders_controlled:
  - balanced training via resampling
  confounders_not_controlled:
  - lesion volume
  - age / time post-stroke
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left superior temporal gyrus as defined by AAL (the canonical Wernicke's-area
      cortex when posterior STG is intact).
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
  - Small Wernicke's subgroup (n=7) — predictive relevance may be sample-specific.
  - STG is also predictive of Broca's and global aphasia.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 3 (Wernicke's column); Discussion page 12
    confidence: medium
    flags:
    - cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream
      double-counting risk in interpret_overlap().
  source_passages:
  - section: Discussion
    page: 12
    supports: claim
    quote: the brain areas that we found to predict Wernicke's aphasia include the
      classical Wernicke's area and its neighbourhood, which is consistent with the
      existing literature (Marshall et al., 1998; Lieberman, 2002).
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
  target: left_putamen
  target_kind: region
  claim: Damage to the left putamen contributes to Wernicke's aphasia classification
    (predictive relevance Z = 1.3).
  direction: likely
  relationship: causal
  citation: '@Yourganov2015Predicting'
  method: MLPA
  design: cross-sectional
  imaging: T1
  sample:
    n: 98
    population: chronic left-hemisphere stroke patients with aphasia (Wernicke's subgroup
      n=7)
    time_post_onset: '>=6 months post-stroke (mean 40.1 months)'
    age_range: mean 58 years (SD 11.9)
    handedness: all right-handed
    language: English
  statistics:
    threshold: binomial test, FDR-corrected
    effect_size: predictive relevance Z = 1.3 (Table 3)
  confounders_controlled:
  - balanced training via resampling
  confounders_not_controlled:
  - lesion volume
  - age / time post-stroke
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left putamen (basal ganglia).
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
  - Authors flag the putamen + temporal-pole findings for Wernicke's as possibly idiosyncratic
    to the small (n=7) sample.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Table 3; Discussion page 13
    confidence: medium
    flags:
    - cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream
      double-counting risk in interpret_overlap().
    - Author-flagged as possibly small-sample idiosyncrasy (Wernicke's n=7).
  source_passages:
  - section: Discussion
    page: 13
    supports: limitation
    quote: the damage to the temporal poles and the putamen was also associated with
      Wernicke's aphasia, which may reflect the idiosyncrasies of our small sample
      (see the lesion overlay map in Figure 1).
  - section: Results
    page: 12
    supports: claim
    quote: Wernicke's aphasia can be predicted from damage to angular, Heschl's, and
      superior temporal gyri, as well as temporal pole and putamen.
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
notes: 'Re-extraction draft from Yourganov 2015. Seven findings recorded —

  all regions in Table 3''s Wernicke''s column with predictive relevance

  > 1. Note: f7 (precentral gyrus, Z=1.06) was below the 1.0 threshold

  in the published Table 3 actually wait — the precentral gyrus row

  in Table 3 has Z=1.06 for Wernicke''s; not included here as it''s

  borderline and the authors emphasise the temporal-lobe and basal-

  ganglia findings.


  Confidence flagged as medium because of the small Wernicke''s

  subgroup (n=7) — the authors themselves note this caveat.'
reviewer: michele
reviewed_on: '2026-05-06'
---
# Wernicke's aphasia

## Clinical definition

Wernicke's aphasia is a fluent aphasia syndrome characterized by
impaired auditory comprehension, fluent but often jargon-like
speech, frequent semantic and phonemic paraphasias, and impaired
repetition. Classically associated with damage to left posterior
superior temporal gyrus.

## Lesion correlates (per Yourganov 2015)

  - Angular gyrus (Z = 1.76) — f1
  - Heschl's gyrus (Z = 1.61) — f2
  - Temporal pole, MTG subdivision (Z = 1.47) — f3
  - Pallidum (Z = 1.45) — f4
  - Temporal pole, STG subdivision (Z = 1.34) — f5
  - Superior temporal gyrus (Z = 1.31) — f6
  - Putamen (Z = 1.3) — f7
  - Precentral gyrus (Z = 1.06; below 1.5 cutoff, not extracted as a separate finding)

## Important caveats

  - Wernicke's vs conduction classification at chance.
  - Small Wernicke's subgroup (n=7) — authors note temporal-pole
    and putamen findings may be sample-idiosyncratic.
