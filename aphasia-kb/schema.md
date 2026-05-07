# Schema v2.4

Every entry is a single markdown file with **YAML frontmatter** followed by
**prose**. The frontmatter is the contract that `aphasia_kb.py`,
`promote.py`, `annotate_paper.py`, and any extraction agent rely on.
Changing field names or controlled vocabularies should be a deliberate,
documented change to *this file* and the loader together.

> **Status note.** Schema v1 → v2.0 → v2.1 → v2.2 → v2.3 → **v2.4** (current).
>
> - **v2.0** introduced the rich finding object (method/sample/stats/etc.).
> - **v2.1** made `source_passages` required and added `imaging_details`
>   for the color-annotated PDF workflow.
> - **v2.2** adds: `method` as a list (multimodal papers), an
>   `imaging_details.modalities` block (per-modality acquisition),
>   `imaging_details.task` (for fMRI), and a `finding.relationship`
>   field that disambiguates "damage causes Y" (causal) from "X is
>   recruited for Y" (correlational/recruitment) from "lesion pattern
>   predicts Y therapy benefit" (responder).
> - **v2.3** adds the `predictors/` bucket. Predictor entries describe
>   a measurable variable (behavioural test, demographic, clinical
>   characteristic, or imaging-derived metric) that has been shown to
>   predict an impairment, therapy response, or prognosis. Adds
>   `target_kind: predictor` so findings in any bucket can target a
>   predictor (e.g. "damage to Broca's area → low WAB-AQ").
> - **v2.4** adds the `reviews/` bucket and `method: narrative_review`
>   for qualitative synthesis entries. Review findings capture
>   consensus positions and theoretical claims from narrative reviews
>   and systematic reviews where no primary dataset is analysed.
>   These findings use `relationship: synthesis`, `evidence_quality:
>   narrative-review`, and omit `sample`, `statistics`, `confounders`,
>   and `region_definition`. A new optional field
>   `primary_papers_cited` lists the citation keys of primary studies
>   the review synthesizes. `source_passages` and `author_limitations`
>   remain required. Downstream tools should weight `narrative-review`
>   evidence distinctly from quantitative findings and may filter it
>   out by default.
>
> New entries must declare `schema_version: 2.4`. The loader reads older
> entries (v1, v2.0–v2.3) for backwards compatibility.

## File-level fields (every entry)

| Field            | Type    | Required | Notes |
|------------------|---------|----------|-------|
| `schema_version` | int     | yes      | Must be `2`. |
| `id`             | string  | yes      | Stable join key, lowercase, dash-or-underscore-separated. |
| `name`           | string  | yes      | Human-readable name. |
| `aliases`        | list    | no       | Other names that should resolve to this entry. |
| `kind`           | enum    | yes      | See per-bucket section below. |
| `status`         | enum    | yes      | `draft` \| `in_review` \| `approved` \| `rejected` \| `legacy_v1`. |
| `reviewer`       | string  | when status=`approved` | Free text identifying the human reviewer. |
| `reviewed_on`    | ISO date | when status=`approved` | When the reviewer signed off. |
| `created_by`     | string  | yes | E.g. `agent:claude-opus-4-7` or `human:michele`. |
| `created_on`     | ISO date | yes | When the entry was first written. |
| `findings`       | list of *finding* objects | yes (may be empty) | See below. |
| `notes`          | string  | no       | Free text, file-level. |

## `regions/` files

In addition to the file-level fields above:

| Field             | Type            | Required | Notes |
|-------------------|-----------------|----------|-------|
| `kind`            | enum            | yes      | `atlas` \| `classical` \| `network` \| `tract`. |
| `atlas`           | string          | when `kind=atlas` | Atlas name + version, e.g. `HarvardOxford-cort-maxprob-thr25-2mm`. |
| `atlas_index`     | int             | when `kind=atlas` | Index into the atlas labels list. |
| `mni_centroid`    | [x, y, z]       | no       | |
| `hemisphere`      | enum            | no       | `left` \| `right` \| `bilateral`. Default `left` for language regions. |
| `members`         | list of region ids | when `kind=network` or `tract` | Constituent regions / endpoints. |
| `networks`        | list of region ids | no | Networks this region participates in. |
| `tracts_adjacent` | list of region ids | no | Tracts that pass through / terminate near this region. |

