---
schema_version: 2.6
id: left_ifg_pars_opercularis
name: Left IFG Pars Opercularis (Broca's area, dorsal stream hub)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: brocas_aphasia
  target_kind: impairment
  claim: In acute stroke, ischemia involving any part of Broca area (BA 44/45) is strongly associated
    with Broca or global aphasia.
  direction: likely
  relationship: causal
  citation: '@Ochfeld2010'
  method: LSM
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 50
    population: right-hand-dominant patients with left hemisphere ischemic stroke
    time_post_onset: <= 48 hours from onset
    phase: acute
    age_range: 31 to 83 years
    handedness: right-hand-dominant
    language: native speakers of English
  statistics:
    threshold: P <= 0.0125 (corrected for 4 comparisons)
    effect_size: chi-square = 38.1
    p_value: '0.0001'
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: atlas
    atlas: probabilistic cytoarchitectural map (Amunts et al. 1999)
    description: Brodmann areas 44 and/or 45
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: DWI
      voxel_size_mm:
      - 4.4
      - 4.4
      - 5.0
    - modality: PWI
      voxel_size_mm:
      - 4.4
      - 4.4
      - 5.0
      sequence: time-to-peak maps
    preprocessing_pipeline: Time-to-peak maps registered to T2 images
    reference_space: not_reported
    atlases_used:
    - Amunts et al. 1999 probabilistic cytoarchitectural map
  author_limitations:
  - Relatively small sample size.
  - Limitations of WAB-R classification compared to clinical impression.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 326
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 326
    quote: The association between infarct and hypoperfusion anywhere within Broca area and the presence
      of Broca or global aphasia was much stronger in acute (chi2=38.1; df1; P<=0.0001) than in chronic
      stroke
    supports: claim
  - section: Participants
    page: 2
    quote: We included consecutive patients who were right-hand-dominant with left hemisphere ischemic
      stroke (<= 48 hours from onset of symptoms...)
    supports: sample
  - section: Statistical Analysis
    page: 2
    quote: We identified the relationship between the dichotomous lesion classifications... and dichotomous
      aphasia classifications... with chi2 tests.
    supports: method
  - section: Results
    page: 326
    quote: chi2=38.1; df1; P<=0.0001
    supports: statistics
  - section: Imaging
    page: 2
    quote: MRI scans, including T2, DWI, and PWI, were obtained on a 3-Tesla Philips magnet... Voxel size
      for PWI and DWI was 4.4 mm3. Slices were 5 mm
    supports: imaging_details
  - section: Imaging
    page: 2
    quote: with Broca area defined as Brodmann area 44 and/or 45 using a probabilistic cytoarchitectural
      map.
    supports: region_definition
  - section: Conclusion
    page: 5
    quote: Recognizing the limitations of WAB-R classification and the relatively small sample size of
      our study
    supports: limitation
- id: f2
  target: brocas_aphasia
  target_kind: impairment
  claim: In chronic stroke, ischemia involving Broca area is not reliably associated with Broca or global
    aphasia.
  direction: no_effect
  relationship: causal
  citation: '@Ochfeld2010'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 30
    population: right-hand-dominant patients with left hemisphere ischemic stroke
    time_post_onset: '>= 6 months after stroke'
    phase: chronic
    age_range: 24 to 85 years
    handedness: right-hand-dominant
    language: native speakers of English
  statistics:
    threshold: P <= 0.0125
    effect_size: chi-square = 0.54
    p_value: '0.46'
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: atlas
    atlas: probabilistic cytoarchitectural map (Amunts et al. 1999)
    description: Brodmann areas 44 and/or 45
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T2
      voxel_size_mm: not_reported
    preprocessing_pipeline: not_reported
    reference_space: not_reported
    atlases_used:
    - Amunts et al. 1999 probabilistic cytoarchitectural map
  author_limitations:
  - Relatively small sample size.
  - Limitations of WAB-R classification.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 326
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 326
    quote: The association between infarct and hypoperfusion anywhere within Broca area and the presence
      of Broca or global aphasia was... [not significant] in chronic stroke (chi2=0.54; df1; P=0.46)
    supports: claim
  - section: Participants
    page: 2
    quote: '...or >= 6 months after stroke'
    supports: sample
  - section: Results
    page: 326
    quote: chi2=0.54; df1; P=0.46
    supports: statistics
  - section: Conclusion
    page: 5
    quote: Recognizing the limitations of WAB-R classification and the relatively small sample size of
      our study
    supports: limitation
- id: f3
  target: brocas_aphasia
  target_kind: impairment
  claim: Longitudinal data shows that ischemia in Broca area predicts Broca or global aphasia acutely,
    but this association disappears by 6 months post-stroke.
  direction: mixed
  relationship: causal
  citation: '@Ochfeld2010'
  method: LSM
  design: longitudinal
  strength: strong
  evidence_quality: cohort
  sample:
    n: 20
    population: right-hand-dominant patients with left hemisphere ischemic stroke
    time_post_onset: acute (<=48h) and chronic (>=6mo)
    phase: longitudinal
    age_range: 39 to 80 years
    handedness: right-hand-dominant
    language: native speakers of English
  statistics:
    threshold: P <= 0.0125
    effect_size: acute chi2=20; chronic chi2=0
    p_value: acute P<=0.0001; chronic p=1
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: atlas
    atlas: probabilistic cytoarchitectural map (Amunts et al. 1999)
    description: Brodmann areas 44 and/or 45
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: multimodal
    preprocessing_pipeline: not_reported
    reference_space: not_reported
    atlases_used:
    - Amunts et al. 1999 probabilistic cytoarchitectural map
  author_limitations:
  - Small longitudinal subset (n=20).
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 326
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 326
    quote: In the 20 patients studied longitudinally, the association between ischemia involving part
      of Broca area and Broca or global aphasia was significant only acutely (chi2=20; df1; P<=0.0001),
      not chronically (chi2=0; df1; p=1; not significant).
    supports: claim
  - section: Results
    page: 326
    quote: 'The subset of 20 patients studied at both time periods was similar to the entire group: age
      39 to 80'
    supports: sample
  - section: Results
    page: 326
    quote: chi2=20; df1; P<=0.0001 vs. chi2=0; df1; p=1
    supports: statistics
  - section: Discussion
    page: 4
    quote: These patients may have had Broca aphasia initially, but it may have resolved over time because
      of reorganization of structure/function relationships (as confirmed in the longitudinal study of
      20 patients).
    supports: limitation
---
