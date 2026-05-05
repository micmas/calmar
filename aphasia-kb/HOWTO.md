# How to extract a paper, end-to-end

This is the operational walkthrough for taking one PDF from your
`papers/` folder all the way to an approved entry in the canonical
KB. It assumes you've already done the one-time setup
(`pip install -r requirements.txt`).

The pipeline has six steps. Steps 1–3 are mostly automatic and run
in a few minutes per paper; steps 4–6 are where you spend judgment.

## Two ways to drive the agent (Cowork vs CLI)

The extraction step (and the optional LLM second-opinion step in
auto-review) can be done either in **Cowork** — the Claude desktop
app, where you chat with Claude and Claude operates files directly
— or via the **CLI** scripts in this folder. They produce identical
output (drafts in `drafts/`, an annotated PDF in `papers/`); pick
whichever fits the moment.

| | Cowork (chat) | CLI (`extract.py`) |
|---|---|---|
| **Cost** | Covered by your Cowork subscription | **Pay-per-call against the Anthropic API** (~$0.35–0.50 / paper at Sonnet) |
| **Auth** | Logged into the desktop app | `ANTHROPIC_API_KEY` env var |
| **Style** | Interactive — Claude can ask clarifying questions, you can steer mid-extraction, you read the drafts as they're written | Fire-and-forget — drop a PDF, run a command, get drafts back |
| **Best for** | One paper at a time, judgment calls, when you want to read along | Batch (`--batch`), unattended runs, scripted pipelines |

Anywhere this doc says **"calls the Anthropic API"** below, the cost
note applies — only to those steps. The validator, auto-review's
deterministic pass, the worksheet emit/apply, and `promote.py` are
all local Python and free.

## TL;DR

```bash
cp ~/Downloads/Foo2024.pdf  aphasia-kb/papers/
# (optional) add a @Foo2024 block to citations.md if you want to
# pre-seed it with the bibliographic info; otherwise extract.py
# (or Cowork-Claude) will leave a placeholder you fill in later.

#  Step 2 — pick ONE of:
#  (a) Cowork: open Claude desktop, ask it to extract from
#      aphasia-kb/papers/Foo2024.pdf following EXTRACTION_SKILL.md.
#      Subscription cost; no per-paper charge.
#  (b) CLI:    python aphasia-kb/extract.py --pdf aphasia-kb/papers/Foo2024.pdf
#              ⚠ calls the Anthropic API (~$0.35–0.50 / paper).

python aphasia-kb/aphasia_kb.py --check aphasia-kb/drafts/   # free, local

python aphasia-kb/auto_review.py --all                       # free, local
python aphasia-kb/auto_review.py --deferred --llm-review     # ⚠ API call
python aphasia-kb/auto_review.py --emit-worksheet worksheet.yaml   # free
# fill in verdicts in worksheet.yaml
python aphasia-kb/auto_review.py --apply-verdicts worksheet.yaml \
    --reviewer "michele"                                     # free

git add aphasia-kb/ && git commit -m "Foo2024 extraction"
```

The rest of this file walks through each step and tells you what to
look at along the way.

---

## 1. Drop the PDF into `papers/`

```
aphasia-kb/papers/Foo2024.pdf
```

That's it for this step. The PDF itself is gitignored
(`aphasia-kb/papers/*.pdf`) — it stays local. The annotated PDF that
gets generated in step 2 is **not** ignored (`!*_annotated.pdf` rule
in `.gitignore`) so it travels with the repo and reviewers on other
machines can do the visual audit.

If the PDF text is image-only (scanned), you'll need to OCR it
yourself first — the extraction pipeline reads PDF text, not pixels.
Most modern PDFs from journals are fine; a few older scans need
`ocrmypdf` or similar before this point.

## 2. Extract — pick a path

This is the only step where the choice matters. Both paths produce
identical output: drafts in `drafts/`, an annotated PDF in `papers/`,
and a line in `extraction_log.md`.

### Option A — Cowork (subscription, no API charge)

Open Claude in the Cowork desktop app. Make sure your workspace
folder includes `aphasia-lesion-pipeline/`. Then say something like:

> Please extract findings from
> `/Users/me/aphasia-lesion-pipeline/aphasia-kb/papers/Foo2024.pdf`
> following `aphasia-kb/EXTRACTION_SKILL.md`. Write draft markdown
> files into `aphasia-kb/drafts/`, run annotate_paper.py to produce
> the annotated PDF, append to `extraction_log.md`, and update
> `citations.md`.

