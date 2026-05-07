---
schema_version: 2.3
id: left_temporobasal__Goldenberg1994
name: Left Temporobasal Cortex (basal temporal lobe / entorhinal–perisylvian junction)
kind: classical
status: approved
created_by: agent:claude-opus-4-7
created_on: 2026-05-07
hemisphere: left
aliases:
- left basal temporal lobe
- left temporo-basal cortex
- basal portion of left temporal lobe
- left entorhinal cortex (adjacent)
networks:
- ventral_language
- hippocampal_perisylvian_disconnection
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: 'In chronic post-stroke aphasia, lesions extending into the basal portion
    of the left temporal lobe are associated with markedly reduced response to intensive
    language therapy and reduced total recovery, but spare the spontaneous-recovery
    phase — a dissociation that persists when lesion size is matched between groups.
    The proposed mechanism is disconnection between the hippocampal formation (via
    entorhinal cortex) and perisylvian language areas, impairing explicit learning
    of linguistic knowledge and compensatory strategies.

    '
  direction: unlikely_responder
  relationship: responder
  citation: '@Goldenberg1994'
  method: LSM
  design: longitudinal
  imaging: CT
  sample:
    n: 18
    population: chronic post-stroke aphasia (4 women, 14 men; left-hemisphere stroke;
      ischaemic n=15, haemorrhagic n=3)
    time_post_onset: 10 patients at 2 months, six at 3–4 months, two at 6–7 months
      post-CVA at study entry
    age_range: mean 61.8 (range 34–79)
    handedness: all right-handed
    language: German (Aachen Aphasia Test)
    recruitment: Neurologisches Krankenhaus Rosenhügel, Vienna; eligible for intensive
      language therapy
    inclusion_criteria: aphasia severe enough to merit intensive therapy; communicative
      behaviour and general health adequate for therapy participation
    exclusion_criteria: ceiling AAT-profile (>65) at therapy onset (n=2 excluded);
      right-hemisphere lesion-volume not counted in size estimate
  statistics:
    threshold: Mann–Whitney U tests (nonparametric, justified by small subgroup sizes);
      p<.05 uncorrected; multiple comparisons not corrected
    cluster_extent: null
    effect_size: 'Subgroup means (Table 4, n=6 with damage vs n=12 without): lesion
      size 8.9 vs 3.6 (p=.005); spontaneous improvement 1.8 vs 4.1 (p>.1); therapy
      improvement 1.5 vs 4.6 (p=.002); total improvement 2.2 vs 7.3 (p=.006). Lesion-size-matched
      comparison (Table 5, n=5 vs n=5): therapy improvement 1.5 vs 4.5 (p=.02); total
      improvement 2.2 vs 5.3 (p=.08). Lesion-size-and-onset-matched comparison (Table
      6, n=3 vs n=5): therapy improvement 1.9 vs 4.5 (p=.05).

      '
    ci_95: not_reported
    p_value: .002 for therapy improvement (Table 4); .02 for therapy improvement after
      lesion-size matching (Table 5); .05 for therapy improvement after also matching
      time post-onset (Table 6)
  confounders_controlled:
  - lesion size (matched by patient selection in Tables 5–6)
  - time post-onset (matched by patient selection in Table 6)
  - 'type of aphasia (distribution equalised in Table 5 subgroups: 2 Wernicke, 2 amnesic,
    1 global per group)'
  confounders_not_controlled:
  - age (analysed only as bivariate r<.2 for whole sample)
  - sex
  - premorbid education / linguistic background
  - multiple comparisons across tables
  - amount of pre-study spontaneous recovery before enrolment
  region_definition:
    kind: manual_ROI
    description: Basal portion of the left temporal lobe identified on CT by visual
      inspection and traced onto standard 2D anatomical templates (Damasio & Damasio
      1989; Kretschmann & Weinrich 1991). Authors note that on CT these lesions either
      directly impinge on, or are very close to, entorhinal cortex (the hippocampal-formation
      relay station for connections between neocortical association areas and the
      hippocampus).
  imaging_details:
    field_strength: not_reported
    acquisition:
      sequence: clinical CT (>=1 month post-CVA)
    preprocessing_pipeline: manual lesion tracing onto 2D anatomical templates (Damasio
      & Damasio 1989; Kretschmann & Weinrich 1991)
    reference_space: other
    atlases_used: []
    coordinates_reported: []
  replications: []
  contradictions: []
  author_limitations:
  - Patient group small (n=18) and heterogeneous in aphasia type/severity.
  - Multiple univariate tests without correction for multiple comparisons; authors
    state interpretation is highly speculative and intended only to propose a hypothesis.
  - The number of patients is not sufficient to unambiguously disentangle effects
    of size and site of temporobasal lesions on recovery.
  - Two of the six temporobasal-lesion patients entered the study at 6–7 months post-CVA,
    later than the rest — temporal-onset confound (partially addressed in Table 6
    sub-analysis with n=3 vs n=5).
  - CT-based 2D template tracing rather than volumetric MRI; entorhinal involvement
    inferred from CT proximity rather than directly visualised.
  - Disconnection mechanism is hypothesised, not directly demonstrated.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-07
    paper_section: Results (Tables 4–6, pages 692–693); Discussion (pages 694–696)
    confidence: medium
    flags:
    - 'OCR scan: 1994 PDF has occasional character errors (e.g., ''Jess'' for ''less'',
      ''parents'' for ''patients'', ''temporal}'' for ''temporal,''); quotes reproduced
      verbatim from OCR — verify against print original if precision matters.'
    - n=6 (damage) vs n=12 (no damage) in primary contrast (Table 4); shrinks to n=5/5
      (Table 5) and n=3/5 (Table 6) in size- and onset-matched sub-analyses.
    - 'direction: unlikely_responder; relationship: responder — the lesion pattern
      is a moderator of *therapy benefit*, not a damage-causes-impairment claim. Spontaneous-recovery
      effect is non-significant.'
    - 'target: prognosis is forward-looking — promote.py will create the stub on first
      use. Could also reasonably target a specific therapy id, but the paper''s therapy
      is generic neurolinguistic deficit-specific training rather than a named protocol.'
    - Mechanism (hippocampal–perisylvian disconnection blocks explicit learning) is
      the authors' own speculative interpretation, not an independent finding; recorded
      in notes rather than as a separate finding.
  source_passages:
  - section: Abstract
    page: 684
    supports: claim
    quote: Patients with lesions to tempo- robasal regions showed Jess improvement
      during therapy and less total recovery, but a similar amount of spontaneous
      recovery than patients without such lesions.
  - section: Abstract
    page: 684
    supports: claim
    quote: Lesions that affected the temporobasal regions were on average larger than
      those which spared them, but the dissociation between reduced therapy success
      and unaffected spontaneous recovery became even more conspicuous when the con-
      current effect of lesion size was minimized by appropriate selection of patients.
  - section: Results
    page: 692
    supports: statistics
    quote: Statistically, the diminution of recovery was highly significant for improvement
      during therapy and for total recovery but not for spontaneous recovery (Table
      4).
  - section: Results
    page: 692
    supports: statistics
    quote: the two groups did not significantly differ in the amount of spontaneous
      re- covery, but therapy success was significantly higher in patients without
      temporobasal lesions, and the difference in total recovery was at the margin
      of statistical significance (Table 5).
  - section: Methods – Patients
    page: 687
    supports: sample
    quote: There remained 4 women and 14 men with a mean age of 61.8 (range 34 to
      79). Ten Patients entered the study for 2 months post CVA, six 3 and 4 months,
      and two 6 and 7 months post-CVA.
  - section: Methods – Computed Tomography
    page: 686
    supports: region_definition
    quote: Lesions were drawn to standard size anatomical templates observing ventricular
      and surface markings relative to the lesion (Damasio & Damasio, 1989; Kretschmann
      & Weinrich, 1991).
  - section: Methods – Computed Tomography
    page: 686
    supports: imaging_details
    quote: CT images were obtained from all patients. All scans had been performed
      at least one month after CVA and showed clearly demarcated vascular lesions.
  - section: Results
    page: 691
    supports: method
    quote: Because the small number of patients in some of the subgroups makes the
      assumption of normal distri- bution questionable, nonparametric U tests were
      preferred for statistical comparisons.
  - section: Results
    page: 692
    supports: confounders
    quote: In order to distinguish between the role of the temporobasal location and
      that of lesion size, groups with approximately equally sized lesions were obtained
      by excluding from analysis the patient with the largest lesion encroaching on
      the temporobasal area (V.K.) and comparing the remaining five patients with
      temporobasal lesions to those five patients who had the largest lesions not
      affecting the basal temporal lobe
  - section: Discussion
    page: 694
    supports: limitation
    quote: the patient group was small and heterogeneous with respect to type and
      severity of aphasia, and that the results were obtained by multiple univariate
      statistical tests without correction for the multiplicity of com- parisons while
      the interpretation considers multivariate relationships.
  - section: Discussion
    page: 695
    supports: claim
    quote: Such lesions may cause a disconnection between the hippocampus and perisylvian
      language area either by damage to entorhi- nal cortex or by disruption of fibers
      which connect entorhinal to perisyl- vian cortex
