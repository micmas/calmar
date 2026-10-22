---
schema_version: 2.6
id: lesion_behavior_mapping_methods__Karnath2018
name: Mapping Human Brain Lesions and Their Functional Consequences
kind: review
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
findings:
- id: f1
  target: lesion_volume
  target_kind: predictor
  claim: There is a strong coupling between impairment and lesion size, where larger lesions are more
    likely to affect critical anatomical structures.
  direction: likely
  relationship: synthesis
  citation: '@Karnath2018'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  author_limitations:
  - The authors note that exceptions exist, such as when critical regions are connected with blood vessels
    associated with small lesions (e.g., basal ganglia injury).
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Potential limitations of the mass-univariate approach, page 3
    confidence: high
    flags: []
  source_passages:
  - section: Potential limitations of the mass-univariate approach
    page: 3
    quote: as a rule of thumb there is a strong coupling between impairment and lesion size.
    supports: claim
  - section: Potential limitations of the mass-univariate approach
    page: 3
    quote: in fact, for many behavioral deficits lesion size is the best predictor for severity of the
      behavioral deficit; larger lesions are usually more likely to affect critical anatomical structures
    supports: claim
  - section: Potential limitations of the mass-univariate approach
    page: 3
    quote: We note that there can be exceptions to this, for example when a critical region is connected
      with blood vessels associated with small lesions (e.g., basal ganglia injury can be associated with
      lacunar infarction).
    supports: limitation
- id: f2
  target: severity_metric
  target_kind: predictor
  claim: Acute behavioral data is a strong predictor of long-term clinical outcome, often following a
    proportional recovery rule.
  direction: likely
  relationship: synthesis
  citation: '@Karnath2018'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  author_limitations: []
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Multivariate lesion analysis with machine learning algorithms, page 7
    confidence: high
    flags: []
  source_passages:
  - section: Multivariate lesion analysis with machine learning algorithms
    page: 7
    quote: The acute behavioral data is a strong predictor of long term outcome... whereas the 'proportional
      recovery rule' (Krakauer and Marshall, 2015) is based on the strong predictive nature of acute impairment.
    supports: claim
- id: f3
  target: lesion_behavior_mapping_methods
  target_kind: prognosis
  claim: Multivariate lesion-behavior mapping (MLBM) can outperform univariate approaches (VLBM) in identifying
    cognitive functions organized in brain networks.
  direction: likely
  relationship: synthesis
  citation: '@Karnath2018'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  author_limitations:
  - Multivariate results may still suffer from a reduced, but present, spatial bias.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Multivariate lesion analysis with machine learning algorithms, page 7
    confidence: high
    flags: []
  source_passages:
  - section: Multivariate lesion analysis with machine learning algorithms
    page: 7
    quote: The authors observed that multivariate lesion-behaviour mapping is superior to its mass-univariate
      counterparts in brain networks, i.e., if a cognitive function is organized in multiple, separate
      brain regions.
    supports: claim
  - section: Multivariate lesion analysis with machine learning algorithms
    page: 8
    quote: However, multivariate results were far from being perfect; they suffered from a reduced, but
      still present spatial bias.
    supports: limitation
---

This review discusses the evolution of lesion-behavior mapping from simple overlap to voxel-based lesion symptom mapping (VLSM) and multivariate machine learning approaches. It highlights the inherent spatial biases of stroke lesions due to vasculature and the importance of controlling for lesion volume.
