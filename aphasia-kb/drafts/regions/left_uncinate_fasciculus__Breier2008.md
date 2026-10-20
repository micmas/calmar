---
schema_version: 2.3
id: left_uncinate_fasciculus
name: "Left Uncinate Fasciculus"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
findings:
  - id: f1
    target: semantics
    target_kind: impairment
    claim: "No significant correlation was found between the integrity of the left uncinate fasciculus and naming deficits in this cohort."
    direction: no_effect
    relationship: correlational
    citation: "@Breier2008"
    method: DTI
    design: cross-sectional
    strength: weak
    evidence_quality: cohort
    sample:
      n: 20
      population: "chronic left-hemisphere stroke"
      time_post_onset: "mean 22 months"
      age_range: "38-77 years"
      handedness: "all premorbidly right handed"
      language: "not_reported"
    statistics:
      threshold: "P < 0.05"
      effect_size: "not_reported"
      p_value: "0.07"
    confounders_controlled:
      - "white matter disease"
    confounders_not_controlled: []
    region_definition:
      kind: manual_ROI
      description: "FA values determined for the UF in the left hemisphere."
    imaging_details:
      field_strength: "3T"
      modalities:
        - modality: DTI
          sequence: "single-shot spin-echo diffusion sensitized echo-planar imaging (EPI)"
          voxel_size_mm: [3, 3, 3]
          TR_ms: 6100
          TE_ms: 84
          n_directions: 21
          b_values: [1000]
      preprocessing_pipeline: "not_reported"
      reference_space: "not_reported"
      atlases_used: ["Mori et al. 2005"]
    author_limitations:
      - "This may have been due to lack of power and/or use of language tests that may not have been sensitive to more subtle semantic deficits."
      - "the UF may be better visualized in a plane other than the sagittal plane"
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 484"
      confidence: high
      flags: ["new_region_id: left_uncinate_fasciculus"]
    source_passages:
      - section: "Results"
        page: 484
        quote: "There were no significant findings for the UF (P 0.07)."
        supports: claim
      - section: "Discussion"
        page: 485
        quote: "This may have been due to lack of power and/or use of language tests that may not have been sensitive to more subtle semantic deficits."
        supports: limitation
---

Findings from Breier 2008 regarding the left uncinate fasciculus and its lack of correlation with naming.