Claude reads the SKILL + schema + the PDF, then writes the drafts
directly with its file tools, runs `annotate_paper.py` via Bash,
and appends to the logs. The advantage is interactive: you can
read the drafts as they're produced, ask Claude to revise a claim,
or stop early if the paper turns out to be a single-case report
that should have been refused.

**Cost:** covered by your Cowork subscription. No per-paper charge,
no API key needed.

### Option B — CLI `extract.py` (pay-per-paper API call)

```bash
python aphasia-kb/extract.py --pdf aphasia-kb/papers/Foo2024.pdf
```

> ⚠ **This calls the Anthropic API.** Roughly $0.35–0.50 per paper
> at the default Sonnet model. Requires `ANTHROPIC_API_KEY` set
> (`export ANTHROPIC_API_KEY="sk-ant-..."`). Get a key at
> https://console.anthropic.com → API Keys.

What happens under the hood (same as Option A, just non-interactive):

- The PDF is loaded with PyMuPDF and converted to plain text.
- `EXTRACTION_SKILL.md` + `schema.md` + the paper text are sent to
  the Anthropic API as a single prompt.
- The model returns one or more draft markdown files, written to the
  appropriate `drafts/{regions,impairments,therapies,predictors}/`
  subfolder.
- `annotate_paper.py` is run automatically against the new drafts to
  produce `papers/Foo2024_annotated.pdf` with colored highlights for
  each `source_passages` entry.
- A line is appended to `extraction_log.md`.

Variants:
- `--batch` to process every PDF in `papers/` that doesn't yet have
  drafts (useful after dropping in 5 papers at once — and the cost
  scales linearly, ~$0.35–0.50 per paper).
- `--citation '@Foo2024'` to set the citation key explicitly; otherwise
  inferred from the filename.
- `--model claude-haiku-4-5-20251001` for ~10× cheaper / lower quality.
- `--model claude-opus-4-6` for ~3× more expensive / highest quality.
- `--dry-run` to preview the prompt without spending API calls.

### Either way

If `citations.md` doesn't have a block for the paper's `@Key` yet,
the agent adds a placeholder — fill in the proper bibliographic
info now (authors, journal, doi). The `[seed | cited | extracted]`
status tag system lives in the citations.md header; this paper
becomes `[extracted]`.

## 3. Validate with `aphasia_kb.py --check`

```bash
python aphasia-kb/aphasia_kb.py --check aphasia-kb/drafts/
```

This checks that every draft conforms to v2.3 schema: required
fields present, controlled-vocabulary values used, source_passages
shape correct, etc. The expected output is `issues: 0`.

If you see issues, the validator names the file, finding ID, and
field. Open the draft in your editor, fix the field, and re-run
`--check`. Common fixes: a `direction` value that's not in the vocab,
an empty `confounders_controlled` field that should be `[]`, a
missing `provenance.flags` list.

If you re-extract the same paper (say, with a stronger model or
after updating the EXTRACTION_SKILL), the agent overwrites the
existing drafts. Diff with git to see what changed.

## 4. Auto-review (deterministic + optional LLM)

`auto_review.py` is the agentic pre-screening pass — it runs
deterministic checks per draft, optionally adds an LLM second
opinion, and writes a sidecar audit YAML to
`auto_review_log/<draft_basename>.yaml`. The verdicts are:

- `auto_approve` — all checks pass; safe to promote without human
  intervention. Will `shell out` to `promote.py --approve` unless
  you pass `--no-promote` or `--dry-run`.
- `defer_to_human` — at least one soft check failed. Needs your
  judgment. The sidecar lists exactly which check tripped and why.
- `auto_reject` — a hard check failed (schema invalid,
  contradictions, low-confidence finding). Stays in drafts/ with the
  failure recorded.
- `provisional_approve` — only set by the LLM-second-opinion pass:
  deterministic deferred but the LLM read the source quotes and
  vouched for the draft. You still see this and confirm.

Run two passes:

