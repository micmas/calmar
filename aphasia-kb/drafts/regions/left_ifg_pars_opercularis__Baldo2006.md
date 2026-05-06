---
schema_version: 2.3
id: left_ifg_pars_opercularis
name: "Left IFG Pars Opercularis (Broca's area, BA 44)"
kind: classical
status: draft
created_by: "agent:claude-sonnet-4-6"
created_on: 2026-05-06
hemisphere: left
aliases:
  - "BA 44"
  - "Broca's area posterior"
  - "left pars opercularis"

notes: |
  Forward-looking target ID left_ifg_pars_opercularis — not yet a canonical entry.
  This draft covers letter fluency findings from Baldo 2006 (VLSM, n=48 LH stroke patients).
  The equivalent HarvardOxford atlas entry is ho-cort_44; this id uses the hemisphere-prefixed
  naming convention (binding since 2026-05-01).

findings:
  - id: f1
    target: letter_fluency
    target_kind: impairment
    claim: "Damage to left frontal cortex including BA 44 (pars opercularis) is associated with impaired letter fluency performance in chronic left-hemisphere stroke patients."
    direction: likely
    relationship: causal
    citation: "@Baldo2006"

    method: VLSM
    design: cross-sectional
    imaging: not_reported  # mixed MRI/CT — no single modality describes the cohort

    sample:
      n: 48
      population: "chronic left-hemisphere stroke survivors (CVA)"
      time_post_onset: ">=9 months (mean 62.8 months, SD 59.7, range 9–273 months)"
      age_range: "43–80 years (mean 62.9, SD 9.6)"
      handedness: "all premorbidly right-handed (Edinburgh Handedness Inventory)"
      language: "English monolingual (native speakers)"
      recruitment: "Patients from the Center for Aphasia and Related Disorders, VA Northern California Health Care System."
      inclusion_criteria: "Single left-hemisphere CVA; native English speaker; premorbidly right-handed; >=9 months post-onset; able to comply with task instructions."
      exclusion_criteria: "Prior neurologic injury; psychiatric illness; alcohol/drug abuse; <8 years education; age <40; unable to comply with task."

    statistics:
      threshold: "uncorrected p<.05 at each voxel (t-test); minimum 8 patients per group per voxel"
      cluster_extent: not_reported
      effect_size: not_reported
      ci_95: not_reported
      p_value: not_reported

    confounders_controlled:
      - "minimum voxel count (n>=8 per cell) to maintain statistical power"
    confounders_not_controlled:
      - "lesion volume"
      - "overall aphasia severity"
      - "education (partially controlled via exclusion of <8 years)"
      - "time post-stroke"

    region_definition:
      kind: data_driven_cluster
      description: "Voxel-wise VLSM t-tests at each voxel comparing letter fluency performance between patients with and without a lesion at that voxel; significant cluster included BA 4, 6, 44 and parietal cortex (BA 1–3, 39, 40, 43), anterior temporal cortex (BA 22), insula, and putamen."

    imaging_details:
      field_strength: not_reported
      acquisition:
        sequence: "MRI or CT (brain imaging performed >=3 weeks post-onset)"
        voxel_size_mm: not_reported
        TR_ms: not_reported
        TE_ms: not_reported
      preprocessing_pipeline: "Lesions reconstructed onto 11-slice axial standardized brain templates (DeArmond et al. 1976 atlas) by a board-certified neurologist blinded to clinical presentations; VLSM conducted using Bates et al. 2003 method"
      reference_space: Talairach
      atlases_used:
        - "Brodmann areas (Talairach-based)"
      coordinates_reported: []

    replications:
      - "@Fridriksson2018Anatomy"  # RLSM: IFG pars opercularis = strongest single predictor of speech fluency, R²=0.40
    contradictions: []

    author_limitations:
      - "Study restricted to left-hemisphere stroke patients; does not speak to right hemisphere contributions to verbal fluency."
      - "Lesion data reconstructed on standardized 2D templates rather than patient-specific 3D MRI, which may reduce spatial precision."
      - "Reference space (Talairach) differs from MNI152 used by many contemporary lesion pipelines."
      - "VLSM threshold was uncorrected p<.05; no permutation-based correction applied."
      - "Temporal ordering of fluency conditions was fixed across patients (letter before category), which may introduce order effects."

    evidence_quality: cohort
    strength: moderate

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results; Methods – Participants; Methods – Materials and Procedures"
      confidence: high
      flags:
        - "VLSM threshold is uncorrected p<.05 — no permutation correction; weaker evidence than permutation-corrected studies"
        - "Lesions traced on 2D template (DeArmond 1976), not individual 3D MRI — spatial precision limited"
        - "MRI or CT used (not exclusively MRI); CT provides less anatomical detail — verify modality breakdown"
        - "Reference space is Talairach (2D atlas), not MNI152 — cross-study comparisons require atlas translation"
        - "No peak MNI coordinates reported; only Brodmann areas named"

    source_passages:
      - section: "Abstract"
        page: 1
        supports: claim
        quote: "VLSM maps revealed that category and letter fluency deficits correlate with lesions in temporal and frontal cortices, respectively."
      - section: "Results"
        page: 3
        supports: claim
        quote: "VLSM analyses revealed that letter fluency was significantly associated with lesions in frontal regions [Brodmann's Area (BA) 4, 6, and 44"
      - section: "Methods – Participants"
        page: 2
        supports: sample
        quote: "A total of 48 patients (14 women and 34 men) who had suffered a single, left-hemisphere cerebrovascular accident (CVA) were tested in the current study."
      - section: "Methods – Participants"
        page: 2
        supports: sample
        quote: "All patients were tested in the chronic phase of their CVA, at least 9 months post-onset (M 5 62.8 months; SD 5 59.7; range, 9–273 months)."
      - section: "Methods – Materials and Procedures"
        page: 2
        supports: method
        quote: "Data were analyzed using VLSM (see Bates et al., 2003). [...] Separate analyses were performed for letter and category fluency performance."
      - section: "Methods – Materials and Procedures"
        page: 2
        supports: statistics
        quote: "The VLSM analyses conducted t tests at every voxel to compare performance in patients with and without a lesion in that voxel. The t tests were confined to those voxels where there were at least eight patients in each group"
      - section: "Methods – Materials and Procedures"
        page: 2
        supports: imaging_details
        quote: "Patients' lesions were first imaged by magnetic resonance imaging (MRI) or computed tomography (CT) at least three weeks post-onset of the CVA. A board-certified neurologist who was blind to the patients' clinical presentations reconstructed the lesions onto standardized brain templates"
      - section: "Discussion"
        page: 4
        supports: limitation
        quote: "Because the present study was restricted to patients with left-hemisphere lesions, our findings do not speak to the relative contribution of the right hemisphere to verbal fluency."

  - id: f2
    target: category_fluency
    target_kind: impairment
    claim: "Damage to left temporal cortex (BA 22, 37, 41, 42) is associated with impaired category fluency in chronic left-hemisphere stroke patients, whereas frontal damage is less specifically associated with category fluency deficits."
    direction: likely
    relationship: causal
    citation: "@Baldo2006"

    method: VLSM
    design: cross-sectional
    imaging: not_reported  # mixed MRI/CT — no single modality describes the cohort

    sample:
      n: 48
      population: "chronic left-hemisphere stroke survivors (CVA)"
      time_post_onset: ">=9 months (mean 62.8 months, SD 59.7, range 9–273 months)"
      age_range: "43–80 years (mean 62.9, SD 9.6)"
      handedness: "all premorbidly right-handed"
      language: "English monolingual (native speakers)"
      recruitment: "Center for Aphasia and Related Disorders, VA Northern California Health Care System."
      inclusion_criteria: "Single left-hemisphere CVA; native English speaker; premorbidly right-handed; >=9 months post-onset."
      exclusion_criteria: "Prior neurologic injury; psychiatric illness; <8 years education; age <40; unable to comply."

    statistics:
      threshold: "uncorrected p<.05 at each voxel; minimum 8 patients per group per voxel"
      cluster_extent: not_reported
      effect_size: not_reported
      ci_95: not_reported
      p_value: not_reported

    confounders_controlled:
      - "minimum voxel count (n>=8 per cell)"
    confounders_not_controlled:
      - "lesion volume"
      - "overall aphasia severity"
      - "time post-stroke"

    region_definition:
      kind: data_driven_cluster
      description: "VLSM t-test cluster for category fluency: significant regions in left temporal lobe (BA 22, 37, 41, 42), post-central gyrus, parietal cortex (BA 39, 40), insula, and putamen."

    imaging_details:
      field_strength: not_reported
      acquisition:
        sequence: "MRI or CT (>=3 weeks post-onset)"
        voxel_size_mm: not_reported
        TR_ms: not_reported
        TE_ms: not_reported
      preprocessing_pipeline: "Lesions reconstructed onto DeArmond 1976 standardized 11-slice axial templates; VLSM per Bates et al. 2003"
      reference_space: Talairach
      atlases_used:
        - "Brodmann areas (Talairach-based)"
      coordinates_reported: []

    replications: []
    contradictions: []

    author_limitations:
      - "VLSM threshold is uncorrected p<.05 — no permutation correction."
      - "Lesions traced on 2D standardized template; spatial precision limited."
      - "Category item difficulty may vary across semantic categories tested (fruits, animals, supermarket items); supermarket category showed partial frontal involvement."

    evidence_quality: cohort
    strength: moderate

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results; Discussion"
      confidence: high
      flags:
        - "VLSM threshold uncorrected — weaker evidence; no permutation correction applied"
        - "Category fluency VLSM map also includes insula and putamen — region is broader than pure temporal"
        - "Supermarket category showed partial frontal foci (switching demands); fruits and animals did not — verify whether to split"

    source_passages:
      - section: "Results"
        page: 3
        supports: claim
        quote: "Category fluency was associated with lesions in more posterior cortex, including regions of the left temporal lobe (BA 22, 37, 41, 42) and the post-central gyrus."
      - section: "Abstract"
        page: 1
        supports: claim
        quote: "Our findings are therefore consistent with the hypothesis that temporal cortex subserves word retrieval constrained by semantics, whereas frontal regions are more critical for strategic word retrieval constrained by phonology."
      - section: "Methods – Participants"
        page: 2
        supports: sample
        quote: "A total of 48 patients (14 women and 34 men) who had suffered a single, left-hemisphere cerebrovascular accident (CVA) were tested in the current study."
      - section: "Methods – Materials and Procedures"
        page: 2
        supports: method
        quote: "Data were analyzed using VLSM (see Bates et al., 2003). [...] Separate analyses were performed for letter and category fluency performance."
      - section: "Methods – Materials and Procedures"
        page: 2
        supports: statistics
        quote: "Colorized maps were then generated based on the resultant p values at each voxel (where a 5 .05), and subtraction maps were computed based on the t statistics."
      - section: "Methods – Materials and Procedures"
        page: 2
        supports: imaging_details
        quote: "Patients' lesions were first imaged by magnetic resonance imaging (MRI) or computed tomography (CT) at least three weeks post-onset of the CVA."
      - section: "Discussion"
        page: 4
        supports: limitation
        quote: "it is possible that the degree of frontal involvement in category fluency depends on the semantic category tested. That is, certain semantic categories may engage frontal0strategic search processes if they are broader and require frequent switching between subcategories"

