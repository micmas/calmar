---
schema_version: 2.3
id: left_occipito_temporal_sulcus
name: Left Occipito-Temporal Sulcus
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: pure_alexia
  target_kind: impairment
  claim: Damage to the left occipito-temporal sulcus is associated with pure alexia.
  direction: likely
  relationship: causal
  citation: '@Pflugshaupt2009'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 12
    population: patients with pure alexia and hemianopic dyslexia
    time_post_onset: not_reported
    age_range: not_reported
    handedness: all right-handed
    language: German
    phase: not_reported
  statistics:
    threshold: not_reported
    cluster_extent: not_reported
    effect_size: identified as one of the largest group differences in subtraction analysis
    p_value: not_reported
  confounders_controlled:
  - ' visual field defect side'
  - degree of macular sparing
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Left occipito-temporal sulcus identified via lesion subtraction analysis (pure alexia
      minus hemianopic dyslexia).
  imaging_details:
    field_strength: not_reported
    acquisition:
      voxel_size_mm: not_reported
      TR_ms: not_reported
      TE_ms: not_reported
      sequence: not_reported
    preprocessing_pipeline: Manual tracing onto CH2 template brain using MRIcro software
    reference_space: MNI152
    atlases_used:
    - AAL
    coordinates_reported: []
  author_limitations:
  - Small sample size may lead to underestimation of visuo-motor deficits.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results - Lesion analysis, page 6
    confidence: high
    flags:
    - target_id pure_alexia is forward-looking
  source_passages:
  - section: Abstract
    page: 1
    quote: subtracting the lesions of the hemianopic dyslexics from those found in pure alexics revealed
      the largest group differences in posterior parts of the left fusiform gyrus, occipito-temporal sulcus
      and inferior temporal gyrus.
    supports: claim
  - section: Methods - Lesion analysis
    page: 5
    quote: brain lesions were manually drawn from clinical MR or CT scans onto axial slices of the CH2
      template brain.
    supports: method
  - section: Discussion
    page: 9
    quote: due to relatively small sample sizes and thus limited statistical power, these comparisons
      are likely to underestimate visuo-motor deficits in patients
    supports: limitation
---
# Left Occipito-Temporal Sulcus

Findings from Pflugshaupt et al. (2009) indicate that the left occipito-temporal sulcus is a key region whose damage is associated with pure alexia, as revealed by lesion subtraction against hemianopic dyslexia.
