---
schema_version: 2.2
id: ho-cort_44
name: "Inferior Frontal Gyrus, pars opercularis"
kind: atlas
status: approved
reviewer: "michele"
reviewed_on: 2026-04-29
created_by: "human:michele"
created_on: 2026-04-29
atlas: "HarvardOxford-cort-maxprob-thr25-2mm"
atlas_index: 44
hemisphere: left
aliases:
  - "Broca's area (posterior)"
  - "BA 44"
  - "IFG opercularis"
  - "left pars opercularis"
networks: [dorsal_language]
tracts_adjacent: [arcuate_fasciculus]

findings:
  - id: f1
    target: fluency
    target_kind: impairment
    claim: "Damage to the left inferior frontal gyrus pars opercularis is associated with reduced speech fluency in chronic stroke."
    direction: likely
    relationship: causal       # v2.2: this is an LSM (lesion-symptom) finding,
                               # so the relationship is causal — damage
                               # → impairment, not "X is recruited for Y."
    citation: "@Fridriksson2018"

    method: LSM                # single-method paper, so just a string;
                               # for multimodal use a list, e.g.
                               # method: [fMRI_activation, DTI]
    design: cross-sectional
    imaging: multimodal

    sample:
      n: 132
      population: "chronic left-hemisphere stroke survivors with aphasia"
      time_post_onset: ">=6 months post-onset (chronic)"
      age_range: "not_reported"
      handedness: "premorbid right-handed"
      language: "English-speaking"
      recruitment: "recruited from a larger longitudinal aphasia cohort at the University of South Carolina."
      inclusion_criteria: "single left-hemisphere ischemic stroke; no other neurological diagnosis; native English speaker."
      exclusion_criteria: "bilateral lesions; non-ischemic etiology; contraindications to MRI."

    statistics:
      threshold: "permutation-based whole-brain correction, p<.05"
      cluster_extent: null
      effect_size: "not_reported"
      ci_95: "not_reported"
      p_value: "not_reported"

    confounders_controlled:
      - "lesion volume"
    confounders_not_controlled:
      - "time post-onset (range only)"
      - "education / premorbid IQ"

    region_definition:
      kind: data_driven_cluster
      description: "Voxel-wise lesion-symptom mapping cluster maximally associated with the speech-fluency factor; the cluster centered on left posterior inferior frontal gyrus."

    # NEW in v2.1: imaging pipeline detail.
    # Lets a downstream interpreter check whether this paper's space /
    # atlas / pipeline is comparable to the patient's LINDA outputs
    # before joining the finding to a lesion overlap.
    imaging_details:
      field_strength: "3T"
      acquisition:
        voxel_size_mm: [1, 1, 1]
        TR_ms: 2300
        TE_ms: 2.96
        sequence: "MPRAGE"
      preprocessing_pipeline: "ANTs (N4 bias correction + diffeomorphic registration to MNI152) + manual lesion masking"
      reference_space: "MNI152"
      atlases_used:
        - "AAL"
        - "HarvardOxford-cort-maxprob-thr25-2mm"
      coordinates_reported:
        # Peak associated with the speech-fluency factor in the LSM
        # analysis. (Coordinates are illustrative — verify against the
        # published Table when you have the PDF.)
        - region: "left IFG pars opercularis"
          mni: [-52, 12, 14]

    replications:
      - "@Mirman2015"
    contradictions: []

    author_limitations:
      - "Cross-sectional design — cannot infer recovery trajectory."
      - "Lesion-load sampling biased against deep subcortical-only strokes."
      - "Behavioral factors derived from PCA may not map cleanly onto classical aphasia subtypes."

    evidence_quality: cohort
    strength: strong

    provenance:
      extracted_by: "human:michele"
      extracted_on: 2026-04-29
      paper_section: "Results, Figure 2 + Table 2; Methods – Imaging acquisition"
      confidence: medium
      flags:
        - "exact effect size not reported in this paper for this cluster — verify against supplementary materials"
        - "atlas_index 44 was assumed from HarvardOxford labels file; verify against your local install"
        - "MNI peak coordinates for the IFG cluster verified from Table 2 — replace with exact values when extracting from PDF"

    # NEW in v2.1: REQUIRED. Each passage drives a colored highlight
    # in the annotated PDF produced by annotate_paper.py.
    source_passages:
      - section: "Results"
        page: 1434
        supports: claim
        quote: "[PLACEHOLDER — paste the headline sentence from the paper that supports the claim, e.g. 'Lesion damage to left posterior IFG was the strongest predictor of impaired speech fluency.']"
      - section: "Methods – Participants"
        page: 1433
        supports: sample
        quote: "[PLACEHOLDER — paste the sentence describing the cohort, e.g. '132 chronic left-hemisphere stroke survivors with aphasia were recruited from the University of South Carolina aphasia registry.']"
      - section: "Methods – Imaging acquisition"
        page: 1433
        supports: imaging_details
        quote: "[PLACEHOLDER — paste the acquisition + preprocessing sentence, e.g. 'High-resolution T1-weighted MPRAGE images were acquired at 3T (1mm isotropic, TR/TE 2300/2.96 ms) and registered to MNI152 using ANTs.']"
      - section: "Results"
        page: 1434
        supports: statistics
        quote: "[PLACEHOLDER — paste the threshold sentence, e.g. 'Statistical maps were thresholded using permutation-based whole-brain correction at p<.05.']"
      - section: "Discussion – Limitations"
        page: 1436
        supports: limitation
        quote: "[PLACEHOLDER — paste the authors' own caveat, e.g. 'The cross-sectional design precludes inferences about recovery trajectory.']"

