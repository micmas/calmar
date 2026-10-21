---
schema_version: 2.3
id: age
name: "Age"
kind: predictor
predictor_type: demographic
short_definition: "The age of the patient at the time of stroke or treatment."
units: "years"
typical_range: "18-90+ years"
direction_of_severity: not_applicable
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Working-age participants (<=65 years) achieve greater overall-language gains with high-intensity SLT (>9 h/week), whereas older participants (>65 years) achieve greatest gains with low-intensity SLT (<=2 h/week)."
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
      age_range: "dichotomized at 65 years"
      handedness: not_reported
      language: "English predominant (26.6%)"
    statistics:
      threshold: "95% CI"
      effect_size: "not_reported"
    confounders_controlled: ["sex", "aphasia severity", "time post-onset"]
    confounders_not_controlled: []
    author_limitations:
      - "Spontaneous recovery may impact treatment gains, especially in early-rehabilitation subgroups."
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
        quote: "Working-age participants made their greatest overall-language and auditory comprehension gains alongside > 9 SLT-h/week. Older participants' greatest overall-language gains occurred for < 2 SLT-h/week..."
        supports: claim
      - section: "Methods"
        page: 5
        quote: "We dichoto-mized IPD based on key demographic and clinical data; males and females, median age (working age <= 65 years and older > 65 years..."
        supports: sample
      - section: "Methods"
        page: 4
        quote: "Drawing only RCT IPD from the wider RELEASE database (21), we conducted a network meta-analysis of SLT interventions delivered by language outcomes (15)."
        supports: method
      - section: "Discussion"
        page: 9
        quote: "We acknowledge that spontaneous recovery may also impact on treatment gains observed..."
        supports: limitation
---
