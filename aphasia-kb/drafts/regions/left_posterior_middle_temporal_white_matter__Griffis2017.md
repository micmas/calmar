---
schema_version: 2.3
id: left_posterior_middle_temporal_white_matter
name: "Left Posterior Middle Temporal White Matter"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: anomic_aphasia
    target_kind: impairment
    claim: "Damage to the left posterior middle temporal white matter is a strong predictor of naming deficits."
    direction: likely
    relationship: causal
    citation: "@Griffis2017"
    method: MLPA
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample: {n: 43, population: "chronic left hemispheric stroke"}
    statistics: {threshold: "FDR p < 0.10", effect_size: "beta = -1.04"}
    confounders_controlled: ["lesion volume"]
    confounders_not_controlled: []
    region_definition: {kind: "data_driven_cluster", description: "SVR-LSM peak in posterior middle temporal white matter"}
    imaging_details: {reference_space: "MNI152", atlases_used: [], preprocessing_pipeline: "SPM12 unified normalization", field_strength: "3T"}
    author_limitations: ["only chronic patients were included"]
    provenance: {extracted_by: "agent", extracted_on: "2026-01-01", paper_section: "Table 1, page 10", confidence: "high", flags: []}
    source_passages:
      - {section: "Results", page: 9, quote: "SVR-LSM + DTLVC analyses revealed significant associations between damage to portions of the left... pMTG and deficits in all three language outcomes", supports: "claim"}
      - {section: "Discussion", page: 12, quote: "only chronic patients were included", supports: "limitation"}
  - id: f2
    target: semantics
    target_kind: impairment
    claim: "Damage to the left posterior middle temporal white matter is a strong predictor of auditory semantic decision deficits."
    direction: likely
    relationship: causal
    citation: "@Griffis2017"
    method: MLPA
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample: {n: 39, population: "chronic left hemispheric stroke"}
    statistics: {threshold: "FDR p < 0.10", effect_size: "beta = -1.10"}
    confounders_controlled: ["lesion volume"]
    confounders_not_controlled: []
    region_definition: {kind: "data_driven_cluster", description: "SVR-LSM peak in posterior middle temporal white matter"}
    imaging_details: {reference_space: "MNI152", atlases_used: [], preprocessing_pipeline: "SPM12 unified normalization", field_strength: "3T"}
    author_limitations: ["only chronic patients were included"]
    provenance: {extracted_by: "agent", extracted_on: "2026-01-01", paper_section: "Table 1, page 10", confidence: "high", flags: []}
    source_passages:
      - {section: "Results", page: 9, quote: "SVR-LSM + DTLVC analyses revealed significant associations between damage to portions of the left... pMTG and deficits in all three language outcomes", supports: "claim"}
      - {section: "Discussion", page: 12, quote: "only chronic patients were included", supports: "limitation"}
---

Findings from @Griffis2017 regarding the posterior middle temporal white matter.
