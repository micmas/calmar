# Aphasia knowledge base (v2.3)

A clinician-controlled, agent-extensible knowledge base linking lesion
locations to aphasia-related impairments, therapy responses, and
behavioural / clinical predictors. The format is **markdown with rich
YAML frontmatter**, designed for both human review and machine
consumption.

> **The user is always in the loop.** No agent writes directly into the
> canonical `regions/`, `impairments/`, `therapies/`, `predictors/`, or
> `ingredients/` folders. Agents write to `drafts/`. A human reviewer
> promotes drafts to canonical entries via `promote.py`. This separation
> is the whole point of v2.

## Layout

```
aphasia-kb/
├── README.md                  # this file
├── schema.md                  # YAML frontmatter spec (v2.3 — read first)
├── HOWTO.md                   # end-to-end walkthrough: one PDF → approved entry
├── EXTRACTION_SKILL.md        # the agent's instruction manual
├── citations.md               # bibliography (@Key references)
├── extraction_log.md          # append-only audit log
│
│   # ---- code: loaders, CLIs, and the imaging bridge ----
├── aphasia_kb.py              # loader + validator + query module
├── promote.py                 # CLI: review / promote / reject drafts
├── extract.py                 # CLI: agent-driven paper extraction (Anthropic API)
├── auto_review.py             # CLI: agentic first-pass review of pending drafts
├── annotate_paper.py          # CLI: color-highlight a PDF from a draft's quotes
├── batch_ocr.py               # CLI: OCR image-only PDFs in papers/
├── decode_lesion.py           # lesion mask → HarvardOxford overlap + Neurosynth terms
├── aphasia_kb_rag.py          # imaging-driven RAG: lesion mask → cited report (+ LLM)
├── neurosynth_bootstrap.py    # (stage-2) scaffold to auto-draft from meta-analyses
│
│   # ---- canonical content (APPROVED; loaded by the KB) ----
├── regions/                   # approved region entries
├── impairments/               # approved impairment entries
├── therapies/                 # approved therapy entries
├── predictors/                # approved predictor entries (v2.3+)
├── ingredients/               # RTSS active-ingredient entries (referenced by therapies)
│
│   # ---- workflow & supporting material ----
├── drafts/                    # AGENT writes here; HUMAN reviews
│   ├── regions/
│   ├── impairments/
│   ├── therapies/
│   └── predictors/
├── reviews/                   # longer-form narrative reviews of review papers
├── examples/                  # worked-example entries (NOT loaded by KB)
├── auto_review_log/           # sidecar audit reports written by auto_review.py
├── papers/                    # source PDFs (tracked; *_annotated.pdf are agent output)
└── _neurosynth_cache/         # Neurosynth v7 data + term maps (NOT tracked; regenerated)
```

### What each script does

| Script                   | Role                                                                                      | Network |
|--------------------------|-------------------------------------------------------------------------------------------|---------|
| `aphasia_kb.py`          | Loads, validates, and queries the KB. `--issues`, `--lookup`, `--check <dir>`.            | local   |
| `promote.py`             | Human review gate: list / diff / show / approve / reject drafts.                          | local   |
| `extract.py`             | Drives an LLM to turn a PDF into draft entries + an annotated PDF.                         | API     |
| `auto_review.py`         | Deterministic safety checks (+ optional LLM second opinion) on pending drafts.            | local/API |
| `annotate_paper.py`      | Renders a color-coded PDF from a draft's `source_passages` for verification.              | local   |
| `batch_ocr.py`           | Detects and OCRs image-only PDFs in `papers/` (`ocrmypdf`).                               | local   |
| `decode_lesion.py`       | Correlates an MNI lesion mask with Neurosynth v7 term maps + HarvardOxford regions.        | local   |
| `aphasia_kb_rag.py`      | Joins `decode_lesion` output to KB findings → deterministic cited report (+ optional LLM). | local/API |
| `neurosynth_bootstrap.py`| Stage-2 scaffold that drafts region entries from Neurosynth meta-analyses.                 | local   |

The validator, deterministic auto-review, annotation, OCR, decoding, and
`promote.py` are all local Python and free. Steps marked **API** read an
`ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`) from the environment and bill
per call — see `HOWTO.md` for cost notes.

## The two workflows

### A. Agent extraction (the new capability)

1. You give an agent a paper (PDF, link, or pasted text) and point it at
   `EXTRACTION_SKILL.md`.
