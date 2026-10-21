---
schema_version: 2.3
id: severity_metric
name: "Aphasia Severity Metric"
kind: predictor
predictor_type: behavioural
short_definition: "Overall measure of aphasia severity, typically assessed via standardized batteries."
assessment: ["Boston Naming Test (BNT)", "Boston Diagnostic Aphasia Examination (BDAE)"]
units: "percent correct"
typical_range: "0-100%"
direction_of_severity: lower_is_worse
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21

findings:
  - id: f1
    target: phonological_component_analysis
    target_kind: therapy
    claim: "Less severe initial naming impairment (higher BNT scores) is associated with a better response to Phonological Components Analysis (PCA) treatment."
    direction: likely
    relationship: responder
    citation: "@Leonard2008"
    method: behavioral_only
    design: case-series
    strength: moderate
    evidence_quality: cohort
    instrument: "BNT"
    score_band: "less severe"
    interpretation: "Higher baseline naming accuracy predicts better treatment gain."
    sample:
      n: 10
      population: "individuals with aphasia"
      time_post_onset: ">= 1 year"
      age_range: "mean 61.7 years"
      handedness: "all right-handed"
      language: "English-speaking"
    statistics:
      threshold: "p < .01, one-tailed"
      effect_size: not_reported
      p_value: ".01"
    confounders_controlled: []
    confounders_not_controlled: ["lesion volume", "age"]
    region_definition:
      kind: not_reported
      description: "behavioural predictor"
    imaging_details:
      reference_space: not_reported
      atlases_used: []
    author_limitations:
      - "Small sample size limits the power of the correlational analysis."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Relationships between pre-treatment tests and response to treatment, page 14"
      confidence: high
      flags: []
    source_passages:
      - section: "Relationships between pre-treatment tests and response to treatment"
        page: 14
        quote: "Significant correlations (p < .01, one-tailed) were found between response to treatment and scores on the BNT... A less severe naming impairment... resulted in better performance during treatment."
        supports: claim
      - section: "Participants"
        page: 4
        quote: "A total of 10 individuals with aphasia participated in this investigation"
        supports: sample
      - section: "Relationships between pre-treatment tests and response to treatment"
        page: 14
        quote: "it is acknowledged that due to the small sample size, the power of this analysis is limited."
        supports: limitation
---

Baseline naming severity (BNT) was a significant predictor of response to PCA treatment.
