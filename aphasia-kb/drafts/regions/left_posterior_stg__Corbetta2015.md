---
schema_version: 2.6
id: left_posterior_stg
name: "Left Posterior Superior Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Damage to the left posterior superior temporal gyrus (Wernicke's area) is associated with language deficits in acute stroke."
    direction: likely
    relationship: causal
    citation: "@Corbetta2015"
    method: MLPA
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 132
      population: "first-time stroke patients"
      time_post_onset: "mean 13 +/- 4.9 days"
      phase: acute
      age_range: "median 54"
      handedness: not_reported
      language: not_reported
    statistics:
      threshold: "z score of 2.5 and 10% of behavioral variance explained"
      effect_size: "44% of variance explained for language factor"
      p_value: not_reported
    confounders_controlled: ["lesion volume"]
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "Predictive weights from ridge regression back-projected to brain anatomy."
    imaging_details:
      field_strength: not_reported
      preprocessing_pipeline: "normalized to a standard brain atlas"
      reference_space: MNI152
      atlases_used: []
    author_limitations:
      - "The relatively small number of lesions that overlapped the same cortical location... renders the anatomo-clinical association in cortical regions less robust."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 933"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 933
        quote: "Language deficits were associated with damage to regions... classic language regions such as... left posterior superior (Wernicke), middle temporal gyrus..."
        supports: claim
      - section: "Results"
        page: 928
        quote: "Subjects (n = 172) with a first symptomatic stroke... n = 132 meeting post-enrollment inclusion criteria... acute neurobehavioral assessment (mean 13 +/- 4.9 days)"
        supports: sample
      - section: "Experimental Procedures"
        page: 939
        quote: "The voxel-wise relationship between lesion maps and behavioral scores for each domain was analyzed using a multivariate leave-one-out ridge regression machine learning algorithm"
        supports: method
      - section: "Results"
        page: 933
        quote: "the location of structural damage explains different amounts of variance for different behavioral factors: ... language (44%)"
        supports: statistics
      - section: "Discussion"
        page: 937
        quote: "A second limitation was the relatively small number of lesions that overlapped the same cortical location... it renders the anatomo-clinical association in cortical regions less robust."
        supports: limitation
---
