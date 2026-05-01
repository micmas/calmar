# Paper-extraction skill — instructions for the agent

> **Purpose.** Take one neuroscience / aphasia paper and produce one or
> more **draft** knowledge-base entries under schema **v2.3**, plus a
> color-annotated version of the source paper that lets the user
> visually verify what was extracted from where. The user reviews
> every draft before it enters the canonical knowledge base. **You
> never write directly to `regions/`, `impairments/`, `therapies/`,
> or `predictors/`.**

This file is the agent's instruction manual. It must be read **in full**
before any extraction. The schema is defined in `schema.md` (v2.3 — read
that too). This file tells you how to *use* the schema responsibly.

## What v2.1 / v2.2 / v2.3 added (since v2.0)

From v2.1:

1. **Every finding's `source_passages` list is required and each entry
   carries a `supports` tag** (one of `claim` / `method` / `sample` /
   `statistics` / `confounders` / `region_definition` / `limitation` /
   `imaging_details`). The tags drive the colored highlights in the
   annotated PDF. No `source_passages`, no annotation, no extraction.
2. **Every imaging-based finding gets an `imaging_details` block** —
   reference space, atlases used, preprocessing pipeline, and any
   reported peak coordinates. Behavioral-only findings can omit it.

From v2.2:

3. **`method` can be a list** for multimodal papers
   (e.g. `[fMRI_activation, DTI]` instead of just one method).
4. **`imaging_details.modalities`** — per-modality acquisition blocks
   for multimodal papers (fMRI volume count, DTI b-values, etc.).
   Single-modality papers can stay with the flat `acquisition` block.
5. **`imaging_details.task`** — paradigm description for task-based
   fMRI findings.
6. **`relationship`** — required field on every finding. One of
   `causal` / `correlational` / `recruitment` / `responder`. Tells the
   reader what kind of claim the finding is making (see "Relationship
   semantics" below). `direction` is the *valence* (likely / unlikely);
   `relationship` is the *type* (causal vs correlational vs …).

From v2.3:

7. **`predictors/` bucket** — new entry kind for measurable variables
   (behavioural test scores, demographics, clinical characteristics,
   imaging-derived scalars) that the literature uses to predict
   outcomes. Each predictor entry declares a `predictor_type`:
   `behavioural` / `demographic` / `clinical` / `imaging_metric`.
   See "When to use predictor entries" below.
8. **`target_kind: predictor`** — findings in any bucket can now point
   to a predictor. Example: a region finding can claim "damage to
   left Heschl's gyrus → reduced WAB-AQ" with
   `target: wab_aq, target_kind: predictor`.

---

## 1. Workflow

For each paper the user gives you:

1. **Acknowledge what you have.** State whether you have the full PDF, an
   abstract only, a preprint, or a secondary description. If you only have
   the abstract, you may produce a draft but you **must** set
   `provenance.confidence: low` and add a flag.

2. **Identify the unit-of-extraction.** A single paper typically yields
   1–10 findings. Each finding is a single (region, impairment-or-therapy,
   direction) triple. If a paper reports 5 regions for naming and 3 for
   fluency, that's 8 findings — but they may live in 5 region files (since
   findings are stored on the *region side*).

   **Anchor perspective rule (avoid duplication).** When a paper makes
   region-tied claims (which is most of the literature), put each
   finding in a *region* draft with the appropriate `target` /
   `target_kind`. Don't mirror the same finding into a second draft on
   the impairment or therapy side — the loader's
   `interpret_overlap()` already pulls findings *across* all region
   entries when you query "what predicts impairment X?", so the
   impairment view is automatically derived.

   Spawn a separate impairment- or therapy-anchored draft only when
   the paper's claim isn't tied to a specific region. Examples:
     * "Naming errors split into semantic vs phonological subtypes
       regardless of lesion location" → impairment draft.
     * "MIT efficacy across mixed-lesion non-fluent aphasia (RCT,
       n=80)" → therapy draft.

   **Multi-bucket papers.** If one paper legitimately produces drafts
   in multiple buckets (e.g., a region anchor draft for the LSM
   finding *and* a therapy anchor draft for an embedded RCT analysis),
   that's fine — write one draft per bucket. The annotator handles
   multi-draft mode (`--draft a.md --draft b.md --pdf paper.pdf`) so
   you produce one annotated PDF per paper, not per draft.