2. The agent reads the SKILL.md *and* the schema, then produces one or
   more `drafts/<bucket>/<entry_id>__<citation>.md` files.
3. The agent appends one `EXTRACTED` line to `extraction_log.md`.
4. You review with `python promote.py --list`, then `--diff` and
   `--show` each draft.
5. You approve with `python promote.py --approve <path> --reviewer "you"`
   or reject with `--reject <path> --reviewer "you" --reason "…"`.
6. `promote.py` validates the draft, stamps approval, merges/moves it
   into the canonical folder, and appends an `APPROVED` log line.

For the full operational walkthrough — including the Cowork-vs-CLI
choice, OCR, annotation, and auto-review — see `HOWTO.md`.

### B. Direct human curation (for entries you write yourself)

1. Read `schema.md` and the worked example in
   `examples/region_ifg_opercularis_fridriksson2018.md`.
2. Write a v2 entry in `drafts/<bucket>/`, set `status: draft` and
   `created_by: human:<your name>`.
3. Run `python aphasia_kb.py --check drafts/` to validate.
4. `python promote.py --approve <path> --reviewer "you"`.

## Quick reference

```bash
# Validate everything
python aphasia_kb.py --issues

# List pending drafts
python promote.py --list

# Diff a draft against the canonical entry it would change
python promote.py --diff drafts/regions/ho-cort_44__Fridriksson2018.md

# Approve a draft
python promote.py --approve drafts/regions/ho-cort_44__Fridriksson2018.md \
                  --reviewer "michele"

# Reject a draft
python promote.py --reject drafts/regions/ho-cort_44__Fridriksson2018.md \
                  --reviewer "michele" --reason "sample too small"

# Lookup a region by name / alias / id
python aphasia_kb.py --lookup "Broca's area"

# Decode a lesion mask and write a cited KB report
python aphasia_kb_rag.py /path/to/Lesion_in_MNI.nii.gz -o report.md
```

## How this connects to the CALMaR pipeline

The main `lesion-interpretation-pipeline.ipynb` calls into this KB at its
clinical-interpretation stage: it decodes each lesion mask
(`decode_lesion.py`), retrieves matching findings, and renders the
predicted impairments, outcome predictions, and therapy recommendations
(with RTSS ingredient badges) that appear in the per-subject report. The
KB can also be used standalone via the CLIs above.

## What changed from v1

| Concern                               | v1                       | v2                                            |
|---------------------------------------|--------------------------|-----------------------------------------------|
| Method (LSM/fMRI/DTI/etc.)            | not captured             | required                                      |
| Sample (n, demographics, criteria)    | only `sample_n`          | structured `sample.*` block                   |
| Statistical thresholding & effect size| not captured             | `statistics.threshold`, `effect_size`, etc.   |
| Confounders controlled / not          | not captured             | two required lists                            |
| How the *paper* defined the region    | not captured             | `region_definition.*` block                   |
| Author-acknowledged limitations       | not captured             | required list                                 |
| Replications / contradictions         | not captured             | optional cross-study links                    |
| Verbatim source quotes                | not captured             | optional `source_passages` (encouraged)       |
| Provenance (who extracted, when, how) | not captured             | required `provenance.*` block + flags         |
| Review workflow                       | none                     | `drafts/` + `status` + `promote.py`           |
| Schema validation                     | minimal                  | full v2 vocab + required-field check          |

v1 has been fully superseded by the v2.3 schema; all canonical entries in
this repo are v2. (Earlier v1 drafts were re-extracted from the original
papers under v2 rather than shipped as a legacy bucket.)

## Status

This is a **proof-of-concept** (~60 entries from ~40 papers). Every
approved entry needs clinician sign-off before being relied upon
clinically; both the deterministic and LLM report paths carry a
research-only, not-clinical-advice caveat. The schema is frozen for
v2.3; expanding it (new methods, new vocabularies, new buckets) is a
v2.4 change that must update `schema.md` and `aphasia_kb.py` together.

### Schema history

- **v2.0** — rich finding object (method, sample, statistics, confounders, region_definition).
- **v2.1** — required `source_passages` + `imaging_details` for the color-annotated PDF workflow.
- **v2.2** — `method` as list (multimodal), `imaging_details.modalities` + `task`, required `relationship` field on findings.
- **v2.3** — new `predictors/` bucket for behavioural / demographic / clinical / imaging-metric variables, plus `target_kind: predictor` so any finding can point at a predictor. Enables querying the KB with scan + behavioural-test data combined.
