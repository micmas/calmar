---
schema_version: 2.3
id: syntactic_processing
name: Syntactic Processing Deficits in Aphasia
kind: classical
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
hemisphere: left
aliases:
- agrammatism
- syntactic processing
- morphosyntactic production
- sentence comprehension
notes: 'den Ouden et al. 2019 (HBM), USC/MUSC cohort (n=71 stroke survivors, n=68
  in LSM).

  Overlaps with @Fridriksson2018, @Yourganov2015Predicting, @Basilakos2015 (same lab
  group,

  likely shared participants from USC/MUSC stroke cohort).

  COHORT_OVERLAP_FLAG: USC/MUSC lab; check for participant overlap with other USC
  papers.

  Paper uses NAVS (Northwestern Assessment of Verbs and Sentences) as primary outcome.

  Both VLSM (gray matter) and CLSM (connectome, DTI-based structural connectivity)
  applied.

  17-node JHU-atlas perisylvian network analyzed in CLSM.

  Lesion size regressed out in primary VLSM analyses; CLSM results based on raw scores.

  '
findings:
- id: f1
  target: morphosyntactic_production_deficit
  target_kind: impairment
  claim: Lesions to the left IFG pars triangularis (BA 45) predict morphosyntactically
    reduced speech output (agrammatic production) after left-hemisphere stroke.
  direction: likely
  relationship: causal
  citation: '@DenOuden2019'
  method: VLSM
  design: cross-sectional
  imaging: structural_MRI
  sample:
    n: 68
    population: chronic left-hemisphere ischemic stroke survivors with and without
      aphasia
    time_post_onset: mean 52.8 months (SD 52.5, range 8-290 months)
    age_range: mean 59.6 years (SD 10.1, range 37-80)
    handedness: all right-handed
    language: English (native speakers)
    recruitment: USC and MUSC stroke cohort
    inclusion_criteria: Right-handed; native English speakers; left-hemisphere ischemic
      stroke; no premorbid neurological or psychiatric disorder.
    exclusion_criteria: Right-hemisphere lesion; cerebellar-only lesion; CT scan only
      (no MRI); excluded 3 participants from LSM for these reasons.
  statistics:
    threshold: p<0.05 permutation-corrected (5000 permutations, one-tailed)
    cluster_extent: voxels with at least 6 participants having lesions
    effect_size: not_reported
    ci_95: not_reported
    p_value: corrected alpha=0.05
  confounders_controlled:
  - Overall lesion size regressed out (binary logistic regression before VLSM)
  - Permutation testing for multiple comparisons
  confounders_not_controlled:
  - Time post-onset
  - Age
  - Education
  - Aphasia type
  - Cohort overlap with other USC/MUSC papers
  region_definition:
    kind: data_driven_cluster
    atlas: NiiStat VLSM output; anatomy confirmed with Catani-Thiebaut de Schotten
      (2008) tractography atlas
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - JHU atlas (Faria et al., 2012; Mori et al., 2008)
    - Catani-Thiebaut de Schotten (2008) tractography atlas
    modalities:
    - modality: T1
    - modality: T2
  author_limitations:
  - Clinical agrammatism classification based on limited speech sample (Cookie-Theft
    picture description only)
  - Cross-sectional design; chronic stage only; compensatory strategies cannot be
    assessed
  - SPPT noncanonical measure showed counterintuitive results; may not validly capture
    noncanonical production deficit
  - Lesion size regression may introduce Type II error (conservative)
  evidence_quality: cohort
  strength: moderate
  cohort_overlap_flag: true
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Abstract; Methods – Participants; Methods – Statistical analyses;
      Discussion (section 4.2)
    confidence: high
    flags:
    - USC/MUSC cohort (n=71); overlaps with @Fridriksson2018, @Yourganov2015Predicting,
      @Basilakos2015 (same lab)
    - PD-MR classification based on single speech sample (Cookie-Theft) — limited
      ecological validity
    - CLSM results not corrected for lesion size; treated as supplementary evidence
  source_passages:
  - section: Discussion
    quote: identification of morphosyntactic production problems in descriptive speech
      was most strongly predicted by structural lesions in the triangular part of
      the IFG
    page: 17
    supports: claim
  - section: Methods – Participants
    quote: 71 right-handed native speakers of English (mean age 59.6 years, SD 10.1,
      range 37–80 years; 23 females)
    page: 4
    supports: sample
  - section: Methods – Lesion-symptom mapping
    quote: corrected for multiple comparisons through permutation testing (5,000 permutations)
    page: 8
    supports: method
  - section: Methods – Lesion-symptom mapping
    quote: regressed out overall lesion size from the binary classifications in Analysis
      1
    page: 8
    supports: method
