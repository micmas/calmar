---
schema_version: 2.3
id: left_arcuate_fasciculus_slf
name: Left Arcuate Fasciculus and Superior Longitudinal Fascicle (Dorsal Language
  Pathway)
kind: tract
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
aliases:
- left AF/SLF
- left dorsal language pathway
- left arcuate fascicle
- left SLF/AF system
- Superior longitudinal fasciculus L
- Superior longitudinal fasciculus left
hemisphere: left
members:
- left_posterior_superior_temporal_gyrus
- left_anterior_superior_temporal_gyrus
- left_ifg_pars_opercularis
- left_dorsal_premotor_cortex
networks:
- dorsal_language
findings:
- id: f1
  target: left_posterior_superior_temporal_gyrus
  target_kind: region
  claim: 'The left arcuate fasciculus and superior longitudinal fascicle (AF/SLF)
    structurally connects the left posterior and anterior superior temporal gyrus
    to the left premotor cortex (pars opercularis BA44 and dorsal premotor BA6), forming
    the dorsal white-matter pathway subserving auditory-motor mapping during speech
    repetition.

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
    threshold: P < 0.001 uncorrected (fMRI seed definition); PIBI threshold 0.0148
      (excludes 95% of voxels with PIBI < 10^-6)
    cluster_extent: null
    effect_size: not_reported
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - only healthy volunteers — no aphasia patients; generalizability to lesion populations
    assumed, not tested
  - handedness mixed (only 18/33 right-handed) — potential effect on language lateralization
    not controlled
  region_definition:
    kind: data_driven_cluster
    description: 'Probabilistic DTI tractography pathway extracted by combining probability
      maps from fMRI-defined seed regions in the superior temporal gyrus (T1a: -57
      -3 -9; T1p: -57 -36 6) with seed regions in left premotor cortex (F3op: -45
      -9 24; PMd: -48 0 36), using a novel Monte Carlo random walk (MCRW) method to
      identify the most probable connecting white-matter pathway (AF/SLF system).

      '
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: fMRI
      sequence: EPI (event-related)
      notes: Siemens TIM Trio 3T; SPM5 preprocessing; random-effects group analysis
    - modality: DTI
      notes: DTI and Fiber Toolbox (MCRW probabilistic tracking); 10^5 random walks
        per seed; max fiber length 150 voxels; white-matter mask applied
    task:
      name: Pseudoword vs. word repetition (sublexical repetition)
      description: 'Subjects overtly repeated aurally presented pseudowords and real
        words. Contrast of pseudoword repetition vs. real-word repetition isolated
        sublexical auditory-motor processing.

        '
      contrasts:
      - Pseudoword repetition > real-word repetition
      baseline: Real-word repetition
    preprocessing_pipeline: SPM5 standard preprocessing + spatial normalization to
      MNI space; DTI probability maps smoothed with isotropic 3mm Gaussian kernel
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
    - region: left IFG pars opercularis / ventral premotor (F3op, BA44)
      mni:
      - -45
      - -9
      - 24
    - region: left dorsal premotor cortex (PMd, BA6)
      mni:
      - -48
      - 0
      - 36
    - region: left deep frontal operculum (FOP)
      mni:
      - -42
      - -27
      - 0
  replications: []
  contradictions: []
  author_limitations:
  - Functional segregation into two streams was produced by an artificial experimental
    situation; in natural speech both networks may interact closely.
  - Only healthy volunteers were studied; the mapping of tract function to aphasia
    syndromes is speculative/inferred.
  - The study used a single DTI tractography method; results may differ with alternative
    tractography approaches.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results, pages 18035-18037; Discussion, page 18038; Methods, pages
      18039-18040
    confidence: high
    flags:
    - Study uses healthy volunteers only — no direct lesion-symptom evidence; causal
      inference to aphasia is interpretive, not tested
    - Handedness not fully right-handed (only 18/33); language lateralization variability
      not addressed
    - DTI acquisition parameters (voxel size, TR, TE, b-values, n-directions) not
      reported in main paper — referred to SI Methods which is not available in this
      PDF
  source_passages:
  - section: Results
    page: 2
    quote: 'T1a/T1p) are connected with the premotor seeds (F3op and PMd) via a dorsal
      route along the AF/SLF system.

      '
    supports: claim
  - section: Results
    page: 2
    quote: 'a composite fiber bundle composed of MdLF and SLF/AF constitutes the dorsal
      pathway for language.

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
    quote: 'In the repetition experiment, subjects were asked to overtly repeat words
      and pseudowords immediately after presentation.

      '
    supports: method
  - section: Methods – Probabilistic DTI-Based Fiber Tracking
    page: 6
    quote: 'Second, a Monte Carlo simulation of random walks (MCRW) similar to the
      probabilistic index of connectivity (PICo) method

      '
    supports: imaging_details
  - section: Methods – Probabilistic DTI-Based Fiber Tracking
    page: 6
    quote: 'only voxels with PIBI

      '
    supports: statistics
  - section: Discussion
    page: 5
    quote: 'in naturally occurring speech (e.g., proposi- tional speech), both networks
      interact closely to reach high

      '
    supports: limitation
