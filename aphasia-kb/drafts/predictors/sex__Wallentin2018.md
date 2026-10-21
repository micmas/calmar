---
schema_version: 2.3
id: sex
name: "Sex"
kind: predictor
predictor_type: demographic
short_definition: "Biological sex of the patient."
units: "category"
typical_range: "male, female"
direction_of_severity: not_applicable
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21

findings:
  - id: f1
    target: aphasia_severity
    target_kind: impairment
    claim: "Women have significantly higher rates of aphasia following stroke than men."
    direction: likely
    relationship: correlational
    citation: "@Wallentin2018"
    method: meta-analysis
    design: meta-analysis
    strength: moderate
    evidence_quality: meta-analysis
    sample:
      n: 48362
      population: "stroke patients"
      time_post_onset: not_reported
      age_range: not_reported
      handedness: not_reported
      language: not_reported
    statistics:
      threshold: "p<0.001"
      effect_size: "ratio 1.14 (1.10-1.18 95% CI), Cohen's d 0.37"
    confounders_controlled: []
    confounders_not_controlled: ["age", "stroke severity"]
    author_limitations:
      - "The observed sex difference does not take age or stroke severity into account."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results of meta-analysis, page 5"
      confidence: high
      flags: []
    source_passages:
      - section: "Results of meta-analysis"
        page: 5
        quote: "29.6% of female stroke patients were diagnosed, while 26% of males were diagnosed with aphasia... This difference was found to be statistically significant using a paired and weighted t-test on the aphasia rates across studies... t(27) = 6.76, p<0.001"
        supports: claim
      - section: "Results of meta-analysis"
        page: 5
        quote: "The overall sex aphasia rate ratio was found to be 1.14 (1.10-1.18 95% CI) with a Cohen's d of 0.37"
        supports: statistics
      - section: "Results of meta-analysis"
        page: 5
        quote: "This effect, however, does not take age or stroke severity into account."
        supports: limitation

  - id: f2
    target: aphasia_severity
    target_kind: impairment
    claim: "When controlling for age and stroke severity, sex does not independently predict aphasia rates."
    direction: no_effect
    relationship: correlational
    citation: "@Wallentin2018"
    method: behavioral_only
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 1967038
      population: "US American stroke patients (HCUP database)"
      time_post_onset: not_reported
      age_range: not_reported
      handedness: not_reported
      language: "English"
    statistics:
      threshold: "p = 0.1"
      effect_size: "t(273.11) = -1.64"
    confounders_controlled: ["age", "stroke severity"]
    confounders_not_controlled: []
    author_limitations:
      - "The database used a crude proxy for stroke severity (hemiplegia diagnoses)."
      - "Data are summary data for participating states, not individual patient data."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results of database analysis, page 9"
      confidence: high
      flags: []
    source_passages:
      - section: "Results of database analysis"
        page: 9
        quote: "When including age and stroke severity in a regression analysis, however, no significant effect of sex over and above that explained by age and severity could be observed, t(273.11) = -1.64, p = 0.1."
        supports: claim
      - section: "Discussion"
        page: 11
        quote: "It has to be said, however, that this analysis used a somewhat crude proxy for stroke severity."
        supports: limitation
      - section: "Methods for database analysis"
        page: 8
        quote: "It is important to note that the database does not offer information about age for any individual patient. These data are all summery data for the participating states for a particular year (2011-2014)."
        supports: limitation
---
