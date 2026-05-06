---
schema_version: 2.3
id: severity_metric
name: "Aphasia severity metric (WAB-R subtest scores)"
aliases:
  - WAB-R subtest
  - WAB-AQ subtest
  - spontaneous speech score
  - naming score
  - repetition score
  - auditory comprehension score
kind: predictor
predictor_type: behavioural
short_definition: >-
  Standardised subtest scores from the Western Aphasia Battery–Revised
  measuring spontaneous speech, naming, repetition, and auditory
  comprehension in post-stroke aphasia.
assessment:
  - "WAB-R spontaneous speech (0–20)"
  - "WAB-R naming (0–10)"
  - "WAB-R repetition (0–10)"
  - "WAB-R auditory comprehension (0–10)"
units: "subtest raw score (ranges vary by subtest)"
typical_range: "spontaneous speech 3–19; naming 0.1–9.6; repetition 0.1–10; auditory comprehension 3–10 (Kristinsson 2025 sample)"
direction_of_severity: lower_is_worse
status: draft
created_by: "agent:claude-sonnet-4-6"
created_on: 2026-05-06
notes: >-
  This draft anchors findings from Kristinsson et al. 2025 (POLAR trial;
  NCT03416738) about multimodal brain network correlates of WAB-R subtest
  performance. The paper is primarily a predictor/prognosis study using
  PLSR to decompose shared vs. unique lesion-behaviour covariance — not a
  region-specific LSM — so findings are anchored here rather than in
  region drafts. Perisylvian region labels in f1 and f2 are aggregate
  (left rolandic operculum, STG, ITG) from VIP-score rankings across
  7 neuroimaging modalities; they are not single-modality LSM coordinates.
  Forward-looking target IDs for unique brain regions (right_putamen,
  left_superior_temporal_lobe, right_precuneus) do not yet exist as
  canonical entries.

