---
schema_version: 2.3
id: left_superior_temporal_gyrus_wernickes
name: "Left Superior Temporal Gyrus (Wernicke's Area)"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: wernickes_aphasia
    target_kind: impairment
    claim: "Damage to the left posterior and anterior temporal and parietal cortex is associated with Wernicke's aphasia."
    direction: likely
    relationship: causal
    citation: "@Henseler2014"
    method: VLSM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 102
      population: "chronic left-hemisphere ischemic stroke"
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
      description: "VLSM cluster associated with Wernicke's syndrome probability."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "SPM8 unified segmentation + cost function masking"
      reference_space: MNI152
      atlases_used: []
    author_limitations:
      - "Chronic aphasia may favour larger lesions, which may sharpen the distinction between syndromes."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 5"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 5
        quote: "lesions associated with Wernicke's aphasia were located in the left posterior and anterior temporal and parietal cortex (including Wernicke's area)."
        supports: claim
      - section: "Materials and methods"
        page: 3
        quote: "One hundred and two patients fulﬁlled these criteria."
        supports: sample
      - section: "Discussion"
        page: 9
        quote: "the fact that we investigated chronic aphasia may favour larger lesions to contribute to the overall results and may sharpen the distinction"
        supports: limitation
---
