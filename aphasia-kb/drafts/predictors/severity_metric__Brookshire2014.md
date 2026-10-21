---
schema_version: 2.3
id: severity_metric
name: "Aphasia Severity Metric"
kind: predictor
predictor_type: clinical
short_definition: "A general measure of aphasia severity, typically derived from a standardized battery."
assessment: ["WAB-R Aphasia Quotient"]
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
findings:
  - id: f1
    target: alexia
    target_kind: impairment
    claim: "Lower aphasia severity (higher WAB-AQ scores) significantly predicts better oral reading performance across total, lexical, and sublexical reading."
    direction: likely
    relationship: correlational
    citation: "@Brookshire2014"
    method: behavioral_only
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    instrument: "WAB-AQ"
    score_band: "all severities"
    interpretation: "Higher WAB-AQ scores (less severe aphasia) correlate with better reading accuracy."
    sample:
      n: 67
      population: "persons with chronic aphasia and alexia"
      time_post_onset: ">= 6 months"
      age_range: "mean 62.02 (SD 13.20)"
      handedness: "91 R, 6 L, 2 A"
      language: "English"
    statistics:
      threshold: "p < .001"
      effect_size: "beta = 0.76 (total), 0.76 (lexical), 0.56 (sublexical)"
      p_value: "<.001"
    confounders_controlled: ["years of education"]
    confounders_not_controlled: ["motor speech impairments"]
    region_definition:
      kind: not_reported
      description: "behavioral predictor"
    author_limitations:
      - "Retrospective design and convenience sample may limit generalizability."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 11"
      confidence: high
      flags: []
    source_passages:
      - section: "Results - Predictors of oral reading performance"
        page: 11
        quote: "Performance on WAB-AQ had a unique, positive effect on total reading, lexical reading, and sublexical reading."
        supports: claim
      - section: "Results - Predictors of oral reading performance"
        page: 11
        quote: "Holding years of education constant, the models predicted for every one-point increase on WAB-AQ, there is an expected 0.7% increase on total reading score, p < .001..."
        supports: statistics
      - section: "Discussion - Limitations"
        page: 14
        quote: "We employed a retrospective analysis of a convenience sample of individuals with chronic aphasia that may not have been fully representative of the population..."
        supports: limitation
---

Finding from Brookshire et al. (2014) that aphasia severity (WAB-AQ) predicts reading performance.
