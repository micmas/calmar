# Extraction log

A running, append-only audit log of every agent extraction run and every
human review action. Every entry is one line, pipe-separated, in this
format:

```
<ISO date> | <ACTION> | <citation> | <entry id> | <metadata...>
```

Actions:

- `EXTRACTED` — agent wrote one or more drafts from a paper.
- `APPROVED`  — human moved a draft to the canonical folder.
- `REJECTED`  — human marked a draft as rejected (it stays in `drafts/`
                with `status: rejected` for the audit trail).
- `EDITED`    — human manually edited a canonical entry without going
                through `promote.py` (please add this manually if so).

This log is appended to automatically by `promote.py`. The agent should
add an `EXTRACTED` line for every run.

---

<!-- New entries are appended below this line -->
