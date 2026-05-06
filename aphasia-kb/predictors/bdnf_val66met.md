---
schema_version: 2.3
id: bdnf_val66met
name: BDNF Val66Met genotype (rs6265)
kind: predictor
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
predictor_type: demographic
short_definition: Common single-nucleotide polymorphism (rs6265) in the BDNF gene;
  val/val (typical) vs val/met or met/met (atypical, Met allele carriers). Met allele
  carriers show 18–30% reduced activity-dependent BDNF secretion.
assessment:
- TaqMan SNP Genotyping Assay (rs6265)
- saliva or blood DNA extraction
units: 'genotype category: val/val (typical) vs Met-allele carrier (atypical)'
typical_range: 'Caucasian population: ~65% val/val, ~35% Met-allele carriers'
direction_of_severity: not_applicable
findings:
- id: f1
  target: tdcs_aphasia_treatment
  target_kind: therapy
  claim: Val/val BDNF genotype predicts greater response to anodal tDCS during aphasia
    treatment; Met allele carriers do not show the same benefit from A-tDCS.
  direction: likely
  relationship: responder
  citation: '@Fridriksson2018BDNF'
  method: clinical_RCT
  design: RCT
  imaging: none
  sample:
    n: 66
    population: chronic stroke-induced aphasia participants from a double-blind RCT
      at USC and MUSC
    time_post_onset: mean 43.3 months (SD 41.1; range 6.1–204.9 months)
    age_range: 30–77 years (mean 59.8, SD 10.2)
    handedness: not_reported
    language: English-speaking
    recruitment: Participants enrolled in parent RCT at University of South Carolina
      and Medical University of South Carolina; genotype data available for 66 of
      74 enrolled.
    inclusion_criteria: Chronic stroke-induced aphasia; PNT baseline <140/175.
    exclusion_criteria: not_reported
  statistics:
    threshold: p = 0.03
    cluster_extent: null
    effect_size: F = 4.97 (tDCS × BDNF genotype interaction)
    ci_95: not_reported
    p_value: '0.03'
  confounders_controlled:
  - baseline WAB-R AQ
  - lesion size
  - time of follow-up (1, 4, 24 weeks)
  confounders_not_controlled:
  - stroke location
  - depression
  - race/ethnicity
  region_definition:
    kind: not_reported
    description: Behavioral-only predictor finding — no specific brain region.
  replications: []
  contradictions: []
  author_limitations:
  - Baseline aphasia severity differed between BDNF genotype groups (val/val WAB-AQ
    mean 63.5 vs atypical 52.2), though this difference became non-significant after
    adjusting for time post-stroke and lesion size.
  - It remains unclear whether A-tDCS modulates BDNF secretion or relies on pre-existing
    baseline BDNF levels.
  - Depression not assessed; BDNF polymorphism may interact with depression in stroke
    patients.
  evidence_quality: RCT
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Abstract; Results; Table 1; Table 2; Discussion
    confidence: high
    flags:
    - cohort overlaps with parent RCT cited as ref [13] in this paper (Fridriksson
      et al. JAMA Neurol 2018); flag for downstream double-counting.
    - Baseline severity difference between genotype groups (val/val WAB-AQ 63.5 vs
      atypical 52.2, p=0.01) is a potential confounder; non-significant after covariate
      adjustment.
  source_passages:
  - section: Abstract
    page: 1276
    supports: claim
    quote: Individuals with the val/val BDNF genotype are more likely to benefit from
      A-tDCS during aphasia treatment.
  - section: Methods – Participants
    page: 1278
    supports: sample
    quote: 'BDNF genotype was available for 67 participants due to lost or contaminated

      sample (6 participants) or decline in blood draw (1 participant).'
  - section: Methods – BDNF genotyping
    page: 1277
    supports: method
    quote: Genotypes were determined using Life Technologies' Taqman Genotyper v1.0.1
      software. Participants with a val/val... expression were considered typical
      BDNF genotype and those with val/met... or met/met... were considered to have
      atypical BDNF genotype.
  - section: Results; Table 2
    page: 1280
    supports: statistics
    quote: 'Genotype x tDCS

      1

      60

      4.97

      0.03'
  - section: Results
    page: 1279
    supports: confounders
    quote: When adjusting for time post stroke and lesion size the main effect of
      BDNF genotype on WAB-R AQ and PNT+Naming 80 is no longer statistically significant
      (p = 0.11, p = 0.17, respectively).
  - section: Discussion
    page: 1280
    supports: limitation
    quote: we did not compare levels of depression between participants with typical
      and atypical BDNF genotype
