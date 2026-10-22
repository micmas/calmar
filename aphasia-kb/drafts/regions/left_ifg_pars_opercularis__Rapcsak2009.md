---
schema_version: 2.3
id: left_ifg_pars_opercularis
name: Left IFG Pars Opercularis (Broca's area, dorsal stream hub)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: phonological_dyslexia
  target_kind: impairment
  claim: Damage to the left inferior frontal gyrus pars opercularis is associated with phonological dyslexia.
  direction: likely
  relationship: causal
  citation: '@Rapcsak2009'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 31
    population: left-hemisphere damaged patients with language impairment
    time_post_onset: subacute or chronic stage
    age_range: 40-78 years
    handedness: not_reported
    language: not_reported
    phase: chronic
  statistics:
    threshold: chi-square design
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: atlas
    atlas: AAL
    description: posterior inferior frontal gyrus/Broca's area (BA44/45)
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: 3D inversion recovery (IR) prepped spoiled-gradient-echo sequence (SPGR)
      voxel_size_mm:
      - 1
      - 1
      - 1.5
    preprocessing_pipeline: SPM2 spatial normalization with lesion masking
    reference_space: MNI152
    atlases_used:
    - AAL
  author_limitations:
  - Relied on a mix of clinical and research scans, introducing variability in image quality.
  - Used binary decisions regarding the presence/absence of damage to an ROI.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 584
    confidence: high
    flags:
    - target_id phonological_dyslexia is forward-looking
  source_passages:
  - section: Results
    page: 12
    quote: damage to both anterior (posterior inferior frontal gyrus/Broca's area, precentral gyrus) and
      posterior (superior temporal gyrus/Wernicke's area, supramarginal gyrus) cortical components of
      the distributed perisylvian phonological network can give rise to phonological dyslexia and dysgraphia.
    supports: claim
  - section: Methods
    page: 3
    quote: 'we were able to identify 31 participants for the study (mean age = 60.07 years, range: 40-78...)'
    supports: sample
  - section: Results
    page: 584
    quote: To determine if lesions involving specific perisylvian cortical subdivisions had a unique association
      with phonological dyslexia and dysgraphia, we used a 2 x 2 chi-square design
    supports: method
  - section: Discussion
    page: 588
    quote: we relied on a mix of clinical and research scans which introduced some variability in terms
      of image quality and detail.
    supports: limitation
  - section: Discussion
    page: 588
    quote: the lesion-deficit correlations used in this study required binary decisions regarding the
      presence/absence of damage to an ROI
    supports: limitation
- id: f2
  target: phonological_dyslexia
  target_kind: impairment
  claim: Damage to the left inferior frontal gyrus pars opercularis is associated with a larger lexicality
    effect in reading.
  direction: likely
  relationship: causal
  citation: '@Rapcsak2009'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 31
    population: left-hemisphere damaged patients with language impairment
    time_post_onset: subacute or chronic stage
    age_range: 40-78 years
    handedness: not_reported
    language: not_reported
    phase: chronic
  statistics:
    threshold: point-biserial correlation
    effect_size: r = .398
    p_value: '.0393'
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: atlas
    atlas: AAL
    description: posterior inferior frontal gyrus/Broca's area (BA44/45)
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: 3D inversion recovery (IR) prepped spoiled-gradient-echo sequence (SPGR)
      voxel_size_mm:
      - 1
      - 1
      - 1.5
    preprocessing_pipeline: SPM2 spatial normalization with lesion masking
    reference_space: MNI152
    atlases_used:
    - AAL
  author_limitations:
  - Relied on a mix of clinical and research scans, introducing variability in image quality.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 584
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 5
    quote: the size of the lexicality effect in reading correlated with damage to posterior inferior frontal
      gyrus/Broca's area (r = .398, p = .0393)
    supports: claim
  - section: Results
    page: 584
    quote: Point-biserial correlation tests did not indicate a significant association between damage
      to any perisylvian ROI and the magnitude of the lexicality effect in spelling... By contrast, the
      size of the lexicality effect in reading correlated with damage to posterior inferior frontal gyrus/Broca's
      area
    supports: statistics
---
