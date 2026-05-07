---
schema_version: 2.3
id: left_precentral_gyrus_insula
name: Left precentral gyrus of the insula
aliases:
- left insula precentral gyrus
- insular precentral gyrus
- left anterior insula (motor speech zone)
- Dronkers insula
kind: classical
hemisphere: left
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
findings:
- id: f1
  target: apraxia_of_speech
  target_kind: impairment
  claim: Damage to the left precentral gyrus of the insula is necessary for apraxia
    of speech; all 25 patients with apraxia of speech had lesions encompassing this
    region, while none of 19 patients without apraxia of speech had lesions there.
  direction: likely
  relationship: causal
  citation: '@Dronkers1996'
  method: LSM
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 44
    population: chronic left-hemisphere stroke survivors; 25 with apraxia of speech,
      19 without
    time_post_onset: '>=1 year post-stroke (injuries occurred at least one year before
      inclusion)'
    age_range: apraxia group 32–79 years; non-apraxia group 52–80 years
    handedness: right-handed
    language: native English-speaking
    recruitment: VA Medical Center, Martinez, California; selected to meet neurological
      and speech-language criteria
    inclusion_criteria: single left-hemisphere CVA; no other neurological or psychiatric
      history; CT or MRI >=3 weeks post-onset; right-handed; native English speaker;
      normal hearing
    exclusion_criteria: disagreement between at least two certified SLPs on apraxia
      diagnosis excluded the patient
  statistics:
    threshold: 100% lesion overlap criterion (all 25 apraxia patients share one region);
      0% overlap in 19 controls — perfect double dissociation
    cluster_extent: null
    effect_size: not_reported
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled:
  - same arterial distribution across the two groups confirmed by lesion overlay
  confounders_not_controlled:
  - no formal statistical correction for multiple comparisons (overlap method only)
  - aphasia type and severity not controlled across groups
  - mixed CT and MRI (89% CT); no standardised normalisation to a common space
  - lesion volume not reported
  region_definition:
    kind: peak_coord_sphere
    description: 'Discrete area of 100% lesion overlap on section 6 of the reconstruction
      programme, localised to the precentral gyrus of the insula, directly anterior
      to the central insular sulcus. Talairach coordinates: -41, -2, 10.'
  imaging_details:
    field_strength: not_reported
    acquisition:
      voxel_size_mm: null
      TR_ms: null
      TE_ms: null
      sequence: CT (89% of cases) and MRI (11% MRI-only; 23% had both)
    preprocessing_pipeline: Manual lesion reconstruction onto Talairach-plane templates
      (DeArmond et al. 1976 atlas, 11 horizontal slices at 0° to orbital-meatal line)
      using PDP 11/45 minicomputer software (Frey et al. 1987). Lesion boundaries
      entered via electronic bitpad. No voxel-based normalisation.
    reference_space: Talairach
    atlases_used: []
    coordinates_reported:
    - region: left precentral gyrus of the insula
      talairach:
      - -41
      - -2
      - 10
  replications: []
  contradictions: []
  author_limitations:
  - Association of a lesion site with a behavioural deficit is not conclusive proof
    that the site carries out that function.
  - Mixed CT and MRI without common-space normalisation; no formal statistical correction.
  - Diagnosis of apraxia of speech is difficult to separate from coexisting aphasia
    and dysarthria.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Abstract; Results (Figure 1); Methods – Lesion reconstructions
    confidence: high
    flags:
    - No formal statistical test reported — double-dissociation is by lesion-overlap
      criterion only; cohort-level but not voxel-wise.
    - Talairach coordinate -41, -2, 10 reported in paper (page 2, col 2); no MNI equivalent.
    - 89% of lesions from CT; single-modality quantitative analyses not possible.
  source_passages:
  - section: Abstract
    page: 1
    supports: claim
    quote: All patients with articulatory planning deficits had lesions that included
      a discrete region of the left precentral gyrus of the insula
  - section: Results
    page: 1
    supports: claim
    quote: One common area of infarction was found in all 25 cases
  - section: Results
    page: 2
    supports: claim
    quote: Every one of the 25 patients with apraxia of speech had a lesion encompassing
      this discrete region of the insula
  - section: Results
    page: 2
    supports: region_definition
    quote: corresponds to Talaraich coordinates -41, - 2, 10
  - section: Methods – Subjects
    page: 3
    supports: sample
    quote: All had suffered a single left-hemisphere cerebrovascular accident with
      no other history of neurological or psychiatric problems
  - section: Methods – Subjects
    page: 3
    supports: sample
    quote: The injuries had occurred at least one year before inclusion in the study
      to ensure that the observed speech and language deficits had stabilized
  - section: Methods – Lesion reconstructions
    page: 3
    supports: imaging_details
    quote: In 89% ofthe cases, CTscans were used, including 23% of all patients who
      had both CT and MRI scans
  - section: Abstract
    page: 1
    supports: limitation
    quote: the association of a lesion site with a behavioural deficit is not conclusive
      proof that the site actually carries out that function
source: curated
last_reviewed: 2026-05-06
notes: 'Classic 3-page Nature paper. Key finding is a perfect double dissociation
  via lesion overlap:

  100% of 25 apraxia-of-speech patients had lesions at the left precentral gyrus of
  the insula

  (section 6 of the reconstruction programme), while 0/19 controls without apraxia
  had lesions

  there. No formal voxel-level statistics reported; the method predates VLSM.

  Talairach peak: -41, -2, 10.

  Coexisting conditions in the apraxia group: Broca''s aphasia 52%, bucco-facial apraxia
  48%,

  limb apraxia 52%, dysarthria 40%. The non-apraxia group had predominantly anomic
  aphasia (37%).'
reviewer: auto-reviewer
reviewed_on: '2026-05-06'
---
# Left precentral gyrus of the insula (Dronkers 1996)

## Anatomical context

The precentral gyrus of the insula is located on the anterior portion of insular cortex,
directly anterior to the central sulcus of the insula. It lies deep to the inferior frontal
and temporal opercula and cannot be seen without retracting or removing those structures.
At Talairach coordinates approximately -41, -2, 10.

## Lesion-overlap evidence

Dronkers (1996) used computerised lesion overlaying (CT/MRI reconstructed onto Talairach-plane
templates). All 25 patients with apraxia of speech shared damage to this one discrete area
(100% overlap on section 6). In a second group of 19 stroke patients without apraxia,
spanning a similar arterial distribution, this same insular area was completely spared.
This constitutes a double dissociation.

## Relation to apraxia of speech

The finding does not imply that the precentral insula *is the only* region supporting
articulation — large lesions extending into Broca's area, premotor cortex, and
subcortical structures co-occurred. Rather, this insular region appears *necessary*
for normal articulatory planning given that its damage was invariably associated with
the deficit.

## Method limitations

The lesion-overlap approach predates voxel-based lesion-symptom mapping (VLSM); no
statistical correction for multiple comparisons or lesion-volume confound was performed.
The mixed CT/MRI imaging without spatial normalisation limits precise spatial inference.
Later studies have partially challenged the uniqueness of this region (e.g., questions
about whether VLSM on larger samples replicates the finding with the same specificity).
