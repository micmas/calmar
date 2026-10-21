---
schema_version: 2.3
id: age
name: "Age"
kind: predictor
predictor_type: demographic
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
short_definition: "Age of the patient at the time of stroke."
units: "years"
findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Older age is associated with worse language recovery (lower WAB-R AQ) at 6 months post-stroke."
    direction: unlikely
    relationship: correlational
    citation: "@Forkel2014"
    method: tractography
    design: longitudinal
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 16
      population: "left hemisphere stroke patients with aphasia"
      time_post_onset: "baseline within 2 weeks; follow-up at 6 months"
      age_range: "28-87 years"
      handedness: "all right-handed"
      language: "native English speaker"
    statistics:
      threshold: "P = 0.010"
      effect_size: "beta = -0.678"
      p_value: 0.01
    confounders_controlled:
      - "sex"
      - "lesion size"
      - "right long segment volume"
    confounders_not_controlled: []
    region_definition:
      kind: not_reported
      description: "Patient age in years."
    author_limitations:
      - "The sample was a selected group able to tolerate long MRI scans in the acute stage of stroke."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 2032"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 2032
        quote: "For the right hemisphere, age [beta = -0.678, t(-3.087), P = 0.010] and volume of the long segment of the arcuate fasciculus [beta = 0.730, t(2.732), P = 0.020] were predictors of longitudinal aphasia severity."
        supports: claim
      - section: "Materials and methods"
        page: 2029
        quote: "Sixteen patients (10 males; mean age 60 +/- 17 years, range 28-87 years) underwent post stroke language assessment with the Revised Western Aphasia Battery and neuroimaging scanning within a fortnight from symptoms onset."
        supports: sample
      - section: "Discussion"
        page: 2036
        quote: "our observations reflect results derived from a selected group of patients that were able to tolerate a 45-min MRI scanning session in the acute stage of stroke."
        supports: limitation
---

# Age

Findings regarding the predictive value of age on aphasia recovery.
