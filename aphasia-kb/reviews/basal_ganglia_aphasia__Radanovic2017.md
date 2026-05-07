---
schema_version: 2.4
id: basal_ganglia_aphasia__Radanovic2017
name: Basal Ganglia Aphasia — Radanovic & Mansur 2017 (Comprehensive Review)
kind: classical
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
primary_papers_cited:
- '@Alexander1987'
- '@NadeauCrosson1997'
- '@Hillis2002'
- '@Mega1994'
- '@Perani1987'
- '@Vallar1988'
notes: 'Comprehensive narrative/systematic review of language disturbances after vascular
  basal ganglia lesions (Brain and Language 2017). 57 eligible studies, 303 patients.
  Chi-square analyses on pooled patient-level data. Key positions: BG aphasias are
  heterogeneous with weak clinicoanatomical correlations; most persistent deficits
  are explained by cortical hypoperfusion; lesion-site associations have modest predictive
  value; prognosis is generally better than for cortical aphasia.

  '
findings:
- id: f1
  target: basal_ganglia_aphasia
  target_kind: impairment
  claim: 'Aphasias caused by basal ganglia vascular lesions are clinically heterogeneous;
    no consistent clinicoanatomical syndrome emerges, and weak or absent correlations
    between lesion site and aphasia type are the norm across 303 pooled patients from
    57 studies spanning 1966–2016.

    '
  direction: likely
  relationship: synthesis
  citation: '@Radanovic2017'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  source_passages:
  - section: \'narrative synthesis\'
    quote: aphasias caused by BG lesions are heterogeneous with weak clinicoanatomical
      correlations
    page: 1
    supports: claim
  - section: \'narrative synthesis\'
    quote: attempts to characterize subcortical aphasic syndromes in a similar way
      to classic cortical syndromes have proved unfruitful
    page: 2
    supports: claim
  author_limitations:
  - High heterogeneity in assessment batteries; chi-square applied to pooled but incompatible
    measures
  - Many studies enrolled patients with co-occurring cortical and periventricular
    white matter involvement, requiring exclusion
  - Frequency data often reported at study level rather than patient level, limiting
    individual-level analysis
  - No formal meta-analytic pooling; statistical power for subgroup associations is
    limited
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: '2026-05-06'
    paper_section: narrative synthesis
    confidence: high
    flags: []
- id: f2
  target: basal_ganglia_aphasia
  target_kind: impairment
  claim: 'In the acute stage, lentiform nucleus lesions are associated with elevated
    odds of repetition impairment (OR=5.78), comprehension deficit (OR=3.50), and
    non-fluent aphasia (OR=3.23); putaminal lesions predict paraphasia (OR=2.71);
    striatal lesions predict dysarthria (OR=3.67). Caudate (OR=0.28) and capsular
    (OR=0.05) lesions are inversely associated with non-fluent aphasia.

    '
  direction: likely
  relationship: synthesis
  citation: '@Radanovic2017'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: weak
  source_passages:
  - section: \'narrative synthesis\'
    quote: lentiform nucleus had a higher chance of the occurrence of repetition impairment
      (OR = 5.78)
    page: 5
    supports: claim
  - section: \'narrative synthesis\'
    quote: occurrence of paraphasia was more strongly associated with putaminal lesions
    page: 5
    supports: claim
  - section: \'narrative synthesis\'
    quote: was less encountered in patients with caudate lesions
    page: 5
    supports: claim
  author_limitations:
  - Odds ratios from chi-square on pooled heterogeneous case data; not regression-controlled
    for lesion size or cortical involvement
  - Lesion categories overlap in many patients; pure single-structure lesions are
    rare
  - Acute-stage ORs may reflect mass effect or hemodynamic factors rather than structural
    anatomy
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: '2026-05-06'
    paper_section: narrative synthesis
    confidence: high
    flags: []
- id: f3
  target: basal_ganglia_aphasia
  target_kind: impairment
  claim: 'Subcortical aphasia from basal ganglia lesions is predominantly mediated
    by cortical hypoperfusion in the MCA/ICA territory; SPECT/PET studies consistently
    show cortical hypometabolism corresponding to language symptom profiles, and in
    at least 50% of chronic cases evidence points to residual cortical hypoperfusion
    as the primary mechanism, with the remaining cases attributable to disconnection
    syndromes or direct white-matter pathway interruption.

    '
  direction: likely
  relationship: synthesis
  citation: '@Radanovic2017'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  source_passages:
  - section: \'narrative synthesis\'
    quote: comprehensive review of language disturbances after vascular lesions in
      the BG
    page: 1
    supports: claim
  - section: \'narrative synthesis\'
    quote: in at least 50% of cases, evidence suggests that more persistent disturbances
      were due to cortical hypoperfusion in the classic language areas
    page: 10
    supports: claim
  - section: \'narrative synthesis\'
    quote: any role of the dominant basal ganglia in language is obscured by associated
      cortical dysfunction, being either minimal or non-existent
    page: 9
    supports: claim
  author_limitations:
  - SPECT/PET studies available only for a subset of included patients
  - Cannot exclude a small direct BG contribution to language independent of cortical
    hypoperfusion
  - Residual vs acute hypoperfusion distinction not consistently documented in the
    reviewed studies
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: '2026-05-06'
    paper_section: narrative synthesis
    confidence: high
    flags: []
- id: f4
  target: basal_ganglia_aphasia
  target_kind: prognosis
  claim: 'Basal ganglia vascular aphasia generally carries a more benign prognosis
    than cortical aphasia; spontaneous improvement is commonly observed within the
    first months post-stroke, particularly for ischemic strokes with smaller lesion
    burden. In the chronic stage (≥6 months), 25.6% of cases in the review showed
    complete language normalisation.

    '
  direction: likely
  relationship: synthesis
  citation: '@Radanovic2017'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: weak
  source_passages:
  - section: \'narrative synthesis\'
    quote: subcortical lesions share some features, such as a more benign clinical
      picture and better long-term prognosis
    page: 2
    supports: claim
  author_limitations:
  - Follow-up data available for only a subset of the 303 patients
  - Variability in time post-onset of assessment across studies makes prognosis comparisons
    unreliable
  - Hemorrhagic strokes tend to have more severe acute presentations; mixed with ischemic
    cases in the pooled sample
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: '2026-05-06'
    paper_section: narrative synthesis
    confidence: high
    flags: []
reviewer: michele
reviewed_on: '2026-05-07'
---
Radanovic & Mansur (2017) conduct a comprehensive search of language disturbances after
vascular BG lesions (57 studies, 303 patients, 1966–2016). The review reaffirms that
clinicoanatomical correlations are weak, and that cortical hypoperfusion is the primary
mediator of persistent deficits. Modest lesion-site associations (lentiform for
repetition/comprehension, putamen for paraphasia) are reported but carry limited
predictive value due to the heterogeneity of lesion extent and associated cortical
involvement.
