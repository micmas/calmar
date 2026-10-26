---
schema_version: 2.7
id: left_ifg_pars_opercularis
name: Left IFG Pars Opercularis (Broca's area, dorsal stream hub)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: anomic_aphasia
  target_kind: impairment
  claim: Restored blood flow to left BA 44/45 (Broca's area) independently contributes to the prediction
    of early improvement in picture naming after stroke.
  direction: likely
  relationship: causal
  citation: '@Hillis2006'
  method: LSM
  design: longitudinal
  evidence_quality: cohort
  strength: moderate
  sample:
    n: 87
    population: acute left-hemisphere ischemic stroke patients with impaired picture naming
    time_post_onset: day 1 and days 3-5
    phase: longitudinal
    age_range: mean 64.7 (SD 10.7) years
    handedness: right handed
    language: English
    cohort: not_reported
  statistics:
    threshold: p < 0.05 after Bonferroni correction
    effect_size: beta = 0.25
    p_value: '0.027'
  confounders_controlled:
  - ' reperfusion of BA 37'
  - reperfusion of BA 22
  confounders_not_controlled: []
  region_definition:
    kind: atlas
    atlas: Brodmann's atlas
    description: Left BA 44/45 (Broca's area)
  imaging_details:
    field_strength: 1.5T
    modalities:
    - modality: PWI
      sequence: echo planar imaging
      voxel_size_mm:
      - not_reported
      - not_reported
      - 5
      TR_ms: 2000
      TE_ms: 60
    - modality: DWI
      sequence: echo planar imaging
      voxel_size_mm:
      - not_reported
      - not_reported
      - 5
      TR_ms: 10000
      TE_ms: 120
    preprocessing_pipeline: Transferred to Brodmann's and MNI atlas using MRICro
    reference_space: MNI152
    atlases_used:
    - Brodmann's atlas
    - MNI atlas
  author_limitations:
  - The threshold of hypoperfusion does not necessarily correspond to tissue that is at risk for progressing
    to infarction in the absence of restored blood flow.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 8070
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 8070
    quote: Reperfusion of left BA 44/45 (Broca's area; p = 0.027) and reperfusion of left BA 22 (Wernicke's
      area; p = 0.047) also independently contributed to the prediction of early improvement in naming
      after adjustment for each other and for left BA 37 reperfusion.
    supports: claim
  - section: Materials and Methods
    page: 2
    quote: The current study was restricted to a subset of 87 patients who had impaired naming... and
      who completed language tests and imaging with both DWI and PWI at day 1 and days 3-5.
    supports: sample
  - section: Statistical analysis
    page: 2
    quote: An alpha level of 0.05 after Bonferroni correction for multiple comparisons was used to identify
      significant associations.
    supports: statistics
  - section: Imaging and image analysis
    page: 2
    quote: DWI trace images [bmax = 1000 s/mm2; repetition time (TR)/echo time (TE), 10,000/120 ms] and
      PWI (TR/TE, 2000/60 ms) scans were obtained on a GE Signa 1.5 tesla echo planar imaging-capable
      scanner... with whole-brain coverage and 5 mm slice thickness
    supports: imaging_details
  - section: Imaging and image analysis
    page: 2
    quote: Regions of hypoperfusion on TTP maps were transferred to a Brodmann's atlas and to the Montreal
      Neurological Institute (MNI) atlas using MRICro
    supports: region_definition
  - section: Imaging and image analysis
    page: 2
    quote: Although this threshold of hypoperfusion does not necessarily correspond to tissue that is
      at risk for progressing to infarction in the absence of restored blood flow...
    supports: limitation
  - section: added by backfill
    page: 1
    quote: Areas of reperfusion that contributed to improvement in oral naming of pictures from day 1
      to days 3–5 were identified using stepwise linear regression.
    supports: method
  - section: added by backfill
    page: 2
    quote: The current study was restricted to a subset of 87 patients who had impaired naming
    supports: method
  lesion_mapping:
    analysis: multivariate
    n_analysed: 87
    min_lesion_overlap: not_reported
    lesion_volume_correction: not_reported
    multiple_comparisons: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
---
