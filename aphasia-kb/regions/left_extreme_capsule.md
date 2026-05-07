---
schema_version: 2.3
id: left_extreme_capsule
name: Left Extreme Capsule (Ventral Language Pathway)
kind: tract
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
aliases:
- left EmC
- left extreme capsule fiber system (ECFS)
- left ventral language pathway
hemisphere: left
members:
- left_posterior_middle_temporal_gyrus
- left_anterior_middle_temporal_gyrus
- left_fusiform_gyrus
- left_ifg_pars_triangularis
- left_ifg_pars_orbitalis
networks:
- ventral_language
tracts_adjacent:
- left_middle_longitudinal_fascicle
- left_inferior_longitudinal_fascicle
findings:
- id: f1
  target: left_posterior_middle_temporal_gyrus
  target_kind: region
  claim: 'The left extreme capsule (EmC) structurally connects the left posterior
    and anterior middle temporal gyrus and fusiform gyrus to the left ventrolateral
    prefrontal cortex (pars triangularis BA45 and pars orbitalis BA47), forming the
    ventral white-matter pathway subserving sentence-level auditory comprehension
    (sound-to-meaning mapping).

    '
  direction: likely
  relationship: correlational
  citation: '@Saur2008'
  method:
  - DTI
  - fMRI_activation
  design: cross-sectional
  imaging: multimodal
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
    threshold: P < 0.05 corrected for multiple comparisons (fMRI comprehension contrast,
      t > 5.2); PIBI > 0.0148 (DTI)
    cluster_extent: null
    effect_size: not_reported
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - only healthy volunteers — no lesion-symptom evidence; clinical inferences are
    interpretive
  - handedness mixed (only 18/33 right-handed)
  - the EmC must be distinguished from the uncinate fascicle (limbic) and external
    capsule (corticostriatal) — this distinction is discussed by authors but relies
    on anatomical landmarks, not confirmed by histology
  region_definition:
    kind: data_driven_cluster
    description: 'Probabilistic DTI tractography pathway extracted by combining probability
      maps from fMRI-defined seed regions in the left middle temporal gyrus (T2p:
      -48 -60 -18; T2a: -51 0 -18) and fusiform gyrus (FUS: -30 -33 -18) with seed
      regions in left ventrolateral PFC (F3tri: -48 -27 12 BA45; F3orb: -45 -27 12
      BA47), using MCRW probabilistic tractography; the resulting pathway traverses
      the extreme capsule entering medially to the insula into the orbitofrontal cortex.

      '
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: fMRI
      sequence: EPI (event-related)
      notes: Siemens TIM Trio 3T; SPM5 random-effects group analysis, n=33; corrected
        threshold t > 5.2
    - modality: DTI
      notes: DTI and Fiber Toolbox MCRW probabilistic tracking; 10^5 random walks;
        white-matter mask; max 150 voxels fiber length
    task:
      name: Meaningful sentence comprehension
      description: 'Subjects listened to aurally presented meaningful German sentences
        vs. meaningless pseudo sentences (phoneme substitution preserving phonotactics).
        Subjects pressed a button at the end of each stimulus regardless of type.

        '
      contrasts:
      - Meaningful sentences > meaningless pseudo sentences
      baseline: Meaningless pseudo sentences
    preprocessing_pipeline: SPM5 standard preprocessing + spatial normalization to
      MNI space; DTI probability maps smoothed with isotropic 3mm Gaussian kernel
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
    - region: left IFG pars triangularis (F3tri, BA45)
      mni:
      - -48
      - -27
      - 12
    - region: left IFG pars orbitalis (F3orb, BA47)
      mni:
      - -45
      - -27
      - 12
  replications: []
  contradictions: []
  author_limitations:
  - Functional segregation into two streams is an artificial experimental result;
    in natural speech both networks interact.
  - Only healthy volunteers were studied; direct clinical evidence requires patient
    studies.
  - The EmC must be distinguished from the uncinate fascicle and external capsule,
    which requires careful anatomical delineation.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results pages 18036-18037; Discussion pages 18037-18039; Methods
      pages 18039-18040
    confidence: high
    flags:
    - Study uses healthy volunteers only — no lesion-symptom evidence linking EmC
      damage to comprehension deficits
    - DTI acquisition parameters (voxel size, b-values, n-directions, TR, TE) referred
      to SI Methods — not available in this PDF
    - 'Coordinates in Table 2 for fMRI use sign convention requiring verification:
      T2p listed as -48 -60 -18 matches the text description ''posterior middle temporal
      gyrus'''
  source_passages:
  - section: Results
    page: 3
    quote: 'all temporal and frontal nodes are connected via a strong ventral pathway
      running through the extreme capsule (EmC) and entering medially to the insula
      into the orbitofrontal cortex.

      '
    supports: claim
  - section: Results
    page: 3
    quote: 'Thus the EmC is the ventral association pathway connecting the anterior
      temporal lobe with the ventrolateral prefrontal cortex.

      '
    supports: region_definition
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
  - section: Methods – Probabilistic DTI-Based Fiber Tracking
    page: 6
    quote: 'poral maps were combined permutatively with all frontal maps.

      '
    supports: imaging_details
  - section: Results – Table 2
    page: 3
    quote: 'Statistical threshold was set at P

      '
    supports: statistics
  - section: Discussion
    page: 4
    quote: 'The ventral pathway along the EmC is in line with DTI findings in humans
      and autoradiographic tracing studies in monkeys.

      '
    supports: claim
  - section: Discussion
    page: 5
    quote: 'Disturbance of this ventral pathway may lead to transcortical sensory
      aphasia, a syndrome characterized by poor comprehension but preserved repetition
      and production.

      '
    supports: limitation
- id: f2
  target: auditory_comprehension
  target_kind: impairment
  claim: 'The left extreme capsule (ventral pathway) is recruited during sentence-level
    auditory comprehension (sound-to-meaning mapping), and its disruption is speculated
    to produce transcortical sensory aphasia (poor comprehension with preserved repetition).

    '
  direction: likely
  relationship: recruitment
  citation: '@Saur2008'
  method:
  - fMRI_activation
  - DTI
  design: cross-sectional
  imaging: multimodal
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
    threshold: P < 0.05 corrected (fMRI; t > 5.2); PIBI > 0.0148 (DTI)
    cluster_extent: null
    effect_size: not_reported
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - only healthy volunteers — aphasia impairment inference is speculative
  - the comprehension task used sentence-level stimuli; single-word or sublexical
    comprehension may activate different subnetworks
  region_definition:
    kind: data_driven_cluster
    description: 'Functionally defined via fMRI meaningful > pseudo-sentence listening
      contrast; structurally confirmed by probabilistic DTI tractography linking MTG/fusiform
      seeds to ventrolateral PFC (BA45/47) seeds via the extreme capsule.

      '
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: fMRI
      sequence: EPI (event-related)
      notes: SPM5 random-effects group analysis; corrected threshold
    - modality: DTI
      notes: MCRW probabilistic tractography
    task:
      name: Sentence comprehension (meaningful vs. pseudo sentences)
      description: 'Subjects listened to meaningful vs. meaningless pseudo sentences.
        Contrast isolates lexical-semantic sentence comprehension.

        '
      contrasts:
      - Meaningful sentences > meaningless pseudo sentences
      baseline: Meaningless pseudo sentences
    preprocessing_pipeline: SPM5 + MNI normalization; DTI maps smoothed 3mm isotropic
      Gaussian
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
    - region: left IFG pars triangularis (F3tri, BA45)
      mni:
      - -48
      - -27
      - 12
    - region: left IFG pars orbitalis (F3orb, BA47)
      mni:
      - -45
      - -27
      - 12
  replications: []
  contradictions: []
  author_limitations:
  - Transcortical sensory aphasia inference is speculative — no patient data in this
    study.
  - The comprehension task targeted only sentence-level semantic processing; word-level
    comprehension is not directly assessed.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Discussion, pages 18038-18039
    confidence: medium
    flags:
    - Auditory comprehension impairment inference is speculative — authors state 'may
      lead to transcortical sensory aphasia'; no patient data
    - target ID 'auditory_comprehension' is forward-looking — no canonical impairment
      entry yet
  source_passages:
  - section: Discussion
    page: 5
    quote: 'the contrast between listening to normal sentences and pseudo sentences
      activated middle and inferior temporal regions and the ventrolateral prefrontal
      cortex (BA 45, 47)

      '
    supports: claim
  - section: Discussion
    page: 5
    quote: 'Disturbance of this ventral pathway may lead to transcortical sensory
      aphasia, a syndrome characterized by poor comprehension but preserved repetition
      and production.

      '
    supports: claim
  - section: Methods – Participants
    page: 5
    quote: 'Thirty-three healthy volunteers (11 females, mean age 34 years, range
      18–71 years, 18 right-handed) were recruited from the database of the Freiburg
      Brain Imaging Centre.

      '
    supports: sample
  - section: Discussion
    page: 5
    quote: 'Structurally, this interaction is provided by the EmC. With this pathway,
      it might be speculated, children learn to derive meaning and construct knowledge.

      '
    supports: limitation
- id: f3
  target: left_posterior_middle_temporal_gyrus
  target_kind: region
  claim: 'The left extreme capsule (EmC) structurally connects the left posterior
    and anterior middle temporal gyrus and fusiform gyrus to the left ventrolateral
    prefrontal cortex (pars triangularis BA45 and pars orbitalis BA47), forming the
    ventral white-matter pathway subserving sentence-level auditory comprehension
    (sound-to-meaning mapping).

    '
  direction: likely
  relationship: correlational
  citation: '@Saur2008'
  method:
  - DTI
  - fMRI_activation
  design: cross-sectional
  imaging: multimodal
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
    threshold: P < 0.05 corrected for multiple comparisons (fMRI comprehension contrast,
      t > 5.2); PIBI > 0.0148 (DTI)
    cluster_extent: null
    effect_size: not_reported
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - only healthy volunteers — no lesion-symptom evidence; clinical inferences are
    interpretive
  - handedness mixed (only 18/33 right-handed)
  - the EmC must be distinguished from the uncinate fascicle (limbic) and external
    capsule (corticostriatal) — this distinction is discussed by authors but relies
    on anatomical landmarks, not confirmed by histology
  region_definition:
    kind: data_driven_cluster
    description: 'Probabilistic DTI tractography pathway extracted by combining probability
      maps from fMRI-defined seed regions in the left middle temporal gyrus (T2p:
      -48 -60 -18; T2a: -51 0 -18) and fusiform gyrus (FUS: -30 -33 -18) with seed
      regions in left ventrolateral PFC (F3tri: -48 -27 12 BA45; F3orb: -45 -27 12
      BA47), using MCRW probabilistic tractography; the resulting pathway traverses
      the extreme capsule entering medially to the insula into the orbitofrontal cortex.

      '
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: fMRI
      sequence: EPI (event-related)
      notes: Siemens TIM Trio 3T; SPM5 random-effects group analysis, n=33; corrected
        threshold t > 5.2
    - modality: DTI
      notes: DTI and Fiber Toolbox MCRW probabilistic tracking; 10^5 random walks;
        white-matter mask; max 150 voxels fiber length
    task:
      name: Meaningful sentence comprehension
      description: 'Subjects listened to aurally presented meaningful German sentences
        vs. meaningless pseudo sentences (phoneme substitution preserving phonotactics).
        Subjects pressed a button at the end of each stimulus regardless of type.

        '
      contrasts:
      - Meaningful sentences > meaningless pseudo sentences
      baseline: Meaningless pseudo sentences
    preprocessing_pipeline: SPM5 standard preprocessing + spatial normalization to
      MNI space; DTI probability maps smoothed with isotropic 3mm Gaussian kernel
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
    - region: left IFG pars triangularis (F3tri, BA45)
      mni:
      - -48
      - -27
      - 12
    - region: left IFG pars orbitalis (F3orb, BA47)
      mni:
      - -45
      - -27
      - 12
  replications: []
  contradictions: []
  author_limitations:
  - Functional segregation into two streams is an artificial experimental result;
    in natural speech both networks interact.
  - Only healthy volunteers were studied; direct clinical evidence requires patient
    studies.
  - The EmC must be distinguished from the uncinate fascicle and external capsule,
    which requires careful anatomical delineation.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results pages 18036-18037; Discussion pages 18037-18039; Methods
      pages 18039-18040
    confidence: high
    flags:
    - Study uses healthy volunteers only — no lesion-symptom evidence linking EmC
      damage to comprehension deficits
    - DTI acquisition parameters (voxel size, b-values, n-directions, TR, TE) referred
      to SI Methods — not available in this PDF
    - 'Coordinates in Table 2 for fMRI use sign convention requiring verification:
      T2p listed as -48 -60 -18 matches the text description ''posterior middle temporal
      gyrus'''
  source_passages:
  - section: Results
    page: 3
    quote: 'all temporal and frontal nodes are connected via a strong ventral pathway
      running through the extreme capsule (EmC) and entering medially to the insula
      into the orbitofrontal cortex.

      '
    supports: claim
  - section: Results
    page: 3
    quote: 'Thus the EmC is the ventral association pathway connecting the anterior
      temporal lobe with the ventrolateral prefrontal cortex.

      '
    supports: region_definition
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
  - section: Methods – Probabilistic DTI-Based Fiber Tracking
    page: 6
    quote: 'poral maps were combined permutatively with all frontal maps.

      '
    supports: imaging_details
  - section: Results – Table 2
    page: 3
    quote: 'Statistical threshold was set at P

      '
    supports: statistics
  - section: Discussion
    page: 4
    quote: 'The ventral pathway along the EmC is in line with DTI findings in humans
      and autoradiographic tracing studies in monkeys.

      '
    supports: claim
  - section: Discussion
    page: 5
    quote: 'Disturbance of this ventral pathway may lead to transcortical sensory
      aphasia, a syndrome characterized by poor comprehension but preserved repetition
      and production.

      '
    supports: limitation
