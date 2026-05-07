---
schema_version: 2.3
id: melodic_intonation_therapy
name: Melodic Intonation Therapy (MIT)
aliases:
- MIT
- melodic intoning therapy
kind: therapy
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-07
short_description: 'A therapy that uses melodic intoning (singing on two pitches) and rhythmic left-hand
  tapping to elicit propositional speech in patients with non-fluent aphasia and apraxia of speech. Hypothesized
  to engage right-hemisphere language homologues via the intact right arcuate fasciculus.

  '
targets_impairments:
- apraxia_of_speech
- brocas_aphasia
- form_to_articulation
- fluency
- global_aphasia
dosage: 'Typically 3–5 sessions/week over several weeks; intensive protocols use 75–90 min daily sessions.
  The original Norton et al. protocol uses ~75 sessions delivered over 15 weeks.

  '
atf_id: 23
atf_evidence_level: level_I
evidence_level: level_I
atf_aliases:
  - Speech-Music Therapy for Aphasia
  - SMTA
  - Modified Melodic Intonation Therapy
  - Tone-Rhythmic Therapy
icf_domain:
  - body_function
  - activity
tidier:
  brief_name: Melodic Intonation Therapy (MIT)
  rationale: |-
    MIT exploits the relative sparing of right-hemisphere prosodic/musical processing in
        non-fluent aphasia. Melodic intoning and left-hand tapping activate right-
        hemisphere language homologues (right pars triangularis, right STG), providing an
        alternative output route that gradually transfers to conventional speech.
  materials: |-
    MIT phrase scripts graded across 4 levels (Level I: humming; Level II: unison singing
        with hand-tap; Level III: SLP voice fading; Level IV: speaking with rhythm); Helm-
        Estabrooks 1996 manual; metronome or hand-tapping board.
  procedures: |-
    SLP and patient sing target phrases using an exaggerated two-pitch melody in unison.
        Patient taps left hand on each syllable throughout. SLP voice progressively fades
        (Level III). At Level IV patient produces phrase with speech rhythm only (no
        melody). Level advancement criterion: >80% correct on that level's items across
        two sessions.
  who_provides: Speech-language pathologist (individual sessions).
  delivery_mode: face_to_face
  setting: Inpatient rehabilitation, acute ward, or outpatient clinic.
  dosage: |-
    van der Meulen 2016 (RCT): 30 min/day × 3 weeks = 15 sessions (~7.5 total hours).
        Albert 1973 original: 15 min twice daily. Some protocols extend to 6–8 weeks for
        patients who plateau at intermediate levels.
  tailoring: |-
    Level progression is individually paced using 80% criterion. Phrase length and
        syntactic complexity increased across levels. Target phrases selected from
        patient's functional communication needs.
  modifications: |-
    Speech-Music Therapy for Aphasia (SMTA) uses live instrument accompaniment (van der
        Meulen 2010). Modified MIT (mMIT) omits left-hand tapping — used when motor
        impairment prevents tapping. Tone-Rhythmic Therapy is an Asian-language
        adaptation.
  fidelity_planned: |-
    Level advancement criteria operationalised and documented per session. van der Meulen
        2016: independent rater coded 20% of sessions for protocol adherence.
  fidelity_actual: |-
    van der Meulen 2016: adherence to protocol reported as high; break-blind rate NR.
        Albert 1973: informal clinician report only.
  confidence: medium
  flags:
    - van der Meulen 2016 RCT not formally extracted from papers/. TIDieR populated from
        published protocol descriptions. Review when papers are formally extracted.
rtss_ingredients:
  - melodic_intoning
  - rhythmic_hand_tapping
  - communicative_shaping
  - massed_practice
findings:
- id: f1
  target: left_precentral_gyrus
  target_kind: region
  claim: 'Patients with non-fluent aphasia who respond best to MIT tend to have lesions involving the
    left precentral gyrus / premotor cortex (motor speech), sparing the right arcuate fasciculus. The
    intact right-hemisphere arcuate is a positive prognostic indicator for MIT response.

    '
  direction: likely
  relationship: treatment_response
  citation: '@Schlaug2008'
  method: DTI
  design: case-series
  imaging: MRI
  sample:
    n: 8
    population: chronic non-fluent aphasia after left-hemisphere stroke
    time_post_onset: '>6 months'
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    confidence: medium
    flags:
    - migrated from _legacy_v1/therapies/mit.md; @Schlaug2008 not formally extracted into papers/ — treat
      as lower-confidence
    paper_section: see entry notes (migrated/clinical-knowledge entry)
  statistics: &id001
    threshold: not_reported
    cluster_extent: not_reported
    effect_size: not_reported
    ci_95: not_reported
    p_value: see claim
  confounders_controlled: &id002 []
  confounders_not_controlled: &id003 []
  region_definition: &id004
    kind: not_reported
    description: Behavioural outcome measure; no region definition applies.
  imaging_details: &id005
    reference_space: not_reported
    atlases_used: []
  replications: &id006 []
  contradictions: &id007 []
  author_limitations: &id008
  - see notes field in entry
  source_passages:
  - section: migrated entry
    page: 0
    supports: claim
    quote: (citation from clinical knowledge — not formally extracted)
