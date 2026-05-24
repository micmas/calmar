---
schema_version: 2.3
id: left_superior_temporal_gyrus__Leff2009
name: Left Posterior Superior Temporal Gyrus and Sulcus (Auditory STM / Comprehension
  Shared Substrate)
kind: region
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
hemisphere: left
aliases:
- left posterior STG
- left superior temporal sulcus (posterior)
- left planum temporale (inferior margin)
- left Heschl's gyrus (lateral to)
networks:
- auditory_language
- ventral_language
- short_term_memory
notes: 'Draft created 2026-05-06 from Leff et al. 2009 (Brain 132:3401-3410, doi:10.1093/brain/awp273).
  UCL cohort, n=210 stroke patients. Novel voxel-based morphometry (VBM) lesion analysis
  using continuous grey matter density values rather than binary lesion maps. Peak
  MNI coordinate of the STM-specific cluster (Analysis 2): [-66, -32, 4]. Key finding:
  a single focal region of left posterior STG predicts both auditory short-term memory
  capacity (digit span, controlling for production/perception/executive confounds)
  AND spoken sentence comprehension ability — supporting a shared substrate model.
  Distinct from Mirman2015 STG entry (USC/MUSC cohort, VLSM, different method).

  '
findings:
- id: f1
  target: auditory_short_term_memory_capacity
  target_kind: impairment
  claim: 'Structural integrity of a focal region of the left posterior superior temporal
    gyrus and sulcus, lateral and posterior to Heschl''s gyrus and overlapping with
    the inferior planum temporale, is causally necessary for auditory short-term memory
    capacity (digit span), even after controlling for speech production, speech perception,
    non-word repetition, verbal fluency, picture naming, and stroke volume.

    '
  direction: likely
  relationship: causal
  citation: '@Leff2009'
  method: VBCM
  design: cross-sectional
  imaging: T1-structural
  sample:
    n: 210
    population: chronic left- and right-hemisphere stroke patients with digit span
      ≥ 2
    time_post_onset: median 35 months (IQR 12–74 months); minimum 1 month; 26% < 12
      months
    age_range: mean 59 years (SD 14)
    handedness: 89% right-handed
    language: English as first (84%) or dominant (16%) language
    recruitment: ongoing UCL research database (Wellcome Trust Centre for Neuroimaging)
    inclusion_criteria: history of stroke; high-resolution T1 MRI; behavioural measures
      available; digit span ≥ 2
    exclusion_criteria: digit span 0–1 (to exclude severe output disorders); other
      neurological/major psychiatric disorder
  statistics:
    threshold: p < 0.05 FWE-corrected across whole brain; extent ≥ 25 contiguous voxels
    cluster_extent: 25 voxels minimum
    effect_size: Z = 5.26 (Analysis 2 peak, posterior STG at [-66, -32, 4])
    ci_95: not_reported
    p_value: < 0.05 FWE (whole brain corrected)
  confounders_controlled:
  - auditory word repetition
  - auditory non-word repetition
  - verbal fluency (category + phonological)
  - picture naming
  - stroke volume (estimated via automated lesion segmentation)
  - age (linear and quadratic)
  - time since stroke
  confounders_not_controlled:
  - hearing loss (no audiometric testing)
  - education / premorbid IQ
  - aphasia subtype
  - right hemisphere lesions included (though left predominated)
  - mood / motivation
  region_definition:
    kind: peak_coord_sphere
    description: 'Posterior superior temporal gyrus and sulcus, lateral and posterior
      to Heschl''s gyrus (primary auditory cortex), overlapping with the inferior
      portion of the planum temporale. MNI peak [-66, -32, 4] from Analysis 2 (the
      key analysis controlling for generic cognitive confounds). Analysis 1 peak (uncontrolled)
      was at [-66, -32, 6] with infinite Z-score. Analysis 3 (additionally controlling
      for spoken word and written sentence comprehension) peak: [-56, -26, 12].

      '
  imaging_details:
    field_strength: 1.5T (Siemens Sonata)
    modalities:
    - modality: T1
      sequence: 3D modified driven equilibrium Fourier transform (MDEFT)
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 12.24
      TE_ms: 3.56
    preprocessing_pipeline: 'SPM5; unified segmentation normalisation to MNI space
      (optimised for focal lesions; Seghier et al. 2008 automated lesion detection
      algorithm); smoothed 8 mm FWHM isotropic kernel; continuous grey matter probability
      images entered into multiple regression general linear model.

      '
    reference_space: MNI305
    atlases_used: []
    coordinates_reported:
    - region: Left posterior STG (Analysis 2 — auditory STM capacity controlling for
        confounds)
      mni:
      - -66
      - -32
      - 4
      note: Z = 5.26, FWE p < 0.05, extent ≥ 25 voxels
    - region: Left posterior STG (Analysis 1 — digit span alone)
      mni:
      - -66
      - -32
      - 6
      note: Z = Inf (first in table)
    - region: Left posterior STG (Analysis 3 — additionally controlling for comprehension)
      mni:
      - -56
      - -26
      - 12
      note: Z = 5.15, FWE p < 0.05
  replications:
  - '@Buchsbaum2001'
  - '@Becker1999'
  contradictions:
  - '@Warrington1969'
  - '@Shallice1977'
  author_limitations:
  - Continuous VBM method cannot detect damage in regions with only partial grey matter
    loss that still functions normally.
  - Patients with digit span 0–1 excluded — most severe output/memory deficits unrepresented.
  - Cross-sectional; cannot address recovery trajectory.
  - Right hemisphere patients included; left-hemisphere-specific effects assumed but
    not exclusively tested.
  - Hearing loss not formally controlled.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results (Analyses 1–2), Table 1, Figures 3–4; Discussion pp. 3407–3409
    confidence: high
    flags:
    - Scanner was 1.5T; reference space reported as MNI but method uses unified segmentation
      — likely MNI305 (SPM5 default).
    - Analysis 1 STG peak is listed as Z=Inf in Table 1, indicating saturation; actual
      Z not recoverable from paper.
    - All analyses used SPM5 VBM on continuous grey matter images, NOT binary lesion
      maps — methodology distinct from VLSM studies.
  source_passages:
  - section: Abstract
    page: 1
    supports: claim
    quote: structural integrity of a posterior region of the superior temporal gyrus
      and sulcus predicted auditory short-term memory capacity
  - section: Results
    page: 6
    supports: claim
    quote: identified a cortical region where grey matter density covaried with digit
      span despite the inclusion of these five extra control regressors
  - section: Discussion
    page: 8
    supports: region_definition
    quote: posterior superior temporal gyrus and sulcus lateral and posterior to Heschl's
      gyrus, overlapping with the most inferior portion of the planum temporale
  - section: Table 1
    page: 8
    supports: statistics
    quote: Superior temporal gyrus (posterior) -66 -32 4 5.26
  - section: Methods — Subjects
    page: 3
    supports: sample
    quote: Two hundred and ten patients were identified from a large, ongoing research
      database compiled for studying the structure-function relationships
