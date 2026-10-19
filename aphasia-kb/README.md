# Aphasia knowledge base

A curated, source-traceable literature base linking stroke lesion
locations to aphasia impairments, therapy responses and recovery
predictors. CALMaR uses it to turn a lesion mask into a cited
interpretation. Entries are markdown files with YAML frontmatter,
readable by people and loaded by code.

Every finding is one claim from one paper and carries the verbatim
passages that support it, so anyone can open the paper and check.
Nothing enters the canonical folders without a second reading of that
paper — by a person, or for routine findings by an independent local
model — and a named person is accountable for all of it. That policy is
[`GOVERNANCE.md`](GOVERNANCE.md). Every model step runs on this machine
via Ollama; paper text and patient data never leave it
([`MODELS.md`](MODELS.md)).

**State (October 2026):** 72 entries, 244 findings, 43 papers. 26
entries were approved by a named person; 33 were approved before the
governance policy and are tagged `review_tier: legacy` pending
re-review. `python kb_status.py` prints the current numbers.

## Start here

| You want to… | Read / run |
|---|---|
| understand the entry format | [`schema.md`](schema.md) (v2.5), then `examples/region_ifg_opercularis_fridriksson2018.md` |
| take one PDF to an approved entry | [`HOWTO.md`](HOWTO.md) |
| know who may approve what | [`GOVERNANCE.md`](GOVERNANCE.md) |
| choose or benchmark a local model | [`MODELS.md`](MODELS.md) and `models.yaml` |
| see what is in the KB and what is thin | `python kb_status.py` |
| check the canonical quotes against the PDFs | `python audit_quotes.py` |
| set up the machine | `pip install -r ../requirements.txt`, `ollama pull gemma4:26b`, `python model_config.py` |

## How a paper becomes an entry

```
papers/<Key>.pdf
   │  extract.py — local model reads the text layer, writes schema-bound drafts
   ▼
drafts/<bucket>/<id>__<Key>.md          + papers/<Key>_annotated.pdf (annotate_paper.py)
   │  auto_review.py — deterministic checks (reject / defer only), tier classification,
   │                   then an INDEPENDENT model re-reads the PDF and answers seven
   │                   per-finding checks; may approve Tier A only
   ▼
promote.py — a person approves Tier B (therapies, strong claims, new entries, reviews);
             stamps reviewer, tier and a per-finding review block
   ▼
regions/ impairments/ therapies/ predictors/ reviews/ ingredients/      ← what CALMaR queries
   │
extraction_log.md — append-only: EXTRACTED · REJECTED · MODEL-APPROVED · APPROVED · AUDIT
```

Minimal session, from the repository root with the venv active:

```bash
cp ~/Downloads/Foo2024.pdf aphasia-kb/papers/Foo2024.pdf       # name = citation key
python aphasia-kb/extract.py --pdf aphasia-kb/papers/Foo2024.pdf
python aphasia-kb/aphasia_kb.py --check aphasia-kb/drafts/
python aphasia-kb/auto_review.py --all --llm-review --require-pdf-match
python aphasia-kb/promote.py --list                               # what still needs you
python aphasia-kb/promote.py --approve aphasia-kb/drafts/<...>.md --reviewer michele
git add aphasia-kb && git commit -m "Foo2024 extraction"
```

## Layout

```
aphasia-kb/
├── README.md                  # this file
├── schema.md                  # YAML frontmatter spec (v2.5) — the data contract
├── HOWTO.md                   # procedure: one PDF → approved entry
├── GOVERNANCE.md              # policy: review tiers, model approval, audit, legacy
├── MODELS.md                  # choosing and benchmarking the local models; decision log
├── EXTRACTION_SKILL.md        # the extractor's instruction manual
├── models.yaml                # which Ollama model each role uses (extract / review / rag)
├── citations.md               # bibliography (@Key, DOI, extraction status)
├── extraction_log.md          # append-only audit log
│
│   # ---- building the KB ----
├── batch_ocr.py               # OCR image-only PDFs in papers/
├── extract.py                 # local model: PDF → drafts + annotated PDF
├── annotate_paper.py          # colour-highlight a PDF from a draft's source_passages
├── auto_review.py             # checks, tier classification, independent model review
├── promote.py                 # the only way into the canonical folders
├── compare_extraction.py      # benchmark a model against entries you already curated
├── audit_quotes.py            # every canonical quote vs its PDF (graded)
├── quote_check.py             # the ONE quote grader the three checkers share
├── kb_status.py               # counts, review provenance, decoder reachability, papers needed
├── model_config.py            # resolves models.yaml / env vars; lists pulled models
├── ollama_client.py           # the one HTTP client to the local Ollama server
├── resource_monitor.py        # GPU/CPU watch during long runs
├── test_review_guardrails.py  # mock-Ollama tests of the review policy (no model needed)
├── neurosynth_bootstrap.py    # scaffold region drafts from Neurosynth meta-analyses
│
│   # ---- using the KB on a lesion ----
├── aphasia_kb.py              # loader + validator + query module
├── decode_lesion.py           # MNI mask → HarvardOxford overlap + Neurosynth terms
├── aphasia_kb_rag.py          # decode → retrieve → deterministic cited report (+ local narrative)
│
│   # ---- canonical content (status: approved; loaded by the KB) ----
├── regions/  impairments/  therapies/  predictors/  reviews/  ingredients/
│
│   # ---- workflow material ----
├── drafts/{regions,impairments,therapies,predictors}/   # extractor writes here
├── auto_review_log/           # per-draft sidecar audit YAML
├── examples/                  # worked example (not loaded)
├── papers/                    # source + annotated PDFs — NOT tracked (copyright)
├── _compare/                  # sandbox extractions and audit CSVs — NOT tracked
└── _neurosynth_cache/         # Neurosynth v7 data — NOT tracked; regenerated
```

