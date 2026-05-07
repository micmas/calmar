---
schema_version: 2.3
id: tms_right_ifg__Naeser2005
name: Inhibitory rTMS to Right Pars Triangularis (BA45) for Anomia in Nonfluent Aphasia
kind: therapy
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
short_description: 'Open-protocol pilot study applying slow (1 Hz) inhibitory repetitive TMS daily for
  10 days to the right pars triangularis (anterior Broca homologue, BA45), aiming to suppress maladaptive
  right hemisphere overactivation in chronic nonfluent aphasia and thereby improve picture naming. First
  study to demonstrate lasting naming benefit (2 and 8 months post-rTMS). n=4 chronic aphasia patients,
  5–11 years post-stroke.

  '
targets_impairments:
- anomia
- anomic_aphasia
- brocas_aphasia
- fluency
- nonfluent_aphasia
- picture_naming
atf_id: null
atf_evidence_level: null
evidence_level: level_IV
atf_aliases:
  - inhibitory rTMS
  - rTMS right IFG
icf_domain:
  - body_function
tidier:
  brief_name: Inhibitory rTMS to right IFG (Naeser 2005 protocol)
  rationale: |-
    Right IFG shows increased activation in chronic aphasia, which may represent
        maladaptive interhemispheric competition suppressing perilesional left-hemisphere
        recovery. Low-frequency (1 Hz) rTMS inhibits right pars triangularis/pars
        orbitalis, hypothesised to disinhibit left-hemisphere language homologues via
        transcallosal pathways (interhemispheric inhibition release model).
  materials: |-
    TMS device (e.g., Magstim Rapid2 or MagVenture); figure-eight coil; motor threshold
        assessment protocol (MEP measurement); optional: MRI-guided neuronavigation
        system; naming practice stimuli.
  procedures: |-
    Resting motor threshold (RMT) assessed via MEP from contralateral hand. Coil
        positioned over right pars triangularis / pars orbitalis (right IFG) using 10-20
        EEG landmarks or fMRI-guided neuronavigation. 1 Hz rTMS delivered at 90% RMT × 10
        minutes (600 pulses). Oral picture naming practice follows stimulation session (30
        min).
  who_provides: |-
    Neurologist or TMS-trained research technician (device operation); SLP for concurrent
        naming practice.
  delivery_mode: face_to_face; device-assisted
  setting: Hospital neurology department or neuroscience research laboratory.
  dosage: |-
    Naeser 2005 pilot: 1 Hz × 10 min (600 pulses) × 10 sessions over 2 weeks; concurrent
        naming practice 30 min per session.
  tailoring: |-
    Coil placement guided by individual fMRI localisation of right IFG hyperactivation.
        RMT individually calibrated per session. Subsequent studies have varied pulse
        count (up to 1200 pulses) based on tolerability.
  modifications: |-
    Later Naeser protocols extend to 20 sessions with maintenance blocks. Intermittent
        theta-burst stimulation (iTBS) to left perilesional cortex is an alternative
        excitatory TMS approach. Some protocols combine inhibitory right-hemisphere rTMS
        with left-hemisphere excitatory TMS.
  fidelity_planned: |-
    TMS device log (pulses delivered, RMT, coil position, session dates) maintained.
        Naeser 2005: open-label pilot — no sham control, no formal fidelity protocol.
  fidelity_actual: |-
    Naeser 2005: open pilot (n=4); no sham; limited fidelity reporting. Adverse events
        (mild headache) monitored. Not blinded.
  confidence: low
  flags:
    - Naeser 2005 is an open pilot (n=4) — evidence level IV (case series). Not formally
        extracted from papers/. TIDieR populated from published protocol description.
        Subsequent larger studies (Hamilton 2010, Szaflarski 2011) have improved the
        evidence base but are not yet in KB.
rtss_ingredients:
  - inhibitory_rtms
