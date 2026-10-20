---
schema_version: 2.3
id: left_posterior_planum_temporale_spt
name: "Left Posterior Planum Temporale (Area Spt)"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
notes: "New region ID created for area Spt (Sylvian-parietal-temporal)."

findings:
  - id: f1
    target: conduction_aphasia
    target_kind: impairment
    claim: "Damage to the left posterior planum temporale (area Spt) is associated with the symptoms of conduction aphasia, including impaired verbatim repetition and phonological short-term memory deficits."
    direction: likely
    relationship: causal
    citation: "@Buchsbaum2011"
    method: LSM
    design: cross-sectional
    evidence_quality: cohort
    strength: moderate
    sample:
      n: 14
      population: "chronic left-hemisphere middle cerebral artery stroke patients with conduction aphasia"
      time_post_onset: "mean 56.1 months (SD 55.8; range 13-247)"
      age_range: "mean 61.6 (SD 9.3; range 48-77)"
      handedness: "all right-handed except one left-handed and one ambidextrous"
      language: "Native English speakers"
    statistics:
      threshold: "not_reported"
      cluster_extent: null
      effect_size: "85% lesion overlap at peak"
      p_value: "not_reported"
    confounders_controlled: []
    confounders_not_controlled: ["lesion volume"]
    region_definition:
      kind: data_driven_cluster
      description: "Region of maximal lesion overlap among 14 patients with conduction aphasia, which circumscribes area Spt."
    imaging_details:
      reference_space: MNI152
      atlases_used: []
      preprocessing_pipeline: "SPM5 non-linear transformation to MNI space; cost function masking used for lesion masks."
      modalities:
        - modality: T1
          sequence: not_reported
        - modality: CT
          sequence: not_reported
    author_limitations:
      - "The peak percentage of overlap in Spt was relatively modest (33%) due to neuroanatomical variability of the posterior planum temporale, making alignment across subjects difficult."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 6"
      confidence: high
      flags: []
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "the region of maximal lesion overlap in a sample of 14 patients with conduction aphasia perfectly circumscribes area Spt"
        supports: claim
      - section: "Methods"
        page: 4
        quote: "The sample consisted of fourteen patients (4 women and 10 men) who suffered a single, left hemisphere (LH) middle cerebral artery stroke resulting in a chronic conduction aphasia."
        supports: sample
      - section: "Methods"
        page: 4
        quote: "All 14 patients' reconstructed lesions were then overlaid to reveal regions of maximal lesion overlap."
        supports: method
      - section: "Results"
        page: 6
        quote: "The area of maximum overlap (85% lesion overlap and signiﬁcant encoding/delay fMRI conjunction) between the lesion overlap map and the fMRI conjunction map is displayed in the rightmost panel of Fig. 4"
        supports: statistics
      - section: "Results"
        page: 5
        quote: "The peak percentage of overlap in Spt was what might appear to be a relatively modest value of 33%... reﬂects to some extent the neuroanatomical var-iability of the posterior portion of the planum temporale"
        supports: limitation

  - id: f2
    target: conduction_aphasia
    target_kind: impairment
    claim: "Area Spt in the left posterior planum temporale is recruited during both the encoding and delay phases of a phonological working memory task, behaviors that are impaired in conduction aphasia."
    direction: likely
    relationship: recruitment
    citation: "@Buchsbaum2011"
    method: fMRI_activation
    design: cross-sectional
    evidence_quality: cohort
    strength: strong
    sample:
      n: 105
      population: "healthy subjects"
      time_post_onset: "not_applicable"
      age_range: "8-42 years"
      handedness: "not_reported"
      language: "not_reported"
    statistics:
      threshold: "permutation-based corrected p < .05; conjunction threshold 22%"
      cluster_extent: 70
      effect_size: "33% of subjects showed significant activation in Spt"
      p_value: ".05"
    confounders_controlled: []
    confounders_not_controlled: ["field strength (3T or 4T)", "imaging sequence"]
    region_definition:
      kind: data_driven_cluster
      description: "Region in the posterior portion of the planum temporale (Spt) identified via aggregate fMRI analysis of phonological working memory."
    imaging_details:
      reference_space: MNI152
      atlases_used: []
      preprocessing_pipeline: "FNIRT non-linear volumetric registration to MNI space; FLIRT linear normalization for subjects without high-res MRI."
      task:
        name: "Phonological working memory"
        description: "Auditory presentation of verbal material followed by a delay period involving verbal rehearsal and a response phase (serial recall or recognition)."
        contrasts: ["encoding > baseline", "delay > baseline", "encoding \\ delay conjunction"]
        baseline: "baseline estimate of BOLD activity"
      modalities:
        - modality: fMRI
          sequence: not_reported
    author_limitations:
      - "The peak percentage of overlap in Spt was relatively modest (33%) due to neuroanatomical variability of the posterior planum temporale."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 5"
      confidence: high
      flags: []
    source_passages:
      - section: "Introduction"
        page: 2
        quote: "area Spt (Sylvian-parietal–temporal), activates during both perception (stimulus encoding) and convert rehearsal in tests of phonological memory"
        supports: claim
      - section: "Methods"
        page: 2
        quote: "we have gathered 105 single subject fMRI scans on a phonological working memory paradigm"
        supports: sample
      - section: "Methods"
        page: 2
        quote: "performed an aggregate analysis on the entire set of statistical activation maps"
        supports: method
      - section: "Methods"
        page: 4
        quote: "A null hypothesis distribution for the conjunction of encoding and delay phases... yielded a threshold of 22%."
        supports: statistics
      - section: "Results"
        page: 5
        quote: "The peak percentage of overlap in Spt was what might appear to be a relatively modest value of 33%"
        supports: limitation
---
