---
schema_version: 2.3
id: left_posterior_stg
name: "Left Posterior Superior Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: syntactic_processing
    target_kind: impairment
    claim: "Damage to the left posterior superior and middle temporal gyri is significantly associated with paragrammatism, independent of speech rate."
    direction: likely
    relationship: causal
    citation: "@Matchin2020"
    method: LSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 53
      population: "chronic left-hemisphere stroke aphasia"
      time_post_onset: ">= 6 months"
      age_range: "mean 59.2 (SD 11.15)"
      handedness: "all right-handed"
      language: "English"
    statistics:
      threshold: "uncorrected voxel-wise p < 0.05"
      effect_size: "t(51) = 3.674 (LV covariate), t(51) = 2.786 (LV + WPM covariates)"
      p_value: "< 0.001"
    confounders_controlled:
      - "lesion volume"
      - "speech rate (words per minute)"
    confounders_not_controlled: []
    region_definition:
      kind: atlas
      atlas: "Johns Hopkins University atlas (Faria et al., 2012)"
      description: "pSTG/MTG ROI combining the posterior superior temporal gyrus and middle temporal gyrus."
    imaging_details:
      field_strength: "not_reported"
      preprocessing_pipeline: "warped to standard space"
      reference_space: "MNI152"
      atlases_used: ["Johns Hopkins University atlas"]
      coordinates_reported:
        - region: "Posterior superior temporal gyrus and sulcus"
          mni: [-47, -45, 11]
    author_limitations:
      - "Omitting subjects with low speech output likely precludes analysis of patients with both severe agrammatic and nonfluent speech."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 216"
      confidence: high
      flags: ["cohort overlaps with @Fridriksson2018 (USC/MUSC Aphasia Lab)"]
    source_passages:
      - section: "Results"
        page: 216
        quote: "PARAGRAMMATISM was significantly associated with damage to pSTG/MTG, t(51) = 3.674, p < 0.001... These results also held when adding speech rate as a covariate: PARAGRAMMATISM was significantly associated with damage to pSTG/MTG, t(51) = 2.786, p = 0.004"
        supports: claim
      - section: "Procedure"
        page: 210
        quote: "All subjects had a single ischemic stroke to the left hemisphere at least six months prior to study inclusion and were also premorbidly right-handed"
        supports: sample
      - section: "ROI Analyses"
        page: 215
        quote: "The left posterior superior and middle temporal gyri (pSTG/MTG) ROI was created by combining the posterior superior temporal gyrus and middle temporal gyrus."
        supports: region_definition
      - section: "Discussion"
        page: 222
        quote: "Omitting subjects with low speech output also likely precludes analysis of patients with both severe agrammatic and nonfluent speech."
        supports: limitation
---
