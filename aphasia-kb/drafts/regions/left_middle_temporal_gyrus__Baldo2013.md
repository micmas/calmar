---
schema_version: 2.6
id: left_middle_temporal_gyrus
name: "Left Middle Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: semantics
    target_kind: impairment
    claim: "Damage to the left mid-posterior middle temporal gyrus is critically associated with the ability to retrieve a name associated with an object (lexical-semantic retrieval)."
    direction: likely
    relationship: causal
    citation: "@Baldo2013"
    method: VLSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 96
      population: "left hemisphere stroke"
      time_post_onset: "at least 10 months post-injury"
      phase: chronic
      age_range: "mean 60.0 years (SD 11.2, range 31-84)"
      handedness: "right-handed"
      language: "native English speaker"
    statistics:
      threshold: "permutation testing (n = 1,000) with alpha set at .05"
      effect_size: "max t-value 6.06"
      p_value: ".05"
    confounders_controlled:
      - "speech fluency"
      - "visual recognition"
      - "age"
      - "education"
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "Left mid-posterior MTG (BA 21 and 37) and underlying white matter."
    imaging_details:
      field_strength: "1.5T"
      modalities:
        - modality: T1
          sequence: "Spoiled Gradient Recall (SPGR)"
          voxel_size_mm: [0.94, 1.3, 0.94]
          TR_ms: 15
          TE_ms: 4.47
      preprocessing_pipeline: "MRIcro tracing + SPM2 nonlinear spatial normalization with cost function masking"
      reference_space: MNI152
      atlases_used: ["Brodmann", "AAL"]
      coordinates_reported:
        - region: "white matter medial to posterior MTG"
          mni: [-46, -48, 0]
    author_limitations:
      - "Lesion reconstruction methods have limitations and some dysfunctional tissue may not be registered, especially in very large lesions."
      - "Lesion coverage did not include the entire left temporal pole, only superior portions."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 5"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 5
        quote: "When we re-ran the VLSM analysis with overall speech fluency as a covariate, the significant voxels were restricted primarily to the mid- to posterior portion of the MTG (BA 21 and 37), again with some extension into the white matter just medial to the MTG"
        supports: claim
      - section: "Methods"
        page: 3
        quote: "The study sample included 96 participants (21 female) who had suffered a single LH stroke. Study criteria included being a native English speaker, right-handed, and in the chronic phase of stroke (at least 10 months post-injury)"
        supports: sample
      - section: "Lesion analysis"
        page: 4
        quote: "To determine the anatomic correlates of picture naming on the BNT, we applied VLSM analyses to the lesion and behavioral data"
        supports: method
      - section: "Lesion analysis"
        page: 4
        quote: "a statistical threshold cut-off (t-value) was determined based on permutation testing (n = 1,000) with alpha set at .05"
        supports: statistics
      - section: "Lesion analysis"
        page: 4
        quote: "In addition to the primary VLSM analysis of spontaneous naming on the BNT, we ran additional VLSM analyses using patients' speech fluency and BNT recognition scores as covariates."
        supports: confounders
      - section: "Brain imaging"
        page: 3
        quote: "T1-weighted images were acquired with a Spoiled Gradient Recall (SPGR) sequence (TR/TE = 15/4.47 msec, FOV = 240 mm, 256 x 256 imaging matrix, flip angle = 35, .94 x 1.3 x .94 mm3 voxels, 212 coronal slices)."
        supports: imaging_details
      - section: "Brain imaging"
        page: 3
        quote: "The lesions were traced directly on the patient's T1 digital MRI image using MRIcro (Rorden and Brett, 2000) and then registered with the MNI template using the standard nonlinear spatial normalization procedure from SPM2"
        supports: imaging_details
      - section: "Brain imaging"
        page: 4
        quote: "It should be noted that lesion reconstruction methods have limitations and that in some cases, there is likely lesioned/dysfunctional tissue that is not registered with these techniques, especially in the case of patients with very large lesions"
        supports: limitation
---
