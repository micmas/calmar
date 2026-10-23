---
schema_version: 2.6
id: left_middle_frontal_gyrus
name: "Left Middle Frontal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-23
hemisphere: left
findings:
  - id: f1
    target: executive_functions
    target_kind: impairment
    claim: "Damage to the left dorsolateral prefrontal cortex (middle frontal gyrus) is associated with impaired response inhibition on the Stroop Test."
    direction: likely
    relationship: causal
    citation: "@Glascher2012"
    method: VLSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 344
      population: "individuals with focal lesions"
      time_post_onset: not_reported
      phase: not_reported
      age_range: not_reported
      handedness: "mostly right-handed (317 of 344)"
      language: not_reported
    statistics:
      threshold: "P < 0.05 (FDR)"
      effect_size: not_reported
    confounders_controlled:
      - "verbal abilities"
      - "spatial abilities"
      - "verbal memory"
      - "spatial memory"
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "Left dlPFC (middle frontal gyrus) identified via VLSM associated with Stroop performance."
    imaging_details:
      reference_space: not_reported
      atlases_used: []
      preprocessing_pipeline: "Manual slice-by-slice tracing onto a reference brain"
    author_limitations:
      - "Findings are relative to the particular tasks for which data were available."
      - "Power was greatest in regions with the densest lesion overlaps (PFC)."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 2"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 2
        quote: "Lower performance on the STROOP was associated with damage to left dlPFC (middle frontal gyrus), which is consistent with the previously described role of this region in response inhibition."
        supports: claim
      - section: "Materials and Methods"
        page: 6
        quote: "The 344 participants were drawn from the Patient Registry of the Department of Neurology at the University of Iowa Hospitals and Clinics."
        supports: sample
      - section: "Materials and Methods"
        page: 6
        quote: "We used nonparametric voxel-based lesion-symptom mapping (VLSM) (28) to map out significant lesion-deficit relationships."
        supports: method
      - section: "Materials and Methods"
        page: 6
        quote: "We used a threshold of 5% FDR to control for multiple comparisons."
        supports: statistics
      - section: "Materials and Methods"
        page: 6
        quote: "Performance scores indexing verbal skills, visual-spatial reasoning, and both verbal and visual memory were derived from additional neuropsychological tests and used as covariates to partial out their effects..."
        supports: confounders
      - section: "Materials and Methods"
        page: 6
        quote: "The visible lesion of each patient's MRI or CT scan was traced manually slice by slice on corresponding regions of a reference brain by a neuroanatomical expert."
        supports: imaging_details
      - section: "Discussion"
        page: 5
        quote: "our results are relative to the particular tasks for which data were available, and different neuropsychological measures might produce somewhat different anatomical results."
        supports: limitation
---
