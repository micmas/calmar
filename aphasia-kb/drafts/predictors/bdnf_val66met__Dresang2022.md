---
schema_version: 2.3
id: bdnf_val66met
name: "BDNF Val66Met genotype (rs6265)"
kind: predictor
status: draft
created_by: "agent:claude-sonnet-4-6"
created_on: 2026-05-06
predictor_type: demographic
short_definition: "Common single-nucleotide polymorphism (rs6265) in the BDNF gene; val/val (typical) vs val/met (atypical, Met allele carriers). Met allele carriers show reduced activity-dependent BDNF secretion and diminished neuroplasticity."
assessment:
  - "TaqMan SNP Genotyping Assay (rs6265)"
  - "saliva DNA extraction (Oragene kits)"
units: "genotype category: val/val vs val/met"
typical_range: "not_reported"
direction_of_severity: "not_applicable"

findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Val/val BDNF genotype is associated with less severe chronic aphasia than val/met genotype, after controlling for lesion volume and time post-stroke; this effect is amplified by interactions with age at stroke, cortical excitability, and stimulation-induced neuroplasticity."
    direction: likely
    relationship: correlational
    citation: "@Dresang2022"

    method: [behavioral_only, TMS]
    design: cross-sectional
    imaging: none

    sample:
      n: 17
      population: "adults with chronic left-hemisphere ischemic stroke and aphasia (University of Pennsylvania)"
      time_post_onset: "greater than 6 months (chronic); range not_reported"
      age_range: "29–79 years (see Table 1)"
      handedness: "not_reported"
      language: "not_reported"
      recruitment: "Subjects provided informed consent prior to participation, in accordance with the University of Pennsylvania Institutional Review Board."
      inclusion_criteria: "Single left-hemisphere ischemic stroke >6 months prior; WAB-AQ below aphasia diagnostic cutoff (≥93.7 excluded)."
      exclusion_criteria: "WAB-AQ ≥93.7 (aphasia diagnosis threshold); Met66Met homozygote excluded (insufficient n for analysis)."

    statistics:
      threshold: "p < .001 (main effect of BDNF genotype on WAB-AQ in linear regression)"
      cluster_extent: null
      effect_size: "β = 32.62, SE = 1.86, t = 17.53, P < .001 (BDNF genotype main effect); LASSO-adjusted R² = 0.431 for base model including BDNF"
      ci_95: "not_reported"
      p_value: "< .001"

    confounders_controlled:
      - "time post-stroke (log-transformed months post-onset)"
      - "total lesion volume"
      - "age at time of stroke"
    confounders_not_controlled:
      - "stroke location"
      - "lesion topology (only volume controlled)"
      - "race/ethnicity"
      - "aphasia type"
      - "treatment history"

    region_definition:
      kind: not_reported
      description: "Behavioral/genetic predictor finding — no specific brain region analyzed."

    imaging_details:
      reference_space: not_reported
      atlases_used: []

    replications:
      - "@Fridriksson2018BDNF"
    contradictions: []

    author_limitations:
      - "Small sample size (n=17) for examining genetic polymorphism effects; comparable to other BDNF/MEP aphasia studies but limits generalizability."
      - "It remains unclear whether BDNF polymorphism is only a significant predictor of chronic but not acute post-stroke aphasia."
      - "Additional predictors such as stroke location were not included in a single combined model due to limited sample size."
      - "Future work should replicate in larger samples of stroke patients with and without aphasia."

    evidence_quality: cohort
    strength: weak

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Abstract; Methods – Participants; Results – Linear Regression; Table 2; Discussion"
      confidence: medium
      flags:
        - "Small sample (n=17) for a genetic predictor study; LASSO cross-validation used to control for overfitting but adjusted R² increases are very small when adding BDNF alone (footnote 1 in paper notes 'small but significant effect')."
        - "BDNF groups differed in lesion volume (val/val mean 148.5 cc vs val/met mean 71.3 cc) and time post-stroke, though authors report these did not differ statistically (t=1.78, p=.12; t=0.42, p=.68); large variability."

    source_passages:
      - section: "Abstract"
        page: 371
        supports: claim
        quote: "Val66Val carriers showed less aphasia severity than Val66Met carriers, after controlling for lesion volume and time post-stroke."
      - section: "Methods – Participants"
        page: 374
        supports: sample
        quote: "Participants were 19 subjects with a single left-hemisphere ischemic stroke that occurred >6 months prior to participation... This resulted in a final sample of 17 participants."
      - section: "Results – Linear Regression"
        page: 375
        supports: statistics
        quote: "BDNF genotype shows a main effect such that when all other factors are constant, Val66Val carriers show less severity than Val66Met carriers (β = 32.62, SE = 1.86, t = 17.53, P < .001)."
      - section: "Methods – Statistical Analysis"
        page: 375
        supports: method
        quote: "We conducted a series of linear regression models in R with aphasia severity (WAB-AQ) as the outcome measure."
      - section: "Methods – Statistical Analysis"
        page: 375
        supports: confounders
        quote: "base model included factors of interest that are common predictors of aphasia, including time post-stroke (log-transformed months post-stroke onset; LogMPO), age at time of stroke, and total lesion volume (LesVol)."
      - section: "Discussion – Limitations"
        page: 378
        supports: limitation
        quote: "A potential limitation of this study is the modest sample size used to examine the behavioral effects of a genetic polymorphism."

  - id: f2
    target: severity_metric
    target_kind: predictor
    claim: "Cortical excitability (baseline MEP amplitude) measured at the intact right primary motor cortex interacts with BDNF genotype to predict chronic aphasia severity: higher excitability is associated with less severe aphasia in val/val carriers but greater severity in val/met carriers."
    direction: mixed
    relationship: correlational
    citation: "@Dresang2022"

    method: TMS
    design: cross-sectional
    imaging: none

    sample:
      n: 17
      population: "adults with chronic left-hemisphere ischemic stroke and aphasia (University of Pennsylvania)"
      time_post_onset: "greater than 6 months (chronic)"
      age_range: "29–79 years"
      handedness: "not_reported"
      language: "not_reported"
      recruitment: "University of Pennsylvania Institutional Review Board approved study."
      inclusion_criteria: "Single left-hemisphere ischemic stroke >6 months prior."
      exclusion_criteria: "WAB-AQ ≥93.7; Met66Met homozygote excluded."

    statistics:
      threshold: "p < .001"
      cluster_extent: null
      effect_size: "Val/val: β = 14.13, SE = .74, t = 19.22, P < .001; Val/met: β = −2.86, SE = .49, t = −5.82, P < .001; interaction model adjusted R² = 0.528, Cohen's f² = 0.097"
      ci_95: "not_reported"
      p_value: "< .001"

    confounders_controlled:
      - "time post-stroke (log-transformed)"
      - "lesion volume"
      - "age at time of stroke"
      - "BDNF genotype (as main effect)"
    confounders_not_controlled:
      - "stroke location"
      - "aphasia type"

    region_definition:
      kind: not_reported
      description: "TMS-based neurophysiological predictor — MEPs recorded from left FDI muscle via single-pulse TMS to right primary motor cortex. Not a brain region finding."

    imaging_details:
      reference_space: not_reported
      atlases_used: []

    replications: []
    contradictions: []

    author_limitations:
      - "Modest sample size (n=17); the distinct patterns for cortical excitability across BDNF genotype groups require replication in larger samples."
      - "MEP measurements index domain-general cortical excitability but may not directly reflect language network excitability."

    evidence_quality: cohort
    strength: weak

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results – Cortical excitability × BDNF; Table 2; Fig. 2B"
      confidence: medium
      flags:
        - "direction: mixed because the sign of the association differs by genotype group (positive for val/val, negative for val/met); this is not a within-paper analytic disagreement but a genuine genotype-moderated reversal."

    source_passages:
      - section: "Results – Cortical excitability × BDNF"
        page: 376
        supports: claim
        quote: "Cortical excitability was positively associated with WAB-AQ for Val66Val carriers (β = 14.13, SE = .74, t = 19.22, P < .001), but negatively associated with WAB-AQ for Val66Met carriers (β = −2.86, SE = .49, t = −5.82, P < .001"
      - section: "Methods – Transcranial Magnetic Stimulation"
        page: 374
        supports: method
        quote: "Magstim 2002 Stimulator with a 70 mm\nﬁgure-eight coil (Magstim Co., Whitland, Dyﬁeld, UK)."
      - section: "Results; Table 2"
        page: 376
        supports: statistics
        quote: "LogMPO + LesVol + AgeCVA + BDNF * MEPbase: Adjusted R2 .528, Cohen's f2 .097"
      - section: "Discussion"
        page: 377
        supports: limitation
        quote: "Future work may explore the utility of these indicators in"

  - id: f3
    target: severity_metric
    target_kind: predictor
    claim: "Stimulation-induced neuroplasticity (cTBS-induced MEP suppression at 10 min post-cTBS) interacts with BDNF genotype to predict chronic aphasia severity; greater MEP suppression (expected cTBS response) is associated with less severe aphasia, with the effect stronger in val/met than val/val carriers."
    direction: likely
    relationship: correlational
    citation: "@Dresang2022"

    method: TMS
    design: cross-sectional
    imaging: none

    sample:
      n: 17
      population: "adults with chronic left-hemisphere ischemic stroke and aphasia (University of Pennsylvania)"
      time_post_onset: "greater than 6 months (chronic)"
      age_range: "29–79 years"
      handedness: "not_reported"
      language: "not_reported"
      recruitment: "University of Pennsylvania Institutional Review Board approved study."
      inclusion_criteria: "Single left-hemisphere ischemic stroke >6 months prior."
      exclusion_criteria: "WAB-AQ ≥93.7; Met66Met homozygote excluded."

    statistics:
      threshold: "p < .001"
      cluster_extent: null
      effect_size: "Val/met × MEPd10 interaction: β = 3.56, SE = .60, t = 5.93, P < .001; plasticity*BDNF model adjusted R² = 0.613, Cohen's f² = 0.182"
      ci_95: "not_reported"
      p_value: "< .001"

    confounders_controlled:
      - "time post-stroke (log-transformed)"
      - "lesion volume"
      - "age at time of stroke"
      - "BDNF genotype (as main effect)"
    confounders_not_controlled:
      - "stroke location"
      - "aphasia type"

    region_definition:
      kind: not_reported
      description: "TMS/cTBS neurophysiological predictor — cTBS administered to right primary motor cortex; MEP difference (pre vs 10-min post-cTBS) as index of stimulation-induced neuroplasticity."

    imaging_details:
      reference_space: not_reported
      atlases_used: []

    replications: []
    contradictions: []

    author_limitations:
      - "Longitudinal investigations are needed to determine the optimal prognostic timepoint at which biomarkers of neuroplasticity have the strongest predictive power."
      - "All predictors could not be examined in a single combined model due to limited sample size."

    evidence_quality: cohort
    strength: weak

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results – Stimulation-induced neuroplasticity × BDNF; Table 2; Fig. 2C"
      confidence: medium
      flags:
        - "10-minute post-cTBS timepoint used because it 'showed peak stimulation effects' per ref [34] (Parchure et al.); other timepoints not analyzed here."

    source_passages:
      - section: "Results – Stimulation-induced neuroplasticity × BDNF"
        page: 376
        supports: claim
        quote: "Less severe aphasia (higher WAB-AQ) was associated with greater MEP suppression (ie, the expected cTBS aftereffects) in both BDNF genotypes. This effect was stronger for Val66Met than Val66Val carriers (β = 3.56, SE = .60, t = 5.93, P < .001"
      - section: "Methods – Continuous Theta Burst Stimulation"
        page: 374
        supports: method
        quote: "CTBS consisted of a continuous delivery of 50 Hz triplets of TMS pulses at 5 Hz for a total of 600 pulses and approximately 40 seconds."
      - section: "Results; Table 2"
        page: 376
        supports: statistics
        quote: "LogMPO + LesVol + AgeCVA + BDNF * MEPd10: Adjusted R2 .613, Cohen's f2 .182"
      - section: "Discussion – Limitations"
        page: 378
        supports: limitation
        quote: "gations may help determine the optimal prognostic time at\nwhich biomarkers of neuroplasticity have the strongest\npredictive power of long-term functional outcomes."

