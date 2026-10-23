---
schema_version: 2.6
id: right_amygdala
name: "Right Amygdala"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-23
hemisphere: right
findings:
  - id: f1
    target: affective_receptive_aprosodia
    target_kind: impairment
    claim: "Damage to the right amygdala is an independent predictor of impairment in the identification of fearful prosody in acute stroke."
    direction: likely
    relationship: causal
    citation: "@Sheppard2020"
    method: RLSM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 23
      population: "acute right hemisphere ischemic stroke"
      time_post_onset: "within 5 days of stroke"
      phase: acute
      age_range: "mean 55.09 years, SD 17.22"
      handedness: "all right-handed"
      language: "premorbid fluent speakers of English"
    statistics:
      threshold: "p < 0.05"
      effect_size: "p = 0.047"
      p_value: 0.047
    confounders_controlled:
      - "age"
      - "education"
      - "lesion volume"
    confounders_not_controlled: []
    region_definition:
      kind: manual_ROI
      description: "Right amygdala traced using MRIcron and coregistered to the Johns Hopkins University atlas."
    imaging_details:
      field_strength: "3.0T"
      acquisition:
        voxel_size_mm: [2, 2, 2]
        sequence: "DWI"
      preprocessing_pipeline: "MRIcron tracing + SPM12 coregistration to Johns Hopkins University atlas"
      reference_space: "other"
      atlases_used: ["Johns Hopkins University atlas"]
    author_limitations:
      - "Relatively small number of participants with longitudinal data prevented brain-behavior mapping in chronic patients."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page e1015"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 4
        quote: "Individual independent predictors of lower accuracy of fearful prosody identification were percent damage to the right amygdala (p = 0.047), older age (p < 0.001), and less education (p = 0.005)."
        supports: claim
      - section: "Methods"
        page: 2
        quote: "We enrolled 23 patients (mean age 55.09 years, SD 17.22) with acute RH ischemic stroke... At the acute time point, 23 patients were tested within 5 days of stroke."
        supports: sample
      - section: "Statistical analysis"
        page: 3
        quote: "Multivariable linear regression was then repeated using the same model... for each of the 6 emotions individually."
        supports: method
      - section: "Results"
        page: 4
        quote: "Of the multivariable linear regression models evaluating emotion identification in each of the 6 emotions, only the fear identification model was significant, F10,10 = 7.61, p = 0.002... Individual independent predictors of lower accuracy of fearful prosody identification were percent damage to the right amygdala (p = 0.047)"
        supports: statistics
      - section: "Methods"
        page: 2
        quote: "Scans were acquired clinically within 48 hours of admission on a 3.0T Siemens (Munich, Germany) Trio scanner. Whole-brain DWI had 40 slices with a 2.0 mm3 voxel size."
        supports: imaging_details
      - section: "Methods"
        page: 2
        quote: "These areas of tissue dysfunction were traced using MRIcron software and were coregistered to the Johns Hopkins University atlas using SPM12"
        supports: region_definition
      - section: "Discussion"
        page: 6
        quote: "There were a relatively small number of participants with longitudinal data at both the acute and chronic stages, which prevented us from conducting brain-behavior mapping in chronic patients."
        supports: limitation
---

Finding f1 describes the causal link between right amygdala damage and the specific impairment of identifying fearful prosody.
