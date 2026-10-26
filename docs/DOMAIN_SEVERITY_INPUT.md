# Domain-level impairment input

Status: proposed report/UI contract. No aphasia-KB schema change is made by
this work; any KB change requires maintainer approval.

## Purpose

CALMaR should be able to record a clinician- or researcher-supplied level of
impairment by functional domain without assuming that scores from different
tests or languages are numerically interchangeable. These values are
participant context, not diagnoses and not participant-level predictions.

The input is independent of WAB aphasia type and WAB-AQ. A supplied domain
level must never be inferred from a total score, syndrome label, lesion, or
another domain. Instrument-to-level mappings below are optional data-entry
guides; the person entering the data remains responsible for the level.

## Level scale

| Stored value | Display label | Meaning |
|---|---|---|
| `not_assessed` | Not assessed | No interpretable domain assessment is available. This is the default. |
| `none` | None observed | Performance was judged within the relevant reference or clinical expectation. |
| `mild` | Mild | Detectable impairment with relatively preserved functional performance. |
| `moderate` | Moderate | Clear impairment with substantial errors or support needs. |
| `severe` | Severe | Profound impairment or little usable performance in the assessed domain. |

“Not assessed” is not “none”. Missing values remain missing and are not
imputed. The initial UI deliberately avoids finer categories because published
instruments use incompatible ranges, norms, cut-offs, and language versions.

## Domain set

The first release uses domains that can be understood across instruments while
retaining the processing constructs already represented in
`aphasia-kb/impairments/`.

| Domain ID | Report label | Current KB relationship |
|---|---|---|
| `naming` | Naming / word finding | Related to `anomic_aphasia`, `phonological_production`, and `semantics`; not treated as an exact alias. |
| `comprehension` | Spoken comprehension | Related to `form_to_meaning`, `semantics`, `phonological_recognition`, and `syntactic_processing`. |
| `repetition` | Repetition | Related to `conduction_aphasia`, `phonological_production`, and `form_to_meaning`. |
| `fluency` | Speech fluency | Directly related to the existing `fluency` entry. |
| `reading` | Reading | Clinically important but no dedicated current impairment entry. |
| `writing` | Writing | Clinically important but no dedicated current impairment entry. |
| `speech_motor` | Speech motor / articulation | Related to `form_to_articulation`; language impairment and apraxia of speech must not be conflated. |
| `semantics` | Semantic processing | Directly related to `semantics` and `form_to_meaning`. |
| `syntax` | Syntactic processing | Directly related to `syntactic_processing`. |
| `executive_function` | Executive function | Directly related to `executive_functions`. |
| `attention` | Attention | No dedicated current impairment entry. |
| `memory` | Memory | No dedicated current impairment entry. |
| `praxis` | Praxis | No dedicated current impairment entry. |
| `visuospatial_attention` | Visuospatial attention | No dedicated current impairment entry. |

Syndrome entries (`brocas_aphasia`, `wernickes_aphasia`, `conduction_aphasia`,
`anomic_aphasia`, and `global_aphasia`) inform why these functional domains are
useful, but a syndrome label is not automatically decomposed into domain
levels. The UI therefore asks for the levels directly.

## Instrument-to-level entry guide

Mappings must use the validated cut-offs or normative rules for the exact test,
version, language, age, and education group where available. CALMaR should
store the entered level and may later store the source instrument and raw
score; it should not recalculate a level from an unrecognised score.

| Instrument or result | Suggested use |
|---|---|
| WAB-R AQ | Overall aphasia context only: 0–50 severe, >50–75 moderate, >75–93.7 mild, >93.7 none observed. This collapses CALMaR's existing 0–25 “very severe” and >25–50 “severe” `wab_band` labels into the domain scale and must not populate individual domains. |
| WAB-R subtests | Map the relevant subtest to naming, spoken comprehension, repetition, or fluency using the manual's cut-offs or the assessor's clinical interpretation; do not use AQ bands for subtests. |
| Boston Naming Test, Philadelphia Naming Test, Cambridge naming tests | Naming, using language- and demographic-appropriate norms or an explicit clinical judgement. |
| Token Test, WAB auditory verbal comprehension, CAT spoken sentence comprehension, NAVS sentence comprehension | Spoken comprehension; record semantic or syntactic domains separately only when the assessment supports that distinction. |
| PALPA immediate/delayed word or non-word repetition | Repetition and, when explicitly interpreted that way, phonological production. |
| Connected-speech measures (words/minute, mean length of utterance, tokens) | Speech fluency; use reference data appropriate to task and language. |
| Camel and Cactus, synonym judgement, word-to-picture matching | Semantic processing. |
| ABA-2 or Apraxia of Speech Rating Scale | Speech motor/articulation, not general fluency. |
| Oxford Cognitive Screen | Enter the corresponding attention, executive, memory, praxis, language, or visuospatial-attention domain from the validated OCS impairment classification; do not compare raw subtest scores across language versions. |
| Custom or translated tasks | Use the assessor's explicit domain interpretation and preserve “not assessed” when validity or reference standards are unclear. |

## Current storage and future KB decision

The UI stores a per-report dictionary in the notebook namespace as
`INTERP_DOMAIN_LEVELS`, keyed by the domain IDs above. The report prints all
domains and clearly distinguishes “not assessed” from “none observed”. It does
not feed these levels into therapy matching or KB evidence retrieval.

If the maintainer approves a KB extension later, the design should decide
whether these are participant observations outside the KB schema or whether
new impairment entries/aliases are needed for `naming`, `comprehension`,
`repetition`, `reading`, `writing`, `attention`, `memory`, `praxis`, and
`visuospatial_attention`. Exact mappings from broad clinical domains to current
processing constructs must remain many-to-many rather than aliases.
