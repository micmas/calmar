---
schema_version: 2.3
id: sex
name: "Patient sex"
aliases:
  - sex
  - gender
  - biological sex
  - patient sex
kind: predictor
predictor_type: demographic
short_definition: >-
  Patient's reported sex (typically male / female), as recorded at study
  intake or extracted from the medical record.
units: "categorical: female | male | other | not_reported"
typical_range: "female / male (most published cohorts; some studies report finer categories)"
direction_of_severity: not_applicable
status: approved
reviewer: human:michele
reviewed_on: 2026-05-01
created_by: human:michele
created_on: 2026-05-01
findings: []
notes: >-
  Starter entry for schema v2.3. The aphasia literature on sex
  differences in lesion-symptom relationships and recovery is mixed
  and methodologically variable: some studies report that women show
  more bilateral language representation (and therefore better
  recovery from left-hemisphere damage), others find no effect after
  controlling for lesion volume and age. When extracting findings
  here, be careful to distinguish:

    * studies that report sex as a *control variable only* (no
      effect-size estimate) — these don't yield a finding;
    * studies that report a *main effect of sex* on the outcome
      (extract with `direction: likely`/`unlikely` as appropriate);
    * studies that report a *sex × lesion-location interaction* —
      flag these as `relationship: correlational` (or `responder`
      if the interaction is with therapy), and note the interaction
      structure in the `claim`.

  Most papers do not distinguish biological sex from gender; default
  to whatever the paper reports and note the ambiguity in
  `provenance.flags` if it matters for the finding.
---

# Patient sex

Patient sex is one of the most universally collected demographic
variables in stroke and aphasia research, and it is almost always
included in the descriptive table of participant characteristics.
Whether it has a robust independent effect on aphasia severity,
lesion-symptom relationships, or recovery is a long-running and
unsettled question.

When linking a paper to this predictor, check whether sex was treated
as:

- a *control variable only* (entered as a covariate but no effect
  estimate reported) — usually not worth a finding;
- a *main-effect predictor* (sex independently predicted the
  outcome) — extract with appropriate `direction`;
- an *interaction term* (the lesion-symptom or therapy-response
  relationship differed between sexes) — extract with
  `relationship: correlational` or `responder` and describe the
  interaction in the `claim`.

Many studies are underpowered to detect sex effects after
controlling for lesion volume, age, and time post-onset. Flag
power concerns in `provenance.flags` when the sample is small
relative to the number of covariates.
