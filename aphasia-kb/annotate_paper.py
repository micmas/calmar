"""
annotate_paper.py — produce a color-highlighted version of a paper's
PDF using the verbatim quotes recorded in a draft KB entry's
`source_passages`.

The user's verification mechanism: open the annotated PDF and the draft
side-by-side. Each color matches a finding-aspect (claim, sample,
statistics, etc.) so they can see at a glance:

  - whether each highlighted sentence is the *right* one for that aspect
  - whether anything important is *un*-highlighted (i.e., missed)

Usage
-----
    # Single draft:
    python annotate_paper.py \
        --pdf   papers/Fridriksson2018.pdf \
        --draft drafts/regions/ho-cort_44__Fridriksson2018.md

    # Multiple drafts from one paper (multi-bucket case):
    python annotate_paper.py \
        --pdf   papers/Fridriksson2018.pdf \
        --draft drafts/regions/ho-cort_44__Fridriksson2018.md \
                drafts/therapies/mit__Fridriksson2018.md

Writes:
    papers/Fridriksson2018_annotated.pdf

Optional:
    --out PATH        explicit output path
    --no-legend       skip the color-legend page
    --fail-on-missing exit non-zero if any quote couldn't be located

Color scheme is the single source of truth in `aphasia_kb.SUPPORTS_COLORS`.

Dependencies
------------
    pip install pymupdf pyyaml

(PyMuPDF / fitz is the only way to add highlight annotations to a PDF
from Python without rasterizing.)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Re-use vocab + colors from the loader so the two stay in sync
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from aphasia_kb import (
    parse_markdown,
    SUPPORTS_VOCAB,
    SUPPORTS_COLORS,
)


# ============================================================
# Quote-finding heuristics
# ============================================================
def _hex_to_rgb01(hex_color: str) -> tuple[float, float, float]:
    """'#a8c8ff' -> (0.658, 0.784, 1.0). PyMuPDF wants 0..1 floats."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))


import re

# Translation table: Unicode variants -> ASCII. The single biggest
# source of "quote not found" misses is hyphen / smart-quote / ligature
# differences between what the agent wrote and what the PDF contains.
_UNICODE_NORM = str.maketrans({
    "\u2010": "-", "\u2011": "-", "\u2012": "-",
    "\u2013": "-", "\u2014": "-", "\u2015": "-", "\u2212": "-",
    "\u2018": "'", "\u2019": "'", "\u201A": "'", "\u201B": "'",
    "\u201C": '"', "\u201D": '"', "\u201E": '"', "\u201F": '"',
    "\u00B4": "'", "\u02B9": "'",
    "\u00A0": " ", "\u2009": " ", "\u200A": " ", "\u202F": " ",
    "\u200B": "",
    "\u2026": "...",
})

_LIGATURES = {
    "\uFB00": "ff", "\uFB01": "fi", "\uFB02": "fl",
    "\uFB03": "ffi", "\uFB04": "ffl", "\uFB05": "st", "\uFB06": "st",
}

# Reverse map: ASCII pairs \u2192 Unicode ligature, for re-ligaturizing
# normalized quotes so they match PDFs that store ligature characters.
_ASCII_TO_LIGATURES = {v: k for k, v in _LIGATURES.items() if len(v) <= 3}
# Longest first to avoid partial replacements (ffi before fi)
_ASCII_TO_LIGATURES_SORTED = sorted(
    _ASCII_TO_LIGATURES.items(), key=lambda x: -len(x[0])
)


def _ligaturize(s: str) -> str:
    """Convert ASCII ligature pairs back to Unicode ligature characters.
    Used to produce a search candidate that matches PDFs which store
    ligatures as single Unicode code points (U+FB00\u2013U+FB06)."""
    for ascii_seq, lig in _ASCII_TO_LIGATURES_SORTED:
        s = s.replace(ascii_seq, lig)
    return s