## `impairments/` files

| Field              | Type            | Required | Notes |
|--------------------|-----------------|----------|-------|
| `kind`             | const `impairment` | yes   | |
| `short_definition` | string          | yes      | One-sentence clinical definition. |
| `assessment`       | list of strings | no       | Standard tests, e.g. `["BNT", "WAB-R Naming"]`. |

## `therapies/` files

| Field                  | Type            | Required | Notes |
|------------------------|-----------------|----------|-------|
| `kind`                 | const `therapy` | yes      | |
| `short_description`    | string          | yes      | |
| `targets_impairments`  | list of strings | yes      | impairment ids this therapy is designed to treat. |
| `dosage`               | string          | no       | Typical dose, e.g. `3 sessions/week × 8 weeks`. |

## `predictors/` files (introduced v2.3)

A *predictor* is any measurable variable that the literature has linked to
an outcome (impairment severity, therapy response, recovery trajectory).
Predictor entries let the KB answer queries like "given this patient's
WAB-AQ, age, lesion volume, and time post-onset, what does the literature
say about their prognosis and likely therapy responsiveness?" — i.e.
combine *imaging* findings (from `regions/`) with *behavioural and
clinical* findings (from `predictors/`).

| Field                  | Type            | Required | Notes |
|------------------------|-----------------|----------|-------|
| `kind`                 | const `predictor` | yes    | |
| `predictor_type`       | enum            | yes      | `behavioural` \| `demographic` \| `clinical` \| `imaging_metric`. See *Predictor types* below. |
| `short_definition`     | string          | yes      | One sentence describing what the variable measures. |
| `assessment`           | list of strings | when `predictor_type=behavioural` or `clinical` | Standard tests, e.g. `["WAB-R", "BNT", "WAB-R Aphasia Quotient"]`. |
| `units`                | string          | no       | E.g. `"score 0–100"`, `"ml"`, `"years"`, `"months"`, `"% of left hemisphere"`. |
| `typical_range`        | string          | no       | E.g. `"0–100 (lower = more severe)"`, `"5–250 ml"`, `"30–85 yrs"`. |
| `direction_of_severity`| enum            | no       | `higher_is_worse` \| `lower_is_worse` \| `nonmonotonic` \| `not_applicable`. Helps the interpreter know which way to read a value. |

### Predictor types

| `predictor_type`  | What it covers                                                      | Examples                                                    |
|-------------------|---------------------------------------------------------------------|-------------------------------------------------------------|
| `behavioural`     | Standardised language/cognition test scores measured on the patient | WAB-AQ, BNT, BDAE comprehension, PALPA, semantic fluency    |
| `demographic`     | Patient characteristics independent of the stroke                   | Age, education, handedness, premorbid bilingualism          |
| `clinical`        | Stroke-related characteristics measurable at bedside / from chart   | Time post-onset, NIHSS, stroke etiology, prior strokes      |
| `imaging_metric`  | Scalar imaging-derived measures (NOT regional findings — those go in `regions/`) | Total lesion volume, white-matter hyperintensity load, brain atrophy index, lesion-load on a specific tract |

Findings inside a predictor entry follow the same rules as findings in
`regions/` / `impairments/` / `therapies/`. Their `target` typically
points to an impairment, therapy, or prognosis (rarely to a region).

Findings in *other* buckets can also point to a predictor by setting
`target_kind: predictor`. Example: a region entry can carry the finding
"damage to left Heschl's gyrus → reduced WAB-AQ" with
`target: wab_aq, target_kind: predictor`.

---

## The `finding` object (the heart of v2)

Each finding is one piece of evidence linking the entry to one impairment,
therapy, or region. Required fields are marked **R**; strongly encouraged
ones are **S**; optional ones are **O**.

### Identity

