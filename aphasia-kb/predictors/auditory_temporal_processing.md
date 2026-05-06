---
schema_version: 2.3
id: auditory_temporal_processing
name: Rapid auditory temporal processing (40-Hz FM detection)
kind: predictor
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
predictor_type: behavioural
short_definition: Perceptual threshold for detecting 40-Hz frequency modulation (FM)
  in tonal stimuli, indexing rapid auditory temporal processing. Measured with an
  adaptive staircase paradigm; lower threshold = better performance.
assessment:
- 40-Hz FM detection (adaptive staircase, 3-interval 2AFC)
- 2-Hz FM detection (slow auditory temporal processing)
units: FM detection threshold (modulation index); lower values = better performance
  (inverse scale)
typical_range: 'not_reported (normative cutoff: ≤0.12 based on 15 neurotypical adults
  aged 50–82)'
direction_of_severity: higher_is_worse
findings:
- id: f1
  target: auditory_comprehension
  target_kind: impairment
  claim: Rapid auditory temporal processing ability (40-Hz FM detection threshold)
    at 2.5 months post-stroke predicts language comprehension outcome at 9 months
    post-stroke in Wernicke's aphasia, over and above initial comprehension severity.
  direction: likely
  relationship: correlational
  citation: '@Robson2019'
  method: behavioral_only
  design: longitudinal
  imaging: none
  sample:
    n: 12
    population: adults with Wernicke's aphasia, subacute phase (2.5 MPO), recruited
      from NHS in-patient services south of England
    time_post_onset: predictor measured at 2.5 MPO; outcome at 9 MPO
    age_range: 46–93 years
    handedness: right-handed (all except 1)
    language: monolingual English speakers
    recruitment: NHS referral; prospective longitudinal design.
    inclusion_criteria: WA diagnosis; monolingual English speaker.
    exclusion_criteria: Previous neurological disorder.
  statistics:
    threshold: p ≤ .001
    cluster_extent: null
    effect_size: r = −0.94, df = 6, P ≤ .001 (partial correlation controlling for
      comprehension at 2.5 MPO)
    ci_95: not_reported
    p_value: ≤ .001
  confounders_controlled:
  - comprehension score at 2.5 MPO (included as covariate in partial correlations)
  confounders_not_controlled:
  - lesion volume (not correlated with 9 MPO comprehension in this study)
  - age (not correlated with comprehension outcome)
  - hearing thresholds (not correlated with comprehension outcome)
  - therapy received
  region_definition:
    kind: not_reported
    description: Behavioral predictor finding — no specific brain region analyzed.
  replications: []
  contradictions: []
  author_limitations:
  - Sample size small (n=12); power calculation was based on chronic WA data and may
    not fully apply to the cross-lagged longitudinal design.
  - Some auditory assessment data missing (participants discontinued); df = 6 for
    this correlation indicates only ~8 usable data pairs.
  - Therapy involvement not controlled; however, amount of therapy was not correlated
    with comprehension outcome.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – Cross-Lagged Correlations; Discussion
    confidence: high
    flags:
    - df = 6 for the 2.5 MPO → 9 MPO rapid auditory processing correlation indicates
      approximately 8 participants contributed (some missing data); n is very small
      for this specific correlation.
    - Partial correlation controls for 2.5 MPO comprehension but df shrinks substantially;
      interpret r = −0.94 with caution.
  source_passages:
  - section: Results – Cross-Lagged Correlations
    page: 805
    supports: claim
    quote: 'Rapid auditory temporal processing (40 Hz FM detection: r = −0.94; df
      = 6; P ≤ .001) and phonological short-term memory (digit span: r = 0.64; df
      = 8; P = .046) at 2.5 MPO were significantly associated with comprehension at
      9 MPO.'
  - section: Methods – Neuropsychological Measures – Auditory Processing
    page: 803
    supports: method
    quote: Rapid and slow auditory temporal modulation processing was measured using
      40- and 2-Hz frequency modulation (FM) detection, respectively.
  - section: Results – Cross-Lagged Correlations
    page: 805
    supports: statistics
    quote: 'Rapid auditory temporal processing (40 Hz FM detection: r = −0.94; df
      = 6; P ≤ .001)'
  - section: Conclusions
    page: 810
    supports: claim
    quote: Rapid auditory temporal processing in the subacute phase was associated
      with comprehension outcome in the chronic phase, presenting a potential prognostic
      indicator for individuals with WA
  - section: Discussion – Limitations
    page: 810
    supports: limitation
    quote: The current study recruited 12 participants with WA. This sample size reflected
      an a priori power calculation; however, this calculation was conducted on chronic
      WA data, and the sample remains small.
