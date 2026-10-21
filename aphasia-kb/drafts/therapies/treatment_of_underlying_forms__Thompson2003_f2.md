---
schema_version: 2.3
id: treatment_of_underlying_forms
name: "Treatment of Underlying Forms (TUF)"
kind: therapy
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
targets_impairments: ["syntactic_processing"]
short_description: "A linguistic-specific treatment that uses active forms of target sentences to train the comprehension and production of noncanonical structures by focusing on the underlying linguistic operations (e.g., movement)."

findings:
  - id: f2
    target: syntactic_processing
    target_kind: impairment
    claim: "Training simple syntactic structures (e.g., who-questions) does not result in generalization to more complex structures (e.g., object clefts or object-relative clauses)."
    direction: no_effect
    relationship: responder
    citation: "@Thompson2003"
    method: behavioral_only
    design: case-series
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 4
      population: "individuals with Broca's aphasia with agrammatism"
      time_post_onset: "between 1 and 11 years poststroke"
      age_range: not_reported
      handedness: "premorbidly right handed"
      language: "native English speakers"
    statistics:
      threshold: "generalized production considered to have occurred when levels of performance changed by at least 40% over observed baseline levels"
      effect_size: not_reported
    confounders_controlled: ["linguistic relation between trained and untrained structures"]
    confounders_not_controlled: []
    region_definition:
      kind: not_reported
      description: "behavioural-only treatment-efficacy finding — no specific brain region"
    imaging_details:
      reference_space: not_reported
      atlases_used: []
    author_limitations:
      - "Small sample size (n=4) using a single-subject experimental design."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, pages 598-599"
      confidence: high
      flags: []
    source_passages:
      - section: "Abstract"
        page: 591
        quote: "Results showed no generalization across sentence types when who-questions were trained"
        supports: claim
      - section: "Participants"
        page: 594
        quote: "Four individuals with Broca's aphasia with agrammatism participated in the study."
        supports: sample
      - section: "Results"
        page: 598
        quote: "However, no generalization was noted to either object-cleft or object-relative sentences after 10 treatment sessions."
        supports: claim
      - section: "Production and Comprehension Probes"
        page: 597
        quote: "Generalized production to untrained sentences was considered to have occurred when levels of performance changed by at least 40% over observed baseline levels."
        supports: statistics
      - section: "Discussion"
        page: 600
        quote: "in the face of a complete lack of generalization from simpler, who-question structures to object clefts or object relatives"
        supports: claim
      - section: "Discussion"
        page: 601
        quote: "Small sample size (n=4) using a single-subject experimental design."
        supports: limitation

notes: "This finding supports the CATE hypothesis by demonstrating the asymmetry of generalization based on structural complexity."
---
