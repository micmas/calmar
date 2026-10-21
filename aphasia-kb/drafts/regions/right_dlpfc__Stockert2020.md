---
schema_version: 2.3
id: right_dlpfc
name: "Right Dorsolateral Prefrontal Cortex"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: right
findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "A stronger increase in right DLPFC activation from the acute to subacute phase is associated with greater improvement in language comprehension."
    direction: likely
    relationship: correlational
    citation: "@Stockert2020"
    method: fMRI_activation
    design: longitudinal
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 34
      population: "post-stroke aphasia (left frontal or temporo-parietal lesions)"
      time_post_onset: "acute (1-7 days), subacute (8-21 days), chronic (4-6 months)"
      age_range: not_reported
      handedness: not_reported
      language: "German"
    statistics:
      threshold: "P < 0.05, two-tailed"
      effect_size: not_reported
    confounders_controlled: []
    confounders_not_controlled: ["lesion volume"]
    region_definition:
      kind: peak_coord_sphere
      mni_peak: [47, 25, 28]
      radius_mm: 9
      description: "Spherical volume of interest based on global activation peak."
    imaging_details:
      field_strength: not_reported
      reference_space: MNI152
      atlases_used: ["AAL"]
      coordinates_reported:
        - region: "right DLPFC"
          mni: [47, 25, 28]
    author_limitations:
      - "The auditory comprehension paradigm may have been more sensitive to mapping dysfunction of temporal cortex."
      - "Coarse split into two groups based on lesion location does not account for within-group lesion variability."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 852"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 852
        quote: "In addition, a stronger early (t2 - t1) increase in right DLPFC language activation was related to a greater improvement of language comprehension"
        supports: claim
      - section: "Materials and methods"
        page: 846
        quote: "Thirty-four patients with first ischaemic stroke, primarily affecting the left frontal (n = 17) or temporo-parietal (n = 17) cortex"
        supports: sample
      - section: "Imaging"
        page: 847
        quote: "we contrasted the responses to SP and REV (SP > REV) to obtain patterns of language-related activation."
        supports: method
      - section: "Imaging"
        page: 853
        quote: "Mean language activation was extracted for all significant activation peaks, using spherical volumes of interest (r = 9 mm)."
        supports: region_definition
      - section: "Limitations"
        page: 858
        quote: "it might in part also be explained by the auditory comprehension paradigms used to map language activation."
        supports: limitation
---
