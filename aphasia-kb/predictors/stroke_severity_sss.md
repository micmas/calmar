---
schema_version: 2.3
id: stroke_severity_sss
name: Neurological stroke severity (Scandinavian Stroke Scale)
aliases:
- Scandinavian Stroke Scale
- SSS neurological severity
- general stroke severity
- modified SSS
- SSS excluding speech and orientation
kind: predictor
predictor_type: clinical
short_definition: Total score on the Scandinavian Stroke Scale (SSS, 0–58) assessing
  general neurological impairment after stroke; a modified version excluding speech
  and orientation items (0–42) was used to avoid confounding with aphasia.
assessment:
- Scandinavian Stroke Scale (SSS, 0–58)
- Modified SSS excluding speech and orientation items (0–42)
units: score 0–58 (SSS) or 0–42 (modified SSS); higher score = less severe impairment
typical_range: mean 23.4 (SD 9.3) for modified SSS in this aphasia sample (n=82)
direction_of_severity: lower_is_worse
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Initial aphasia severity (WAB-AQ) and neurological stroke severity (modified
    SSS) together predict 60% of variance in 1-year WAB-AQ; initial WAB-AQ and modified
    SSS were both retained in the final model, while age and sex were not.
  direction: likely
  relationship: correlational
  citation: '@Pedersen2004'
  method: behavioral_only
  design: longitudinal
  imaging: none
  sample:
    n: 203
    population: consecutive acute stroke patients with aphasia and first-ever stroke,
      prospectively included from three Copenhagen hospitals; n=84 reassessed at 1
      year (subset with available SSS in subgroup analyses, n=82 for SSS analyses)
    time_post_onset: initial assessment median 4 days after stroke onset (mean 7.3
      days, SD 11.2); 1-year follow-up median 385 days (mean 406.8 days, SD 76.1)
    age_range: mean 75.4 years (SD 11.0) for first-ever stroke patients
    handedness: not_reported
    language: Danish as first language
    recruitment: prospective consecutive inclusion from Bispebjerg, Hvidovre, and
      Frederiksberg Hospitals, Copenhagen, December 1996 – May 1999
    inclusion_criteria: suspected aphasia; Danish as first language; no previous dementia;
      stroke diagnosis confirmed
    exclusion_criteria: impaired consciousness; pure dysarthria; unable to cooperate;
      severe somatic condition; refused participation
  statistics:
    threshold: multiple linear regression, backward elimination of non-significant
      variables; significance level p<0.05
    cluster_extent: null
    effect_size: R²=0.60 for 1-year AQ model (initial AQ + modified SSS); R²=0.47
      for simple regression of initial AQ on 1-year AQ
    ci_95: not_reported
    p_value: p<0.001 for initial AQ (correlation with 1-year AQ); p<0.001 for SSS–AQ
      correlation (r=0.53)
  confounders_controlled:
  - initial aphasia severity (WAB-AQ) — included in same regression model
  - age (not significant, removed from final model)
  - sex (not significant, removed from final model)
  confounders_not_controlled:
  - lesion location and volume (CT data available for 228/270 but not entered as predictors)
  - speech-language therapy amount and type
  - SSS available in only 84 of 270 patients — subsample may not be representative
  - 73 patients died within first year — survival bias
  - 42 refused follow-up participation
  region_definition:
    kind: not_reported
    description: Behavioural-only / clinical finding; no lesion-symptom mapping performed.
      CT-verified diagnosis available for 228/270 patients but imaging not used as
      predictor.
  imaging_details:
    reference_space: not_reported
    atlases_used: []
    modalities:
    - modality: not_reported
  replications:
  - '@Lazar2010'
  contradictions: []
  author_limitations:
  - SSS available for only a subset of patients (82–84 of 203 first-ever stroke cases).
  - 'Significant attrition at 1 year: 73 died, 42 refused, 13 had new stroke.'
  - WAB aphasia classification does not allow for unclassified or mixed aphasia.
  - All patients were Danish-speaking; generalisability to other languages uncertain.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Abstract; Methods; Results – Aphasia 1 Year after Stroke; Discussion
      – Determinants of Recovery
    confidence: high
    flags:
    - 'Two predictors retained: initial WAB-AQ and modified SSS. Type of aphasia,
      age, and sex not significant.'
    - SSS subsample (n=82–84) smaller than total cohort (n=203); subsample representativeness
      uncertain.
    - Figure 1 (scattergram of AQ admission vs 1-year AQ) shows R²=0.47 for simple
      regression; full model R²=0.60.
  source_passages:
  - section: Abstract
    page: 1
    supports: claim
    quote: The outcome for language function was predicted by initial severity of
      the aphasia and by the initial stroke severity (assessed by the Scandinavian
      Stroke Scale), but not by age, sex or type of aphasia
  - section: Results – Aphasia 1 Year after Stroke
    page: 4
    supports: statistics
    quote: The resulting model explained 60% (R2) of the variation in the 1-year AQ
      and included initial AQ and neurological stroke severity, but neither sex nor
      age
  - section: Results – Aphasia on Admission
    page: 3
    supports: statistics
    quote: There was a significant association between neurological severity and AQ
      (r = 0.53, p < 0.001)
  - section: Methods – Patients
    page: 2
    supports: sample
    quote: All stroke patients with suspected aphasia, Danish as their first language,
      and without a previous dementia were included from three Copenhagen hospitals
  - section: Methods – Assessments
    page: 2
    supports: method
    quote: The initial assessment was carried out on the ward as soon as possible
      after admission, in most cases within the first week after stroke onset (median
      4 days, mean 7.3 days, SD 11.2)
  - section: Methods – Assessments
    page: 2
    supports: method
    quote: we made a modified total score for the SSS excluding the speech and orientation
      items (ranging from 0 to 42 points)
  - section: Results – Aphasia 1 Year after Stroke
    page: 4
    supports: limitation
    quote: 73 died within the first year, 13 had a new stroke, 11 moved away from
      the Copenhagen area and 42 refused to participate
  - section: Discussion – Determinants of Recovery
    page: 8
    supports: claim
    quote: the inclusion of neurological stroke severity on admission improved the
      accuracy of the prognosis of aphasia
