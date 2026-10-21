---
schema_version: 2.3
id: left_uncinate_fasciculus
name: "Left Uncinate Fasciculus"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: fluency
    target_kind: impairment
    claim: "Damage to the left uncinate fasciculus predicts impaired speech fluency, particularly when controlling for motor speech agility."
    direction: likely
    relationship: causal
    citation: "@Fridriksson2013"
    method: VBCM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 64
      population: "chronic left hemisphere stroke"
      time_post_onset: "mean 39.86 months (SD 49.24)"
      age_range: "mean 61.6 years (SD 12.27)"
      handedness: not_reported
      language: not_reported
    statistics:
      threshold: "Bonferroni corrected P < 0.002"
      effect_size: "R2 = 0.51"
      p_value: "0.0001"
    confounders_controlled: ["diadochokinetic rate"]
    confounders_not_controlled: ["agrammatism"]
    region_definition:
      kind: atlas
      atlas: "Catani et al. (2012) white matter atlas"
      description: "Uncinate fasciculus defined by a probability threshold of 0.50."
    imaging_details:
      field_strength: "3T"
      reference_space: MNI152
      atlases_used: ["Catani et al. (2012)"]
    author_limitations:
      - "Lack of explicit measures of patients' ability to initiate or to maintain fluent speech."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 3454"
      confidence: high
      flags: ["new region id: left_uncinate_fasciculus"]
    source_passages:
      - section: "Results"
        page: 3454
        quote: "A separate regression analysis included diadochokinetic rate as a cofactor and revealed involvement of the uncinate fasciculus as the single best predictor of speech fluency, P = 0.0001, R2 = 0.51."
        supports: claim
  - id: f2
    target: form_to_meaning
    target_kind: impairment
    claim: "Damage to the left uncinate fasciculus is a strong predictor of auditory comprehension impairment in patients with Broca's or global aphasia."
    direction: likely
    relationship: causal
    citation: "@Fridriksson2013"
    method: VBCM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 26
      population: "patients with Broca's or global aphasia"
      time_post_onset: not_reported
      age_range: not_reported
      handedness: not_reported
      language: not_reported
    statistics:
      threshold: "not_reported"
      effect_size: "R2 = 0.324"
      p_value: "0.002"
    confounders_controlled: []
    confounders_not_controlled: ["lesion size"]
    region_definition:
      kind: atlas
      atlas: "Catani et al. (2012) white matter atlas"
      description: "Uncinate fasciculus defined by a probability threshold of 0.50."
    imaging_details:
      field_strength: "3T"
      reference_space: MNI152
      atlases_used: ["Catani et al. (2012)"]
    author_limitations:
      - "Sample size for global aphasia (n = 6) was particularly small."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 3456"
      confidence: high
      flags: ["new region id: left_uncinate_fasciculus"]
    source_passages:
      - section: "Results"
        page: 3456
        quote: "A linear regression analysis that only included patients with Broca's or global aphasia revealed that damage to the uncinate fasciculus is the single best predictor of the auditory comprehension subscore on the WAB, F(1,25) = 11.98, P = 0.002, R2 = 0.324."
        supports: claim
---
