---
schema_version: 2.3
id: left_posterior_stg
name: "Left Posterior Superior Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:claude-sonnet-4-6"
created_on: 2026-05-06
hemisphere: left
aliases:
  - "posterior STG"
  - "left pSTG"
  - "Wernicke's area (posterior)"

notes: |
  Forward-looking target ID left_posterior_stg — not yet a canonical entry.
  This draft covers ventral-stream and sentence-comprehension findings from Fridriksson 2018
  "Anatomy of aphasia revisited" (Brain). Cite as @Fridriksson2018Anatomy.
  The paper includes both RLSM (region-wise conventional LSM) and CLSM (connectome-based LSM).
  Posterior STG is the strongest predictor of sentence comprehension and auditory word recognition
  in both univariate and multivariate analyses, and is the most frequently implicated region
  in multivariate RLSM across 16 tests (8 of 16 tests).
  Cohort (n=159) from USC/MUSC Aphasia Lab; overlaps with @Fridriksson2018 (n=138, same lab).
  The paper uses Faria et al. 2012 118-region atlas in MNI152 space.

findings:
  - id: f1
    target: sentence_comprehension
    target_kind: impairment
    claim: "Damage to left posterior STG is the strongest independent predictor of sentence comprehension impairment in chronic left-hemisphere stroke aphasia, accounting for 60% of variance in the multivariate RLSM analysis."
    direction: likely
    relationship: causal
    citation: "@Fridriksson2018Anatomy"

    method: LSM
    design: cross-sectional
    imaging: multimodal

    sample:
      n: 57
      population: "chronic left-hemisphere stroke survivors with aphasia (subset completing sentence comprehension battery)"
      time_post_onset: ">=6 months (mean 36.4 months, SD 43.1 for full sample)"
      age_range: "mean 60.0 years (SD 11.2) for full sample"
      handedness: not_reported
      language: "English (native speakers)"
      recruitment: "Archival database, Aphasia Lab, University of South Carolina and Medical University of South Carolina."
      inclusion_criteria: "Single left-hemisphere stroke >=6 months prior; native English speaker; completed sentence comprehension battery."
      exclusion_criteria: "History of dementia or other neurological problems."

    statistics:
      threshold: "permutation thresholding (4000 permutations), p<0.05 one-tailed (univariate); stepwise regression p<0.05 for entry (multivariate)"
      cluster_extent: not_reported
      effect_size: "R2=0.60 (posterior STG as first entry in multivariate RLSM for sentence comprehension); total model R2=0.63 (posterior STG + IFG orbitalis)"
      ci_95: not_reported
      p_value: not_reported

    confounders_controlled:
      - "time post-stroke (verified non-significant correlation with all 16 tests)"
    confounders_not_controlled:
      - "age"
      - "education"
      - "lesion volume"

    region_definition:
      kind: atlas
      atlas: "Faria et al. 2012 (118 grey matter regions)"
      description: "Posterior STG defined as a region of interest within the 118-region Faria et al. atlas used for RLSM analyses. Lesion load computed as proportion of intact voxels within the posterior STG grey matter region."

    imaging_details:
      field_strength: "3T"
      acquisition:
        sequence: "T1-weighted MP-RAGE (1mm isotropic) + T2 3D-SPACE + DTI EPI"
        voxel_size_mm: [1, 1, 1]
        TR_ms: 2250
        TE_ms: 4.52
      modalities:
        - modality: T1
          sequence: MP-RAGE
          voxel_size_mm: [1, 1, 1]
          TR_ms: 2250
          TE_ms: 4.52
        - modality: T2
          sequence: "3D-SPACE (TSE)"
          TR_ms: 2800
          TE_ms: 402
        - modality: DTI
          sequence: EPI
          voxel_size_mm: [2.7, 2.7, 2.7]
          TR_ms: 6100
          TE_ms: 101
          n_directions: 30
          b_values: [0, 1000, 2000]
      preprocessing_pipeline: "Enantiomorphic normalization via SPM12; SPM12 unified segmentation-normalization to MNI152; Faria 2012 118-region atlas parcellation; FSL FDT probabilistic tractography (BEDPOST + probtrackX)"
      reference_space: MNI152
      atlases_used:
        - "Faria et al. 2012 (118 grey matter regions)"
      coordinates_reported: []

    replications: []
    contradictions: []

    author_limitations:
      - "Number of participants who completed sentence comprehension assessment was 57 out of 159 total — reduced statistical power compared to tests administered to the full sample."
      - "The sentence comprehension task used here may not capture the full range of comprehension impairments; more sensitive measures exist."
      - "Univariate and multivariate results should be considered complementary."

    evidence_quality: cohort
    strength: strong

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results – RLSM; Table 2; Table 3; Discussion"
      confidence: high
      flags:
        - "n=57 for sentence comprehension subtest (not full n=159); verify this subgroup is still adequately powered"
        - "cohort overlaps with @Fridriksson2018 (same USC Aphasia Lab archival database)"
        - "posterior STG is also the top univariate predictor for AQ (Z=7.61, Table 2), auditory word recognition (Z=6.99), reading (Z=5.72), PNT correct (Z=5.13), syllable identification (Z=4.67) — it is by far the most widely-significant region across tests"
        - "CLSM for sentence comprehension: top connection is MTG <-> ITG (Z=3.92) — MTG-ITG connection more prominent than pSTG in CLSM"

    source_passages:
      - section: "Table 3"
        page: 9
        supports: statistics
        quote: "Sentence Comprehension\nPosterior STG\n0.60\n0.60\nIFG orbitalis\n0.63\n0.03"
      - section: "Table 2"
        page: 7
        supports: statistics
        quote: "Sentence Comprehension\nPosterior STG"
      - section: "Results – RLSM"
        page: 6
        supports: claim
        quote: "as predictors of speech and language performance in the univariate RLSM were: (i) pars opercularis; (ii) STG; and (iii) SMG. Damage to each of these three regions was a statistically significant predictor of performance on 14 of the 16 speech and language tests."
      - section: "Methods – Participants"
        page: 3
        supports: sample
        quote: "The total sample size was 159 chronic stroke survivors and\nthe number of tested participants varied across the different"
      - section: "Methods – Brain imaging"
        page: 4
        supports: imaging_details
        quote: "T1-weighted MRI using an\nMP-RAGE sequence with 1\nmm isotropic voxels"
      - section: "Methods – Data analyses"
        page: 5
        supports: method
        quote: "The univariate lesion analyses relied on conventional lesion symptom mapping: General Linear Model (GLM) (pooled variance t-test) with P < 0.05 (one-tailed) and control for multiple comparisons used permutation threshholding (4000 permutations)."
      - section: "Discussion"
        page: 11
        supports: limitation
        quote: "the number of participants who completed each test or task varied. Therefore, statistical power was not equal across all univariate analyses."

  - id: f2
    target: auditory_word_recognition
    target_kind: impairment
    claim: "Damage to left STG and posterior STG is the strongest predictor of impaired auditory word recognition in chronic left-hemisphere stroke aphasia, consistent with the ventral stream's role in auditory-to-meaning mapping."
    direction: likely
    relationship: causal
    citation: "@Fridriksson2018Anatomy"

    method: LSM
    design: cross-sectional
    imaging: multimodal

    sample:
      n: 159
      population: "chronic left-hemisphere stroke survivors with aphasia"
      time_post_onset: ">=6 months (mean 36.4 months, SD 43.1)"
      age_range: "mean 60.0 years (SD 11.2)"
      handedness: not_reported
      language: "English (native speakers)"
      recruitment: "USC/MUSC Aphasia Lab archival database."

    statistics:
      threshold: "permutation thresholding (4000 permutations), p<0.05 one-tailed"
      cluster_extent: not_reported
      effect_size: "STG R2=0.31 (first entry multivariate RLSM); total model R2=0.39 (STG + AG + MTG pole)"
      ci_95: not_reported
      p_value: not_reported

    confounders_controlled:
      - "time post-stroke (verified non-significant)"
    confounders_not_controlled:
      - "age"
      - "lesion volume"
      - "education"

    region_definition:
      kind: atlas
      atlas: "Faria et al. 2012 (118 grey matter regions)"
      description: "STG and posterior STG as separate regions in the 118-region atlas; lesion load computed per region."

    imaging_details:
      field_strength: "3T"
      acquisition:
        sequence: "T1-weighted MP-RAGE + T2 3D-SPACE + DTI EPI"
        voxel_size_mm: [1, 1, 1]
        TR_ms: 2250
        TE_ms: 4.52
      preprocessing_pipeline: "Enantiomorphic normalization SPM12; Faria 2012 atlas parcellation; FSL FDT tractography"
      reference_space: MNI152
      atlases_used:
        - "Faria et al. 2012"
      coordinates_reported: []

    replications: []
    contradictions: []

    author_limitations:
      - "Auditory word recognition relied on a 60-point pointing-to-picture task (WAB Auditory Word Recognition subtest) — may not capture subtle comprehension deficits."

    evidence_quality: cohort
    strength: strong

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results – RLSM; Table 2; Table 3"
      confidence: high
      flags:
        - "cohort overlaps with @Fridriksson2018 (same USC Aphasia Lab archival database)"
        - "CLSM for auditory word recognition: top univariate connection STG <-> posterior STG (Z=4.75), then AG <-> posterior STG (Z=4.29); predominantly ventral stream links"
        - "Multivariate RLSM for auditory word recognition: STG (R2=0.31), AG (R2=0.36), MTG pole (R2=0.39)"

    source_passages:
      - section: "Table 3"
        page: 9
        supports: statistics
        quote: "Auditory Word Recognition\nSTG\n0.31\n0.31\nAG\n0.36\n0.05\nMTG p"
      - section: "Table 2"
        page: 7
        supports: statistics
        quote: "Auditory Word Recognition\nSTG"
      - section: "Discussion"
        page: 9
        supports: claim
        quote: "Much of the damage associated with 'auditory word recognition' involved the ventral stream with relatively fewer links involving the dorsal stream"
      - section: "Methods – Participants"
        page: 3
        supports: sample
        quote: "The total sample size was 159 chronic stroke survivors"
      - section: "Methods – Brain imaging"
        page: 4
        supports: imaging_details
        quote: "T1-weighted MRI using an MP-RAGE sequence with 1 mm isotropic voxels"
      - section: "Methods – Data analyses"
        page: 5
        supports: method
        quote: "The univariate lesion analyses relied on conventional lesion symptom mapping: General Linear Model (GLM) (pooled variance t-test) with P < 0.05 (one-tailed) and control for multiple comparisons used permutation threshholding (4000 permutations)."
      - section: "Discussion"
        page: 11
        supports: limitation
        quote: "The reading and writing subtests on the Western Aphasia Battery provide a somewhat shallow picture of alexia and agraphia, respectively."

  - id: f3
    target: naming
    target_kind: impairment
    claim: "Naming impairment (PNT correct) in chronic left-hemisphere stroke aphasia is associated with damage to an extensive cortical network including both ventral stream (posterior STG) and dorsal stream (precentral gyrus) regions, with no single dominant lesion location."
    direction: likely
    relationship: causal
    citation: "@Fridriksson2018Anatomy"

    method: LSM
    design: cross-sectional
    imaging: multimodal

    sample:
      n: 105
      population: "chronic left-hemisphere stroke survivors with aphasia (subset completing PNT)"
      time_post_onset: ">=6 months (mean 36.4 months, SD 43.1 for full sample)"
      age_range: "mean 60.0 years (SD 11.2) for full sample"
      handedness: not_reported
      language: "English (native speakers)"
      recruitment: "USC/MUSC Aphasia Lab archival database."

    statistics:
      threshold: "permutation thresholding (4000 permutations), p<0.05 one-tailed"
      cluster_extent: not_reported
      effect_size: "Posterior STG R2=0.22 (first entry multivariate RLSM for PNT correct); PrCG adds R2=0.29 total"
      ci_95: not_reported
      p_value: not_reported

    confounders_controlled:
      - "time post-stroke (verified non-significant)"
    confounders_not_controlled:
      - "age"
      - "lesion volume"

    region_definition:
      kind: atlas
      atlas: "Faria et al. 2012 (118 grey matter regions)"
      description: "Region-wise RLSM and CLSM across 20 dorsal/ventral stream ROIs."

    imaging_details:
      field_strength: "3T"
      acquisition:
        sequence: "T1-weighted MP-RAGE + T2 3D-SPACE + DTI EPI"
        voxel_size_mm: [1, 1, 1]
        TR_ms: 2250
        TE_ms: 4.52
      preprocessing_pipeline: "Enantiomorphic normalization SPM12; Faria 2012 atlas parcellation; FSL FDT tractography"
      reference_space: MNI152
      atlases_used:
        - "Faria et al. 2012"
      coordinates_reported: []

    replications:
      - "@Yourganov2015Predicting"
    contradictions: []

    author_limitations:
      - "Anomia (as captured by PNT correct) relies on an extensive cortical network — different lesion locations can cause similar naming impairment."
      - "Multivariate RLSM for PNT correct explains only 29% of variance; much variance remains unexplained by region-level damage alone."

    evidence_quality: cohort
    strength: moderate

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results – RLSM; Results – CLSM; Table 2; Table 3; Discussion"
      confidence: high
      flags:
        - "n=105 for PNT (not full n=159)"
        - "cohort overlaps with @Fridriksson2018 (same USC Aphasia Lab)"
        - "paper states 'unlike Wernicke's, Broca's, conduction, or global aphasia, anomic aphasia has no specific lesion location' (citing Yourganov 2015) — this is consistent with low R2 for naming"
        - "CLSM for PNT correct: top univariate link is PrCG <-> posterior STG (Z=4.21); multivariate CLSM: posterior STG <-> PrCG R2=0.18 (first entry), then multiple additional links adding to total R2=0.48"
        - "The naming finding illustrates the key claim: many different lesion locations can impair naming because naming relies on both dorsal and ventral stream networks"

    source_passages:
      - section: "Table 3"
        page: 9
        supports: statistics
        quote: "PNT Correct\nPosterior STG\n0.22\n0.22\nPrCG\n0.29\n0.06"
      - section: "Table 2"
        page: 7
        supports: statistics
        quote: "PNT Correct\nPosterior STG"
      - section: "Discussion"
        page: 9
        supports: claim
        quote: "ated by damage that predicts naming impair-\nment, anomia. In the current study, 'correct naming' was pre-\ndicted in the univariate analysis by a lesion location mostly\ninvolving posterior structures, including the posterior STG\nand angular gyrus."
      - section: "Discussion"
        page: 9
        supports: claim
        quote: "unlike\nWernicke's, Broca's, conduction, or global aphasia, anomic\naphasia has no specific lesion location."
      - section: "Methods – Participants"
        page: 3
        supports: sample
        quote: "The total sample size was 159 chronic stroke survivors and the number of tested participants varied across the different assessment batteries"
      - section: "Methods – Brain imaging"
        page: 4
        supports: imaging_details
        quote: "T1-weighted MRI using an MP-RAGE sequence with 1 mm isotropic voxels"
      - section: "Methods – Data analyses"
        page: 5
        supports: method
        quote: "The lesion and connectome analyses focused on grey matter regions of interest within the dual streams defined in Fridriksson et al. (2016)."
      - section: "Discussion"
        page: 11
        supports: limitation
        quote: "It is also possible that error responses on individual tasks reflected impaired processes rooted in different cortical locations."