- id: f2
  target: verb_argument_structure_production
  target_kind: impairment
  claim: Lesions to the left posterior superior temporal gyrus (pSTG) and angular
    gyrus predict impaired verb argument structure production on the NAVS ASPT-A subtest.
  direction: likely
  relationship: causal
  citation: '@DenOuden2019'
  method: VLSM
  design: cross-sectional
  imaging: structural_MRI
  sample:
    n: 68
    population: chronic left-hemisphere ischemic stroke survivors with and without
      aphasia
    time_post_onset: mean 52.8 months (SD 52.5, range 8-290 months)
    age_range: mean 59.6 years (SD 10.1, range 37-80)
    handedness: all right-handed
    language: English (native speakers)
    recruitment: USC and MUSC stroke cohort
    inclusion_criteria: Right-handed; native English speakers; left-hemisphere ischemic
      stroke; no premorbid neurological or psychiatric disorder.
    exclusion_criteria: Right-hemisphere lesion; cerebellar-only lesion; CT scan only.
  statistics:
    threshold: p<0.05 permutation-corrected (5000 permutations, one-tailed)
    cluster_extent: k=47 voxels (ASPT-A cluster includes STG BA41 + angular gyrus
      + middle occipital gyrus)
    effect_size: not_reported
    ci_95: not_reported
    p_value: corrected alpha=0.05
  confounders_controlled:
  - Overall lesion size regressed out (linear regression before VLSM)
  - Permutation testing for multiple comparisons
  confounders_not_controlled:
  - Time post-onset
  - Age
  - Lexical-semantic ability (angular gyrus region may reflect semantic event knowledge)
  - Cohort overlap with other USC/MUSC papers
  region_definition:
    kind: data_driven_cluster
    atlas: NiiStat VLSM; peak BA 41 (superior temporal gyrus), extending into angular
      gyrus and middle occipital gyrus
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - JHU atlas (Faria et al., 2012; Mori et al., 2008)
    - Catani-Thiebaut de Schotten (2008) tractography atlas
    modalities:
    - modality: T1
    - modality: T2
  author_limitations:
  - Angular gyrus finding may reflect semantic event knowledge interface rather than
    stored argument-structure representations
  - Cross-sectional; chronic stage only
  - Lesion size regression may introduce Type II error
  evidence_quality: cohort
  strength: moderate
  cohort_overlap_flag: true
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results (Table 8; section 3.4.2); Discussion (section 4.2)
    confidence: high
    flags:
    - USC/MUSC cohort; overlaps with other USC papers
    - Angular gyrus result may reflect semantic-syntactic interface rather than pure
      syntax
  source_passages:
  - section: Results – VLSM
    quote: ASPT-A scores were negatively correlated with damage to the angular gyrus,
      extending into middle occipital gyrus
    page: 12
    supports: claim
  - section: Results – Table 8
    quote: angular gyrus, middle occipital gyrus
    page: 12
    supports: statistics
  - section: Discussion
    quote: location of this region makes a lot of sense. If "syntactic processing"
      is not exclusively a function of the dorsal stream
    page: 18
    supports: claim