- id: f2
  target: spoken_sentence_comprehension
  target_kind: impairment
  claim: 'Structural integrity of the left posterior superior temporal gyrus (same
    region supporting auditory STM capacity) also predicts spoken sentence comprehension
    ability, but NOT single spoken word comprehension or written sentence comprehension,
    consistent with a shared substrate for auditory STM and propositional speech comprehension.

    '
  direction: likely
  relationship: causal
  citation: '@Leff2009'
  method: VBCM
  design: cross-sectional
  imaging: T1-structural
  sample:
    n: 210
    population: chronic left- and right-hemisphere stroke patients
    time_post_onset: median 35 months (IQR 12–74 months)
    age_range: mean 59 years (SD 14)
    handedness: 89% right-handed
    language: English (first or dominant)
    recruitment: UCL Wellcome Trust Centre for Neuroimaging research database
    inclusion_criteria: same as f1
    exclusion_criteria: same as f1
  statistics:
    threshold: r(199) = 0.22, p = 0.002 (spoken sentence comprehension); non-significant
      for single words r = -0.03, p = 0.66; and written sentences r = 0.05, p = 0.45
    cluster_extent: not_reported
    effect_size: r = 0.22
    ci_95: not_reported
    p_value: '0.002'
  confounders_controlled:
  - same five regressors as Analysis 2 (repetition, fluency, naming, stroke volume)
  - age (linear and quadratic)
  - time since stroke
  confounders_not_controlled:
  - hearing loss
  - education / premorbid IQ
  - no active control modality task correction
  region_definition:
    kind: peak_coord_sphere
    description: 'Principal eigenvariate extracted from the Analysis 2 cluster (left
      posterior STG/sulcus, peak MNI [-66, -32, 4]) used as predictor for each comprehension
      measure in partial regression analyses.

      '
  imaging_details:
    field_strength: 1.5T (Siemens Sonata)
    modalities:
    - modality: T1
      sequence: 3D MDEFT
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 12.24
      TE_ms: 3.56
    preprocessing_pipeline: Same as f1; principal eigenvariate from Analysis 2 cluster
      used in partial regressions.
    reference_space: MNI305
    atlases_used: []
    coordinates_reported:
    - region: Left posterior STG (STM capacity cluster, used as predictor)
      mni:
      - -66
      - -32
      - 4
      note: Same cluster as f1 Analysis 2
  replications:
  - '@Crinion2003'
  - '@Spitsyna2006'
  contradictions:
  - '@Butterworth1986'
  author_limitations:
  - Correlation between STG integrity and spoken sentence comprehension (r=0.22) is
    modest, indicating other regions also contribute.
  - Cannot rule out that adjacency of structures (rather than functional sharing)
    explains co-occurrence of STM and comprehension deficits.
  - Single time-point; cannot address recovery.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results pp. 3406; Discussion pp. 3408–3409
    confidence: high
    flags:
    - Correlation r=0.22 is statistically significant but modest; effect size is smaller
      than the primary digit-span finding.
    - Dissociation from written sentence comprehension (r=0.05, ns) is a key theoretical
      claim — supports auditory-specific storage.
  source_passages:
  - section: Results
    page: 6
    supports: claim
    quote: significant correlation between the structural integrity of this region
      and spoken sentence comprehension score, r(199) = 0.22, P = 0.002
  - section: Results
    page: 6
    supports: claim
    quote: grey matter density in a region important for auditory short-term memory
      capacity correlated more strongly with comprehension of spoken sentences than
      with comprehension of either single words or written sentences
  - section: Conclusion
    page: 9
    supports: claim
    quote: identified the left posterior superior temporal gyrus and sulcus as the
      substrate mediating the capacity of auditory short-term memory
  - section: Discussion
    page: 8
    supports: region_definition
    quote: it is the posterior superior temporal gyrus and sulcus rather than the
      inferior parietal lobe that is necessary for intact auditory short-term memory
      capacity
