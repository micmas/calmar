---
schema_version: 2.6
id: left_arcuate_fasciculus
name: "Left Arcuate Fasciculus"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Damage to the posterior and long segments of the left arcuate fasciculus is associated with poorer chronic language outcomes."
    direction: likely
    relationship: causal
    citation: "@Ramsey2017"
    method: MLPA
    design: longitudinal
    evidence_quality: cohort
    strength: moderate
    sample:
      n: 132
      population: "first-time stroke patients with heterogeneous lesions"
      time_post_onset: "approximately two weeks after their stroke"
      phase: longitudinal
      age_range: "mean 54 (s.d. 11), range 19–83"
      handedness: not_reported
      language: not_reported
    statistics:
      threshold: "P < 0.001"
      effect_size: not_reported
    confounders_controlled:
      - "sub-acute score"
      - "lesion size"
      - "age"
      - "education"
      - "hours of therapy"
    confounders_not_controlled: []
    region_definition:
      kind: tract
      description: "Overlap of the lesion with the topography of atlas-based white matter tracts."
    imaging_details:
      reference_space: Talairach
      atlases_used: []
      preprocessing_pipeline: "manual segmentation using Analyze biomedical imaging software"
    author_limitations:
      - "The behavioural battery was a trade-off between completeness and feasibility."
      - "Did not track perfusion or functional MRI data that could clarify other possible mechanisms of recovery."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 4"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 4
        quote: "An analysis of the overlap of the lesion with the topography of atlas-based white matter tracts indicated a poor language outcome for damage of the posterior and long segment of the arcuate fasciculus..."
        supports: claim
      - section: "Results"
        page: 2
        quote: "Subjects (n = 172) with a first symptomatic stroke anywhere in the brain and clinical evidence of any neurological impairment were prospectively recruited, with n = 132 meeting post-enrolment inclusion criteria."
        supports: sample
      - section: "Methods"
        page: 8
        quote: "To provide low-dimensional information about lesion location for deficit recovery models we conducted a PCA analysis on lesion locations across all subjects."
        supports: method
      - section: "Results"
        page: 4
        quote: "Prediction of language recovery improved significantly when the 'unflipped' components were used (13% variance explained, P < 0.001)"
        supports: statistics
      - section: "Results"
        page: 3
        quote: "For each behavioural domain, a regression analysis was conducted in which the dependent measure was the three-month behavioural score, and the predictors were lesion size, age, education, therapy and the sub-acute behavioural score"
        supports: confounders
      - section: "Discussion"
        page: 6
        quote: "Another limitation is that the behavioural battery was a trade-off between completeness and feasibility."
        supports: limitation
      - section: "Discussion"
        page: 6
        quote: "it is important to note that we did not track either perfusion or functional MRI data that could clarify other possible mechanisms of recovery."
        supports: limitation
---
