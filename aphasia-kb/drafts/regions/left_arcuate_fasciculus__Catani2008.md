---
schema_version: 2.4
id: left_arcuate_fasciculus
name: "Left Arcuate Fasciculus"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
findings:
  - id: f1
    target: left_arcuate_fasciculus
    target_kind: region
    claim: "The left arcuate fasciculus consists of a direct segment connecting Wernicke's and Broca's areas, and an indirect pathway comprising anterior and posterior segments via the inferior parietal lobule."
    direction: likely
    relationship: synthesis
    citation: "@Catani2008"
    method: narrative_review
    design: narrative-review
    strength: moderate
    evidence_quality: narrative-review
    author_limitations:
      - "Mapping symptoms onto single tracts is subject to criticisms of narrow cortical localizationism."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Recent contribution from DTI tractography"
      confidence: high
      flags: []
    source_passages:
      - section: "Recent contribution from DTI tractography"
        page: 5
        quote: "In addition to the long direct segment connecting Wernicke's area with Broca's area, there is an indirect pathway consisting of two segments, an anterior segment linking Broca's territory with the inferior parietal lobule and a posterior segment linking the inferior parietal lobule with Wernicke's territory."
        supports: claim
      - section: "Concluding remarks"
        page: 8
        quote: "mapping symptoms onto single tracts is subjected to the same criticisms directed to narrow cortical localizationism"
        supports: limitation
  - id: f2
    target: left_arcuate_fasciculus
    target_kind: region
    claim: "Extreme left lateralization of the direct arcuate fasciculus segment occurs in approximately 60% of the normal population, with higher prevalence in males (85%) than females (40%)."
    direction: likely
    relationship: synthesis
    citation: "@Catani2008"
    method: narrative_review
    design: narrative-review
    strength: moderate
    evidence_quality: narrative-review
    author_limitations:
      - "Knowledge of human white matter anatomy remains limited."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Recent contribution from DTI tractography"
      confidence: high
      flags: []
    source_passages:
      - section: "Recent contribution from DTI tractography"
        page: 5
        quote: "Tractography analysis... showed an extreme degree of leftward lateralization in w60% of the normal population... extreme left lateralization is observed in 40% of the female population... whereas 85% of males appear to be extremely left lateralised."
        supports: claim
      - section: "Concluding remarks"
        page: 8
        quote: "our knowledge of human white matter anatomy is still very limited"
        supports: limitation
---
