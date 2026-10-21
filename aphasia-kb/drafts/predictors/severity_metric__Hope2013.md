---
schema_version: 2.3
id: severity_metric
name: "Aphasia Severity Metric"
kind: predictor
predictor_type: behavioural
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
findings:
  - id: f1
    target: prognosis
    target_kind: prognosis
    claim: "A combination of baseline lesion site and time post-stroke accurately predicts future speech production scores."
    direction: likely
    relationship: correlational
    citation: "@Hope2013"
    method: MLPA
    design: longitudinal
    strength: strong
    evidence_quality: cohort
    sample:
      n: 38
      population: "stroke patients assessed more than once"
      time_post_onset: "less than a month to more than 30 years"
      age_range: "20 to 90 years"
      handedness: "not_reported"
      language: "English"
    statistics:
      threshold: "p < 0.001"
      effect_size: "R2 = 0.84"
    confounders_controlled: ["baseline lesion site", "time post-stroke"]
    confounders_not_controlled: []
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, Section 3.7"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 5
        quote: "our learner can predict the later assessment scores very accurately (R2 = 0.84, F = 225.00, p b 0.001)"
        supports: claim
      - section: "Results"
        page: 5
        quote: "38 of the 270 patients in our original dataset were assessed more than once"
        supports: sample
      - section: "Discussion"
        page: 8
        quote: "our preferred predictor configuration systematically under-estimates the severity of the impairments suffered by the most impaired patients"
        supports: limitation
    author_limitations:
      - "The model systematically underestimates severity for the most impaired patients."
---
