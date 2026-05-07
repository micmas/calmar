---
schema_version: 2.3
id: constraint_induced_aphasia_therapy
name: Constraint-Induced Aphasia Therapy (CIAT / CILT)
aliases:
- CIAT
- CILT
- constraint-induced language therapy
- constraint-induced aphasia treatment
kind: therapy
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-07
short_description: 'An intensive, massed-practice therapy in which compensatory strategies (gesture, drawing,
  writing) are prohibited and the patient is constrained to verbal communication during structured language
  games. The original Pulvermüller protocol uses 3–4 hours/day × 10 days. Supported by RCT evidence for
  broad aphasia improvement across fluent and non-fluent types.

  '
targets_impairments:
- anomic_aphasia
- brocas_aphasia
- fluency
- form_to_articulation
- form_to_meaning
- global_aphasia
dosage: 'Highly intensive: original Pulvermüller protocol is 3–4 hours/day × 10 consecutive weekdays.
  Modified CIAT-PACE uses smaller groups (2–3 patients) and structured card-exchange games. Some protocols
  extend to 3 weeks at lower daily intensity.

  '
atf_id: 4
atf_evidence_level: level_I
evidence_level: level_I
atf_aliases:
  - ILAT
  - CILT
  - Intensive Language Action Therapy
  - Constraint-Induced Language Therapy
icf_domain:
  - body_function
  - activity
tidier:
  brief_name: Constraint-Induced Aphasia Therapy (CIAT / CILT)
  # Source: ATF (aphasiatherapyfinder.com, therapy #4) + Pulvermüller 2001
  rationale: |-
    CIAT applies four key therapeutic principles established in the ATF evidence summary:
    (1) High intensity / massed practice — provide as much therapy as possible in as short
    a time as possible to facilitate learning;
    (2) Behaviourally relevant communication tasks — integrate verbal utterances into
    everyday communicative acts (requests, rejections, planning, clarification);
    (3) Strengths-based approach — target patients' preserved spoken language skills
    (e.g., repetition) and specific therapeutic goals rather than deficits globally;
    (4) Constraint to avoid learned non-use — verbal utterances are required for all
    communication; gesture as the sole means is discouraged via physical barriers;
    gesture is permitted only when accompanied by a verbal utterance. Positive
    reinforcement of verbal communication embedded in social interaction is central.
    Neuroplastic mechanism: massed verbal practice with constraint drives reorganisation
    of perilesional left-hemisphere language cortex (Pulvermüller 2001).
  materials: |-
    Picture-card sets beginning with high-frequency concrete nouns, progressing to
    medium-frequency nouns, low-frequency nouns, minimal pairs, verbs, adjectives,
    number words, colour words, prepositions, and specific semantic categories
    (animals, clothing, furniture, food, etc.). Generic commercially available
    picture cards are suitable; personalised cards are not required but items should
    be behaviourally relevant to the patient's daily life (food/drink, clothing,
    leisure activities). Barrier screen or divider to prevent non-verbal strategies.
    Pulvermüller 2001 protocol manual; session log sheets.
  procedures: |-
    Participants (SLP + 1–2 patients with aphasia) engage in structured verbal language
    games around a table with a barrier between participants. Each turn requires a
    verbal communicative act (request, accept, reject, clarify). Gesture as the sole
    means of communication is blocked by the barrier; verbal utterances are required.
    Gestures that accompany verbal attempts are allowed. Clinician shapes each verbal
    response from simpler to more complex forms using the least-to-most prompt hierarchy.
    Card complexity is systematically increased across sessions based on patient progress:
    high-frequency nouns → low-frequency nouns → minimal pairs → verbs/adjectives →
    abstract/functional vocabulary.
  who_provides: |-
    Speech-language pathologist. Delivery formats: individual (1:1), dyad (2 patients
    + SLP), or small group (up to 3 patients with aphasia + SLP).
  delivery_mode: |-
    face_to_face (primary); telehealth adaptations validated. Formats: one-to-one,
    dyad/pair, group (up to 3 people with aphasia).
  setting: |-
    Inpatient rehabilitation or outpatient clinic. Telehealth delivery is a documented
    modification.
  dosage: |-
    Most evidence from protocols delivering 2–4 hours/day × 2 consecutive weeks
    (approximately 30 hours total treatment). Pulvermüller 2001 original: 3–4 h/day
    × 10 weekdays. Modified protocols: 1–2 h/day × 3–4 weeks for lower-intensity
    settings. Schedule flexibility is documented but intensity is the key dosage variable.
  tailoring: |-
    Clinical guidance (ATF): Clinician should have a good sense of the patient's aphasia
    profile (type, severity, specific semantic and phonological deficits) and communication
    strengths before commencing. Ideally a brief standardised assessment informs starting
    level, though clinical judgement is acceptable. Stimulus difficulty is adjusted
    continuously: start with high-frequency nouns and increase complexity (frequency,
    part of speech, abstraction) based on the patient's progress within and across sessions.
    Stimuli should be drawn from behaviourally relevant daily-life categories.
    Group composition is matched for broadly similar communication level.
  modifications: |-
    CILT (Constraint-Induced Language Therapy) / ILAT (Intensive Language Action Therapy)
    are procedurally similar variants. CIAT-PACE combines CIAT structure with PACE
    communicative pragmatics. Dyadic (2-person) protocols validated for resource-limited
    settings. Telehealth delivery trialled and documented. Some protocols extend to 3 weeks
    at lower daily intensity. Modified CIAT omits group format for individual sessions.
  fidelity_planned: |-
    Protocol manual adherence monitored by supervising SLP. Session audio/video recording
    recommended for fidelity coding of: (a) constraint adherence (no gesture-only
    communication), (b) shaping hierarchy application, (c) positive reinforcement delivery.
    Stimulus progression log maintained per session.
  fidelity_actual: |-
    Pulvermüller 2001: fidelity not formally assessed (therapist-as-researcher design).
    Maher 2006: treatment logs maintained; independent fidelity coding NR.
    ATF does not report formal fidelity data from included trials.
  confidence: medium
  source: ATF therapy #4 (aphasiatherapyfinder.com) + Pulvermüller 2001 protocol
  flags:
    - ATF clinical principles and FAQ content integrated 2026-05-07 from
      aphasiatherapyfinder.com therapy #4 (CIAT/CILT).
    - Pulvermüller 2001 and Maher 2006 not formally extracted from papers/ —
      review when formally extracted.