def _normalize(s: str) -> str:
    """Aggressive normalization: Unicode -> ASCII, ligatures expanded,
    elision markers stripped, soft hyphens joined, whitespace collapsed.

    Soft-hyphen handling (two passes, applied symmetrically to both PDF
    text and quotes so they compare correctly):
      1. (\w)-\s+(\w)  \u2014 hyphen at end of line followed by whitespace:
         the hyphen is a line-break artefact; join the syllables with no
         separator (e.g. "corre-\nsponding" -> "corresponding",
         "Harvard-\nOxford" -> "HarvardOxford").
      2. (\w)-(\w)     \u2014 remaining mid-word hyphens in compound words:
         also stripped so that a quote written as "Harvard-Oxford" still
         matches "HarvardOxford" after pass 1 above.
    Both transformations are applied to every string, so the comparison
    is symmetric even though it loses the hyphen.
    """
    s = s.translate(_UNICODE_NORM)
    for lig, repl in _LIGATURES.items():
        if lig in s:
            s = s.replace(lig, repl)
    s = re.sub(r"\s*\[\s*(?:\.\.\.|\u2026)\s*\]\s*", " ", s)
    # Pass 1: soft hyphen \u2014 line-break artefact (hyphen + whitespace between
    # word chars).  Join without any separator.
    s = re.sub(r"(\w)-\s+(\w)", r"\1\2", s)
    # Pass 2: remaining intra-word hyphens (compound words, acronyms) \u2014 strip
    # the hyphen so both sides normalise identically.
    s = re.sub(r"(\w)-(\w)", r"\1\2", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def _find_quote_rects(page, quote: str):
    """Try several normalizations + fallbacks; return (rects, label) or
    ([], None) if nothing matched.

    Strategy, in order:
      1. Exact raw quote.
      2. Whitespace-collapsed only.
      3. Full Unicode-normalized quote.
      4. Normalized, parenthetical asides removed.
      5. First sentence only.
      6. Head of quote (first 120 chars, then 8/6/4 words).
      7. Last resort: confirm normalized quote IS in normalized page
         text, then search for progressively shorter prefixes.
    """
    raw = quote.strip()
    if not raw:
        return [], None

    candidates = []
    seen = set()

    def _add(label, text):
        text = (text or "").strip()
        if text and text not in seen:
            seen.add(text)
            candidates.append((label, text))

    _add("raw", raw)
    _add("ws", re.sub(r"\s+", " ", raw))
    norm = _normalize(raw)
    _add("norm", norm)
    # Also try with ASCII ligature pairs converted back to Unicode ligature
    # characters — needed for PDFs that store ﬁ/ﬂ/ﬀ as single code points.
    _add("lig", _ligaturize(norm))
    _add("no-parens", re.sub(r"\s*\([^)]*\)", "", norm))
    _add("no-parens-lig", _ligaturize(re.sub(r"\s*\([^)]*\)", "", norm)))
    first_sent = re.split(r"[.?!](?:\s|$)", norm, maxsplit=1)[0]
    if len(first_sent) >= 25:
        _add("first-sent", first_sent)
        _add("first-sent-lig", _ligaturize(first_sent))
    if len(norm) > 120:
        _add("head120", norm[:120])
        _add("head120-lig", _ligaturize(norm[:120]))
    words = norm.split()
    for n in (8, 6, 4):
        if len(words) > n:
            _add(f"head{n}w", " ".join(words[:n]))
            _add(f"head{n}w-lig", _ligaturize(" ".join(words[:n])))

    for label, cand in candidates:
        try:
            rects = page.search_for(cand, quads=False)
        except Exception:
            rects = []
        if rects:
            return rects, f"{label}: {cand[:60]}"

    # Last resort: the normalized quote is in the normalized page text,
    # so the *content* is right. Fall back to progressively shorter
    # prefixes hoping one survives PyMuPDF's tokenization.
    try:
        page_norm = _normalize(page.get_text())
    except Exception:
        page_norm = ""
    if norm and page_norm and norm[:60] in page_norm:
        for end in range(min(len(norm), 100), 25, -8):
            chunk = norm[:end]
            for search_text in (chunk, _ligaturize(chunk)):
                try:
                    rects = page.search_for(search_text, quads=False)
                except Exception:
                    rects = []
                if rects:
                    return rects, f"fallback-{end}: {search_text[:60]}"

    return [], None


# ============================================================
# Main
# ============================================================
def annotate(
    draft_paths,                       # Path | list[Path]
    pdf_path: Path,
    out_path: Path | None = None,
    *,
    add_legend: bool = True,
    fail_on_missing: bool = False,
) -> dict:
    """Annotate `pdf_path` based on the union of source_passages from
    one or more draft files.

    `draft_paths` may be a single Path (single-draft, original API) or
    a list of Paths (multi-draft, e.g., region + therapy drafts from
    the same paper)."""
    try:
        import fitz  # PyMuPDF
    except ImportError as e:
        raise SystemExit(
            "PyMuPDF is required. Install with:\n"
            "    pip install pymupdf"
        ) from e

    # Normalize draft_paths to a list
    if isinstance(draft_paths, (str, Path)):
        draft_paths = [Path(draft_paths)]
    else:
        draft_paths = [Path(p) for p in draft_paths]

    # Collect all source_passages from all drafts. The finding_id we
    # pass into the legend prefixes the source draft so the user can
    # tell which draft a highlight came from.
    all_passages = []      # list of (display_id, passage_dict)
    for dp in draft_paths:
        fm, _ = parse_markdown(dp)
        if not fm:
            raise SystemExit(f"No frontmatter in draft: {dp}")
        findings = fm.get("findings") or []
        if not findings:
            print(f"  ⚠ {dp.name}: no findings — skipped")
            continue
        # Use draft basename minus .md as a short prefix
        prefix = dp.stem
        for f in findings:
            fid = f.get("id", "?")
            for p in (f.get("source_passages") or []):
                all_passages.append((f"{prefix}:{fid}", p))

    if not all_passages:
        raise SystemExit("No source_passages in any draft.")

    # Open the PDF
    doc = fitz.open(str(pdf_path))

    # Output path: <pdf_stem>_annotated.pdf next to the source
    if out_path is None:
        out_path = pdf_path.with_name(f"{pdf_path.stem}_annotated.pdf")

    # Pre-compute text per page once (for fallback search)
    n_pages = doc.page_count

    summary = {"placed": [], "missed": []}

    for fid, passage in all_passages:
        supports = passage.get("supports", "claim")
        if supports not in SUPPORTS_VOCAB:
            print(f"  ⚠ {fid}: unknown supports={supports!r} — using grey")
            color = (0.7, 0.7, 0.7)
        else:
            color = _hex_to_rgb01(SUPPORTS_COLORS[supports])

        quote = (passage.get("quote") or "").strip()
        if not quote or quote.startswith("[PLACEHOLDER"):
            print(f"  ⚠ {fid} ({supports}): quote is empty/placeholder — skipped")
            summary["missed"].append({
                "finding": fid, "supports": supports,
                "reason": "placeholder/empty quote",
                "section": passage.get("section"),
            })
            continue

        # Search across all pages (start with the hinted page if any)
        hinted_page = passage.get("page")
        page_order = list(range(n_pages))
        if isinstance(hinted_page, int) and 0 <= hinted_page - 1 < n_pages:
            # Convert 1-based page label to 0-based index, prioritize it
            zero_based = hinted_page - 1
            page_order = [zero_based] + [p for p in page_order if p != zero_based]

        placed = False
        for pno in page_order:
            page = doc[pno]
            rects, matched = _find_quote_rects(page, quote)
            if not rects:
                continue
            for rect in rects:
                annot = page.add_highlight_annot(rect)
                annot.set_colors(stroke=color)
                annot.set_info(
                    title=f"[{fid}] {supports}",
                    content=quote[:200] + ("…" if len(quote) > 200 else ""),
                )
                annot.update()
            summary["placed"].append({
                "finding": fid, "supports": supports,
                "page": pno + 1, "n_rects": len(rects),
                "matched_form": matched[:60] + ("…" if len(matched or "") > 60 else ""),
            })
            placed = True
            break
        if not placed:
            print(f"  ⚠ {fid} ({supports}, page hint {hinted_page}): "
                  f"quote not found in PDF")
            summary["missed"].append({
                "finding": fid, "supports": supports,
                "reason": "quote not located in PDF",
                "section": passage.get("section"),
                "page_hint": hinted_page,
                "quote_preview": quote[:80] + ("…" if len(quote) > 80 else ""),
            })

    # Add a legend page
    if add_legend:
        page = doc.new_page()
        text = "Color legend\n" + "=" * 40 + "\n\n"
        for sup in sorted(SUPPORTS_VOCAB):
            text += f"  {sup:20s}  {SUPPORTS_COLORS[sup]}\n"
        text += "\n\nGenerated by aphasia-kb/annotate_paper.py"
        page.insert_text((50, 50), text, fontsize=11)
        # Also draw small color rectangles next to each line
        y = 50 + 40    # roughly where the first entry starts
        for sup in sorted(SUPPORTS_VOCAB):
            r = fitz.Rect(280, y, 320, y + 12)
            page.draw_rect(r, color=(0.2, 0.2, 0.2),
                           fill=_hex_to_rgb01(SUPPORTS_COLORS[sup]),
                           width=0.5)
            y += 13.7    # matches insert_text default leading

    doc.save(str(out_path))
    doc.close()

    # Report
    print(f"\n✓ Annotated PDF: {out_path}")
    print(f"  Placed: {len(summary['placed'])} highlight(s)")
    print(f"  Missed: {len(summary['missed'])} passage(s)")
    if summary["missed"] and fail_on_missing:
        sys.exit(2)

    return summary


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--draft", required=True, type=Path, nargs="+",
                   help="One or more draft KB entry markdown files. "
                        "All passages from all drafts are highlighted "
                        "on the same PDF.")
    p.add_argument("--pdf", required=True, type=Path,
                   help="Source paper PDF.")
    p.add_argument("--out", type=Path, default=None,
                   help="Output PDF path (default: <pdf>_annotated.pdf).")
    p.add_argument("--no-legend", action="store_true",
                   help="Skip the color-legend page.")
    p.add_argument("--fail-on-missing", action="store_true",
                   help="Exit non-zero if any quote couldn't be located.")
    args = p.parse_args(argv)

    for d in args.draft:
        if not d.exists():
            p.error(f"draft not found: {d}")
    if not args.pdf.exists():
        p.error(f"pdf not found: {args.pdf}")

    annotate(args.draft, args.pdf, args.out,
             add_legend=not args.no_legend,
             fail_on_missing=args.fail_on_missing)


if __name__ == "__main__":
    main()
