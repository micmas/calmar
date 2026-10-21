"""Participant data for local datasets: WAB-R scores, age, sex, days to WAB.

Everything is written to the dataset's BIDS ``participants.tsv`` (one row per
participant) with a ``participants.json`` describing each column, which is what
the participant report already reads (:func:`calmar.participant_report.participant_row`).

Two ways in:

* :class:`ParticipantForm` — a notebook form for one participant at a time.
* :func:`import_spreadsheet` — a CSV / TSV / XLSX for a cohort; its columns are
  matched to ours by name (:data:`ALIASES`), checked, and merged.

WAB-R (Kertesz, 2007): the four Aphasia Quotient subtests are entered as their
0–10 summary scores; the AQ is computed from them when it is not given
(AQ = 2 × (information content + fluency + comprehension + repetition + naming)),
and a given AQ that disagrees is reported. :func:`suggest_wab_type` applies the
WAB-R classification criteria to the subtest scores; it is a suggestion shown in
the form, never written unless the user chooses it.

Nothing here reads images or runs a tool.
"""
from __future__ import annotations

from dataclasses import dataclass
from html import escape
import json
import os
from pathlib import Path
import re
import tempfile

import pandas as pd


@dataclass(frozen=True)
class Column:
    name: str
    label: str
    description: str
    kind: str = "number"            # "number" | "text" | "choice"
    low: float | None = None
    high: float | None = None
    units: str | None = None
    choices: tuple = ()


WAB_TYPES = ("Global", "Broca's", "Isolation", "Transcortical motor", "Wernicke's",
             "Transcortical sensory", "Conduction", "Anomic", "Not aphasic (AQ >= 93.8)")

COLUMNS = (
    Column("age_at_stroke", "Age at stroke", "Age in years at the stroke.", low=0, high=120, units="years"),
    Column("sex", "Sex", "Sex as recorded by the site.", kind="choice", choices=("F", "M", "other")),
    Column("wab_days", "Days stroke → WAB", "Days from stroke onset to the WAB-R assessment "
           "(sets the recovery phase in the report).", low=0, high=36500, units="days"),
    Column("wab_info_content", "WAB-R information content", "Spontaneous speech: information content (0–10).",
           low=0, high=10),
    Column("wab_fluency", "WAB-R fluency", "Spontaneous speech: fluency, grammatical competence and "
           "paraphasias (0–10).", low=0, high=10),
    Column("wab_comprehension", "WAB-R auditory verbal comprehension", "Auditory verbal comprehension "
           "summary score (0–10; total / 20).", low=0, high=10),
    Column("wab_repetition", "WAB-R repetition", "Repetition summary score (0–10; total / 10).", low=0, high=10),
    Column("wab_naming", "WAB-R naming and word finding", "Naming and word finding summary score "
           "(0–10; total / 10).", low=0, high=10),
    Column("wab_aq", "WAB-R Aphasia Quotient", "Aphasia Quotient (0–100); computed from the subtests "
           "when not given.", low=0, high=100),
    Column("wab_type", "WAB-R aphasia type", "Aphasia classification from the WAB-R criteria.",
           kind="choice", choices=WAB_TYPES),
    Column("wab_date", "WAB-R date", "Date of the WAB-R assessment (YYYY-MM-DD), optional.", kind="text"),
)
BY_NAME = {c.name: c for c in COLUMNS}
SUBTESTS = ("wab_info_content", "wab_fluency", "wab_comprehension", "wab_repetition", "wab_naming")

#: Spreadsheet header spellings → our column (matching ignores case, spaces, '-' and '_').
ALIASES = {
    "participant_id": ("participant_id", "participant", "subject", "subject_id", "sub", "id", "study_id"),
    "age_at_stroke": ("age_at_stroke", "age", "age_stroke", "age_at_onset"),
    "sex": ("sex", "gender"),
    "wab_days": ("wab_days", "days_post_onset", "days_post_stroke", "time_post_onset", "dpo", "days"),
    "wab_info_content": ("wab_info_content", "information_content", "info_content", "wab_info"),
    "wab_fluency": ("wab_fluency", "fluency"),
    "wab_comprehension": ("wab_comprehension", "auditory_verbal_comprehension", "avc", "comprehension"),
    "wab_repetition": ("wab_repetition", "repetition"),
    "wab_naming": ("wab_naming", "naming", "naming_word_finding", "naming_and_word_finding"),
    "wab_aq": ("wab_aq", "aq", "aphasia_quotient", "wab_r_aq", "wabaq"),
    "wab_type": ("wab_type", "aphasia_type", "wab_classification", "type"),
    "wab_date": ("wab_date", "assessment_date", "date"),
}
_SQUASH = re.compile(r"[^a-z0-9]")