3. **Refuse early when in doubt.** See "Refusal rules" below. A refused
   paper is a clean outcome; an over-confident extraction is not.

4. **Write each finding into the appropriate `drafts/` subfolder.** File
   naming convention:
   `drafts/regions/<region_id>__<citation_key>.md`
   for example: `drafts/regions/ho-cort_44__Fridriksson2018.md`.
   If a region file for that combination already exists in `regions/`, your
   draft *adds findings* by mirroring the existing file, appending your
   findings to the `findings:` list, bumping `status: draft`, and updating
   `created_by` / `created_on` to your run.

5. **Run `annotate_paper.py`** on the draft + the source PDF. This
   produces `papers/<basename>_annotated.pdf` with colored highlights
   showing exactly which sentences you extracted for each finding-aspect.
   Hand the user both the draft and the annotated PDF — the annotated
   PDF is the user's primary verification tool.

6. **Update `extraction_log.md`** with one line per paper processed:
   `2026-04-29 | @Fridriksson2018 | 4 drafts | confidence: medium | flags: 2 | agent: claude-opus-4-7`

7. **Stop and ask** if you encounter any of the conditions in "When to ask
   the user" below.

---

## 1b. When to use predictor entries (v2.3)

A *predictor* is any measurable variable (a number on a chart, a test
score, a demographic field, an imaging-derived scalar) that papers use
as an *input* to predict an outcome — distinct from a brain region
(`regions/`), a clinical syndrome (`impairments/`), or an intervention
(`therapies/`).

**Use a predictor draft (`drafts/predictors/`) when** the paper's claim
is "patients with high/low X tend to show outcome Y" and X is measured
the same way (or by a closely-related family of instruments) across
patients regardless of lesion location:

- `severity_metric` — overall aphasia severity, from any instrument
  (WAB-AQ, BDAE severity, CAT, AAT, ASRS). Tag the finding with the
  exact `instrument` used in that paper. Examples: "Patients with
  baseline WAB-AQ > 60 responded better to semantic feature analysis
  (n=42, β=0.41, p=.003)"; "Severe-baseline patients (BDAE 0–1)
  responded to MIT but moderate-baseline patients did not."
- `lesion_volume` — "After controlling for lesion location, total
  lesion volume independently predicted naming severity (R²=.18, p<.001)."
- `age` — "Younger patients (<55) showed greater post-therapy gains
  in fluency than older patients (n=68, p=.012)."
- `time_post_onset` — "Patients enrolled within 6 months post-stroke
  showed steeper recovery slopes than chronic patients."

**Use the `severity_metric` umbrella, not one entry per battery.**
Different studies use different instruments to measure the same
construct. Rather than fragmenting the literature into `wab_aq`,
`bdae_severity`, `cat_score`, etc. — which would also fragment a
clinician's prognostic query when the patient was tested with a
different battery — a single `severity_metric` entry holds findings
from any instrument and tags each finding with its `instrument`,
`score_band`, and `interpretation`. The interpreter
(`interpret_predictors()`) preferentially weights findings whose
instrument matches the patient's, but still surfaces cross-instrument
evidence.