- id: f2
  target: auditory_comprehension
  target_kind: impairment
  claim: Phonological processing (word phonological discrimination) at 5 months post-stroke
    predicts language comprehension outcome at 9 months in Wernicke's aphasia, over
    and above initial comprehension severity.
  direction: likely
  relationship: correlational
  citation: '@Robson2019'
  method: behavioral_only
  design: longitudinal
  imaging: none
  sample:
    n: 12
    population: adults with Wernicke's aphasia, south of England NHS services
    time_post_onset: predictor at 5 MPO; outcome at 9 MPO
    age_range: 46–93 years
    handedness: right-handed (all except 1)
    language: monolingual English speakers
    recruitment: NHS referral; prospective longitudinal design.
    inclusion_criteria: WA diagnosis.
    exclusion_criteria: Previous neurological disorder.
  statistics:
    threshold: p = .002
    cluster_extent: null
    effect_size: r = 0.84, df = 8, P = .002 (partial correlation controlling for comprehension
      at 2.5 MPO)
    ci_95: not_reported
    p_value: '.002'
  confounders_controlled:
  - comprehension score at 2.5 MPO
  confounders_not_controlled:
  - lesion volume
  - age
  - therapy received
  region_definition:
    kind: not_reported
    description: Behavioral predictor finding — no specific brain region analyzed.
  replications: []
  contradictions: []
  author_limitations:
  - Small sample; further associations may have been identified with a larger sample.
  - Phonological processing showed no significant improvement across time points —
    the predictive effect reflects residual capacity rather than improvement.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – Cross-Lagged Correlations
    confidence: high
    flags: []
  source_passages:
  - section: Results – Cross-Lagged Correlations
    page: 807
    supports: claim
    quote: Word phonological processing at 5 MPO was significantly associated with
      comprehension at 9 MPO (r = 0.84; df = 8; P = .002)
  - section: Discussion
    page: 810
    supports: claim
    quote: "temporal processing (40-Hz FM detection) at 2.5 \nMPO and word phonological\
      \ discrimination capacity at 5 \nMPO."
  - section: Discussion
    page: 809
    supports: limitation
    quote: these results indicate that individuals with significant impairments in
      auditory and phonological abilities at 2.5 to 5 MPO are at risk for poor language
      comprehension outcomes.
source: curated
last_reviewed: 2026-05-06
notes: "This predictor entry captures two cross-lagged behavioral predictors from\n\
  Robson 2019. Both are subacute-to-chronic predictors of language comprehension\n\
  outcome in Wernicke's aphasia.\n\nf1: 40-Hz FM detection (rapid auditory temporal\
  \ processing) at 2.5 MPO → \n    comprehension at 9 MPO (r=−0.94, very strong but\
  \ based on small df=6).\n    \nf2: Word phonological discrimination at 5 MPO → comprehension\
  \ at 9 MPO \n    (r=0.84, df=8).\n\nThe key interpretive insight: these abilities\
  \ do NOT consistently improve over\ntime, yet predict outcome. This suggests recovery\
  \ is driven by network\nreorganization exploiting residual auditory-phonological\
  \ capacity, not by\nimprovement in these underlying abilities per se.\n\nThe entry\
  \ id 'auditory_temporal_processing' is forward-looking. Promote.py\nwill create\
  \ the canonical entry on first use."
reviewer: claude-cowork
reviewed_on: '2026-05-06'
---
# Rapid auditory temporal processing (40-Hz FM detection)

## Robson 2019 — Subacute auditory and phonological processing predicting chronic comprehension in Wernicke's aphasia

This study provides the first longitudinal evidence that residual rapid auditory
temporal processing capacity in the subacute phase (2.5 MPO) is a strong predictor
of language comprehension outcome in the near-chronic phase (9 MPO) of Wernicke's
aphasia. Crucially, this capacity does not reliably improve over time — its predictive
value reflects baseline neural integrity rather than recovery of the auditory system.
