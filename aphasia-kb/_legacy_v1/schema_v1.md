# Schema

Every entry is a single markdown file with **YAML frontmatter** followed by
**prose**. The frontmatter is the contract: changing field names or value
vocabularies should be a deliberate, documented decision because
`aphasia_kb.py` and any future agent rely on them.

## Common fields (all entry types)

| Field           | Type             | Required | Notes |
|-----------------|------------------|----------|-------|
| `id`            | string           | yes      | Stable, lowercase, dash-or-underscore-separated. Used as the join key. |
| `name`          | string           | yes      | Human-readable name. |
| `aliases`       | list of strings  | no       | Other names this entry should match (case-insensitive). |
| `source`        | enum             | yes      | `curated` \| `neurosynth_auto` \| `agent_draft`. |
| `last_reviewed` | ISO date         | yes      | When a clinician last verified the entry. |
| `notes`         | string           | no       | Free text. |

## `regions/` files

| Field             | Type            | Required | Notes |
|-------------------|-----------------|----------|-------|
| `kind`            | enum            | yes      | `atlas` \| `classical` \| `network` \| `tract`. |
| `atlas`           | string          | when `kind=atlas` | e.g. `HarvardOxford-cort-maxprob-thr25-2mm`. |
| `atlas_index`     | int             | when `kind=atlas` | Index into the atlas labels list. |
| `mni_centroid`    | [x, y, z]       | no       | Optional; useful for `single`-source lookups. |
| `hemisphere`      | enum            | no       | `left` \| `right` \| `bilateral`. Default `left` for language regions. |
| `members`         | list of region ids | when `kind=network` or `kind=tract` | Constituent regions / endpoints. |
| `networks`        | list of region ids | no | Networks this region participates in. |
| `tracts_adjacent` | list of region ids | no | Tracts that pass through / terminate near this region. |
| `findings`        | list of *finding* objects | yes (may be empty) | See below. |

### `finding` object

A single piece of evidence linking this region to one impairment or therapy.

| Field              | Type             | Required | Notes |
|--------------------|------------------|----------|-------|
| `target`           | string           | yes      | An `id` from `impairments/` or `therapies/`. |
| `target_kind`      | enum             | yes      | `impairment` \| `therapy` \| `prognosis`. |
| `direction`        | enum             | yes      | `likely` \| `unlikely` \| `likely_responder` \| `unlikely_responder`. |
| `strength`         | enum             | yes      | `weak` \| `moderate` \| `strong`. |
| `evidence_quality` | enum             | yes      | `case-study` \| `cohort` \| `RCT` \| `meta-analysis` \| `tentative`. |
| `sample_n`         | int              | no       | Number of patients. |
| `citation`         | string           | yes      | `@Key` referencing `citations.md`. |
| `notes`            | string           | no       | One-liner about the finding. |

## `impairments/` files

| Field              | Type            | Required | Notes |
|--------------------|-----------------|----------|-------|
| `kind`             | const `impairment` | yes   | Always `impairment`. |
| `short_definition` | string          | yes      | One-sentence clinical definition. |
| `assessment`       | list of strings | no       | Standard tests, e.g. `["BNT", "WAB-R-Naming"]`. |
| `findings`         | list of *finding* objects | yes (may be empty) | Mirrors the region findings, but here `target` is a region id. |

## `therapies/` files

| Field            | Type            | Required | Notes |
|------------------|-----------------|----------|-------|
| `kind`           | const `therapy` | yes      | Always `therapy`. |
| `short_description` | string       | yes      | What the therapy is and what it targets. |
| `targets_impairments` | list of strings | yes | impairment ids this therapy is designed to treat. |
| `dosage`         | string          | no       | Typical dose (sessions/week × weeks). |
| `findings`       | list of *finding* objects | yes | `target` is a region id; `direction` is `likely_responder` / `unlikely_responder`. |

## Vocabularies (frozen for v1)

To keep the data joinable, please use exactly these strings in `direction`,
`strength`, `evidence_quality`, and `kind`. New values should be added by
editing this file *and* `aphasia_kb.py` together.

```
direction        = likely | unlikely | likely_responder | unlikely_responder
strength         = weak | moderate | strong
evidence_quality = case-study | cohort | RCT | meta-analysis | tentative
region.kind      = atlas | classical | network | tract
```

## Citations

`citations.md` holds one block per `@Key` referenced in any frontmatter, in a
free-form but consistent style:

```markdown
## @Fridriksson2018
Fridriksson J, Yourganov G, Bonilha L, Basilakos A, Den Ouden DB, Rorden C.
Revealing the dual streams of speech processing.
*Proc Natl Acad Sci USA*. 2018;115(22):E5188–E5196.
doi:10.1073/pnas.1720984115
```