| Field         | R/S/O | Type   | Notes |
|---------------|-------|--------|-------|
| `id`          | R     | string | Stable id within the file (e.g. `f1`, `f2`). Used by `replications` / `contradictions` to refer to specific findings. |
| `target`      | R     | string | The other-side `id` (an impairment id from this entry, or a region id from an impairment/therapy entry). |
| `target_kind` | R     | enum   | `impairment` \| `therapy` \| `region` \| `prognosis` \| `predictor`. |
| `claim`       | R     | string | One sentence stating the finding in plain language. The agent's own prose, not a quote. |
| `direction`   | R     | enum   | `likely` \| `unlikely` \| `likely_responder` \| `unlikely_responder` \| `no_effect` \| `mixed`. |
| `citation`    | R     | string | `@Key` referencing `citations.md`. |

### Method

| Field      | R/S/O | Type   | Notes |
|------------|-------|--------|-------|
| `method`   | R     | enum or list | **v2.2:** can be a string (single method) or a list of strings (multimodal paper). E.g. `LSM` or `[fMRI_activation, DTI]`. |
| `design`   | S     | enum   | `cross-sectional` \| `longitudinal` \| `RCT` \| `case-series` \| `single-case` \| `meta-analysis` \| `systematic-review` \| `narrative-review` (v2.4). |
| `imaging`  | S     | enum   | `T1` \| `T2` \| `FLAIR` \| `CT` \| `DWI` \| `fMRI` \| `multimodal` \| `none` \| `not_reported`. |
| `relationship` | R | enum | **v2.2:** what kind of relationship the finding describes. See *Relationship semantics* below. |

### Relationship semantics (v2.2)

The `relationship` field tells a downstream interpreter what kind of
claim a finding is making. `direction` (likely / unlikely / no_effect /
mixed) is the *valence*; `relationship` is the *type*. Both are needed
to know what e.g. `direction: likely` actually means.

| `relationship`   | Typical methods                        | "likely" means                                                                                          |
|------------------|----------------------------------------|---------------------------------------------------------------------------------------------------------|
| `causal`         | LSM, VLSM, VBCM, MLPA, lesion_network_mapping, disconnectome | "Damage to this region is associated with the impairment" — the canonical lesion-symptom claim. |
| `correlational`  | fMRI_FC, rs_fMRI, DTI, NODDI, EEG, MEG | "Activity / integrity of this region tracks behavior" — no causal claim, just covariation.              |
| `recruitment`    | fMRI_activation                        | "This region is recruited (active) during this task" — task-functional claim.                           |
| `responder`      | clinical_RCT, behavioral_only          | "Patients with this lesion / region pattern respond well to this therapy" — a moderator claim.          |
| `treatment_response` (added 2026-05-01) | fMRI_activation pre/post a treatment   | "This region's activation changes as a *consequence* of the treatment." Distinct from `causal` (damage→impairment) and `responder` (which patients respond). Use for treatment-induced upregulation / functional reorganization findings. |
| `synthesis` (added v2.4)    | narrative_review                       | "This is the consensus or majority position of the review literature." No primary measurement — a synthesized claim with `evidence_quality: narrative-review`. |

For `interpret_overlap()` (the per-patient lesion → literature interpretation),
all four `relationship` values with `direction: likely` get treated as
"damage to this region predicts the impairment" — which is the right
inference whether the underlying evidence is causal LSM, correlational
fMRI, recruitment, or therapy-responder data. The `relationship` field
preserves the *epistemic distinction* for the user and for any
downstream agent that needs to reason about evidence type.

### Sample

A nested object — fields inside `sample` may be `not_reported` if the paper
doesn't say.

| Field                       | R/S/O | Notes |
|-----------------------------|-------|-------|
| `sample.n`                  | R     | int. Use `not_reported` if absent. |
| `sample.population`         | R     | E.g. `chronic left-hemisphere stroke`. |
| `sample.time_post_onset`    | S     | E.g. `>=6 months`, `mean 38 months (SD 24)`. |
| `sample.age_range`          | S     | E.g. `35-78 years`, `mean 58 (SD 12)`. |
| `sample.handedness`         | S     | E.g. `all right-handed`, `mixed`. |
| `sample.language`           | S     | E.g. `English monolingual`, `Spanish-English bilingual`. |
| `sample.recruitment`        | O     | One sentence. |
| `sample.inclusion_criteria` | O     | List or one-sentence summary. |
| `sample.exclusion_criteria` | O     | List or one-sentence summary. |