```bash
# Pass 1: deterministic only. Free — local Python, no API call.
# Anything that's clearly fine auto-promotes; anything iffy lands
# in defer_to_human.
python aphasia-kb/auto_review.py --all

# Pass 2: re-review the deferred ones with an LLM second opinion.
# ⚠ This calls the Anthropic API (sonnet by default; cost scales
# with the number of deferred drafts × tokens per draft, typically
# a few cents per draft).
# This is where the "weak strength because Z=1.14 is marginal but
# the agent's own author_limitation already explains why" kind of
# edge case gets resolved.
python aphasia-kb/auto_review.py --deferred --llm-review
```

**Cowork alternative for Pass 2:** instead of `--llm-review`, you
can open the deferred drafts in Cowork and ask Claude to read them
+ the annotated PDF and recommend approve/defer/reject for each.
Same logic, no API charge. Then either edit the sidecar YAMLs in
`auto_review_log/` directly, or jump straight to step 5 with the
Cowork verdicts in mind.

If you want to require PDF quote-match (a hard check that every
`source_passages[].quote` is found in the corresponding annotated
PDF), add `--require-pdf-match`. This catches fabricated quotes — but
only works on machines that have the source PDFs locally (i.e., not
on a fresh clone where only annotated PDFs traveled with git).

After both passes, every draft has a verdict in its sidecar YAML.

## 5. Generate a worksheet, fill in verdicts, apply

```bash
python aphasia-kb/auto_review.py --emit-worksheet worksheet.yaml
```

This produces `worksheet.yaml` at the repo root with one entry per
deferred draft, including a digest of each finding's claim, target,
strength, confidence, flags, and the raw `claim` source-passage
quotes. You don't need to open the underlying drafts — the worksheet
gives you everything you need at a glance.

Open `worksheet.yaml` in your editor and for each draft fill in:

```yaml
verdict: approve | agree_defer | reject
rationale: 1-3 sentences explaining the call.
per_finding:           # optional; omit if not needed
  - id: f1
    concern: "weak rating is correct: Z=1.14 is marginal."
    supports_approval: true
```

Then:

```bash
python aphasia-kb/auto_review.py --apply-verdicts worksheet.yaml \
    --reviewer "michele"
```

`approve` lifts a deferred draft to `auto_approve` and shells out to
`promote.py --approve --reviewer michele`. `reject` marks it
`auto_reject`. `agree_defer` keeps it deferred.

The annotated PDF is the visual aid you use while filling out the
worksheet. Open it in any PDF viewer side-by-side with worksheet.yaml.
Each `source_passages[].supports` field maps to a color
(`SUPPORTS_COLORS` in `aphasia_kb.py`); the colored highlight shows
exactly the sentence that justifies each claim/sample/method
field.

