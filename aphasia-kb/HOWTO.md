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
| **Cost** | Covered by your Cowork subscription | Free — local inference |
| **Auth** | Logged into the desktop app | None; needs `ollama serve` running |
| **Paper text leaves the machine?** | Yes — full text is sent to Anthropic | **No** — stays local |
| **Quality** | Frontier model | Lower; review drafts more carefully |
| **Speed** | Fast | Minutes per paper |
| **Style** | Interactive — Claude can ask clarifying questions, you can steer mid-extraction, you read the drafts as they're written | Fire-and-forget — drop a PDF, run a command, get drafts back |
| **Best for** | One paper at a time, judgment calls, when you want to read along | Batch (`--batch`), unattended runs, copyright-sensitive PDFs |

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
#              free + fully local (Ollama); slower, lower quality.

python aphasia-kb/aphasia_kb.py --check aphasia-kb/drafts/   # free, local

python aphasia-kb/auto_review.py --all                       # free, local
python aphasia-kb/auto_review.py --deferred --llm-review     # free, local
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
folder includes `calmar/`. Then say something like:

> Please extract findings from
> `/Users/me/calmar/aphasia-kb/papers/Foo2024.pdf`
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

### Option B — CLI `extract.py` (fully local, via Ollama)

```bash
ollama pull gemma4:26b                    # once
python aphasia-kb/model_config.py         # check what's configured
python aphasia-kb/extract.py --pdf aphasia-kb/papers/Foo2024.pdf
```

#### Choosing the model

Local models improve constantly, so the model choice lives in
**`models.yaml`**, not in the scripts. Three roles, each independently
settable:

| Role | Used by | Demands |
|---|---|---|
| `extract` | `extract.py` | Hardest — 50K-token context, structured JSON. Upgrade this first. |
| `review` | `auto_review.py --llm-review` | Subtle judgement; can promote into the KB. |
| `rag` | `aphasia_kb_rag.py --llm` | Easiest — summarises text it's handed. A smaller model is fine. |

To adopt a newer model, pull it and edit one line:

```bash
ollama pull <new-model>
$EDITOR aphasia-kb/models.yaml     # set roles.extract.model
python aphasia-kb/model_config.py  # confirm it resolved + is pulled
```

Resolution order, highest first: `--pick-model` → `--model` → role env
var (`APHASIA_EXTRACT_MODEL` etc.) → `APHASIA_LOCAL_MODEL` (all roles at
once, handy for A/B testing) → `models.yaml` → `default`. Every script
prints which layer won, so there's no guessing.

```bash
# try a new model across the whole pipeline without editing anything
APHASIA_LOCAL_MODEL=gemma4:31b python aphasia-kb/extract.py --batch
```

**Interactive picker.** To choose a model at run time — e.g. to A/B a
12B against a 26B — add `--pick-model`. It lists your locally-pulled
gemma models (biggest first, with size and parameter count) and lets
you pick one for that run only:

```bash
python aphasia-kb/extract.py --pdf papers/Foo2024.pdf \
    --out-dir _compare/gemma12 --pick-model
```

#### Live GPU/CPU monitor

Every real extraction run now samples load in the background and prints
a one-line summary when the model returns:

```
resource: GPU offload min 100% / avg 100%  ·  CPU avg 140% (peak 220%)  ·  RAM peak 63%  ✓ stayed fully on GPU
```

The number that matters is **GPU offload**: the fraction of the model
held in VRAM. At 100% the model is fully GPU-resident; below that it has
spilled to CPU RAM and inference slows by roughly an order of magnitude.
If a spill happens mid-run you get a live warning, not just a slow run —
lower `num_ctx` (or pick a smaller model) to fit. Disable with
`--no-monitor`. Sample the currently-loaded model on its own with:

```bash
python aphasia-kb/resource_monitor.py
```

