---
schema_version: 2.3
id: initial_aphasia_severity
name: "Initial Aphasia Severity"
kind: predictor
predictor_type: behavioural
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
findings:
  - id: f1
    target: prognosis
    target_kind: prognosis
    claim: "Acute behavioral impairment is a strong predictor of long-term outcome, consistent with the proportional recovery rule."
    direction: likely
    relationship: synthesis
    citation: "@Karnath2018"
    method: narrative_review
    design: narrative-review
    strength: moderate
    evidence_quality: narrative-review
    sample:
      n: null
      population: "not_reported"
    author_limitations:
      - "Lesion-behavior mapping is necessarily spatially biased by vasculature."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Multivariate lesion analysis with machine learning algorithms, page 7"
      confidence: high
      flags: ["finding is a synthesis of field consensus, not a primary data result"]
    source_passages:
      - section: "Multivariate lesion analysis with machine learning algorithms"
        page: 7
        quote: "The acute behavioral data is a strong predictor of long term outcome... whereas the 'proportional recovery rule' (Krakauer and Marshall, 2015) is based on the strong predictive nature of acute impairment."
        supports: claim
      - section: "Voxel-based lesion behavior mapping (VLBM)"
        page: 3
        quote: "The use of naturally occurring strokes to infer lesion-behavior relationships is necessarily spatially biased."
        supports: limitation
---