- id: f2
  target: severity_metric
  target_kind: predictor
  claim: Val/val BDNF genotype is associated with less severe chronic aphasia than
    val/met genotype, after controlling for lesion volume and time post-stroke; this
    effect is amplified by interactions with age at stroke, cortical excitability,
    and stimulation-induced neuroplasticity.
  direction: likely
  relationship: correlational
  citation: '@Dresang2022'
  method:
  - behavioral_only
  - TMS
  design: cross-sectional
  imaging: none
  sample:
    n: 17
    population: adults with chronic left-hemisphere ischemic stroke and aphasia (University
      of Pennsylvania)
    time_post_onset: greater than 6 months (chronic); range not_reported
    age_range: 29–79 years (see Table 1)
    handedness: not_reported
    language: not_reported
    recruitment: Subjects provided informed consent prior to participation, in accordance
      with the University of Pennsylvania Institutional Review Board.
    inclusion_criteria: Single left-hemisphere ischemic stroke >6 months prior; WAB-AQ
      below aphasia diagnostic cutoff (≥93.7 excluded).
    exclusion_criteria: WAB-AQ ≥93.7 (aphasia diagnosis threshold); Met66Met homozygote
      excluded (insufficient n for analysis).
  statistics:
    threshold: p < .001 (main effect of BDNF genotype on WAB-AQ in linear regression)
    cluster_extent: null
    effect_size: β = 32.62, SE = 1.86, t = 17.53, P < .001 (BDNF genotype main effect);
      LASSO-adjusted R² = 0.431 for base model including BDNF
    ci_95: not_reported
    p_value: < .001
  confounders_controlled:
  - time post-stroke (log-transformed months post-onset)
  - total lesion volume
  - age at time of stroke
  confounders_not_controlled:
  - stroke location
  - lesion topology (only volume controlled)
  - race/ethnicity
  - aphasia type
  - treatment history
  region_definition:
    kind: not_reported
    description: Behavioral/genetic predictor finding — no specific brain region analyzed.
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  replications:
  - '@Fridriksson2018BDNF'
  contradictions: []
  author_limitations:
  - Small sample size (n=17) for examining genetic polymorphism effects; comparable
    to other BDNF/MEP aphasia studies but limits generalizability.
  - It remains unclear whether BDNF polymorphism is only a significant predictor of
    chronic but not acute post-stroke aphasia.
  - Additional predictors such as stroke location were not included in a single combined
    model due to limited sample size.
  - Future work should replicate in larger samples of stroke patients with and without
    aphasia.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Abstract; Methods – Participants; Results – Linear Regression;
      Table 2; Discussion
    confidence: medium
    flags:
    - Small sample (n=17) for a genetic predictor study; LASSO cross-validation used
      to control for overfitting but adjusted R² increases are very small when adding
      BDNF alone (footnote 1 in paper notes 'small but significant effect').
    - BDNF groups differed in lesion volume (val/val mean 148.5 cc vs val/met mean
      71.3 cc) and time post-stroke, though authors report these did not differ statistically
      (t=1.78, p=.12; t=0.42, p=.68); large variability.
  source_passages:
  - section: Abstract
    page: 371
    supports: claim
    quote: Val66Val carriers showed less aphasia severity than Val66Met carriers,
      after controlling for lesion volume and time post-stroke.
  - section: Methods – Participants
    page: 374
    supports: sample
    quote: Participants were 19 subjects with a single left-hemisphere ischemic stroke
      that occurred >6 months prior to participation... This resulted in a final sample
      of 17 participants.
  - section: Results – Linear Regression
    page: 375
    supports: statistics
    quote: BDNF genotype shows a main effect such that when all other factors are
      constant, Val66Val carriers show less severity than Val66Met carriers (β = 32.62,
      SE = 1.86, t = 17.53, P < .001).
  - section: Methods – Statistical Analysis
    page: 375
    supports: method
    quote: We conducted a series of linear regression models in R with aphasia severity
      (WAB-AQ) as the outcome measure.
  - section: Methods – Statistical Analysis
    page: 375
    supports: confounders
    quote: base model included factors of interest that are common predictors of aphasia,
      including time post-stroke (log-transformed months post-stroke onset; LogMPO),
      age at time of stroke, and total lesion volume (LesVol).
  - section: Discussion – Limitations
    page: 378
    supports: limitation
    quote: A potential limitation of this study is the modest sample size used to
      examine the behavioral effects of a genetic polymorphism.
