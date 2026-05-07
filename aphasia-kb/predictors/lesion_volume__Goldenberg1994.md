---
schema_version: 2.3
id: lesion_volume__Goldenberg1994
name: Total lesion volume as predictor of recovery and therapy gain (Goldenberg &
  Spatt 1994)
aliases:
- lesion size
- CT-measured lesion size
kind: predictor
predictor_type: imaging_metric
short_definition: Total left-hemisphere lesion size measured on CT scans (drawn to
  standard anatomical templates) as a percentage of total left-hemisphere pixels.
  Used as a continuous predictor of AAT profile level and of change scores across
  spontaneous-recovery, therapy, and post-therapy phases.
units: '% of left-hemisphere template pixels'
typical_range: approx. 1–18% in this n=18 chronic stroke aphasia cohort
direction_of_severity: higher_is_worse
status: approved
created_by: agent:claude-opus-4-7
created_on: 2026-05-07
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  instrument: AAT mean profile level (Aachen Aphasia Test)
  score_band: AAT profile level (T-score weighted by subtest reliability; higher =
    less severe)
  interpretation: Larger CT-measured left-hemisphere lesion size is associated with
    lower initial AAT profile level (more severe aphasia) and with smaller improvement
    during all three observation phases (spontaneous recovery, intensive therapy,
    post-therapy follow-up).
  claim: Larger total left-hemisphere lesion size on CT is associated with lower initial
    aphasia severity and with smaller AAT-profile improvement across spontaneous recovery,
    intensive language therapy, and the combined observation period in chronic post-stroke
    aphasia.
  direction: likely
  relationship: correlational
  citation: '@Goldenberg1994'
  method: LSM
  design: longitudinal
  imaging: CT
  sample:
    n: 18
    population: chronic post-stroke aphasia patients eligible for intensive language
      therapy (4 women, 14 men; left-hemisphere stroke; ischaemic n=15, haemorrhagic
      n=3)
    time_post_onset: 10 patients entered at 2 months post-CVA, six at 3–4 months,
      two at 6–7 months post-CVA
    age_range: mean 61.8 years (range 34–79)
    handedness: all right-handed
    language: German (Aachen Aphasia Test administered)
    recruitment: Neurologisches Krankenhaus Rosenhügel, Vienna; 20 patients initially
      considered, 2 excluded for ceiling AAT-profile (>65)
    inclusion_criteria: aphasia sufficiently severe to merit intensive therapy; communicative
      behaviour not so severely affected as to make therapy impossible; sufficient
      general health, endurance, and motivation
    exclusion_criteria: AAT mean profile level above 65 at start of intensive therapy
      (ceiling effect); contralateral lesion not counted (one patient had additional
      right-hemisphere lesion neglected for size calculation)
  statistics:
    threshold: Pearson correlation, p<.05 (uncorrected; multiple univariate tests
      as authors note)
    cluster_extent: null
    effect_size: r = -0.47 (initial AAT-profile); r = -0.49 (spontaneous recovery);
      r = -0.41 (therapy improvement); r = -0.75 (whole observation period)
    ci_95: not_reported
    p_value: <.05 for initial AAT-profile, spontaneous recovery and therapy improvement;
      <.001 for whole observation period
  confounders_controlled: []
  confounders_not_controlled:
  - age (separately reported as r<.2; not partialled in the lesion-size correlations)
  - sex
  - time post-onset (range 2–7 months at study entry)
  - lesion site (analysed separately via subgroup contrasts)
  - type of aphasia
  - multiple-comparisons correction (authors explicitly note none was applied)
  region_definition:
    kind: manual_ROI
    description: Lesions hand-drawn on standard anatomical CT templates (Damasio &
      Damasio 1989; Kretschmann & Weinrich 1991), using ventricular and surface markings
      to align. Relative lesion size = number of redrawn-lesion pixels / total left-hemisphere
      template pixels (expressed as percentage).
  imaging_details:
    field_strength: not_reported
    acquisition:
      sequence: CT (clinical scan, performed >=1 month after CVA)
    preprocessing_pipeline: manual lesion tracing onto standard 2D anatomical templates
      (Damasio & Damasio 1989; Kretschmann & Weinrich 1991); pixel counting on the
      template
    reference_space: other
    atlases_used: []
  replications:
  - '@Pedersen2004'
  contradictions: []
  author_limitations:
  - Small (n=18) and heterogeneous sample (mixed aphasia types and severities).
  - Multiple univariate statistical tests without correction for multiple comparisons.
  - Discussion is explicitly described by the authors as speculative — intended to
    propose a hypothesis in need of confirmation.
  - Two patients (J.K., E.K.) entered the study at 6–7 months post-CVA, later than
    the rest, and showed very little recovery — temporal-onset confound.
  - CT (not MRI) lesion delineation; templates 2D rather than volumetric.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-07
    paper_section: Results, page 689 (lesion-size correlations); Methods – Computed
      Tomography, page 686
    confidence: high
    flags:
    - 'OCR scan: occasional character errors in the 1994 PDF (e.g., ''Selves'' for
      ''Selnes'', ''Jess'' for ''less'', ''parents'' for ''patients'') — quotes below
      are reproduced as the OCR rendered them; verify against original print if needed.'
    - Multiple-comparisons correction not applied; authors flag this themselves.
    - 'Forward-looking target_kind: severity_metric is the umbrella predictor entry;
      instrument here is the AAT mean profile level (German clinical battery).'
  source_passages:
  - section: Abstract
    page: 684
    supports: claim
    quote: Size of lesion had a negative influence on recovery in all phases.
  - section: Results
    page: 689
    supports: statistics
    quote: Lesion size had negative correlations to initial AAT-profile height (r
      = —0.47, p < .05) as well as to the amount of improvement during spontaneous
      recovery (r = —.49, p < .05), during therapy (r = —.41, p < .05) and across
      the whole observation period which includes spontaneous recovery, therapy and
      the post-therapeutic period (r = —.75, p < .001).
  - section: Methods – Patients
    page: 687
    supports: sample
    quote: There remained 4 women and 14 men with a mean age of 61.8 (range 34 to
      79). Ten Patients entered the study for 2 months post CVA, six 3 and 4 months,
      and two 6 and 7 months post-CVA.
  - section: Methods – Computed Tomography
    page: 686
    supports: method
    quote: Lesions were drawn to standard size anatomical templates observing ventricular
      and surface markings relative to the lesion (Damasio & Damasio, 1989; Kretschmann
      & Weinrich, 1991). Relative lesion size was estimated by counting the number
      of pixels covered by the redrawn lesion on the standard template.
  - section: Methods – Computed Tomography
    page: 686
    supports: imaging_details
    quote: CT images were obtained from all patients. All scans had been performed
      at least one month after CVA and showed clearly demarcated vascular lesions.
  - section: Discussion
    page: 694
    supports: limitation
    quote: the patient group was small and heterogeneous with respect to type and
      severity of aphasia, and that the results were obtained by multiple univariate
      statistical tests without correction for the multiplicity of comparisons while
      the interpretation considers multivariate relationships.
  - section: Discussion
    page: 694
    supports: claim
    quote: Our results confirm that size of lesion exerts a negative influence on
      recovery of aphasia
