---
schema_version: 2.3
id: left_superior_temporal_gyrus
name: Left Superior Temporal Gyrus (Dorsal Stream Node)
kind: classical
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
aliases:
- left STG
- left T1 region
- left posterior/anterior superior temporal gyrus
- left Wernicke's area region
hemisphere: left
networks:
- dorsal_language
- ventral_language
tracts_adjacent:
- left_arcuate_fasciculus_slf
- left_middle_longitudinal_fascicle
findings:
- id: f1
  target: speech_repetition
  target_kind: impairment
  claim: 'The left posterior and anterior superior temporal gyrus is activated during
    sublexical speech repetition (pseudoword > word repetition), forming the temporal
    node of the dorsal language stream involved in sublexical speech perception and
    auditory-motor mapping.

    '
  direction: likely
  relationship: recruitment
  citation: '@Saur2008'
  method: fMRI_activation
  design: cross-sectional
  imaging: fMRI
  sample:
    n: 33
    population: healthy adult volunteers (German-speaking)
    time_post_onset: not_reported (healthy controls)
    age_range: 18-71 years, mean 34 years
    handedness: 18 right-handed (mixed)
    language: German-speaking
    recruitment: Recruited from the database of the Freiburg Brain Imaging Centre.
    inclusion_criteria: Healthy volunteers.
    exclusion_criteria: not_reported
  statistics:
    threshold: P < 0.001 uncorrected (t > 3.1)
    cluster_extent: null
    effect_size: t = 4.36 (T1p), t = 3.39 (T1a)
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - only healthy volunteers — no lesion-symptom evidence
  - repetition contrast uses uncorrected threshold (p < 0.001) vs. corrected for comprehension
    — differential sensitivity may affect comparison
  region_definition:
    kind: peak_coord_sphere
    mni_peak:
    - -57
    - -36
    - 6
    radius_mm: 4
    description: 'fMRI peak voxel in the left posterior superior temporal gyrus (T1p;
      MNI -57 -36 6, t=4.36) and anterior superior temporal gyrus (T1a; MNI -57 -3
      -9, t=3.39), defined from the random-effects group analysis of the pseudoword
      > real-word repetition contrast. Each peak enlarged to 4mm sphere (33 seed voxels)
      for DTI seeding.

      '
  imaging_details:
    field_strength: 3T
    acquisition:
      sequence: EPI (event-related fMRI)
      notes: Siemens TIM Trio 3T; SPM5 preprocessing and random-effects analysis
    task:
      name: Sublexical pseudoword repetition
      description: 'Subjects overtly repeated aurally presented pseudowords vs. real
        words. Contrast of pseudoword > word isolates sublexical processing in auditory-motor
        mapping network.

        '
      contrasts:
      - Pseudoword repetition > real-word repetition
      baseline: Real-word repetition
    preprocessing_pipeline: SPM5 standard preprocessing + spatial normalization to
      MNI space
    reference_space: MNI152
    atlases_used: []
    coordinates_reported:
    - region: left posterior superior temporal gyrus (T1p)
      mni:
      - -57
      - -36
      - 6
    - region: left anterior superior temporal gyrus (T1a)
      mni:
      - -57
      - -3
      - -9
  replications: []
  contradictions: []
  author_limitations:
  - Only healthy volunteers — clinical impairment inferences are speculative.
  - The repetition contrast uses uncorrected threshold (p<0.001) — weaker statistical
    evidence than the comprehension contrast (corrected p<0.05).
  - The STG activation for repetition reflects sublexical processing demand (pseudoword
    > word); real-word repetition activates the STG too (not shown in this contrast).
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results, pages 18035-18036; Table 1, page 18036; Discussion, page
      18038
    confidence: high
    flags:
    - Repetition fMRI contrast uses uncorrected p<0.001 threshold — less stringent
      than comprehension contrast (corrected p<0.05)
    - Healthy volunteers only — no causal claim to aphasia supported by this study
    - fMRI acquisition parameters (TR, TE, voxel size) in SI Methods — not available
      in this PDF
    - target ID 'speech_repetition' is forward-looking
  source_passages:
  - section: Results
    page: 2
    quote: 'By contrasting repetition of pseudowords with real words, activation focused
      on the superior temporal gyrus in the left temporal lobe and shifted from

      '
    supports: claim
  - section: Discussion
    page: 4
    quote: 'We ascribed activation of the superior tem- poral gyrus (T1a/T1p) to sublexical
      processing steps during speech perception

      '
    supports: claim
  - section: Results – Table 1
    page: 2
    quote: 'Posterior superior temporal gyrus

      '
    supports: statistics
  - section: Methods – Participants
    page: 5
    quote: 'Thirty-three healthy volunteers (11 females, mean age 34 years, range
      18–71 years, 18 right-handed) were recruited from the database of the Freiburg
      Brain Imaging Centre.

      '
    supports: sample
  - section: Methods
    page: 5
    quote: 'In the repetition experiment, subjects were asked to overtly repeat words
      and pseudowords immediately after presentation.

      '
    supports: method
  - section: Methods
    page: 5
    quote: 'Within the major activation clusters the peak voxels were identified,
      resliced to the native space of each subject''s DTI data, and enlarged to a
      sphere with a radius of 4 mm.

      '
    supports: region_definition
notes: 'The left STG findings here are specifically the fMRI activation seeds for
  the dorsal stream

  (repetition contrast). The STG is also a key region in auditory comprehension (bilateral

  primary auditory cortex activation in the main effect), but the ventral stream seeds
  for

  the comprehension contrast shift to the MIDDLE temporal gyrus (T2a/T2p) — captured
  in

  left_middle_temporal_gyrus__Saur2008.md.

  The DTI finding linking STG to premotor cortex via AF/SLF is in

  left_arcuate_fasciculus_slf__Saur2008.md (f1).

  Target ID ''speech_repetition'' is forward-looking.'
reviewer: auto-reviewer
reviewed_on: '2026-05-06'
---
# Left Superior Temporal Gyrus (Dorsal Stream Node)

Saur et al. (2008) identify the left superior temporal gyrus (posterior: MNI -57 -36 6;
anterior: MNI -57 -3 -9) as the temporal node of the dorsal language stream, activated
preferentially during sublexical pseudoword repetition (t=4.36 and 3.39, uncorrected p<0.001).

These STG peaks served as seed regions for probabilistic DTI tractography tracing the
dorsal pathway through the AF/SLF to the left premotor cortex (BA44 and BA6). The STG is
interpreted as mediating sublexical speech perception — the early stage of auditory-motor
mapping that interfaces with premotor planning for articulation.

Note that the comprehension task also activates the STG bilaterally as a main effect
(primary auditory processing), but the comprehension contrast (meaningful > pseudo sentences)
preferentially activates the MIDDLE temporal gyrus rather than the STG, distinguishing
the dorsal from the ventral stream temporal nodes.
