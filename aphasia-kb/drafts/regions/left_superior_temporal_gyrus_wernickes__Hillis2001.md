---
schema_version: 2.6
id: left_superior_temporal_gyrus_wernickes
name: Left Superior Temporal Gyrus (Wernicke's region, mid-posterior)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: In acute stroke, the severity of lexical-semantic impairment is strongly correlated with the
    magnitude of perfusion delay in left Brodmann's area 22 (Wernicke's area).
  direction: likely
  relationship: correlational
  citation: '@Hillis2001'
  method:
  - PWI
  - behavioral_only
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 50
    population: acute left hemisphere ischemic stroke
    time_post_onset: 0.5 to 24 hours
    phase: acute
    age_range: 23 to 86 years (mean 61.0, SD 14.8)
    handedness: right-handed
    language: English
  statistics:
    threshold: p < 0.00001
    effect_size: r = 0.84
  confounders_controlled:
  - infarct in BA 22 (excluded)
  - impaired visual recognition (excluded)
  - impaired spoken word recognition (excluded)
  confounders_not_controlled: []
  region_definition:
    kind: atlas
    atlas: Brodmann
    description: Brodmann's area 22 (Wernicke's area)
  imaging_details:
    field_strength: 1.5T
    modalities:
    - modality: PWI
      sequence: single-shot gradient echo EPI
      TR_ms: 2000
      TE_ms: 60
      notes: Gd-DTPA bolus power injected at 5ml/sec
    - modality: DWI
      sequence: multi-slice, isotropic, single-shot EPI
      TR_ms: 10000
      TE_ms: 120
      b_values:
      - 1000
    preprocessing_pipeline: TTP maps coregistered with T2-weighted images; BA 22 identified via published
      templates
    reference_space: native
    atlases_used:
    - Brodmann
  author_limitations:
  - TTP is not an absolute measure of blood flow; hypoperfusion of the right hemisphere could lead to
    underestimation of left-sided hypoperfusion.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 563
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: we found a strong Pearson correlation between the rate of errors on a word comprehension test
      and the mean number of seconds of delay in time-to-peak concentration of contrast in Wernicke's
      area, relative to the homologous region on the right.
    supports: claim
  - section: Patients and Methods
    page: 2
    quote: A total of 80 patients met inclusion criteria of (1) clinical diagnosis of acute left hemispheric
      ischemic stroke within 24 hours of symptom onset or symptom progression and (2) right-handed and
      premorbid proficiency in English
    supports: sample
  - section: Patients and Methods
    page: 2
    quote: After language testing and MRI scans were obtained, 29 subjects with DWI abnormalities in BA
      22 were excluded... Thus, 50 subjects were included in the analysis of lexical-semantic impairment
      versus delay on PWI.
    supports: sample
  - section: Magnetic Resonance Imaging Protocol
    page: 3
    quote: Gd-DTPA PWI were obtained on a Sigma 1.5-T echo planar imaging capable system... Single-shot
      gradient echo EPI perfusion images (TR/TE of 2000/60msec) were obtained with 20ml Gd-DTPA bolus
      power injected at 5ml/sec
    supports: imaging_details
  - section: Results
    page: 3
    quote: A very high correlation (r = 0.84; p < 0.00001) was found between the mean number of seconds
      delay in left BA 22 and the error rate in spoken word/picture verification
    supports: statistics
  - section: Discussion
    page: 5
    quote: TTP is not an absolute measure of blood flow. Thus, hypoperfusion of the right hemisphere (eg,
      due to diaschesis, or arterial stenosis) would lead to underestimation of the degree of hypoperfusion
      in the homologous region on the left.
    supports: limitation
---