- id: f3
  target: auditory_short_term_memory_capacity
  target_kind: impairment
  claim: 'Structural integrity of a focal region of the left posterior superior temporal
    gyrus and sulcus, lateral and posterior to Heschl''s gyrus and overlapping with
    the inferior planum temporale, is causally necessary for auditory short-term memory
    capacity (digit span), even after controlling for speech production, speech perception,
    non-word repetition, verbal fluency, picture naming, and stroke volume.

    '
  direction: likely
  relationship: causal
  citation: '@Leff2009'
  method: VBCM
  design: cross-sectional
  imaging: T1-structural
  sample:
    n: 210
    population: chronic left- and right-hemisphere stroke patients with digit span
      ≥ 2
    time_post_onset: median 35 months (IQR 12–74 months); minimum 1 month; 26% < 12
      months
    age_range: mean 59 years (SD 14)
    handedness: 89% right-handed
    language: English as first (84%) or dominant (16%) language
    recruitment: ongoing UCL research database (Wellcome Trust Centre for Neuroimaging)
    inclusion_criteria: history of stroke; high-resolution T1 MRI; behavioural measures
      available; digit span ≥ 2
    exclusion_criteria: digit span 0–1 (to exclude severe output disorders); other
      neurological/major psychiatric disorder
  statistics:
    threshold: p < 0.05 FWE-corrected across whole brain; extent ≥ 25 contiguous voxels
    cluster_extent: 25 voxels minimum
    effect_size: Z = 5.26 (Analysis 2 peak, posterior STG at [-66, -32, 4])
    ci_95: not_reported
    p_value: < 0.05 FWE (whole brain corrected)
  confounders_controlled:
  - auditory word repetition
  - auditory non-word repetition
  - verbal fluency (category + phonological)
  - picture naming
  - stroke volume (estimated via automated lesion segmentation)
  - age (linear and quadratic)
  - time since stroke
  confounders_not_controlled:
  - hearing loss (no audiometric testing)
  - education / premorbid IQ
  - aphasia subtype
  - right hemisphere lesions included (though left predominated)
  - mood / motivation
  region_definition:
    kind: peak_coord_sphere
    description: 'Posterior superior temporal gyrus and sulcus, lateral and posterior
      to Heschl''s gyrus (primary auditory cortex), overlapping with the inferior
      portion of the planum temporale. MNI peak [-66, -32, 4] from Analysis 2 (the
      key analysis controlling for generic cognitive confounds). Analysis 1 peak (uncontrolled)
      was at [-66, -32, 6] with infinite Z-score. Analysis 3 (additionally controlling
      for spoken word and written sentence comprehension) peak: [-56, -26, 12].

      '
  imaging_details:
    field_strength: 1.5T (Siemens Sonata)
    modalities:
    - modality: T1
      sequence: 3D modified driven equilibrium Fourier transform (MDEFT)
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 12.24
      TE_ms: 3.56
    preprocessing_pipeline: 'SPM5; unified segmentation normalisation to MNI space
      (optimised for focal lesions; Seghier et al. 2008 automated lesion detection
      algorithm); smoothed 8 mm FWHM isotropic kernel; continuous grey matter probability
      images entered into multiple regression general linear model.

      '
    reference_space: MNI305
    atlases_used: []
    coordinates_reported:
    - region: Left posterior STG (Analysis 2 — auditory STM capacity controlling for
        confounds)
      mni:
      - -66
      - -32
      - 4
      note: Z = 5.26, FWE p < 0.05, extent ≥ 25 voxels
    - region: Left posterior STG (Analysis 1 — digit span alone)
      mni:
      - -66
      - -32
      - 6
      note: Z = Inf (first in table)
    - region: Left posterior STG (Analysis 3 — additionally controlling for comprehension)
      mni:
      - -56
      - -26
      - 12
      note: Z = 5.15, FWE p < 0.05
  replications:
  - '@Buchsbaum2001'
  - '@Becker1999'
  contradictions:
  - '@Warrington1969'
  - '@Shallice1977'
  author_limitations:
  - Continuous VBM method cannot detect damage in regions with only partial grey matter
    loss that still functions normally.
  - Patients with digit span 0–1 excluded — most severe output/memory deficits unrepresented.
  - Cross-sectional; cannot address recovery trajectory.
  - Right hemisphere patients included; left-hemisphere-specific effects assumed but
    not exclusively tested.
  - Hearing loss not formally controlled.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results (Analyses 1–2), Table 1, Figures 3–4; Discussion pp. 3407–3409
    confidence: high
    flags:
    - Scanner was 1.5T; reference space reported as MNI but method uses unified segmentation
      — likely MNI305 (SPM5 default).
    - Analysis 1 STG peak is listed as Z=Inf in Table 1, indicating saturation; actual
      Z not recoverable from paper.
    - All analyses used SPM5 VBM on continuous grey matter images, NOT binary lesion
      maps — methodology distinct from VLSM studies.
  source_passages:
  - section: Abstract
    page: 1
    supports: claim
    quote: structural integrity of a posterior region of the superior temporal gyrus
      and sulcus predicted auditory short-term memory capacity
  - section: Results
    page: 6
    supports: claim
    quote: identified a cortical region where grey matter density covaried with digit
      span despite the inclusion of these five extra control regressors
  - section: Discussion
    page: 8
    supports: region_definition
    quote: posterior superior temporal gyrus and sulcus lateral and posterior to Heschl's
      gyrus, overlapping with the most inferior portion of the planum temporale
  - section: Table 1
    page: 8
    supports: statistics
    quote: Superior temporal gyrus (posterior) -66 -32 4 5.26
  - section: Methods — Subjects
    page: 3
    supports: sample
    quote: Two hundred and ten patients were identified from a large, ongoing research
      database compiled for studying the structure-function relationships
