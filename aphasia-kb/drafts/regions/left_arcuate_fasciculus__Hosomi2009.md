---
schema_version: 2.3
id: left_arcuate_fasciculus
name: "Left Arcuate Fasciculus"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
findings:
  - id: f1
    target: aphasia
    target_kind: impairment
    claim: "Loss of leftward asymmetry in the number of arcuate fasciculus fibers predicts the presence of aphasia at discharge in acute left MCA stroke patients."
    direction: likely
    relationship: causal
    citation: "@Hosomi2009"
    method: tractography
    design: cross-sectional
    strength: weak
    evidence_quality: cohort
    sample:
      n: 13
      population: "right-handed patients with left middle cerebral artery infarcts"
      time_post_onset: "within 48 h after stroke onset"
      age_range: "41-85 years"
      handedness: "right-handed"
      language: "not_reported"
    statistics:
      threshold: "P < 0.05"
      effect_size: "sensitivity of 0.83 and specificity of 0.86"
      p_value: "0.015"
    confounders_controlled: []
    confounders_not_controlled: 
      - "initial stroke severity (NIHSS)"
      - "lesion size (ASPECTS DWI)"
    region_definition:
      kind: manual_ROI
      description: "Three ROIs placed on the anterior part of the superior longitudinal fasciculus, the posterior part of the superior longitudinal fasciculus, and the posterior temporal lobe."
    imaging_details:
      field_strength: "1.5-T"
      reference_space: "not_reported"
      atlases_used: []
      acquisition:
        voxel_size_mm: [2.2, 2.3, 3]
        TR_ms: 6000
        TE_ms: 88
        sequence: "single-shot echo planar imaging"
    author_limitations:
      - "The number of patients was somewhat limited."
      - "This study was performed in retrospective fashion."
    provenance:
      extracted_by: "agent"
      extracted_on: "2026-01-01"
      paper_section: "Results"
      confidence: high
      flags: 
        - "target 'aphasia' is forward-looking"
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "Loss of leftward asymmetry in number of AF fibers predicted aphasia at discharge with a sensitivity of 0.83 and specificity of 0.86."
        supports: claim
      - section: "Subjects"
        page: 2
        quote: "We carried out a retrospective review of the records of 13 consecutive right-handed patients... with left MCA infarcts identified on MRI within 48 h after stroke onset"
        supports: sample
      - section: "Abstract"
        page: 1
        quote: "We examined whether diffusion tensor (DT) tractography is of clinical value in assessing aphasia."
        supports: method
      - section: "Abstract"
        page: 1
        quote: "Asymmetry index of number of fibers was significantly lower (rightward) in the aphasic group than in the nonaphasic (P=0.015) and control (P=0.005) groups."
        supports: statistics
      - section: "Imaging"
        page: 2
        quote: "All images were obtained with a 1.5-T whole-body MRI... Images were acquired using a single-shot echo planar imaging technique with the following parameters: 6,000/88 (repetition time millisecond/echo time millisecond), with a motion-probing gradient in 15 orientations; b value=1,000 s/mm2"
        supports: imaging_details
      - section: "Image analysis"
        page: 2
        quote: "When tracking the AF, we placed three ROIs so that they covered the unilateral AF... The first ROI was on the anterior part of the superior longitudinal fasciculus, the second in the posterior part of the superior longitudinal fasciculus, and the third on the posterior temporal lobe"
        supports: region_definition
      - section: "Discussion"
        page: 6
        quote: "First, the number of patients was somewhat limited. More subjects must be included in further analyses. Second, this study was performed in retrospective fashion."
        supports: limitation
---

# Findings from Hosomi et al. (2009)

This study investigated the predictive value of arcuate fasciculus (AF) tractography in acute left MCA stroke patients. The authors found that the loss of normal leftward asymmetry in the number of AF fibers was a significant predictor of persistent aphasia at discharge.