def _key(text):
    return _SQUASH.sub("", str(text).lower())


_ALIAS_LOOKUP = {_key(a): col for col, names in ALIASES.items() for a in names}
_SEX = {"f": "F", "female": "F", "woman": "F", "m": "M", "male": "M", "man": "M"}


def participant_id(label):
    """BIDS participant label: ``"12"``, ``"P 12"`` or ``"sub-12"`` → ``"sub-12"`` (letters and digits only)."""
    text = str(label).strip()
    text = text[4:] if text.lower().startswith("sub-") else text
    text = re.sub(r"[^A-Za-z0-9]", "", text)
    if not text:
        raise ValueError(f"Not a usable participant ID: {label!r}")
    return f"sub-{text}"


# ── WAB-R ────────────────────────────────────────────────────────────────────

def wab_aq(scores):
    """AQ from the five subtest scores (each 0–10), or None if one is missing."""
    values = [scores.get(name) for name in SUBTESTS]
    if any(v is None for v in values):
        return None
    return round(2 * sum(float(v) for v in values), 1)


#: WAB-R classification criteria: (fluency, comprehension, repetition, naming) ranges, inclusive.
WAB_CRITERIA = (
    ("Global",                ((0, 4), (0, 3.9), (0, 4.9), (0, 6))),
    ("Broca's",               ((0, 4), (4, 10), (0, 7.9), (0, 8))),
    ("Isolation",             ((0, 4), (0, 3.9), (5, 10), (0, 6))),
    ("Transcortical motor",   ((0, 4), (4, 10), (8, 10), (0, 8))),
    ("Wernicke's",            ((5, 10), (0, 6.9), (0, 7.9), (0, 9))),
    ("Transcortical sensory", ((5, 10), (0, 6.9), (8, 10), (0, 9))),
    ("Conduction",            ((5, 10), (7, 10), (0, 6.9), (0, 9))),
    ("Anomic",                ((5, 10), (7, 10), (7, 10), (0, 9))),
)


def suggest_wab_type(scores):
    """The WAB-R type whose criteria the subtest scores meet, or None.

    Uses fluency, comprehension, repetition and naming (and AQ >= 93.8 for no
    aphasia). Scores between two categories' ranges match none. A suggestion
    only: check it against the WAB-R manual for the participant.
    """
    aq = scores.get("wab_aq")
    if aq is None:
        aq = wab_aq(scores)
    if aq is not None and float(aq) >= 93.8:
        return WAB_TYPES[-1]
    values = [scores.get(name) for name in ("wab_fluency", "wab_comprehension", "wab_repetition", "wab_naming")]
    if any(v is None for v in values):
        return None
    for name, ranges in WAB_CRITERIA:
        if all(low <= float(v) <= high for v, (low, high) in zip(values, ranges)):
            return name
    return None


# ── Values and checks ────────────────────────────────────────────────────────

