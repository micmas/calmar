---
schema_version: 2.3
id: time_post_onset
name: "Time Post-Onset"
kind: predictor
predictor_type: clinical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
findings:
  - id: f1
    target: fluency
    target_kind: impairment
    claim: "Time post-stroke is the most significant single predictor of speech production recovery."
    direction: likely
    relationship: correlational
    citation: "@Hope2013"
    method: MLPA
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 270
      population: "stroke patients"
      time_post_onset: "less than a month to more than 30 years"
      age_range: "20 to 90 years"
      handedness: "242 right handed"
      language: "English"
    statistics:
      threshold: "p < 0.001"
      effect_size: "R2 = 0.59 (as part of best subset)"
    confounders_controlled: ["lesion volume", "lesion site"]
    confounders_not_controlled: []
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, Section 3.5"
      confidence: high
      flags: ["target fluency used as proxy for composite speech production score"]
    source_passages:
      - section: "Results"
        page: 5
        quote: "The best subset included 37 relevant predictors (R2 = 0.59, F = 38.38, p b 0.001), including time post-stroke (the most significant, single predictor)"
        supports: claim
      - section: "Method"
        page: 2
        quote: "This selection process left us with data from 270 patients"
        supports: sample
      - section: "Discussion"
        page: 8
        quote: "our preferred predictor configuration systematically under-estimates the severity of the impairments suffered by the most impaired patients"
        supports: limitation
    author_limitations:
      - "The model systematically underestimates severity for the most impaired patients."
---
