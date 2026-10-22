---
schema_version: 2.6
id: melodic_intonation_therapy
name: Melodic Intonation Therapy (MIT)
kind: therapy
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
short_description: A hierarchically structured treatment using intoned patterns and rhythmic left-hand
  tapping to facilitate speech production in nonfluent aphasia.
targets_impairments:
- brocas_aphasia
- fluency
findings:
- id: f1
  target: fluency
  target_kind: impairment
  claim: Melodic Intonation Therapy (MIT) leads to significant improvements in propositional speech and
    confrontational naming that surpass gains from non-intoned speech repetition therapy.
  direction: likely
  relationship: responder
  citation: '@Schlaug2008'
  method: behavioral_only
  design: case-series
  strength: weak
  evidence_quality: case-study
  sample:
    n: 2
    population: patients with severe nonfluent Broca's aphasia
    time_post_onset: 12-13 months
    phase: chronic
    age_range: 47-58 years
    handedness: all right-handed
    language: English
  statistics:
    threshold: not_reported
    effect_size: Patient 1 (MIT) CIUs/min increased from 4.40 to 13.90 (315.9% change); Patient 2 (SRT)
      CIUs/min increased from 3.60 to 6.80 (188.9% change).
  confounders_controlled:
  - lesion size/location
  - baseline speech production abilities
  - treatment intensity
  confounders_not_controlled:
  - small sample size
  region_definition:
    kind: not_reported
    description: behavioural-only treatment-efficacy finding — no specific brain region
  author_limitations:
  - Caution should be exercised when making generalizations from results in two prototypical patients.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, pages 5-6
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: Both interventions' post-treatment outcomes revealed significant improvement in propositional
      speech that generalized to unpracticed words and phrases; however, the MIT-treated patient's gains
      surpassed those of the control-treated patient.
    supports: claim
  - section: Participants
    page: 3
    quote: Both were diagnosed with severe nonfluent aphasia [...] and classified as having Broca's aphasia.
    supports: sample
  - section: Results
    page: 5
    quote: 'The between-treatments comparison (Patient #1 MIT vs. Patient #2 SRT) made after 40 sessions
      (see also Table 1) showed that the MIT-treated patient had greater improvement on all outcomes than
      the SRT-treated patient.'
    supports: statistics
  - section: Discussion
    page: 7
    quote: Although caution should be exercised when making generalizations from results in two prototypical
      patients...
    supports: limitation
- id: f2
  target: right_inferior_frontal_gyrus
  target_kind: region
  claim: MIT treatment is associated with increased activation in a right-hemisphere network involving
    the inferior frontal gyrus, premotor cortex, and temporal lobes during speech production.
  direction: likely
  relationship: treatment_response
  citation: '@Schlaug2008'
  method: fMRI_activation
  design: case-series
  strength: weak
  evidence_quality: case-study
  sample:
    n: 2
    population: patients with severe nonfluent Broca's aphasia
    time_post_onset: 12-13 months
    phase: chronic
    age_range: 47-58 years
    handedness: all right-handed
    language: English
  statistics:
    threshold: not_reported
    effect_size: not_reported
  confounders_controlled:
  - baseline fMRI activation
  confounders_not_controlled:
  - small sample size
  region_definition:
    kind: data_driven_cluster
    description: Right-hemisphere network involving the premotor, inferior frontal, and temporal lobes.
  imaging_details:
    field_strength: not_reported
    reference_space: not_reported
    atlases_used: []
    task:
      name: Repetition of bisyllabic words/phrases
      description: Participants repeated spoken or sung two-syllable words or phrases after an auditory
        cue.
      contrasts:
      - speaking vs. silence
      baseline: silence
  author_limitations:
  - Caution should be exercised when making generalizations from results in two prototypical patients.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, pages 5-6
    confidence: high
    flags:
    - imaging_details.reference_space not reported in text
  source_passages:
  - section: Results
    page: 5
    quote: the post40 scan also showed more prominent right-hemispheric activation involving the right
      posterior middle premotor cortex and right inferior frontal gyrus...
    supports: claim
  - section: Experimental Stimuli and fMRI Paradigm
    page: 4
    quote: 'The functional task consisted of five conditions: two experimental (spoken or sung bisyllabic
      words/phrases) and three control (humming, phonation, and silence).'
    supports: imaging_details
  - section: Results
    page: 6
    quote: 'fMRI studies revealed that Patient #1 showed significant fMRI changes in a right-hemisphere
      network involving the premotor, inferior frontal, and temporal lobes...'
    supports: statistics
  - section: Discussion
    page: 7
    quote: Although caution should be exercised when making generalizations from results in two prototypical
      patients...
    supports: limitation
---

# Notes
This is a case-series study (n=2) comparing MIT to a control Speech Repetition Therapy (SRT). The findings suggest that while both are effective, MIT's efficacy is linked to right-hemisphere recruitment.
