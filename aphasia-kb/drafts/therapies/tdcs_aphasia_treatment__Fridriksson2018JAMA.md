---
schema_version: 2.3
id: tdcs_aphasia_treatment
name: Transcranial Direct Current Stimulation (tDCS) during aphasia treatment
kind: therapy
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
short_description: Non-invasive brain stimulation using low-intensity electrical current to modulate cortical
  excitability during speech therapy.
targets_impairments:
- anomic_aphasia
findings:
- id: f1
  target: naming
  target_kind: impairment
  claim: Adjunctive anodal tDCS during speech therapy is not futile for improving naming in chronic aphasia
    and showed numerically greater gains than sham stimulation.
  direction: likely
  relationship: responder
  citation: '@Fridriksson2018JAMA'
  method: clinical_RCT
  design: RCT
  strength: moderate
  evidence_quality: RCT
  sample:
    n: 74
    population: chronic left-hemisphere stroke aphasia
    time_post_onset: '>6 months'
    age_range: mean 60 (SD 10) years
    handedness: previously right-handed
    language: not_reported
    phase: chronic
  statistics:
    threshold: 1-sided significance level of .10 (futility design)
    effect_size: mean difference of 5.7 (3.3) words (95% CI, -0.9 to 12.3)
    p_value: .90 (futility P value)
  confounders_controlled:
  - enrolling site
  - baseline aphasia severity (AQ)
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Individualized temporal lobe region with the highest naming-related activation on fMRI.
  imaging: fMRI
  imaging_details:
    reference_space: native
    atlases_used: []
    preprocessing_pipeline: fMRI data coregistered with T1 scan; magnetic position tracker used for scalp
      coordinates
    modalities:
    - modality: fMRI
      notes: Used to identify the temporal lobe region with the highest naming-related activation for
        anode placement.
  author_limitations:
  - The current study was not powered for superiority analyses to compare A-tDCS with S-tDCS.
  - cannot definitively determine that the naming improvements translate to improvements in quality of
    life.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1470
    confidence: high
    flags:
    - target ID 'naming' is forward-looking
    - cohort overlaps with @Fridriksson2018, @Yourganov2015Predicting (USC/MUSC Aphasia Lab); flag for
      downstream double-counting risk in interpret_overlap().
  source_passages:
  - section: Abstract
    page: 1
    quote: The futility hypothesis P value was .90, indicating failure to reject the null hypothesis and,
      therefore, providing no evidence that further study of A-tDCS is futile.
    supports: claim
  - section: Methods - Patients
    page: 1
    quote: Patients with long-term (>6 months) aphasia due to 1 previous left hemisphere stroke were enrolled.
    supports: sample
  - section: Methods - Design
    page: 1
    quote: Double-blinded, prospective randomized clinical trial using a futility design to test adjunctive
      A-tDCS during speech therapy.
    supports: method
  - section: Results
    page: 1
    quote: The adjusted mean (SE) change from pretreatment baseline in correct naming was 13.9 (2.4) words
      (95% CI, 9.0-18.7) for A-tDCS and 8.2 (2.2) words (95% CI, 3.8-12.6) for sham tDCS, with mean (SE)
      A-tDCS difference of 5.7 (3.3) words (95% CI, -0.9 to 12.3)
    supports: statistics
  - section: Methods - Transcranial Direct Current Stimulation
    page: 2
    quote: As our goal was to stimulate surviving eloquent tissue, the anode electrode was placed over
      the temporal lobe region with the highest naming related activation on the fMRI
    supports: imaging_details
  - section: Limitations
    page: 6
    quote: The current study was not powered for superiority analyses to compare A-tDCS with S-tDCS.
    supports: limitation
---
