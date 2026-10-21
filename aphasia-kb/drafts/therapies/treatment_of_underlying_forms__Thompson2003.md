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
  - id: f1
    target: syntactic_processing
    target_kind: impairment
    claim: "Training the most syntactically complex structures (e.g., object-relative clauses) results in generalization to less complex structures (e.g., object clefts and who-questions) that share the same linguistic operations."
    direction: likely
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
      - "Possibility that training the longest, most resource-demanding sentences improved general sentence processing ability rather than specific syntactic structures."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Discussion, pages 600-601"
      confidence: high
      flags: []
    source_passages:
      - section: "Abstract"
        page: 591
        quote: "object-relative training resulted in robust generalization to both object clefts and who-questions."
        supports: claim
      - section: "Participants"
        page: 594
        quote: "Four individuals with Broca's aphasia with agrammatism participated in the study."
        supports: sample
      - section: "Participants"
        page: 594
        quote: "At the time of the experiment, participants were between 1 and 11 years poststroke."
        supports: sample
      - section: "Experimental Design"
        page: 596
        quote: "A single subject multiple baseline design across behaviors and participants was used"
        supports: method
      - section: "Production and Comprehension Probes"
        page: 597
        quote: "Generalized production to untrained sentences was considered to have occurred when levels of performance changed by at least 40% over observed baseline levels."
        supports: statistics
      - section: "Discussion"
        page: 601
        quote: "it is possible that training on the longest, most resource-demanding sentences improved general sentence processing/production ability... and that these abilities translated to improvements in processing of sentences of shorter length"
        supports: limitation

notes: "This paper introduces the Complexity Account of Treatment Efficacy (CATE), arguing that the direction of treatment from complex to simple structures enhances generalization."
---