- id: f2
  target: brocas_aphasia
  target_kind: impairment
  claim: 'MIT is designed for non-fluent Broca-type aphasia with relatively preserved comprehension and
    severe production impairment. RCT evidence (van der Meulen 2012, Stahl 2013) shows significant gains
    on verbal output measures in chronic Broca''s aphasia compared to control conditions.

    '
  direction: likely
  relationship: responder
  citation: '@vanderMeulen2012'
  method: clinical_RCT
  design: RCT
  imaging: none
  sample:
    n: 17
    population: chronic non-fluent aphasia (Broca/global), >6 months post-stroke
  evidence_quality: RCT
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    confidence: medium
    flags:
    - '@vanderMeulen2012 not in papers/ — citation is from clinical knowledge, not formally extracted.
      Flag for formal review.'
    paper_section: see entry notes (migrated/clinical-knowledge entry)
  statistics: *id001
  confounders_controlled: *id002
  confounders_not_controlled: *id003
  region_definition: *id004
  imaging_details: *id005
  replications: *id006
  contradictions: *id007
  author_limitations: *id008
  source_passages:
  - section: migrated entry
    page: 0
    supports: claim
    quote: (citation from clinical knowledge — not formally extracted)
- id: f3
  target: apraxia_of_speech
  target_kind: impairment
  claim: 'MIT''s rhythmic-melodic scaffolding reduces apraxic errors in patients with acquired apraxia
    of speech (AOS) by slowing speech rate and providing temporal-rhythmic cueing for articulatory planning.

    '
  direction: likely
  relationship: responder
  citation: '@Stahl2013'
  method: clinical_RCT
  design: RCT
  imaging: none
  sample:
    n: 11
    population: chronic acquired AOS and aphasia
  evidence_quality: RCT
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    confidence: medium
    flags:
    - '@Stahl2013 not in papers/ — citation from clinical knowledge, not formally extracted. Flag for
      formal review.'
    paper_section: see entry notes (migrated/clinical-knowledge entry)
  statistics: *id001
  confounders_controlled: *id002
  confounders_not_controlled: *id003
  region_definition: *id004
  imaging_details: *id005
  replications: *id006
  contradictions: *id007
  author_limitations: *id008
  source_passages:
  - section: migrated entry
    page: 0
    supports: claim
    quote: (citation from clinical knowledge — not formally extracted)
source:
- migrated_from: _legacy_v1/therapies/mit.md
- basis: Schlaug 2008, van der Meulen 2012, Stahl 2013 (not formally extracted)
last_reviewed: 2026-05-07
reviewer: agent:claude-sonnet-4-6
reviewed_on: 2026-05-07
notes: 'NOT the best choice for: posterior/Wernicke''s aphasia with fluent paraphasic output; patients
  who cannot sustain attention for prolonged sessions; patients with significant hearing impairment. Evidence
  quality is limited by small sample sizes in RCTs; larger multicenter trials are ongoing.

  '
---

# Melodic Intonation Therapy (MIT)

## What it is

Patients are taught to intone short utterances (sung on two pitches, a minor
third apart) while tapping the left hand rhythmically on each syllable.
Therapy progresses through four stages of decreasing clinician support, with
the ultimate goal of carry-over to unintoned propositional speech.

## Evidence base

- Schlaug 2008: DTI/neuroimaging evidence that intensive MIT is associated
  with increased right-hemisphere arcuate fasciculus volume in non-fluent
  aphasia patients; also demonstrated behavioral improvement.
- van der Meulen 2012 (RCT): MIT produced significant gains in verbal output
  in Broca's aphasia compared to a control condition.
- Stahl 2013 (RCT): Benefits in AOS, particularly for articulatory accuracy
  and fluency measures.

## Who benefits

The canonical MIT population: chronic (>6 months), non-fluent aphasia with
anterior-dominant lesion, relatively preserved auditory comprehension,
motivated/cooperative patient. The intact right arcuate is a positive
prognostic indicator.

## Limitations

Small sample sizes in most trials. Benefit for severe global aphasia is
less well-established. Generalisation beyond trained utterances varies.
