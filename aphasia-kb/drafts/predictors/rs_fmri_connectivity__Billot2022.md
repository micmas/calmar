---
schema_version: 2.3
id: rs_fmri_connectivity
name: "Resting-State fMRI Connectivity"
kind: predictor
predictor_type: imaging_metric
short_definition: "Bivariate Fisher-transformed Pearson correlations between anatomic regions of interest during resting state."
units: "Fisher-z correlation"
typical_range: "not_reported"
direction_of_severity: not_applicable
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
findings:
  - id: f1
    target: rehabilitation_response
    target_kind: prognosis
    claim: "Resting-state functional connectivity independently predicts responsiveness to language rehabilitation in chronic stroke."
    direction: likely
    relationship: responder
    citation: "@Billot2022"
    method: MLPA
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 55
      population: "chronic left-hemisphere stroke aphasia"
      time_post_onset: "mean 59.0 months"
      age_range: "mean 58.8 years"
      handedness: not_reported
      language: not_reported
    statistics:
      threshold: not_reported
      effect_size: "SVM F1 = 0.812; RF F1 = 0.87"
      p_value: not_reported
    confounders_controlled: ["demographics", "structural imaging", "behavioral scores"]
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "Bivariate correlations between 50 AAL regions of interest."
    imaging_details:
      field_strength: "3T"
      reference_space: "MNI152"
      atlases_used: ["AAL"]
      preprocessing_pipeline: "fMRIPrep v1.4.1 + CONN toolbox"
    author_limitations:
      - "Small sample size may lead to less accurate results when using machine learning models on neuroimaging data."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 1610"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 5
        quote: "Notably, among SVM models trained on an individual feature set, aphasia severity (ie, AQ) and rs-fMRI connectivity (ie, RS) independently provided the best prediction performance scores, with an accuracy of 0.782 and 0.764 and an F1 score of 0.842 and 0.812, respectively."
        supports: statistics
      - section: "Results"
        page: 4
        quote: "Across random forest models, training on resting-state functional magnetic resonance imaging connectivity data yielded the best F1 score (F1=0.87)."
        supports: statistics
      - section: "Limitations"
        page: 7
        quote: "Previous studies demonstrated that small sample sizes can lead to less accurate results when using machine learning models on neuroimaging data to predict behavior."
        supports: limitation
---

Finding f1 highlights RS connectivity as a top individual predictor for both SVM and RF models.
