---
schema_version: 2.6
id: initial_aphasia_severity
name: Initial aphasia severity (acute WAB composite)
kind: predictor
predictor_type: behavioural
short_definition: The severity of aphasia measured shortly after stroke onset.
assessment:
- Aphasia Rapid Test (ART)
- WAB-AQ
- BDAE severity rating
- CAT
- AAT
- ASRS
units: score
typical_range: varies by instrument
direction_of_severity: higher_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Initial aphasia severity measured at day 7 post-stroke is a strong independent predictor of functional
    language outcome at 3 months.
  direction: likely
  relationship: correlational
  citation: '@Benghanem2019'
  method: behavioral_only
  design: longitudinal
  strength: strong
  evidence_quality: cohort
  instrument: Aphasia Rapid Test (ART)
  score_band: all severities
  interpretation: Higher ART scores at day 7 correlate with poorer 3-month functional outcome.
  sample:
    n: 73
    population: ischemic stroke in the left middle cerebral artery (MCA) territory
    time_post_onset: day 7
    phase: early_subacute
    age_range: median 63.7 (IQR 52.3-78)
    handedness: not_reported
    language: not_reported
  statistics:
    threshold: p < 0.0002
    effect_size: OR 0.744
    p_value: '0.0002'
  confounders_controlled:
  - lesion volume
  - intersection index of left temporo-parietal region
  confounders_not_controlled:
  - amount of Speech and Language Therapy
  author_limitations:
  - The initial severity was measured with the ART, which by definition does not capture the complexity
    of aphasia.
  - The study is a single center study based on data acquired during routine care.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1306
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 1306
    quote: It retained ART D7 with an OR of 0.744 (95% CI 0.636-0.871, p < 0.0002) [as an independent
      predictor of good outcome].
    supports: claim
  - section: Materials and methods
    page: 1304
    quote: 'We enrolled 73 patients admitted to the stroke unit of the Pitié-Salpêtrière Hospital who
      consecutively met the following criteria: (1) ischemic stroke in the left middle cerebral artery
      (MCA) territory...'
    supports: sample
  - section: Materials and methods
    page: 1304
    quote: The initial severity of aphasia was assessed at day 7 post-stroke using the ART...
    supports: method
  - section: Limitations
    page: 1308
    quote: Second, the initial severity of aphasia was measured with the ART, which by definition does
      not capture the complexity of aphasia...
    supports: limitation
  region_definition:
    kind: not_reported
---