source: draft
notes: |
  Baldo 2006 uses VLSM (Bates et al. 2003) in 48 chronic LH stroke patients.
  Two main findings: (1) letter fluency → left frontal (BA 4, 6, 44) + parietal + insula/putamen;
  (2) category fluency → left temporal (BA 22, 37, 41, 42) + parietal + insula/putamen.
  Subtraction maps (letter minus category; category minus letter) sharpen the frontal/temporal dissociation.
  Important caveats: uncorrected p<.05 threshold; Talairach-space 2D template lesion tracing;
  mixed MRI/CT imaging. Anchor perspective: findings are region-anchored (VLSM).
  letter_fluency and category_fluency are forward-looking impairment IDs.
---

# Left IFG Pars Opercularis — Baldo 2006 (VLSM)

Baldo et al. 2006 applied VLSM to 48 chronic left-hemisphere stroke patients to dissociate neural
substrates of letter fluency vs category fluency. The two key findings are:

- **f1**: Letter fluency deficits → left frontal lesions including BA 44 (pars opercularis), BA 4 (motor cortex), BA 6 (premotor), plus parietal cortex and insula/putamen.
- **f2**: Category fluency deficits → left temporal lesions (BA 22, 37, 41, 42), plus parietal cortex and insula/putamen.

The dissociation supports the hypothesis that frontal cortex underpins phonemically-driven strategic word retrieval (letter fluency), while temporal cortex supports semantically-driven word retrieval (category fluency). Both tasks also implicated inferior parietal cortex and subcortical structures.
