---
schema_version: 2.6
id: left_superior_temporal_gyrus
name: "Left Superior Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: semantics
    target_kind: impairment
    claim: "Overall picture-naming performance on the BNT is associated with a network including the left superior temporal gyrus, though this association is reduced when controlling for speech production."
    direction: likely
    relationship: causal
    citation: "@Baldo2013"
    method: VLSM
    design: cross-sectional
    strength: moderate
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
      effect_size: "max t-value 9.21"
      p_value: ".05"
    confounders_controlled: ["age", "education"]
    confounders_not_controlled: ["speech fluency", "visual recognition"]
    region_definition:
      kind: data_driven_cluster
      description: "Left superior temporal gyrus (STG) as part of a larger network including MTG and inferior parietal cortex."
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
    author_limitations:
      - "Lesion reconstruction methods have limitations and some dysfunctional tissue may not be registered, especially in very large lesions."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 5"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 5
        quote: "The map revealed significant foci primarily in the anterior, middle, and posterior portions of the left MTG and STG, as well as the underlying white matter."
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
      - section: "Brain imaging"
        page: 3
        quote: "T1-weighted images were acquired with a Spoiled Gradient Recall (SPGR) sequence (TR/TE = 15/4.47 msec, FOV = 240 mm, 256 x 256 imaging matrix, flip angle = 35, .94 x 1.3 x .94 mm3 voxels, 212 coronal slices)."
        supports: imaging_details
      - section: "Brain imaging"
        page: 4
        quote: "It should be noted that lesion reconstruction methods have limitations and that in some cases, there is likely lesioned/dysfunctional tissue that is not registered with these techniques, especially in the case of patients with very large lesions"
        supports: limitation
---