- id: f2
  target: initial_aphasia_severity
  target_kind: predictor
  claim: Initial WAB-AQ alone accounts for 47% of variance in 1-year WAB-AQ (R²=0.47).
    When combined with modified SSS this rises to 60%. Type of aphasia on admission
    does not independently predict degree of recovery beyond its correlation with
    initial severity.
  direction: likely
  relationship: correlational
  citation: '@Pedersen2004'
  method: behavioral_only
  design: longitudinal
  imaging: none
  sample:
    n: 84
    population: first-ever stroke patients with aphasia reassessed at 1 year; subset
      of the 203 first-ever stroke cases with aphasia on admission
    time_post_onset: initial assessment median 4 days; 1-year follow-up median 385
      days
    age_range: mean 75.4 years (SD 11.0)
    handedness: not_reported
    language: Danish as first language
    recruitment: prospective consecutive inclusion from three Copenhagen hospitals
    inclusion_criteria: first-ever stroke; aphasia confirmed on WAB; alive and in
      Copenhagen area at 1 year
    exclusion_criteria: died within 1 year; new stroke; moved away; refused; unable
      to cooperate
  statistics:
    threshold: Pearson r (simple regression); multiple linear regression with backward
      elimination; p<0.05
    cluster_extent: null
    effect_size: 'R²=0.47 (initial AQ vs 1-year AQ simple regression); regression
      formula: initial AQ = 45.3 + 0.65 × AQ at 1 year'
    ci_95: not_reported
    p_value: not_reported for R²=0.47; p<0.001 for SSS–AQ correlation
  confounders_controlled:
  - neurological stroke severity (modified SSS) in full model
  - age (not retained in final model)
  - sex (not retained in final model)
  confounders_not_controlled:
  - lesion volume and location
  - speech-language therapy amount
  - survival bias (73/203 died before reassessment)
  region_definition:
    kind: not_reported
    description: Behavioural-only finding; no imaging analysis of lesion-outcome relationships.
  imaging_details:
    reference_space: not_reported
    atlases_used: []
    modalities:
    - modality: not_reported
  replications:
  - '@Lazar2010'
  contradictions: []
  author_limitations:
  - Significant attrition at 1 year limits generalisability.
  - Wide scatter in outcomes for patients with low initial AQ (some fully recover,
    others do not) — individual prognosis unreliable until 2nd–4th week.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – Aphasia 1 Year after Stroke; Figure 1; Discussion
    confidence: high
    flags:
    - 'R²=0.47 for simple regression initial AQ → 1-year AQ; formula: initial AQ =
      45.3 + 0.65 × (1-year AQ) — note this is AQ-at-admission as dependent variable
      in the printed formula; interpret carefully.'
    - Type of aphasia not an independent predictor after controlling for initial AQ.
  source_passages:
  - section: Results – Aphasia 1 Year after Stroke
    page: 4
    supports: statistics
    quote: R2 for the regression line is 0.47
  - section: Discussion – Determinants of Recovery – Initial Severity
    page: 8
    supports: claim
    quote: Numerous studies have shown initial severity of aphasia to be far more
      important for the final outcome of aphasia than any other factor
  - section: Discussion – Determinants of Recovery – Type of Aphasia
    page: 8
    supports: claim
    quote: We did two types of analyses to compensate for this and found no effect
      of type of aphasia on improvement in AQ in either case
  - section: Conclusion
    page: 9
    supports: claim
    quote: the initial type of aphasia does not predict the degree of recovery beyond
      its association with aphasia severity