- id: f3
  target: sentence_comprehension_production
  target_kind: impairment
  claim: Reduced structural connectivity in a ventral pathway between left IFG and
    temporal regions (especially IFG-pars-triangularis to pSTG/MTG) predicts impaired
    noncanonical sentence production on the NAVS SPPT.
  direction: likely
  relationship: correlational
  citation: '@DenOuden2019'
  method: VLSM
  design: cross-sectional
  imaging: DTI
  sample:
    n: 68
    population: chronic left-hemisphere ischemic stroke survivors with and without
      aphasia
    time_post_onset: mean 52.8 months (SD 52.5, range 8-290 months)
    age_range: mean 59.6 years (SD 10.1, range 37-80)
    handedness: all right-handed
    language: English (native speakers)
    recruitment: USC and MUSC stroke cohort
    inclusion_criteria: Right-handed; native English speakers; left-hemisphere ischemic
      stroke.
    exclusion_criteria: Right-hemisphere lesion; cerebellar-only lesion; CT scan only.
  statistics:
    threshold: p<0.05 permutation-corrected (5000 permutations, one-tailed) — CLSM
      analyses
    cluster_extent: 15 connections predictive of SPPT noncanonical performance
    effect_size: z values reported (range ~2.6-3.2)
    ci_95: not_reported
    p_value: corrected alpha=0.05
  confounders_controlled:
  - Canonical sentence performance partialed out as nuisance regressor (Freedman-Lane
    procedure)
  - Permutation testing for multiple comparisons
  confounders_not_controlled:
  - Overall lesion size NOT regressed out in CLSM (did not survive with regression)
  - General aphasia severity may confound results
  - Cohort overlap with other USC/MUSC papers
  region_definition:
    kind: tract
    atlas: JHU atlas 17-node perisylvian network; probabilistic tractography (FSL
      FDT, 5000 pathways)
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - JHU atlas (Faria et al., 2012; Mori et al., 2008)
    modalities:
    - modality: T1
    - modality: DTI
  author_limitations:
  - CLSM results did not survive correction for overall lesion size; treated as informative
    but less reliable
  - Connectome-based LSM is relatively novel; standards for optimal lesion size correction
    not yet established
  - SPPT noncanonical measure may have validity issues (counterintuitive patient performance
    pattern noted)
  evidence_quality: cohort
  strength: weak
  cohort_overlap_flag: true
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results (section 3.4.4; Table 9); Discussion (section 4.2); Methods
      (section 2.3.3)
    confidence: medium
    flags:
    - USC/MUSC cohort; overlaps with other USC papers
    - CLSM results not corrected for lesion size — lower reliability than VLSM findings
    - Ventral stream connectivity finding is unexpected given prior literature emphasizing
      dorsal stream
  source_passages:
  - section: Discussion
    quote: preserved noncanonical sentence production on this priming task was strongly
      reliant on the integrity of ventral-stream connections to IFG
    page: 18
    supports: claim
  - section: Results – CLSM
    quote: Out of 136 possible connections in this restricted analysis, ASPT-A scores
      were predicted by integrity of 27 connections
    page: 12
    supports: statistics
  - section: Methods – Structural brain connectivity
    quote: Individual structural white matter whole-brain connectomes were constructed
      based on probabilistic diffusion tensor imaging
    page: 7
    supports: method
  - section: Methods – Connectivity analyses
    quote: results from the CLSM analyses did not survive correction for overall lesion
      size
    page: 17
    supports: limitation
- id: f4
  target: morphosyntactic_production_deficit
  target_kind: impairment
  claim: Lesions to the left IFG pars triangularis (BA 45) predict morphosyntactically
    reduced speech output (agrammatic production) after left-hemisphere stroke.
  direction: likely
  relationship: causal
  citation: '@DenOuden2019'
  method: VLSM
  design: cross-sectional
  imaging: structural_MRI
  sample:
    n: 68
    population: chronic left-hemisphere ischemic stroke survivors with and without
      aphasia
    time_post_onset: mean 52.8 months (SD 52.5, range 8-290 months)
    age_range: mean 59.6 years (SD 10.1, range 37-80)
    handedness: all right-handed
    language: English (native speakers)
    recruitment: USC and MUSC stroke cohort
    inclusion_criteria: Right-handed; native English speakers; left-hemisphere ischemic
      stroke; no premorbid neurological or psychiatric disorder.
    exclusion_criteria: Right-hemisphere lesion; cerebellar-only lesion; CT scan only
      (no MRI); excluded 3 participants from LSM for these reasons.
  statistics:
    threshold: p<0.05 permutation-corrected (5000 permutations, one-tailed)
    cluster_extent: voxels with at least 6 participants having lesions
    effect_size: not_reported
    ci_95: not_reported
    p_value: corrected alpha=0.05
  confounders_controlled:
  - Overall lesion size regressed out (binary logistic regression before VLSM)
  - Permutation testing for multiple comparisons
  confounders_not_controlled:
  - Time post-onset
  - Age
  - Education
  - Aphasia type
  - Cohort overlap with other USC/MUSC papers
  region_definition:
    kind: data_driven_cluster
    atlas: NiiStat VLSM output; anatomy confirmed with Catani-Thiebaut de Schotten
      (2008) tractography atlas
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - JHU atlas (Faria et al., 2012; Mori et al., 2008)
    - Catani-Thiebaut de Schotten (2008) tractography atlas
    modalities:
    - modality: T1
    - modality: T2
  author_limitations:
  - Clinical agrammatism classification based on limited speech sample (Cookie-Theft
    picture description only)
  - Cross-sectional design; chronic stage only; compensatory strategies cannot be
    assessed
  - SPPT noncanonical measure showed counterintuitive results; may not validly capture
    noncanonical production deficit
  - Lesion size regression may introduce Type II error (conservative)
  evidence_quality: cohort
  strength: moderate
  cohort_overlap_flag: true
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Abstract; Methods – Participants; Methods – Statistical analyses;
      Discussion (section 4.2)
    confidence: high
    flags:
    - USC/MUSC cohort (n=71); overlaps with @Fridriksson2018, @Yourganov2015Predicting,
      @Basilakos2015 (same lab)
    - PD-MR classification based on single speech sample (Cookie-Theft) — limited
      ecological validity
    - CLSM results not corrected for lesion size; treated as supplementary evidence
  source_passages:
  - section: Discussion
    quote: identification of morphosyntactic production problems in descriptive speech
      was most strongly predicted by structural lesions in the triangular part of
      the IFG
    page: 17
    supports: claim
  - section: Methods – Participants
    quote: 71 right-handed native speakers of English (mean age 59.6 years, SD 10.1,
      range 37–80 years; 23 females)
    page: 4
    supports: sample
  - section: Methods – Lesion-symptom mapping
    quote: corrected for multiple comparisons through permutation testing (5,000 permutations)
    page: 8
    supports: method
  - section: Methods – Lesion-symptom mapping
    quote: regressed out overall lesion size from the binary classifications in Analysis
      1
    page: 8
    supports: method