- id: f4
  target: auditory_comprehension
  target_kind: impairment
  claim: 'The left extreme capsule (ventral pathway) is recruited during sentence-level
    auditory comprehension (sound-to-meaning mapping), and its disruption is speculated
    to produce transcortical sensory aphasia (poor comprehension with preserved repetition).

    '
  direction: likely
  relationship: recruitment
  citation: '@Saur2008'
  method:
  - fMRI_activation
  - DTI
  design: cross-sectional
  imaging: multimodal
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
    threshold: P < 0.05 corrected (fMRI; t > 5.2); PIBI > 0.0148 (DTI)
    cluster_extent: null
    effect_size: not_reported
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - only healthy volunteers — aphasia impairment inference is speculative
  - the comprehension task used sentence-level stimuli; single-word or sublexical
    comprehension may activate different subnetworks
  region_definition:
    kind: data_driven_cluster
    description: 'Functionally defined via fMRI meaningful > pseudo-sentence listening
      contrast; structurally confirmed by probabilistic DTI tractography linking MTG/fusiform
      seeds to ventrolateral PFC (BA45/47) seeds via the extreme capsule.

      '
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: fMRI
      sequence: EPI (event-related)
      notes: SPM5 random-effects group analysis; corrected threshold
    - modality: DTI
      notes: MCRW probabilistic tractography
    task:
      name: Sentence comprehension (meaningful vs. pseudo sentences)
      description: 'Subjects listened to meaningful vs. meaningless pseudo sentences.
        Contrast isolates lexical-semantic sentence comprehension.

        '
      contrasts:
      - Meaningful sentences > meaningless pseudo sentences
      baseline: Meaningless pseudo sentences
    preprocessing_pipeline: SPM5 + MNI normalization; DTI maps smoothed 3mm isotropic
      Gaussian
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
    - region: left IFG pars triangularis (F3tri, BA45)
      mni:
      - -48
      - -27
      - 12
    - region: left IFG pars orbitalis (F3orb, BA47)
      mni:
      - -45
      - -27
      - 12
  replications: []
  contradictions: []
  author_limitations:
  - Transcortical sensory aphasia inference is speculative — no patient data in this
    study.
  - The comprehension task targeted only sentence-level semantic processing; word-level
    comprehension is not directly assessed.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Discussion, pages 18038-18039
    confidence: medium
    flags:
    - Auditory comprehension impairment inference is speculative — authors state 'may
      lead to transcortical sensory aphasia'; no patient data
    - target ID 'auditory_comprehension' is forward-looking — no canonical impairment
      entry yet
  source_passages:
  - section: Discussion
    page: 5
    quote: 'the contrast between listening to normal sentences and pseudo sentences
      activated middle and inferior temporal regions and the ventrolateral prefrontal
      cortex (BA 45, 47)

      '
    supports: claim
  - section: Discussion
    page: 5
    quote: 'Disturbance of this ventral pathway may lead to transcortical sensory
      aphasia, a syndrome characterized by poor comprehension but preserved repetition
      and production.

      '
    supports: claim
  - section: Methods – Participants
    page: 5
    quote: 'Thirty-three healthy volunteers (11 females, mean age 34 years, range
      18–71 years, 18 right-handed) were recruited from the database of the Freiburg
      Brain Imaging Centre.

      '
    supports: sample
  - section: Discussion
    page: 5
    quote: 'Structurally, this interaction is provided by the EmC. With this pathway,
      it might be speculated, children learn to derive meaning and construct knowledge.

      '
    supports: limitation