source: curated
last_reviewed: 2026-05-07
notes: 'Goldenberg & Spatt 1994 (Brain Lang 47:684–698). Vienna cohort, n=18 chronic

  left-hemisphere stroke aphasia patients. Three sequential 8-week phases:

  spontaneous recovery, intensive language therapy (2 × 45 min × 5 days/wk),

  and post-therapy observation. Linguistic outcome = mean AAT profile level.


  This draft adds findings to the canonical predictors/lesion_volume.md entry.

  The lesion-size correlations across all four windows (initial severity,

  spontaneous recovery, therapy gain, total) are reproduced verbatim from the

  Results section. The lesion-size correlation with whole-observation recovery

  is the strongest reported (r = -0.75, p < .001).


  Companion draft (regions/left_temporobasal__Goldenberg1994.md) covers the

  paper''s distinct claim that *site* matters above and beyond size: temporobasal

  damage selectively impairs therapy success.'
reviewer: cowork-claude:sonnet-4-6
reviewed_on: '2026-05-07'
---
# Lesion volume as predictor of aphasia recovery (Goldenberg & Spatt 1994)

## Study overview

Vienna cohort (n=18) of chronic left-hemisphere stroke patients with aphasia,
followed across three 8-week phases: spontaneous recovery (≤1 session/week),
intensive therapy (10 sessions/week), and post-therapy observation. Outcome
measure: AAT mean profile level. Lesions traced on CT onto 2D standard
anatomical templates; size = % of left-hemisphere template pixels.

## Lesion-size correlations (Results, p. 689)

| Window                              | r       | p     |
|-------------------------------------|---------|-------|
| Initial AAT profile height          | -0.47   | <.05  |
| Spontaneous-recovery improvement    | -0.49   | <.05  |
| Therapy improvement                 | -0.41   | <.05  |
| Whole observation period (total)    | -0.75   | <.001 |

Larger lesions → lower initial scores and smaller gains in every window.
Effect on therapy gain is roughly comparable to effect on spontaneous recovery
(see companion temporobasal draft for the dissociation by *site*).

## Caveats flagged by the authors

- Small heterogeneous sample (n=18, mixed aphasia types).
- Multiple univariate tests, no multiple-comparisons correction.
- Two patients enrolled at 6–7 months post-CVA showed minimal recovery overall.
- CT-based 2D template tracings (not volumetric MRI).