source: curated
last_reviewed: 2026-05-07
notes: 'Goldenberg & Spatt 1994 (Brain Lang 47:684–698). Vienna cohort, n=18 chronic

  left-hemisphere stroke aphasia patients followed across three 8-week phases:

  spontaneous recovery, intensive language therapy (2 × 45 min × 5 days/wk),

  and post-therapy observation. Outcome = AAT mean profile level.


  This draft captures the paper''s *site*-specific finding: among the regions

  considered (Wernicke''s area, adjacent superior/middle temporal gyrus, inferior

  parietal lobe, and basal temporal lobe), only temporobasal damage produced a

  selective deficit in therapy benefit that survived lesion-size matching. The

  spontaneous-recovery phase was not impaired in this subgroup. The authors''

  proposed mechanism is hippocampal–perisylvian disconnection (via entorhinal

  cortex), blocking explicit/declarative learning of linguistic knowledge and

  compensatory strategies (procedural learning is presumed spared and to drive

  spontaneous recovery and the lesion-size effect).


  This is encoded as relationship: responder + direction: unlikely_responder

  because the claim is about a lesion pattern moderating *therapy gain* rather

  than a damage→impairment claim. The lesion-volume effect on overall recovery

  is captured in the companion predictor draft

  (drafts/predictors/lesion_volume__Goldenberg1994.md).


  Forward-looking target id `prognosis` is a top-level prognosis target — the

  paper''s outcome is "responsiveness to intensive language therapy" rather

  than a specific impairment.


  OCR caveats: the PDF text layer has scattered character errors typical of

  1994 scans; quotes are reproduced as the OCR rendered them so that the

  annotator''s `Ctrl+F` matching works against the same text layer.'
