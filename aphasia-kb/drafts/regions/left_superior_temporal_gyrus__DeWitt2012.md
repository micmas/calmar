---
schema_version: 2.3
id: left_superior_temporal_gyrus
name: Left Superior Temporal Gyrus (Dorsal Stream Node)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: phonological_recognition
  target_kind: impairment
  claim: The left mid-superior temporal gyrus is recruited for the processing of phonemes during auditory
    speech perception.
  direction: likely
  relationship: recruitment
  citation: '@DeWitt2012'
  method: meta-analysis
  design: meta-analysis
  evidence_quality: meta-analysis
  strength: strong
  sample:
    n: 26
    population: healthy adults (meta-analysis of fMRI studies)
    time_post_onset: not_reported
    age_range: not_reported
    handedness: not_reported
    language: not_reported
    phase: not_reported
  statistics:
    threshold: FDR < 10^-3, k > 150cm3
    cluster_extent: not_reported
    effect_size: not_reported
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Peak focus density for phoneme-associated activation in left mid-STG identified via ALE
      meta-analysis.
  imaging_details:
    field_strength: not_reported
    preprocessing_pipeline: Activation Likelihood Estimation (ALE)
    reference_space: not_reported
    atlases_used: []
  author_limitations: []
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 2
    confidence: high
    flags:
    - author_limitations not explicitly stated in summary
    - reference_space not reported but ALE typically uses MNI152
  source_passages:
  - section: Results
    page: 2
    quote: Peak focus density for phoneme-associated activation was found in left mid-STG
    supports: claim
  - section: Figure 1
    page: 1
    quote: phoneme-length studies' peak focus density in left mid-STG (A; n=14) [and] phoneme-length studies'
      peak density in left mid-STG (D; n=12)
    supports: sample
  - section: Results
    page: 2
    quote: Using a coordinate-based method of meta-analysis (activation likelihood estimation), we identified
      regions of significant focus density
    supports: method
  - section: Figure 1
    page: 1
    quote: Intensity represents activation likelihood estimation statistic value (P value for false discovery
      rate < 10^-3, k > 150cm3).
    supports: statistics
- id: f2
  target: semantics
  target_kind: impairment
  claim: The left anterior superior temporal gyrus is recruited for auditory word-form recognition.
  direction: likely
  relationship: recruitment
  citation: '@DeWitt2012'
  method: meta-analysis
  design: meta-analysis
  evidence_quality: meta-analysis
  strength: strong
  sample:
    n: 32
    population: healthy adults (meta-analysis of fMRI studies)
    time_post_onset: not_reported
    age_range: not_reported
    handedness: not_reported
    language: not_reported
    phase: not_reported
  statistics:
    threshold: FDR < 10^-3, k > 150cm3
    cluster_extent: not_reported
    effect_size: not_reported
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Peak focus density for word-associated activation in left anterior STG identified via
      ALE meta-analysis.
  imaging_details:
    field_strength: not_reported
    preprocessing_pipeline: Activation Likelihood Estimation (ALE)
    reference_space: not_reported
    atlases_used: []
  author_limitations: []
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 2
    confidence: high
    flags:
    - author_limitations not explicitly stated in summary
    - reference_space not reported but ALE typically uses MNI152
  source_passages:
  - section: Results
    page: 2
    quote: peak focus density for word-associated activation was found in left anterior STG
    supports: claim
  - section: Figure 1
    page: 1
    quote: word-length studies' peak density in left anterior STG (B; n=16) [and] word-length studies'
      peak density in left anterior STG (E; n=16)
    supports: sample
  - section: Results
    page: 2
    quote: Using a coordinate-based method of meta-analysis (activation likelihood estimation), we identified
      regions of significant focus density
    supports: method
  - section: Figure 1
    page: 1
    quote: Intensity represents activation likelihood estimation statistic value (P value for false discovery
      rate < 10^-3, k > 150cm3).
    supports: statistics
---
This entry adds findings from a meta-analysis of healthy speech perception, supporting a hierarchical ventral stream model where phoneme and word recognition are localized to the mid and anterior STG respectively.
