---
schema_version: 2.3
id: lesion_volume
name: "Lesion Volume"
kind: predictor
predictor_type: imaging_metric
short_definition: "The total volume of the brain lesion, typically measured in cubic centimeters (cc)."
units: "cc"
typical_range: "5.38–376.12 cc"
direction_of_severity: higher_is_worse
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Overall lesion size is a significant predictor of general aphasia severity (WAB-AQ) and object naming (PNT) accuracy."
    direction: likely
    relationship: correlational
    citation: "@Thye2018"
    method: VLSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 128
      population: "individuals with aphasia secondary to left hemisphere stroke"
      time_post_onset: "at least 1 month post onset"
      age_range: "26–79"
      handedness: "premorbidly right handed"
      language: "English as the primary language"
    statistics:
      threshold: "p < .01"
      effect_size: "WAB AQ R2=31%; PNT R2=21%"
    confounders_controlled: []
    confounders_not_controlled: []
    author_limitations:
      - "The modest amount of variance in deficit severity explained by the models represents a lower bound on what can be accomplished with simple models based on lesion size and location alone."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 6"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 6
        quote: "For both VLSM and SCCAN, lesion size alone was a significant predictor of PNT accuracy, WAB AQ, Semantics, and Speech Production (p < .01)."
        supports: claim
      - section: "Results"
        page: 6
        quote: "The largest percentage of the variance explained by lesion size was seen for the broad deficit measures: WAB AQ (31%) and PNT (21%)."
        supports: statistics
      - section: "General discussion"
        page: 9
        quote: "As a result, the modest amount of variance in deficit severity explained by the models represents a lower bound on what can be accomplished with simple models based on lesion size and location alone."
        supports: limitation

  - id: f2
    target: severity_metric
    target_kind: predictor
    claim: "Lesion size is a stronger predictor of broad language deficits (WAB-AQ, PNT) than of specific functional language systems (Speech Production, Speech Recognition)."
    direction: likely
    relationship: correlational
    citation: "@Thye2018"
    method: VLSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 128
      population: "individuals with aphasia secondary to left hemisphere stroke"
      time_post_onset: "at least 1 month post onset"
      age_range: "26–79"
      handedness: "premorbidly right handed"
      language: "English as the primary language"
    statistics:
      threshold: "p < .01"
      effect_size: "Speech Recognition R2=0.1%"
    confounders_controlled: []
    confounders_not_controlled: []
    author_limitations:
      - "The modest amount of variance in deficit severity explained by the models represents a lower bound on what can be accomplished with simple models based on lesion size and location alone."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 6"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 6
        quote: "across both types of LSM, lesion size accounted for 10%, 8%, and 0.1% of the variance in scores on Semantics, Speech Production, and Speech Recognition, respectively, suggesting that lesion size did not explain as much variability in performance for these functional language systems."
        supports: claim
      - section: "General discussion"
        page: 9
        quote: "As a result, the modest amount of variance in deficit severity explained by the models represents a lower bound on what can be accomplished with simple models based on lesion size and location alone."
        supports: limitation
---

Findings from Thye & Mirman (2018) regarding the predictive power of total lesion volume across different types of language deficits.
