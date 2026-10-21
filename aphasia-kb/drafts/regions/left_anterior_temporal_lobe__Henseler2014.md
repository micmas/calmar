---
schema_version: 2.3
id: left_anterior_temporal_lobe
name: "Left Anterior Temporal Lobe"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: anomic_aphasia
    target_kind: impairment
    claim: "Naming of compound nouns correlates with the integrity of the left anterior temporal lobe."
    direction: likely
    relationship: causal
    citation: "@Henseler2014"
    method: VLSM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 30
      population: "chronic left-hemisphere ischemic stroke (mildly affected subgroup)"
      time_post_onset: ">= 12 months"
      age_range: "mean 52 (SD 12)"
      handedness: "all right-handed"
      language: "native German"
    statistics:
      threshold: "FDR p < 0.05"
      effect_size: not_reported
    confounders_controlled: []
    confounders_not_controlled: ["lesion size"]
    region_definition:
      kind: data_driven_cluster
      description: "VLSM cluster associated with compound noun naming."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "SPM8 unified segmentation + cost function masking"
      reference_space: MNI152
      atlases_used: []
    author_limitations:
      - "Clinical judgement introduces a bias as these tests were administered to smaller subgroups of patients typically with mild or residual aphasia."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 6"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 6
        quote: "naming of compound when compared with single nouns correlated with relative integrity of the left anterior temporal lobe."
        supports: claim
      - section: "Results"
        page: 6
        quote: "Patients examined by these tests typically had a mild or residual aphasia"
        supports: limitation
---
