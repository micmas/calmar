---
schema_version: 2.3
id: lesion_volume
name: "Lesion Volume"
kind: predictor
predictor_type: imaging_metric
short_definition: "The total volume of necrotic brain tissue resulting from a stroke."
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
findings:
  - id: f1
    target: anomic_aphasia
    target_kind: impairment
    claim: "Total necrotic lesion volume is not associated with treatment-induced improvements in naming."
    direction: no_effect
    relationship: responder
    citation: "@Bonilha2016"
    method: LSM
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
      effect_size: "r = -.28"
      p_value: ".18"
    confounders_controlled: []
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
        quote: "Lesion volume was not associated with treatment-induced improvements in naming (r = -.28, P = .18)."
        supports: claim
---

Finding f1 indicates that total lesion volume does not significantly predict the degree of naming recovery after therapy.
