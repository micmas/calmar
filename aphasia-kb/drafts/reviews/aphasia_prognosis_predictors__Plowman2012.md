---
schema_version: 2.3
id: aphasia_prognosis_predictors__Plowman2012
name: "Post-stroke aphasia prognosis: a review of patient-related and stroke-related factors"
kind: review
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
findings:
  - id: f1
    target: initial_aphasia_severity
    target_kind: predictor
    claim: "Initial aphasia severity is the most predictive factor for long-term language recovery following stroke."
    direction: likely
    relationship: synthesis
    citation: "@Plowman2012"
    method: narrative_review
    design: narrative-review
    evidence_quality: narrative-review
    strength: moderate
    author_limitations:
      - "The review notes that predictive factors are highly variable, making prognosis difficult."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 1"
      confidence: high
      flags: []
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "Initial severity of aphasia emerged as the factor most predictive of long-term aphasia recovery."
        supports: claim
      - section: "Results"
        page: 3
        quote: "While a strong relationship existed between initial aphasia severity and language outcomes, the relationship was most predictive of long-term language outcomes during the 2- to 4-week post-stroke period..."
        supports: claim
      - section: "Abstract"
        page: 1
        quote: "Unfortunately, predictive factors are highly variable making prognosis of aphasia recovery difficult."
        supports: limitation
  - id: f2
    target: age
    target_kind: predictor
    claim: "Age influences the incidence and type of post-stroke aphasia, but there is no consistent evidence that it predicts the ability for language recovery."
    direction: mixed
    relationship: synthesis
    citation: "@Plowman2012"
    method: narrative_review
    design: narrative-review
    evidence_quality: narrative-review
    strength: moderate
    author_limitations:
      - "Conflicting reports exist, with some studies suggesting younger patients recover better and others finding age to be a poor indicator."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 2-3"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 3
        quote: "While age does appear to influence both the incidence and type of post-stroke aphasia, the impact of age on aphasia recovery is unclear."
        supports: claim
      - section: "Results"
        page: 3
        quote: "Younger patients have been reported to demonstrate a higher recovery rate than older patients [27]; however, conflicting reports have deemed age to be a poor prognostic indicator of aphasia recovery [16,17,22,28]."
        supports: limitation
  - id: f3
    target: sex
    target_kind: predictor
    claim: "Gender does not appear to significantly impact the incidence, type, or recovery patterns of post-stroke aphasia."
    direction: no_effect
    relationship: synthesis
    citation: "@Plowman2012"
    method: narrative_review
    design: narrative-review
    evidence_quality: narrative-review
    strength: moderate
    author_limitations: []
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 2"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 2
        quote: "In summary, evidence is largely equivocal and gender does not appear to significantly impact incidence of aphasia, aphasia type or recovery patterns in post-stroke individuals."
        supports: claim
  - id: f4
    target: lesion_volume
    target_kind: predictor
    claim: "Smaller lesion size is generally associated with better language recovery outcomes."
    direction: likely
    relationship: synthesis
    citation: "@Plowman2012"
    method: narrative_review
    design: narrative-review
    evidence_quality: narrative-review
    strength: moderate
    author_limitations: []
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 3-4"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 3
        quote: "Size of lesion negatively influenced overall recovery, with larger lesions to the temporobasal area associated with lower improvement and less total recovery."
        supports: claim
      - section: "Results"
        page: 4
        quote: "a recent study of 669 patients with aphasia by Maas and colleagues indicated that better outcomes were associated with clinically and radiographically smaller strokes..."
        supports: claim
---
