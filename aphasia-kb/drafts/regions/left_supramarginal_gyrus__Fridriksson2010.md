---
schema_version: 2.3
id: left_supramarginal_gyrus
name: "Left Supramarginal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
findings:
  - id: f1
    target: speech_repetition
    target_kind: impairment
    claim: "Hypoperfusion in the inferior portion of the left supramarginal gyrus is a strong predictor of impaired speech repetition."
    direction: likely
    relationship: causal
    citation: "@Fridriksson2010"
    method: VBCM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 39
      population: "left hemisphere ischemic stroke"
      time_post_onset: "within 3 d of hospital admission (some up to 20 d)"
      age_range: "mean 63.5 years (range 34-85, SD 12)"
      handedness: not_reported
      language: "Icelandic"
    statistics:
      threshold: "1% false-discovery rate (FDR)"
      effect_size: "Z = -4.21"
      p_value: not_reported
    confounders_controlled: []
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "Inferior portion of the left supramarginal gyrus identified via perfusion-weighted MRI (PWI)."
    imaging_details:
      modalities:
        - modality: PWI
          voxel_size_mm: [1.8, 1.8, 6.5]
      preprocessing_pipeline: "SPM5 used to align the PWI images... reslice the TTP image to standard 2 mm isotropic stereotaxic space."
      reference_space: MNI152
      atlases_used: []
      coordinates_reported: []
    author_limitations:
      - "The study sample included patients with various aphasia types and other deficits (e.g., apraxia of speech), not just pure conduction aphasia."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 3"
      confidence: high
      flags: ["target impairment 'speech_repetition' is forward-looking", "region 'left_supramarginal_gyrus' is forward-looking"]
    source_passages:
      - section: "Results"
        page: 3
        quote: "The WLS regression analysis of the PWI data revealed that the best predictor of impaired speech repetition was located in the inferior portion of the left supramarginal gyrus, Z = -4.21"
        supports: claim
      - section: "Materials and Methods"
        page: 2
        quote: "Therefore, data from 39 patients were included in the final statistical analyses described below."
        supports: sample
      - section: "Materials and Methods"
        page: 2
        quote: "The mean patient age was 63.5 years (range 34-85, SD 12)."
        supports: sample
      - section: "Materials and Methods"
        page: 2
        quote: "All participants had incurred a single event ischemic stroke to the left hemisphere"
        supports: sample
      - section: "Materials and Methods"
        page: 2
        quote: "The results were corrected for multiple comparisons using a 1% FDR."
        supports: statistics
      - section: "Materials and Methods"
        page: 2
        quote: "SPM5 was used to align the PWI images... This transform was used to reslice the TTP image to standard 2 mm isotropic stereotaxic space."
        supports: imaging_details
      - section: "Discussion"
        page: 4
        quote: "the study sample included some patients who had difficulty repeating due to factors such as apraxia of speech, nonfluent aphasia, or auditory comprehension impairment rather than the primary repetition impairment seen in conduction aphasia."
        supports: limitation
---
