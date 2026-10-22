---
schema_version: 2.3
id: left_ifg_pars_triangularis
name: Left IFG Pars Triangularis (BA 45)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Higher activation in the left inferior frontal gyrus pars triangularis is associated with better
    language comprehension across acute, subacute, and chronic phases.
  direction: likely
  relationship: correlational
  citation: '@Stockert2020'
  method: fMRI_activation
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 34
    population: post-stroke aphasia (left frontal or temporo-parietal lesions)
    time_post_onset: acute (1-7 days), subacute (8-21 days), chronic (4-6 months)
    age_range: not_reported
    handedness: not_reported
    language: German
    phase: mixed
  statistics:
    threshold: P < 0.05, two-tailed
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: peak_coord_sphere
    mni_peak:
    - -51
    - 23
    - 23
    radius_mm: 9
    description: Spherical volume of interest based on global activation peak.
  imaging_details:
    field_strength: not_reported
    reference_space: MNI152
    atlases_used:
    - AAL
    coordinates_reported:
    - region: left IFG(tri)
      mni:
      - -51
      - 23
      - 23
  author_limitations:
  - The auditory comprehension paradigm may have been more sensitive to mapping dysfunction of temporal
    cortex as mere listening was sufficient.
  - Coarse split into two groups based on lesion location does not account for within-group lesion variability.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 852
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 9
    quote: Independent of lesion location, we found a statistically significant positive relationship
      between the magnitude of IFG(tri) activation and language performance in the acute, subacute and
      chronic phase
    supports: claim
  - section: Materials and methods
    page: 846
    quote: Thirty-four patients with first ischaemic stroke, primarily affecting the left frontal (n =
      17) or temporo-parietal (n = 17) cortex
    supports: sample
  - section: Imaging
    page: 4
    quote: we contrasted the responses to SP and REV (SP > REV) to obtain patterns of language-related
      activation.
    supports: method
  - section: Imaging
    page: 6
    quote: Mean language activation was extracted for all significant activation peaks, using spherical
      volumes of interest (r = 9 mm).
    supports: region_definition
  - section: Limitations
    page: 15
    quote: it might in part also be explained by the auditory comprehension paradigms used to map language
      activation. These may have been more sensitive to mapping dysfunction of temporal cortex
    supports: limitation
---
