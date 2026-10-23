---
schema_version: 2.6
id: left_angular_gyrus
name: "Left Angular Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-23
hemisphere: left
findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Damage to the left angular gyrus is independently associated with global cognitive impairment after stroke."
    direction: likely
    relationship: causal
    citation: "@Zhao2018"
    method: MLPA
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 410
      population: "acute ischemic stroke patients"
      time_post_onset: "three to six months after stroke"
      phase: late_subacute
      age_range: "mean 68.6 (SD 10.4)"
      handedness: "96.6% right-handed"
      language: not_reported
    statistics:
      threshold: "permutation-based p < 0.01"
      effect_size: not_reported
    confounders_controlled:
      - "age"
      - "gender"
      - "education year"
      - "presence of prior TIA or ischemic stroke"
      - "total lesion volume"
    confounders_not_controlled: []
    region_definition:
      kind: atlas
      atlas: "AAL"
      description: "Left angular gyrus as defined by the AAL atlas."
    imaging_details:
      field_strength: "1.5T or 3.0T"
      preprocessing_pipeline: "elastix linear and non-linear registration to MNI-152 template via age-specific intermediate template"
      reference_space: MNI152
      atlases_used: ["AAL"]
    author_limitations:
      - "Insufficient lesion coverage in some brain regions."
      - "Findings may not be generalizable to patients with large cerebral infarcts due to the high prevalence of small infarcts in the cohort."
      - "Used MoCA instead of detailed neuropsychological testing."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Abstract, Results"
      confidence: high
      flags: []
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "These two assumption-free analyses consistently identified the left angular gyrus, left basal ganglia structures and the white matter around the left basal ganglia as strategic structures for global cognitive impairment after stroke."
        supports: claim
      - section: "Methods - Subjects"
        page: 2
        quote: "Finally, 410 patients were included in this study"
        supports: sample
      - section: "Methods - Subjects"
        page: 2
        quote: "Montreal Cognitive Assessment at three to six months after stroke was used to assess global cognitive functioning"
        supports: sample
      - section: "Methods - Statistical analysis"
        page: 3
        quote: "Support vector regression-based lesion symptom mapping (SVR-LSM) was performed to determine the association between AIL location and post-stroke cognition measured by MoCA."
        supports: method
      - section: "Methods - Statistical analysis"
        page: 3
        quote: "The voxels with permutation-based p < 0.01 were treated as significant voxels in the multivariate analysis."
        supports: statistics
      - section: "Methods - Statistical analysis"
        page: 3
        quote: "Total MoCA and sub-scores for cognitive domains were norm-corrected for age, gender, education year and the presence of prior TIA or ischemic stroke. A correction for total lesion volume was performed..."
        supports: confounders
      - section: "Methods - Generation of lesion maps"
        page: 2
        quote: "The DWI sequences were first linearly registered to the T1 sequences of the patients (if available) and were further registered to the 1-mm T1 MNI-152 (Montreal Neurological Institute) template."
        supports: imaging_details
      - section: "Discussion"
        page: 11
        quote: "Despite this being the largest lesion-symptom mapping study in post-stroke cognitive impairment to date, there was still insufficient lesion coverage in some brain regions to be included in the analyses."
        supports: limitation
      - section: "Discussion"
        page: 11
        quote: "Consequently, some of our findings may not be generalizable to patients with large cerebral infarcts."
        supports: limitation
      - section: "Discussion"
        page: 11
        quote: "Second, we used the MoCA instead of detailed neuropsychological testing to assess global cognitive functioning and cognitive domains performance."
        supports: limitation
  - id: f2
    target: semantics
    target_kind: impairment
    claim: "Damage to the left angular gyrus is associated with language impairment."
    direction: likely
    relationship: causal
    citation: "@Zhao2018"
    method: RLSM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 410
      population: "acute ischemic stroke patients"
      time_post_onset: "three to six months after stroke"
      phase: late_subacute
      age_range: "mean 68.6 (SD 10.4)"
      handedness: "96.6% right-handed"
      language: not_reported
    statistics:
      threshold: "permutation-based p < 0.01"
      effect_size: "beta = 0.0457"
      p_value: 0.0002
    confounders_controlled:
      - "total lesion volume"
    confounders_not_controlled: []
    region_definition:
      kind: atlas
      atlas: "AAL"
      description: "Left angular gyrus as defined by the AAL atlas."
    imaging_details:
      field_strength: "1.5T or 3.0T"
      preprocessing_pipeline: "elastix linear and non-linear registration to MNI-152 template via age-specific intermediate template"
      reference_space: MNI152
      atlases_used: ["AAL"]
    author_limitations:
      - "Insufficient lesion coverage in some brain regions."
      - "Findings may not be generalizable to patients with large cerebral infarcts."
      - "Used MoCA instead of detailed neuropsychological testing."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Table 3"
      confidence: high
      flags: []
    source_passages:
      - section: "Discussion"
        page: 7
        quote: "language was most strongly (but not exclusively) associated with left hemispheric cortical regions (including the left inferior frontal gyrus, left middle temporal gyrus, left middle occipital lobe, left angular gyrus)"
        supports: claim
      - section: "Methods - Statistical analysis"
        page: 3
        quote: "Subsequently, we performed an assumption-free region of interest (ROI)-based analysis also using support vector regression."
        supports: method
      - section: "Methods - Statistical analysis"
        page: 3
        quote: "The ROIs with permutation-based p < 0.01 were treated as significant in the multivariate analysis."
        supports: statistics
      - section: "Discussion"
        page: 11
        quote: "Despite this being the largest lesion-symptom mapping study in post-stroke cognitive impairment to date, there was still insufficient lesion coverage in some brain regions to be included in the analyses."
        supports: limitation
---

Findings from Zhao et al. (2018) indicate that the left angular gyrus is a strategic region for both global cognitive impairment and specific language deficits.