- id: f3
  target: prognosis
  target_kind: prognosis
  claim: Initial aphasia severity (WAB-AQ) and neurological stroke severity (modified
    SSS) together predict 60% of variance in 1-year WAB-AQ; initial WAB-AQ and modified
    SSS were both retained in the final model, while age and sex were not.
  direction: likely
  relationship: correlational
  citation: '@Pedersen2004'
  method: behavioral_only
  design: longitudinal
  imaging: none
  sample:
    n: 203
    population: consecutive acute stroke patients with aphasia and first-ever stroke,
      prospectively included from three Copenhagen hospitals; n=84 reassessed at 1
      year (subset with available SSS in subgroup analyses, n=82 for SSS analyses)
    time_post_onset: initial assessment median 4 days after stroke onset (mean 7.3
      days, SD 11.2); 1-year follow-up median 385 days (mean 406.8 days, SD 76.1)
    age_range: mean 75.4 years (SD 11.0) for first-ever stroke patients
    handedness: not_reported
    language: Danish as first language
    recruitment: prospective consecutive inclusion from Bispebjerg, Hvidovre, and
      Frederiksberg Hospitals, Copenhagen, December 1996 – May 1999
    inclusion_criteria: suspected aphasia; Danish as first language; no previous dementia;
      stroke diagnosis confirmed
    exclusion_criteria: impaired consciousness; pure dysarthria; unable to cooperate;
      severe somatic condition; refused participation
  statistics:
    threshold: multiple linear regression, backward elimination of non-significant
      variables; significance level p<0.05
    cluster_extent: null
    effect_size: R²=0.60 for 1-year AQ model (initial AQ + modified SSS); R²=0.47
      for simple regression of initial AQ on 1-year AQ
    ci_95: not_reported
    p_value: p<0.001 for initial AQ (correlation with 1-year AQ); p<0.001 for SSS–AQ
      correlation (r=0.53)
  confounders_controlled:
  - initial aphasia severity (WAB-AQ) — included in same regression model
  - age (not significant, removed from final model)
  - sex (not significant, removed from final model)
  confounders_not_controlled:
  - lesion location and volume (CT data available for 228/270 but not entered as predictors)
  - speech-language therapy amount and type
  - SSS available in only 84 of 270 patients — subsample may not be representative
  - 73 patients died within first year — survival bias
  - 42 refused follow-up participation
  region_definition:
    kind: not_reported
    description: Behavioural-only / clinical finding; no lesion-symptom mapping performed.
      CT-verified diagnosis available for 228/270 patients but imaging not used as
      predictor.
  imaging_details:
    reference_space: not_reported
    atlases_used: []
    modalities:
    - modality: not_reported
  replications:
  - '@Lazar2010'
  contradictions: []
  author_limitations:
  - SSS available for only a subset of patients (82–84 of 203 first-ever stroke cases).
  - 'Significant attrition at 1 year: 73 died, 42 refused, 13 had new stroke.'
  - WAB aphasia classification does not allow for unclassified or mixed aphasia.
  - All patients were Danish-speaking; generalisability to other languages uncertain.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Abstract; Methods; Results – Aphasia 1 Year after Stroke; Discussion
      – Determinants of Recovery
    confidence: high
    flags:
    - 'Two predictors retained: initial WAB-AQ and modified SSS. Type of aphasia,
      age, and sex not significant.'
    - SSS subsample (n=82–84) smaller than total cohort (n=203); subsample representativeness
      uncertain.
    - Figure 1 (scattergram of AQ admission vs 1-year AQ) shows R²=0.47 for simple
      regression; full model R²=0.60.
  source_passages:
  - section: Abstract
    page: 1
    supports: claim
    quote: The outcome for language function was predicted by initial severity of
      the aphasia and by the initial stroke severity (assessed by the Scandinavian
      Stroke Scale), but not by age, sex or type of aphasia
  - section: Results – Aphasia 1 Year after Stroke
    page: 4
    supports: statistics
    quote: The resulting model explained 60% (R2) of the variation in the 1-year AQ
      and included initial AQ and neurological stroke severity, but neither sex nor
      age
  - section: Results – Aphasia on Admission
    page: 3
    supports: statistics
    quote: There was a significant association between neurological severity and AQ
      (r = 0.53, p < 0.001)
  - section: Methods – Patients
    page: 2
    supports: sample
    quote: All stroke patients with suspected aphasia, Danish as their first language,
      and without a previous dementia were included from three Copenhagen hospitals
  - section: Methods – Assessments
    page: 2
    supports: method
    quote: The initial assessment was carried out on the ward as soon as possible
      after admission, in most cases within the first week after stroke onset (median
      4 days, mean 7.3 days, SD 11.2)
  - section: Methods – Assessments
    page: 2
    supports: method
    quote: we made a modified total score for the SSS excluding the speech and orientation
      items (ranging from 0 to 42 points)
  - section: Results – Aphasia 1 Year after Stroke
    page: 4
    supports: limitation
    quote: 73 died within the first year, 13 had a new stroke, 11 moved away from
      the Copenhagen area and 42 refused to participate
  - section: Discussion – Determinants of Recovery
    page: 8
    supports: claim
    quote: the inclusion of neurological stroke severity on admission improved the
      accuracy of the prognosis of aphasia
