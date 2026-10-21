---
schema_version: 2.3
id: right_ifg_pars_triangularis
name: Right Inferior Frontal Gyrus Pars Triangularis
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: right
findings:
- id: f1
  target: aphasia_recovery
  target_kind: prognosis
  claim: The right pars triangularis is recruited in patients with left inferior frontal lesions but is
    not functionally homologous to the left pars triangularis, potentially hindering recovery.
  direction: unlikely
  relationship: recruitment
  citation: '@Turkeltaub2011'
  method: meta-analysis
  design: meta-analysis
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 105
    population: chronic aphasia after stroke
    time_post_onset: chronic
    age_range: not_reported
    handedness: not_reported
    language: not_reported
    phase: chronic
  statistics:
    threshold: FDR q = 0.01, cluster extent threshold of 100 mm3
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - aphasia type
  - language task
  region_definition:
    kind: data_driven_cluster
    description: ALE cluster in the right pars triangularis identified via meta-analysis of fMRI/PET coordinates.
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - AAL
  author_limitations:
  - The simple presence of activity for a given task does not necessarily imply normal computational efficiency.
  - Conclusions are limited to stroke-induced aphasia.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1729
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 4
    quote: A right PTr cluster in the IF- map was closely homotopic with a LH control site (4.9 mm), but
      was not functionally homologous to it.
    supports: claim
  - section: Discussion
    page: 7
    quote: The lack of a relationship between the function of the right PTr and that of the left in our
      analysis suggests that the right PTr is truly dysfunctional with respect to language processing...
    supports: claim
  - section: Methods
    page: 1
    quote: Functional neuroimaging articles using language tasks in patients with chronic aphasia after
      stroke (n = 105) and control subjects (n = 129) were collected.
    supports: sample
  - section: Methods
    page: 2
    quote: We used activation likelihood estimation (ALE), a validated, quantitative neuroimaging meta-analysis
      method...
    supports: method
  - section: Methods
    page: 1727
    quote: Significance was tested... with a false discovery rate (FDR) of 0.01, and a cluster extent
      threshold of 100 mm3.
    supports: statistics
  - section: Discussion
    page: 7
    quote: Still, the simple presence of activity for a given task does not necessarily imply normal computational
      efficiency...
    supports: limitation
---