reviewer: cowork-claude:sonnet-4-6
reviewed_on: '2026-05-07'
---
# Left Temporobasal Cortex — therapy-responsiveness moderator (Goldenberg & Spatt 1994)

## Anatomical context

Basal portion of the left temporal lobe — the under-surface of the temporal
lobe abutting the parahippocampal gyrus. CT lesions in this region either
directly impinge on or sit very close to entorhinal cortex, the major relay
between neocortical association areas and the hippocampus. The authors
hypothesise that damage here disconnects the hippocampal formation from
perisylvian language cortex, blocking explicit (declarative) learning of
new or compensatory linguistic knowledge — while sparing procedural-learning
mechanisms presumed to drive spontaneous recovery.

## Key result by phase (Tables 4–6)

| Comparison                                      | Spontaneous     | Therapy         | Total           |
|-------------------------------------------------|-----------------|-----------------|-----------------|
| All temporobasal vs none (Table 4, 6 vs 12)     | 1.8 vs 4.1 ns   | 1.5 vs 4.6 **p=.002** | 2.2 vs 7.3 **p=.006** |
| Size-matched (Table 5, 5 vs 5)                  | 1.8 vs 2.9 ns   | 1.5 vs 4.5 **p=.02**  | 2.2 vs 5.3 p=.08      |
| Size + onset matched (Table 6, 3 vs 5)          | 2.4 vs 2.9 ns   | 1.9 vs 4.5 **p=.05**  | 3.1 vs 5.3 ns         |

The therapy-phase deficit survives both lesion-size matching and time-post-onset
matching; the spontaneous-recovery deficit does not.

## Subtest pattern (Table 7, size-matched groups)

The differential effect on therapy gain was strongest for Comprehension,
Repetition, and Written language; least for Naming and the Token Test.

## Caveats

- n=18 overall; the most stringent comparison rests on n=3 vs n=5.
- Multiple univariate tests, no multiple-comparisons correction (authors note).
- CT-based 2D template tracing; entorhinal involvement inferred from CT
  proximity rather than directly visualised.
- Disconnection mechanism is hypothesised, not demonstrated. The authors
  themselves describe the discussion as highly speculative.
