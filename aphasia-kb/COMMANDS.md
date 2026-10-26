# Aphasia KB — command reference

Every command the knowledge base uses, in the order a paper moves
through them, with every option. Run from the **repository root** with
the venv active (`source .venv/bin/activate`). Policy (who may approve
what) is in [`GOVERNANCE.md`](GOVERNANCE.md); the procedure in prose is
in [`HOWTO.md`](HOWTO.md).

**Dry run is the default.** Every command that renames, moves or
rewrites files only prints what it would do until you add `--execute`.
The exceptions are `extract.py`, `promote.py` and `auto_review.py`,
which act when run (each has its own preview flag, listed below).

---

## The everyday sequence

```
# 1. add papers: drop PDFs into aphasia-kb/papers/ (= OneDrive calmar-papers), any name
python aphasia-kb/intake_papers.py                                      # preview
python aphasia-kb/intake_papers.py --execute --allow-probable --extract # register, rename, clean, OCR, extract

# 2. review
python aphasia-kb/normalize_drafts.py --execute                         # mechanical fixes to drafts
python aphasia-kb/auto_review.py --all --llm-review --require-pdf-match # model clears Tier A
python aphasia-kb/review_sheet.py --all --fix-pages --fill-phase        # sheets in drafts/_review/
python aphasia-kb/promote.py --list                                     # what is left for you
python aphasia-kb/promote.py --approve aphasia-kb/drafts/<bucket>/<file>.md --reviewer human:michele
python aphasia-kb/promote.py --reject  aphasia-kb/drafts/<bucket>/<file>.md --reviewer human:michele --reason "..."

# 3. check and publish
python aphasia-kb/kb_status.py
git add aphasia-kb && git commit -m "..." && git pull --rebase --autostash && git push
```

---

## 1. Getting papers in

### `intake_papers.py` — everything between the download and the extractor

Runs, in order: register → rename → strip cover sheets → OCR → status →
(optionally) extract. Each step skips what is already done, so
re-running is safe and resumes an interrupted batch.

| Option | Meaning |
|---|---|
| *(none)* | Dry run of every step. |
| `--execute` | Apply all steps. |
| `--allow-probable` | Also rename files matched only by author + year + title (PDFs that print no DOI, e.g. Lancet, Neurology). The dry run shows which. |
| `--extract` | Afterwards run `extract.py --batch` on every paper with no findings yet. With `--execute` it extracts; without, it lists the queue. |
| `--from DIR` | First copy PDFs out of `DIR` (e.g. `~/Downloads`) whose DOI matches a cited paper that has no PDF yet. Nothing is moved; other files are ignored. |
| `--no-register` | Skip step 1: do not create `citations.md` entries for unknown PDFs. |
| `--no-ocr` | Skip the OCR step. |
| `--papers-dir DIR` | Use another papers folder (default `aphasia-kb/papers`). |

The steps also run on their own:

### `register_papers.py` — give every PDF a citation entry

Looks up each unknown PDF's DOI at Crossref and appends a `[seed]`
block to `citations.md` under "Registered automatically", with a dated
note. Needs network. A PDF with no DOI is listed for a hand-written
block.

| Option | Meaning |
|---|---|
| `--execute` | Append the entries. |
| `--papers-dir DIR`, `--citations FILE` | Other locations. |

### `match_papers.py` — rename downloads to `<Key>.pdf`

Matches on the DOI in the text, the DOI in the filename, or the title
in the filename; author + year + title as a last resort ("probable").
Never overwrites.

| Option | Meaning |
|---|---|
| `--execute` | Rename. |
| `--allow-probable` | With `--execute`, also rename the author/year/title matches. |
| `--papers-dir DIR`, `--citations FILE` | Other locations. |

### `strip_cover_pages.py` — drop publisher cover sheets

JSTOR, HighWire/AJNR, Taylor & Francis, ProQuest, ResearchGate,
Elsevier/Springer author copies, ClinicalKey. Scanned pages and running
footers are never treated as covers. Originals go to `papers/_originals/`.

| Option | Meaning |
|---|---|
| `FILE …` | Only these PDFs (default: all of `papers/`). |
| `--execute` | Strip. |
| `--pages N` | With named files: drop exactly N leading pages, no detection. |
| `--papers-dir DIR` | Other folder. |

### `batch_ocr.py` — make scans searchable

Needs `brew install ocrmypdf`. Detects image-only PDFs, including scans
with a stamped text line; retries with forced OCR if the first pass
leaves the text thin. Originals go to `papers/_originals/`.

| Option | Meaning |
|---|---|
| `--execute` | Run OCR (default is a dry run). |
| `--threshold N` | Characters in the first 3 pages below which a PDF counts as image-only (default 200). |
| `--limit N` | Stop after N files (testing). |
| `--papers-dir DIR` | Other folder. |