### Statistics

| Field                  | R/S/O | Notes |
|------------------------|-------|-------|
| `statistics.threshold` | R     | E.g. `FWE p<.05`, `FDR q<.05`, `uncorrected p<.001 with k>10`. Use `not_reported` if absent. |
| `statistics.cluster_extent` | O | int (voxels). |
| `statistics.effect_size` | S   | E.g. `β = 0.34`, `OR 2.1`, `r = .42`. Use `not_reported` if absent. |
| `statistics.ci_95`     | O     | E.g. `[1.4, 3.1]`. |
| `statistics.p_value`   | O     | E.g. `.003`. |

### Confounders

| Field                          | R/S/O | Notes |
|--------------------------------|-------|-------|
| `confounders_controlled`       | R     | List of strings, e.g. `["lesion volume", "age", "time post-stroke"]`. Use `[]` (empty) only if the paper explicitly states none. |
| `confounders_not_controlled`   | R     | Things you (the extractor) noticed weren't controlled for. Use `[]` if the methods are exhaustive or you can't tell. |

### Region definition (how the *paper* defined the region)

| Field                          | R/S/O | Notes |
|--------------------------------|-------|-------|
| `region_definition.kind`       | R     | `atlas` \| `manual_ROI` \| `peak_coord_sphere` \| `tract` \| `data_driven_cluster` \| `not_reported`. |
| `region_definition.atlas`      | when `kind=atlas` | Atlas name + version. |
| `region_definition.mni_peak`   | when `kind=peak_coord_sphere` | `[x, y, z]` in mm, MNI. |
| `region_definition.radius_mm`  | when `kind=peak_coord_sphere` | int. |
| `region_definition.description`| S     | One sentence. |

### Imaging details (introduced v2.1; expanded v2.2)

A nested object capturing the imaging pipeline. Lets a downstream
interpreter check whether this finding's space/atlas is comparable to
the patient's imaging.

| Field                                  | R/S/O | Notes |
|----------------------------------------|-------|-------|
| `imaging_details.field_strength`       | S     | E.g. `"3T"`, `"1.5T"`, `not_reported`. |
| `imaging_details.acquisition.voxel_size_mm` | O | `[x, y, z]` in mm. *Single-modality shortcut* — for multimodal papers, prefer the `modalities` list below. |
| `imaging_details.acquisition.TR_ms`    | O     | int / float. |
| `imaging_details.acquisition.TE_ms`    | O     | int / float. |
| `imaging_details.acquisition.sequence` | O     | E.g. `"MPRAGE"`, `"FSE"`, `"EPI"`. |
| `imaging_details.modalities`           | O     | **v2.2:** list of per-modality acquisition blocks. Use this when the paper combines several modalities (e.g. T1 + fMRI + DTI). Each entry: `{modality: "T1"\|"fMRI"\|"DTI"\|...; voxel_size_mm: [], TR_ms, TE_ms, sequence, n_directions (DTI), b_values (DTI), volumes (fMRI), notes}`. Free-form per-modality. |
| `imaging_details.task`                 | when `method` includes `fMRI_activation` | **v2.2:** `{name: str, description: str, contrasts: [str], baseline: str}` — the fMRI paradigm. Skip for resting-state or non-fMRI findings. |
| `imaging_details.preprocessing_pipeline`| S    | One-line description, e.g. `"FreeSurfer 6.0 + FSL FLIRT/FNIRT"`, `"SPM12 unified segmentation + DARTEL"`, `"FSL FEAT + ANTs registration to MNI152"`. |
| `imaging_details.reference_space`      | R     | `MNI152` \| `MNI305` \| `Talairach` \| `native` \| `other` \| `not_reported`. |
| `imaging_details.atlases_used`         | R     | List of strings, e.g. `["HarvardOxford-cort-maxprob-thr25-2mm", "AAL"]`. Use `[]` if none. |
| `imaging_details.coordinates_reported` | O     | List of `{region: str, mni: [x, y, z]}` objects for explicitly reported peak coordinates. |

