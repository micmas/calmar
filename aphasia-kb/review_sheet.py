#!/usr/bin/env python3
"""
review_sheet.py — one HTML page per draft that shows every quote where
it sits in the paper, so a reviewer reads the evidence without opening
the PDF.

    python review_sheet.py --draft drafts/therapies/semantic_feature_analysis__Boyle2004.md
    python review_sheet.py --all                 # every draft in drafts/
    python review_sheet.py --all --fix-pages     # also correct `page:` in the drafts

For each finding the sheet lists the claim, relationship, strength and
confidence, then each source passage with:
  * its grade from quote_check.py (exact / elided / table / anchored /
    near / absent) — the same grade auto_review.py uses;
  * the page it was FOUND on (and the page the extractor claimed, when
    they differ);
  * a crop of that page with the passage highlighted.

Sheets go to drafts/_review/<draft-stem>.html, one self-contained file
each (images inline). They contain page images of copyrighted papers,
so drafts/_review/ is git-ignored like papers/.

--fix-pages rewrites each draft's `source_passages[].page` to the page
the quote was actually found on. Page numbers from the model are often
off by one or more; the annotator only uses them as a hint, but the
reviewer and the per-finding `review` block are better served by the
real ones. Only drafts are rewritten, never canonical entries.
"""
from __future__ import annotations

import argparse
import base64
import html
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from annotate_paper import _find_quote_rects  # noqa: E402
from aphasia_kb import parse_markdown  # noqa: E402
from quote_check import PaperText, find_paper, grade_quote  # noqa: E402
from phase import PHASE_VOCAB, finding_phase, infer_phase  # noqa: E402

OUT_DIR = ROOT / "drafts" / "_review"
DPI = 110
MARGIN_PT = 28          # context above / below the highlighted lines

# CALMaR palette (docs/CALMAR_PALETTE.md)
GRAPE, BLUE, CYAN_INK, GREY, PINK = "#52489c", "#4062bb", "#1f7f7f", "#ebebeb", "#f45b69"
GRADE_COLOUR = {"exact": CYAN_INK, "elided": CYAN_INK, "table": CYAN_INK,
                "anchored": BLUE, "near": BLUE, "absent": PINK, "no_pdf": PINK}


def _open(path: Path):
    try:
        import pymupdf as fitz
    except ImportError:  # pragma: no cover
        import fitz
    return fitz.open(str(path))


def locate(doc, quote: str, hint_page) -> tuple[int | None, list]:
    """(0-based page index, rects) of the first page where the quote is
    found, trying the hinted page first."""
    order = list(range(doc.page_count))
    if isinstance(hint_page, int) and 0 <= hint_page - 1 < doc.page_count:
        order = [hint_page - 1] + [p for p in order if p != hint_page - 1]
    for pno in order:
        rects, _ = _find_quote_rects(doc[pno], quote)
        if rects:
            return pno, rects
    return None, []


def crop_png(doc, pno: int, rects, colour=(0.95, 0.85, 0.35)) -> str:
    """Base64 PNG of the page region around rects, highlighted."""
    page = doc[pno]
    union = rects[0]
    for r in rects[1:]:
        union |= r
    for r in rects:
        a = page.add_highlight_annot(r)
        a.set_colors(stroke=colour)
        a.update()
    clip = page.rect
    clip.y0 = max(page.rect.y0, union.y0 - MARGIN_PT)
    clip.y1 = min(page.rect.y1, union.y1 + MARGIN_PT)
    pix = page.get_pixmap(dpi=DPI, clip=clip)
    return base64.b64encode(pix.tobytes("png")).decode("ascii")


