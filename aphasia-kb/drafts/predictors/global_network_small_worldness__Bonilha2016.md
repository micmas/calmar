---
schema_version: 2.3
id: global_network_small_worldness
name: "Global Network Small-Worldness"
kind: predictor
predictor_type: imaging_metric
short_definition: "A measure of the non-random, efficient structural organization of the whole-brain connectome."
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
findings:
  - id: f1
    target: anomic_aphasia
    target_kind: impairment
    claim: "Preservation of global brain network small-worldness is associated with greater improvement in naming following speech therapy."
    direction: likely
    relationship: responder
    citation: "@Bonilha2016"
    method: DTI
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
      effect_size: "model F = 8.89, model R2 = .712"
      p_value: ".0002"
    confounders_controlled:
      - "age"
      - "time since the stroke"
      - "stroke lesion size"
      - "WAB-AQ"
    confounders_not_controlled: []
    author_limitations:
      - "Heterogeneous population pooling different aphasic syndromes."
      - "Focused only on anomia."
      - "Identical treatment regardless of individual baseline performance or aphasia type."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 272"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 272
        quote: "We also observed a robust relationship between PNT improvement and global network NSW. Patients with higher global NSW demonstrated greater treatment-related improvement in naming (controlling for age, time since the stroke, stroke lesion size, and WAB-AQ) (model F = 8.89, P = .0002, model R = .84, model R2 = .712)"
        supports: claim
      - section: "Discussion"
        page: 276
        quote: "we recruited a heterogeneous population of chronic stroke patients, pooling together different aphasic syndromes."
        supports: limitation
---

Finding f1 links global structural network integrity (NSW) to the capacity for naming recovery in chronic aphasia.
