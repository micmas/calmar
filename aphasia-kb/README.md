# Aphasia knowledge base (v2)

A clinician-controlled, agent-extensible knowledge base linking lesion
locations to aphasia-related impairments and therapy responses. The
format is **markdown with rich YAML frontmatter**, designed for both
human review and machine consumption.

> **The user is always in the loop.** No agent writes directly into the
> canonical `regions/`, `impairments/`, or `therapies/` folders. Agents
> write to `drafts/`. A human reviewer promotes drafts to canonical
> entries via `promote.py`. This separation is the whole point of v2.

## Layout

```
aphasia-kb/
├── README.md                  # this file
├── schema.md                  # YAML frontmatter spec (v2 — read first)
├── EXTRACTION_SKILL.md        # agent's instruction manual
├── citations.md               # bibliography (@Key references)
├── extraction_log.md          # append-only audit log
├── aphasia_kb.py              # loader + validator + query module
├── promote.py                 # CLI for reviewing/promoting drafts
├── neurosynth_bootstrap.py    # (stage-2) auto-draft from meta-analyses
│
├── regions/                   # APPROVED region entries (canonical)
├── impairments/               # APPROVED impairment entries (canonical)
├── therapies/                 # APPROVED therapy entries (canonical)
├── drafts/                    # AGENT writes here; HUMAN reviews
│   ├── regions/
│   ├── impairments/
│   └── therapies/
├── examples/                  # worked-example entries (NOT loaded by KB)
├── papers/                    # PDFs the agent has been given (optional)
└── _legacy_v1/                # archived v1 entries; loader tags them legacy_v1
```

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
```

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

The v1 entries are preserved under `_legacy_v1/` and surface in the
loader with `status: legacy_v1` so the LINDA notebook can choose to
ignore them. They are kept as a starting point — the intent is for the
agent to re-extract each of them under v2 from the original papers.

## Status

This is a **proof-of-concept**. Every approved entry needs clinician
sign-off before being relied upon clinically. The schema is frozen for
v2; expanding it (new methods, new vocabularies) is a v2.1 change that
must update `schema.md` and `aphasia_kb.py` together.
