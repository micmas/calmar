---
schema_version: 2.6
id: left_temporal_fusiform_cortex_posterior
name: "Left Posterior Temporal Fusiform Cortex"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-23
hemisphere: left
findings:
  - id: f1
    target: executive_functions
    target_kind: impairment
    claim: "Damage to the left posterior temporal fusiform cortex is associated with deficits in the shift-update component of attention and executive function."
    direction: likely
    relationship: causal
    citation: "@Schumacher2019"
    method: VBCM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 32
      population: "chronic post-stroke aphasia"
      time_post_onset: "at least 1 year"
      phase: chronic
      age_range: "mean 64 (SD 11.9), range 45-88"
      handedness: "pre-morbidly right-handed"
      language: "native English speakers"
    statistics:
      threshold: "voxel-level P = 0.001 and family-wise error corrected (FWEc) cluster-level P = 0.05"
      effect_size: not_reported
    confounders_controlled: ["lesion volume", "age", "education", "time post-stroke"]
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "Cluster identified via VBCM associated with the shift-update PCA component."
    imaging_details:
      field_strength: "3.0 T"
      acquisition:
        voxel_size_mm: [1.0, 1.0, 1.0]
        sequence: "T1-weighted inversion recovery"
      preprocessing_pipeline: "SPM8 modified unified segmentation-normalization (Seghier et al., 2008) + 8mm FWHM Gaussian kernel"
      reference_space: MNI152
      atlases_used: ["Harvard-Oxford atlas for grey matter"]
      coordinates_reported:
        - region: "Temporal fusiform cortex posterior"
          mni: [-40, -32, -16]
    author_limitations:
      - "Future work will require replication based on larger group sizes."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, Table 2"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 10
        quote: "shift-update was uniquely correlated with left lateral temporo-occipital regions (encompassing parts of the medial and inferior temporal gyrus, fusiform cortex...)"
        supports: claim
      - section: "Materials and methods"
        page: 3
        quote: "Thirty-eight participants were recruited... All participants had a single left hemispheric stroke... at least 1 year before assessment and imaging"
        supports: sample
      - section: "Neuroimaging data acquisition and analysis"
        page: 4
        quote: "The smoothed FCP images (% abnormality) were used to determine the brain regions where abnormality correlated with PCA component scores using a voxel-based correlational methodology (VBCM)"
        supports: method
      - section: "Neuroimaging data acquisition and analysis"
        page: 4
        quote: "Unless noted otherwise, we applied the threshold at voxel-level P = 0.001 and family-wise error corrected (FWEc) cluster-level P = 0.05."
        supports: statistics
      - section: "Neuroimaging data acquisition and analysis"
        page: 4
        quote: "High resolution structural T1-weighted MRI scans were acquired on a 3.0 T Philips Achieva scanner... acquired voxel size 1.0 x 1.0 x 1.0 mm"
        supports: imaging_details
      - section: "Discussion"
        page: 12
        quote: "In the current study we obtained 32 cases... and so future work will require replication based on larger groups sizes."
        supports: limitation
---
