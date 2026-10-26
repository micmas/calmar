---
schema_version: 2.7
id: left_superior_longitudinal_fasciculus
name: Left Superior Longitudinal Fasciculus
kind: tract
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
hemisphere: left
findings:
- id: f1
  target: phonological_production
  target_kind: impairment
  claim: Reduced integrity of the left superior longitudinal fasciculus is associated with impaired repetition
    of spoken language, independent of cortical damage.
  direction: likely
  relationship: causal
  citation: '@Breier2008'
  method: DTI
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 20
    population: left hemisphere stroke
    time_post_onset: at least 1 month poststroke onset (mean, 22 months; SD, 24 months; range, 1–72 months)
    phase: chronic
    age_range: 38–77 years
    handedness: all premorbidly right handed
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: P < 0.017
    effect_size: F[1,18] = 15.51
    p_value: '.001'
  confounders_controlled:
  - damage to cortical areas of the left hemisphere involved in language function
  - month post-stroke onset
  - sex
  - presence of lacunar infarcts and/or periventricular WM abnormalities
  confounders_not_controlled: []
  region_definition:
    kind: manual_ROI
    description: FA values for the SLF as it runs anteroposterior, deep to the shoulder of the Sylvian
      fissure.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: DTI
      sequence: single-shot spin-echo diffusion sensitized echo-planar imaging (EPI)
      voxel_size_mm:
      - 3
      - 3
      - 3
      TR_ms: 6100
      TE_ms: 84
      n_directions: 21
      b_values:
      - 0
      - 1000
    preprocessing_pipeline: SENSE acceleration factor or k-space under-sampling of R = 2.2
    reference_space: not_reported
    atlases_used:
    - standard WM atlas
  author_limitations:
  - DTI analysis was restricted to FA value measurement, which may be non-specific.
  - Use of standard rectangular rather than tailored irregular ROIs may contribute to spuriously decreased
    FA values.
  - Poststroke reorganization is a potential confound given the large range of time since stroke.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 484
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 484
    quote: For the SLF, only the relationship between the FA value and repetition was significant (F[1,18]
      = 15.51; P = .001).
    supports: claim
  - section: Methods
    page: 483
    quote: Twenty patients aged 38–77 years with a history of stroke in the left hemisphere underwent
      diffusion tensor imaging, structural MR imaging, and language testing.
    supports: sample
  - section: Methods
    page: 483
    quote: All of the participants were at least 1 month poststroke onset (mean, 22 months; SD, 24 months;
      range, 1–72 months).
    supports: sample
  - section: Methods
    page: 484
    quote: We obtained FA values for the SLF as it runs anteroposterior, deep to the shoulder of the Sylvian
      fissure.
    supports: region_definition
  - section: Methods
    page: 483
    quote: The diffusion-weighted data were acquired using a single-shot spin-echo diffusion sensitized
      echo-planar imaging (EPI) sequence with the balanced Icosa (21 encoding directions) encoding scheme...
      a diffusion sensitization of b = 1000 s/mm2, TR of 6.1 seconds, and TE of 84 ms.
    supports: imaging_details
  - section: Discussion
    page: 486
    quote: In addition, the DTI analysis was restricted to FA value measurement. Different contributions
      to FA decrease may be present other than injury to the tract, thus potentially rendering the FA
      decreases non-specific.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
Findings from Breier et al. (2008) using DTI to correlate FA values of the SLF with WAB-R indices.
