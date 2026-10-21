---
schema_version: 2.6
id: left_inferior_fronto_occipital_fasciculus
name: "Left Inferior Fronto-Occipital Fasciculus"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: semantics
    target_kind: impairment
    claim: "Damage to the left inferior fronto-occipital fasciculus is associated with deficits in object semantic processing across visual and auditory modalities."
    direction: likely
    relationship: causal
    citation: "@Han2013"
    method: [LSM, DTI]
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 76
      population: "right-handed brain-damaged patients"
      time_post_onset: "at least 1 month post-onset"
      phase: chronic
      age_range: "mean 47 (SD 13; range 20-76)"
      handedness: "all right-handed"
      language: "native Chinese speakers"
    statistics:
      threshold: "Bonferroni corrected P < 0.05"
      effect_size: "lesion correlation r = -0.56 (composite); FA correlation r = 0.63 (composite)"
    confounders_controlled:
      - "overall cognitive state (MMSE)"
      - "whole lesion volume"
      - "type of brain damage"
      - "grey matter lesions in semantic-relevant regions"
      - "non-semantic control tasks (repetition, number processing)"
    confounders_not_controlled: []
    region_definition:
      kind: atlas
      atlas: "JHU white-matter tractography atlas (25%-threshold sub-template)"
      description: "Left inferior fronto-occipital fasciculus as defined by the JHU atlas."
    imaging_details:
      field_strength: "1.5T"
      modalities:
        - modality: T1
          sequence: "3D MPRAGE"
          voxel_size_mm: [0.49, 0.49, 0.7]
        - modality: DTI
          voxel_size_mm: [1.95, 1.95, 2.6]
          n_directions: 32
          b_values: [0, 1000]
      preprocessing_pipeline: "SPM5 co-registration + manual lesion tracing + ANTs registration to Talairach/MNI space; PANDA pipeline for DTI (BET, Eddycorrect, DTIFIT)"
      reference_space: MNI152
      atlases_used: ["JHU white-matter tractography atlas"]
    author_limitations:
      - "Lesion distribution was constrained to the middle cerebral artery territory, potentially limiting generalizability."
      - "The individual tracts investigated may not have specific functions; the overall network pattern might be what matters."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, pages 6, 8-10"
      confidence: high
      flags: []
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "We found that the lesion volume and fractional anisotropy value of the left inferior fronto-occipital fasciculus, left anterior thalamic radiation, and left uncinate fasciculus significantly correlated with severity of impairment in all three semantic tasks."
        supports: claim
      - section: "Materials and methods - Patients"
        page: 2
        quote: "Eighty-three patients with brain damage... Seven patients were not included in the analyses... The majority of the remaining 76 patients (61 males) patients suffered from stroke (n = 66)."
        supports: sample
      - section: "Materials and methods - Imaging data"
        page: 3
        quote: "Patients were scanned... with a 1.5 T GE SIGNA EXCITE scanner... 3D T1-weighted 3D MPRAGE images... Diffusion-weighted imaging had two separate sequences... 32 directions were covered in total."
        supports: imaging_details
      - section: "Brain-behaviour mapping analysis - Tract-semantic mapping"
        page: 5
        quote: "we adopted a widely used human brain white-matter template, the 'JHU white-matter tractography atlas' from FSL... We chose to use the 25%-threshold sub-template."
        supports: region_definition
      - section: "Results - Lesion-behaviour correlation"
        page: 8
        quote: "the lesion percentages of the following three tracts significantly correlated negatively with all three semantic tasks: left IFOF, left ATR, left uncinate fasciculus (corrected P-values = 0.05)."
        supports: statistics
      - section: "Discussion"
        page: 12
        quote: "our analyses here were constrained by the lesion distribution in the patient groups... our patients tended to have lesions in the territory of the middle cerebral artery"
        supports: limitation
---
