---
schema_version: 2.6
id: right_motor_cortex
name: "Right Motor Cortex"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-23
hemisphere: right
findings:
  - id: f1
    target: naming
    target_kind: impairment
    claim: "In patients with left motor cortex lesions, increased activity in the right motor cortex is positively associated with better naming performance."
    direction: likely
    relationship: correlational
    citation: "@SkipperKallal2017"
    method: fMRI_activation
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 24
      population: "chronic left hemisphere stroke survivors with aphasia and left motor lesions"
      time_post_onset: "at least six months after their stroke (mean chronicity = 52.9 months)"
      phase: chronic
      age_range: "mean 59.8 (SD 10.1)"
      handedness: "mixed"
      language: "native English speakers"
    statistics:
      threshold: "not_reported"
      effect_size: "t(21) = 3.67"
      p_value: ".001"
    confounders_controlled: ["lesion volume"]
    confounders_not_controlled: []
    region_definition:
      kind: peak_coord_sphere
      mni_peak: [52, -10, 26]
      radius_mm: 5
      description: "Right motor cortex/central sulcus ROI based on control group peak."
    imaging_details:
      field_strength: "3.0 T"
      modalities:
        - modality: T1
          sequence: MPRAGE
          voxel_size_mm: [1, 1, 1]
        - modality: fMRI
          sequence: gradient-echo echo-planar pulse
          voxel_size_mm: [3.2, 3.2, 3.2]
      task:
        name: "Delayed naming task"
        description: "Participants named line drawings silently (covert) then aloud (overt)."
        contrasts: ["overt > fixation"]
        baseline: "fixation"
      preprocessing_pipeline: "FSL 5.0.6: high pass filter, MCFLIRT motion correction, slice timing correction, intensity normalization, 5mm FWHM smoothing, registration to MNI"
      reference_space: MNI152
      atlases_used: []
    author_limitations:
      - "Upregulation of the motor region in people with aphasia may be a marker of increased demands on domain general systems such as cognitive control and attention rather than language specific function."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 9"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 9
        quote: "However, for participants with left motor lesions (N = 24), right motor activity was positively associated with naming, t(21) = 3.67, P = 0.001."
        supports: claim
      - section: "Materials and Methods"
        page: 3
        quote: "Forty-nine chronic left hemisphere stroke survivors with a history of aphasia were recruited... resulting in a final sample of 39 participants"
        supports: sample
      - section: "fMRI Analysis"
        page: 4
        quote: "Regressions were carried out which tested whether lesion status in a left hemisphere ROI predicted activity levels in each of the other left and right hemisphere ROIs, controlling for lesion volume."
        supports: method
      - section: "Results"
        page: 9
        quote: "t(21) = 3.67, P = 0.001"
        supports: statistics
      - section: "Scanning Parameters and Preprocessing"
        page: 4
        quote: "MRI data were collected on a 3.0 T Siemens Trio Scanner... Registration and normalization were carried out to the MNI standardized brain provided by FSL."
        supports: imaging_details
      - section: "General Discussion"
        page: 14
        quote: "upregulation of the region in people with aphasia is a marker of increased demands on domain general systems such as cognitive control and attention"
        supports: limitation
---

Notes: This finding specifically applies to the subgroup with left motor cortex lesions.
