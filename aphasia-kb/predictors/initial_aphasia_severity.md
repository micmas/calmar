---
schema_version: 2.3
id: initial_aphasia_severity
name: Initial aphasia severity (acute WAB composite)
aliases:
- WABinitial
- baseline WAB
- acute aphasia severity
- admission aphasia severity
- initial severity
- WAB at admission
kind: predictor
predictor_type: behavioural
short_definition: Composite WAB score (comprehension + repetition + naming subtests,
  0–30) obtained within 24–72 hours of stroke onset; lower scores indicate more severe
  aphasia.
assessment:
- Western Aphasia Battery (WAB) — comprehension, repetition, and naming subtests
- WAB composite score (0–30)
units: score 0–30 (lower = more severe)
typical_range: 0–30; cut-off for aphasia ≤28; mild-to-moderate range 14–28 in this
  sample
direction_of_severity: lower_is_worse
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: 'Initial WAB composite score (WABinitial) accounts for 81% of variance in
    aphasia change score at 90 days (R²=0.81, p<0.001), and the recovery is proportional:
    patients recover 0.73 of their maximal potential recovery regardless of therapy
    status.'
  direction: likely
  relationship: correlational
  citation: '@Lazar2010'
  method: behavioral_only
  design: longitudinal
  imaging: none
  sample:
    n: 21
    population: acute left-hemisphere ischemic stroke patients with mild-to-moderate
      aphasia; subset of the PARIS (Performance and Recovery in Stroke) database
    time_post_onset: initial assessment 24–72 hours post-stroke (mean 2.1 days, SD
      1.3); follow-up at 90 days (mean 93.1 days, SD 18.8)
    age_range: mean 59.4 years (SD 14.9); range not reported
    handedness: right-handed
    language: not_reported
    recruitment: adult inpatient stroke service, Columbia University Medical Center,
      New York; screened May 2002 to August 2007
    inclusion_criteria: image-verified first-time ischemic stroke; clinical deficit
      in language at admission; sufficient comprehension to sign informed consent;
      WABinitial ≤28 (aphasia criterion)
    exclusion_criteria: severe comprehension deficits (unable to consent); non-first
      stroke; no image verification
  statistics:
    threshold: linear regression, two-tailed; p<0.001 criterion for significance
    cluster_extent: null
    effect_size: 'WABinitial alone: R²=0.81; full model (WABinitial + age + lesion
      volume): R²=0.83'
    ci_95: 'regression coefficient for WABinitial: B=−0.691, 95% CI [−0.873, −0.508]'
    p_value: <0.001 for WABinitial; age p=0.818; lesion volume p=0.236
  confounders_controlled:
  - age (included in regression model, not significant)
  - lesion volume (included in regression model, not significant)
  confounders_not_controlled:
  - type or intensity of speech-language therapy (9/21 received therapy, 8 did not,
    4 unknown)
  - specific lesion location (lobar/subcortical distribution tabulated but not entered
    as predictor)
  - aphasia subtype
  - dynamic changes in DWI lesion volume after 24–72 hour imaging
  - excluded severe aphasia due to consent restrictions — findings may not generalise
    to severe aphasia
  region_definition:
    kind: not_reported
    description: Behavioural-only finding; no lesion-symptom or imaging analysis performed.
      Lesion volumes estimated from DWI using perpendicular-diameter formula but not
      entered as primary predictor.
  imaging_details:
    reference_space: not_reported
    atlases_used: []
    modalities:
    - modality: DWI
  replications:
  - '@Pedersen2004'
  contradictions: []
  author_limitations:
  - Small sample (n=21); severe aphasia excluded due to consent restrictions.
  - No direct comparison between therapy and no-therapy conditions.
  - Lesion volume measured by perpendicular-diameter formula; small lesions may have
    larger measurement error.
  - DWI volume can change dynamically after 24–72 hours (reperfusion or penumbra progression).
  - Therapy type and intensity not recorded.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Abstract; Methods – Subjects and Methods; Results; Discussion
    confidence: high
    flags:
    - Sample restricted to mild-to-moderate aphasia (consent requirement); findings
      may not generalise to severe aphasia.
    - Proportionality constant 0.73 derived from mean potential vs achieved WAB across
      n=21; held for both therapy (R²=0.76) and no-therapy (R²=0.90) subgroups.
  source_passages:
  - section: Abstract
    page: 1
    supports: claim
    quote: WABinitial was highly correlated with WAB (R2=0.81, P<0.001)
  - section: Abstract
    page: 1
    supports: claim
    quote: patients recovered 0.73 of maximal potential recovery (WABmaximum−WABinitial)
  - section: Methods
    page: 1
    supports: sample
    quote: Twenty-one stroke patients had aphasia scores on the Western Aphasia Battery
      (WAB) obtained on stroke admission (WABinitial) and at 90 days (WAB3 mo)
  - section: Methods
    page: 1
    supports: method
    quote: Initial assessment occurred 24 to 72 hours after stroke onset (mean=2.1
      days; SD=1.3)
  - section: Results
    page: 2
    supports: statistics
    quote: WABinitial alone accounted for 81% of the variance
  - section: Results
    page: 2
    supports: statistics
    quote: regression coefficient was significant for WABinitial; the estimated regression
      coefficients of lesion volume and age, however, were not significant
  - section: Discussion
    page: 3
    supports: limitation
    quote: We were unable to address the question regarding recovery from severe aphasia
      because of consent restrictions imposed by local law
source: curated
last_reviewed: 2026-05-06
notes: 'Lazar et al. 2010 (Stroke) is a 4-page paper using n=21 mild-to-moderate aphasic

  stroke patients from the PARIS database. The key finding is that initial WAB composite

  score (WABinitial, 0–30) predicts 81% of variance in 90-day change score, and that

  recovery is proportional (0.73 of maximum potential recovery) regardless of whether

  patients received speech-language therapy. The proportionality is interpreted as
  evidence

  for a domain-general spontaneous biological recovery mechanism in the first 90 days

  post-stroke. Lesion volume and age are not significant predictors when WABinitial
  is

  in the model.


  Note: imaging used DWI for lesion volume estimation only; not a lesion-symptom mapping
  paper.

  Method coded as behavioral_only; imaging: none for this finding.'
reviewer: auto-reviewer
reviewed_on: '2026-05-06'
---
# Initial aphasia severity as predictor of 90-day recovery (Lazar 2010)

## Predictor definition

Initial WAB composite score measured at 24–72 hours post-stroke using three standardised
WAB subtests: comprehension (0–10), repetition (0–10), and naming (0–10), yielding a
composite score of 0–30 (WABmax). A score ≤28 was the operational definition of aphasia
in this study.

## Key finding

In a regression model with WABinitial, age, and lesion volume as predictors of
90-day WAB change:
- WABinitial alone R² = 0.81 (p<0.001)
- Full model R² = 0.83
- Age: not significant (p=0.818)
- Lesion volume: not significant (p=0.236)

The proportional recovery relation (achieved ΔWAB ≈ 0.73 × potential ΔWAB) was found
for both therapy-treated (R²=0.76) and untreated (R²=0.90) subgroups.

## Clinical implication

A new therapy within the first 90 days post-stroke should produce a WAB change score
*greater* than that predicted by the 0.73 proportionality model to be considered
more effective than current modalities.

## Scope limitation

Severe aphasia was excluded (consent restriction). The proportionality constant and
R² values apply only to mild-to-moderate aphasia. Whether the model holds for severe
aphasia remains untested.
