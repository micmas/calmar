---
schema_version: 2.3
id: phonological_component_analysis
name: "Phonological Component Analysis (PCA)"
kind: therapy
status: draft
created_by: "agent:claude-sonnet-4-6"
created_on: 2026-05-06

short_description: >
  Anomia therapy in which patients generate phonological components of a
  target word (first phoneme, final phoneme, number of syllables, rhyming
  word, another word starting with the same phoneme) cued by a picture and
  visual orthographic supports. Aims to strengthen lexical-phonological
  retrieval for naming impairment, primarily in chronic post-stroke aphasia.

targets_impairments:
  - anomia
  - phonological_production
  - lexical_retrieval

findings:
  - id: f1
    target: left_temporal_fusiform_cortex_anterior
    target_kind: region
    claim: >
      PCA therapy in French is associated with increased resting-state functional
      connectivity between the anterior left temporal fusiform cortex and bilateral
      supracalcarine cortex, and between the left supracalcarine cortex and the
      anterior left inferior temporal gyrus.
    direction: likely
    relationship: treatment_response
    citation: "@MassonTrottier2021"

    method: rs_fMRI
    design: longitudinal
    imaging: fMRI

    sample:
      n: 10
      population: "chronic left-hemisphere ischemic stroke survivors with aphasia and anomia"
      time_post_onset: "11–172 months post-onset (chronic)"
      age_range: "mean 68.9 ± 10.2 years"
      handedness: "premorbid right-handed"
      language: "French-speaking (Quebec)"
      recruitment: "recruited through local patient associations and self-referral following discharge from rehabilitation centers in Quebec"
      inclusion_criteria: "single LH ischemic stroke; diagnosis of aphasia per Montreal-Toulouse battery; presence of anomia; right-handed premorbid"
      exclusion_criteria: "neurological/psychiatric diagnosis other than stroke; fMRI incompatibility; mild cognitive impairment or dementia before stroke"

    statistics:
      threshold: "p-FDR < 0.05 (ROI-to-ROI paired t-test, CONN toolbox)"
      cluster_extent: not_reported
      effect_size: not_reported
      ci_95: not_reported
      p_value: "ant. Temporal Fusiform L – SCC L: T(9)=7.20, p-FDR=0.0053; SCC R: T(9)=4.83, p-FDR=0.0488; SCC L – ant. ITG L: T(9)=5.07, p-FDR=0.0443"

    confounders_controlled:
      - "pre/post paired design (participants serve as own controls)"
      - "white matter, CSF, realignment, and scrubbing parameters used as nuisance regressors"
      - "lesion segmented as CSF and regressed out"
    confounders_not_controlled:
      - "no active control group"
      - "lesion volume not formally covaried in main FC analysis"
      - "liberal motion outlier settings (>2mm/2deg) may inflate FC estimates"

    region_definition:
      kind: atlas
      atlas: "FSL Harvard-Oxford atlas (via CONN toolbox v18.b)"
      description: "106 ROIs (91 cortical + 15 subcortical from Harvard-Oxford atlas) parcellating the whole brain; ROI-to-ROI FC matrix 106×106"

    imaging_details:
      field_strength: "3T"
      modalities:
        - modality: fMRI_resting_state
          sequence: "T2*-weighted EPI"
          voxel_size_mm: [3, 3, 3]
          TR_ms: 2200
          TE_ms: 30
          volumes: 184
        - modality: T1
          sequence: "MP-RAGE (TFE)"
          voxel_size_mm: [1, 1, 1]
          TR_ms: 2300
          TE_ms: 2.98
      preprocessing_pipeline: "SPM12; slice-time correction; motion correction (12 params); ART outlier detection; spatial normalization to MNI using EPI template (due to lesions altering T1 normalization); resampled 2×2×2 mm; band-pass filter 0.008–0.09 Hz; nuisance regression (WM, CSF, motion, scrubbing); CONN toolbox v18.b for FC"
      reference_space: "MNI152"
      atlases_used:
        - "FSL Harvard-Oxford cortical atlas"
        - "FSL Harvard-Oxford subcortical atlas"
      coordinates_reported: []

    replications: []
    contradictions: []

    author_limitations:
      - "Small sample (n=10) without an active control group; healthy controls showed stable rsFC over 5 weeks in a prior publication, supporting therapy-related interpretation."
      - "Liberal motion outlier thresholds (>2mm/2deg) may increase frame-wise displacement and inflate results."
      - "Lesion segmented and regressed out as CSF — additional preprocessing steps to remove lesion artifacts may be warranted, though impact appears minimal as changed FC regions are distant from lesion sites."
      - "No significant correlation found between rsFC changes and naming improvements on trained or untrained items."

    evidence_quality: cohort
    strength: weak

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results – Functional Connectivity Results (p.6); Methods – Data Acquisition (p.5); Discussion (p.9)"
      confidence: high
      flags:
        - "n=10 is very small for rs-fMRI; results should be treated as exploratory"
        - "No correlation between rsFC changes and behavioral naming gains — directionality of connectivity finding as therapy mechanism is assumed, not demonstrated"
        - "forward-looking target IDs used: left_temporal_fusiform_cortex_anterior, left_supracalcarine_cortex, left_inferior_temporal_gyrus_anterior"

    source_passages:
      - section: "Results – Functional Connectivity Results"
        page: 6
        supports: claim
        quote: >
          the anterior division of the left temporal fusiform cortex was more functionally
          connected to the supracalcarine (SCC) cortex bilaterally. Furthermore, the left
          SCC cortex was more functionally connected with the anterior division of the left
          inferior temporal gyrus.
      - section: "Methods – Participants"
        page: 3
        supports: sample
        quote: >
          Ten participants with chronic aphasia (3 women, mean age = 68.9 ± 10.2) following
          a single left hemisphere ischemic stroke recruited through local patient association
          by referral following discharge from rehabilitation centers in the area and
          following self-referral are included in this study.
      - section: "Methods – Data Acquisition and Preprocessing"
        page: 5
        supports: imaging_details
        quote: >
          Images were acquired using a 3 T MRI Siemens Trio scanner updated to Prisma Fit
          with a standard 32-channel head coil during data collection. The image sequence
          is a T2*-weighted pulse sequence (184 volumes; TR = 2200 ms; TE = 30 ms; matrix
          = 64 × 64 voxels; FOV = 210 mm; flip angle = 90°; slice thickness = 3 mm).
      - section: "Methods – Functional Connectivity Analysis"
        page: 6
        supports: method
        quote: >
          Resting-state functional connectivity analysis was performed using the CONN func-
          tional connectivity toolbox (v.18.b, available online: http://www.nitrc.org/projects/conn,
          accessed on 29 January 2021, [63]). An ROI-to-ROI analysis was conducted by comput-
          ing the Fisher-transformed bivariate correlation coefﬁcients between the time-series of
          each pair of ROIs.
      - section: "Results – Functional Connectivity Results"
        page: 7
        supports: statistics
        quote: >
          ant. Temporal Fusiform Cortex L Supracalcarine Cortex L 7.20 0.0053
          Supracalcarine Cortex R 4.83 0.0488 Supracalcarine Cortex L
          ant. Inferior Temporal Gyrus L 5.07 0.0443 Lingual Gyrus R
          Superior Frontal Gyrus R −5.73 0.0298
      - section: "Discussion – Limitations"
        page: 10
        supports: limitation
        quote: >
          regarding the outlier detection, although the parameters used are commonly applied
          in the clinical studies, using liberal settings leads to higher frame-wise
          displacement values, which can have an impact on the results.

  - id: f2
    target: right_lingual_gyrus
    target_kind: region
    claim: >
      PCA therapy in French is associated with decreased resting-state functional
      connectivity between the right lingual gyrus and right superior frontal gyrus,
      concurrent with naming improvement, possibly reflecting reduction of maladaptive
      right hemisphere recruitment.
    direction: likely
    relationship: treatment_response
    citation: "@MassonTrottier2021"

    method: rs_fMRI
    design: longitudinal
    imaging: fMRI

    sample:
      n: 10
      population: "chronic left-hemisphere ischemic stroke survivors with aphasia and anomia"
      time_post_onset: "11–172 months post-onset (chronic)"
      age_range: "mean 68.9 ± 10.2 years"
      handedness: "premorbid right-handed"
      language: "French-speaking (Quebec)"
      recruitment: "recruited through local patient associations and self-referral"
      inclusion_criteria: "single LH ischemic stroke; diagnosis of aphasia; presence of anomia; premorbid right-handed"
      exclusion_criteria: "neurological/psychiatric diagnosis other than stroke; fMRI incompatibility; MCI/dementia before stroke"

    statistics:
      threshold: "p-FDR < 0.05 (ROI-to-ROI paired t-test, CONN toolbox)"
      cluster_extent: not_reported
      effect_size: not_reported
      ci_95: not_reported
      p_value: "Lingual Gyrus R – Superior Frontal Gyrus R: T(9)=−5.73, p-FDR=0.0298"

    confounders_controlled:
      - "pre/post paired design (participants serve as own controls)"
      - "nuisance regression of WM, CSF, motion, scrubbing"
    confounders_not_controlled:
      - "no active control group"
      - "lesion volume not covaried in main analysis"

    region_definition:
      kind: atlas
      atlas: "FSL Harvard-Oxford atlas (via CONN toolbox v18.b)"
      description: "ROI-to-ROI analysis across 106 Harvard-Oxford atlas regions"

    imaging_details:
      field_strength: "3T"
      acquisition:
        voxel_size_mm: [3, 3, 3]
        TR_ms: 2200
        TE_ms: 30
        sequence: "T2*-weighted EPI"
      preprocessing_pipeline: "SPM12; EPI-template normalization to MNI; band-pass 0.008–0.09 Hz; nuisance regression; CONN toolbox v18.b"
      reference_space: "MNI152"
      atlases_used:
        - "FSL Harvard-Oxford cortical atlas"
      coordinates_reported: []

    replications: []
    contradictions: []

    author_limitations:
      - "Small sample (n=10) without active control group."
      - "No significant correlation between rsFC changes and naming improvement — therapy-driven interpretation is presumptive."

    evidence_quality: cohort
    strength: weak

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results – Functional Connectivity Results (Table 2, p.7); Discussion (p.9)"
      confidence: high
      flags:
        - "Decrease in RH FC interpreted by authors as reduction of maladaptive RH recruitment — this is an inference, not directly tested"
        - "forward-looking target IDs: right_lingual_gyrus, right_superior_frontal_gyrus"

    source_passages:
      - section: "Results – Functional Connectivity Results"
        page: 7
        supports: claim
        quote: >
          the lingual gyrus was less functionally connected with the superior frontal gyrus
          in the RH.
      - section: "Discussion"
        page: 9
        supports: claim
        quote: >
          going in the same direction as theories regarding maladaptive effects of RH
          recruitment on language function following aphasia, the results of this work show
          that naming recovery following Fr-PCA happened concomitantly with a decreased RH
          functional connectivity between visual (lingual gyrus, BA18) and semantic (SFG,
          BA8–9) networks.
      - section: "Results – Functional Connectivity Results"
        page: 7
        supports: statistics
        quote: >
          Lingual Gyrus R Superior Frontal Gyrus R −5.73 0.0298

source: extracted
notes: |
  This is a therapy-anchored draft (PCA → rsFC changes). The anchor is the therapy because the
  paper does not report lesion-symptom associations; it reports pre/post rsFC changes following a
  specific named therapy (Fr-PCA). Per the anchor-perspective rule, two findings are extracted:
  f1 (increased LH visual-semantic connectivity) and f2 (decreased RH connectivity). Both use
  relationship: treatment_response per the v2.3 convention for treatment-induced activation/connectivity
  changes. Forward-looking region target IDs used (regions not yet in canonical KB).
  Behavioral efficacy: trained items W(10)=55.0, Z=2.805, p=0.005, r=0.89;
  untrained items W(10)=55.0, Z=2.807, p=0.005, r=0.89. Behavioral finding not separately
  extracted as it is behavioral-only and the paper's primary contribution is the rsFC result.
---
