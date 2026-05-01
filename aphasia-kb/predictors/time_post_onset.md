---
schema_version: 2.3
id: time_post_onset
name: "Time post-stroke onset"
aliases:
  - time post-onset
  - time since stroke
  - time post-stroke
  - chronicity
  - post-stroke interval
kind: predictor
predictor_type: clinical
short_definition: >-
  Time elapsed between the patient's stroke event and the measurement of
  interest (imaging, behavioural assessment, or therapy onset), typically
  reported in days or months.
assessment:
  - Stroke onset date (chart review)
  - Symptom-onset interview (when chart unavailable)
units: "days or months (specify per finding)"
typical_range: "<7 days (acute) | 7–30 days (subacute) | >6 months (chronic)"
direction_of_severity: not_applicable
status: approved
reviewer: human:michele
reviewed_on: 2026-05-01
created_by: human:michele
created_on: 2026-05-01
findings: []
notes: >-
  Starter entry for schema v2.3. Time post-onset gates almost every other
  prediction in the aphasia literature: acute findings (oedema, diaschisis)
  rarely generalise to chronic stages, and chronic-stage prognostic
  relationships have already absorbed most spontaneous recovery. Findings
  attached here should specify the exact window being reported and whether
  any patients changed window during follow-up.
---

# Time post-stroke onset

Time post-onset is best thought of as a *moderator* rather than a simple
predictor — most lesion-symptom and therapy-response relationships in
the literature are conditional on the chronicity stage. Conventional
windows in the aphasia literature:

- **Hyperacute** (<24 h): rare for aphasia studies; mostly stroke-unit work
- **Acute** (1–7 d): substantial oedema, ongoing thrombolysis effects
- **Subacute** (7–30 d): peak spontaneous recovery
- **Early chronic** (1–6 mo): residual recovery slows, therapy is most active
- **Chronic** (>6 mo, often ≥12 mo): considered the stable platform for
  lesion-symptom mapping and most published aphasia therapy trials

`direction_of_severity` is `not_applicable` because the relationship to
outcome is U-shaped or stage-dependent — a longer interval can mean
more spontaneous recovery (good) or more atrophy and decreased
plasticity (bad).