**Don't create a predictor entry for** outcome variables that the paper
just *measures* (post-therapy WAB-AQ as the dependent variable of a
trial → that's a `direction: likely` finding on `target: severity_metric,
target_kind: predictor` from a *therapy* draft, not a finding *inside*
the predictor entry).

**Anchor perspective rule for predictors.**

- The paper's claim is "X predicts Y." Anchor on whichever side has the
  richer claim space:
  - If the paper's main finding is about *which lesion patterns make
    patients responsive* and they happen to also report baseline WAB-AQ
    as a covariate → the finding belongs in a *region* draft with
    `target_kind: predictor` (or `target_kind: therapy` if the actual
    target is the therapy). The predictor entry stays untouched.
  - If the paper's main finding is "WAB-AQ at baseline predicts
    responsiveness to therapy" with no lesion-location claim → write
    the finding *into the predictor entry* (`drafts/predictors/wab_aq__<key>.md`),
    targeting the therapy.

**File-naming convention for predictor drafts:**
`drafts/predictors/<predictor_id>__<citation_key>.md`
(e.g., `drafts/predictors/wab_aq__Schlaug2008.md`).

**Findings inside a predictor entry** follow exactly the same schema as
findings inside a region/impairment/therapy entry — same identity,
method, sample, statistics, confounders, source_passages, etc. The only
difference is the `target` typically points to a therapy, impairment,
or prognosis, not to another region.

**A predictor entry's findings should rarely have `relationship: causal`.**
Most behavioural/demographic predictors are `correlational` (the
predictor co-varies with outcome) or `responder` (the predictor
moderates therapy response). Only use `causal` if the paper makes a
genuine causal claim (rare, and almost always restricted to
`imaging_metric` predictors like lesion-load on a tract).

---

## 2. Refusal rules

Refuse to produce a draft (and explain why) when:

- The paper is an **editorial, commentary, or letter** without primary
  data.
- The paper is a **single-case report** *and* the finding is not novel
  enough to warrant a `case-study` entry. Default: extract single cases
  only when the user explicitly asks.
- You cannot identify the paper's **method**. If you can't choose a
  `method` value from the controlled vocabulary, you do not understand the
  paper well enough.
- The **direction of the claim is ambiguous** in the paper. Don't guess.
- The paper is a **review/meta-analysis without primary tables**. If it
  cites other papers' findings, extract from those papers instead.
- The paper makes claims about **non-human models** or **non-stroke
  etiologies** unless the user has scoped the request to those.

---

## 3. When to ask the user (don't proceed silently)

Ask before continuing if:

- The atlas the paper uses is **different from the LINDA pipeline's atlas**
  and you can't tell whether the regions are equivalent. Surface the
  mismatch; let the user decide whether to map across atlases.
- The paper reports a **direction opposite to existing approved entries**
  on the same (region, target) pair. This is a contradiction worth
  surfacing for review, not silently overwriting.
- The paper's `sample.population` does not match the KB's intended scope
  (e.g., the KB is for adult chronic stroke aphasia and the paper is on
  primary progressive aphasia or paediatric aphasia). Confirm before
  extracting.

---

## 4. Field-by-field extraction guidance

For each `finding` field listed in `schema.md`, here's how to fill it
honestly. Re-read this whenever you're unsure.

### `claim`
One sentence in your own words. Mirror the paper's *direction* (likely vs
unlikely) but use plain language. **Never paste a paper sentence here** —
that's what `source_passages` is for.

Bad: `"Cluster centered on left BA44 was significantly associated with the speech-fluency factor (p<.001 corrected)."`
Good: `"Damage to the left inferior frontal gyrus pars opercularis is associated with reduced speech fluency in chronic stroke."`

### `direction`
- `likely` / `unlikely`: positive / negative finding (use with any
  `relationship`).
- `likely_responder` / `unlikely_responder`: legacy v2.0/2.1 shortcut
  for therapy responsiveness. In v2.2 prefer `relationship: responder`
  + `direction: likely | unlikely`.
- `no_effect`: the paper specifically tested and found no association
  (a useful and under-recorded class of finding).
- `mixed`: the paper reports both supporting and contradicting evidence
  within the same study.

### `relationship` (v2.2, required)

| value           | use when…                                            |
|-----------------|------------------------------------------------------|
| `causal`        | LSM, VLSM, MLPA, lesion-network mapping, disconnectome — "damage to X is associated with Y." |
| `correlational` | fMRI_FC, rs_fMRI, DTI, NODDI, EEG, MEG — "activity / integrity of X tracks Y" without a causal claim. |
| `recruitment`   | task-based fMRI_activation — "X is recruited / active during the Y task." |
| `responder`     | clinical_RCT or behavioral_only — "patients with X lesion / region pattern respond to Y therapy." |

The combination `relationship` + `direction` tells the reader exactly
what the finding means. `causal + likely` = "damage causes Y";
`recruitment + likely` = "X lights up for Y task";
`correlational + unlikely` = "X activity does not correlate with Y."

`interpret_overlap()` (the per-patient lesion → literature aggregator)
treats all four `relationship` values with `direction: likely` as
"damage to this region predicts the impairment" — which is the right
inference whether the underlying evidence is causal or correlational.
The `relationship` field preserves the epistemic distinction for
human readers and downstream agents.

### `method`
**v2.2:** can be a single string OR a list of strings. Pick the closest
entry/entries from the vocabulary in `schema.md`. If you can't pick one,
refuse the extraction.

- Single-modality paper (most LSM, most fMRI, most DTI):
  `method: LSM` or `method: fMRI_activation`, etc.
- Multimodal paper (fMRI + DTI; T1 + lesion-network mapping; etc.):
  `method: [fMRI_activation, DTI]`. Order doesn't matter for the
  loader, but list the *primary* method used to derive the specific
  finding first.

Common ambiguities:
- "Univariate VLSM" → `VLSM`. "Multivariate / SVR-LSM" → `MLPA`.
- "Lesion network mapping" (using a normative connectome) → `lesion_network_mapping`.
- An fMRI paper that reports both activation and connectivity → list
  both: `[fMRI_activation, fMRI_FC]`, with the dominant one first.

### `sample`
Read the **Methods → Participants** section. If the paper splits its
sample into subgroups, extract the sample size of the subgroup the finding
applies to, not the overall study n.

If a sample field is genuinely not reported (common for `age_range`,
`handedness`), use the literal string `not_reported`. Do **not** guess.

### `statistics`
Read the relevant **Results** sentence and the corresponding figure / table.
- For LSM/VLSM: the threshold is usually permutation-based; report it
  exactly as the paper does (e.g., `"permutation p<.05 corrected; minimum cluster size 100 voxels"`).
- For RCTs: report the omnibus test threshold and the per-comparison
  effect size + CI when the finding is about a treatment effect.
- If only a *figure* shows the result with no numeric reporting in the
  text, set `statistics.threshold: not_reported` and add a flag.

### `confounders_controlled` / `confounders_not_controlled`
Read the **Methods** + **Results** sections. Common controls to look for:
lesion volume, age, sex, time post-stroke, education, baseline severity.
List what's controlled in the analysis that produced *this finding*.
Things that aren't controlled go in `_not_controlled`. If the paper truly
controls for nothing relevant, use `[]` for `_controlled` — don't fake it.

### `region_definition`
Critical for cross-study comparison. **How did the paper define the brain
region the finding is about?** Three common patterns:
1. **`atlas`**: paper used a named atlas → fill `atlas` and (ideally) the
   atlas index.
2. **`peak_coord_sphere`**: paper reports a peak voxel and built a
   spherical ROI → fill `mni_peak` and `radius_mm`.
3. **`data_driven_cluster`**: paper let the data define the cluster (LSM,
   ICA, etc.) → fill `description` with one sentence.

This field is what allows a downstream interpreter to know whether two
papers are talking about the *same* region.

### `replications` / `contradictions`
Only fill if the paper itself cites the prior work. Don't go fishing in
your training data. Use the same `@Key` style as `citation`. If the paper
references work that isn't yet in `citations.md`, add a flag and surface
it to the user — they can decide whether to add the reference.

### `author_limitations`
Read the **Discussion → Limitations** subsection (or the paper's Discussion
generally if there's no dedicated Limitations heading). Transcribe the
authors' own caveats in your words, one per list item. Do **not** invent
limitations — if the paper claims none, write `[]` and add a flag.

### `evidence_quality` (the *paper's* class)
- `meta-analysis`: a coordinate-based or effect-size meta-analysis.
- `RCT`: randomized controlled therapy trial.
- `cohort`: a typical group-level lesion-symptom or imaging study.
- `case-study`: a single subject or 2–3 subjects.
- `tentative`: preliminary, exploratory, or methodologically limited
  findings (e.g., uncorrected statistics, very small samples).

### `strength` (the *agent's* read)
- `strong`: large sample, robust correction, large effect, replicated
  elsewhere (per the paper itself), no fatal confounders.
- `moderate`: typical group study, plausibly correct but not airtight.
- `weak`: small sample, marginal correction, or a known limitation
  affects the interpretation.

`strength` is your call as the extractor. It's not the same as
`evidence_quality` (which classifies the *paper*). A weak finding can
appear in a high-quality paper.

### `provenance.confidence` (the agent's confidence in the *extraction*)
- `high`: you have the full paper, you understood the relevant section
  end-to-end, no ambiguities about what the finding is.
- `medium`: you have the paper but had to infer at least one field, or
  there's a borderline judgment somewhere.
- `low`: abstract only, or you noticed multiple ambiguities, or the
  reporting is poor enough that you're partly guessing.

If `confidence: low`, the user should expect to need to verify most of
the extraction.

### `provenance.flags`
Specific, one-line concerns. Write the kind of flag a reviewer needs to
act on. Bad flags are vague ("uncertain"); good flags name the field and
the issue.

Bad: `"unsure"`
Good: `"sample n inferred from Figure 1 caption — not stated in text"`
Good: `"effect direction is positive in Table 2 but negative in Figure 4 — verify"`

### `source_passages` (REQUIRED in v2.1)

A list of `{section, page, quote, supports}` objects. Each one is a
short verbatim quote (1–3 sentences) and the category of finding-aspect
it supports. The annotator uses these to produce the colored
highlighted PDF, so quotes must be **exact** — `Ctrl+F` should find
each one in the PDF. Use `[…]` to elide irrelevant clauses; never edit
the substantive claim.

Aim for one passage per `supports` category that the finding actually
makes a claim about. Typical complete set per finding:

  - `claim` (1×)  — the headline result sentence
  - `sample` (1×) — the cohort description
  - `method` (1×) — the analytical approach
  - `statistics` (1×) — the threshold / effect-size sentence
  - `imaging_details` (1×) — acquisition + preprocessing
  - `region_definition` (1×) — how the region was defined
  - `limitation` (1× or more) — the authors' own caveats
  - `confounders` (0–1×) — only if explicitly listed

If you only have the abstract (not the full paper), label
`section: "Abstract"` and lower `provenance.confidence` to `medium` or
`low`. The user will know the annotator can only highlight the
abstract in that case.

### `imaging_details` (new in v2.1; required for imaging-based findings)

Skip only when `method` is `behavioral_only` / `clinical_RCT` /
`meta-analysis` / `computational_model`. For everything else, fill:

  - `field_strength` — `"3T"`, `"1.5T"`, etc., or `not_reported`.
  - `acquisition.{voxel_size_mm, TR_ms, TE_ms, sequence}` — pull from
    the Methods *Imaging Acquisition* / *MRI Acquisition* section. Any
    sub-field can be omitted if not reported, but at least try for
    voxel size and sequence.
  - `preprocessing_pipeline` — one-line summary of the preprocessing
    stack (e.g. `"FreeSurfer 6.0 + FSL FLIRT/FNIRT to MNI152"`,
    `"SPM12 unified segmentation + DARTEL"`, `"ANTs N4 + diffeomorphic
    registration"`). The single most important field after
    `reference_space` for cross-study compatibility.
  - `reference_space` — `MNI152` / `MNI305` / `Talairach` / `native` /
    `other` / `not_reported`. Required (will fail validation otherwise
    for imaging-based findings).
  - `atlases_used` — list of strings, e.g. `["AAL", "HarvardOxford"]`.
    Required (use `[]` if the paper used no atlas, e.g. pure
    voxel-wise LSM with manual tracings).
  - `coordinates_reported` — list of `{region, mni: [x,y,z]}` for any
    peak coordinates explicitly given. The most useful imaging field
    for downstream interpretation, since you can spatially compare
    these to the patient's lesion location. Skip if the paper reports
    only cluster maps without peak coordinates.

**v2.2 — multimodal acquisition (`modalities`):**
For papers with more than one modality (e.g., T1 anatomy + task fMRI +
DTI), use the `modalities` list instead of (or in addition to) the
single `acquisition` block:

```yaml
imaging_details:
  modalities:
    - modality: T1
      sequence: MPRAGE
      voxel_size_mm: [1, 1, 1]
      TR_ms: 2300
      TE_ms: 2.96
    - modality: fMRI
      sequence: EPI
      voxel_size_mm: [3, 3, 3]
      TR_ms: 2000
      TE_ms: 30
      volumes: 240
    - modality: DTI
      voxel_size_mm: [2, 2, 2]
      n_directions: 64
      b_values: [0, 1000]
```

Each entry needs a `modality` key; the rest is free-form per modality.

**v2.2 — fMRI task (`task`):**
For findings whose `method` includes `fMRI_activation`, fill the
`imaging_details.task` block:

```yaml
imaging_details:
  task:
    name: "Picture naming"
    description: "Subjects named line drawings of common objects."
    contrasts: ["Naming > Rest", "Naming > Scrambled"]
    baseline: "Visual fixation"
```

Add a corresponding `source_passages` entry with
`supports: imaging_details` so the acquisition / task sentences get
highlighted in the annotated PDF.

---

## 5. Output format

For each paper:

1. Produce one **draft markdown file per (region, paper)** combination,
   placed in `drafts/regions/`. Same convention for impairment-targeted
   findings → `drafts/impairments/`, therapy-targeted → `drafts/therapies/`.
2. The frontmatter follows schema v2 exactly. Validate with
   `python aphasia_kb.py --check drafts/`.
3. Append one line to `extraction_log.md`.

### File-naming convention

`drafts/<bucket>/<entry_id>__<citation_key>.md`

- `bucket` ∈ `regions`, `impairments`, `therapies`, `predictors`.
- `entry_id` is the existing entry's `id` (e.g., `ho-cort_44`) or, for a
  new entry, the proposed `id` you assigned.
- `citation_key` is the paper's `@Key` minus the `@`.

Examples:
- `drafts/regions/ho-cort_44__Fridriksson2018.md`
- `drafts/impairments/naming__Mirman2015.md`
- `drafts/therapies/mit__Schlaug2008.md`
- `drafts/predictors/wab_aq__Schlaug2008.md`

### When the entry already exists

If `regions/ho-cort_44.md` already exists and you're adding new findings
for it from a new paper:

1. **Copy the approved file** into `drafts/` under the naming convention
   above.
2. **Bump `status: draft`** and update `created_by` / `created_on` to your
   run.
3. **Append** your new findings to the existing `findings:` list. Give
   them new `id`s (`f4`, `f5`, …) that don't collide with existing ones.
4. **Do not modify** existing findings. The reviewer decides whether to
   accept your additions.

---

## 6. Discipline rules (non-negotiable)

- **Never invent a citation.** If you reference a paper, it must already
  exist in `citations.md` *or* you must add a properly-formatted entry
  there in the same run.
- **Never invent statistics, effect sizes, or sample numbers.** If the
  paper doesn't report the field, use `not_reported`.
- **Never silently change `direction`** based on prior knowledge. The
  direction comes from *this paper*.
- **Never write outside `drafts/`, `papers/`, `extraction_log.md`, and
  `citations.md`.** No exceptions.
- **Always set `status: draft` and `created_by: agent:<your-id>`.**
- **Always update `extraction_log.md`** in the same run.

## 6b. Naming conventions (decided 2026-05-01)

These are the conventions for target IDs. They were settled after the
Yourganov / Alyahya / Barbieri extractions and are now binding for
new drafts. The full rationale is in `schema.md`; the operational
rules are below.

### Always prefix region target IDs with hemisphere

New region target IDs must include a `left_` or `right_` prefix.
Examples:
  - `left_angular_gyrus`, `right_anterior_middle_temporal_gyrus`
  - `left_posterior_arcuate_fasciculus`, `right_temporal_pole`
  - `left_heschls_gyrus`, `right_ifg_pars_triangularis`

Treat hemisphere as part of the region's identity, not a separate
attribute. Legacy IDs without the prefix (e.g., `ho-cort_44`,
`arcuate_fasciculus`) stay as-is for backward compat — but **do not**
create new unprefixed region IDs.

This rule applies to *region* target IDs only. Impairment IDs
(`agrammatism`, `phonological_production`, etc.), therapy IDs
(`treatment_of_underlying_forms`), and predictor IDs (`severity_metric`)
are not hemispheric and don't take a prefix.

### Forward-looking target IDs are accepted

You may target an ID that doesn't yet have a canonical file. Pick a
descriptive snake_case ID, mention in the file-level `notes` that the
target ID is forward-looking, and proceed. **Don't** add a per-finding
`provenance.flag` for every non-existent target ID — that just creates
noise. `promote.py` will create the stub canonical entry on first use.

### Use `VBCM` for VBCM analyses

If the paper cites Tyler et al. 2005 or describes a continuous-intensity
voxel-based correlation, use `method: VBCM` (not `VLSM`). VBCM was added
to the controlled vocabulary on 2026-05-01.

### Cross-paper cohort overlap → `provenance.flags`

When the cohort overlaps with another paper already in the KB (or
expected to be added later), add a flag of the form:

```
"cohort overlaps with @OtherPaperKey (same n=X subgroup, same trial
NCTxxxxx); flag for downstream double-counting risk in
interpret_overlap()."
```

Identifying overlap is your responsibility — check the paper's
"Participants" section for references to a parent cohort, registry
number, or a "subset of a larger study" clause. Common patterns:
shared NIH grant (e.g., P50DC012283), shared trial registration
(e.g., NCT01927302), and authors who appear together on multiple
papers in the same year.

### Treatment-induced reorganization → `relationship: treatment_response`

When a paper reports that a treatment causes activation changes in a
region (typically pre-vs-post fMRI), use
`relationship: treatment_response` (not `causal`). This is a v2.3+
addition that disambiguates "damage → impairment" claims (`causal`)
from "treatment → activation change" claims (`treatment_response`)
and from "patients with X respond to therapy Y" claims (`responder`).

### Behavioural-only findings inside an fMRI paper

Common case: a paper is primarily an fMRI study, but the
treatment-efficacy claim itself is behavioural-only. Code those
findings as:

  - `method: clinical_RCT` (or `behavioral_only` for non-RCT)
  - `imaging: none`
  - `region_definition.kind: not_reported` with a description noting
    "behavioural-only treatment-efficacy finding — no specific brain
    region"
  - `imaging_details.reference_space: not_reported` and
    `atlases_used: []` (the validator skips imaging-detail checks
    for these methods)

Then put the imaging-based findings from the same paper in separate
`f2`, `f3`, … entries with `method: fMRI_activation` (or VBCM, etc.)
and full `imaging_details`.

### Splitting findings when one paper's analyses disagree

When the same paper reports a positive finding under one analytic
choice (e.g., voxel-level FWE-corrected) and a null under another
(e.g., ROI-level with covariates), do **not** code as
`direction: mixed`. Instead, split into two separate findings:

  - One finding with the positive result (`direction: likely`) and
    its specific method / threshold.
  - A second finding with the null result (`direction: no_effect`)
    and its specific method / threshold.

Each finding carries its own statistics, region_definition, and
source_passages. The `direction: mixed` value is reserved for cases
where the *paper itself* reports both supporting and contradicting
evidence on the same analysis (e.g., subgroup-by-subgroup
disagreement), not for cross-analysis disagreement within one paper.

### Multi-paper region consolidation (for `promote.py`)

When `promote.py` first encounters a target ID that has findings
from multiple drafts across multiple papers (e.g., `left_heschls_gyrus`
from both Yourganov 2015 and Alyahya 2018), it consolidates by:

1. Creating one canonical region entry.
2. Appending all findings (one per paper) into the entry's `findings:`
   list, preserving citation + provenance.
3. Renumbering finding IDs to be unique within the file.
4. Carrying forward the hemisphere prefix in the canonical `id`.

If two drafts disagree, both findings stay; cross-link via
`replications` / `contradictions` rather than overwriting.

---

## 7. Worked example

See `examples/region_ifg_opercularis_fridriksson2018.md` for a fully
extracted v2 entry. Pay particular attention to:

- How `not_reported` is used for `sample.age_range` and several
  `statistics` fields.
- How `provenance.flags` records the specific things a reviewer needs to
  verify.
- How `confounders_not_controlled` makes the analysis gaps visible.
- How `source_passages` is filled (or not — the example currently has a
  placeholder, which the agent should replace when the PDF is available).

---

## 8. When the user asks you to extract from multiple papers at once

Process them one at a time and produce one draft set per paper. Do not
combine findings across papers into a single file — every finding has a
single `citation`, and conflating papers makes provenance impossible to
audit.

After all papers are processed, summarize for the user: papers processed,
drafts written, refusals and why, papers requiring user input before
proceeding.