- id: f2
  target: speech_repetition
  target_kind: impairment
  claim: 'The left dorsal pathway (AF/SLF connecting superior temporal gyrus to premotor
    cortex) is recruited during sublexical speech repetition, and disruption of this
    network after stroke is speculated to relate to conduction aphasia (impaired repetition
    with preserved comprehension and phonological paraphasias).

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
    threshold: P < 0.001 uncorrected (fMRI); PIBI > 0.0148 (DTI)
    cluster_extent: null
    effect_size: not_reported
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - only healthy volunteers — aphasia-related disruption claim is speculative
  - repetition vs. rest contrast not used; pseudoword > word contrast isolates sublexical
    processing
  region_definition:
    kind: data_driven_cluster
    description: 'Functionally defined via fMRI pseudoword > word repetition contrast;
      structurally confirmed by probabilistic DTI tractography linking STG seeds to
      premotor seeds via AF/SLF.

      '
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: fMRI
      sequence: EPI (event-related)
      notes: SPM5 random-effects group analysis, n=33
    - modality: DTI
      notes: MCRW probabilistic tractography; pathway defined by combining STG and
        premotor probability maps
    task:
      name: Pseudoword repetition
      description: Overt repetition of pseudowords vs. real words to isolate sublexical
        auditory-motor processing.
      contrasts:
      - Pseudoword repetition > real-word repetition
      baseline: Real-word repetition
    preprocessing_pipeline: SPM5 + MNI normalization; DTI maps smoothed 3mm isotropic
      Gaussian
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
    - region: left IFG pars opercularis (F3op, BA44)
      mni:
      - -45
      - -9
      - 24
    - region: left dorsal premotor cortex (PMd, BA6)
      mni:
      - -48
      - 0
      - 36
  replications: []
  contradictions: []
  author_limitations:
  - Disruption of the dorsal pathway relating to conduction aphasia is speculative
    — based on inference from healthy volunteers, not aphasia patient data.
  - The study does not test the dorsal pathway in patients with stroke.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Discussion, page 18038-18039
    confidence: medium
    flags:
    - Impairment inference (conduction aphasia) is speculative — authors state 'may
      relate to'; no patient data in this study
    - target ID 'speech_repetition' is forward-looking — no canonical impairment entry
      yet
  source_passages:
  - section: Discussion
    page: 4
    quote: 'Anatomical connectivity between the temporal and premotor seeds is provided
      by the dorsal AF/SLF

      '
    supports: claim
  - section: Discussion
    page: 5
    quote: 'Disruption of this network (e.g., after stroke) may relate to two aspects
      ascribed to conduction aphasia: relatively selective impairment of repetition

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
    quote: 'In isolation, this stream may suffice to produce nonpropositional speech
      and echolalia.

      '
    supports: limitation