rtss_ingredients:
  - verbal_constraint
  - communicative_shaping
  - massed_practice
findings:
- id: f1
  target: brocas_aphasia
  target_kind: impairment
  claim: 'CIAT produces significantly greater improvement than traditional therapy of equal total duration
    in patients with chronic aphasia, including non-fluent (Broca-type) patients, on the Aachen Aphasia
    Test (AAT) Token Test and picture naming.

    '
  direction: likely
  relationship: responder
  citation: '@Pulvermuller2001'
  method: clinical_RCT
  design: RCT
  imaging: none
  sample:
    n: 17
    population: chronic aphasia (mixed types, >6 months post-stroke)
    age_range: 42–69 years
  statistics:
    p_value: p<0.05 on Token Test and picture naming between groups
    effect_size: not reported (original paper)
    threshold: not_reported
  evidence_quality: RCT
  strength: strong
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    confidence: medium
    flags:
    - migrated from _legacy_v1/therapies/ciat.md; @Pulvermuller2001 not in papers/ — treat as lower-confidence
      pending formal extraction.
    paper_section: see entry notes (migrated/clinical-knowledge entry)
  confounders_controlled: &id001 []
  confounders_not_controlled: &id002 []
  region_definition: &id003
    kind: not_reported
    description: Behavioural outcome measure; no region definition applies.
  imaging_details: &id004
    reference_space: not_reported
    atlases_used: []
  replications: &id005 []
  contradictions: &id006 []
  author_limitations: &id007
  - see notes field in entry
  source_passages:
  - section: migrated entry
    page: 0
    supports: claim
    quote: (citation from clinical knowledge — not formally extracted)
- id: f2
  target: anomic_aphasia
  target_kind: impairment
  claim: 'CIAT/CILT shows generalisation effects to untrained words and everyday communication in anomic
    aphasia, with gains maintained at 6-month follow-up in some studies.

    '
  direction: likely
  relationship: responder
  citation: '@Maher2006'
  method: behavioral_only
  design: case-series
  imaging: none
  sample:
    n: 9
    population: chronic anomic/mild aphasia
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    confidence: low
    flags:
    - '@Maher2006 not in papers/ — citation from clinical knowledge, not formally extracted. Treat as
      placeholder.'
    paper_section: see entry notes (migrated/clinical-knowledge entry)
  statistics:
    threshold: not_reported
    cluster_extent: not_reported
    effect_size: not_reported
    ci_95: not_reported
    p_value: see claim
  confounders_controlled: *id001
  confounders_not_controlled: *id002
  region_definition: *id003
  imaging_details: *id004
  replications: *id005
  contradictions: *id006
  author_limitations: *id007
  source_passages:
  - section: migrated entry
    page: 0
    supports: claim
    quote: (citation from clinical knowledge — not formally extracted)
source:
- migrated_from: _legacy_v1/therapies/ciat.md
- basis: Pulvermüller 2001, Maher 2006 (not formally extracted)
last_reviewed: 2026-05-07
reviewer: agent:claude-sonnet-4-6
reviewed_on: 2026-05-07
notes: 'Less well-suited to: acute presentations; patients with severe global aphasia who cannot participate
  in verbal exchange; patients with limited stamina for intensive schedules. Evidence quality is moderate
  overall; the dose-response relationship and optimal scheduling remain active research questions. CILT
  and PACE are related variants with slightly different procedural details.

  '
---

# Constraint-Induced Aphasia Therapy (CIAT / CILT)

## What it is

Adapted from constraint-induced movement therapy (CIMT). The patient is
constrained to verbal communication as the *only* channel during structured
language games (e.g., card-request tasks requiring object naming and
sentence production). Compensatory strategies (gesture, drawing) are
prohibited. Key elements: massed practice, shaping, verbal constraint.

## Evidence base

- Pulvermüller 2001 (RCT): CIAT produced significantly greater gains than
  conventional therapy (equal total hours) on AAT subtests in chronic aphasia.
- Multiple subsequent studies confirm benefits across aphasia types, with
  effect sizes varying by lesion, severity, and time post-onset.

## Who benefits

Chronic aphasia with at least minimal verbal output; sufficient stamina and
cognitive capacity for intensive participation. Benefits reported across
Broca's, anomic, and mild/moderate aphasia; less evidence for severe global
aphasia.

## Limitations

Dropout due to intensity. Most trials are small. Maintenance of gains beyond
6 months is less well-characterised.