notes: 'This is a healthy-volunteer fMRI + DTI study. The extreme capsule finding
  is correlational

  (DTI structural connectivity) and recruitment (fMRI activation) — NOT causal.

  The inference to transcortical sensory aphasia is speculative, made by the authors
  in the Discussion.

  No aphasia patients were studied. The EmC must be distinguished from the uncinate
  fascicle

  (limbic, amygdala-hippocampus to PFC) and the external capsule (corticostriatal).

  The target ID ''auditory_comprehension'' is forward-looking.'
reviewer: claude-cowork
reviewed_on: '2026-05-06'
last_reviewed: '2026-05-06'
---
# Left Extreme Capsule (Ventral Language Pathway)

Saur et al. (2008) identify the left extreme capsule as the structural backbone of the
ventral language stream, connecting the left middle temporal gyrus and fusiform gyrus to
the left ventrolateral prefrontal cortex (BA45 pars triangularis and BA47 pars orbitalis).
The pathway was defined by combining fMRI seeds (from meaningful > pseudo-sentence listening
contrast) with probabilistic DTI tractography.

Two additional temporal tracts contribute fibers to the extreme capsule: the middle
longitudinal fascicle (MdLF, from superior temporal lobe) and inferior longitudinal
fascicle (ILF, from fusiform gyrus looping back in the caudal temporal lobe).

The ventral pathway is proposed to subserve lexical-semantic processing and the sound-to-meaning
interface. Disruption is speculated to underlie transcortical sensory aphasia.
