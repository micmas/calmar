# Governance of the aphasia knowledge base

How entries get in, who is accountable for them, and what the
downstream report is allowed to assume. This file is policy; `HOWTO.md`
is the procedure and `schema.md` is the data contract. When they
disagree, this file wins and the other two get fixed.

**Status:** adopted 2026-10 · replaces the implicit policy under which
`auto_review.py` could promote drafts on its own.

---

## 1. Principles

1. **Every finding traces to the page.** A finding exists only if each
   of its `source_passages` is found verbatim in the paper's text layer.
   A paraphrase is not a passage. A quote the checker cannot find is a
   failed draft, not a quality issue.
2. **Nothing is approved without a reader who re-opened the PDF.** The
   reader may be a person or an independent model (§3), but in either
   case the review is a *second reading of the paper*, not a check of
   the draft's internal consistency.
3. **A named person is accountable for everything in the canonical
   folders.** Model review is delegated review: the maintainer who
   enabled it owns its approvals and audits them (§4).
4. **Paper text and patient data stay on the machine.** Extraction,
   review and lesion decoding run locally. Source PDFs are never
   committed. The repository ships findings and DOIs.
5. **The report may only say what the KB says.** Causal stays causal,
   correlational stays correlational, review-synthesis is weighted
   separately, and every line cites an entry id and a paper. A region
   with no approved findings is reported as a gap, not filled in.
6. **Research use only.** No output of this KB is clinical advice; the
   caveat is part of every report and is not removable by a flag.

---

## 2. Who may do what

| Actor | Identifier in `reviewer:` / log | May | May not |
|---|---|---|---|
| Extractor model | `created_by: agent:<model-tag>` | write to `drafts/`, `papers/*_annotated.pdf`, `extraction_log.md`, `citations.md` | touch any canonical folder; review its own drafts |
| Deterministic checks (`auto_review.py`) | `auto-reviewer` | reject or defer a draft; emit a reviewer worksheet | approve anything |
| Independent reviewer model | `model:<model-tag>` | verify passages against the PDF, check interpretation, **approve Tier A drafts** (§3), defer or reject any draft | approve Tier B; edit a draft; review drafts from the same model tag that extracted them |
| Person | `human:<name>` | everything above; approve Tier B; audit model approvals; change this policy | approve a draft without opening the annotated PDF |

"Independent" means a different model tag from the extractor. Same
family at a different size counts (`gemma4:31b` reviewing `gemma4:26b`
drafts); the same tag does not. The log line records both.

---

## 3. The two review tiers

Every draft is classified **before** review by `auto_review.py` from
its frontmatter. The classification is logged and is not a judgement
call.

### Tier A — an independent model may approve

All of the following must hold:

- every `source_passage` matches the PDF text layer **exactly**
  (`--require-pdf-match`; near-matches are Tier B);
- schema valid with no warnings;
- `provenance.confidence` is `high` or `medium`, and `provenance.flags`
  is empty;
- the draft **appends findings to an existing canonical entry** (a new
  entry id is Tier B);
- `strength` is `weak` or `moderate`;
- `evidence_quality` is a primary quantitative class (not
  `narrative-review`, not `case-study`);
- the bucket is `regions`, `impairments` or `predictors`.

### Tier B — a person must approve

Anything not Tier A, and always:

- any `therapies/` or `ingredients/` entry — these become
  recommendations downstream;
- `strength: strong` or `definitive`;
- any new entry id, region consolidation, or alias change;
- `reviews/` entries (narrative synthesis);
- any draft the model reviewer did not fully agree with, on any field;
- any draft where the model reviewer and the deterministic checks
  disagree;
- single-case extractions, and anything with `provenance.flags`.

### What the reviewer model must actually do

The model reviewer gets the draft, the full text layer of the paper,
and the schema. For every finding it must report, per field:

| Check | Question answered |
|---|---|
| Passage location | Is each passage present verbatim? On which page? |
| Passage relevance | Does the passage support the field it is tagged for (claim / statistics / sample / limitation …), or only something nearby? |
| Direction and relationship | Does the paper itself make a *causal* claim, or has the draft upgraded a correlation? |
| Strength | Is `strength` at or below what the authors claim for their own result? |
| Numbers | Do n, effect size, thresholds and p-values match the text and tables exactly? |
| Limitations | Are the authors' stated limitations captured, including ones that weaken the finding? |
| Omission | Is there a result in the paper that contradicts or qualifies the finding and was left out? |

Output is schema-constrained (Ollama `format`): per-field
`agree | disagree | cannot_verify` with a one-line reason, and a verdict
`approve | defer | reject`. The reviewer never edits the draft; a
disagreement defers it to a person with the reasons attached. The
sidecar in `auto_review_log/` keeps the full output.

`approve` is honoured only for Tier A. For Tier B it is recorded as
`agree_defer` and the draft goes to a person with the model's notes,
which is the current guardrail behaviour (`--allow-local-override`
stays off).

---

## 4. Accountability for model approvals

- **Log line.** `MODEL-APPROVED | @Cite | entry | reviewer: model:<tag> |
  extractor: agent:<tag> | tier: A`. Never `APPROVED` and never a
  person's name.
- **Entry stamp.** `reviewer: model:<tag>`, `reviewed_on`, and
  `review_tier: A` (schema v2.5 adds `review_tier` and `audited_by` as
  optional fields; older entries load unchanged).
- **Audit.** After every 20 model approvals, or monthly, whichever
  comes first, a person re-reviews a random 20 % (minimum 3) against
  the annotated PDFs and logs `AUDIT | pass|fail | entries…`. One
  substantive failure (a wrong number, an upgraded relationship, a
  passage that does not support its field) pauses model approval; all
  `MODEL-APPROVED` entries since the last clean audit return to
  `in_review` until a person has read them.
- **Downstream.** `aphasia_kb_rag.py` marks model-approved and
  pre-policy findings in the report and accepts `--human-approved-only`;
  the same switch for code is `KnowledgeBase(..., review_kinds=("human",))`.
  The notebook's clinical-interpretation cell should load the KB with it
  (follow-up: wire and test in Neurodesk).
- **Revocation.** A person can reject any approved entry at any time
  with `promote.py --reject --reviewer human:<name> --reason`; the log
  keeps the history, the file moves back to `drafts/`.

---

## 5. Legacy entries (approved before this policy)

As of 2026-10-16, 33 of the 59 canonical entries with a reviewer field
were approved by `auto-reviewer` or a model without a PDF-verified
second reading, and several more carry `AUTO-APPROVED` log lines under
a person's name. They remain loadable but are tagged
`review_tier: legacy` and are excluded by `--human-approved-only`
until re-reviewed through §3. Order of re-review: `therapies/` first
(they drive recommendations), then entries with `strength: strong`,
then the rest.

---

## 6. Sources and rights

- Papers are obtained through the maintainer's institutional access or
  open licences and are never redistributed; `papers/` is git-ignored.
- `source_passages` are short attributed quotations for verification.
  They are not a substitute for the paper and the KB links the DOI.
- Extraction of copyrighted PDFs runs on the local model only. The
  cloud-API path is retired; `OLLAMA_HOST` pointing off-machine is a
  configuration error, and the scripts warn.
- Lesion masks used with `aphasia_kb_rag.py` are patient-derived data
  and are processed locally only; nothing about a lesion is written to
  the KB or the log.
- The KB is MIT-licensed as part of CALMaR. Model licences are noted
  in `MODELS.md` (OpenMDW for Nemotron, Apache 2.0 for Granite, Gemma
  terms for Gemma).

---

## 7. Changing this policy

Open a pull request that edits this file and, in the same PR, the code
that enforces it (`auto_review.py` tier classification, `promote.py`
stamps, `aphasia_kb_rag.py` filters). A policy the scripts do not
enforce is not a policy. Record the change and date at the top.
