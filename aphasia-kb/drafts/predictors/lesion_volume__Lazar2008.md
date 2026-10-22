---
schema_version: 2.6
id: lesion_volume
name: Total lesion volume
kind: predictor
predictor_type: imaging_metric
short_definition: The total volume of the stroke lesion.
units: mm3 (calculated from axial DWI)
typical_range: not_reported
direction_of_severity: higher_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Lesion size does not significantly correlate with initial language severity, 90-day language
    functioning, or total language recovery.
  direction: no_effect
  relationship: correlational
  citation: '@Lazar2008'
  method: behavioral_only
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 22
    population: first-time stroke patients with aphasia
    time_post_onset: 24-72 hours (baseline), 90 days (follow-up)
    phase: longitudinal
    age_range: mean 63.8 (SD 5.6)
    handedness: 20/22 right-handed
    language: English- and Spanish-speaking
  statistics:
    threshold: p = 0.30 to 0.40
    effect_size: r = -0.23 (baseline), -0.19 (90-day)
  confounders_controlled: []
  confounders_not_controlled:
  - speech-language therapy intensity
  region_definition:
    kind: not_reported
    description: Global lesion volume metric.
  author_limitations:
  - Small sample size may have limited the power to detect a correlation.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 532
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 532
    quote: Calculation of Pearson correlation coefficients also revealed that lesion size was not associated
      with baseline language functioning (r = -0.23; p = 0.30), 90-day language functioning (r = -0.19;
      p = 0.40), nor with the total recovery
    supports: claim
  - section: Subjects and Methods
    page: 530
    quote: Relative lesion volumes on MRI were calculated by measuring the largest X and Y diameters of
      the lesion on axial diffusion imaging, and multiplying by the number of visualised slices times
      the slice thickness (5 mm) divided by 2
    supports: method
  - section: Discussion
    page: 532
    quote: Among the limits of this study was the small sample size; a larger cohort might have increased
      the extent to which our regression model would explain variance
    supports: limitation
---
