---
schema_version: 2.6
id: severity_metric
name: "Aphasia Severity Metric"
kind: predictor
predictor_type: behavioural
short_definition: "A measure of overall aphasia severity based on standardized language batteries."
assessment: ["Quick Aphasia Battery (QAB)", "Western Aphasia Battery-Revised (WAB-R)"]
units: "score 0-10"
typical_range: "0-10 (lower = more severe)"
direction_of_severity: lower_is_worse
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Initial aphasia severity is a strong predictor of subsequent recovery trajectories, with larger improvements occurring in patients with lower initial scores."
    direction: likely
    relationship: correlational
    citation: "@Wilson2023"
    method: behavioral_only
    design: longitudinal
    strength: strong
    evidence_quality: cohort
    instrument: "Quick Aphasia Battery (QAB)"
    score_band: "all severities"
    interpretation: "Baseline severity determines the potential for gain."
    sample:
      n: 121
      population: "individuals with aphasia after left hemisphere stroke"
      time_post_onset: "1-5 days (T1) to 1 year (T4)"
      phase: longitudinal
      age_range: "mean 62.6 (SD 13.6)"
      handedness: "193 R; 20 L; 5 Am"
      language: "English"
    statistics:
      threshold: "P < 0.0001"
      effect_size: "explained 44.9% of the variance"
      p_value: "< 0.0001"
    confounders_controlled: ["lesion location", "lesion extent", "time point", "stroke type", "age", "sex", "handedness", "education"]
    confounders_not_controlled: []
    region_definition:
      kind: not_reported
      description: "behavioural-only predictor finding"
    author_limitations:
      - "Longitudinal data were acquired for only 121 (56%) of the individuals with aphasia."
      - "The QAB is a relatively brief battery and does not probe every aspect of language function."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results - Trajectories of recovery, page 1028"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 1028
        quote: "Recovery was strongly predicted by preceding score [chi2(2) = 133.6, P < 0.0001], with larger improvements taking place when preceding scores were lower"
        supports: claim
      - section: "Materials and methods"
        page: 1023
        quote: "A total of 316 patients were able to be tested within the first 5 days after stroke (Time 1, T1)... We obtained one or more follow-up time points for a total of 121 patients"
        supports: sample
      - section: "Statistical analysis"
        page: 1027
        quote: "We modelled change over time by fitting linear mixed-effects models using the 'fitlme' function in MATLAB."
        supports: method
      - section: "Results"
        page: 1028
        quote: "Together, these two factors explained an additional 44.9% of the variance compared to a model excluding these factors."
        supports: statistics
      - section: "Limitations"
        page: 1036
        quote: "Longitudinal data were acquired for only 121 (56%) of the individuals with aphasia."
        supports: limitation
---