- id: f3
  target: left_posterior_superior_temporal_gyrus
  target_kind: region
  claim: 'The left arcuate fasciculus and superior longitudinal fascicle (AF/SLF)
    structurally connects the left posterior and anterior superior temporal gyrus
    to the left premotor cortex (pars opercularis BA44 and dorsal premotor BA6), forming
    the dorsal white-matter pathway subserving auditory-motor mapping during speech
    repetition.

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
    threshold: P < 0.001 uncorrected (fMRI seed definition); PIBI threshold 0.0148
      (excludes 95% of voxels with PIBI < 10^-6)
    cluster_extent: null
    effect_size: not_reported
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - only healthy volunteers — no aphasia patients; generalizability to lesion populations
    assumed, not tested
  - handedness mixed (only 18/33 right-handed) — potential effect on language lateralization
    not controlled
  region_definition:
    kind: data_driven_cluster
    description: 'Probabilistic DTI tractography pathway extracted by combining probability
      maps from fMRI-defined seed regions in the superior temporal gyrus (T1a: -57
      -3 -9; T1p: -57 -36 6) with seed regions in left premotor cortex (F3op: -45
      -9 24; PMd: -48 0 36), using a novel Monte Carlo random walk (MCRW) method to
      identify the most probable connecting white-matter pathway (AF/SLF system).

      '
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: fMRI
      sequence: EPI (event-related)
      notes: Siemens TIM Trio 3T; SPM5 preprocessing; random-effects group analysis
    - modality: DTI
      notes: DTI and Fiber Toolbox (MCRW probabilistic tracking); 10^5 random walks
        per seed; max fiber length 150 voxels; white-matter mask applied
    task:
      name: Pseudoword vs. word repetition (sublexical repetition)
      description: 'Subjects overtly repeated aurally presented pseudowords and real
        words. Contrast of pseudoword repetition vs. real-word repetition isolated
        sublexical auditory-motor processing.

        '
      contrasts:
      - Pseudoword repetition > real-word repetition
      baseline: Real-word repetition
    preprocessing_pipeline: SPM5 standard preprocessing + spatial normalization to
      MNI space; DTI probability maps smoothed with isotropic 3mm Gaussian kernel
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
    - region: left IFG pars opercularis / ventral premotor (F3op, BA44)
      mni:
      - -45
      - -9
      - 24
    - region: left dorsal premotor cortex (PMd, BA6)
      mni:
      - -48
      - 0
      - 36
    - region: left deep frontal operculum (FOP)
      mni:
      - -42
      - -27
      - 0
  replications: []
  contradictions: []
  author_limitations:
  - Functional segregation into two streams was produced by an artificial experimental
    situation; in natural speech both networks may interact closely.
  - Only healthy volunteers were studied; the mapping of tract function to aphasia
    syndromes is speculative/inferred.
  - The study used a single DTI tractography method; results may differ with alternative
    tractography approaches.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results, pages 18035-18037; Discussion, page 18038; Methods, pages
      18039-18040
    confidence: high
    flags:
    - Study uses healthy volunteers only — no direct lesion-symptom evidence; causal
      inference to aphasia is interpretive, not tested
    - Handedness not fully right-handed (only 18/33); language lateralization variability
      not addressed
    - DTI acquisition parameters (voxel size, TR, TE, b-values, n-directions) not
      reported in main paper — referred to SI Methods which is not available in this
      PDF
  source_passages:
  - section: Results
    page: 2
    quote: 'T1a/T1p) are connected with the premotor seeds (F3op and PMd) via a dorsal
      route along the AF/SLF system.

      '
    supports: claim
  - section: Results
    page: 2
    quote: 'a composite fiber bundle composed of MdLF and SLF/AF constitutes the dorsal
      pathway for language.

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
    quote: 'In the repetition experiment, subjects were asked to overtly repeat words
      and pseudowords immediately after presentation.

      '
    supports: method
  - section: Methods – Probabilistic DTI-Based Fiber Tracking
    page: 6
    quote: 'Second, a Monte Carlo simulation of random walks (MCRW) similar to the
      probabilistic index of connectivity (PICo) method

      '
    supports: imaging_details
  - section: Methods – Probabilistic DTI-Based Fiber Tracking
    page: 6
    quote: 'only voxels with PIBI

      '
    supports: statistics
  - section: Discussion
    page: 5
    quote: 'in naturally occurring speech (e.g., proposi- tional speech), both networks
      interact closely to reach high

      '
    supports: limitation
