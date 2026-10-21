---
schema_version: 2.3
id: right_medial_frontal_cortex
name: "Right Medial Frontal Cortex"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: right
findings:
  - id: f1
    target: intention_treatment
    target_kind: therapy
    claim: "Intention Treatment leads to a significant rightward shift in medial frontal cortex activity, though this effect is only observed at the 3-month follow-up."
    direction: likely
    relationship: treatment_response
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
      threshold: "P < .05"
      effect_size: "t = -2.615"
    confounders_controlled: ["
      picture-naming impairment (BNT)",
      "frontal lesion extent"
    ]
    confounders_not_controlled: []
    region_definition:
      kind: atlas
      atlas: "Harvard-Oxford"
      description: "Medial frontal ROI constructed by combining regions from the Harvard-Oxford atlas."
    imaging_details:
      field_strength: "3T"
      reference_space: MNI152
      atlases_used: ["Harvard-Oxford"]
    author_limitations:
      - "Small sample size."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 548"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 548
        quote: "There also was a significant rightward shift in medial frontal activity for IT at 3 months posttreatment (t = -2.615, df = 5, P < .05)."
        supports: claim
      - section: "Discussion"
        page: 551
        quote: "Medial frontal cortex also showed a laterality shift for IT, but only at 3-month follow-up."
        supports: claim
---

# Right Medial Frontal Cortex

This region shows delayed rightward relateralization following Intention Treatment.
