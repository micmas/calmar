---
schema_version: 2.3
id: left_anterior_arcuate_fasciculus
name: "Left Anterior Arcuate Fasciculus"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: fluency
    target_kind: impairment
    claim: "Damage to the anterior segment of the left arcuate fasciculus is the sole significant predictor of long-term speech production impairment when controlling for other left frontal regions."
    direction: likely
    relationship: causal
    citation: "@GajardoVidal2021"
    method: RLSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 134
      population: "left-hemisphere stroke patients"
      time_post_onset: "at least 3 months post-stroke"
      age_range: "31-87 years (mean 60)"
      handedness: "all right-handed"
      language: "native speaker of English"
    statistics:
      threshold: "p < 0.05"
      effect_size: "beta = -0.330"
      p_value: 0.008
    confounders_controlled:
      - "total lesion volume"
      - "months post-stroke"
      - "age at stroke"
      - "CAT semantic memory scores"
    confounders_not_controlled: []
    region_definition:
      kind: atlas
      atlas: "Natbrainlab"
      description: "Anterior segment of the arcuate fasciculus (aAF)."
    imaging_details:
      field_strength: "mixed (1.5T and 3T)"
      preprocessing_pipeline: "automated procedures reported in Seghier et al. (2008)"
      reference_space: MNI152
      atlases_used: ["Natbrainlab"]
    author_limitations:
      - "Estimating the effect of damage only in terms of lesion load in atlas-based regions of interest may therefore lead to false negative results."
      - "white matter lesions are likely to damage fibres with a range of different cortical projections."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 824"
      confidence: high
      flags: ["cohort overlaps with @White2024 (PLORAS database); flag for downstream double-counting risk."]
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "long-term speech production impairments (lasting beyond 3 months post-stroke) were solely predicted by the degree of damage to white matter, directly above the insula, in the vicinity of the anterior part of the arcuate fasciculus"
        supports: claim
      - section: "Materials and methods"
        page: 4
        quote: "These criteria were met by 134 left-hemisphere stroke patients, aged between 31 and 87 years (mean age = 60 years)."
        supports: sample
      - section: "Materials and methods"
        page: 6
        quote: "multiple regression on continuous measures of structural damage (i.e. percentage of damage to each area) and speech production abilities"
        supports: method
      - section: "Results"
        page: 8
        quote: "Across all eight anatomical predictors included in Model 2, only lesion load in aAF reached statistical significance (P = 0.008)."
        supports: statistics
      - section: "Materials and methods"
        page: 6
        quote: "All T1-weighted images were converted into a binary image of the lesion in MNI space, using automated procedures reported in Seghier et al. (2008)"
        supports: imaging_details
      - section: "Limitations and future directions"
        page: 12
        quote: "Estimating the effect of damage only in terms of lesion load in atlas-based regions of interest may therefore lead to false negative results."
        supports: limitation
---

Findings from @GajardoVidal2021 demonstrate that the anterior arcuate fasciculus is the primary driver of long-term speech production deficits in left frontal stroke, independent of Broca's area.