> ✅ **Nothing leaves this machine.** Paper full text goes only to a
> local Ollama server, so no publisher PDF is transmitted to a
> third-party API. No API key, no per-paper cost.
>
> ⚠ Trade-off: slower (minutes per paper) and lower extraction
> quality than a frontier model. Expect more validation issues at the
> `promote.py` review step — review local drafts more carefully.

What happens under the hood (same as Option A, just non-interactive):

- The PDF is loaded with PyMuPDF and converted to plain text.
- `EXTRACTION_SKILL.md` + `schema.md` + the paper text are sent to
  the local model as a single prompt via `POST /api/chat`.
- The model returns one or more draft markdown files, written to the
  appropriate `drafts/{regions,impairments,therapies,predictors}/`
  subfolder.
- `annotate_paper.py` is run automatically against the new drafts to
  produce `papers/Foo2024_annotated.pdf` with colored highlights for
  each `source_passages` entry.
- A line is appended to `extraction_log.md`.

Variants:
- `--batch` to process every PDF in `papers/` that doesn't yet have
  drafts. Free, but budget real wall-clock time — run it overnight.
- `--citation '@Foo2024'` to set the citation key explicitly; otherwise
  inferred from the filename.
- `--model <tag>` for any model in `ollama list` (default `gemma4:26b`).
- `--num-ctx N` if you see the truncation warning (prompt filled the
  context) or if you run out of RAM and need to shrink it.
- `--ollama-host http://host:11434` if Ollama runs elsewhere.
- `--dry-run` to preview the prompt and the num_ctx that would be used.

**Troubleshooting**

| Symptom | Cause | Fix |
|---|---|---|
| `Couldn't reach Ollama` | server not running | `ollama serve` |
| HTTP 404 on the model | not pulled | `ollama pull gemma4:26b` |
| "prompt filled num_ctx" warning | paper truncated | raise `--num-ctx` |
| "0 drafts returned" | silent truncation, or model ignored the JSON contract | check `_last_extraction_response_*.txt`; raise `--num-ctx` |
| Empty response / process killed | out of RAM | lower `--num-ctx` or use a smaller model |
| "output hit num_predict" | JSON cut off | raise `--max-tokens` |
| Extraction very slow, `ollama ps` shows `100% GPU` → partly CPU | KV cache for a large `num_ctx` no longer fits in memory | lower `num_ctx` for `extract` in models.yaml |

#### About `ollama ps` and CONTEXT

`ollama ps` shows the context of the **currently loaded instance**,
which reflects whatever last called the model — often 4096, Ollama's
default for an interactive `ollama run`. That number does *not* limit
these scripts: they pass `num_ctx` explicitly on every request, which
makes Ollama reload the model at the requested size.

What it does tell you is **memory cost**. A 26B model is ~17GB of
weights; a 90K-token KV cache adds several GB on top. On a Mac with
unified memory, exceeding what's available doesn't error — Ollama
quietly spills to CPU and extraction slows by an order of magnitude.
If that happens, check `ollama ps` mid-run: a PROCESSOR reading that's
no longer `100% GPU` is the tell. Fix by lowering `num_ctx` for the
`extract` role in `models.yaml`.

Worth doing one paper before a `--batch` run, to see the real timing
and memory behaviour on your hardware.

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

