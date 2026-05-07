---
schema_version: 2.4
id: lsm_language_systems_review__MirmanThye2018
name: LSM Core Language Systems Review — Mirman & Thye 2018
kind: network
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
primary_papers_cited:
- '@Mirman2015'
- '@Fridriksson2016'
- '@Fridriksson2018'
- '@Butler2014'
- '@Halai2017'
- '@Lacey2017'
notes: 'Concise synthesis (Current Directions in Psychological Science 2018) of four
  independent data-driven LSM research groups'' findings on the neuroanatomy of core
  language systems in post-stroke aphasia. Reviews convergent evidence for four cognitive
  language systems (phonology, semantics, fluency, executive functions) and their
  neural substrates. Key theoretical synthesis: dual-pathway phonological architecture,
  ATL semantic hub, frontal fluency system, and the non-emergence of lexicon or syntax
  as discrete systems in data-driven studies.

  '
findings:
- id: f1
  target: phonological_production
  target_kind: impairment
  claim: 'Phonological production deficits in post-stroke aphasia are consistently
    associated with dorsal-pathway damage involving inferior parietal and frontal
    regions; phonological recognition deficits are associated with a ventral pathway
    extending from posterior to anterior superior temporal lobe. This dual-stream
    phonological architecture converges across four independent data-driven LSM laboratories
    and broadly aligns with the Hickok & Poeppel dual-stream model.

    '
  direction: likely
  relationship: synthesis
  citation: '@MirmanThye2018'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  source_passages:
  - section: \'narrative synthesis\'
    quote: phonological-production subsystem
    page: 3
    supports: claim
  - section: \'narrative synthesis\'
    quote: recognition subsystem are associated with damage in a ventral pathway extending
    page: 3
    supports: claim
  - section: \'narrative synthesis\'
    quote: dual-stream architecture of the phonological system
    page: 3
    supports: claim
  author_limitations:
  - Convergence across groups is qualitative, not a quantitative meta-analysis; spatial
    overlap in neural maps not formally computed
  - Groups used different test batteries; composite phonological scores are not identical
    across studies
  - Four groups represent non-independent literature; some overlap in theoretical
    framework exists
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: '2026-05-06'
    paper_section: narrative synthesis
    confidence: high
    flags: []
- id: f2
  target: semantic_errors_in_naming
  target_kind: impairment
  claim: 'Post-stroke semantic deficits are reliably associated with anterior temporal
    lobe damage, including the temporal pole and mid-anterior portions of the middle
    and superior temporal gyri, representing the terminal ventral-stream hub for integrating
    distributed semantic knowledge. White-matter bottleneck damage (inferior fronto-occipital
    and uncinate fasciculi) also contributes by disrupting the distributed semantic
    network, with bottleneck lesions being particularly disruptive because a small
    amount of damage can affect multiple tracts simultaneously.

    '
  direction: likely
  relationship: synthesis
  citation: '@MirmanThye2018'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  source_passages:
  - section: \'narrative synthesis\'
    quote: Deficits in the semantic system are associated with anterior temporal lobe
      damage
    page: 3
    supports: claim
  - section: \'narrative synthesis\'
    quote: Poststroke semantic deficits are also associated with damage to white-matter
      pathways, particularly the inferior fronto-occipital fasciculus and the uncinate
      fasciculus
    page: 4
    supports: claim
  - section: \'narrative synthesis\'
    quote: Damage to white-matter bottlenecks—regions where multiple tracts come together—is
      particularly disruptive
    page: 4
    supports: claim
  author_limitations:
  - ATL lesions are underrepresented in stroke cohorts due to MCA territory sparing;
    ATL findings may be less robust
  - White-matter bottleneck findings rely on a specific disconnectome approach not
    uniformly adopted across reviewed groups
  - Some studies did not separate semantic recognition from semantic production, collapsing
    them into a single factor
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: '2026-05-06'
    paper_section: narrative synthesis
    confidence: high
    flags: []
- id: f3
  target: fluency
  target_kind: impairment
  claim: 'Speech fluency deficits (impaired rapid, smooth connected speech; reduced
    sentence complexity and syntactic structure) are associated with damage to the
    insula and inferior frontal and precentral areas, anterior to the region associated
    with single-word phonological production deficits, suggesting a hierarchical planning
    and execution system for sentence-level speech that is distinct from phonological
    production.

    '
  direction: likely
  relationship: synthesis
  citation: '@MirmanThye2018'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: weak
  source_passages:
  - section: \'narrative synthesis\'
    quote: Fluency deficits are associated with damage in the insula and inferior
      frontal and precentral areas
    page: 4
    supports: claim
  - section: \'narrative synthesis\'
    quote: anterior to the region associated with phonological production deficits
    page: 4
    supports: claim
  author_limitations:
  - Fluency system identified only in a subset of reviewed studies; not all four groups
    reported this factor
  - Insula/frontal fluency region overlaps with dysarthria and apraxia of speech substrates;
    these may not be fully dissociated
  - Sentence-comprehension deficits not strongly associated with this system, limiting
    interpretation as a general syntactic processor
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: '2026-05-06'
    paper_section: narrative synthesis
    confidence: high
    flags: []
- id: f4
  target: left_anterior_temporal_lobe
  target_kind: region
  claim: 'The lexicon and syntax have not emerged as discrete neural systems in data-driven
    LSM studies across four independent groups; the lexicon may be an emergent property
    of phonological-semantic interactions rather than a discrete system, and syntax
    deficits in aphasia may reflect general cognitive resource reduction rather than
    a dedicated syntactic module — a significant convergent null finding constraining
    models of language organisation.

    '
  direction: no_effect
  relationship: synthesis
  citation: '@MirmanThye2018'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: weak
  source_passages:
  - section: \'narrative synthesis\'
    quote: Two psycholinguistic constructs have not emerged in these data-driven lesion-symptom
      mapping studies
    page: 5
    supports: claim
  - section: \'narrative synthesis\'
    quote: the lexicon—a mental inventory of words. It may be that the lexicon is
      an emergent property
    page: 5
    supports: claim
  - section: \'narrative synthesis\'
    quote: syntax knowl
    page: 5
    supports: claim
  author_limitations:
  - Null finding for lexicon/syntax depends on specific composite measures; different
    battery choices might yield different factor solutions
  - Pragmatic aspects of language and real-world communication not assessed in any
    of the reviewed studies
  - Data-driven methods are limited by the tasks available; rare or specific syntactic
    deficits may not be captured
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: '2026-05-06'
    paper_section: narrative synthesis
    confidence: high
    flags: []
reviewer: michele
reviewed_on: '2026-05-07'
---
Mirman & Thye (2018) synthesise data-driven LSM findings from four independent research
groups (Philadelphia, USC/MUSC, Washington DC, Manchester) to characterise the neural
bases of four core language cognitive systems. The review confirms a dual-stream
phonological architecture (dorsal production / ventral recognition) consistent with
Hickok & Poeppel (2007) and an anterior temporal lobe semantic hub consistent with
hub-and-spoke models. A fluency system is associated with anterior frontal and insular
damage. The lexicon and syntax have not emerged as discrete neural systems in these
data-driven analyses, representing a theoretically significant null finding.
