---
schema_version: 2.3
id: left_superior_temporal_gyrus
name: "Left Superior Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: form_to_meaning
    target_kind: impairment
    claim: "Damage to the anterior and middle left superior temporal gyrus and left anterior IFG is associated with impaired language comprehension."
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
      description: "VLSM cluster associated with AAT language comprehension subtest."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "SPM8 unified segmentation + cost function masking"
      reference_space: MNI152
      atlases_used: []
    author_limitations:
      - "The rather coarse rating of syntactic abilities in the AAT certainly does not allow us to disentangle differential contributions."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 6"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 6
        quote: "Critical areas included the anterior and middle part of the left superior temporal gyrus and in the left anterior inferior frontal gyrus"
        supports: claim
      - section: "Materials and methods"
        page: 3
        quote: "One hundred and two patients fulﬁlled these criteria."
        supports: sample
      - section: "Results"
        page: 6
        quote: "The rather coarse rating of syntactic abilities in the AAT certainly does not allow us to disentangle differential contributions"
        supports: limitation
---
