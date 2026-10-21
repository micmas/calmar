---
schema_version: 2.3
id: time_post_onset
name: "Time Post-Onset"
kind: predictor
predictor_type: clinical
short_definition: "The duration of time elapsed since the stroke event."
units: "months"
typical_range: "0-100+ months"
direction_of_severity: not_applicable
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Participants within 3 months of onset achieve greatest overall-language gains with low-intensity SLT (<=2 h/week), whereas those >3 months post-onset achieve greatest gains with moderate-intensity SLT (3-4 h/week)."
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
      time_post_onset: "dichotomized at 3 months"
      age_range: not_reported
      handedness: not_reported
      language: "English predominant"
    statistics:
      threshold: "95% CI"
      effect_size: "not_reported"
    confounders_controlled: ["age", "sex", "aphasia severity"]
    confounders_not_controlled: []
    author_limitations:
      - "Spontaneous recovery may impact treatment gains observed, with median overall-language gains higher for the early-rehabilitation subgroup."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 5"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 5
        quote: "Participants <= 3 months post-onset demonstrated greatest overall-language gains for SLT at low intensity/moderate dosage (<= 2 SLT-h/week...); for those > 3 months, post-stroke greatest gains were associated with moderate-intensity/high-dosage SLT (3-4 SLT-h/week...)."
        supports: claim
      - section: "Methods"
        page: 5
        quote: "We dichoto-mized IPD based on key demographic and clinical data... rehabilitation timing after aphasia onset (early <= 3 months and late > 3 months)."
        supports: sample
      - section: "Discussion"
        page: 9
        quote: "We acknowledge that spontaneous recovery may also impact on treatment gains observed, with median overall-language gains higher for the early-rehabilitation subgroup than the late-rehabilitation group."
        supports: limitation
---
