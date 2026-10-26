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
  target: apraxia_of_speech
  target_kind: impairment
  claim: Dysfunction (infarct or hypoperfusion) of the left posterior inferior frontal gyrus (Broca's
    area) is strongly associated with apraxia of speech in acute stroke.
  direction: likely
  relationship: causal
  citation: '@Hillis2004'
  method: LSM
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 80
    population: acute left hemisphere, non-lacunar stroke
    time_post_onset: within 24 h
    age_range: not_reported
    handedness: all right-handed
    language: English
    phase: hyperacute
    cohort: not_reported
  statistics:
    threshold: chi-square test
    effect_size: chi2(1) = 46.4
    p_value: P < 0.00001
  confounders_controlled:
  - ' insular damage status (association held in both patients with and without insular damage)'
  confounders_not_controlled: []
  region_definition:
    kind: manual_ROI
    description: Left posterior inferior frontal gyrus (Broca's area) identified on DWI and PWI.
  imaging_details:
    field_strength: 1.5 Tesla
    modalities:
    - modality: DWI
      sequence: single shot EPI
      voxel_size_mm: not_reported
      TR_ms: 10000
      TE_ms: 120
      notes: bmax = 1000 s/mm2
    - modality: PWI
      sequence: single shot gradient echo EPI
      voxel_size_mm: not_reported
      TR_ms: 2000
      TE_ms: 60
    preprocessing_pipeline: PWI hypoperfusion defined as >2.5 s delay in time to peak arrival of contrast
      relative to homologous region in intact hemisphere
    reference_space: native
    atlases_used: []
  author_limitations:
  - The behavioral tests used may have missed subtle cases of apraxia of speech.
  - Dysfunction may occur via diaschisis (deafferentation of remote cortex) without being apparent on
    DWI or PWI.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1481
    confidence: high
    flags:
    - paper refers to 'posterior inferior frontal gyrus (Broca's area)'; mapped to left_ifg_pars_opercularis
      as the closest existing KB entry
  source_passages:
  - section: Summary
    page: 1
    quote: apraxia of speech was associated with structural damage or low blood flow in left posterior
      inferior frontal gyrus.
    supports: claim
  - section: Methods - Subjects
    page: 2
    quote: 'Subjects were adults with first ever, non-lacunar, ischaemic stroke affecting the left MCA
      territory as determined by MRI. Exclusion criteria were: [...] left-handedness [...] or lack of
      proficiency in English.'
    supports: sample
  - section: Methods - Imaging
    page: 3
    quote: Scans were done on a GE Signa 1.5 Tesla, echo planar imaging (EPI)-capable system. DWI trace
      images were obtained using a multislice, isotropic, single shot EPI sequence, with bmax = 1000 s/mm2
      and repetition time (TR)/echo time (TE) of 10 000/120 ms. Single shot gradient echo EPI PWI, with
      TR/TE of 2000/60 ms, was obtained...
    supports: imaging_details
  - section: Results
    page: 3
    quote: Instead, the presence of apraxia of speech was associated with hypoperfusion and/or infarct
      of Broca's area [c2(1) = 46.4; P < 0.00001; Table 3], but not with other regions evaluated.
    supports: statistics
  - section: Methods - Neuropsychological tests
    page: 3
    quote: Thus, it should be recognized that our tests may have missed subtle apraxia of speech (in patients
      with or without insular damage).
    supports: limitation
  - section: Discussion
    page: 7
    quote: For example, a lesion may cause deafferentation of a remote area of cortex, causing dysfunction
      of that region ('diaschisis') without causing hypoperfusion apparent on PWI or bioenergetic failure
      apparent on DWI.
    supports: limitation
  - section: added by backfill
    page: not_reported
    quote: 'We studied two consecutive series of patients with acute strokes in the territory of the left
      MCA: one series of 40 patients with insular damage and one series of 40 patients without insular
      damage'
    supports: method
  - section: added by backfill
    page: not_reported
    quote: Association between apraxia of speech and each area of infarct and/or hypoperfusion was identified
      by c2.
    supports: method
  lesion_mapping:
    analysis: univariate
    n_analysed: 80
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
This finding supports the classical localization of speech articulation to Broca's area and challenges the insula-centric model proposed by @Dronkers1996.
