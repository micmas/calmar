---
schema_version: 2.3
id: left_supramarginal_gyrus_premotor
name: "Left Supramarginal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: phonological_production
    target_kind: impairment
    claim: "Damage to the left supramarginal gyrus is associated with impaired phonematic structure in spontaneous speech and impaired speech repetition."
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
      threshold: "FDR p < 0.01"
      effect_size: not_reported
    confounders_controlled: []
    confounders_not_controlled: ["lesion size"]
    region_definition:
      kind: data_driven_cluster
      description: "VLSM cluster associated with phonematic structure and repetition subtests."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "SPM8 unified segmentation + cost function masking"
      reference_space: MNI152
      atlases_used: []
    author_limitations:
      - "Performance in tests of speech repetition may also be influenced by impaired verbal working memory capacity."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, pages 5-6"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 5
        quote: "there was a significant association between behavioural impairment and damage to the left supramarginal gyrus"
        supports: claim
      - section: "Results"
        page: 6
        quote: "For 'speech repetition' damage to the left supramarginal gyrus and the left posterior superior temporal gyrus correlated with lesser performance."
        supports: claim
      - section: "Results"
        page: 6
        quote: "performance in tests of speech repetition in patients with left posterior superior temporal gyrus/supramarginal gyrus lesions may also be inﬂuenced by their impaired verbal working memory capacity."
        supports: limitation
---