source: curated
last_reviewed: 2026-05-06
notes: |
  This draft adds three findings from Dresang 2022 to the bdnf_val66met predictor
  entry. This is a separate file from bdnf_val66met__Fridriksson2018BDNF.md and
  must be merged by promote.py when the canonical predictor entry is created.

  Key features of the Dresang 2022 extraction:
  - n=17 chronic aphasia patients, University of Pennsylvania
  - Three findings: (1) BDNF main effect on WAB-AQ severity; (2) BDNF ×
    cortical excitability interaction; (3) BDNF × stimulation-induced
    neuroplasticity interaction
  - All coded method: TMS or [behavioral_only, TMS] as appropriate
  - relationship: correlational throughout (no causal manipulation of BDNF)
  - strength: weak due to very small sample
  - This paper explicitly cites @Fridriksson2018BDNF as replication context
    (ref [20] in Dresang), providing cross-study convergence on val/val advantage
---

# BDNF Val66Met genotype (rs6265) — Dresang 2022 findings

## Dresang 2022 — BDNF genotype + TMS neurophysiology predicting chronic aphasia severity

This paper is the first to combine genetic (BDNF Val66Met) and neurophysiological
(TMS-derived cortical excitability and cTBS-induced neuroplasticity) biomarkers
to predict aphasia severity in chronic post-stroke aphasia patients.

Three key findings:
1. Val/val carriers show less severe aphasia than val/met carriers, controlling
   for established predictors (lesion volume, age at stroke, time post-stroke).
2. The relationship between cortical excitability (baseline MEP) and aphasia
   severity reverses sign between genotype groups.
3. Greater stimulation-induced neuroplasticity (MEP suppression after cTBS)
   predicts less severe aphasia, with a stronger effect in val/met carriers.
