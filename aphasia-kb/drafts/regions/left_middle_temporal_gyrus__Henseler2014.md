---
schema_version: 2.3
id: left_middle_temporal_gyrus
name: "Left Middle Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: anomic_aphasia
    target_kind: impairment
    claim: "Integrity of the posterior middle temporal gyrus and left orbital IFG is critical for picture naming."
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
      description: "VLSM cluster associated with large picture naming battery."
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
        quote: "a large picture naming battery (170 items) suggests that integrity of the left orbital inferior frontal gyrus (Brodmann area 47) and the posterior middle temporal gyrus are most critical for naming"
        supports: claim
      - section: "Results"
        page: 6
        quote: "Patients examined by these tests typically had a mild or residual aphasia"
        supports: limitation
---
