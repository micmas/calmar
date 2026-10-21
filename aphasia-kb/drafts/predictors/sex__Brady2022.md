---
schema_version: 2.3
id: sex
name: "Sex"
kind: predictor
predictor_type: demographic
short_definition: "The biological sex of the patient."
units: "category"
typical_range: "male, female"
direction_of_severity: not_applicable
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Males achieve greatest overall-language and auditory comprehension gains with high-intensity SLT (>9 h/week), while females achieve greatest gains with low-intensity SLT (<2 h/week)."
    direction: likely
    relationship: responder
    citation: "@Brady2022"
    method: meta-analysis
    design: meta-analysis
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 959
      population: "stroke-related aphasia"
      time_post_onset: not_reported
      age_range: not_reported
      handedness: not_reported
      language: "English predominant"
    statistics:
      threshold: "95% CI"
      effect_size: "not_reported"
    confounders_controlled: ["age", "aphasia severity", "time post-onset"]
    confounders_not_controlled: []
    author_limitations:
      - "Risk of false negatives and positives due to hypothesis-generating approach."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 5"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 5
        quote: "Males' greatest gains were associated with SLT of moderate (functional communication; 3-to-4 h/weekly) or high intensity (overall-language and auditory comprehension; (> 9 h/weekly) compared to females for whom the greatest gains were associated with lower-intensity SLT (< 2 SLT-h/weekly)."
        supports: claim
      - section: "Methods"
        page: 5
        quote: "We dichoto-mized IPD based on key demographic and clinical data; males and females..."
        supports: sample
      - section: "Discussion"
        page: 9
        quote: "Our statistical inferencing, hypothesis generating approach carries a risk of false nega-tive and positive findings."
        supports: limitation
---