def clean_value(name, value):
    """A cell value in our column's form (number, F/M/other, WAB type label), or None if blank.

    Raises ValueError for a value that does not fit the column.
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip()
    if text == "" or text.lower() in ("n/a", "na", "nan", "none"):
        return None
    column = BY_NAME[name]
    if column.kind == "number":
        try:
            number = float(text)
        except ValueError:
            raise ValueError(f"{column.label}: {text!r} is not a number") from None
        if (column.low is not None and number < column.low) or (column.high is not None and number > column.high):
            raise ValueError(f"{column.label}: {number:g} is outside {column.low:g}–{column.high:g}")
        return int(number) if number.is_integer() and name in ("age_at_stroke", "wab_days") else number
    if name == "sex":
        sex = _SEX.get(text.lower(), "other" if text.lower() == "other" else None)
        if sex is None:
            raise ValueError(f"Sex: {text!r} is not F, M or other")
        return sex
    if name == "wab_type":
        return wab_type_label(text)
    return text


def wab_type_label(text):
    """Our WAB type label for a free-text type (aliases as in aphasia_rules), or ValueError."""
    for label in WAB_TYPES:
        if _key(label) == _key(text):
            return label
    import sys
    kb = Path(__file__).resolve().parents[1] / "aphasia-kb"
    if str(kb) not in sys.path:
        sys.path.insert(0, str(kb))
    import aphasia_rules
    canonical = aphasia_rules.canonical_aphasia_type(text)
    if canonical is None:
        if _key(text) in ("none", "notaphasic", "normal", "wnl", "withinnormallimits", "noaphasia"):
            return WAB_TYPES[-1]
        raise ValueError(f"WAB-R aphasia type: {text!r} is not a WAB-R type ({', '.join(WAB_TYPES)})")
    label = aphasia_rules.APHASIA_LABELS[canonical]
    return "Isolation" if canonical == "mixed_transcortical_aphasia" else label


def check_row(row):
    """(cleaned row, problems, notes) for one participant's values.

    Problems are values that cannot be stored; notes are consistency warnings
    (a given AQ that differs from the subtests by more than 0.5, a type that
    differs from the suggested one). The AQ is filled in from the subtests when blank.
    """
    cleaned, problems, notes = {}, [], []
    for name in BY_NAME:
        if name not in row:
            continue
        try:
            cleaned[name] = clean_value(name, row[name])
        except ValueError as error:
            problems.append(str(error))
    computed = wab_aq(cleaned)
    if computed is not None:
        if cleaned.get("wab_aq") is None:
            cleaned["wab_aq"] = computed
            notes.append(f"WAB-R AQ computed from the subtests: {computed:g}")
        elif abs(float(cleaned["wab_aq"]) - computed) > 0.5:
            notes.append(f"WAB-R AQ {cleaned['wab_aq']:g} differs from the subtests' {computed:g}")
    suggested = suggest_wab_type(cleaned)
    if cleaned.get("wab_type") and suggested and cleaned["wab_type"] != suggested:
        notes.append(f"WAB-R type {cleaned['wab_type']} differs from the criteria's {suggested}")
    return cleaned, problems, notes


# ── participants.tsv ─────────────────────────────────────────────────────────

def read_participants(dataset):
    """The dataset's participants.tsv as strings ('' for blanks), or an empty table."""
    path = Path(dataset) / "participants.tsv"
    if not path.exists():
        return pd.DataFrame(columns=["participant_id"])
    return pd.read_csv(path, sep="\t", dtype=str, keep_default_na=False)


def _atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp",
                                     delete=False, encoding="utf-8") as stream:
        stream.write(text)
        temporary = Path(stream.name)
    os.replace(temporary, path)


def _format(value):
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


def save_participants(dataset, rows):
    """Merge ``{participant_id: {column: value}}`` into participants.tsv and write participants.json.

    Values given replace the stored ones; columns not given, other columns
    (e.g. a site's own) and other participants are kept. Returns the tsv path.
    """
    dataset = Path(dataset)
    table = read_participants(dataset)
    ours = [c.name for c in COLUMNS]
    for column in ["participant_id", *ours]:
        if column not in table:
            table[column] = "n/a"
    for pid, values in rows.items():
        pid = participant_id(pid)
        if pid not in set(table["participant_id"]):
            table.loc[len(table)] = {c: "n/a" for c in table.columns} | {"participant_id": pid}
        index = table.index[table["participant_id"] == pid][0]
        for name, value in values.items():
            if name in BY_NAME:
                table.at[index, name] = _format(value)
    table = table.replace("", "n/a").sort_values("participant_id", kind="stable")
    other = [c for c in table.columns if c not in ("participant_id", *ours)]
    table = table[["participant_id", *ours, *other]]
    path = dataset / "participants.tsv"
    _atomic_write(path, table.to_csv(sep="\t", index=False))
    write_sidecar(dataset)
    return path


