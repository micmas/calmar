---
schema_version: 2.6
id: executive_functions
name: "Executive Functions"
kind: predictor
predictor_type: behavioural
short_definition: "A collection of higher-level cognitive processes including inhibition, attention, task-switching, working memory, and self-monitoring."
assessment: ["Wisconsin Card Sort Task (WCST)", "Wiegl Sorting Test (WST)", "Cognitive Linguistic Quick Test (CLQT)", "Test of Everyday Attention (TEA)", "Raven's Coloured Progressive Matrices (RCPM)"]
units: "score"
typical_range: "not_reported"
direction_of_severity: "lower_is_worse"
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-23

findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Baseline executive control and cognitive abilities are positively correlated with language therapy outcomes, particularly in patients with moderate-to-severe aphasia."
    direction: likely
    relationship: correlational
    citation: "@Simic2019"
    method: narrative_review
    design: systematic-review
    evidence_quality: narrative-review
    strength: moderate
    author_limitations:
      - "Heterogeneity of EC tasks used across studies makes it difficult to identify which specific processes drive the relationship."
      - "Lack of a-priori theoretical models in most included studies' test selection."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 409"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 409
        quote: "Overall, greater performance on measures of EC and other cognitive tasks was significantly correlated to better language therapy outcomes in 10 of the 15 studies reviewed (67%...)"
        supports: claim
      - section: "Discussion"
        page: 425
        quote: "It appears that baseline measures of EC and/or cognitive ability are important indicators of language therapy success, but primarily in individuals with moderate-to-severe language deficits."
        supports: claim
      - section: "Discussion"
        page: 426
        quote: "The heterogeneity of the tasks used to measure EC, in part due to a lack of a-priori operational definitions of EC, also calls into question the validity of the findings."
        supports: limitation

  - id: f2
    target: constraint_induced_aphasia_therapy
    target_kind: therapy
    claim: "Baseline executive control abilities do not significantly correlate with treatment success in intensive constraint-induced aphasia therapy."
    direction: no_effect
    relationship: responder
    citation: "@Simic2019"
    method: narrative_review
    design: systematic-review
    evidence_quality: narrative-review
    strength: moderate
    author_limitations:
      - "The nature of CIAT may bypass the positive relationship between EC and outcomes found in non-intensive therapies."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Abstract, page 1"
      confidence: high
      flags: []
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "This relationship emerged when EC was measured using specific (e.g., divided attention), as opposed to broad (e.g., reasoning) tasks, and primarily when naming therapy was administered; intensive constraint-induced therapy did not correlate with treatment success."
        supports: claim
      - section: "Discussion"
        page: 424
        quote: "Rose and colleagues (2013) suggest that the nature of CIAT (e.g., intense treatment within a socially mediated practice context) bypasses the positive relationship between EC and language therapy outcomes..."
        supports: limitation
---

This entry captures the synthesis of 15 studies reviewed by Simic et al. (2019) regarding the prognostic value of executive control for language therapy outcomes.
