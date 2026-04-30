---
id: ho-cort_44
name: "Inferior Frontal Gyrus, pars opercularis"
kind: atlas
atlas: HarvardOxford-cort-maxprob-thr25-2mm
atlas_index: 44
hemisphere: left
aliases:
  - "Broca's area (posterior)"
  - "BA 44"
  - "IFG opercularis"
  - "left pars opercularis"
networks: [dorsal_language]
tracts_adjacent: [arcuate_fasciculus]
findings:
  - target: fluency
    target_kind: impairment
    direction: likely
    strength: strong
    evidence_quality: meta-analysis
    sample_n: 250
    citation: "@Fridriksson2018"
    notes: "Lesion-symptom mapping in 250 chronic stroke; pars opercularis damage strongly predicts non-fluent output."
  - target: repetition
    target_kind: impairment
    direction: likely
    strength: moderate
    evidence_quality: cohort
    citation: "@Mirman2015"
    notes: "Damage to posterior IFG contributes to repetition deficits when combined with arcuate involvement."
  - target: auditory_comprehension
    target_kind: impairment
    direction: unlikely
    strength: moderate
    evidence_quality: cohort
    citation: "@Mirman2015"
    notes: "Pure pars opercularis lesions tend to spare comprehension."
  - target: mit
    target_kind: therapy
    direction: likely_responder
    strength: moderate
    evidence_quality: cohort
    citation: "@Schlaug2008"
    notes: "Patients with non-fluent aphasia from left frontal lesions show MIT-related gains in propositional speech."
source: curated
last_reviewed: 2026-04-29
notes: "Verify atlas_index against your local HarvardOxford .xml — labels are off-by-one in some installs."
---

# Inferior Frontal Gyrus, pars opercularis (Broca's area, posterior)

## Anatomical context

Posterior third of the left inferior frontal gyrus, corresponding roughly to
Brodmann area 44. Sits immediately anterior to ventral premotor cortex and
just lateral to the insula, with dense connectivity to posterior temporal
cortex via the arcuate fasciculus and to anterior temporal regions via the
extreme capsule.

## Lesion-symptom evidence

Posterior IFG damage is one of the most reliable predictors of **non-fluent,
effortful output** in chronic stroke (Fridriksson 2018). Pure cortical lesions
of pars opercularis produce milder, more transient deficits than the broader
"Broca's aphasia" syndrome, which typically additionally involves
subcortical white matter and the underlying insula.

Repetition is often impaired when posterior IFG damage co-occurs with arcuate
fasciculus involvement (Mirman 2015) — the finding in this entry should be
considered conditional on that combination.

## Therapy implications

Melodic Intonation Therapy (MIT) was developed for left-frontal non-fluent
aphasia and remains the most-cited evidence-based candidate for patients
matching this lesion pattern (Schlaug 2008). Constraint-Induced Aphasia
Therapy (CIAT) is also frequently used in this group; see `therapies/ciat.md`.

## Cautions

- Localization uncertainty: posterior IFG is anatomically adjacent to ventral
  premotor cortex; LSM studies vary in how they parcellate the boundary.
- Hemispheric assumption: this entry assumes left-hemisphere dominance for
  language. Right-handed left-dominant patients dominate the cited cohorts.
