---
schema_version: 2.3
id: multivariate_aphasia_approaches
name: "Multivariate Approaches to Understanding Aphasia"
kind: review
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
findings:
  - id: f1
    target: aphasia_severity
    target_kind: predictor
    claim: "Aphasia is inherently multifactorial, and traditional characterizations by subtype and severity have limited explanatory power regarding underlying neural substrates."
    direction: likely
    relationship: synthesis
    citation: "@WilsonHula2019"
    method: narrative_review
    design: narrative-review
    evidence_quality: narrative-review
    strength: moderate
    author_limitations: []
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Abstract"
      confidence: high
      flags: []
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "Aphasia is often characterized in terms of subtype and severity, yet these constructs have limited explanatory power, because aphasia is inherently multifactorial both in its neural substrates and in its symptomatology."
        supports: claim
  - id: f2
    target: multivariate_lsm
    target_kind: region
    claim: "Multivariate lesion-symptom mapping (MLSM) generally outperforms univariate VLSM in identifying brain regions associated with specific language deficits, particularly in synthetic data with multiple contributing regions."
    direction: likely
    relationship: synthesis
    citation: "@WilsonHula2019"
    method: narrative_review
    design: narrative-review
    evidence_quality: narrative-review
    strength: moderate
    author_limitations: []
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Abstract"
      confidence: high
      flags: ["target_kind: region used for a method-based synthesis"]
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "Multivariate lesion-symptom mapping has been shown to outperform univariate approaches to lesion-symptom mapping for identifying brain regions where damage is associated with specific speech and language deficits."
        supports: claim
  - id: f3
    target: left_superior_temporal_gyrus
    target_kind: region
    claim: "Speech recognition processes are localized to the superior temporal gyrus, while speech production is localized to the supramarginal gyrus."
    direction: likely
    relationship: synthesis
    citation: "@WilsonHula2019"
    method: narrative_review
    design: narrative-review
    evidence_quality: narrative-review
    strength: moderate
    primary_papers_cited:
      - "@Mirman2015"
    author_limitations: []
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Multivariate analysis of the neural substrates of aphasia"
      confidence: high
      flags: []
    source_passages:
      - section: "Multivariate analysis of the neural substrates of aphasia"
        page: 5
        quote: "Some highlights include a dissociation between speech recognition and speech production processes, which were localized to the superior temporal gyrus and supramarginal gyrus respectively [30]"
        supports: claim
  - id: f4
    target: left_posterior_stg
    target_kind: region
    claim: "Sentence comprehension is localized to the posterior temporal cortex."
    direction: likely
    relationship: synthesis
    citation: "@WilsonHula2019"
    method: narrative_review
    design: narrative-review
    evidence_quality: narrative-review
    strength: moderate
    primary_papers_cited:
      - "@Fridriksson2018Anatomy"
    author_limitations: []
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Multivariate analysis of the neural substrates of aphasia"
      confidence: high
      flags: []
    source_passages:
      - section: "Multivariate analysis of the neural substrates of aphasia"
        page: 5
        quote: "and localization of sentence comprehension to posterior temporal cortex [32]."
        supports: claim
  - id: f5
    target: left_arcuate_fasciculus
    target_kind: region
    claim: "Reduced interhemispheric connectivity between homotopic regions is highly predictive of deficits in higher functions, including language."
    direction: likely
    relationship: synthesis
    citation: "@WilsonHula2019"
    method: narrative_review
    design: narrative-review
    evidence_quality: narrative-review
    strength: moderate
    primary_papers_cited:
      - "@Siegel2016"
    author_limitations: []
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Multivariate analysis of the neural substrates of aphasia"
      confidence: high
      flags: ["target is a proxy for network connectivity"]
    source_passages:
      - section: "Multivariate analysis of the neural substrates of aphasia"
        page: 6
        quote: "Most saliently, they showed that reduced interhemispheric connectivity between homotopic regions is highly predictive of deficits in higher functions, including language [68•]."
        supports: claim
---

This review surveys the shift from univariate to multivariate statistical approaches in aphasia research, emphasizing that aphasia is a multidimensional disorder both behaviorally and neurally.
