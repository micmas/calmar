---
schema_version: 2.3
id: left_middle_temporal_gyrus
name: "Left Middle Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
findings:
  - id: f1
    target: semantics
    target_kind: impairment
    claim: "Damage to the left posterior middle temporal gyrus is associated with impaired semantic processing."
    direction: likely
    relationship: causal
    citation: "@Alyahya2020"
    method: VBCM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 46
      population: "chronic left-hemisphere stroke"
      time_post_onset: "4-12 months"
      age_range: "mean 63.21 (SD 11.93)"
      handedness: "right-handed"
      language: "English"
    statistics:
      threshold: "P = 0.001 voxel-level, FWE P = 0.05 cluster-level"
      effect_size: "Z = 3.15"
    confounders_controlled: ["age", "education", "time since stroke onset"]
    confounders_not_controlled: []
    region_definition:
      kind: atlas
      atlas: "Harvard-Oxford"
      description: "Posterior middle temporal gyrus"
    imaging_details:
      field_strength: "3.0 T"
      reference_space: "MNI"
      atlases_used: ["Harvard-Oxford"]
      preprocessing_pipeline: "SPM8"
    author_limitations:
      - "White matter tracts were descriptive based on atlas overlap rather than directly measured via DWI."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, Table 2"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 8
        quote: "the 'semantic processing' component correlated with the... posterior middle temporal gyrus"
        supports: claim
      - section: "Materials and methods"
        page: 4
        quote: "The unified PCA model was mapped onto brain lesions using a voxel-based correlational methodology (VBCM) (Tyler et al., 2005)."
        supports: method
      - section: "Discussion"
        page: 12
        quote: "it must be acknowledged that white matter tracts described in this study are descriptive... rather than directly measured using diffusion-weighted imaging."
        supports: limitation
---
