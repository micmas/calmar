---
schema_version: 2.6
id: left_arcuate_fasciculus
name: Left arcuate fasciculus
kind: tract
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
hemisphere: left
findings:
- id: f1
  target: phonological_production
  target_kind: impairment
  claim: Reduced integrity of the left arcuate fasciculus is associated with impaired repetition of spoken
    language, independent of cortical damage.
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
  statistics:
    threshold: P < 0.017
    effect_size: F[1,18] = 10.64
    p_value: '.004'
  confounders_controlled:
  - damage to cortical areas of the left hemisphere involved in language function
  - month post-stroke onset
  - sex
  - presence of lacunar infarcts and/or periventricular WM abnormalities
  confounders_not_controlled: []
  region_definition:
    kind: manual_ROI
    description: FA values for the AF in the portion that curves around the depth of the caudal portion
      of the Sylvian fissure, forming an arc.
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
    quote: The relationship between the FA value for the AF and the repetition AQ (F[1,18] = 10.64; P
      = .004) was significant
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
    quote: We obtained FA values for the AF in the portion that curves around the depth of the caudal
      portion of the Sylvian fissure, forming an arc.
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
- id: f2
  target: form_to_meaning
  target_kind: impairment
  claim: Damage to the left arcuate fasciculus is associated with comprehension deficits, though this
    relationship is not independent of cortical damage.
  direction: likely
  relationship: causal
  citation: '@Breier2008'
  method: DTI
  design: cross-sectional
  strength: weak
  evidence_quality: cohort
  sample:
    n: 20
    population: left hemisphere stroke
    time_post_onset: at least 1 month poststroke onset
    phase: chronic
    age_range: 38–77 years
    handedness: all premorbidly right handed
    language: not_reported
  statistics:
    threshold: P < 0.017
    effect_size: F[1,18] = 6.74
    p_value: '.018'
  confounders_controlled: []
  confounders_not_controlled:
  - damage to cortical areas of the left temporal lobe involved in comprehension
  region_definition:
    kind: manual_ROI
    description: FA values for the AF in the portion that curves around the depth of the caudal portion
      of the Sylvian fissure, forming an arc.
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
  - The relationship between damage to the AF and comprehension was not independent of cortical areas
    within the left hemisphere associated with language comprehension.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 484
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 484
    quote: the relationship with the comprehension AQ (F[1,18] = 6.74; P = .018) was marginally significant.
    supports: claim
  - section: Results
    page: 484
    quote: However, the relationship between comprehension and damage to the AF did not [remain significant]
      [when using cortical ratings as covariates].
    supports: claim
  - section: Discussion
    page: 485
    quote: whereas damage to the SLF and AF may both contribute independently to repetition deficits after
      stroke, comprehension deficits may be either mediated through or moderated by cortical damage to
      left temporal lobe language areas.
    supports: limitation
---

Findings from Breier et al. (2008) using DTI to correlate FA values of the AF and SLF with WAB-R indices.