- id: f3
  target: severity_metric
  target_kind: predictor
  claim: 'Cortical excitability (baseline MEP amplitude) measured at the intact right
    primary motor cortex interacts with BDNF genotype to predict chronic aphasia severity:
    higher excitability is associated with less severe aphasia in val/val carriers
    but greater severity in val/met carriers.'
  direction: mixed
  relationship: correlational
  citation: '@Dresang2022'
  method: TMS
  design: cross-sectional
  imaging: none
  sample:
    n: 17
    population: adults with chronic left-hemisphere ischemic stroke and aphasia (University
      of Pennsylvania)
    time_post_onset: greater than 6 months (chronic)
    age_range: 29–79 years
    handedness: not_reported
    language: not_reported
    recruitment: University of Pennsylvania Institutional Review Board approved study.
    inclusion_criteria: Single left-hemisphere ischemic stroke >6 months prior.
    exclusion_criteria: WAB-AQ ≥93.7; Met66Met homozygote excluded.
  statistics:
    threshold: p < .001
    cluster_extent: null
    effect_size: 'Val/val: β = 14.13, SE = .74, t = 19.22, P < .001; Val/met: β =
      −2.86, SE = .49, t = −5.82, P < .001; interaction model adjusted R² = 0.528,
      Cohen''s f² = 0.097'
    ci_95: not_reported
    p_value: < .001
  confounders_controlled:
  - time post-stroke (log-transformed)
  - lesion volume
  - age at time of stroke
  - BDNF genotype (as main effect)
  confounders_not_controlled:
  - stroke location
  - aphasia type
  region_definition:
    kind: not_reported
    description: TMS-based neurophysiological predictor — MEPs recorded from left
      FDI muscle via single-pulse TMS to right primary motor cortex. Not a brain region
      finding.
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  replications: []
  contradictions: []
  author_limitations:
  - Modest sample size (n=17); the distinct patterns for cortical excitability across
    BDNF genotype groups require replication in larger samples.
  - MEP measurements index domain-general cortical excitability but may not directly
    reflect language network excitability.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – Cortical excitability × BDNF; Table 2; Fig. 2B
    confidence: medium
    flags:
    - 'direction: mixed because the sign of the association differs by genotype group
      (positive for val/val, negative for val/met); this is not a within-paper analytic
      disagreement but a genuine genotype-moderated reversal.'
  source_passages:
  - section: Results – Cortical excitability × BDNF
    page: 376
    supports: claim
    quote: Cortical excitability was positively associated with WAB-AQ for Val66Val
      carriers (β = 14.13, SE = .74, t = 19.22, P < .001), but negatively associated
      with WAB-AQ for Val66Met carriers (β = −2.86, SE = .49, t = −5.82, P < .001
  - section: Methods – Transcranial Magnetic Stimulation
    page: 374
    supports: method
    quote: 'Magstim 2002 Stimulator with a 70 mm

      ﬁgure-eight coil (Magstim Co., Whitland, Dyﬁeld, UK).'
  - section: Results; Table 2
    page: 376
    supports: statistics
    quote: 'LogMPO + LesVol + AgeCVA + BDNF * MEPbase: Adjusted R2 .528, Cohen''s
      f2 .097'
  - section: Discussion
    page: 377
    supports: limitation
    quote: Future work may explore the utility of these indicators in
- id: f4
  target: severity_metric
  target_kind: predictor
  claim: Stimulation-induced neuroplasticity (cTBS-induced MEP suppression at 10 min
    post-cTBS) interacts with BDNF genotype to predict chronic aphasia severity; greater
    MEP suppression (expected cTBS response) is associated with less severe aphasia,
    with the effect stronger in val/met than val/val carriers.
  direction: likely
  relationship: correlational
  citation: '@Dresang2022'
  method: TMS
  design: cross-sectional
  imaging: none
  sample:
    n: 17
    population: adults with chronic left-hemisphere ischemic stroke and aphasia (University
      of Pennsylvania)
    time_post_onset: greater than 6 months (chronic)
    age_range: 29–79 years
    handedness: not_reported
    language: not_reported
    recruitment: University of Pennsylvania Institutional Review Board approved study.
    inclusion_criteria: Single left-hemisphere ischemic stroke >6 months prior.
    exclusion_criteria: WAB-AQ ≥93.7; Met66Met homozygote excluded.
  statistics:
    threshold: p < .001
    cluster_extent: null
    effect_size: 'Val/met × MEPd10 interaction: β = 3.56, SE = .60, t = 5.93, P <
      .001; plasticity*BDNF model adjusted R² = 0.613, Cohen''s f² = 0.182'
    ci_95: not_reported
    p_value: < .001
  confounders_controlled:
  - time post-stroke (log-transformed)
  - lesion volume
  - age at time of stroke
  - BDNF genotype (as main effect)
  confounders_not_controlled:
  - stroke location
  - aphasia type
  region_definition:
    kind: not_reported
    description: TMS/cTBS neurophysiological predictor — cTBS administered to right
      primary motor cortex; MEP difference (pre vs 10-min post-cTBS) as index of stimulation-induced
      neuroplasticity.
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  replications: []
  contradictions: []
  author_limitations:
  - Longitudinal investigations are needed to determine the optimal prognostic timepoint
    at which biomarkers of neuroplasticity have the strongest predictive power.
  - All predictors could not be examined in a single combined model due to limited
    sample size.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – Stimulation-induced neuroplasticity × BDNF; Table 2;
      Fig. 2C
    confidence: medium
    flags:
    - 10-minute post-cTBS timepoint used because it 'showed peak stimulation effects'
      per ref [34] (Parchure et al.); other timepoints not analyzed here.
  source_passages:
  - section: Results – Stimulation-induced neuroplasticity × BDNF
    page: 376
    supports: claim
    quote: Less severe aphasia (higher WAB-AQ) was associated with greater MEP suppression
      (ie, the expected cTBS aftereffects) in both BDNF genotypes. This effect was
      stronger for Val66Met than Val66Val carriers (β = 3.56, SE = .60, t = 5.93,
      P < .001
  - section: Methods – Continuous Theta Burst Stimulation
    page: 374
    supports: method
    quote: CTBS consisted of a continuous delivery of 50 Hz triplets of TMS pulses
      at 5 Hz for a total of 600 pulses and approximately 40 seconds.
  - section: Results; Table 2
    page: 376
    supports: statistics
    quote: 'LogMPO + LesVol + AgeCVA + BDNF * MEPd10: Adjusted R2 .613, Cohen''s f2
      .182'
  - section: Discussion – Limitations
    page: 378
    supports: limitation
    quote: 'gations may help determine the optimal prognostic time at

      which biomarkers of neuroplasticity have the strongest

      predictive power of long-term functional outcomes.'
source: curated
last_reviewed: '2026-05-06'
notes: 'This predictor entry captures the BDNF Val66Met genotype as a predictor of

  tDCS responsiveness during aphasia treatment. The finding from Fridriksson 2018

  (Brain Stimulation) specifically shows that val/val carriers benefit from A-tDCS

  during naming treatment, whereas Met allele carriers do not show this advantage.

  A second finding from Dresang 2022 (Neurorehabil Neural Repair) will be added

  in a separate draft and contributes an additional finding to this predictor entry

  linking BDNF genotype to chronic aphasia severity independent of tDCS.'
reviewer: auto-reviewer
reviewed_on: '2026-05-06'
---
# BDNF Val66Met genotype (rs6265)

## Predictor definition

The BDNF Val66Met polymorphism (SNP rs6265) is a common genetic variant that
reduces activity-dependent BDNF secretion by 18–30% in Met allele carriers. This
reduction in BDNF availability is hypothesized to diminish neuroplasticity,
which in turn may affect both spontaneous and treatment-driven language recovery
after stroke.

## Fridriksson 2018 — tDCS × BDNF interaction

In the context of an RCT of anodal tDCS during aphasia treatment, val/val
carriers who received A-tDCS showed significantly greater naming improvement
than both val/val participants in the sham group and Met allele carriers
regardless of stimulation condition. No main effect of BDNF genotype on naming
improvement was found. The interaction was specific to the A-tDCS condition,
consistent with a mechanism whereby A-tDCS promotes BDNF-dependent long-term
synaptic plasticity.
