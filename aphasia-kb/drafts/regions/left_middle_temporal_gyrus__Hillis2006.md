---
schema_version: 2.6
id: left_middle_temporal_gyrus
name: "Left Middle Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: anomic_aphasia
    target_kind: impairment
    claim: "Restored blood flow to the left posterior middle temporal/fusiform gyrus (BA 37) is strongly associated with acute improvement in picture naming after stroke."
    direction: likely
    relationship: causal
    citation: "@Hillis2006"
    method: LSM
    design: longitudinal
    evidence_quality: cohort
    strength: strong
    sample:
      n: 87
      population: "acute left-hemisphere ischemic stroke patients with impaired picture naming"
      time_post_onset: "day 1 and days 3-5"
      phase: longitudinal
      age_range: "mean 64.7 (SD 10.7) years"
      handedness: "right handed"
      language: "English"
    statistics:
      threshold: "p < 0.05 after Bonferroni correction"
      effect_size: "beta = 0.71"
      p_value: "0.0001"
    confounders_controlled: ["
      reperfusion of BA 44/45",
      "reperfusion of BA 22"
    ]
    confounders_not_controlled: []
    region_definition:
      kind: atlas
      atlas: "Brodmann's atlas"
      description: "Left BA 37 (posterior middle and inferior temporal/fusiform gyrus)"
    imaging_details:
      field_strength: "1.5T"
      modalities:
        - modality: PWI
          sequence: "echo planar imaging"
          voxel_size_mm: [not_reported, not_reported, 5]
          TR_ms: 2000
          TE_ms: 60
        - modality: DWI
          sequence: "echo planar imaging"
          voxel_size_mm: [not_reported, not_reported, 5]
          TR_ms: 10000
          TE_ms: 120
      preprocessing_pipeline: "Transferred to Brodmann's and MNI atlas using MRICro"
      reference_space: MNI152
      atlases_used: ["Brodmann's atlas", "MNI atlas"]
    author_limitations:
      - "The threshold of hypoperfusion does not necessarily correspond to tissue that is at risk for progressing to infarction in the absence of restored blood flow."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 8070"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 8070
        quote: "This model indicates that reperfusion of left BA 37 (posterior middle and inferior temporal/fusiform gyrus) was the strongest predictor of acute improvement in picture naming after stroke (p < 0.0001)."
        supports: claim
      - section: "Materials and Methods"
        page: 2
        quote: "The current study was restricted to a subset of 87 patients who had impaired naming... and who completed language tests and imaging with both DWI and PWI at day 1 and days 3-5."
        supports: sample
      - section: "Statistical analysis"
        page: 2
        quote: "An alpha level of 0.05 after Bonferroni correction for multiple comparisons was used to identify significant associations."
        supports: statistics
      - section: "Imaging and image analysis"
        page: 2
        quote: "DWI trace images [bmax = 1000 s/mm2; repetition time (TR)/echo time (TE), 10,000/120 ms] and PWI (TR/TE, 2000/60 ms) scans were obtained on a GE Signa 1.5 tesla echo planar imaging-capable scanner... with whole-brain coverage and 5 mm slice thickness"
        supports: imaging_details
      - section: "Imaging and image analysis"
        page: 2
        quote: "Regions of hypoperfusion on TTP maps were transferred to a Brodmann's atlas and to the Montreal Neurological Institute (MNI) atlas using MRICro"
        supports: region_definition
      - section: "Imaging and image analysis"
        page: 2
        quote: "Although this threshold of hypoperfusion does not necessarily correspond to tissue that is at risk for progressing to infarction in the absence of restored blood flow..."
        supports: limitation
---
