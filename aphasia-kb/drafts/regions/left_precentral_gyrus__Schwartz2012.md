---
schema_version: 2.3
id: left_precentral_gyrus
name: "Left Precentral Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
findings:
  - id: f1
    target: phonological_production
    target_kind: impairment
    claim: "Damage to the left precentral gyrus is associated with increased phonological errors in object naming."
    direction: likely
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
      effect_size: "t = 5.17"
    confounders_controlled: []
    confounders_not_controlled: ["lesion volume"]
    region_definition:
      kind: data_driven_cluster
      description: "Voxel-based cluster in the inferior portion of the precentral gyrus."
    imaging_details:
      reference_space: MNI152
      atlases_used: ["AAL"]
      preprocessing_pipeline: "Symmetric diffeomorphic registration (ANTS) to MNI Colin27"
      coordinates_reported:
        - region: "precentral gyrus"
          mni: [-62, -16, 11]
    author_limitations:
      - "Spatial coherence problem limits the ability to detect differences between positively correlated regions."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 3804"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 3804
        quote: "The voxel with the highest t-value (t = 5.17) was located in the inferior portion of the precentral gyrus (MNI x = -62, y = -16, z = 11)."
        supports: claim
      - section: "Materials and methods"
        page: 3801
        quote: "Of the 142 individuals enrolled, 106 qualified for the current study."
        supports: sample
      - section: "Discussion"
        page: 3811
        quote: "the spatial coherence problem sets limits on what VLSM can tell about interregional differences"
        supports: limitation
---