- id: f4
  target: initial_aphasia_severity
  target_kind: predictor
  claim: Initial WAB-AQ alone accounts for 47% of variance in 1-year WAB-AQ (R²=0.47).
    When combined with modified SSS this rises to 60%. Type of aphasia on admission
    does not independently predict degree of recovery beyond its correlation with
    initial severity.
  direction: likely
  relationship: correlational
  citation: '@Pedersen2004'
  method: behavioral_only
  design: longitudinal
  imaging: none
  sample:
    n: 84
    population: first-ever stroke patients with aphasia reassessed at 1 year; subset
      of the 203 first-ever stroke cases with aphasia on admission
    time_post_onset: initial assessment median 4 days; 1-year follow-up median 385
      days
    age_range: mean 75.4 years (SD 11.0)
    handedness: not_reported
    language: Danish as first language
    recruitment: prospective consecutive inclusion from three Copenhagen hospitals
    inclusion_criteria: first-ever stroke; aphasia confirmed on WAB; alive and in
      Copenhagen area at 1 year
    exclusion_criteria: died within 1 year; new stroke; moved away; refused; unable
      to cooperate
  statistics:
    threshold: Pearson r (simple regression); multiple linear regression with backward
      elimination; p<0.05
    cluster_extent: null
    effect_size: 'R²=0.47 (initial AQ vs 1-year AQ simple regression); regression
      formula: initial AQ = 45.3 + 0.65 × AQ at 1 year'
    ci_95: not_reported
    p_value: not_reported for R²=0.47; p<0.001 for SSS–AQ correlation
  confounders_controlled:
  - neurological stroke severity (modified SSS) in full model
  - age (not retained in final model)
  - sex (not retained in final model)
  confounders_not_controlled:
  - lesion volume and location
  - speech-language therapy amount
  - survival bias (73/203 died before reassessment)
  region_definition:
    kind: not_reported
    description: Behavioural-only finding; no imaging analysis of lesion-outcome relationships.
  imaging_details:
    reference_space: not_reported
    atlases_used: []
    modalities:
    - modality: not_reported
  replications:
  - '@Lazar2010'
  contradictions: []
  author_limitations:
  - Significant attrition at 1 year limits generalisability.
  - Wide scatter in outcomes for patients with low initial AQ (some fully recover,
    others do not) — individual prognosis unreliable until 2nd–4th week.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – Aphasia 1 Year after Stroke; Figure 1; Discussion
    confidence: high
    flags:
    - 'R²=0.47 for simple regression initial AQ → 1-year AQ; formula: initial AQ =
      45.3 + 0.65 × (1-year AQ) — note this is AQ-at-admission as dependent variable
      in the printed formula; interpret carefully.'
    - Type of aphasia not an independent predictor after controlling for initial AQ.
  source_passages:
  - section: Results – Aphasia 1 Year after Stroke
    page: 4
    supports: statistics
    quote: R2 for the regression line is 0.47
  - section: Discussion – Determinants of Recovery – Initial Severity
    page: 8
    supports: claim
    quote: Numerous studies have shown initial severity of aphasia to be far more
      important for the final outcome of aphasia than any other factor
  - section: Discussion – Determinants of Recovery – Type of Aphasia
    page: 8
    supports: claim
    quote: We did two types of analyses to compensate for this and found no effect
      of type of aphasia on improvement in AQ in either case
  - section: Conclusion
    page: 9
    supports: claim
    quote: the initial type of aphasia does not predict the degree of recovery beyond
      its association with aphasia severity
