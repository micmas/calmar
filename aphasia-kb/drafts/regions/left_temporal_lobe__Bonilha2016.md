---
schema_version: 2.3
id: left_temporal_lobe
name: "Left Temporal Lobe"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
findings:
  - id: f1
    target: anomic_aphasia
    target_kind: impairment
    claim: "Higher nodal betweenness centrality of the left temporal lobe is associated with greater improvement in naming following speech therapy."
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
      effect_size: "model F = 6.79, model R2 = .74"
      p_value: ".00077"
    confounders_controlled:
      - "age"
      - "time since the stroke"
      - "stroke lesion size"
      - "WAB-AQ"
    confounders_not_controlled: []
    region_definition:
      kind: atlas
      atlas: "Brodmann Areas"
      description: "Left temporal ROIs including BA 20, 21, 22, 37, 38."
    imaging_details:
      modalities:
        - modality: T1
          sequence: "3D MP-RAGE"
          voxel_size_mm: not_reported
          TR_ms: 2250
          TE_ms: 4.15
        - modality: DTI
          sequence: "Diffusion EPI"
          n_directions: 30
          b_values: [1000, 2000]
          TR_ms: 6100
          TE_ms: 101
      preprocessing_pipeline: "Probabilistic GM/WM segmentation, registration of ROIs to DTI space, probabilistic fiber tracking"
      reference_space: MNI152
      atlases_used: ["Brodmann Areas"]
    author_limitations:
      - "Heterogeneous population pooling different aphasic syndromes."
      - "Focused only on anomia."
      - "Identical treatment regardless of individual baseline performance or aphasia type."
      - "Brodmann area ROIs are large and may encompass regions with distinct functions."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 271"
      confidence: high
      flags: ["target_id left_temporal_lobe is new; flag for promotion"]
    source_passages:
      - section: "Results"
        page: 271
        quote: "We observed a robust relationship between treatment-related improvement in naming and a higher left temporal BC (controlling for age, time since the stroke, stroke lesion size, and WAB-AQ) (model F = 6.79, P = .00077, model R = .86, model R2 = .74)"
        supports: claim
      - section: "Methods"
        page: 268
        quote: "We studied 24 individuals recruited from the local community with chronic aphasia as a result of a left hemisphere ischemic stroke that occurred at least 6 months prior to enrolling in this study."
        supports: sample
      - section: "Discussion"
        page: 276
        quote: "the ROIs of this atlas are large, usually encompassing different brain regions that serve distinct functions"
        supports: limitation
---

Finding f1 describes the association between the network influence (betweenness centrality) of the left temporal lobe and the ability to improve naming after intense speech therapy.
