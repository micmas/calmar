---
schema_version: 2.3
id: left_posterior_stg
name: "Left Posterior Superior Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
findings:
  - id: f1
    target: phonological_production
    target_kind: impairment
    claim: "Damage to the left posterior superior temporal gyrus is not significantly associated with phonological errors in object naming."
    direction: no_effect
    relationship: causal
    citation: "@Schwartz2012"
    method: VLSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 106
      population: "chronic left-hemisphere stroke aphasia"
      age_range: "mean 58 (range 26-79)"
      handedness: "premorbid right-handed"
      language: "English"
    statistics:
      threshold: "FDR q = 0.01"
      effect_size: "not_reported"
    confounders_controlled: []
    confounders_not_controlled: ["lesion volume"]
    region_definition:
      kind: data_driven_cluster
      description: "Posterior superior temporal gyrus and sulcus."
    imaging_details:
      reference_space: MNI152
      atlases_used: ["AAL"]
      preprocessing_pipeline: "Symmetric diffeomorphic registration (ANTS) to MNI Colin27"
    author_limitations:
      - "Poor lesion coverage in the inferior temporal and fusiform gyri may have reduced power."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 3804"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 3804
        quote: "Critical to the study hypotheses, there were no voxel clusters in the posterior superior temporal gyrus or posterior superior temporal sulcus."
        supports: claim
      - section: "Materials and methods"
        page: 3801
        quote: "Of the 142 individuals enrolled, 106 qualified for the current study."
        supports: sample
      - section: "Discussion"
        page: 3811
        quote: "poor lesion coverage in the inferior temporal and fusiform gyri prevents us from addressing whether phonological errors in naming correlate with lesions in this basal temporal language area"
        supports: limitation
---
