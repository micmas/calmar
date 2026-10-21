---
schema_version: 2.3
id: education
name: "Education"
kind: predictor
predictor_type: demographic
short_definition: "The number of years of formal education completed by the patient."
units: "years"
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
findings:
  - id: f1
    target: alexia
    target_kind: impairment
    claim: "Years of education did not significantly predict oral reading performance in persons with chronic aphasia and alexia."
    direction: no_effect
    relationship: correlational
    citation: "@Brookshire2014"
    method: behavioral_only
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 67
      population: "persons with chronic aphasia and alexia"
      time_post_onset: ">= 6 months"
      age_range: "mean 62.02 (SD 13.20)"
      handedness: "91 R, 6 L, 2 A"
      language: "English"
    statistics:
      threshold: "p > .05"
      effect_size: "p = .07 (total), .14 (lexical), .06 (sublexical)"
      p_value: ".06 to .14"
    confounders_controlled: ["WAB-AQ score"]
    confounders_not_controlled: ["motor speech impairments"]
    region_definition:
      kind: not_reported
      description: "demographic predictor"
    author_limitations:
      - "The group may have lacked enough variability in years of education (97% had at least high school education) to detect an effect."
      - "The finding is specific to the 52 reading items on the SAPA."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 11"
      confidence: high
      flags: ["new predictor id: education"]
    source_passages:
      - section: "Results - Predictors of oral reading performance"
        page: 11
        quote: "Education, on the other hand, was not uniquely predictive of total reading, lexical reading, or sublexical reading, p = .07, p = .14, p = .06, respectively."
        supports: claim
      - section: "Results - Predictors of oral reading performance"
        page: 11
        quote: "Education, on the other hand, was not uniquely predictive of total reading, lexical reading, or sublexical reading, p = .07, p = .14, p = .06, respectively."
        supports: statistics
      - section: "Discussion"
        page: 14
        quote: "it is possible that our group of PWA and alexia did not have enough variability in their years of education for this variable to significantly predict reading."
        supports: limitation
---

Finding from Brookshire et al. (2014) that education does not predict reading performance in this specific cohort.