For drafts that already auto-approved (didn't go to defer), you've
got nothing to do — they were promoted in step 4.

## 6. Spot-check the canonical KB and commit

`promote.py` (called by auto_review.py during apply-verdicts):

1. Validates the draft once more.
2. Stamps `status: approved`, `reviewer:`, `reviewed_on:`.
3. If the canonical entry doesn't exist, moves the draft to
   `regions/` / `impairments/` / `therapies/` / `predictors/`.
4. If the canonical entry **does** exist (multi-paper consolidation),
   appends the new findings into the existing `findings:` list with
   renumbered IDs (`f1`, `f2`, … bumped as needed).
5. Removes the draft from `drafts/`.
6. Appends an `APPROVED` line to `extraction_log.md`.

Quick sanity checks before committing:

```bash
python aphasia-kb/aphasia_kb.py --check         # full KB, not just drafts/
git status aphasia-kb/                          # what got moved/added?
```

`--check` over the whole KB confirms canonical entries are still
valid after the merge. The new `regions/foo.md` (or whichever) and
the absence of the old draft show up in `git status`. The annotated
PDF should also be listed as a new file the first time:

```
new file:   aphasia-kb/papers/Foo2024_annotated.pdf
new file:   aphasia-kb/regions/left_foo_gyrus.md
modified:   aphasia-kb/extraction_log.md
modified:   aphasia-kb/citations.md
deleted:    aphasia-kb/drafts/regions/left_foo_gyrus__Foo2024.md
```

Commit:

```bash
git add aphasia-kb/
git commit -m "Foo2024 extraction (3 drafts approved, 1 rejected)"
git push
```

The annotated PDF travels with the commit. On any other machine,
`git pull` brings everything: the canonical entries, the annotated
PDF for visual audit, and the updated logs. The source PDF stays
local (gitignored) — that's the only thing you need to ship by
hand.

---

## Quick reference: where things live

| File / folder | What it is |
|---|---|
| `papers/Foo2024.pdf` | Source PDF you dropped in (gitignored) |
| `papers/Foo2024_annotated.pdf` | Color-highlighted PDF for review (tracked in git) |
| `drafts/{kind}/{id}__{citation}.md` | Pending drafts before promotion |
| `regions/`, `impairments/`, `therapies/`, `predictors/` | Approved canonical entries |
| `auto_review_log/{draft_basename}.yaml` | Per-draft audit sidecar (status + LLM rationale) |
| `worksheet.yaml` (repo root) | Reviewer worksheet for deferred drafts |
| `citations.md` | Bibliography with `[extracted | cited | seed]` tags |
| `extraction_log.md` | Append-only audit log of every extract / approve / reject |

## Quick reference: commands

The "Cost" column flags whether running the command spends Anthropic
API credits. Cowork-equivalent paths exist for the API rows; see
the prose above.

| Command | Purpose | Cost |
|---|---|---|
| (Cowork chat) "Extract from papers/X.pdf following the SKILL" | Extract one paper, interactively | Subscription |
| `python extract.py --pdf papers/X.pdf` | Extract one paper | ⚠ API (~$0.35–0.50) |
| `python extract.py --batch` | Extract every un-extracted PDF in papers/ | ⚠ API (~$0.35–0.50 per paper) |
| `python aphasia_kb.py --check drafts/` | Validate drafts | Free |
| `python aphasia_kb.py --check` | Validate the whole KB | Free |
| `python auto_review.py --all` | Deterministic auto-review pass | Free |
| `python auto_review.py --deferred --llm-review` | LLM second opinion on deferred | ⚠ API (a few cents / draft) |
| (Cowork chat) "Review the deferred drafts in auto_review_log/" | LLM second opinion, interactive | Subscription |
| `python auto_review.py --emit-worksheet worksheet.yaml` | Generate reviewer worksheet | Free |
| `python auto_review.py --apply-verdicts worksheet.yaml --reviewer "X"` | Apply human verdicts | Free |
| `python promote.py --list` | List pending drafts | Free |
| `python promote.py --show drafts/X.md` | Print one draft | Free |
| `python promote.py --diff drafts/X.md` | Diff against canonical | Free |
| `python promote.py --approve drafts/X.md --reviewer "X"` | Approve single draft | Free |
| `python promote.py --reject drafts/X.md --reviewer "X" --reason "Y"` | Reject single draft | Free |
| `python annotate_paper.py --pdf P.pdf --draft D.md` | Re-render the annotated PDF (rarely needed; extract.py / Cowork runs this for you) | Free |

## Common pitfalls

- **The PDF doesn't sync to the other machine.** Source PDFs are
  gitignored (size + copyright). Use the annotated PDF for review
  on the other machine — that's the whole point of the
  `!*_annotated.pdf` exception in `.gitignore`.
- **`pdf_quote_match` shows `passed: null`.** That's the auto-review
  noting it can't run the check because the source PDF isn't on this
  machine. The annotated PDF alone isn't enough — quote-match needs
  the *unannotated* source. Either copy the source PDF over manually
  or skip this check (the LLM second-opinion pass uses the annotated
  PDF's verbatim text, which is sufficient for most reviews).
- **`--apply-verdicts` won't promote.** The verdict in worksheet.yaml
  must literally be `approve` (not `approved`). The error message names
  the bad row.
- **Re-extracting overwrites my edits.** If you've manually edited a
  draft and then re-run `extract.py` (or asked Cowork to re-extract),
  the agent rewrites the file and your edits are gone (visible via
  `git diff`). Either don't re-extract, or commit your edits first
  and merge after.
- **API cost surprise.** Only `extract.py` and
  `auto_review.py --llm-review` hit the Anthropic API. The rest is
  free local Python. If you're cost-sensitive, do the extraction in
  Cowork (subscription-covered) and use only the deterministic
  auto-review pass (no `--llm-review`); for borderline drafts, ask
  Cowork-Claude to weigh in instead of running `--llm-review`.
- **`promote.py --approve` refuses on validation.** Run
  `python aphasia_kb.py --check drafts/X.md` first; the validator
  names the field that's broken.
