---
schema_version: 2.7
id: left_superior_temporal_gyrus_wernicke
name: Left Superior Temporal Gyrus (Wernicke's Area and Planum Temporale)
kind: classical
status: approved
review_tier: legacy
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
hemisphere: left
aliases:
- left STG
- Wernicke's area
- left planum temporale
- left superior temporal sulcus (posterior)
- left infra-Sylvian speech recognition region
- ventral speech recognition route
networks:
- ventral_language
- auditory_language
notes: 'Draft created 2026-05-06 from Mirman et al. 2015 (Nat Commun 6:6762).

  This entry captures the VLSM finding for the Speech Recognition factor:

  an infra-Sylvian cluster centred on the superior temporal gyrus, extending

  deep into planum temporale, with prominent involvement of Wernicke''s area.

  Shown in red-yellow in Figure 4. Approximate MNI coordinates from Figure 4

  panel labels: y = -33 to -65, z = -18 to 20. This cluster is BELOW the

  Sylvian fissure, in contrast to the supra-Sylvian production cluster.

  Together the two clusters instantiate the dorsal/ventral (production/

  recognition) division in dual-pathway models, reframed here as a

  superior/inferior peri-Sylvian division.

  '
findings:
- id: f1
  target: speech_recognition_phonological
  target_kind: impairment
  claim: 'Lesions in the left superior temporal gyrus (including Wernicke''s area)
    extending deep into the planum temporale, inferior to the Sylvian fissure, are
    associated with auditory-phonological speech recognition deficits in chronic post-stroke
    aphasia, as captured by a Speech Recognition factor loading on auditory lexical
    decision, phoneme discrimination, and rhyme discrimination tasks.

    '
  direction: likely
  relationship: causal
  citation: '@Mirman2015'
  method: VLSM
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 99
    population: chronic left-hemisphere stroke survivors with aphasia
    time_post_onset: mean 53 months post-onset (SD 68; range 1–381); 83% chronic (≥6
      months)
    age_range: mean 58 years (SD 11; range 26–79)
    handedness: premorbid right-handed
    language: English as primary language
    recruitment: Philadelphia aphasia registry (Moss Rehabilitation Research Institute
      / University of Pennsylvania).
    inclusion_criteria: ≥1 month post aphasia onset secondary to stroke; living at
      home; medically stable; CT or MRI-confirmed left hemisphere cortical lesion;
      completed all 17 tests.
    exclusion_criteria: left-handed premorbidly; right hemisphere or bilateral lesions;
      did not complete full battery.
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: FDR q = 0.05; isolated clusters ≤50 voxels removed
    cluster_extent: null
    effect_size: t-range approximately -2.67 to -5.46 (from Figure 4 colour bar, red-yellow
      scale)
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled:
  - total lesion volume (direct lesion-volume control)
  confounders_not_controlled:
  - time post-onset
  - age
  - education / premorbid IQ
  - aphasia subtype
  - hearing loss (tests are auditory but pure-tone audiometry not controlled)
  region_definition:
    kind: data_driven_cluster
    description: 'VLSM cluster for Speech Recognition factor located inferior to the
      Sylvian fissure, primarily in the superior temporal gyrus with prominent involvement
      of Wernicke''s area (posterior STG/STS) and extending deep into planum temporale.
      Shown in red-yellow in Figure 4. Approximate coronal extent y ≈ -65 to -28;
      approximate z ≈ -18 to 20. The cluster spans the full posterior-to-anterior
      extent of the superior temporal lobe along the STG, consistent with a posterior-to-anterior
      progression from phoneme to word recognition described by DeWitt & Rauschecker
      (2012) in a meta-analysis.

      '
  imaging_details:
    field_strength: 3T (primary); 1.5T for 6 participants; CT for 37 participants
    acquisition:
      sequence: MPRAGE (MRI) or CT (60 axial slices, 3 mm thick)
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 1620
      TE_ms: 3.87
    preprocessing_pipeline: 'MRI registered to custom scanner-specific template then
      MNI152 ''Colin27''. CT drawn on Colin27 after pitch rotation. Lesions manually
      segmented blinded to behaviour. VLSM in SPM8, 1000 permutations, FDR q = 0.05.

      '
    reference_space: MNI152
    atlases_used: []
    coordinates_reported:
    - region: left superior temporal gyrus / Wernicke's area (Speech Recognition cluster)
      mni:
      - null
      - null
      - null
      note: Exact MNI peak not reported numerically. Approximate range visible in
        Figure 4.
  replications:
  - '@DeWitt2012'
  contradictions: []
  author_limitations:
  - Factor analysis shows repetition and rhyme tasks cross-loaded on both Speech Production
    and Speech Recognition factors — so the infra/supra-Sylvian division is not absolute;
    many tasks recruit both.
  - Cross-sectional design; cannot infer recovery trajectory.
  - Only left hemisphere studied; cannot address contribution of right STG to speech
    recognition.
  - Anatomical alignment of lesions does not guarantee functional alignment.
  - Hearing ability not formally assessed/controlled.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – Voxel-based lesion–symptom mapping (page 3–4); Discussion
      (pages 4–5); Figure 4
    confidence: high
    flags:
    - Exact MNI peak coordinates not reported numerically; approximate range read
      from Figure 4 panel labels.
    - t-statistic range read from Figure 4 colour bar (red-yellow scale); verify in
      supplementary.
    - DeWitt & Rauschecker 2012 cited as convergent meta-analysis — confirm citation
      key in citations.md.
    - The factor analysis shows Speech Recognition also had moderate loadings on repetition
      tests — some cross-factor variance; the VLSM cluster may therefore partially
      overlap with production-related regions at uncorrected thresholds.
  source_passages:
  - section: Results – Voxel-based lesion–symptom mapping
    page: 4
    supports: claim
    quote: 'VLSM of the Speech Recognition factor identiﬁed a parallel region inferior
      to the Sylvian ﬁssure, primarily in the superior temporal gyrus, including prominent
      involvement in Wernicke''s area and extending deep into planum temporale (Fig.
      4, red–yellow).

      '
  - section: Results – Voxel-based lesion–symptom mapping
    page: 5
    supports: claim
    quote: 'Together, these two factors map the classic peri-Sylvian language regions
      and the superior-inferior division between production and recognition provides
      new evidence to reﬁne the dorsal–ventral division in dual-pathway models of
      speech processing.

      '
  - section: Discussion
    page: 5
    supports: claim
    quote: 'Our ﬁndings support the involvement of planum temporale and Wernicke''s
      area in speech recognition, but as components of the ventral route, which our
      VLSM of Speech Recognition locates deep and inferior to the Sylvian ﬁssure along
      the length of the superior temporal gyrus.

      '
  - section: Discussion
    page: 5
    supports: region_definition
    quote: 'This localization of the ventral route converges with a recent meta-analysis
      of functional neuroimaging studies that localized speech recognition processes
      to the superior temporal gyrus and revealed a posterior-to-anterior progression
      from recognition of speech sounds to spoken words in the superior temporal lobe.

      '
  - section: Results – Factor analysis
    page: 2
    supports: method
    quote: 'The third factor had high loadings from auditory lexical decision and
      phoneme discrimination tests, and moderate loadings from rhyme discrimination
      and word and nonword repetition tests. These tests capture auditory-phonolo-
      gical perception; hence, we call this factor ''Speech Recognition''.

      '
  - section: Methods – Participants
    page: 7
    supports: sample
    quote: 'The sample consisted of 43 women and 56 men, 48 African Americans and
      51 Caucasians. They averaged 58 years of age (s.d. ¼ 11; range ¼ 26–79), 14
      years of education (s.d. ¼ 3; range ¼ 10–21) and 53 months post onset of stroke
      (s.d. ¼ 68; range ¼ 1–381).

      '
  - section: Methods – Lesion analysis
    page: 8
    supports: statistics
    quote: 'The derived statistical p-map was thresholded with FDR q ¼ 0.05 (Semantic
      Recognition factor was thresholded with FDR q ¼ 0.1) and isolated clusters with
      voxel number no more than 50 after thresholding were removed.

      '
  - section: Discussion
    page: 5
    supports: limitation
    quote: 'the factor analysis showed that many tasks involve both phonological input
      and output processes. For example, word and nonword repetition, immediate serial
      recall and rhyme discrimination all loaded on both the Speech Production and
      Speech Recognition factors, although to different extents.

      '
  - section: added by backfill
    page: 7
    quote: VLSM analysis was performed by running a simple regression analysis at
      each voxel, with the lesion status as the independent variable and the factor
      score as the dependent variable.
    supports: method
  - section: added by backfill
    page: 7
    quote: Only voxels lesioned in at least 10 participants were included in analysis
    supports: method
  - section: added by backfill
    page: 8
    quote: We call this approach ‘direct total lesion volume control’.
    supports: method
  lesion_mapping:
    analysis: univariate
    n_analysed: 99
    min_lesion_overlap: 10 participants
    lesion_volume_correction: direct
    multiple_comparisons: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
