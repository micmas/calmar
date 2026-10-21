---
schema_version: 2.3
id: neuroplasticity_language_network
name: "Neuroimaging of Stroke Recovery from Aphasia"
kind: review
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
findings:
  - id: f1
    target: left_arcuate_fasciculus
    target_kind: region
    claim: "Integrity of the left arcuate fasciculus is associated with better language outcome six months post-stroke."
    direction: likely
    relationship: synthesis
    citation: "@Hartwigsen2019"
    method: narrative_review
    design: narrative-review
    evidence_quality: narrative-review
    strength: moderate
    primary_papers_cited:
      - "@Kim2013"
    author_limitations: []
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Neuroimaging-based outcome prediction, page 6"
      confidence: high
      flags: []
    source_passages:
      - section: "Neuroimaging-based outcome prediction"
        page: 6
        quote: "a similar finding for the left hemisphere was reported by Kim and Jang (2013) who found that successful reconstruction of the left arcuate fascicle by means of diffusion-tensor based tractography was associated with better language outcome after six months."
        supports: claim

  - id: f2
    target: right_arcuate_fasciculus
    target_kind: region
    claim: "The volume of the right arcuate fasciculus is a predictive factor for language recovery six months post-stroke."
    direction: likely
    relationship: synthesis
    citation: "@Hartwigsen2019"
    method: narrative_review
    design: narrative-review
    evidence_quality: narrative-review
    strength: moderate
    primary_papers_cited:
      - "@Forkel2014"
    author_limitations: []
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Neuroimaging-based outcome prediction, page 6"
      confidence: high
      flags: []
    source_passages:
      - section: "Neuroimaging-based outcome prediction"
        page: 6
        quote: "They observed that the volume of the long segment of the arcuate fascicle in the right hemisphere, in addition to other predictive variables including age, gender and lesion size, is an important predictive factor for language recovery six months post-stroke."
        supports: claim

  - id: f3
    target: right_middle_temporal_gyrus
    target_kind: region
    claim: "Structural plasticity in the right middle temporal gyrus, specifically grey matter increase, supports language recovery and object naming improvement."
    direction: likely
    relationship: synthesis
    citation: "@Hartwigsen2019"
    method: narrative_review
    design: narrative-review
    evidence_quality: narrative-review
    strength: moderate
    primary_papers_cited:
      - "@Hope2017"
    author_limitations: []
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Network reorganization in chronic stroke, page 4"
      confidence: high
      flags: []
    source_passages:
      - section: "Network reorganization in chronic stroke"
        page: 4
        quote: "Using VBM, they found two clusters in the right middle temporal gyrus where spontaneous improvement of object naming correlated with an increase of grey matter."
        supports: claim

  - id: f4
    target: severity_metric
    target_kind: predictor
    claim: "Initial severity of language deficit and age are established factors that influence later recovery from aphasia."
    direction: likely
    relationship: synthesis
    citation: "@Hartwigsen2019"
    method: narrative_review
    design: narrative-review
    evidence_quality: narrative-review
    strength: strong
    primary_papers_cited:
      - "@Pedersen1995"
    author_limitations: []
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Neuroimaging-based outcome prediction, page 5"
      confidence: high
      flags: []
    source_passages:
      - section: "Neuroimaging-based outcome prediction"
        page: 5
        quote: "It is well established that initial severity of the language deficit and age are factors that influence later recovery (Pedersen et al., 1995)."
        supports: claim
---

This review synthesizes neuroimaging evidence on the temporal dynamics of language recovery, the role of bilateral networks, and the use of NIBS to probe plasticity.
