---
schema_version: 2.3
id: corpus_callosum
name: "Corpus Callosum"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: bilateral
findings:
  - id: f1
    target: tactile_aphasia
    target_kind: impairment
    claim: "Tactile aphasia (inability to name objects tactilely) can result from a disconnection between the somesthetic association areas and the speech area, such as through a callosal infarction."
    direction: likely
    relationship: synthesis
    citation: "@Geschwind1965"
    method: narrative_review
    design: narrative-review
    strength: moderate
    evidence_quality: narrative-review
    author_limitations:
      - "The author notes that the synthesis contains much speculation subject to future experimental checks."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Tactile Aphasia, page 582"
      confidence: high
      flags: ["new region id", "target impairment id tactile_aphasia is forward-looking"]
    source_passages:
      - section: "Tactile Aphasia"
        page: 582
        quote: "We interpreted these disturbances as reflecting a failure of somesthetic stimulation to cross to the opposite hemisphere and thought that we would probably find a callosal lesion. The post-mortem confirmed the presence of a callosal infarction..."
        supports: claim
      - section: "Introduction"
        page: 241
        quote: "There are many facts recorded in the following pages; there is also much speculation which is, however, nearly all subject to the checks of future experiment and clinical observation."
        supports: limitation
---