- id: f2
  target: speech_recognition_phonological
  target_kind: impairment
  claim: 'Lesions in the left superior temporal gyrus (including Wernicke''s area)
    extending deep into the planum temporale, inferior to the Sylvian fissure, are
    associated with auditory-phonological speech recognition deficits in chronic post-stroke
    aphasia, as captured by a Speech Recognition factor loading on auditory lexical
    decision, phoneme discrimination, and rhyme discrimination tasks.

    '
  direction: likely
  relationship: causal
  citation: '@Mirman2015'
  method: VLSM
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 99
    population: chronic left-hemisphere stroke survivors with aphasia
    time_post_onset: mean 53 months post-onset (SD 68; range 1–381); 83% chronic (≥6
      months)
    age_range: mean 58 years (SD 11; range 26–79)
    handedness: premorbid right-handed
    language: English as primary language
    recruitment: Philadelphia aphasia registry (Moss Rehabilitation Research Institute
      / University of Pennsylvania).
    inclusion_criteria: ≥1 month post aphasia onset secondary to stroke; living at
      home; medically stable; CT or MRI-confirmed left hemisphere cortical lesion;
      completed all 17 tests.
    exclusion_criteria: left-handed premorbidly; right hemisphere or bilateral lesions;
      did not complete full battery.
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: FDR q = 0.05; isolated clusters ≤50 voxels removed
    cluster_extent: null
    effect_size: t-range approximately -2.67 to -5.46 (from Figure 4 colour bar, red-yellow
      scale)
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled:
  - total lesion volume (direct lesion-volume control)
  confounders_not_controlled:
  - time post-onset
  - age
  - education / premorbid IQ
  - aphasia subtype
  - hearing loss (tests are auditory but pure-tone audiometry not controlled)
  region_definition:
    kind: data_driven_cluster
    description: 'VLSM cluster for Speech Recognition factor located inferior to the
      Sylvian fissure, primarily in the superior temporal gyrus with prominent involvement
      of Wernicke''s area (posterior STG/STS) and extending deep into planum temporale.
      Shown in red-yellow in Figure 4. Approximate coronal extent y ≈ -65 to -28;
      approximate z ≈ -18 to 20. The cluster spans the full posterior-to-anterior
      extent of the superior temporal lobe along the STG, consistent with a posterior-to-anterior
      progression from phoneme to word recognition described by DeWitt & Rauschecker
      (2012) in a meta-analysis.

      '
  imaging_details:
    field_strength: 3T (primary); 1.5T for 6 participants; CT for 37 participants
    acquisition:
      sequence: MPRAGE (MRI) or CT (60 axial slices, 3 mm thick)
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 1620
      TE_ms: 3.87
    preprocessing_pipeline: 'MRI registered to custom scanner-specific template then
      MNI152 ''Colin27''. CT drawn on Colin27 after pitch rotation. Lesions manually
      segmented blinded to behaviour. VLSM in SPM8, 1000 permutations, FDR q = 0.05.

      '
    reference_space: MNI152
    atlases_used: []
    coordinates_reported:
    - region: left superior temporal gyrus / Wernicke's area (Speech Recognition cluster)
      mni:
      - null
      - null
      - null
      note: Exact MNI peak not reported numerically. Approximate range visible in
        Figure 4.
  replications:
  - '@DeWitt2012'
  contradictions: []
  author_limitations:
  - Factor analysis shows repetition and rhyme tasks cross-loaded on both Speech Production
    and Speech Recognition factors — so the infra/supra-Sylvian division is not absolute;
    many tasks recruit both.
  - Cross-sectional design; cannot infer recovery trajectory.
  - Only left hemisphere studied; cannot address contribution of right STG to speech
    recognition.
  - Anatomical alignment of lesions does not guarantee functional alignment.
  - Hearing ability not formally assessed/controlled.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – Voxel-based lesion–symptom mapping (page 3–4); Discussion
      (pages 4–5); Figure 4
    confidence: high
    flags:
    - Exact MNI peak coordinates not reported numerically; approximate range read
      from Figure 4 panel labels.
    - t-statistic range read from Figure 4 colour bar (red-yellow scale); verify in
      supplementary.
    - DeWitt & Rauschecker 2012 cited as convergent meta-analysis — confirm citation
      key in citations.md.
    - The factor analysis shows Speech Recognition also had moderate loadings on repetition
      tests — some cross-factor variance; the VLSM cluster may therefore partially
      overlap with production-related regions at uncorrected thresholds.
  source_passages:
  - section: Results – Voxel-based lesion–symptom mapping
    page: 4
    supports: claim
    quote: 'VLSM of the Speech Recognition factor identiﬁed a parallel region inferior
      to the Sylvian ﬁssure, primarily in the superior temporal gyrus, including prominent
      involvement in Wernicke''s area and extending deep into planum temporale (Fig.
      4, red–yellow).

      '
  - section: Results – Voxel-based lesion–symptom mapping
    page: 5
    supports: claim
    quote: 'Together, these two factors map the classic peri-Sylvian language regions
      and the superior-inferior division between production and recognition provides
      new evidence to reﬁne the dorsal–ventral division in dual-pathway models of
      speech processing.

      '
  - section: Discussion
    page: 5
    supports: claim
    quote: 'Our ﬁndings support the involvement of planum temporale and Wernicke''s
      area in speech recognition, but as components of the ventral route, which our
      VLSM of Speech Recognition locates deep and inferior to the Sylvian ﬁssure along
      the length of the superior temporal gyrus.

      '
  - section: Discussion
    page: 5
    supports: region_definition
    quote: 'This localization of the ventral route converges with a recent meta-analysis
      of functional neuroimaging studies that localized speech recognition processes
      to the superior temporal gyrus and revealed a posterior-to-anterior progression
      from recognition of speech sounds to spoken words in the superior temporal lobe.

      '
  - section: Results – Factor analysis
    page: 2
    supports: method
    quote: 'The third factor had high loadings from auditory lexical decision and
      phoneme discrimination tests, and moderate loadings from rhyme discrimination
      and word and nonword repetition tests. These tests capture auditory-phonolo-
      gical perception; hence, we call this factor ''Speech Recognition''.

      '
  - section: Methods – Participants
    page: 7
    supports: sample
    quote: 'The sample consisted of 43 women and 56 men, 48 African Americans and
      51 Caucasians. They averaged 58 years of age (s.d. ¼ 11; range ¼ 26–79), 14
      years of education (s.d. ¼ 3; range ¼ 10–21) and 53 months post onset of stroke
      (s.d. ¼ 68; range ¼ 1–381).

      '
  - section: Methods – Lesion analysis
    page: 8
    supports: statistics
    quote: 'The derived statistical p-map was thresholded with FDR q ¼ 0.05 (Semantic
      Recognition factor was thresholded with FDR q ¼ 0.1) and isolated clusters with
      voxel number no more than 50 after thresholding were removed.

      '
  - section: Discussion
    page: 5
    supports: limitation
    quote: 'the factor analysis showed that many tasks involve both phonological input
      and output processes. For example, word and nonword repetition, immediate serial
      recall and rhyme discrimination all loaded on both the Speech Production and
      Speech Recognition factors, although to different extents.

      '
  - section: added by backfill
    page: 7
    quote: VLSM analysis was performed by running a simple regression analysis at
      each voxel, with the lesion status as the independent variable and the factor
      score as the dependent variable.
    supports: method
  - section: added by backfill
    page: 7
    quote: Only voxels lesioned in at least 10 participants were included in analysis
    supports: method
  - section: added by backfill
    page: 8
    quote: We call this approach ‘direct total lesion volume control’.
    supports: method
  lesion_mapping:
    analysis: univariate
    n_analysed: 99
    min_lesion_overlap: 10 participants
    lesion_volume_correction: direct
    multiple_comparisons: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