### Cross-study links

| Field            | R/S/O | Notes |
|------------------|-------|-------|
| `replications`   | O     | List of `@Key`s of papers that replicate this finding. |
| `contradictions` | O     | List of `@Key`s of papers that contradict this finding. |

### Author-acknowledged caveats

| Field                | R/S/O | Notes |
|----------------------|-------|-------|
| `author_limitations` | R     | List of one-line caveats the authors themselves note in their Discussion or Limitations section. Use `[]` only if the paper truly has none. |

### Extractor's assessment

These fields capture the *agent's* judgment, separate from what the paper
reports.

| Field                 | R/S/O | Notes |
|-----------------------|-------|-------|
| `evidence_quality`    | R     | `case-study` \| `cohort` \| `RCT` \| `meta-analysis` \| `tentative` \| `narrative-review` (v2.4). Reflects the *paper*. Use `narrative-review` for any `method: narrative_review` finding. |
| `strength`            | R     | `weak` \| `moderate` \| `strong`. The agent's read of how robustly this paper supports the claim. |

### Audit trail (provenance)

| Field                       | R/S/O | Notes |
|-----------------------------|-------|-------|
| `provenance.extracted_by`   | R     | E.g. `agent:claude-opus-4-7` or `human:michele`. |
| `provenance.extracted_on`   | R     | ISO date. |
| `provenance.paper_section`  | R     | E.g. `Results, page 1435`, `Table 2`, `Figure 4 caption`. |
| `provenance.confidence`     | R     | Agent's confidence in the *extraction itself* (not in the finding). `high` \| `medium` \| `low`. |
| `provenance.flags`          | R     | List of one-line concerns, e.g. `["effect direction unclear", "sample n inferred from figure"]`. Use `[]` if none. |

### Source passages (REQUIRED in v2.1)

The verbatim quotes that justify each finding. These drive the
color-annotated PDF that `annotate_paper.py` produces — without them
there's no visual audit, so they are required.