source: curated
last_reviewed: '2026-05-07'
notes: "Pedersen et al. 2004 (Cerebrovasc Dis) is the Copenhagen Aphasia Study, a\
  \ 9-page\nprospective longitudinal study of 270 acute stroke patients with aphasia\
  \ (203 first-ever\nstrokes) from three Copenhagen hospitals (1996–1999), assessed\
  \ with the Danish WAB.\n\nTwo main predictor findings:\n1. Initial WAB-AQ + modified\
  \ SSS together predict R²=0.60 of 1-year WAB-AQ.\n2. Initial WAB-AQ alone predicts\
  \ R²=0.47 of 1-year WAB-AQ.\n\nNon-significant predictors: age, sex, aphasia type.\n\
  \nAdditional descriptive findings (not encoded as KB findings):\n- Acute aphasia\
  \ types: global 32%, anomic 25%, Wernicke's 16%, Broca's 12%, transcortical\n  sensory\
  \ 7%, conduction 5%, transcortical motor 2%, isolation 2%.\n- 61% still aphasic\
  \ at 1 year (in milder form).\n- Aphasia type always changed to a less severe form;\
  \ nonfluent → fluent evolution possible,\n  but fluent → nonfluent never observed.\n\
  - No imaging (lesion-symptom) analyses performed; study is purely clinical/behavioural."
reviewer: claude-cowork
reviewed_on: '2026-05-06'
---
# Stroke severity (SSS) as predictor of aphasia prognosis (Pedersen 2004)

## Study overview

The Copenhagen Aphasia Study prospectively enrolled 270 consecutive acute stroke patients
with aphasia (203 first-ever strokes) from three Copenhagen hospitals, assessed with the
Danish WAB at admission (median 4 days post-onset) and again at 1 year.

## Main predictor findings

**Finding f1** — Two-variable prediction model:
- Predictors retained: initial WAB-AQ and neurological stroke severity (modified SSS, 0–42)
- Predictors dropped: age, sex, aphasia type
- R² = 0.60 for 1-year WAB-AQ

**Finding f2** — Single-variable prediction:
- Initial WAB-AQ alone R² = 0.47 for 1-year WAB-AQ
- Regression formula (printed in paper): initial AQ = 45.3 + 0.65 × AQ at 1 year

## Aphasia type evolution

Type of aphasia always changed to a less severe classification over the year.
Non-fluent aphasia (e.g. global) could evolve to fluent (e.g. anomic),
but fluent types never became non-fluent. Initial aphasia type does not predict
degree of recovery beyond its correlation with severity.

## Clinical takeaway

Adding a brief neurological severity rating (Scandinavian Stroke Scale) at admission
improves aphasia outcome prediction beyond initial WAB-AQ alone (R² 0.47 → 0.60).
Age and sex do not improve prediction.