# Pass 2: re-review the deferred ones with a LOCAL LLM second opinion.
# Runs on Ollama — draft text and verbatim quotes stay on this machine.
# This is where the "weak strength because Z=1.14 is marginal but
# the agent's own author_limitation already explains why" kind of
# edge case gets resolved.
python aphasia-kb/auto_review.py --deferred --llm-review
```

#### Guardrails on the local reviewer

This step can **promote drafts into the canonical KB**, so a wrong
approval is the most expensive mistake in the pipeline — and a mid-size
local model is more likely to make it than a frontier model, because
small models tend to be agreeable and the prompt explicitly invites them
to bless something the checker already flagged.

So local review is deliberately **asymmetric**:

| Model says | Effect |
|---|---|
| `agree_defer` | Stays deferred (fails safe) |
| `escalate_reject` | Honoured — always |
| `override_approve` | **Downgraded to `agree_defer`** unless you pass `--allow-local-override` |

Four nets sit in front of any override, each failing toward "leave it
for a human":

1. **Schema-constrained decoding** — Ollama restricts sampling to a JSON
   schema, so the verdict can't fall outside the enum and no required
   key can go missing. This is the single biggest reliability win for a
   26B model; far more robust than asking for a YAML block.
2. **Structural validation** — the response must review exactly the real
   finding ids (catches skipped findings and confabulated ids), must not
   contradict itself (approving while marking a finding unsupported),
   and must give a rationale long enough to audit.
3. **Self-consistency** — `--votes 3` (default) runs the review three
   times at temperature 0.4 and honours an override only if all three
   agree. Disagreement *is* the signal: it means the model is guessing.
4. **Override lockout** — the table above.

Everything that fires is recorded under `llm_review.guardrails` in the
sidecar YAML, so you can audit how the local model behaved before
deciding whether to trust it further:

```bash
grep -A3 guardrails aphasia-kb/auto_review_log/*.yaml
```

Once you've spot-checked a batch where you already know the right
answers and the rationales look sound, you can hand it more rope:

```bash
python aphasia-kb/auto_review.py --deferred --llm-review \
    --allow-local-override --votes 5
```

To verify the guardrails still work after editing the review code:

```bash
python aphasia-kb/test_review_guardrails.py   # no Ollama needed
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
python aphasia-kb/auto_review.py --all --emit-worksheet worksheet.yaml
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

Every CLI command is now free and fully local. The "Where it runs"
column flags whether any text leaves this machine.

| Command | Purpose | Where it runs |
|---|---|---|
| (Cowork chat) "Extract from papers/X.pdf following the SKILL" | Extract one paper, interactively | ⚠ Off-machine (Anthropic) |
| `python extract.py --pdf papers/X.pdf` | Extract one paper | Local (Ollama) |
| `python extract.py --batch` | Extract every un-extracted PDF in papers/ | Local (Ollama) |
| `python aphasia_kb.py --check drafts/` | Validate drafts | Local |
| `python aphasia_kb.py --check` | Validate the whole KB | Local |
| `python auto_review.py --all` | Deterministic auto-review pass | Local |
| `python auto_review.py --deferred --llm-review` | Local LLM second opinion on deferred | Local (Ollama) |
| `python test_review_guardrails.py` | Verify the review guardrails | Local (no model needed) |
| (Cowork chat) "Review the deferred drafts in auto_review_log/" | LLM second opinion, interactive | ⚠ Off-machine (Anthropic) |
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
- **`OLLAMA_HOST` set to a remote box.** Both scripts warn if the host
  isn't local, but the warning is easy to miss in a batch run — and it
  silently defeats the reason for running locally. Check with
  `echo $OLLAMA_HOST`, or pass `--ollama-host http://localhost:11434`.
- **Local review approves nothing.** Expected. `override_approve` is
  downgraded to `agree_defer` unless you pass `--allow-local-override`;
  check `llm_review.guardrails` in the sidecar to confirm that's why.
- **Everything defers after switching to local extraction.** Likely the
  extraction, not the review: check whether the extract run printed a
  `num_ctx` truncation warning. A truncated paper produces plausible-
  looking drafts whose quotes don't match the source.
- **Legacy cost note.** Only the Cowork chat paths now go off-machine.
  The CLI is free local Python. If you're cost-sensitive, do the
  extraction locally and use only the deterministic
  auto-review pass (no `--llm-review`); for borderline drafts, ask
  Cowork-Claude to weigh in instead of running `--llm-review`.
- **`promote.py --approve` refuses on validation.** Run
  `python aphasia_kb.py --check drafts/X.md` first; the validator
  names the field that's broken.