findings:
  - id: f1
    target: left_perisylvian_network
    target_kind: region
    claim: >-
      Damage to left perisylvian regions — particularly the rolandic
      operculum, superior temporal gyrus, and inferior temporal gyrus —
      accounts for the largest shared variance across all four WAB-R
      subtests in chronic post-stroke aphasia, with the rolandic operculum
      implicated across seven out of eleven neuroimaging modality-specific
      PLSR models.
    direction: likely
    relationship: correlational
    citation: "@Kristinsson2025"
    method: [MLPA, DTI, fMRI_FC]
    design: cross-sectional
    imaging: multimodal

    sample:
      n: 86
      population: "chronic left-hemisphere stroke with aphasia (WAB-AQ ≤93.8)"
      time_post_onset: "≥12 months post-stroke (chronic)"
      age_range: "not_reported"
      handedness: "not_reported"
      language: "not_reported"
      recruitment: "POLAR trial (NCT03416738); recruited via local advertisement at University of South Carolina and Medical University of South Carolina."
      inclusion_criteria: "chronic (≥12 months) left-hemisphere stroke; aphasia (WAB-AQ ≤93.8); all neuroimaging modalities available."
      exclusion_criteria: "WAB-AQ >93.8 (no aphasia); missing any neuroimaging modality."

    statistics:
      threshold: "VIP > 1.5 across ≥4 modality-specific PLSR models; LOOCV-validated Pearson r"
      effect_size: "shared variance: R²=0.22–0.25 across WAB-R subtests; highest r for auditory comprehension DTI model (r=0.45, p<0.01), spontaneous speech DTI model (r=0.42, p<0.01)"
      ci_95: "not_reported"
      p_value: "<0.01 (LOOCV-validated)"

    confounders_controlled:
      - "leave-one-out cross-validation (LOOCV) used for model validation"
    confounders_not_controlled:
      - "age"
      - "sex"
      - "time post-stroke"
      - "lesion volume (not covaried out; modelled as one of the neuroimaging inputs)"
      - "modalities not combined within a single model"

    region_definition:
      kind: data_driven_cluster
      description: >-
        Regions ranked by Variable Importance in Projection (VIP) scores
        across 11 modality-specific PLSR models using the AICHA atlas
        (384 homotopic regions). Regions appearing in ≥4 models with
        VIP>1.5 were considered shared predictors. Rolandic operculum
        (G_Rolandic_Oper-2-L, S_Rolando-1-L), superior and inferior
        temporal gyri (G_Temporal_Sup-2-L, G_Temporal_Inf-5-L) were
        most consistently implicated.

    imaging_details:
      field_strength: "3T"
      modalities:
        - modality: T1
          sequence: "MP-RAGE"
          voxel_size_mm: [1, 1, 1]
          TR_ms: not_reported
          TE_ms: not_reported
        - modality: fMRI
          sequence: EPI
          voxel_size_mm: [3.25, 3.25, 3.2]
          TR_ms: 10000
          TE_ms: 30
          volumes: not_reported
          task: "Picture-naming (real nouns > abstract images)"
        - modality: DTI
          voxel_size_mm: not_reported
          n_directions: not_reported
          b_values: not_reported
        - modality: ASL
          sequence: PCASL
          voxel_size_mm: [3.0, 3.0, 6.0]
          TR_ms: 2500
          TE_ms: 13
      preprocessing_pipeline: >-
        Lesion: manual tracing on T2 in native space; enantiomorphic normalization via Clinical Toolbox (SPM12 unified segmentation-normalization to MNI). Connectomics: AICHA-atlas-based DTI tractography and rsfMRI connectivity. VBM: CAT12 toolbox (enantiomorphically healed T1). Task-fMRI: SPM12 GLM (real>abstract contrast). FA/MD: FSL DTIFIT. CBF: ASLtbx.
      reference_space: "MNI152"
      atlases_used:
        - "AICHA (Atlas of Intrinsic Connectivity of Homotopic Areas; 384 regions)"
      coordinates_reported: []

    replications: []
    contradictions: []

    author_limitations:
      - "Primary purpose was to characterise latent lesion-behaviour structure rather than optimise prediction accuracy."
      - "Language impairment quantified using WAB-R only — a coarse measure; other batteries might reveal a different anatomical structure."
      - "Neuroimaging modalities were not combined within a single model; additive multimodal benefit was not tested."
      - "Findings do not represent an exhaustive overview of all contributing regions."

    evidence_quality: cohort
    strength: moderate

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results — Predicting language deficits from shared lesion characteristics (pages 10–12)"
      confidence: high
      flags:
        - "cohort overlaps with @Fridriksson2018, @Yourganov2015Predicting (USC/MUSC Aphasia Lab, POLAR trial NCT03416738); flag for downstream double-counting risk."
        - "left_perisylvian_network is a forward-looking target ID — does not yet exist as a canonical entry."

    source_passages:
      - section: "Abstract"
        page: 1
        quote: >-
          damage to regions surrounding the perisylvian fissure accounting for
          the largest amount of shared variance across Western Aphasia Battery-Revised subtests
        supports: claim

      - section: "Results — Predicting language deficits from shared lesion characteristics"
        page: 10
        quote: >-
          Across modality-specific models, the left rolandic operculum emerged as the most
          frequently implicated region, identified in seven models (Fig. 5; Supplementary Fig. 1).
        supports: claim

      - section: "Results — Predicting language deficits from shared lesion characteristics"
        page: 10
        quote: >-
          The structural connectivity model yielded the highest correlation coefficients
          for auditory comprehension (r = 0.45, P < 0.01) and spontaneous speech (r = 0.42, P < 0.01)
        supports: statistics

      - section: "Methods — Study design and participants"
        page: 4
        quote: >-
          A total of 86 participants with chronic (at least 12 months prior to enrolment)
          left hemisphere strokes were examined
        supports: sample

      - section: "Methods — Data analysis"
        page: 6
        quote: >-
          PLSR was employed to examine co-varying patterns of lesion damage and language impairment
        supports: method

      - section: "Methods — Acquisition of neuroimaging data"
        page: 4
        quote: >-
          All participants underwent research MRI scanning on Siemens Trio 3T scanners equipped
          with a 20-channel head coil
        supports: imaging_details

      - section: "Methods — Data analysis"
        page: 6
        quote: >-
          we restricted the regression analysis to the first five LVs and the regions with the
          highest-ranking VIP scores (NVIP = 50 for structural and functional connectivity models;
          NVIP = 30 for all other modalities; all VIP > 1.5)
        supports: statistics

      - section: "Limitations"
        page: 16
        quote: >-
          which is a fairly coarse measure of language processing
        supports: limitation

  - id: f2
    target: left_perisylvian_network
    target_kind: region
    claim: >-
      After controlling for shared perisylvian lesion variance, right putamen
      integrity uniquely and independently predicts naming and repetition
      performance, while left superior temporal lobe and right precuneus
      integrity uniquely predict auditory comprehension.
    direction: likely
    relationship: correlational
    citation: "@Kristinsson2025"
    method: [MLPA, DTI]
    design: cross-sectional
    imaging: multimodal

    sample:
      n: 86
      population: "chronic left-hemisphere stroke with aphasia (WAB-AQ ≤93.8)"
      time_post_onset: "≥12 months post-stroke (chronic)"
      age_range: "not_reported"
      handedness: "not_reported"
      language: "not_reported"
      recruitment: "POLAR trial (NCT03416738); University of South Carolina and Medical University of South Carolina."
      inclusion_criteria: "chronic (≥12 months) left-hemisphere stroke; aphasia; complete multimodal neuroimaging."
      exclusion_criteria: "WAB-AQ >93.8; missing neuroimaging modality."

    statistics:
      threshold: "post-hoc linear regression; p=0.013 (naming, right putamen), p=0.021 (repetition, right putamen), p=0.049 (auditory comprehension, left STL), p=0.045 (auditory comprehension, right precuneus)"
      effect_size: "unique variance explained: naming 17.4%, repetition 19.4%, auditory comprehension 27.9%, spontaneous speech 5.0%"
      ci_95: "not_reported"
      p_value: "see above per region/subtest pair"

    confounders_controlled:
      - "shared perisylvian lesion variance (rolandic operculum, STG, ITG proportional lesion)"
    confounders_not_controlled:
      - "age"
      - "sex"
      - "time post-stroke"
      - "post-hoc analysis not pre-specified"

    region_definition:
      kind: data_driven_cluster
      description: >-
        Unique regions identified via post-hoc residual analysis: WAB-R
        subtest scores residualised on shared perisylvian lesion then
        regressed on mean diffusivity (MD) of regions with average
        beta ≥±0.2 for one subtest and lower for others (AICHA atlas).
        Right putamen, left superior temporal lobe, and right precuneus
        were the dominant unique predictors.

    imaging_details:
      field_strength: "3T"
      modalities:
        - modality: T1
          sequence: "MP-RAGE"
          voxel_size_mm: [1, 1, 1]
        - modality: DTI
          voxel_size_mm: not_reported
      preprocessing_pipeline: >-
        FA and MD extracted per AICHA atlas region using FSL DTIFIT after TOPUP and EDDY correction. Enantiomorphic normalization of lesion maps to MNI.
      reference_space: "MNI152"
      atlases_used:
        - "AICHA (384 regions)"
      coordinates_reported: []

    replications: []
    contradictions: []

    author_limitations:
      - "Post-hoc residual analysis is not exhaustive — aims only to illustrate the unique versus shared lesion distinction in a principled manner."
      - "No spontaneous speech unique effects observed — may reflect ceiling in shared-variance explanation or the breadth of processes tapped by spontaneous speech."

    evidence_quality: cohort
    strength: weak

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results — Neural architecture uniquely associated with specific language deficits (page 12)"
      confidence: medium
      flags:
        - "post-hoc analysis; not pre-specified; interpret as exploratory."
        - "cohort overlaps with @Fridriksson2018, @Yourganov2015Predicting (USC/MUSC Aphasia Lab, POLAR trial NCT03416738)."
        - "right_putamen, left_superior_temporal_lobe, right_precuneus are forward-looking target IDs."

    source_passages:
      - section: "Results — Neural architecture uniquely associated with specific language deficits"
        page: 12
        quote: >-
          the right putamen emerged as the strongest unique predictor of naming and
          repetition performance (P = 0.013 and 0.021, respectively)
        supports: claim

      - section: "Results — Neural architecture uniquely associated with specific language deficits"
        page: 12
        quote: >-
          the unique models accounted for a significant portion of additional variance:
          5.0% in spontaneous speech, 19.4% in repetition, 17.4% in naming, and 27.9% in
          auditory comprehension
        supports: statistics

      - section: "Results — Neural architecture uniquely associated with specific language deficits"
        page: 12
        quote: >-
          part of the left superior temporal lobe (P = 0.049) and the right precuneus
          (P = 0.045) emerged as the strongest predictors of auditory comprehension
        supports: claim

      - section: "Methods — Study design and participants"
        page: 4
        quote: >-
          A total of 86 participants with chronic (at least 12 months prior to enrolment)
          left hemisphere strokes were examined
        supports: sample

      - section: "Methods — Data analysis"
        page: 6
        quote: >-
          we predicted language outcomes based on proportional lesion in the four shared
          regions — assuming that damage leads to poorer performance — and MD in regions
          uniquely associated with specific subtest scores
        supports: method

      - section: "Limitations"
        page: 16
        quote: >-
          [...] of several key areas for language performance, they do not represent an exhaustive
          overview of regions that contribute to language functioning.
        supports: limitation
---

## Notes

Kristinsson et al. 2025 is a multimodal PLSR study that decomposes lesion-behaviour covariance
into shared (perisylvian) and unique (region-specific) components across four WAB-R subtests
in 86 chronic post-stroke aphasia patients from the POLAR trial. Because the primary claims
are about multivariate network-level predictors of WAB-R performance rather than about
specific regions per se, findings are anchored in the `predictors/` bucket targeting the
shared network and unique sub-networks.

Key cohort note: POLAR trial (NCT03416738) is a USC/MUSC cohort that may overlap with
other USC Aphasia Lab papers (e.g., @Fridriksson2018, @Yourganov2015Predicting) — flag
for downstream double-counting risk in interpret_overlap().
