---
schema_version: 2.3
id: left_precentral_gyrus
name: "Left Precentral Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: form_to_articulation
    target_kind: impairment
    claim: "Damage to the left lateral precentral gyrus is associated with a reduced diadochokinetic rate."
    direction: likely
    relationship: causal
    citation: "@Fridriksson2013"
    method: VBCM
    design: cross-sectional
    strength: weak
    evidence_quality: cohort
    sample:
      n: 64
      population: "chronic left hemisphere stroke"
      time_post_onset: "mean 39.86 months (SD 49.24)"
      age_range: "mean 61.6 years (SD 12.27)"
      handedness: not_reported
      language: not_reported
    statistics:
      threshold: "not significant at Bonferroni corrected alpha-level of 0.002"
      effect_size: "R2 = 0.16"
      p_value: "0.003"
    confounders_controlled: ["lesion size"]
    confounders_not_controlled: []
    region_definition:
      kind: atlas
      atlas: "Harvard-Oxford standard brain atlas"
      description: "Left lateral precentral gyrus defined by a probability threshold of 0.50."
    imaging_details:
      field_strength: "3T"
      reference_space: MNI152
      atlases_used: ["Harvard-Oxford"]
    author_limitations:
      - "Reduced diadochokinetic rate is not a measure that clearly adjudicates between those who do or do not have motor speech impairment."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 3454"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 3454
        quote: "Diadochokinetic rate was predicted by involvement of the lateral precentral gyrus, P = 0.003, R2 = 0.16... note that this model was not statistically significant at the Bonferroni corrected alpha-level of 0.002."
        supports: claim
---
