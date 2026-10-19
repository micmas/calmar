"""
quote_check.py — the ONE place that decides whether a `source_passages`
quote is in a paper.

`auto_review.py` (drafts), `compare_extraction.py` (model benchmarks)
and `audit_quotes.py` (the canonical KB) all grade quotes against the
PDF text layer. Until v2.5 each had its own matcher and they disagreed:
a quote the audit called "elided" the benchmark called "absent". They
now share this module, so a quote gets the same grade everywhere.

Grades, best to worst
---------------------
    exact     verbatim in the text layer (modulo the shared normaliser:
              ligatures, soft hyphens, smart quotes, whitespace, case)
    elided    contains `[...]` / `…` / `...` and every fragment (>= 20
              chars) is exact. A faithful quote with a clause skipped.
    table     exact once `|` separators are treated as whitespace —
              table cells quoted in row form. The text layer puts each
              cell on its own line, so this IS verbatim content; it is
              graded separately because the annotator cannot highlight
              it as one span and the extractor is asked for prose.
    anchored  the first ANCHOR characters match, then the quote and the
              text layer diverge — almost always a glyph the PDF font
              encodes oddly (`<` as `5`, `=` as `¼`, `×` dropped) that
              the writer silently corrected. Real, not verbatim.
    near      not verbatim, but a passage >= NEAR_RATIO similar sits at
              the anchored location, or the quote matches with all
              whitespace removed. A paraphrase or a lost space.
    absent    nothing similar anywhere. The fabrication signal.

`FOUND = {exact, elided, table}` is what `auto_review` counts as a
located quote; Tier A additionally requires every quote to be FOUND
(GOVERNANCE.md §3). `anchored` and `near` are for a person to confirm.

Usage
-----
    from quote_check import PaperText, grade_quote, FOUND
    paper = PaperText.from_pdf(Path("papers/Foo2024.pdf"))
    grade_quote(quote, paper)          # -> "exact" | ... | "absent"
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from pathlib import Path

try:
    from annotate_paper import _normalize
except Exception:  # pragma: no cover — annotate_paper imports pymupdf lazily
    def _normalize(s: str) -> str:  # type: ignore[misc]
        return re.sub(r"\s+", " ", s).strip()

GRADES = ("exact", "elided", "table", "anchored", "near", "absent")
FOUND = frozenset({"exact", "elided", "table"})
ANCHOR = 60          # chars that must match to call a quote "anchored"
NEAR_RATIO = 0.82    # similarity to call a non-verbatim quote "near"
MIN_FRAGMENT = 20    # shortest elision fragment that counts

_ELISION = re.compile(r"\[\s*(?:\.\.\.|…)\s*\]|…|\.\.\.")
_PIPE = re.compile(r"\s*\|\s*")


def read_pdf_text(path: Path) -> str:
    """Raw text layer of a PDF (or a .txt stand-in)."""
    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")
    try:
        import pymupdf as fitz  # PyMuPDF >= 1.24
    except ImportError:  # pragma: no cover
        import fitz  # older PyMuPDF
    doc = fitz.open(str(path))
    try:
        return "\n".join(page.get_text() for page in doc)
    finally:
        doc.close()


def _norm(s: str) -> str:
    return _normalize(s).casefold()


@dataclass
class PaperText:
    """A paper's text layer in the forms the grader needs, built once."""
    norm: str            # normalised, casefolded
    nospace: str         # the same with all whitespace removed

    @classmethod
    def from_text(cls, raw: str) -> "PaperText":
        n = _norm(raw)
        return cls(norm=n, nospace=re.sub(r"\s+", "", n))

    @classmethod
    def from_pdf(cls, path: Path) -> "PaperText":
        return cls.from_text(read_pdf_text(path))


def find_paper(citation: str, papers_dir: Path) -> Path | None:
    """papers/<Key>.pdf or .txt for a citation key, or None."""
    key = (citation or "").lstrip("@")
    if not key:
        return None
    for ext in (".pdf", ".txt"):
        p = papers_dir / f"{key}{ext}"
        if p.exists():
            return p
    return None


def grade_quote(quote: str, paper: PaperText) -> str:
    """Grade one quote against a paper. See module docstring."""
    raw = (quote or "").strip()
    if not raw:
        return "absent"
    q = _norm(raw)
    text = paper.norm
    if q in text:
        return "exact"

    # Elision: split the RAW quote (the normaliser strips the markers)
    if _ELISION.search(raw):
        parts = [_norm(p).strip() for p in _ELISION.split(raw)]
        parts = [p for p in parts if len(p) >= MIN_FRAGMENT]
        if len(parts) >= 2 and all(p in text for p in parts):
            return "elided"

    # Table row: cells joined with "|"; the text layer has them on lines
    if "|" in raw:
        cells = [_norm(c).strip() for c in _PIPE.split(raw)]
        cells = [c for c in cells if c]
        joined = " ".join(cells)
        if len(cells) >= 2 and (joined in text or
                                re.sub(r"\s+", "", joined) in paper.nospace):
            return "table"

    if len(q) > ANCHOR and q[:ANCHOR] in text:
        return "anchored"

    if len(q) >= MIN_FRAGMENT and re.sub(r"\s+", "", q) in paper.nospace:
        return "near"

    words = q.split()
    if len(words) >= 5:
        for start in (0, 3, len(words) // 2):
            anchor = " ".join(words[start:start + 4])
            if len(anchor) < 8:
                continue
            idx = text.find(anchor)
            if idx < 0:
                continue
            lo = max(0, idx - start * 8)
            window = text[lo:lo + len(q) + 60]
            if difflib.SequenceMatcher(None, q, window[:len(q)]).ratio() >= NEAR_RATIO:
                return "near"
    return "absent"


def grade_finding(finding: dict, paper: PaperText) -> list[tuple[dict, str]]:
    """[(source_passage, grade), ...] for every non-empty quote."""
    out = []
    for sp in finding.get("source_passages") or []:
        if (sp.get("quote") or "").strip():
            out.append((sp, grade_quote(sp["quote"], paper)))
    return out
