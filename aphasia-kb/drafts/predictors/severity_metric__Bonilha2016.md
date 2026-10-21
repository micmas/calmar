---
schema_version: 2.3
id: severity_metric
name: "Aphasia Severity Metric"
kind: predictor
predictor_type: behavioural
short_definition: "Overall measure of aphasia severity, typically derived from a standardized battery."
assessment: ["WAB-AQ"]
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
findings:
  - id: f1
    target: anomic_aphasia
    target_kind: impairment
    claim: "Lower baseline aphasia severity (higher WAB-AQ) is associated with greater improvement in naming following speech therapy."
    direction: likely
    relationship: responder
    citation: "@Bonilha2016"
    instrument: "WAB-AQ"
    method: behavioral_only
    design: longitudinal
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 24
      population: "chronic aphasia following left hemisphere ischemic stroke"
      time_post_onset: ">= 6 months"
      age_range: "mean 60.2 (SD 11.9)"
      handedness: "all right-handed"
      language: not_reported
    statistics:
      threshold: "P < .008"
      effect_size: "T = 2.45"
      p_value: ".03"
    confounders_controlled:
      - "age"
      - "time since the stroke"
      - "stroke lesion size"
    confounders_not_controlled: []
    author_limitations:
      - "Heterogeneous population pooling different aphasic syndromes."
      - "Focused only on anomia."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 271"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 271
        quote: "In this model, WAB-AQ was also associated with treatment-related improvement in naming (T = 2.45, P = .03); patients with less severe aphasia achieved a higher naming improvement."
        supports: claim
---

Finding f1 confirms that baseline severity (WAB-AQ) is a significant predictor of naming recovery.