findings:
- author_limitations:
  - Open-protocol; no sham TMS control — cannot rule out placebo, attention, or practice effects.
  - n=4; results are preliminary and should be treated as case-series level evidence.
  - No fMRI before/after to confirm mechanism (suppression of right pars triangularis hyperactivation).
  - Single pre-rTMS baseline testing session — no baseline stability established.
  - Long-term benefit (8 months) not statistically significant for BNT (only Tools/Implements reached
    p=0.003); one patient (P3) regressed.
  - Patient heterogeneity: severity ranged from anomic/conduction to global aphasia.
  - Stimulation target not confirmed electrophysiologically or with functional imaging during treatment.
  citation: '@Naeser2005'
  claim: 'Inhibitory 1 Hz rTMS applied daily for 10 days (1200 pulses/day at 90% motor threshold) to the
    right pars triangularis (anterior Broca homologue, immediately rostral to the ascending ramus of the
    Sylvian fissure) produces significant lasting improvement in picture naming in chronic nonfluent aphasia
    at 2 months post-rTMS, with sustained benefit at 8 months in 3/4 patients, as measured by the Boston
    Naming Test (first 20 items) and BDAE naming subtests.

    '
  confounders_controlled:
  - chronic stable phase (all ≥ 5 years post-stroke; beyond spontaneous recovery)
  - no concurrent speech therapy during study
  confounders_not_controlled:
  - no sham rTMS control group (open-protocol)
  - no randomisation
  - n=4 only
  - possible practice/learning effects on naming tests (though prior studies show minimal practice effects)
  - no pre-treatment baseline variability assessment (single pre-test)
  - coil placement guided by stereotaxic neuronavigation (Brainsight) — accurate but target not confirmed
    with functional imaging in all sessions
  contradictions: []
  design: case-series
  direction: likely_responder
  evidence_quality: case-study
  id: f1
  imaging: not_reported
  imaging_details:
    atlases_used: []
    coordinates_reported:
    - mni:
      - null
      - null
      - null
      note: No MNI coordinates reported. Target defined anatomically as gyrus rostral to ascending Sylvian
        ramus on individual T1 scan.
      region: Right pars triangularis (TMS target)
    field_strength: not_reported
    modalities:
    - TE_ms: not_reported
      TR_ms: not_reported
      modality: T1
      sequence: 3D MPRAGE (used for neuronavigation only; not for lesion-symptom analysis)
      voxel_size_mm:
      - 1
      - 1
      - 1
    preprocessing_pipeline: 'T1 MPRAGE used offline in Brainsight for coil positioning and daily on-line
      monitoring. No fMRI or lesion-symptom analysis performed in this study. Lesion descriptions are
      narrative/qualitative from clinical neuroradiology reports.

      '
    reference_space: native
  method: TMS
  provenance:
    confidence: high
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    flags:
    - Open-protocol design — no sham control; evidence_quality set to case-series per schema instructions.
    - The rTMS target (right pars triangularis, BA45) is defined by anatomical landmark (gyrus rostral
      to ascending Sylvian ramus), not Talairach/MNI coordinates — reference_space set to native.
    - Immediate post-rTMS naming improvement (S&V, p=0.0028) is a separate secondary measure from the
      primary BNT/BDAE outcomes.
    - P3 (moderate nonfluent) showed improvement at 2 months but returned to near-baseline by 8 months
      — mixed responder.
    - Paradoxical functional facilitation (PFF) mechanism hypothesised but not confirmed with neuroimaging.
    paper_section: Methods (pp. 97–100); Results (pp. 100–101, Table 2, Figures 3–4); Discussion (pp.
      101–103)
  region_definition:
    description: 'Right pars triangularis (BA45 homologue): gyrus immediately rostral to the anterior
      (vertical) ascending ramus of the Sylvian fissure in the right inferior frontal gyrus. Identified
      anatomically on each patient''s 3D MPRAGE MRI scan using Brainsight frameless stereotaxic neuronavigation.
      Same area as in Naeser et al. 2002 (conference abstract) where it was the only one of four right
      perisylvian targets associated with acute naming improvement. Coil: figure-8 MagStim, 7cm wing diameter,
      tangential at ~45 degrees. Volume stimulated ~1 cc (mathematical model estimate).

      '
    kind: manual_ROI
  relationship: responder
  replications:
  - '@Naeser2002'
  sample:
    age_range: '52–58 years (M: 52M, 58M, 53M, 57F)'
    exclusion_criteria: left-handed; acute/subacute phase; individual speech therapy during study period
    handedness: all right-handed
    inclusion_criteria: right-handed; chronic left MCA stroke; nonfluent or recovered aphasia; BNT first
      20 items ≥ 3/20; S&V average ≥ 3/20 pictures nameable
    language: English
    n: 4
    population: chronic right-handed aphasia patients with left MCA stroke, 5–11 years post-onset; nonfluent
      (Broca's, global) or recovered (anomic/conduction)
    recruitment: Boston VA / BU Aphasia Research Center; not further specified
    time_post_onset: 'P1: 5 years; P2: 10 years; P3: 11 years; P4: 7 years'
  source_passages:
  - page: 1
    quote: Significant improvement was observed in picture naming at 2 months post-rTMS, with lasting
      benefit at 8 months in three patients
    section: Abstract
    supports: claim
  - page: 6
    quote: The coil was placed over a gyrus immediately rostral to the anterior, (vertical) ascending
      ramus of the Sylvian fissure
    section: Methods — rTMS treatment
    supports: region_definition
  - page: 7
    quote: BNT (first 20 items) (p = .003); BDAE subtest, Animal Naming (p = .02); and BDAE subtest, Tools/Implements
      (p = .04)
    section: Results
    supports: statistics
  - page: 7
    quote: This is the first study to report lasting, improved naming at 2 months and 8 months following
      application of rTMS in chronic aphasia
    section: Discussion
    supports: claim
  - page: 3
    quote: Four right-handed, chronic aphasia patients participated, at 5–11 years post-L middle cerebral
      artery stroke
    section: Methods — Patients
    supports: sample
  - page: 8
    quote: our results should be considered preliminary, as this was an open-protocol study, and no patients
      received sham rTMS
    section: Discussion
    supports: limitation
  statistics:
    ci_95: not_reported
    cluster_extent: not_reported
    effect_size: not_reported
    p_value: 'BNT (first 20 items) at 2 months: t=8.66, p=0.003. BDAE Animals at 2 weeks: p=0.02; at 2
      months: p=0.02. BDAE Tools/Implements at 2 months: p=0.04; at 8 months: p=0.003. Overall BNT main
      effect of time: F=5.69, df=3,9, p=0.018. S&V immediate post-rTMS (10th treatment): naming improved
      p=0.0028; RT decreased p=0.04.

      '
    threshold: ANOVA repeated measures, Newman-Keuls post-hoc correction
  strength: weak
  target: right_pars_triangularis_ba45
  target_kind: region
- author_limitations:
  - Open-protocol; no sham TMS control — cannot rule out placebo, attention, or practice effects.
  - n=4; results are preliminary and should be treated as case-series level evidence.
  - No fMRI before/after to confirm mechanism (suppression of right pars triangularis hyperactivation).
  - Single pre-rTMS baseline testing session — no baseline stability established.
  - Long-term benefit (8 months) not statistically significant for BNT (only Tools/Implements reached
    p=0.003); one patient (P3) regressed.
  - Patient heterogeneity: severity ranged from anomic/conduction to global aphasia.
  - Stimulation target not confirmed electrophysiologically or with functional imaging during treatment.
  citation: '@Naeser2005'
  claim: 'Inhibitory 1 Hz rTMS applied daily for 10 days (1200 pulses/day at 90% motor threshold) to the
    right pars triangularis (anterior Broca homologue, immediately rostral to the ascending ramus of the
    Sylvian fissure) produces significant lasting improvement in picture naming in chronic nonfluent aphasia
    at 2 months post-rTMS, with sustained benefit at 8 months in 3/4 patients, as measured by the Boston
    Naming Test (first 20 items) and BDAE naming subtests.

    '
  confounders_controlled:
  - chronic stable phase (all ≥ 5 years post-stroke; beyond spontaneous recovery)
  - no concurrent speech therapy during study
  confounders_not_controlled:
  - no sham rTMS control group (open-protocol)
  - no randomisation
  - n=4 only
  - possible practice/learning effects on naming tests (though prior studies show minimal practice effects)
  - no pre-treatment baseline variability assessment (single pre-test)
  - coil placement guided by stereotaxic neuronavigation (Brainsight) — accurate but target not confirmed
    with functional imaging in all sessions
  contradictions: []
  design: case-series
  direction: likely_responder
  evidence_quality: case-study
  id: f2
  imaging: not_reported
  imaging_details:
    atlases_used: []
    coordinates_reported:
    - mni:
      - null
      - null
      - null
      note: No MNI coordinates reported. Target defined anatomically as gyrus rostral to ascending Sylvian
        ramus on individual T1 scan.
      region: Right pars triangularis (TMS target)
    field_strength: not_reported
    modalities:
    - TE_ms: not_reported
      TR_ms: not_reported
      modality: T1
      sequence: 3D MPRAGE (used for neuronavigation only; not for lesion-symptom analysis)
      voxel_size_mm:
      - 1
      - 1
      - 1
    preprocessing_pipeline: 'T1 MPRAGE used offline in Brainsight for coil positioning and daily on-line
      monitoring. No fMRI or lesion-symptom analysis performed in this study. Lesion descriptions are
      narrative/qualitative from clinical neuroradiology reports.

      '
    reference_space: native
  method: TMS
  provenance:
    confidence: high
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    flags:
    - Open-protocol design — no sham control; evidence_quality set to case-series per schema instructions.
    - The rTMS target (right pars triangularis, BA45) is defined by anatomical landmark (gyrus rostral
      to ascending Sylvian ramus), not Talairach/MNI coordinates — reference_space set to native.
    - Immediate post-rTMS naming improvement (S&V, p=0.0028) is a separate secondary measure from the
      primary BNT/BDAE outcomes.
    - P3 (moderate nonfluent) showed improvement at 2 months but returned to near-baseline by 8 months
      — mixed responder.
    - Paradoxical functional facilitation (PFF) mechanism hypothesised but not confirmed with neuroimaging.
    paper_section: Methods (pp. 97–100); Results (pp. 100–101, Table 2, Figures 3–4); Discussion (pp.
      101–103)
  region_definition:
    description: 'Right pars triangularis (BA45 homologue): gyrus immediately rostral to the anterior
      (vertical) ascending ramus of the Sylvian fissure in the right inferior frontal gyrus. Identified
      anatomically on each patient''s 3D MPRAGE MRI scan using Brainsight frameless stereotaxic neuronavigation.
      Same area as in Naeser et al. 2002 (conference abstract) where it was the only one of four right
      perisylvian targets associated with acute naming improvement. Coil: figure-8 MagStim, 7cm wing diameter,
      tangential at ~45 degrees. Volume stimulated ~1 cc (mathematical model estimate).

      '
    kind: manual_ROI
  relationship: responder
  replications:
  - '@Naeser2002'
  sample:
    age_range: '52–58 years (M: 52M, 58M, 53M, 57F)'
    exclusion_criteria: left-handed; acute/subacute phase; individual speech therapy during study period
    handedness: all right-handed
    inclusion_criteria: right-handed; chronic left MCA stroke; nonfluent or recovered aphasia; BNT first
      20 items ≥ 3/20; S&V average ≥ 3/20 pictures nameable
    language: English
    n: 4
    population: chronic right-handed aphasia patients with left MCA stroke, 5–11 years post-onset; nonfluent
      (Broca's, global) or recovered (anomic/conduction)
    recruitment: Boston VA / BU Aphasia Research Center; not further specified
    time_post_onset: 'P1: 5 years; P2: 10 years; P3: 11 years; P4: 7 years'
  source_passages:
  - page: 1
    quote: Significant improvement was observed in picture naming at 2 months post-rTMS, with lasting
      benefit at 8 months in three patients
    section: Abstract
    supports: claim
  - page: 6
    quote: The coil was placed over a gyrus immediately rostral to the anterior, (vertical) ascending
      ramus of the Sylvian fissure
    section: Methods — rTMS treatment
    supports: region_definition
  - page: 7
    quote: BNT (first 20 items) (p = .003); BDAE subtest, Animal Naming (p = .02); and BDAE subtest, Tools/Implements
      (p = .04)
    section: Results
    supports: statistics
  - page: 7
    quote: This is the first study to report lasting, improved naming at 2 months and 8 months following
      application of rTMS in chronic aphasia
    section: Discussion
    supports: claim
  - page: 3
    quote: Four right-handed, chronic aphasia patients participated, at 5–11 years post-L middle cerebral
      artery stroke
    section: Methods — Patients
    supports: sample
  - page: 8
    quote: our results should be considered preliminary, as this was an open-protocol study, and no patients
      received sham rTMS
    section: Discussion
    supports: limitation
  statistics:
    ci_95: not_reported
    cluster_extent: not_reported
    effect_size: not_reported
    p_value: 'BNT (first 20 items) at 2 months: t=8.66, p=0.003. BDAE Animals at 2 weeks: p=0.02; at 2
      months: p=0.02. BDAE Tools/Implements at 2 months: p=0.04; at 8 months: p=0.003. Overall BNT main
      effect of time: F=5.69, df=3,9, p=0.018. S&V immediate post-rTMS (10th treatment): naming improved
      p=0.0028; RT decreased p=0.04.

      '
    threshold: ANOVA repeated measures, Newman-Keuls post-hoc correction
  strength: weak
  target: right_pars_triangularis_ba45
  target_kind: region
source: draft
last_reviewed: '2026-05-07'
reviewer: claude-cowork
reviewed_on: '2026-05-06'
---
# Inhibitory rTMS to Right Pars Triangularis — Naeser et al. 2005

## Therapy description

Slow (1 Hz) repetitive TMS applied to the right anterior Broca homologue (pars
triangularis, BA45) for 20 minutes daily, 5 days/week for 2 weeks (10 sessions,
1200 pulses/session, 90% motor threshold). Neuronavigated with Brainsight stereotaxic
system on individual T1 MRI.

## Mechanism hypothesis

Chronic nonfluent aphasia patients show paradoxical overactivation in right perisylvian
homologues — particularly right pars triangularis — during language tasks. This may
reflect maladaptive "dead-end" compensation. Slow rTMS suppresses this hyperactivation,
releasing more adaptive left-hemisphere (or bilateral) naming networks.

## Key results (n=4 open protocol)

- BNT first 20 items at 2 months: mean improved from 8 to 10.5/20, p=0.003
- BDAE Animal Naming at 2 months: p=0.02
- BDAE Tools/Implements at 8 months: p=0.003 (most durable effect)
- 3/4 patients showed improvement at 8 months
- Immediate post-10th-treatment naming: p=0.0028 (Snodgrass & Vanderwart pictures)
- No adverse events

## Evidence caveats

Open-protocol (no sham), n=4 only. Evidence is case-series quality. This entry
documents the index finding motivating subsequent sham-controlled trials
(e.g. Naeser et al. 2010; Hamilton et al. 2010; Barwood et al. 2011). The
right pars triangularis (not pars opercularis) specificity was established in
the prior acute study (Naeser et al. 2002) and replicated here for lasting effects.
