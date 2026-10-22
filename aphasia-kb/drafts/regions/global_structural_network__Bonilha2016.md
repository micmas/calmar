---
schema_version: 2.6
id: global_structural_network
name: "Global Structural Network"
kind: network
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-22
hemisphere: bilateral
findings:
  - id: f1
    target: anomic_aphasia
    target_kind: therapy
    claim: "Higher global network small-worldness (NSW) is associated with greater treatment-related improvement in naming in chronic aphasia."
    direction: likely
    relationship: responder
    citation: "@Bonilha2016"
    method: DTI
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 24
      population: "chronic left-hemisphere ischemic stroke"
      time_post_onset: "at least 6 months"
      phase: chronic
      age_range: "mean 60.2 (SD 11.9)"
      handedness: "all right-handed"
      language: "not_reported"
    statistics:
      threshold: "P < .008"
      effect_size: "model R2 = .712"
      p_value: ".0002"
    confounders_controlled: ["age", "time since the stroke", "stroke lesion size", "WAB-AQ"]
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "Global network small-worldness (NSW) calculated as the ratio between normalized clustering and normalized characteristic path length."
    imaging_details:
      field_strength: "3T"
      modalities:
        - modality: T1
          sequence: "3D MP-RAGE"
          voxel_size_mm: not_reported
          TR_ms: 2250
          TE_ms: 4.15
        - modality: DTI
          sequence: "Diffusion EPI"
          voxel_size_mm: [2.7, 2.7, 2.7]
          n_directions: 30
          b_values: [1000, 2000]
          TR_ms: 6100
          TE_ms: 101
      preprocessing_pipeline: "Probabilistic gray/white matter segmentation, registration to DTI space, probabilistic fiber tracking, and correction for ROI volume and distance."
      reference_space: "native"
      atlases_used: ["Brodmann"]
    author_limitations:
      - "The study focused on only one aspect of aphasia, namely, anomia."
      - "Evaluation occurred within a week after a 2-week intense intervention; longitudinal follow-up is needed."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 272"
      confidence: high
      flags: ["cohort overlaps with @Fridriksson2010 (n=20 subgroup); flag for downstream double-counting risk in interpret_overlap()"]
    source_passages:
      - section: "Results"
        page: 272
        quote: "We also observed a robust relationship between PNT improvement and global network NSW. Patients with higher global NSW demonstrated greater treatment-related improvement in naming (controlling for age, time since the stroke, stroke lesion size, and WAB-AQ) (model F = 8.89, P = .0002, model R = .84, model R2 = .712; Figure 5, Supplemental Table 2)."
        supports: claim
      - section: "Subjects"
        page: 268
        quote: "We studied 24 individuals recruited from the local community with chronic aphasia as a result of a left hemisphere ischemic stroke that occurred at least 6 months prior to enrolling in this study."
        supports: sample
      - section: "Measures of Neural Network Architecture"
        page: 269
        quote: "NSW was calculated as the ratio between the normalized clustering and the normalized characteristic path length, thus representing one unique score per participant reflecting global network integrity."
        supports: region_definition
      - section: "Baseline MRI Scanning"
        page: 268
        quote: "All subjects underwent MRI scanning at USC in a 3T Siemens Trio... (a) T1-weighted images (3D MP-RAGE, TR = 2250 ms, TE = 4.15 ms...); (b) Diffusion EPI scan (30-directions with b = 1000 s/mm2 and b = 2000 s/mm2, TR = 6100 ms, TE = 101 ms... 45 contiguous 2.7 mm axial slices...)"
        supports: imaging_details
      - section: "Limitations and Future Studies"
        page: 276
        quote: "Second, we focused on just one aspect of aphasia, namely, anomia."
        supports: limitation
---
