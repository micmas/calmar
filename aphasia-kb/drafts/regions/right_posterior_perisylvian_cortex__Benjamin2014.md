---
schema_version: 2.3
id: right_posterior_perisylvian_cortex
name: "Right Posterior Perisylvian Cortex"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: right
findings:
  - id: f1
    target: intention_treatment
    target_kind: therapy
    claim: "In patients receiving Intention Treatment, a rightward shift in posterior perisylvian activity is significantly correlated with greater treatment gains in category-member generation."
    direction: likely
    relationship: responder
    citation: "@Benjamin2014"
    method: fMRI_activation
    design: longitudinal
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 14
      population: "chronic left-hemisphere stroke aphasia"
      time_post_onset: ">6 months"
      age_range: "not_reported"
      handedness: "all right-handed"
      language: "English"
    statistics:
      threshold: "P < .01"
      effect_size: "r = -0.86"
    confounders_controlled: []
    confounders_not_controlled: ["
      aphasia type (IT group dominated by conduction aphasia)"
    ]
    region_definition:
      kind: atlas
      atlas: "Harvard-Oxford"
      description: "Posterior perisylvian ROI constructed by combining regions from the Harvard-Oxford atlas."
    imaging_details:
      field_strength: "3T"
      reference_space: MNI152
      atlases_used: ["Harvard-Oxford"]
    author_limitations:
      - "Small sample size; removal of one subject at either end of the regression line for the CT group could alter the regression line."
      - "Aphasia type and lesion location may affect roles of left and right posterior perisylvian cortex."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 550"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 550
        quote: "However, rightward shifts in posterior persylvian activity showed a significant correlation with treatment gains for IT (r = -0.86, n = 7, P < .01), but for CT, treatment gains were marginally associated with a leftward shift in posterior perisylvian activity (r = 0.77, n = 6, P < .10)."
        supports: claim
      - section: "Discussion"
        page: 552
        quote: "One surprising finding was that a rightward increase in laterality of posterior perisylvian, not lateral frontal, activity was associated with better treatment outcome for the Intention group."
        supports: claim
      - section: "Discussion"
        page: 552
        quote: "Hence, type of aphasia and lesion location may affect roles of left and right posterior perisylvian cortex in the Intention treatment."
        supports: limitation
---

# Right Posterior Perisylvian Cortex

Rightward shift in this region is a predictor of positive response to Intention Treatment in fluent aphasias.