## Scripts

| Script | Role | Needs |
|---|---|---|
| `batch_ocr.py` | Detect and OCR image-only PDFs so their text layer is searchable. Run before extracting an older paper. | local |
| `extract.py` | Read a PDF's text layer and emit schema-bound drafts plus the annotated PDF. `--dry-run` previews prompt size and `num_ctx`; `--batch` does every un-extracted PDF; `--out-dir _compare/<model>` sandboxes a benchmark run. | Ollama |
| `annotate_paper.py` | Highlight each `source_passage` in the PDF, colour-coded by what it supports. The reviewer's primary tool. | local |
| `auto_review.py` | Deterministic checks (schema, every quote in the PDF, no low confidence, no contradictions) that **reject or defer, never approve**; Tier A/B classification; with `--llm-review`, an independent model re-reads the paper and may approve Tier A. | local / Ollama |
| `promote.py` | Approve or reject as `human:<name>` or (Tier A only) `model:<tag>`; refuses a model on Tier B or reviewing its own extraction; stamps review provenance; writes the log line. | local |
| `compare_extraction.py` | Run a candidate model on a paper you already curated and grade quote fidelity, schema, coverage and calibration. The model-selection test in `MODELS.md` §3. | local |
| `audit_quotes.py` | Grade every canonical quote against its PDF: found / elided / table / anchored / near / absent / no_pdf. The legacy re-review triage. | local |
| `quote_check.py` | The shared grader behind `auto_review.py`, `compare_extraction.py` and `audit_quotes.py`, so one quote gets one grade. Module, not a CLI. | local |
| `kb_status.py` | Entries and findings per bucket, review provenance, relationship and strength counts, which KB regions the lesion decoder can reach, papers missing from `papers/` (`--papers-needed`), `--tag-legacy`. | local |
| `aphasia_kb.py` | Load, validate (`--check DIR`, `--issues`), query (`--lookup`); `KnowledgeBase(review_kinds=("human",))` restricts to person-approved findings. | local |
| `decode_lesion.py` | Atlas overlap and Neurosynth term decoding of an MNI mask. | local |
| `aphasia_kb_rag.py` | Decode → retrieve → deterministic cited report; `--llm` adds a local narrative over the same evidence; `--human-approved-only` drops model-approved and legacy findings. | local / Ollama |

Nothing here calls a cloud API. `OLLAMA_HOST` pointing off-machine is a
configuration error and the scripts warn about it.

## Papers

Source PDFs are not redistributed. `citations.md` carries the DOI for
every key; fetch papers through your own access and save them as
`papers/<Key>.pdf` (the key exactly, e.g. `Fridriksson2018Anatomy.pdf`).
`kb_status.py --papers-needed` lists what the canonical KB depends on
and is missing. Annotated copies (`<Key>_annotated.pdf`) are generated
locally and stay local.

## What each finding captures

A finding is a structured object, not a note: the claim; its target
(impairment, therapy, predictor or region) and `relationship` (causal,
correlational, recruitment, responder, treatment_response, synthesis);
method, design and evidence class; sample; statistics; confounders
controlled and not; how the paper defined the region; the authors' own
limitations; the extractor's `strength` and `provenance.confidence`;
and the required `source_passages`, each tagged by what it supports.
From v2.5 a `review` block records who approved it, when, and at which
tier. `schema.md` has the full specification.

## How this connects to CALMaR

The notebooks call the KB at the clinical-interpretation stage:
`decode_lesion.py` maps the mask to atlas regions and Neurosynth terms,
`aphasia_kb_rag.py` retrieves the matching approved findings and
renders the cited report that appears per subject. The report carries a
research-only caveat that no flag removes. Only regions present in
`decode_lesion.py`'s atlas map can be reached from a mask;
`kb_status.py` lists which KB regions are currently unreachable.

## Schema history

- **v2.0** rich finding object · **v2.1** required `source_passages`,
  `imaging_details` · **v2.2** multimodal `method`, required
  `relationship` · **v2.3** `predictors/` bucket · **v2.4** `reviews/`
  bucket, `method: narrative_review` · **v2.5** review provenance
  (`review_tier`, per-finding `review` block, `human:`/`model:` reviewers).

Changing the schema is a change to `schema.md` and `aphasia_kb.py`
together; changing who may approve what is a change to `GOVERNANCE.md`
and the scripts that enforce it together.