- id: f4
  target: spoken_sentence_comprehension
  target_kind: impairment
  claim: 'Structural integrity of the left posterior superior temporal gyrus (same
    region supporting auditory STM capacity) also predicts spoken sentence comprehension
    ability, but NOT single spoken word comprehension or written sentence comprehension,
    consistent with a shared substrate for auditory STM and propositional speech comprehension.

    '
  direction: likely
  relationship: causal
  citation: '@Leff2009'
  method: VBCM
  design: cross-sectional
  imaging: T1-structural
  sample:
    n: 210
    population: chronic left- and right-hemisphere stroke patients
    time_post_onset: median 35 months (IQR 12–74 months)
    age_range: mean 59 years (SD 14)
    handedness: 89% right-handed
    language: English (first or dominant)
    recruitment: UCL Wellcome Trust Centre for Neuroimaging research database
    inclusion_criteria: same as f1
    exclusion_criteria: same as f1
  statistics:
    threshold: r(199) = 0.22, p = 0.002 (spoken sentence comprehension); non-significant
      for single words r = -0.03, p = 0.66; and written sentences r = 0.05, p = 0.45
    cluster_extent: not_reported
    effect_size: r = 0.22
    ci_95: not_reported
    p_value: '0.002'
  confounders_controlled:
  - same five regressors as Analysis 2 (repetition, fluency, naming, stroke volume)
  - age (linear and quadratic)
  - time since stroke
  confounders_not_controlled:
  - hearing loss
  - education / premorbid IQ
  - no active control modality task correction
  region_definition:
    kind: peak_coord_sphere
    description: 'Principal eigenvariate extracted from the Analysis 2 cluster (left
      posterior STG/sulcus, peak MNI [-66, -32, 4]) used as predictor for each comprehension
      measure in partial regression analyses.

      '
  imaging_details:
    field_strength: 1.5T (Siemens Sonata)
    modalities:
    - modality: T1
      sequence: 3D MDEFT
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 12.24
      TE_ms: 3.56
    preprocessing_pipeline: Same as f1; principal eigenvariate from Analysis 2 cluster
      used in partial regressions.
    reference_space: MNI305
    atlases_used: []
    coordinates_reported:
    - region: Left posterior STG (STM capacity cluster, used as predictor)
      mni:
      - -66
      - -32
      - 4
      note: Same cluster as f1 Analysis 2
  replications:
  - '@Crinion2003'
  - '@Spitsyna2006'
  contradictions:
  - '@Butterworth1986'
  author_limitations:
  - Correlation between STG integrity and spoken sentence comprehension (r=0.22) is
    modest, indicating other regions also contribute.
  - Cannot rule out that adjacency of structures (rather than functional sharing)
    explains co-occurrence of STM and comprehension deficits.
  - Single time-point; cannot address recovery.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results pp. 3406; Discussion pp. 3408–3409
    confidence: high
    flags:
    - Correlation r=0.22 is statistically significant but modest; effect size is smaller
      than the primary digit-span finding.
    - Dissociation from written sentence comprehension (r=0.05, ns) is a key theoretical
      claim — supports auditory-specific storage.
  source_passages:
  - section: Results
    page: 6
    supports: claim
    quote: significant correlation between the structural integrity of this region
      and spoken sentence comprehension score, r(199) = 0.22, P = 0.002
  - section: Results
    page: 6
    supports: claim
    quote: grey matter density in a region important for auditory short-term memory
      capacity correlated more strongly with comprehension of spoken sentences than
      with comprehension of either single words or written sentences
  - section: Conclusion
    page: 9
    supports: claim
    quote: identified the left posterior superior temporal gyrus and sulcus as the
      substrate mediating the capacity of auditory short-term memory
  - section: Discussion
    page: 8
    supports: region_definition
    quote: it is the posterior superior temporal gyrus and sulcus rather than the
      inferior parietal lobe that is necessary for intact auditory short-term memory
      capacity