### `verify_dois.py` — check `citations.md` against Crossref

Flags entries whose DOI resolves to a different title or first author.
Run after writing citation blocks by hand. Needs network; read-only.

| Option | Meaning |
|---|---|
| `--status TAG` | Only entries with this tag (`seed`, `cited`, …). |
| `--key @Key` | Only this entry (repeatable). |
| `--citations FILE` | Check another file in the same format. |

---

## 2. Extracting

### `extract.py` — the local model reads a paper and writes drafts

Writes `drafts/<bucket>/<id>__<Key>.md`, the annotated PDF and an
EXTRACTED line in `extraction_log.md`. Streams the response (progress
every 2 minutes), cuts repetition loops early and retries once, and
retries once with a larger budget if a genuine output overflows.

| Option | Meaning |
|---|---|
| `--pdf FILE …` | Extract these PDFs (one or more). Works even if the paper already has findings. |
| `--batch` | Every PDF in `papers/` with no findings yet. Skips `[refused]` papers, PDFs over 60 pages, and PDFs with no `citations.md` entry. |
| `--citation @Key` | Force the key (single `--pdf` only; normally inferred from the filename). |
| `--out-dir DIR` | Sandbox: write drafts under `DIR/drafts/`, no annotated PDF, no log line. For benchmarks and second opinions. |
| `--dry-run` | Build the prompt, don't call the model; saves it to `aphasia-kb/_extraction_dry_run.txt`. |
| `--model TAG` | Ollama model for this run (default from `models.yaml`). |
| `--pick-model` | Choose interactively from the pulled models. |
| `--max-tokens N` | Output budget (default from `models.yaml`, 16000). |
| `--num-ctx N` | Context window (default: sized from the prompt). |
| `--lean` | Leave `citations.md` out of the prompt (smaller, faster; the model then can't see what is already cited). |
| `--timeout S` | Give up on one paper after S seconds (default 3600). |
| `--no-monitor` | No GPU/CPU monitor line. |
| `--ollama-host URL` | Another Ollama server (default `http://localhost:11434`; a non-local host is warned about). |

### `backfill.py` — bring older findings up to schema v2.7

Asks the extraction model, once per paper, only for the fields a finding
is missing (`lesion_mapping`, `sample.phase`, `sample.cohort`,
`author_limitations`). Claims, quotes and reviews are untouched. A value
is written only if its quote is found in the PDF (or it is
`not_reported`); the quote is added to the finding's `source_passages`
and the finding gets `filled: {by, date, tool, fields}`. Approved entries
are written too; the report labels these values "filled in by a model".
A file moves to `schema_version: 2.7` once all its findings are complete.

| Option | Meaning |
|---|---|
| (none) | Dry run: papers and their missing fields. |
| `--execute` | Ask the model and write the verified values. |
| `--citation @Key` | Only these papers (repeatable). |
| `--fields a,b` | Subset of `lesion_mapping,phase,cohort,author_limitations`. |
| `--drafts-only` | Leave approved entries alone. |
| `--limit N` | Stop after N papers. |
| `--from-response FILE` | Apply a saved response (`_last_backfill_response_<Key>.txt`) for one `--citation`. |

### `reextract.py` — extract chosen papers again, on purpose

Old drafts and sidecars move to `_compare/superseded/<date>/` (nothing
deleted); a paper that already has approved findings goes to the
sandbox `_compare/rerun/` instead, so nothing approved is duplicated.

| Option | Meaning |
|---|---|
| `KEY …` | Citation keys, with or without `@`. |
| `--preset placeholder` | The five therapy papers whose May findings quote "clinical knowledge". |
| `--preset selective-retry` | The fifteen papers cut to 8 findings by the 20–21 Oct overflow retry. |
| `--into-drafts` | Write fresh drafts even when approved findings exist (to replace, not compare). |
| `--execute` | Move the old drafts and extract. |
| `--papers-dir DIR` | Other folder. |

### `compare_extraction.py` — compare a sandbox extraction with the KB

Quote fidelity, schema, coverage and calibration of a sandbox run
against the curated entries for the same paper. The model-selection
test in `MODELS.md` §3, and the way to merge a `reextract.py` sandbox run.

| Option | Meaning |
|---|---|
| `--citation @Key` | The paper (required). |
| `--candidate-dir DIR` | Where the sandbox run wrote (required). |
| `--show-claims` | Print every claim from both sides. Recommended. |
| `--reference-root DIR`, `--papers-dir DIR` | Other locations. |

### `annotate_paper.py` — highlight a draft's quotes in its PDF

`extract.py` runs this itself; use it to redo one by hand.

| Option | Meaning |
|---|---|
| `--draft FILE …` | Drafts whose passages to highlight (required). |
| `--pdf FILE` | The paper (required). |
| `--out FILE` | Output path (default `<pdf>_annotated.pdf`). |
| `--no-legend` | No colour-legend page. |
| `--fail-on-missing` | Exit non-zero if a quote can't be placed. |
| `--no-rename` | Don't rename the source PDF to `<Key>.pdf` first. |

---

## 3. Reviewing

### `normalize_drafts.py` — apply the save-time repairs to existing drafts

Missing `author_limitations` → `[]` + flag; missing `sample.phase` →
inferred; `region_definition` without `kind` → `not_reported`; imaging
finding without `reference_space` → `not_reported` + flag; predictor
fields copied from the canonical entry. Never touches canonical folders.

| Option | Meaning |
|---|---|
| `--execute` | Rewrite the drafts. |
| `--draft FILE` | Only this draft (repeatable). |

### `auto_review.py` — checks, tier, independent model review

Deterministic checks (schema, every quote in the PDF, confidence,
contradictions) can only reject or defer. With `--llm-review` the
review model re-reads the paper; it may approve **Tier A only** and
never its own extraction. Verdicts: `auto_approve` (promoted),
`checks_passed` (Tier B, yours), `defer_to_human`, `auto_reject`
(blocked until fixed; the draft stays where it is). Each draft gets a
sidecar in `auto_review_log/`.

| Option | Meaning |
|---|---|
| `--all` | Every pending draft. |
| `--draft FILE` | One draft. |
| `--deferred` | Only drafts whose last verdict was `defer_to_human`. |
| `--pending-pdf` | Only drafts provisionally approved on a machine without the PDF. |
| `--llm-review` | Use the local review model (`models.yaml` → `review`). Without it, deterministic checks only. |
| `--require-pdf-match` | Refuse approval when the PDF is unavailable. Use always. |
| `--provisional-without-pdf` | Without the PDF, mark would-be approvals provisional instead (for a laptop without papers). |
| `--votes N` | Model reviews per draft; approval needs all N to agree (default 3). |
| `--no-model-approve` | Record the model's verdicts but promote nothing (calibrating a new reviewer). |
| `--no-promote` | Compute and log verdicts, don't promote. |
| `--dry-run` | Compute verdicts; no promotion, no logs. |
| `--emit-worksheet FILE` | Write the selected drafts and their problems to a YAML worksheet for batch human review. |
| `--apply-verdicts FILE` | Apply a filled-in worksheet; needs `--reviewer human:<name>`. |
| `--reviewer human:<name>` | Who filled in the worksheet. |
| `--model TAG`, `--ollama-host URL`, `--papers-dir DIR` | Overrides. |

### `review_sheet.py` — one HTML page per draft, every quote on its page

Output in `drafts/_review/` (git-ignored: contains page images). Shows
each finding's claim, phase and time post-onset, and each quote with
its grade, the page it was found on, and a highlighted crop.

| Option | Meaning |
|---|---|
| `--all` | Every draft. |
| `--draft FILE` | One draft (repeatable). |
| `--fix-pages` | Write the page each quote was actually found on into the draft. |
| `--fill-phase` | Write the inferred `sample.phase` into drafts that lack it. |
| `--out-dir DIR`, `--papers-dir DIR` | Other locations. |

### `promote.py` — the only way into the canonical KB

| Option | Meaning |
|---|---|
| `--list` | Pending drafts — your review queue. |
| `--show FILE` | Print one draft. |
| `--diff FILE` | Diff a draft against the canonical entry it would merge into. |
| `--approve FILE` | Approve: merge into the canonical entry, stamp the review block, log APPROVED. |
| `--reject FILE` | Mark `status: rejected` in place, log REJECTED. |
| `--reviewer human:<name>` | Required for approve/reject. `model:<tag>` only for Tier A and only if it didn't extract the draft. |
| `--reason "..."` | Why rejected (goes to the log). |
| `--tier A\|B` | Tier from `auto_review.py`; required (as A) for a model reviewer. |
| `--extractor agent:<tag>` | Who extracted the draft (default: its `created_by`). |

---

## 4. Checking the KB

### `kb_status.py` — counts and gaps

Entries and findings per bucket, review provenance (person / model /
legacy), findings by recovery phase, relationship and strength, which
regions the lesion decoder can reach, papers cited vs present.

| Option | Meaning |
|---|---|
| *(none)* | The summary. |
| `--papers-needed` | Cited papers with no PDF, with DOIs. |
| `--tag-legacy` | Tag pre-policy entries `review_tier: legacy` (with `--dry-run` to list only). |
| `--json` | Machine-readable output. |

### `audit_quotes.py` — every canonical quote against its PDF

Grades: found · elided · table (verified) · anchored · near (check by
eye) · absent (re-review first) · no_pdf. The legacy re-review triage
and the 20 % audit in GOVERNANCE.md.

| Option | Meaning |
|---|---|
| `--bucket NAME` | Only this bucket (repeatable). |
| `--show-absent` | List every absent quote. |
| `--csv FILE` | One row per passage. |
| `--fail-on-missing` | Exit 1 if any quote is absent (for CI). |
| `--root DIR`, `--papers-dir DIR` | Other locations. |

### `aphasia_kb.py` — loader and validator

| Option | Meaning |
|---|---|
| `--check DIR` | Validate the entries in DIR (`aphasia-kb/drafts/`, `aphasia-kb/regions`, …). |
| `--issues` | Print every validation issue in the KB. |
| `--drafts` | List pending drafts. |
| `--lookup NAME` | Find a region by id, name or alias. |
| `--include STATUS …` | Statuses to load (default: everything). |
| `--root DIR` | Other KB folder. |

### `atlas_mapping.py` — atlas labels → KB regions

| Option | Meaning |
|---|---|
| `--write-table` | Regenerate `atlas_mapping/MAPPING.md` and `EVIDENCE_GAPS.md`. |
| `--coverage` | How many location findings the mapping can reach. |

### Tests

```
python aphasia-kb/test_review_guardrails.py      # the review policy, against a mock Ollama
python -m pytest tests/test_kb_atlas_mapping.py  # the atlas mapping
```

---

## 5. Repairs

### `rekey_paper.py` — move a paper from a wrong key to the right one

Renames the PDF, annotated PDF, drafts and sidecars; rewrites `id:` and
`citation:`; fixes the log and adds a REKEYED line. Drafts only.

| Option | Meaning |
|---|---|
| `--auto` | Every draft key missing from `citations.md`, matched by the PDF's DOI. |
| `--from @Old --to @New` | One paper explicitly (the new key must exist in `citations.md`). |
| `--execute` | Apply. |

---

## 6. Using the KB on a lesion

### `aphasia_kb_rag.py` — decode a mask, retrieve evidence, write the report

| Option | Meaning |
|---|---|
| `LESION` | Binary lesion mask in MNI space (`.nii.gz`). |
| `--human-approved-only` | Use only findings a person approved (the notebook default). |
| `--phase PHASE …` | Only findings from these recovery phases, e.g. `--phase chronic mixed longitudinal` for a chronic patient. |
| `--llm` | Add a narrative written by the local model over the same evidence. |
| `--min-overlap-pct X` | Ignore atlas regions the lesion covers less than X % of (default 1). |
| `--min-term-r R` | Ignore Neurosynth terms below correlation R (default 0). |
| `-o FILE` | Write the report markdown here. |
| `--model TAG`, `--ollama-host URL`, `--kb-root DIR` | Overrides. |

### `decode_lesion.py` — atlas overlap and Neurosynth terms only

| Option | Meaning |
|---|---|
| `LESION` | The mask. |
| `--terms T …` | Neurosynth terms to decode (default list in the script). |
| `--cache DIR` | Neurosynth cache (default `_neurosynth_cache/`). |

---

## 7. Models

```
python aphasia-kb/model_config.py      # which model each role uses, and what is pulled
ollama ps                              # what is loaded, and whether it is 100 % on the GPU
```

Roles live in `models.yaml` (`extract`, `review`, `rag`). One-off
overrides without editing it:

```
APHASIA_EXTRACT_MODEL=qwen3.8:27b python aphasia-kb/extract.py --pdf …
APHASIA_REVIEW_MODEL=… python aphasia-kb/auto_review.py …
APHASIA_RAG_MODEL=…     python aphasia-kb/aphasia_kb_rag.py …
```

Benchmark a candidate before adopting it (`MODELS.md` §3):

```
python aphasia-kb/extract.py --pdf aphasia-kb/papers/Alyahya2018NounVerb.pdf --model <tag> --out-dir aphasia-kb/_compare/<tag>
python aphasia-kb/compare_extraction.py --citation @Alyahya2018NounVerb --candidate-dir aphasia-kb/_compare/<tag> --show-claims
```

---

## 8. Git and the papers folder

```
git pull --rebase --autostash          # before starting work
git add aphasia-kb                     # papers/, _compare/, drafts/_review/ are ignored
git commit -m "..."
git push
git status --short                     # should list nothing after the push
ls -la aphasia-kb/papers               # should end in "-> …/OneDrive…/calmar-papers"
```

`aphasia-kb/papers` is a link to `calmar-papers` in OneDrive on every
computer (set "Always Keep on This Device" on that folder). To set it
up on a new clone, from the repository root:

```
rm -rf aphasia-kb/papers
ln -s "$HOME/Library/CloudStorage/OneDrive-TheUniversityofQueensland/Documents/calmar-papers" aphasia-kb/papers
```

Extract on one computer only; two computers annotating the same paper
at once make OneDrive write conflict copies.
