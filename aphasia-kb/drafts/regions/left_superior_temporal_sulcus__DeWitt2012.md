---
schema_version: 2.3
id: left_superior_temporal_sulcus
name: Left Superior Temporal Sulcus
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: auditory_comprehension
  target_kind: impairment
  claim: The left anterior superior temporal sulcus is recruited for the processing of phrase-length auditory
    stimuli.
  direction: likely
  relationship: recruitment
  citation: '@DeWitt2012'
  method: meta-analysis
  design: meta-analysis
  evidence_quality: meta-analysis
  strength: strong
  sample:
    n: 19
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
    description: Peak focus density for phrase-associated activation in left anterior STS identified via
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
    - target_id auditory_comprehension is forward-looking
    - author_limitations not explicitly stated in summary
    - reference_space not reported but ALE typically uses MNI152
  source_passages:
  - section: Results
    page: 2
    quote: Peak focus density for phrase-associated activation was found in left anterior STS
    supports: claim
  - section: Figure 1
    page: 1
    quote: phrase-length studies' peak density in left anterior STS (C; n=19)
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
This entry describes the recruitment of the left anterior STS for phrase-level auditory processing as part of a hierarchical ventral stream.
