---
schema_version: 2.3
id: left_inferior_fronto_occipital_fasciculus
name: "Left Inferior Fronto-Occipital Fasciculus"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: semantics
    target_kind: impairment
    claim: "The inferior fronto-occipital fasciculus is involved in semantic processing, as evidenced by semantic paraphasias during electrostimulation."
    direction: likely
    relationship: synthesis
    citation: "@Dick2012"
    method: narrative_review
    design: narrative-review
    strength: weak
    evidence_quality: narrative-review
    author_limitations:
      - "The existence of direct occipital-frontal connectivity via the inferior fronto-occipital fasciculus remains a major controversy."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "The inferior longitudinal fasciculus and inferior fronto-occipital fasciculus, page 13"
      confidence: high
      flags: ["new region id - flag for reviewer to add to KB"]
    source_passages:
      - section: "The inferior longitudinal fasciculus and inferior fronto-occipital fasciculus"
        page: 13
        quote: "Duffau and colleagues (2005) and Mandonnet et al. (2007) have shown that intraoperative electrostimulation of the white matter under the superior temporal sulcus leads to semantic paraphasias. They identified this as the white matter of the inferior fronto-occipital fasciculus"
        supports: claim
      - section: "Summary and concluding remarks"
        page: 14
        quote: "With respect to the ventral stream, outstanding questions focus on: [...] (ii) the existence of direct occipital-frontal connectivity via the inferior fronto-occipital fasciculus"
        supports: limitation
---