- id: f5
  target: verb_argument_structure_production
  target_kind: impairment
  claim: Lesions to the left posterior superior temporal gyrus (pSTG) and angular
    gyrus predict impaired verb argument structure production on the NAVS ASPT-A subtest.
  direction: likely
  relationship: causal
  citation: '@DenOuden2019'
  method: VLSM
  design: cross-sectional
  imaging: structural_MRI
  sample:
    n: 68
    population: chronic left-hemisphere ischemic stroke survivors with and without
      aphasia
    time_post_onset: mean 52.8 months (SD 52.5, range 8-290 months)
    age_range: mean 59.6 years (SD 10.1, range 37-80)
    handedness: all right-handed
    language: English (native speakers)
    recruitment: USC and MUSC stroke cohort
    inclusion_criteria: Right-handed; native English speakers; left-hemisphere ischemic
      stroke; no premorbid neurological or psychiatric disorder.
    exclusion_criteria: Right-hemisphere lesion; cerebellar-only lesion; CT scan only.
  statistics:
    threshold: p<0.05 permutation-corrected (5000 permutations, one-tailed)
    cluster_extent: k=47 voxels (ASPT-A cluster includes STG BA41 + angular gyrus
      + middle occipital gyrus)
    effect_size: not_reported
    ci_95: not_reported
    p_value: corrected alpha=0.05
  confounders_controlled:
  - Overall lesion size regressed out (linear regression before VLSM)
  - Permutation testing for multiple comparisons
  confounders_not_controlled:
  - Time post-onset
  - Age
  - Lexical-semantic ability (angular gyrus region may reflect semantic event knowledge)
  - Cohort overlap with other USC/MUSC papers
  region_definition:
    kind: data_driven_cluster
    atlas: NiiStat VLSM; peak BA 41 (superior temporal gyrus), extending into angular
      gyrus and middle occipital gyrus
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - JHU atlas (Faria et al., 2012; Mori et al., 2008)
    - Catani-Thiebaut de Schotten (2008) tractography atlas
    modalities:
    - modality: T1
    - modality: T2
  author_limitations:
  - Angular gyrus finding may reflect semantic event knowledge interface rather than
    stored argument-structure representations
  - Cross-sectional; chronic stage only
  - Lesion size regression may introduce Type II error
  evidence_quality: cohort
  strength: moderate
  cohort_overlap_flag: true
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results (Table 8; section 3.4.2); Discussion (section 4.2)
    confidence: high
    flags:
    - USC/MUSC cohort; overlaps with other USC papers
    - Angular gyrus result may reflect semantic-syntactic interface rather than pure
      syntax
  source_passages:
  - section: Results – VLSM
    quote: ASPT-A scores were negatively correlated with damage to the angular gyrus,
      extending into middle occipital gyrus
    page: 12
    supports: claim
  - section: Results – Table 8
    quote: angular gyrus, middle occipital gyrus
    page: 12
    supports: statistics
  - section: Discussion
    quote: location of this region makes a lot of sense. If "syntactic processing"
      is not exclusively a function of the dorsal stream
    page: 18
    supports: claim
