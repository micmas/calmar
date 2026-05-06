---
schema_version: 2.3
id: left_middle_temporal_gyrus
name: Left Middle Temporal Gyrus (Ventral Stream Node)
kind: classical
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
aliases:
- left MTG
- left T2 region
- left posterior and anterior middle temporal gyrus
hemisphere: left
networks:
- ventral_language
tracts_adjacent:
- left_extreme_capsule
- left_middle_longitudinal_fascicle
- left_inferior_longitudinal_fascicle
findings:
- id: f1
  target: auditory_comprehension
  target_kind: impairment
  claim: 'The left posterior and anterior middle temporal gyrus is activated during
    sentence-level auditory comprehension (listening to meaningful vs. pseudo sentences),
    forming the temporal node of the ventral language stream involved in lexical-semantic
    and conceptual processing.

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
    inclusion_criteria: Healthy volunteers with no neurological history.
    exclusion_criteria: not_reported
  statistics:
    threshold: P < 0.05 corrected for multiple comparisons (t > 5.2)
    cluster_extent: null
    effect_size: t = 10.11 (T2p), t = 9.70 (T2a)
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - only healthy volunteers — no lesion-symptom data
  - handedness mixed (18/33 right-handed)
  region_definition:
    kind: peak_coord_sphere
    mni_peak:
    - -48
    - -60
    - -18
    radius_mm: 4
    description: 'fMRI peak voxel in the left posterior middle temporal gyrus (T2p;
      MNI -48 -60 -18, t=10.11) and anterior middle temporal gyrus (T2a; MNI -51 0
      -18, t=9.70), defined from the random-effects group analysis of the meaningful
      > pseudo-sentence contrast. Each peak was enlarged to a 4mm radius sphere containing
      33 seed voxels for DTI tracking.

      '
  imaging_details:
    field_strength: 3T
    acquisition:
      sequence: EPI (event-related fMRI)
      notes: Siemens TIM Trio 3T; SPM5 preprocessing and random-effects analysis
    task:
      name: Sentence comprehension
      description: 'Subjects listened to aurally presented meaningful German sentences
        vs. meaningless pseudo sentences (phoneme substitution preserving phonotactics).
        Button press at end of each stimulus.

        '
      contrasts:
      - Meaningful sentences > meaningless pseudo sentences
      baseline: Meaningless pseudo sentences
    preprocessing_pipeline: SPM5 standard preprocessing + spatial normalization to
      MNI space (Siemens TIM Trio 3T)
    reference_space: MNI152
    atlases_used: []
    coordinates_reported:
    - region: left posterior middle temporal gyrus (T2p)
      mni:
      - -48
      - -60
      - -18
    - region: left anterior middle temporal gyrus (T2a)
      mni:
      - -51
      - 0
      - -18
    - region: left fusiform gyrus (FUS)
      mni:
      - -30
      - -33
      - -18
  replications: []
  contradictions: []
  author_limitations:
  - Only healthy volunteers were studied; clinical inferences about lesion effects
    are speculative.
  - The comprehension contrast targets sentence-level semantics; single-word or sublexical
    comprehension may have partially different activation.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results, pages 18036-18037; Table 2, page 18037; Discussion, pages
      18038-18039
    confidence: high
    flags:
    - Healthy volunteers only — the MTG activation finding is recruitment (fMRI),
      not causal (no lesion data)
    - fMRI acquisition parameters (TR, TE, voxel size) referred to SI Methods — not
      available in main paper PDF
  source_passages:
  - section: Results
    page: 2
    quote: 'activation shifted to the middle and inferior temporal gyrus in the left
      temporal lobe and to the ventrolateral prefron- tal cortex in the left frontal
      lobe

      '
    supports: claim
  - section: Discussion
    page: 5
    quote: 'The middle temporal lobe was shown to participate in accessing lexical,
      semantic, and concep- tual information

      '
    supports: claim
  - section: Table 2
    page: 3
    quote: 'Posterior middle temporal gyrus

      '
    supports: statistics
  - section: Methods – Participants
    page: 5
    quote: 'Thirty-three healthy volunteers (11 females, mean age 34 years, range
      18–71 years, 18 right-handed) were recruited from the database of the Freiburg
      Brain Imaging Centre.

      '
    supports: sample
  - section: Methods – fMRI Event-Related Experiments
    page: 5
    quote: 'In the comprehension experiment, subjects were asked to listen carefully
      to all stimuli and press a button at the end of each stimulus, irrespective
      of whether they had heard a normal sentence or a pseudo sentence.

      '
    supports: method
  - section: Methods – Definition of Seed Regions
    page: 5
    quote: 'Within the major activation clusters the peak voxels were identified,
      resliced to the native space of each subject''s DTI data, and enlarged to a
      sphere with a radius of 4 mm.

      '
    supports: region_definition
notes: "The left MTG finding here is specifically the fMRI activation node for sentence\
  \ comprehension.\nThe DTI finding linking MTG to ventrolateral PFC via the extreme\
  \ capsule is captured in\nthe left_extreme_capsule__Saur2008.md draft (f1). Both\
  \ are from the same study (n=33 healthy volunteers).\nFor lesion-symptom evidence\
  \ of left MTG involvement in comprehension, see @Fridriksson2018 \n(form_to_meaning\
  \ findings) and @Mirman2015 (cited entry)."
reviewer: auto-reviewer
reviewed_on: '2026-05-06'
---
# Left Middle Temporal Gyrus (Ventral Stream Node)

Saur et al. (2008) identify the left middle temporal gyrus (posterior: MNI -48 -60 -18;
anterior: MNI -51 0 -18) as a key temporal node of the ventral language stream, strongly
activated during sentence comprehension (t=10.11 and 9.70 respectively, corrected p<0.05).

These MTG peaks served as the seed regions for probabilistic DTI tractography, which traced
the ventral pathway through the extreme capsule to the left ventrolateral prefrontal cortex
(BA45/47). The MTG is interpreted as mediating lexical, semantic, and conceptual access
during sentence comprehension.
