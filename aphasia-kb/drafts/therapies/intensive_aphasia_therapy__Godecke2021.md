---
schema_version: 2.6
id: intensive_aphasia_therapy
name: "Intensive Aphasia Therapy (Early Acute)"
kind: therapy
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
short_description: "High-intensity aphasia rehabilitation delivered within the first 14 days post-stroke."
targets_impairments: ["global_aphasia", "brocas_aphasia", "wernickes_aphasia", "anomic_aphasia"]

findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Early intensive aphasia therapy (approx. 5h/week) starting within 14 days of stroke does not significantly improve communication recovery at 12 weeks compared to usual care."
    direction: no_effect
    relationship: responder
    citation: "@Godecke2021"
    method: clinical_RCT
    design: RCT
    strength: strong
    evidence_quality: RCT
    sample:
      n: 245
      population: "acute stroke patients with aphasia"
      time_post_onset: "within 14 days of stroke onset"
      phase: early_subacute
      age_range: "mean 75-76 years"
      handedness: not_reported
      language: "English"
    statistics:
      threshold: "p = 0.59"
      effect_size: "difference -1.8 (95% CI -8.7 to 5.0) in %MPR"
    confounders_controlled: ["baseline WAB-R AQ", "baseline NIHSS", "hospital site"]
    confounders_not_controlled: []
    region_definition:
      kind: not_reported
      description: "behavioural-only treatment-efficacy finding — no specific brain region"
    imaging:
      none
    imaging_details:
      reference_space: not_reported
      atlases_used: []
    author_limitations:
      - "The increase in usual care service delivery in this trial compared to earlier pilots may have masked the effect of high-intensity therapy."
      - "It remains unclear whether a much higher dose (e.g., 100h over 12 weeks) would be more efficacious."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 8"
      confidence: high
      flags: []
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "Early, intensive aphasia therapy did not improve communication recovery within 12 weeks post stroke compared to usual care."
        supports: claim
      - section: "Methods - Participants"
        page: 3
        quote: "Participants were aged over 18 years and admitted to hospital with an acute stroke, resultant acute aphasia of any type, within 14 days of stroke onset."
        supports: sample
      - section: "Methods - Study design"
        page: 3
        quote: "A phase three, multicenter, randomized controlled trial... blinded outcomes assessed at 12 (primary outcome) and 26 weeks post stroke."
        supports: method
      - section: "Results"
        page: 8
        quote: "The between-group difference of -1.8 (favoring control; (95% CI -8.7-5.0) was not significant (p = 0.59; Figure 2; Supplemental Table S3 for all group comparisons)."
        supports: statistics
      - section: "Statistical analysis"
        page: 4
        quote: "...using a linear mixed model which controlled for baseline WAB-R AQ and baseline National Institute of Health Stroke Scale (NIHSS) as fixed effects and hospital site as a random effect."
        supports: confounders
      - section: "Discussion"
        page: 9
        quote: "In addition, we found a considerable increase in the amount of aphasia therapy provided as usual care... compared with the results of our pilot trial."
        supports: limitation
      - section: "Discussion"
        page: 12
        quote: "...it remains unclear whether a much higher dose, for example, 100 h over 12 weeks, would be more efficacious."
        supports: limitation
---

# Notes
This is a high-powered Phase III RCT (VERSE) challenging the 'more is better' hypothesis in the very early acute phase of recovery.
