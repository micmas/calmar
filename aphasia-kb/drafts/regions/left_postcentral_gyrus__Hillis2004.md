---
schema_version: 2.3
id: left_postcentral_gyrus
name: "Left Postcentral Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: apraxia_of_speech
    target_kind: impairment
    claim: "In a subset of patients with apraxia of speech who lack Broca's area dysfunction, dysfunction of the left postcentral gyrus (sensory cortex) is associated with the deficit."
    direction: likely
    relationship: causal
    citation: "@Hillis2004"
    method: LSM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 5
      population: "acute left hemisphere stroke patients with apraxia of speech and no Broca's area dysfunction"
      time_post_onset: "within 24 h"
      age_range: not_reported
      handedness: "all right-handed"
      language: "English"
    statistics:
      threshold: "visual inspection of DWI/PWI"
      effect_size: "5/5 patients"
      p_value: not_reported
    confounders_controlled: ["
      absence of Broca's area dysfunction"
    ]
    confounders_not_controlled: []
    region_definition:
      kind: manual_ROI
      description: "Left postcentral gyrus (sensory cortex) identified on DWI and PWI."
    imaging_details:
      field_strength: "1.5 Tesla"
      modalities:
        - modality: DWI
          sequence: "single shot EPI"
          voxel_size_mm: not_reported
          TR_ms: 10000
          TE_ms: 120
        - modality: PWI
          sequence: "single shot gradient echo EPI"
          voxel_size_mm: not_reported
          TR_ms: 2000
          TE_ms: 60
      preprocessing_pipeline: "PWI hypoperfusion defined as >2.5 s delay in time to peak arrival of contrast relative to homologous region in intact hemisphere"
      reference_space: native
      atlases_used: []
    author_limitations:
      - "Small sample size for this specific subgroup (n=5)."
      - "Dysfunction may occur via diaschisis without being apparent on DWI or PWI."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 1482"
      confidence: high
      flags: ["new region ID: left_postcentral_gyrus"]
    source_passages:
      - section: "Results"
        page: 4
        quote: "Among all 80 patients, there were five patients with apraxia of speech who had neither dense ischaemia (on DWI) nor hypoperfusion (on PWI) in Broca's area... All five of these patients had infarct or hypoperfusion of the postcentral gyrus..."
        supports: claim
      - section: "Methods - Subjects"
        page: 2
        quote: "Subjects were adults with first ever, non-lacunar, ischaemic stroke affecting the left MCA territory as determined by MRI. Exclusion criteria were: [...] left-handedness [...] or lack of proficiency in English."
        supports: sample
      - section: "Methods - Imaging"
        page: 3
        quote: "Scans were done on a GE Signa 1.5 Tesla, echo planar imaging (EPI)-capable system."
        supports: imaging_details
      - section: "Discussion"
        page: 7
        quote: "For example, a lesion may cause deafferentation of a remote area of cortex, causing dysfunction of that region ('diaschisis') without causing hypoperfusion apparent on PWI or bioenergetic failure apparent on DWI."
        supports: limitation
---

This finding suggests that speech articulation may depend on a network including sensory cortex, rather than being localized to a single region.
