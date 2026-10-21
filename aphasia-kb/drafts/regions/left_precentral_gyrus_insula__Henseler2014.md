---
schema_version: 2.3
id: left_precentral_gyrus_insula
name: "Left Precentral Gyrus of the Insula"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: form_to_articulation
    target_kind: impairment
    claim: "Damage to the left insula and adjacent opercular cortex is associated with impaired articulation and prosody in spontaneous speech."
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
      description: "VLSM cluster associated with AAT articulation and prosody score."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "SPM8 unified segmentation + cost function masking"
      reference_space: MNI152
      atlases_used: []
    author_limitations:
      - "Patients with chronic aphasia modify communicative behaviour over time and the network will show partial functional adaptation."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 5"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 5
        quote: "performance on the level 'articulation and prosody' in spontaneous speech significantly correlated with damage to the left insula and the adjacent opercular cortex, and the putamen"
        supports: claim
      - section: "Materials and methods"
        page: 3
        quote: "One hundred and two patients fulﬁlled these criteria."
        supports: sample
      - section: "Limitations and perspectives"
        page: 12
        quote: "patients with chronic aphasia modify communicative behaviour over time and the network affording linguistic processing will show partial functional adaptation to the lesion"
        supports: limitation
---
