---
schema_version: 2.3
id: typicality_semantic_feature_analysis
name: "Semantic Feature Analysis"
kind: therapy
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
short_description: "A semantic-based treatment that improves naming by having patients generate semantic features of a target object using a structured chart."
targets_impairments: ["anomic_aphasia"]

findings:
  - id: f1
    target: anomic_aphasia
    target_kind: impairment
    claim: "Semantic Feature Analysis (SFA) effectively improves the naming of trained items across a variety of aphasia syndromes, though generalization to untrained items is limited."
    direction: likely
    relationship: causal
    citation: "@Efstratiadou2018"
    method: narrative_review
    design: systematic-review
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 55
      population: "persons with aphasia"
      time_post_onset: "mean 59.75 months (SD 68.70)"
      age_range: "mean 55.39 (SD 12.66)"
      handedness: "not_reported"
      language: "predominantly monolingual"
    statistics:
      threshold: "not_reported"
      effect_size: "small treatment effect (Cohen's d)"
    confounders_controlled: []
    confounders_not_controlled: ["treatment dosage", "duration", "protocol variations"]
    author_limitations:
      - "Limited generalization to untrained items and connected speech was reported in the majority of the included studies."
      - "Lack of a standardized dosage and treatment duration across studies."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results and Discussion"
      confidence: high
      flags: []
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "Naming of trained items improved for 45 participants (81.82%). Effect sizes indicated that there was a small treatment effect."
        supports: claim
      - section: "Results"
        page: 10
        quote: "Improvement in naming of trained items was found for 45 participants (81.82%). [...] The percentage of generalization to untrained items for all studies was small (40%)."
        supports: statistics
      - section: "Discussion"
        page: 14
        quote: "limited generalization to untrained items and connected speech was reported (40%)."
        supports: limitation
      - section: "Discussion"
        page: 14
        quote: "Another limiting factor is the lack of a standardized dosage and treatment duration across studies."
        supports: limitation

  - id: f2
    target: anomic_aphasia
    target_kind: impairment
    claim: "SFA may be more effective for individuals with fluent aphasia and mild-to-moderate severity compared to those with nonfluent or severe aphasia."
    direction: likely
    relationship: responder
    citation: "@Efstratiadou2018"
    method: narrative_review
    design: systematic-review
    strength: weak
    evidence_quality: cohort
    sample:
      n: 55
      population: "persons with aphasia"
      time_post_onset: "not_reported"
      age_range: "not_reported"
      handedness: "not_reported"
      language: "not_reported"
    statistics:
      threshold: "not_reported"
      effect_size: "not_reported"
    confounders_controlled: []
    confounders_not_controlled: []
    author_limitations:
      - "Further research with large numbers of participants is necessary in order to begin to unravel the impact of different aphasic profiles and severities on the efficacy of SFA."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Discussion"
      confidence: high
      flags: []
    source_passages:
      - section: "Discussion"
        page: 14
        quote: "Overall, results suggested that SFA as a treatment for word-finding difficulties may be more effective for persons with fluent and moderate or mild aphasia [...] compared with those with nonfluent and more severe aphasia."
        supports: claim
      - section: "Discussion"
        page: 14
        quote: "Further research with large numbers of participants is necessary in order to begin to unravel the impact of different aphasic profiles and severities on the efficacy of SFA."
        supports: limitation
---
