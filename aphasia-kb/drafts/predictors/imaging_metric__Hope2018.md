---
schema_version: 2.3
id: imaging_metric_structural_disconnection
name: "Structural Disconnection (Network Modification)"
kind: predictor
predictor_type: imaging_metric
short_definition: "The degree of white matter connectivity disruption between cortical regions inferred from T1-weighted MRI using the Network Modification toolbox."
units: "mean disconnection index"
typical_range: "not_reported"
direction_of_severity: "higher_is_worse"
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21

findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Structural connectivity disruption does not provide unique prognostic information for language outcomes beyond that provided by regional lesion load."
    direction: no_effect
    relationship: correlational
    citation: "@Hope2018"
    method: MLPA
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 818
      population: "stroke patients from the PLORAS database"
      time_post_onset: "mean 58 months (SD 66 months)"
      age_range: "mean 55 years (SD 13 years)"
      handedness: "98 patients left-handed or ambidextrous"
      language: "not_reported"
    statistics:
      threshold: "one-tailed variance test"
      effect_size: "all p > 0.2"
      p_value: "not_reported"
    confounders_controlled:
      - "lesion volume"
      - "time post-stroke"
      - "age at stroke"
      - "pre-stroke handedness"
      - "bilingualism"
      - "lesion load (regional)"
    confounders_not_controlled: []
    region_definition:
      kind: atlas
      atlas: "Automatic Anatomical Labelling (AAL)"
      description: "116 grey-matter regions defined by the AAL atlas."
    imaging_details:
      field_strength: "not_reported"
      acquisition:
        sequence: "T1-weighted MRI"
      preprocessing_pipeline: "SPM2012 unified segmentation optimized for focal lesions"
      reference_space: "MNI152"
      atlases_used: ["AAL"]
    author_limitations:
      - "Connectivity disruption was inferred from T1-weighted MRI rather than measured directly with subject-specific diffusion data."
      - "The use of binary lesion segmentation may diverge from manual segmentation gold standards."
      - "Results may be dependent on the choice of brain parcellation (AAL atlas)."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, pages 4-5"
      confidence: high
      flags: ["cohort overlaps with @White2024 (PLORAS database); flag for downstream double-counting risk in interpret_overlap()"]
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "We found no consistent evidence that connectivity disruption data in these models improved our ability to predict any language score."
        supports: claim
      - section: "Methods - Patient data"
        page: 2
        quote: "Our patient data were extracted from our PLORAS database (Seghier et al., 2016)..."
        supports: sample
      - section: "Methods - Structural brain imaging data"
        page: 2
        quote: "We examined models driven by both lesion load in these regions... and by the disconnection of the white matter connections between them... calculated via the Network Modification toolbox."
        supports: method
      - section: "Results - Predicting all the language scores"
        page: 4
        quote: "we find no evidence that the use of connectivity disruption data significantly improves our ability to predict any language score (all p > 0.2)."
        supports: statistics
      - section: "Discussion"
        page: 5
        quote: "One caveat to these results is that we have inferred connectivity disruption from T1-weighted MRI, rather than measuring it \"directly\" with subject-specific diffusion data."
        supports: limitation
---

Notes: This study specifically tests whether structural disconnection (as a predictor) adds value over regional lesion load. It concludes that it does not, likely because the two are highly correlated (r = -0.94 for first principal components).