source: draft
notes: |
  Fridriksson 2018 "Anatomy of aphasia revisited" (Brain) — posterior STG / ventral stream draft.
  Three findings extracted anchored on left_posterior_stg:
    f1: posterior STG -> sentence comprehension (strongest predictor, R2=0.60 multivariate RLSM; n=57 subset)
    f2: STG/posterior STG -> auditory word recognition (R2=0.31 multivariate; full n=159)
    f3: posterior STG (+ precentral gyrus) -> naming/PNT (R2=0.22 multivariate; n=105 subset)
  The paper's main message: posterior STG is the most widely implicated region (top predictor on 8/16 tests
  in multivariate RLSM). It is the primary ventral stream hub for auditory-to-meaning processing.
  Dorsal stream (pars opercularis, precentral) hub findings are in companion draft
  left_ifg_pars_opercularis__Fridriksson2018Anatomy.md.
  Cohort overlaps with @Fridriksson2018 (USC Aphasia Lab, n=138 vs n=159).
  sentence_comprehension, auditory_word_recognition, naming are forward-looking impairment IDs.
---

# Left Posterior STG — Fridriksson 2018 Anatomy (RLSM + CLSM)

Fridriksson et al. 2018 "Anatomy of aphasia revisited" (Brain) establishes the posterior STG as
the most widely-implicated region for speech and language impairment across 16 clinical aphasia tests,
in 159 chronic LH stroke patients. It is the strongest predictor of sentence comprehension (R2=0.60)
and auditory word recognition (R2=0.31) in multivariate RLSM, and is prominently involved in
naming networks via CLSM.

The study demonstrates that the posterior STG is a critical ventral stream hub, while pars opercularis
and precentral gyrus anchor the dorsal stream. Naming (anomia) uniquely requires both streams.