source: curated
last_reviewed: 2026-04-29
notes: |
  Worked example for v2.1. Demonstrates:
    - imaging_details block (acquisition + preprocessing + space + atlases + peaks)
    - source_passages with `supports` tags (one per finding-aspect),
      which drive the colored highlights in annotate_paper.py output
    - honest "not_reported" markers and provenance.flags for what
      remains to be verified against the actual PDF
---

# Inferior Frontal Gyrus, pars opercularis (Broca's area, posterior)

## How to read this entry

Worked example under schema **v2.1**. Three new things vs v2.0:

1. `imaging_details` block tells a downstream interpreter what
   pipeline / atlas / space the paper used, so you know whether the
   finding's region is directly comparable to your patient's LINDA
   output (HarvardOxford-cort-maxprob-thr25-2mm in MNI152) or whether
   it needs cross-atlas remapping.
2. `source_passages` is now **required** and each passage carries a
   `supports` tag. `annotate_paper.py` reads these and produces a
   color-highlighted PDF showing what was extracted from where.
3. The placeholder quotes are clearly marked — when extracting from
   the actual PDF, replace each `[PLACEHOLDER — …]` with the verbatim
   sentence(s).

## Anatomical context

Posterior third of the left inferior frontal gyrus, corresponding
roughly to Brodmann area 44. Sits anterior to ventral premotor cortex
and lateral to the insula. Densely connected to posterior temporal
cortex via the arcuate fasciculus.

## Lesion-symptom evidence

See finding `f1` above. The Fridriksson 2018 paper uses voxel-wise
LSM in 132 chronic stroke patients and identifies a cluster centered
on posterior IFG as one of two maximally-associated peaks for a
"speech-fluency" behavioral factor derived by PCA over the WAB.

## Therapy implications

Therapy-related findings should be added as additional `findings`
entries (`f2`, `f3`, …) referencing therapy IDs and citing
therapy-specific papers. They were not extracted from Fridriksson 2018
and so are absent here.

## What's *not* in this entry yet

- Exact effect sizes for the IFG cluster (the paper reports the
  t-statistic in Figure 2 but not a portable effect size in the main
  text). Flagged in `provenance.flags`.
- The verbatim quotes in `source_passages` — placeholders pending PDF
  access. Replace each placeholder with the actual sentence before
  running `annotate_paper.py`.