def write_sidecar(dataset):
    """participants.json: description (and units / levels) of each of our columns, others kept."""
    path = Path(dataset) / "participants.json"
    sidecar = json.loads(path.read_text()) if path.exists() else {}
    sidecar["participant_id"] = {"Description": "Participant identifier (sub-<label>)."}
    for c in COLUMNS:
        entry = {"LongName": c.label, "Description": c.description}
        if c.units:
            entry["Units"] = c.units
        if c.kind == "choice":
            entry["Levels"] = {v: v for v in c.choices}
        sidecar[c.name] = entry
    _atomic_write(path, json.dumps(sidecar, indent=2, ensure_ascii=False) + "\n")
    return path


def stored_row(dataset, pid):
    """One participant's stored values (None for n/a), {} if not in participants.tsv."""
    table = read_participants(dataset)
    rows = table[table["participant_id"] == participant_id(pid)]
    if rows.empty:
        return {}
    return {k: (None if v in ("", "n/a") else v) for k, v in rows.iloc[0].items()}


# ── Spreadsheet import ───────────────────────────────────────────────────────

def read_spreadsheet(path, sheet=0):
    """A CSV, TSV or Excel sheet as strings."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in (".xlsx", ".xlsm", ".xls"):
        return pd.read_excel(path, sheet_name=sheet, dtype=str)
    return pd.read_csv(path, sep="\t" if suffix == ".tsv" else None, engine="python", dtype=str)


def match_columns(headers, mapping=None):
    """{spreadsheet header: our column} by alias; ``mapping`` overrides or adds pairs."""
    matched = {}
    for header in headers:
        column = _ALIAS_LOOKUP.get(_key(header))
        if column and column not in matched.values():
            matched[header] = column
    for header, column in (mapping or {}).items():
        if column not in ("participant_id", *BY_NAME):
            raise ValueError(f"Unknown column {column!r} for {header!r}")
        matched = {h: c for h, c in matched.items() if c != column}
        matched[header] = column
    return matched


def check_spreadsheet(table, mapping=None):
    """Clean every row: returns (rows {participant_id: values}, report DataFrame, matched columns)."""
    matched = match_columns(table.columns, mapping)
    if "participant_id" not in matched.values():
        raise ValueError(f"No participant ID column among {list(table.columns)}; "
                         "pass mapping={'<header>': 'participant_id'}")
    id_header = next(h for h, c in matched.items() if c == "participant_id")
    rows, report = {}, []
    for number, raw in table.iterrows():
        values = {matched[h]: raw[h] for h in matched if matched[h] != "participant_id"}
        try:
            pid = participant_id(raw[id_header])
        except ValueError as error:
            report.append({"row": number + 2, "participant_id": raw[id_header], "status": "skipped",
                           "details": str(error)})
            continue
        cleaned, problems, notes = check_row(values)
        if problems:
            report.append({"row": number + 2, "participant_id": pid, "status": "skipped",
                           "details": "; ".join(problems)})
            continue
        if pid in rows:
            report.append({"row": number + 2, "participant_id": pid, "status": "skipped",
                           "details": "participant appears twice; the first row is used"})
            continue
        # Blank cells do not erase stored values.
        rows[pid] = {k: v for k, v in cleaned.items() if v is not None}
        report.append({"row": number + 2, "participant_id": pid, "status": "ok", "details": "; ".join(notes)})
    return rows, pd.DataFrame(report, columns=["row", "participant_id", "status", "details"]), matched


def import_spreadsheet(path, dataset, *, mapping=None, sheet=0, dry_run=True):
    """Check a cohort spreadsheet and (unless ``dry_run``) merge it into participants.tsv.

    Returns the per-row report (row number as in the spreadsheet, status ok /
    skipped, details) and prints which columns were matched.
    """
    rows, report, matched = check_spreadsheet(read_spreadsheet(path, sheet), mapping)
    ignored = [h for h in read_spreadsheet(path, sheet).columns if h not in matched]
    print("Matched columns: " + ", ".join(f"{h} → {c}" for h, c in matched.items()))
    if ignored:
        print("Not imported: " + ", ".join(map(str, ignored)) + " (pass mapping={header: column} to map them)")
    if dry_run:
        print(f"Dry run: {len(rows)} participant(s) would be written to {Path(dataset) / 'participants.tsv'}.")
    elif rows:
        print(f"Wrote {len(rows)} participant(s) to {save_participants(dataset, rows)}.")
    return report


# ── Notebook form ────────────────────────────────────────────────────────────

class ParticipantForm:
    """One participant at a time: pick or type an ID, fill the fields, Save.

    Saving writes only that participant's row (others are kept). Values are
    checked on save; the AQ is computed from the subtests when blank and the
    WAB-R type the criteria suggest is shown (*Use suggested type* copies it).
    """

    def __init__(self, dataset, participants=()):
        import ipywidgets as w
        self.dataset = Path(dataset)
        known = sorted(set(participants) | set(read_participants(self.dataset)["participant_id"]))
        self.pid = w.Combobox(options=known, placeholder="sub-01", description="Participant:",
                              ensure_option=False, style={"description_width": "initial"})
        self.fields = {}
        for c in COLUMNS:
            label = c.label + (f" ({c.units})" if c.units else "")
            if c.kind == "choice":
                widget = w.Dropdown(options=[("—", None), *[(v, v) for v in c.choices]], value=None)
            else:
                widget = w.Text(placeholder=("" if c.low is None else f"{c.low:g}–{c.high:g}"))
            widget.description, widget.tooltip = label, c.description
            widget.style = {"description_width": "260px"}
            widget.layout = w.Layout(width="480px")
            self.fields[c.name] = widget
        self.suggestion = w.HTML()
        self.use_suggestion = w.Button(description="Use suggested type", layout=w.Layout(width="180px"))
        self.save = w.Button(description="Save participant", button_style="primary")
        self.message = w.HTML()
        self.pid.observe(self.load, names="value")
        for name in SUBTESTS + ("wab_aq",):
            self.fields[name].observe(self._suggest, names="value")
        self.use_suggestion.on_click(self._apply_suggestion)
        self.save.on_click(lambda _: self.submit())
        self.widget = w.VBox([
            w.HTML(f"<b>Participant data</b> → <code>{escape(str(self.dataset / 'participants.tsv'))}</code>"),
            self.pid, *self.fields.values(), w.HBox([self.suggestion, self.use_suggestion]),
            self.save, self.message])

    def values(self):
        return {name: widget.value for name, widget in self.fields.items()}

    def load(self, *_):
        try:
            stored = stored_row(self.dataset, self.pid.value) if self.pid.value.strip() else {}
        except ValueError as error:
            self.message.value = escape(str(error))
            return
        for name, widget in self.fields.items():
            value = stored.get(name)
            if BY_NAME[name].kind == "choice":
                widget.value = value if value in BY_NAME[name].choices else None
            else:
                widget.value = "" if value is None else str(value)
        self.message.value = "Loaded the saved values." if stored else ""
        self._suggest()

    def _suggest(self, *_):
        cleaned, _, _ = check_row({k: v for k, v in self.values().items() if k in SUBTESTS + ("wab_aq",)})
        self.suggested = suggest_wab_type(cleaned)
        aq = wab_aq(cleaned)
        self.suggestion.value = ((f"Subtest AQ: <b>{aq:g}</b> · " if aq is not None else "")
                                 + (f"WAB-R criteria suggest: <b>{escape(self.suggested)}</b>"
                                    if self.suggested else "Enter fluency, comprehension, repetition and "
                                                           "naming for a suggested type."))
        self.use_suggestion.disabled = self.suggested is None

    def _apply_suggestion(self, *_):
        if self.suggested:
            self.fields["wab_type"].value = self.suggested

    def submit(self):
        """Check and save; returns True when the row was written."""
        try:
            pid = participant_id(self.pid.value)
        except ValueError as error:
            self.message.value = f"<span style='color:#a00'>{escape(str(error))}</span>"
            return False
        cleaned, problems, notes = check_row(self.values())
        if problems:
            self.message.value = "<span style='color:#a00'>Not saved: " + escape("; ".join(problems)) + "</span>"
            return False
        path = save_participants(self.dataset, {pid: cleaned})
        if cleaned.get("wab_aq") is not None:
            self.fields["wab_aq"].value = f"{cleaned['wab_aq']:g}"
        self.message.value = (f"Saved <b>{escape(pid)}</b> to <code>{escape(str(path))}</code>."
                              + "".join(f"<br>⚠ {escape(n)}" for n in notes))
        if pid not in self.pid.options:
            self.pid.options = sorted({*self.pid.options, pid})
        return True


def show_participant_form(dataset, participants=()):
    from IPython.display import display
    form = ParticipantForm(dataset, participants)
    display(form.widget)
    return form