- id: f4
  target: speech_repetition
  target_kind: impairment
  claim: 'The left dorsal pathway (AF/SLF connecting superior temporal gyrus to premotor
    cortex) is recruited during sublexical speech repetition, and disruption of this
    network after stroke is speculated to relate to conduction aphasia (impaired repetition
    with preserved comprehension and phonological paraphasias).

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
    threshold: P < 0.001 uncorrected (fMRI); PIBI > 0.0148 (DTI)
    cluster_extent: null
    effect_size: not_reported
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - only healthy volunteers — aphasia-related disruption claim is speculative
  - repetition vs. rest contrast not used; pseudoword > word contrast isolates sublexical
    processing
  region_definition:
    kind: data_driven_cluster
    description: 'Functionally defined via fMRI pseudoword > word repetition contrast;
      structurally confirmed by probabilistic DTI tractography linking STG seeds to
      premotor seeds via AF/SLF.

      '
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: fMRI
      sequence: EPI (event-related)
      notes: SPM5 random-effects group analysis, n=33
    - modality: DTI
      notes: MCRW probabilistic tractography; pathway defined by combining STG and
        premotor probability maps
    task:
      name: Pseudoword repetition
      description: Overt repetition of pseudowords vs. real words to isolate sublexical
        auditory-motor processing.
      contrasts:
      - Pseudoword repetition > real-word repetition
      baseline: Real-word repetition
    preprocessing_pipeline: SPM5 + MNI normalization; DTI maps smoothed 3mm isotropic
      Gaussian
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
    - region: left IFG pars opercularis (F3op, BA44)
      mni:
      - -45
      - -9
      - 24
    - region: left dorsal premotor cortex (PMd, BA6)
      mni:
      - -48
      - 0
      - 36
  replications: []
  contradictions: []
  author_limitations:
  - Disruption of the dorsal pathway relating to conduction aphasia is speculative
    — based on inference from healthy volunteers, not aphasia patient data.
  - The study does not test the dorsal pathway in patients with stroke.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Discussion, page 18038-18039
    confidence: medium
    flags:
    - Impairment inference (conduction aphasia) is speculative — authors state 'may
      relate to'; no patient data in this study
    - target ID 'speech_repetition' is forward-looking — no canonical impairment entry
      yet
  source_passages:
  - section: Discussion
    page: 4
    quote: 'Anatomical connectivity between the temporal and premotor seeds is provided
      by the dorsal AF/SLF

      '
    supports: claim
  - section: Discussion
    page: 5
    quote: 'Disruption of this network (e.g., after stroke) may relate to two aspects
      ascribed to conduction aphasia: relatively selective impairment of repetition

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
    quote: 'In isolation, this stream may suffice to produce nonpropositional speech
      and echolalia.

      '
    supports: limitation
reviewer: claude-cowork
reviewed_on: '2026-05-06'
last_reviewed: '2026-05-06'
---
# Left Arcuate Fasciculus / Superior Longitudinal Fascicle (Dorsal Language Pathway)

Saur et al. (2008) identify this composite fiber bundle as the structural backbone of the
dorsal language stream, connecting the superior temporal gyrus (posterior and anterior) to
the premotor cortex (BA44 pars opercularis and BA6 dorsal premotor). The pathway was defined
by combining fMRI activation seeds (from pseudoword > word repetition contrast) with
probabilistic DTI tractography using a novel Monte Carlo random-walk method.

The dorsal pathway is proposed to subserve auditory-motor mapping (mapping phonemic
representations onto articulatory representations). A speculative clinical implication offered
by the authors is that disruption of this pathway may underlie conduction aphasia.