def build_sheet(draft: Path, papers_dir: Path, fix_pages: bool,
                out_dir: Path = OUT_DIR, fill_phase: bool = False) -> tuple[Path | None, dict]:
    fm, body = parse_markdown(draft)
    if not fm:
        return None, {"error": "no frontmatter"}
    findings = [f for f in fm.get("findings") or [] if isinstance(f, dict)]
    cite = next((str(f.get("citation")) for f in findings if f.get("citation")), "")
    pdf = find_paper(cite, papers_dir)
    if pdf is None or pdf.suffix.lower() != ".pdf":
        return None, {"error": f"no PDF for {cite or '(no citation)'}"}
    paper = PaperText.from_pdf(pdf)
    doc = _open(pdf)
    counts: dict[str, int] = {}
    changed = 0
    changed_phase = 0
    parts: list[str] = []

    for f in findings:
        fid = f.get("id", "?")
        ph, ph_src = finding_phase(f)
        if fill_phase and ph_src != "stated" and isinstance(f.get("sample"), dict):
            f["sample"]["phase"] = ph
            changed_phase += 1
        tpo = (f.get("sample") or {}).get("time_post_onset")
        ph_txt = (f"phase {html.escape(ph)}" + (" (inferred)" if ph_src == "inferred" else "")
                  + (f" — <i>{html.escape(str(tpo))}</i>" if tpo else ""))
        parts.append(f"<section class='finding'><h2>{html.escape(str(fid))} · "
                     f"{html.escape(str(f.get('target', '')))} "
                     f"<span class='meta'>{html.escape(str(f.get('relationship', '')))} · "
                     f"{html.escape(str(f.get('strength', '')))} · "
                     f"confidence {html.escape(str((f.get('provenance') or {}).get('confidence', '')))}"
                     f" · {ph_txt}</span></h2>"
                     f"<p class='claim'>{html.escape(str(f.get('claim', '')).strip())}</p>")
        stats = f.get("statistics") or f.get("stats")
        if stats:
            parts.append("<pre class='stats'>" + html.escape(
                yaml.safe_dump(stats, sort_keys=False, allow_unicode=True).strip()) + "</pre>")
        for sp in f.get("source_passages") or []:
            quote = (sp.get("quote") or "").strip()
            if not quote:
                continue
            grade = grade_quote(quote, paper)
            counts[grade] = counts.get(grade, 0) + 1
            claimed = sp.get("page")
            pno, rects = locate(doc, quote, claimed)
            found = pno + 1 if pno is not None else None
            if fix_pages and found and found != claimed:
                sp["page"] = found
                changed += 1
            where = (f"p.{found}" if found else "not located in PDF")
            if found and claimed and found != claimed:
                where += f" <span class='was'>(extractor said p.{claimed})</span>"
            elif not found and claimed:
                where += f" <span class='was'>(extractor said p.{claimed})</span>"
            colour = GRADE_COLOUR.get(grade, GREY)
            parts.append(
                f"<div class='passage'><div class='tags'>"
                f"<span class='tag' style='background:{colour}'>{grade}</span>"
                f"<span class='tag grey'>{html.escape(str(sp.get('supports', '')))}</span>"
                f"<span class='where'>{where}</span></div>"
                f"<blockquote>{html.escape(quote)}</blockquote>")
            if rects:
                parts.append(f"<img src='data:image/png;base64,{crop_png(doc, pno, rects)}' "
                             f"alt='page {found}'>")
            parts.append("</div>")
        parts.append("</section>")
    doc.close()

    if (fix_pages and changed) or (fill_phase and changed_phase):
        fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=100)
        out = f"---\n{fm_text.rstrip()}\n---\n"
        if body.strip():
            out += body if body.endswith("\n") else body + "\n"
        draft.write_text(out, encoding="utf-8")

    total = sum(counts.values())
    verified = sum(counts.get(g, 0) for g in ("exact", "elided", "table"))
    summary = " · ".join(f"{g} {n}" for g, n in sorted(counts.items(), key=lambda x: -x[1]))
    head = (f"<h1>{html.escape(fm.get('id', draft.stem))}</h1>"
            f"<p class='sub'>{html.escape(str(fm.get('name', '')))}<br>"
            f"{html.escape(cite)} · {html.escape(pdf.name)} · {len(findings)} finding(s) · "
            f"{total} passage(s): <b>{verified} verified</b> ({summary})"
            + (f" · <b>{changed} page number(s) corrected</b>" if changed else "")
            + (f" · <b>{changed_phase} phase value(s) written</b>" if changed_phase else "")
            + "</p>")
    page = _HTML.replace("{{title}}", html.escape(fm.get("id", draft.stem))) \
                .replace("{{body}}", head + "".join(parts))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{draft.stem}.html"
    out_path.write_text(page, encoding="utf-8")
    return out_path, {"passages": total, "verified": verified, "counts": counts,
                      "fixed": changed, "phased": changed_phase}


_HTML = """<!doctype html><html><head><meta charset="utf-8">
<title>{{title}} — review sheet</title>
<style>
body{font:15px/1.45 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#222;max-width:900px;margin:32px auto;padding:0 16px}
h1{color:#52489c;margin:0 0 4px} .sub{color:#555;margin:0 0 24px}
h2{font-size:17px;color:#4062bb;border-top:2px solid #ebebeb;padding-top:14px;margin:28px 0 6px}
h2 .meta{font-weight:normal;color:#777;font-size:13px;margin-left:8px}
.claim{margin:0 0 8px} .stats{background:#f6f6f6;padding:8px;font-size:12px;overflow:auto}
.passage{margin:14px 0 20px;padding-left:12px;border-left:3px solid #ebebeb}
.tags{font-size:12px;margin-bottom:4px}
.tag{display:inline-block;color:#fff;border-radius:3px;padding:1px 7px;margin-right:6px}
.tag.grey{background:#999} .where{color:#555} .was{color:#f45b69}
blockquote{margin:4px 0 8px;color:#333;font-style:italic}
img{max-width:100%;border:1px solid #ddd;display:block}
</style></head><body>{{body}}</body></html>"""


def _cli(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--draft", type=Path, action="append", help="draft file (repeatable)")
    ap.add_argument("--all", action="store_true", help="every draft under drafts/")
    ap.add_argument("--papers-dir", type=Path, default=ROOT / "papers")
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR)
    ap.add_argument("--fix-pages", action="store_true",
                    help="rewrite source_passages[].page to the page the quote was found on")
    ap.add_argument("--fill-phase", action="store_true",
                    help="write sample.phase (v2.6) into drafts that lack it, inferred from time_post_onset")
    args = ap.parse_args(argv)

    drafts = list(args.draft or [])
    if args.all:
        drafts += sorted(p for p in (ROOT / "drafts").rglob("*.md")
                         if "_review" not in p.parts)
    if not drafts:
        ap.error("pass --draft FILE or --all")

    rc = 0
    for d in drafts:
        out, info = build_sheet(d, args.papers_dir, args.fix_pages, args.out_dir, args.fill_phase)
        if out is None:
            print(f"  ✗ {d.name}: {info['error']}")
            rc = 1
            continue
        shown = out.relative_to(ROOT) if out.is_relative_to(ROOT) else out
        print(f"  ✓ {shown}  {info['verified']}/{info['passages']} verified"
              + (f", {info['fixed']} page(s) fixed" if info["fixed"] else "")
              + (f", {info['phased']} phase(s) written" if info["phased"] else ""))
    return rc


if __name__ == "__main__":
    sys.exit(_cli())