source: draft
last_reviewed: '2026-05-07'
reviewer: claude-cowork
reviewed_on: '2026-05-06'
---
# Left Posterior Superior Temporal Gyrus and Sulcus (Leff et al. 2009)

## Anatomical context

The left posterior superior temporal gyrus (STG) and superior temporal sulcus (STS),
lateral and posterior to Heschl's gyrus, overlapping with the inferior planum temporale.
MNI peak [-66, -32, 4] in the key analysis (Analysis 2). This region is distinct from
primary auditory cortex (Heschl's gyrus) and lies at the inferolateral boundary of the
classical Wernicke's area zone.

## Key findings (Leff et al. 2009, n=210, UCL cohort)

**Finding f1**: VBM lesion analysis (Analysis 2) controlling for speech production,
perception, executive confounds and stroke volume identifies a single focal cluster in
the left posterior STG/STS as necessary for auditory STM capacity (digit span). Peak
MNI [-66, -32, 4], Z=5.26, FWE p<0.05.

**Finding f2**: The same region's structural integrity correlates with spoken sentence
comprehension (r=0.22, p=0.002) but not single word comprehension or written sentence
comprehension — supporting a shared substrate model for auditory STM and propositional
comprehension.

## Methodological note

This study uses continuous grey matter density (VBM) rather than binary lesion maps
(VLSM). The method treats partial grey matter loss as meaningful signal, potentially
detecting subtle structural changes invisible to binary VLSM. This makes it
methodologically distinct from the Mirman2015, Bonilha2014, and Fridriksson2018Anatomy
entries in this KB, all of which use binary VLSM/LSM approaches.

## Relation to other KB entries

Convergent with `left_superior_temporal_gyrus_wernickes` (Mirman2015) and
`left_posterior_stg` (Bonilha2014, Fridriksson2018Anatomy), but with a different
emphasis: Leff et al. specifically demonstrate that this STG subregion is the
**necessary** locus for auditory STM capacity, not the inferior parietal lobe
(which is activated in fMRI studies of auditory STM but is not necessary per lesion data).
