---
schema_version: 2.3
id: severity_metric
name: "Aphasia severity metric (instrument-agnostic)"
aliases:
  - severity
  - aphasia severity
  - baseline severity
  - severity metric
  - WAB-AQ
  - WAB AQ
  - Aphasia Quotient
  - Western Aphasia Battery Aphasia Quotient
  - BDAE severity
  - CAT severity
  - AAT severity
  - aphasia severity rating
  - severity at intake
  - pre-treatment severity
  - initial aphasia severity
kind: predictor
predictor_type: behavioural
short_definition: >-
  Standardised score of overall aphasia severity. The exact instrument
  varies across studies (WAB-AQ, BDAE, CAT, AAT, Aphasia Severity Rating
  Scale, etc.); this entry holds findings from any of them and
  disambiguates per-finding via the `instrument` field.
assessment:
  - WAB-R Aphasia Quotient (WAB-AQ, 0–100)
  - BDAE Severity Rating (0–5)
  - Comprehensive Aphasia Test (CAT)
  - Aachen Aphasia Test (AAT)
  - Aphasia Severity Rating Scale (ASRS, 0–5)
  - Token Test
units: "varies by instrument — see `instrument` field on each finding"
typical_range: "WAB-AQ 0–100 (cut-off ~93.8); BDAE 0–5 (5 = no aphasia)"
direction_of_severity: lower_is_worse
status: approved
reviewer: human:michele
reviewed_on: 2026-05-01
created_by: human:michele
created_on: 2026-05-01
findings: []
notes: >-
  This is the umbrella entry for *any* finding about how aphasia severity
  predicts an outcome. Different studies use different instruments
  (WAB-AQ, BDAE severity, CAT, AAT, …); rather than fragmenting the
  literature into one predictor entry per instrument — which would also
  fragment the user's prognostic query when their patient was tested
  with a different battery — we keep one entry and tag each finding
  with its `instrument`, `score_band`, and a plain-language
  `interpretation`.

  When extracting:
    * Use this entry whenever the paper reports overall aphasia severity
      as a predictor of an outcome, regardless of instrument.
    * On each finding, fill `instrument` (e.g. "WAB-AQ", "BDAE severity"),
      `score_band` (e.g. "WAB-AQ 50–75 (moderate)"), and
      `interpretation` (one sentence in plain language).
    * If the paper used a *subscale* of a battery (e.g. WAB Naming, BDAE
      Auditory Comprehension) and that subscale is the *predictor*, this
      entry is fine — but consider whether a more specific predictor
      entry (e.g. `naming_score`) would be more accurate.

  When querying (`interpret_predictors`):
    * The user supplies the patient's measured value and the instrument
      that produced it. The interpreter matches findings by
      `severity_metric`, then optionally filters / weights by matching
      `instrument` (preferring exact-instrument matches).
---

# Aphasia severity metric (instrument-agnostic)

Aphasia severity is one of the most universally reported predictors in
the aphasia literature, but the field has not converged on a single
instrument. WAB-AQ dominates anglophone neuroscience papers; BDAE
severity ratings dominate older and clinical literature; CAT, AAT, and
the Token Test are more common in European and multilingual studies;
the Aphasia Severity Rating Scale appears in many therapy trials.

Putting all of these into a single `severity_metric` predictor entry
keeps the literature unified and lets a downstream interpreter answer
questions like *"my patient has a WAB-AQ of 65 — what does the
literature say about their prognosis?"* by:

1. Looking up findings on `severity_metric`.
2. Preferring findings whose `instrument` exactly matches the patient's
   instrument (WAB-AQ).
3. Falling back to findings on other instruments with a confidence
   penalty, so the user still sees the relevant evidence.

## Per-finding fields used by this entry

The optional v2.3 finding-level fields below are most useful inside
this entry (and any other predictor entry where the same construct can
be measured by multiple instruments):

| Field            | Example                                          |
|------------------|--------------------------------------------------|
| `instrument`     | `"WAB-AQ"`, `"BDAE severity"`, `"CAT"`, `"AAT"`  |
| `score_band`     | `"WAB-AQ 50–75 (moderate)"`, `"BDAE severity 2"` |
| `interpretation` | `"Moderate aphasia, intermediate prognosis"`     |

These three fields stay together — none is required, but if you fill
one, fill all three. They make per-finding filtering and per-patient
querying possible without forcing the schema to model every battery.
