---
schema_version: 2.3
id: right_ifg_pars_opercularis
name: "Right Inferior Frontal Gyrus Pars Opercularis"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: right
findings:
  - id: f1
    target: aphasia_recovery
    target_kind: prognosis
    claim: "The right dorsal pars opercularis is recruited as a compensatory mechanism for language function, particularly in patients with left inferior frontal lesions, and is functionally homologous to the left pars opercularis."
    direction: likely
    relationship: recruitment
    citation: "@Turkeltaub2011"
    method: meta-analysis
    design: meta-analysis
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 105
      population: "chronic aphasia after stroke"
      time_post_onset: "chronic"
      age_range: not_reported
      handedness: not_reported
      language: not_reported
    statistics:
      threshold: "FDR q = 0.01, cluster extent threshold of 100 mm3"
      effect_size: not_reported
    confounders_controlled: []
    confounders_not_controlled: ["aphasia type", "language task"]
    region_definition:
      kind: data_driven_cluster
      description: "ALE cluster in the right dorsal pars opercularis identified via meta-analysis of fMRI/PET coordinates."
    imaging_details:
      reference_space: MNI152
      atlases_used: ["AAL"]
      coordinates_reported:
        - region: "right ventral POp"
          mni: [52, 20, 2]
    author_limitations:
      - "The simple presence of activity for a given task does not necessarily imply normal computational efficiency."
      - "Conclusions are limited to stroke-induced aphasia."
      - "Findings cannot be extrapolated to acute or subacute aphasia."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, pages 1728-1729"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 1729
        quote: "The dorsal right POp and the right POrb were present in the IF- map, but not the IF+ map, and were homotopic and homologous with their LH counterparts in the control map."
        supports: claim
      - section: "Methods"
        page: 1727
        quote: "Functional neuroimaging articles using language tasks in patients with chronic aphasia after stroke (n = 105) and control subjects (n = 129) were collected."
        supports: sample
      - section: "Methods"
        page: 1727
        quote: "We used activation likelihood estimation (ALE), a validated, quantitative neuroimaging meta-analysis method..."
        supports: method
      - section: "Methods"
        page: 1727
        quote: "Significance was tested... with a false discovery rate (FDR) of 0.01, and a cluster extent threshold of 100 mm3."
        supports: statistics
      - section: "Methods"
        page: 1727
        quote: "Coordinates were converted to Montreal Neurological Institute space... AAL atlas anatomic labels were assigned."
        supports: imaging_details
      - section: "Discussion"
        page: 1732
        quote: "Still, the simple presence of activity for a given task does not necessarily imply normal computational efficiency..."
        supports: limitation
---
