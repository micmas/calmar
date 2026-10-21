---
schema_version: 2.3
id: left_anterior_temporal_lobe
name: "Left Anterior Temporal Lobe"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: syntactic_processing
    target_kind: impairment
    claim: "The left anterior temporal lobe is implicated in general sentence processing, but is not strongly associated with the specific agrammatic comprehension pattern (noncanonical < canonical)."
    direction: mixed
    relationship: causal
    citation: "@Rogalsky2018"
    method: VLSM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 66
      population: "chronic left-hemisphere stroke and unilateral left temporal lobectomy patients"
      time_post_onset: "6 months or more postonset"
      age_range: "mean 62 (stroke), 46 (lobectomy)"
      handedness: "vast majority strongly right-handed"
      language: "native speakers of English"
    statistics:
      threshold: "p < .001, corrected"
      effect_size: "not_reported"
    confounders_controlled:
      - "lesion size"
    confounders_not_controlled: []
    region_definition:
      kind: manual_ROI
      description: "Any damage within any left temporal lobe gray and white matter anterior to the anterior edge of Heschl's gyrus."
    imaging_details:
      field_strength: "not_reported"
      preprocessing_pipeline: "MAP-3 lesion analysis methods implemented on Brainvox software"
      reference_space: "Talairach"
      atlases_used: []
    author_limitations:
      - "Temporal lobectomy patients may have experienced functional neural reorganization due to epilepsy."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results: VLSM Results: All Sentence Types, page 13"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 13
        quote: "the VLSMs for overall performance in both tasks identified significant voxels in the ATL... but no frontal lobe voxels were significant."
        supports: claim
      - section: "Discussion"
        page: 16
        quote: "The finding that the ATL is not strongly associated with agrammatic comprehension is at odds with the agrammatic comprehension findings that were localized to the ATL in Magnusdottir et al.'s study of acute stroke patients."
        supports: claim
      - section: "Methods"
        page: 8
        quote: "left ATL, defined as any damage within any left temporal lobe gray and white matter anterior to the anterior edge of Heschl's gyrus."
        supports: region_definition
---
