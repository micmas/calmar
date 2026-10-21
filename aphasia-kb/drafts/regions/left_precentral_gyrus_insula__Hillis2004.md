---
schema_version: 2.3
id: left_precentral_gyrus_insula
name: "Left Precentral Gyrus of the Insula"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: apraxia_of_speech
    target_kind: impairment
    claim: "Damage or dysfunction of the left insula, including the anterior insula and the superior tip of the precentral gyrus of the insula, is not associated with apraxia of speech in acute stroke."
    direction: no_effect
    relationship: causal
    citation: "@Hillis2004"
    method: LSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 80
      population: "acute left hemisphere, non-lacunar stroke"
      time_post_onset: "within 24 h"
      age_range: not_reported
      handedness: "all right-handed"
      language: "English"
    statistics:
      threshold: "chi-square test"
      effect_size: "chi2(1) = 0.47 (insula), 0.09 (anterior insula), 0.16 (superior tip of precentral gyrus of insula)"
      p_value: "NS"
    confounders_controlled: ["
      insular damage status (analyzed both patients with and without insular lesions)"
    ]
    confounders_not_controlled: []
    region_definition:
      kind: manual_ROI
      description: "Left insula, anterior insula, and superior tip of the precentral gyrus of the insula identified on DWI and PWI."
    imaging_details:
      field_strength: "1.5 Tesla"
      modalities:
        - modality: DWI
          sequence: "single shot EPI"
          voxel_size_mm: not_reported
          TR_ms: 10000
          TE_ms: 120
          notes: "bmax = 1000 s/mm2"
        - modality: PWI
          sequence: "single shot gradient echo EPI"
          voxel_size_mm: not_reported
          TR_ms: 2000
          TE_ms: 60
      preprocessing_pipeline: "PWI hypoperfusion defined as >2.5 s delay in time to peak arrival of contrast relative to homologous region in intact hemisphere"
      reference_space: native
      atlases_used: []
    author_limitations:
      - "The behavioral tests used may have missed subtle cases of apraxia of speech."
      - "Dysfunction may occur via diaschisis (deafferentation of remote cortex) without being apparent on DWI or PWI."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, pages 1481-1482"
      confidence: high
      flags: []
    source_passages:
      - section: "Summary"
        page: 1
        quote: "we found no association between apraxia of speech and lesions of the left insula, anterior insula or superior tip of the precentral gyrus of the insula."
        supports: claim
      - section: "Methods - Subjects"
        page: 2
        quote: "Subjects were adults with first ever, non-lacunar, ischaemic stroke affecting the left MCA territory as determined by MRI. Exclusion criteria were: [...] left-handedness [...] or lack of proficiency in English."
        supports: sample
      - section: "Methods - Imaging"
        page: 3
        quote: "Scans were done on a GE Signa 1.5 Tesla, echo planar imaging (EPI)-capable system. DWI trace images were obtained using a multislice, isotropic, single shot EPI sequence, with bmax = 1000 s/mm2 and repetition time (TR)/echo time (TE) of 10 000/120 ms. Single shot gradient echo EPI PWI, with TR/TE of 2000/60 ms, was obtained..."
        supports: imaging_details
      - section: "Results"
        page: 3
        quote: "Analysis of the regions of damage on DWI demonstrated no evidence of an association between apraxia of speech and damage to the left insula [c2(1) = 0.47; NS], as shown in Table 1. Apraxia of speech was also independent of DWI abnormality in left anterior insula [c2(1) = 0.09; NS], and independent of DWI abnormality in the superior tip of the left precentral gyrus of the insula [c2(1) = 0.16; NS]..."
        supports: statistics
      - section: "Methods - Neuropsychological tests"
        page: 3
        quote: "Thus, it should be recognized that our tests may have missed subtle apraxia of speech (in patients with or without insular damage)."
        supports: limitation
      - section: "Discussion"
        page: 7
        quote: "For example, a lesion may cause deafferentation of a remote area of cortex, causing dysfunction of that region ('diaschisis') without causing hypoperfusion apparent on PWI or bioenergetic failure apparent on DWI."
        supports: limitation
---

Finding f1 contradicts the widely cited claim from @Dronkers1996 that the superior tip of the precentral gyrus of the insula is essential for speech articulation.