| Field                  | R/S/O | Notes |
|------------------------|-------|-------|
| `source_passages`      | R     | List of `{section, page, quote, supports}` objects. At least one entry. The exact sentence(s) in the paper, copied verbatim. |
| `source_passages[].section` | R | E.g. `"Results"`, `"Methods – Participants"`, `"Discussion – Limitations"`, `"Table 2 caption"`. |
| `source_passages[].page`    | R | int (or `null` if it's a table/figure caption with unclear page). |
| `source_passages[].quote`   | R | Verbatim text. Use `[…]` for elided clauses; never edit the substantive claim. Keep short — 1–3 sentences max per passage. |
| `source_passages[].supports`| R | One of: `claim` \| `method` \| `sample` \| `statistics` \| `confounders` \| `region_definition` \| `limitation` \| `imaging_details`. Drives which color highlights this passage in the annotated PDF. |

### Predictor-finding fields (introduced v2.3)

These optional fields apply to findings inside a `predictor` entry (or
findings in any other entry that target a predictor) where the same
construct is measured by multiple instruments. They let one umbrella
predictor entry (e.g. `severity_metric`) carry findings from
WAB-AQ-based, BDAE-based, CAT-based, etc. studies without
fragmenting the literature.

| Field             | R/S/O | Type   | Notes |
|-------------------|-------|--------|-------|
| `instrument`      | O     | string | The exact assessment used in this finding, e.g. `"WAB-AQ"`, `"BDAE severity rating"`, `"CAT"`, `"AAT"`. Pulled from the paper's Methods. |
| `score_band`      | O     | string | The range or threshold the finding applies to, written naturally. E.g. `"WAB-AQ 50–75 (moderate)"`, `"BDAE severity 2 (severe)"`, `"all severities"`. |
| `interpretation`  | O     | string | One plain-language sentence stating what falling in that band means clinically (e.g. `"Moderate aphasia, intermediate prognosis"`). |

The three fields are coupled: if you fill one, fill all three. The
loader does not require them, but `interpret_predictors()` uses them
when matching a patient's specific instrument + score to literature
findings.

### Free notes

| Field   | R/S/O | Notes |
|---------|-------|-------|
| `notes` | O     | Free text, finding-level. |

---

## Controlled vocabularies

> **Vocabulary extensibility (decided 2026-05-01).** The controlled
> vocabularies below are *extensible*. Adding a new value (e.g., a
> new method like `VBCM`) does **not** require a schema version
> bump — just add the value to the relevant set in `aphasia_kb.py`
> and document it here. **Structural** changes (new fields, new
> bucket types, changed required-ness) DO require a version bump.

```
schema_version    = 2 | 2.1 | 2.2 | 2.3 | 2.4 (current)
status            = draft | in_review | approved | rejected | legacy_v1
supports          = claim | method | sample | statistics | confounders
                  | region_definition | limitation | imaging_details
reference_space   = MNI152 | MNI305 | Talairach | native | other
                  | not_reported
relationship      = causal | correlational | recruitment | responder
                  | treatment_response | synthesis              # v2.4
direction         = likely | unlikely | likely_responder | unlikely_responder
                  | no_effect | mixed
strength          = weak | moderate | strong
evidence_quality  = case-study | cohort | RCT | meta-analysis | tentative
                  | narrative-review                            # v2.4
confidence        = high | medium | low
region.kind       = atlas | classical | network | tract
predictor_type    = behavioural | demographic | clinical | imaging_metric
direction_of_severity = higher_is_worse | lower_is_worse | nonmonotonic
                      | not_applicable
target_kind       = impairment | therapy | region | prognosis | predictor
method            = LSM | VLSM | VBCM | MLPA | MVPA
                  | fMRI_activation | fMRI_FC | rs_fMRI
                  | DTI | NODDI | tractography
                  | lesion_network_mapping | disconnectome
                  | EEG | MEG | TMS | tDCS
                  | behavioral_only | clinical_RCT | meta-analysis
                  | computational_model
                  | narrative_review                            # v2.4
design            = cross-sectional | longitudinal | RCT | case-series
                  | single-case | meta-analysis | systematic-review
                  | narrative-review                            # v2.4
imaging           = T1 | T2 | FLAIR | CT | DWI | fMRI | multimodal
                  | none | not_reported
region_definition.kind = atlas | manual_ROI | peak_coord_sphere | tract
                       | data_driven_cluster | not_reported
```

### Method-vocabulary notes

- **`narrative_review`** (v2.4): Use when the paper is a narrative review,
  systematic review (without formal meta-analytic pooling), or opinion
  article with substantive synthesized claims. Findings with this method
  use `relationship: synthesis`, `evidence_quality: narrative-review`, and
  **omit** `sample`, `statistics`, `confounders_controlled`,
  `confounders_not_controlled`, and `region_definition` (these are not
  applicable to review findings). `source_passages` (verbatim quotes) and
  `author_limitations` remain required. An optional top-level field
  `primary_papers_cited` (list of citation keys) documents the primary
  studies the review synthesizes.

  These findings are stored in `drafts/reviews/` and should be weighted
  lower than quantitative findings by downstream tools. Use `strength:
  weak` unless the review is explicitly based on a large evidence base
  with little contradictory evidence.

- **`VBCM`** (Voxel-Based Correlational Methodology, Tyler et al. 2005):
  a continuous-intensity variant of VLSM. Instead of binarised lesion
  masks, VBCM correlates per-voxel signal intensity (typically T1) with
  behavioural scores. Use `VBCM` rather than `VLSM` when the paper
  explicitly cites Tyler et al. 2005 or describes a continuous-intensity
  approach.

## Naming conventions for target IDs

### Hemisphere prefixing (decided 2026-05-01)

**Always prefix new region target IDs with `left_` or `right_`.**
Hemisphere is part of the identity of a region for KB purposes.
Examples: `left_angular_gyrus`, `right_temporal_pole`,
`left_posterior_arcuate_fasciculus`. Existing entries that pre-date
this convention (e.g., `ho-cort_44` with `hemisphere: left` as a
file-level field) are kept as legacy IDs for backward compatibility,
but new entries should use the prefixed form.

### Forward-looking target IDs (decided 2026-05-01)

**Draft findings may target IDs that don't yet exist as canonical
entries.** When `promote.py` first encounters a target ID that has
no corresponding file in `regions/`, `impairments/`, `therapies/`, or
`predictors/`, it creates a stub entry on first use rather than
rejecting the draft. Agents should pick descriptive snake_case IDs
(e.g., `left_heschls_gyrus`, `agrammatism`) and let the reviewer flesh
out the canonical file at promotion time.

### Cross-paper cohort overlap (decided 2026-05-01)

When a paper's cohort overlaps with another paper already in the KB
(or expected to be added), agents must add a flag to
`provenance.flags` of the form:

```
"cohort overlaps with @OtherPaperKey (e.g., same n=12 agrammatic
participants from NCT01927302); flag for downstream double-counting
risk in interpret_overlap()."
```

This lets `interpret_overlap()` (or a future deduplication step)
identify findings that derive from the same individuals and avoid
counting them as independent evidence.

### Behavioural-only findings inside an fMRI paper (decided 2026-05-01)

A paper that *primarily* uses imaging may also report a
behavioural-only treatment-efficacy finding (e.g., "treatment
significantly improved behavioural outcome X" without imaging in the
analysis). Code these findings as:

  - `method: clinical_RCT` (for treatment-efficacy claims with a
    randomized design and natural-history controls) or
    `method: behavioral_only` (for non-RCT behavioural-only claims)
  - `imaging: none` (NOT `not_reported` — the finding has no imaging
    component, even though the paper does)
  - `region_definition.kind: not_reported` with a short
    `description` noting "behavioural-only treatment-efficacy
    finding — no specific brain region"
  - `imaging_details.reference_space: not_reported` and
    `imaging_details.atlases_used: []` (the validator skips
    imaging-detail checks for `clinical_RCT` / `behavioral_only` /
    `meta-analysis` / `computational_model`)

Imaging-based findings from the same paper sit in separate `f2`,
`f3`, … entries with `method: fMRI_activation` (or VBCM, etc.) and
their full `imaging_details` block.

### Multi-paper region consolidation (decided 2026-05-01)

When `promote.py` first encounters a target ID (e.g.,
`left_heschls_gyrus`) that has findings from multiple draft files
across multiple papers, it should:

1. Create a single canonical region entry.
2. Append all findings (one per paper) to the entry's `findings:`
   list, preserving each finding's `citation` and `provenance`.
3. Renumber finding IDs to be unique within the file (`f1`, `f2`,
   `f3`, …) without colliding with any pre-existing IDs.
4. Carry forward each draft's hemisphere prefix into the canonical
   `id` (so `left_heschls_gyrus` stays `left_heschls_gyrus`, not
   `heschls_gyrus`).

If two drafts disagree on the same (region, target) pair, both
findings stay in the file and the disagreement is captured in
`replications` / `contradictions` of each finding.

## "Not reported" handling

Many real papers omit one or more required fields. The convention is:

- Use the literal string `not_reported` for any required string field that
  the paper does not report.
- Use the literal `null` (or omit the field) for `int`/`list` fields that
  are not reported, and add a flag in `provenance.flags`.
- An entry can still be `approved` with `not_reported` fields, but a
  reviewer should consider whether the missing fields undermine the claim.

## Citations

`citations.md` holds one block per `@Key` referenced in any frontmatter:

```markdown
## @Fridriksson2018
Fridriksson J, Yourganov G, Bonilha L, ... Revealing the dual streams of
speech processing. Proc Natl Acad Sci USA. 2018;115(7):1432–1437.
doi:10.1073/pnas.1714922115
```
