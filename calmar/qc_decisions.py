"""Persistent, participant-scoped choices at the notebook QC checkpoint."""

from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import tempfile


def _read(directory, entry):
    path = Path(directory) / "QC_decision.json"
    if not path.exists():
        return {"schema_version": 1, "subject": entry["subject"],
                "session": entry.get("session") or "", "events": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if (data.get("schema_version") != 1
            or data.get("subject") != entry["subject"]
            or data.get("session") != (entry.get("session") or "")
            or not isinstance(data.get("events"), list)):
        raise ValueError(f"QC decision record does not match this participant/session: {path}")
    return data


def record_qc_choice(directory, entry, choice, checkpoint_id):
    """Append a user action atomically; preserve ratings and previous choices."""
    if choice not in ("review_requested", "skipped", "existing_reused"):
        raise ValueError(f"Unknown QC choice: {choice}")
    directory = Path(directory)
    data = _read(directory, entry)
    # Retrying a cohort write after a failure must not duplicate prior events.
    if any(event.get("checkpoint_id") == checkpoint_id and event.get("choice") == choice
           for event in data["events"]):
        return directory / "QC_decision.json"
    data["events"].append({"choice": choice, "chosen_by": "user",
                           "timestamp": datetime.now(timezone.utc).isoformat(),
                           "checkpoint_id": checkpoint_id})
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "QC_decision.json"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=directory,
                                         prefix=".QC_decision.", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(data, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return path


def report_qc_text(directory, entry):
    """Plain-text notice for PDF reports."""
    events = _read(directory, entry)["events"]
    if not events:
        return "QC status: no checkpoint choice recorded."
    if events[-1].get("choice") == "skipped":
        return "QC was skipped by the user."
    if events[-1].get("choice") == "existing_reused":
        return "Existing QC reused by the user; consult saved ratings for stage coverage."
    return "QC review selected; consult saved ratings for completion."


def report_qc_notice(directory, entry):
    """Render the saved choice in both inline and standalone report HTML."""
    events = _read(directory, entry)["events"]
    if not events:
        return "<p><b>QC status:</b> No QC checkpoint choice is recorded.</p>"
    event = events[-1]
    timestamp = escape(str(event.get("timestamp", "")))
    if event.get("choice") == "skipped":
        return (
            '<div role="note" style="border:2px solid #b36b00;background:#fff3cd;'
            'color:#352400;padding:12px;margin:12px 0;break-inside:avoid">'
            '<b>QC was skipped by the user.</b> '
            'This report was generated without requiring QC review at the checkpoint. '
            f'<br><small>Choice recorded: {timestamp}</small></div>')
    if event.get("choice") == "review_requested":
        return (
            '<p><b>QC review was selected by the user.</b> '
            'This choice does not confirm completion of the review; consult the saved QC ratings.'
            f'<br><small>Choice recorded: {timestamp}</small></p>')
    if event.get("choice") == "existing_reused":
        return (
            '<p><b>Existing QC was reused by the user.</b> '
            'Previously saved ratings were retained; consult them for stage coverage and any repair flags.'
            f'<br><small>Choice recorded: {timestamp}</small></p>')
    raise ValueError("Unrecognized saved QC choice")
