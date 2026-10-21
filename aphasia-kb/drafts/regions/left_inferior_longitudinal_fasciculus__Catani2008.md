---
schema_version: 2.4
id: left_inferior_longitudinal_fasciculus
name: "Left Inferior Longitudinal Fasciculus"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
findings:
  - id: f1
    target: semantics
    target_kind: impairment
    claim: "The left inferior longitudinal fasciculus is likely involved in visual object recognition and linking object representations to lexical labels."
    direction: likely
    relationship: synthesis
    citation: "@Catani2008"
    method: narrative_review
    design: narrative-review
    strength: weak
    evidence_quality: narrative-review
    author_limitations:
      - "Knowledge of human white matter anatomy remains limited."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Beyond the arcuate fasciculus: the ventral pathways"
      confidence: high
      flags: ["target_id left_inferior_longitudinal_fasciculus is forward-looking"]
    source_passages:
      - section: "Beyond the arcuate fasciculus: the ventral pathways"
        page: 5
        quote: "The inferior longitudinal fasciculus... is likely to play an important role in visual object recognition, and in linking object representations to their lexical labels."
        supports: claim
      - section: "Concluding remarks"
        page: 8
        quote: "our knowledge of human white matter anatomy is still very limited"
        supports: limitation
---