- id: f3
  target: semantics
  target_kind: impairment
  claim: Damage to the left posterior superior temporal gyrus (Wernicke's area) was
    not significantly associated with the production of semantic naming errors.
  direction: no_effect
  relationship: causal
  citation: '@Schwartz2009'
  method: VLSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 64
    population: post-stroke aphasia
    phase: not_reported
    cohort: not_reported
  statistics:
    threshold: FDR q = 0.01
    effect_size: peak t around 1.8
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Posterior superior temporal gyrus, corresponding to Wernicke's area.
  imaging_details:
    reference_space: MNI152
    atlases_used: []
  author_limitations:
  - The study focuses on chronic patients; acute patients may show different patterns
    due to diaschisis.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 3417
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 7
    quote: As indicated in Fig. 4, there were no sig- niﬁcant voxels in the posterior
      superior temporal gyrus, corre- sponding to Wernicke's area; indeed, the peak
      t-values observed in this region were around 1.8, far below the critical t (3.27).
    supports: claim
  - section: Discussion
    page: 14
    quote: The superior temporal gyrus, including Wernicke's area in the posterior
      third, yielded low t-values in both unﬁltered and ﬁltered analyses.
    supports: claim
  - section: Discussion
    page: 14
    quote: In acute patients, tissue damage in posterior superior temporal gyrus could
      temporarily impede or suppress this residual capacity (e.g. through diaschisis),
      thereby yielding the correlation with performance that Hillis and colleagues
      observed.
    supports: limitation
  - section: added by backfill
    page: 5
    quote: Voxels in which fewer than ﬁve patients were lesioned were excluded from
      the voxel-based lesion-symptom mapping analyses.
    supports: method
  - section: added by backfill
    page: 5
    quote: A simple t-test comparing the scores between patients with and without
      lesions was performed at each voxel using the VoxBo brain imaging package
    supports: method
  - section: added by backfill
    page: 5
    quote: The resulting t-map was thresholded to control the false discovery rate
      (Genovese et al., 2002) at q = 0.01
    supports: method
  review:
    reviewer: model:gemma4:26b
    reviewed_on: '2026-10-22'
    tier: A
    extractor: agent:ollama-extract-cli/gemma4:31b-it-q8_0
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
  lesion_mapping:
    analysis: univariate
    n_analysed: 64
    min_lesion_overlap: '>= 5 patients'
    lesion_volume_correction: not_reported
    multiple_comparisons: fdr
source: draft
last_reviewed: '2026-10-22'
reviewer: claude-cowork
reviewed_on: '2026-05-06'
---
# Left Superior Temporal Gyrus (Wernicke's Area and Planum Temporale)

## Anatomical context

The left superior temporal gyrus (STG) runs along the superior surface of the
temporal lobe, below the Sylvian fissure. Its posterior portion corresponds
to the classical Wernicke's area (approximately BA 22 / posterior STG/STS).
The planum temporale lies on the superior surface of the temporal lobe
posterior to Heschl's gyrus, within the Sylvian fissure. Together, these
structures form the core of the ventral/infra-Sylvian speech recognition
pathway.

## Lesion-symptom evidence

Finding f1 (Mirman et al. 2015, n = 99, VLSM): damage to the left STG and
planum temporale is associated with auditory-phonological speech recognition
deficits (factor loading on phoneme discrimination, auditory lexical decision,
rhyme discrimination). The cluster is located INFERIOR to the Sylvian fissure
— the infra-Sylvian complement to the supra-Sylvian speech production cluster
(see entry for left_supramarginal_gyrus_premotor).

## Key theoretical implication

This finding refines dual-pathway models by placing planum temporale and
Wernicke's area on the VENTRAL (recognition) rather than the dorsal
(production) route. This contradicts some influential versions of the
dorsal stream model (e.g. Hickok & Poeppel 2007) where planum temporale
is assigned to the dorsal route for auditory-motor integration. Mirman et al.
2015 instead argue planum temporale and Wernicke's area serve speech
recognition (input), forming the infra-Sylvian portion of the ventral route.
