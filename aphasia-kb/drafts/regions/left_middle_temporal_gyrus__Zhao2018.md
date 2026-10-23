---
schema_version: 2.6
id: left_middle_temporal_gyrus
name: Left Middle Temporal Gyrus (Ventral Stream Node)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
hemisphere: left
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: Damage to the left middle temporal gyrus is associated with language impairment.
  direction: likely
  relationship: causal
  citation: '@Zhao2018'
  method: RLSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 410
    population: acute ischemic stroke patients
    time_post_onset: three to six months after stroke
    phase: late_subacute
    age_range: mean 68.6 (SD 10.4)
    handedness: 96.6% right-handed
    language: not_reported
  statistics:
    threshold: permutation-based p < 0.01
    effect_size: beta = 0.0263
    p_value: 0.003
  confounders_controlled:
  - total lesion volume
  confounders_not_controlled: []
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left middle temporal gyrus as defined by the AAL atlas.
  imaging_details:
    field_strength: 1.5T or 3.0T
    preprocessing_pipeline: elastix linear and non-linear registration to MNI-152 template via age-specific
      intermediate template
    reference_space: MNI152
    atlases_used:
    - AAL
  author_limitations:
  - Insufficient lesion coverage in some brain regions.
  - Findings may not be generalizable to patients with large cerebral infarcts.
  - Used MoCA instead of detailed neuropsychological testing.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Table 3
    confidence: high
    flags: []
  source_passages:
  - section: Discussion
    page: 7
    quote: language was most strongly (but not exclusively) associated with left hemispheric cortical
      regions (including the left inferior frontal gyrus, left middle temporal gyrus, left middle occipital
      lobe, left angular gyrus)
    supports: claim
  - section: Methods - Statistical analysis
    page: 3
    quote: Subsequently, we performed an assumption-free region of interest (ROI)-based analysis also
      using support vector regression.
    supports: method
  - section: Methods - Statistical analysis
    page: 3
    quote: The ROIs with permutation-based p < 0.01 were treated as significant in the multivariate analysis.
    supports: statistics
  - section: Discussion
    page: 11
    quote: Despite this being the largest lesion-symptom mapping study in post-stroke cognitive impairment
      to date, there was still insufficient lesion coverage in some brain regions to be included in the
      analyses.
    supports: limitation
---

Findings from Zhao et al. (2018) associate the left middle temporal gyrus with language deficits as part of a strategic network.