- id: f6
  target: sentence_comprehension_production
  target_kind: impairment
  claim: Reduced structural connectivity in a ventral pathway between left IFG and
    temporal regions (especially IFG-pars-triangularis to pSTG/MTG) predicts impaired
    noncanonical sentence production on the NAVS SPPT.
  direction: likely
  relationship: correlational
  citation: '@DenOuden2019'
  method: VLSM
  design: cross-sectional
  imaging: DTI
  sample:
    n: 68
    population: chronic left-hemisphere ischemic stroke survivors with and without
      aphasia
    time_post_onset: mean 52.8 months (SD 52.5, range 8-290 months)
    age_range: mean 59.6 years (SD 10.1, range 37-80)
    handedness: all right-handed
    language: English (native speakers)
    recruitment: USC and MUSC stroke cohort
    inclusion_criteria: Right-handed; native English speakers; left-hemisphere ischemic
      stroke.
    exclusion_criteria: Right-hemisphere lesion; cerebellar-only lesion; CT scan only.
  statistics:
    threshold: p<0.05 permutation-corrected (5000 permutations, one-tailed) — CLSM
      analyses
    cluster_extent: 15 connections predictive of SPPT noncanonical performance
    effect_size: z values reported (range ~2.6-3.2)
    ci_95: not_reported
    p_value: corrected alpha=0.05
  confounders_controlled:
  - Canonical sentence performance partialed out as nuisance regressor (Freedman-Lane
    procedure)
  - Permutation testing for multiple comparisons
  confounders_not_controlled:
  - Overall lesion size NOT regressed out in CLSM (did not survive with regression)
  - General aphasia severity may confound results
  - Cohort overlap with other USC/MUSC papers
  region_definition:
    kind: tract
    atlas: JHU atlas 17-node perisylvian network; probabilistic tractography (FSL
      FDT, 5000 pathways)
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - JHU atlas (Faria et al., 2012; Mori et al., 2008)
    modalities:
    - modality: T1
    - modality: DTI
  author_limitations:
  - CLSM results did not survive correction for overall lesion size; treated as informative
    but less reliable
  - Connectome-based LSM is relatively novel; standards for optimal lesion size correction
    not yet established
  - SPPT noncanonical measure may have validity issues (counterintuitive patient performance
    pattern noted)
  evidence_quality: cohort
  strength: weak
  cohort_overlap_flag: true
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results (section 3.4.4; Table 9); Discussion (section 4.2); Methods
      (section 2.3.3)
    confidence: medium
    flags:
    - USC/MUSC cohort; overlaps with other USC papers
    - CLSM results not corrected for lesion size — lower reliability than VLSM findings
    - Ventral stream connectivity finding is unexpected given prior literature emphasizing
      dorsal stream
  source_passages:
  - section: Discussion
    quote: preserved noncanonical sentence production on this priming task was strongly
      reliant on the integrity of ventral-stream connections to IFG
    page: 18
    supports: claim
  - section: Results – CLSM
    quote: Out of 136 possible connections in this restricted analysis, ASPT-A scores
      were predicted by integrity of 27 connections
    page: 12
    supports: statistics
  - section: Methods – Structural brain connectivity
    quote: Individual structural white matter whole-brain connectomes were constructed
      based on probabilistic diffusion tensor imaging
    page: 7
    supports: method
  - section: Methods – Connectivity analyses
    quote: results from the CLSM analyses did not survive correction for overall lesion
      size
    page: 17
    supports: limitation
reviewer: claude-cowork
reviewed_on: '2026-05-06'
last_reviewed: '2026-05-07'
---
## Summary

den Ouden et al. (2019) examined neural correlates of syntactic processing deficits in aphasia using VLSM and connectome-based LSM in a cohort of 71 left-hemisphere stroke survivors (68 in imaging analyses) tested on the Northwestern Assessment of Verbs and Sentences (NAVS). Key findings: (1) morphosyntactically reduced speech (agrammatic output) is predicted by lesions to left IFG pars triangularis (BA 45); (2) verb argument structure production deficits are predicted by damage to left pSTG/angular gyrus; (3) overall sentence production/comprehension performance correlates with medial pSTG damage; (4) connectome analyses show both dorsal and ventral stream connections are critical for syntactic processing. The USC/MUSC cohort overlaps with other papers from the same lab.
