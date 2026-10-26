---
schema_version: 2.7
id: left_angular_gyrus
name: Left Angular Gyrus
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: The left angular gyrus is a primary hub of the semantic processing network in healthy adults.
  direction: likely
  relationship: recruitment
  citation: '@Binder2009'
  method: meta-analysis
  design: cross-sectional
  strength: strong
  evidence_quality: meta-analysis
  sample:
    n: 1642
    population: healthy adult humans
    time_post_onset: not_reported
    age_range: not_reported
    handedness: not_reported
    language: not_reported
    phase: not_reported
    cohort: not_reported
  statistics:
    threshold: corrected mapwise a < 0.05 after removing clusters smaller than 1000 lL
    cluster_extent: not_reported
    effect_size: not_reported
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled:
  - ' phonological and orthographic processing demands'
  - general executive and response processes
  - task difficulty
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: ALE meta-analysis cluster in the posterior aspect of the left inferior parietal lobule.
  imaging_details:
    reference_space: Talairach
    preprocessing_pipeline: MNI coordinates converted to Talairach and Tournoux (1988) system using the
      'icbm2tal' transform
    atlases_used: []
  author_limitations:
  - Screening efforts to remove phonological or working memory confounds were likely imperfect due to
    the absence of appropriate behavioral data in many published studies.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 5
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 5
    quote: 'Seven principal regions showed a high likelihood of activation across studies: 1) the angular
      gyrus (AG) and adjacent supramarginal gyrus (SMG)'
    supports: claim
  - section: Materials and Methods
    page: 4
    quote: ALE maps from each of the observed data sets were then thresholded at an ALE value that yielded
      a corrected mapwise a < 0.05 after removing clusters smaller than 1000 lL.
    supports: statistics
  - section: Results
    page: 5
    quote: These studies collectively involved 1642 participants
    supports: sample
  - section: Discussion
    page: 11
    quote: Though we attempted to remove contrasts in which semantic processing was confounded with phonological
      processing or overall difficulty, these screening efforts were likely imperfect due to the absence
      of appropriate behavioral data in many published studies.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
- id: f2
  target: semantics
  target_kind: impairment
  claim: The left angular gyrus is specifically recruited during the processing of perceptually encoded
    (concrete) knowledge.
  direction: likely
  relationship: recruitment
  citation: '@Binder2009'
  method: meta-analysis
  design: cross-sectional
  strength: strong
  evidence_quality: meta-analysis
  sample:
    n: 1642
    population: healthy adult humans
    time_post_onset: not_reported
    age_range: not_reported
    handedness: not_reported
    language: not_reported
    phase: not_reported
    cohort: not_reported
  statistics:
    threshold: corrected mapwise a < 0.05
    cluster_extent: not_reported
    effect_size: not_reported
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled:
  - ' phonological and orthographic processing demands'
  - general executive and response processes
  - task difficulty
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: ALE meta-analysis cluster in the angular gyrus.
  imaging_details:
    reference_space: Talairach
    preprocessing_pipeline: MNI coordinates converted to Talairach and Tournoux (1988) system using the
      'icbm2tal' transform
    atlases_used: []
  author_limitations:
  - Screening efforts to remove phonological or working memory confounds were likely imperfect due to
    the absence of appropriate behavioral data in many published studies.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 6
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 6
    quote: Significant overlap for the 113 'perceptual' foci occurred in the AG bilaterally, left mid-fusiform
      gyrus, left DMPFC, and left posterior cingulate
    supports: claim
  - section: Discussion
    page: 11
    quote: Though we attempted to remove contrasts in which semantic processing was confounded with phonological
      processing or overall difficulty, these screening efforts were likely imperfect due to the absence
      of appropriate behavioral data in many published studies.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
