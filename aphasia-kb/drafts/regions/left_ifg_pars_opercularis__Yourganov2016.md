---
schema_version: 2.3
id: left_ifg_pars_opercularis
name: "Left Inferior Frontal Gyrus Pars Opercularis"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: fluency
    target_kind: impairment
    claim: "Damage to the left inferior frontal gyrus pars opercularis is a significant predictor of speech fluency in chronic aphasia."
    direction: likely
    relationship: causal
    citation: "@Yourganov2016"
    method: MLPA
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 90
      population: "chronic left-hemisphere stroke aphasia"
      time_post_onset: "mean 42.8 months"
      age_range: "mean 58.8 years"
      handedness: not_reported
      language: not_reported
    statistics:
      threshold: "p < 0.05 with Bonferroni's correction"
      effect_size: not_reported
    confounders_controlled: []
    confounders_not_controlled: ["lesion volume"]
    region_definition:
      kind: atlas
      atlas: "Faria et al. (2012)"
      description: "Inferior frontal gyrus pars opercularis"
    imaging_details:
      field_strength: "3T"
      reference_space: "MNI152"
      atlases_used: ["Faria et al. (2012)"]
    author_limitations:
      - "Feature selection by discarding low-correlation features might miss variables that are predictive only in combination with others."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 5"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 5
        quote: "For lesion-based analysis, the most important regions for predicting fluency scores were the precentral gyrus, opercular part of inferior frontal gyrus, and the posterior part of the superior temporal gyrus (PSTG)"
        supports: claim
---

Findings from Yourganov 2016 using multivariate SVR to predict WAB scores from lesion maps and connectomes.
