"""Report sections that show the evidence itself, with its direction.

Two sections of the participant report:

* ``location_section``: lesion location. One row per damaged knowledge-base
  region (how much is damaged, on which side) with the findings about it:
  what damage there was associated with, in which direction, by which study
  and method. A summary of the impairments this points to comes first, built
  from the same rows, so every impairment can be traced to a region.
* ``measures_section``: the participant's measures (lesion volume, WAB-AQ,
  age, ...). One row per measure: its value, the direction the evidence gives
  for it (e.g. "larger lesions: more severe aphasia"), the individual claims,
  and cautions such as a score measured years after the stroke being compared
  with findings about initial severity.

A predictor finding marked "likely" in the KB means "an association was found",
not "this outcome is likely"; these sections never show it as a prediction.
"""
from html import escape
from pathlib import Path
import re

import pandas as pd

DIRECTION_TEXT = {"likely": "association", "likely_responder": "association",
                  "unlikely": "inverse association", "unlikely_responder": "inverse association",
                  "no_effect": "no association", "mixed": "mixed results"}
# Kertesz's WAB-AQ severity bands (a common convention; < 93.8 = aphasia).
WAB_BANDS = ((25, "very severe"), (50, "severe"), (75, "moderate"), (93.7, "mild"), (100, "within normal limits"))
EARLY = r"(?i)\b(?:initial|acute|admission|baseline|early|first (?:week|month)|subacute|onset)\b"
# A damaged region whose findings come from this many studies or fewer is marked
# as resting on thin evidence (see aphasia-kb/atlas_mapping/EVIDENCE_GAPS.md).
THIN_STUDIES = 2
ABBREVIATIONS = {"ifg", "stg", "mtg", "itg", "smg", "slf", "ilf", "ifof", "dlpfc", "sma", "ba"}


def _name(kb, rid):
    """Readable name of a KB id; ids without an entry are prettified."""
    name = kb.label_for(rid) if rid else rid
    if name == rid:
        words = re.sub(r"__.*$", "", str(rid)).split("_")
        name = " ".join(w.upper() if w in ABBREVIATIONS else w for w in words)
    return name[:1].upper() + name[1:]


def _anatomy_key(region):
    """Regions mapped to the same units and side are the same anatomy (KB synonyms)."""
    import atlas_mapping
    _, mapped, _ = atlas_mapping.load()
    r = mapped.get(region)
    return (tuple(sorted(r["units"])), r["side"]) if r else (region,)


def _present(value):
    """True for a useful scalar/list/dict value, without pandas' ambiguous truth rules."""
    if value is None:
        return False
    if isinstance(value, (list, tuple, set, dict, str)):
        return bool(value)
    if pd.api.types.is_scalar(value):
        try:
            return not bool(pd.isna(value))
        except TypeError:
            return True
    return True


def _first(*values, default=None):
    """First present value, including fallbacks after pandas missing scalars."""
    return next((value for value in values if _present(value)), default)


def _text(value):
    """Deterministic, readable text for a nested KB value."""
    if not _present(value):
        return ""
    if isinstance(value, dict):
        return "; ".join(f"{str(k).replace('_', ' ')}: {_text(v)}" for k, v in value.items() if _present(v))
    if isinstance(value, (list, tuple, set)):
        return "; ".join(_text(v) for v in value if _present(v))
    return str(value)


def _evidence_context(kb):
    """Raw findings and bibliography records needed only for report disclosure panels."""
    cached = getattr(kb, "_report_evidence_context", None)
    if cached is not None:
        return cached
    raw = {}
    by_id = {}
    for table in (kb.regions, kb.impairments, kb.therapies, kb.predictors):
        if table is None or table.empty:
            continue
        for _, entry in table.iterrows():
            for finding in _first(entry.get("findings"), default=[]):
                item = dict(finding)
                item["_source_status"] = entry.get("status")
                item["_entry_reviewer"] = entry.get("reviewer")
                item["_entry_review_tier"] = entry.get("review_tier")
                key = (str(entry.get("_path") or ""), finding.get("id"))
                raw[key] = item
                by_id.setdefault((entry.get("id"), finding.get("id")), []).append(item)

    flat = {}
    if kb.findings is not None and not kb.findings.empty:
        for _, finding in kb.findings.iterrows():
            source_path = str(_first(finding.get("source_path"), default=""))
            flat[(source_path, finding.get("id"))] = finding.to_dict()

    citations = {}
    path = Path(kb.root) / "citations.md"
    if path.exists():
        for block in re.split(r"^## (?=@)", path.read_text(encoding="utf-8"), flags=re.M)[1:]:
            heading, _, body = block.partition("\n")
            key = heading.split()[0]
            lines = []
            for line in body.splitlines():
                line = line.strip()
                if line.startswith((">", "#", "---")):
                    if lines:
                        break
                    continue
                if line:
                    lines.append(re.sub(r"\*([^*]+)\*", r"\1", line))
            citations[key] = " ".join(lines)
    context = {"raw": raw, "flat": flat, "by_id": by_id, "citations": citations}
    setattr(kb, "_report_evidence_context", context)
    return context


def _citation_details(citation, context):
    citation = str(citation or "")
    full = context["citations"].get(citation)
    if not citation:
        return ""
    if not full:
        return f"<span class='citation-key'>{escape(citation)}</span>"
    return ("<details class='citation-detail'><summary>Full citation for "
            f"<span class='citation-key'>{escape(citation)}</span></summary>"
            f"<p>{escape(full)}</p></details>")


def _review_text(raw, flat):
    status = _first(flat.get("source_status"), raw.get("_source_status"))
    kind = _first(flat.get("review_kind"))
    reviewer = _first(flat.get("reviewer"), (raw.get("review") or {}).get("reviewer"), raw.get("_entry_reviewer"))
    tier = _first(flat.get("review_tier"), (raw.get("review") or {}).get("tier"), raw.get("_entry_review_tier"))
    parts = []
    if _present(status):
        parts.append(f"Entry status: {status}")
    if _present(kind):
        label = {"none": "no named reviewer", "legacy": "legacy approval"}.get(str(kind), str(kind))
        parts.append(f"Review provenance: {label}")
    if _present(reviewer):
        parts.append(f"Reviewer: {reviewer}")
    if _present(tier) and str(tier) != "legacy":
        parts.append(f"Review tier: {tier}")
    return " · ".join(parts)


def _finding_more(raw, flat):
    """Expandable sample, limitations, review, statistics and source passages."""
    sections = []
    sample = raw.get("sample") or {}
    if sample:
        items = "".join(f"<dt>{escape(str(k).replace('_', ' ').title())}</dt><dd>{escape(_text(v))}</dd>"
                        for k, v in sample.items() if _present(v))
        if items:
            sections.append(f"<div><p class='detail-heading'>Sample</p><dl class='detail-list'>{items}</dl></div>")

    stats = raw.get("statistics") or {}
    if stats:
        items = "".join(f"<dt>{escape(str(k).replace('_', ' ').title())}</dt><dd>{escape(_text(v))}</dd>"
                        for k, v in stats.items() if _present(v))
        if items:
            sections.append(f"<div><p class='detail-heading'>Reported statistics</p><dl class='detail-list'>{items}</dl></div>")

    limitations = raw.get("author_limitations") or []
    if limitations:
        sections.append("<div><p class='detail-heading'>Author-reported limitations</p><ul>" +
                        "".join(f"<li>{escape(_text(item))}</li>" for item in limitations) + "</ul></div>")
    flags = (raw.get("provenance") or {}).get("flags") or flat.get("flags") or []
    if flags:
        sections.append("<div><p class='detail-heading'>Extraction flags</p><ul>" +
                        "".join(f"<li>{escape(_text(item))}</li>" for item in flags) + "</ul></div>")

    review = _review_text(raw, flat)
    if review:
        sections.append(f"<div><p class='detail-heading'>Review provenance</p><p>{escape(review)}</p></div>")

    passages = raw.get("source_passages") or []
    if passages:
        rendered = []
        for passage in passages:
            where = " · ".join(x for x in (
                f"page {passage.get('page')}" if _present(passage.get("page")) else "",
                passage.get("section") or "",
                f"supports {str(passage.get('supports')).replace('_', ' ')}" if passage.get("supports") else "",
            ) if x)
            rendered.append(f"<blockquote><p>{escape(str(passage.get('quote') or ''))}</p>"
                            f"<footer>{escape(where)}</footer></blockquote>")
        sections.append("<div><p class='detail-heading'>Source passages</p>" + "".join(rendered) + "</div>")

    if not sections:
        return ""
    return ("<details class='finding-more'><summary>Study context, limitations, review and source passages"
            "</summary><div class='finding-more-body'>" + "".join(sections) + "</div></details>")


def _finding_article(row, context):
    finding_id = _first(row.get("finding_id"), row.get("id"))
    key = (str(_first(row.get("source_path"), default="")), finding_id)
    raw, flat = context["raw"].get(key, {}), context["flat"].get(key, {})
    if not raw and not key[0]:
        candidates = context["by_id"].get((row.get("source_id"), finding_id), [])
        raw = candidates[0] if len(candidates) == 1 else {}
    citation = _first(row.get("citation"), flat.get("citation"))
    method = _first(row.get("method"), flat.get("method"), default="Not reported")
    method = ", ".join(method) if isinstance(method, list) else (method or "Not reported")
    design = _first(flat.get("design"), raw.get("design"))
    method_line = method + (f" · {design}" if _present(design) and str(design) != str(method) else "")
    raw_direction = _first(row.get("direction"), default="Not reported")
    direction = DIRECTION_TEXT.get(raw_direction, str(raw_direction))
    strength = _first(row.get("strength"), flat.get("strength"), default="Not reported")
    confidence = _first(row.get("confidence"), flat.get("confidence"), default="Not reported")
    governance = _review_text(raw, flat)
    return (
        "<article class='finding'>"
        f"<p class='finding-claim'>{escape(_text(row.get('claim')))}</p>"
        f"<p class='finding-source'><span class='citation-key'>{escape(str(citation or 'Citation not recorded'))}</span>"
        f"<span aria-hidden='true'> · </span>Study method: {escape(str(method_line))}</p>"
        "<dl class='finding-indicators'>"
        f"<div><dt>Relationship</dt><dd>{escape(direction)}</dd></div>"
        f"<div><dt>Evidence strength</dt><dd>{escape(str(strength))}</dd></div>"
        f"<div><dt>Extraction confidence</dt><dd>{escape(str(confidence))}</dd></div>"
        "</dl>"
        + (f"<p class='finding-governance'>{escape(governance)}</p>" if governance else "")
        + _citation_details(citation, context)
        + _finding_more(raw, flat)
        + "</article>")


def _distinct_findings(rows, target_column=None):
    """Apply the report's longstanding claim/citation de-duplication once."""
    subset = [c for c in (target_column, "claim", "citation") if c and c in rows.columns]
    return rows.drop_duplicates(subset=subset) if subset else rows


def _claims(kb, rows, *, target_column=None, dedupe_target=True, context=None):
    """Distinct findings, optionally grouped by their outcome."""
    rows = _distinct_findings(rows, target_column if dedupe_target else None)
    context = context or _evidence_context(kb)
    if not target_column or target_column not in rows:
        return "<div class='findings-list'>" + "".join(_finding_article(r, context) for _, r in rows.iterrows()) + "</div>"
    groups = []
    for _, group in rows.groupby(target_column, sort=False):
        name = group["target_name"].iloc[0] if "target_name" in group else _name(kb, group[target_column].iloc[0])
        groups.append("<section class='outcome-findings'>"
                      f"<h6>{escape(str(name))} <span>{len(group)} finding{'s' if len(group) != 1 else ''}</span></h6>"
                      "<div class='findings-list'>" +
                      "".join(_finding_article(r, context) for _, r in group.iterrows()) +
                      "</div></section>")
    return "".join(groups)


def _damage_text(r):
    parts = [f"{r['lesion_pct']:.1f}% of the lesion"]
    if pd.notna(r.get("region_pct")):
        parts.append(f"{r['region_pct']:.0f}% of the region destroyed")
    return " · ".join(parts)


def _html_id(prefix, value):
    token = re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")
    return f"{prefix}-{token}" if token else prefix


def location_section(kb, rules, rows, damage, coverage, settings):
    """HTML for the lesion-location evidence.

    ``rows``: ``KnowledgeBase.location_findings``; ``damage``:
    ``atlas_mapping.region_damage``; ``coverage``: counts of KB location
    findings by reachability (``location_coverage``).
    """
    intro = (f"<p class='section-intro'>This section connects the participant&rsquo;s lesion location to "
             "published group-level findings. Start with the outcome summaries, then open a damaged region to "
             "inspect each supporting, null or mixed finding.</p>"
             f"<p class='method-note'>A region counts as damaged when it holds "
             f"&ge;{settings.min_overlap_pct:g}% of the lesion or &ge;{settings.min_region_pct:g}% of it is destroyed. "
             f"Regions are matched to the knowledge base through the curated atlas mapping "
             f"(<code>aphasia-kb/atlas_mapping/</code>). Of the knowledge base's {coverage['findings']} location "
             f"findings, <b>{len(rows)}</b> concern regions this lesion damages, {coverage['undamaged']} concern "
             f"regions it does not damage, and {coverage['unmappable']} concern regions no atlas can represent "
             f"(e.g. the extreme capsule).</p>")
    if rows is None or rows.empty:
        return intro + "<p style='color:#666'><em>No knowledge-base findings concern the damaged regions.</em></p>"
    rows = rows.assign(target_name=rows["predicts"].map(lambda t: _name(kb, t)),
                       region_name=rows["region"].map(lambda t: _name(kb, t)),
                       anatomy=rows["region"].map(_anatomy_key))
    context = _evidence_context(kb)
    # One name per anatomy: the KB entry with most findings here; synonyms listed.
    names = {key: g["region_name"].value_counts().index.tolist() for key, g in rows.groupby("anatomy")}
    rows["region_name"] = rows["anatomy"].map(lambda k: names[k][0])

    # Summary: the same selected rows as before, presented as outcome blocks.
    summary = []
    for target, g in rows.groupby("predicts", sort=False):
        score = g["contribution"].sum()
        shown = _distinct_findings(g, "predicts")
        counts = {
            "Associations": int(shown["direction"].isin(["likely", "likely_responder"]).sum()),
            "Inverse associations": int(shown["direction"].isin(["unlikely", "unlikely_responder"]).sum()),
            "Null findings": int((shown["direction"] == "no_effect").sum()),
            "Mixed results": int((shown["direction"] == "mixed").sum()),
        }
        classified = sum(counts.values())
        if classified < len(shown):
            counts["Other / unclassified"] = len(shown) - classified
        statements = []
        for label, number in counts.items():
            if number:
                statements.append(f"{number} {label.lower()}")
        finding_summary = ", ".join(statements[:-1]) + ((" and " + statements[-1]) if len(statements) > 1 else
                                                        (statements[0] if statements else "no classified findings"))
        if len(statements) == 1:
            finding_summary = statements[0]
        # Region coverage is anatomical context, so it must not be reduced when
        # an identical claim/citation is stored for more than one region.
        regions = sorted({n for n in g["region_name"]})
        preview = ", ".join(regions[:3])
        region_detail = ""
        if len(regions) > 3:
            region_detail = (f"<details class='region-list'><summary>Show all {len(regions)} implicated regions</summary>"
                             "<ul>" + "".join(f"<li>{escape(region)}</li>" for region in regions) + "</ul></details>")
        cites = sorted({c for c in shown["citation"] if isinstance(c, str)})
        sources = (f"<details class='source-list'><summary>Sources ({len(cites)} citation "
                   f"key{'s' if len(cites) != 1 else ''})</summary><div>" +
                   "".join(_citation_details(cite, context) for cite in cites) + "</div></details>")
        _, signal = rules.evidence_strength(score)
        count_items = "".join(f"<div><dt>{escape(label)}</dt><dd>{number}</dd></div>"
                              for label, number in counts.items() if number)
        card = (
            "<article class='outcome-card'>"
            f"<header><div><p class='outcome-kind'>{escape(str(g['predicts_kind'].iloc[0]))}</p>"
            f"<h5>{escape(g['target_name'].iloc[0])}</h5></div>"
            f"<span class='display-signal'>Display signal: {escape(signal)}"
            "<span class='visually-hidden'>. Project-specific ordering heuristic, not an evidence grade.</span></span>"
            "</header>"
            f"<p>Across {len(shown)} distinct matched finding{'s' if len(shown) != 1 else ''}, {escape(finding_summary)}. "
            "These are group associations, not a participant-level prediction.</p>"
            f"<dl class='finding-counts'>{count_items}</dl>"
            f"<p class='region-preview'><strong>Region preview:</strong> {escape(preview)}</p>"
            f"{region_detail}{sources}"
            "<div class='print-only outcome-print-detail'>"
            f"<p><strong>All implicated regions:</strong> {escape(', '.join(regions))}</p>"
            f"<p><strong>Sources:</strong> {escape(', '.join(cites) or 'None recorded')}</p>"
            "</div></article>")
        summary.append((abs(score), card))
    summary = sorted(summary, key=lambda x: -x[0])[: settings.top_n * 2]
    signal_note = ("<details class='display-signal-note' id='display-signal-note'>"
                   "<summary>What does the display signal mean?</summary>"
                   "<p><strong>Project-specific display heuristic, not an evidence grade.</strong> It is used only "
                   "to order these summaries. The calculation combines the proportion of each matched region "
                   "damaged with the stored finding strength, study evidence class, extraction confidence and "
                   "relationship direction. Finding counts do not measure certainty, and findings may come from "
                   "the same study or overlapping cohorts.</p></details>")
    signal_note += ("<p class='print-only display-signal-print'><strong>Display signal:</strong> a project-specific "
                    "ordering heuristic, not an evidence grade. It combines lesion overlap with stored finding "
                    "strength, study evidence class, extraction confidence and relationship direction. Counts "
                    "do not measure certainty, and records may share studies or cohorts.</p>")
    html = intro + signal_note + "<div class='outcome-cards'>" + "".join(r for _, r in summary) + "</div>"

    # Detail: one block per damaged region, largest damage first.
    blocks = []
    order = (rows.assign(_d=rows["region_pct"].fillna(rows["lesion_pct"]))
             .groupby("anatomy")["_d"].max().sort_values(ascending=False).index)
    review = damage.set_index("region")["review"]
    for key in order:
        g = rows[rows["anatomy"] == key]
        shown = _distinct_findings(g, "predicts")
        first = g.iloc[0]
        flag = ("<span class='mapping-note'>Atlas match includes a documented judgement call</span>"
                if review.reindex(g["region"].unique()).fillna(False).any() else "")
        studies = g["citation"].dropna().nunique()
        thin = (f"<span class='thin-evidence'>Limited citation base: {studies} citation "
                f"key{'s' if studies != 1 else ''}</span>") if studies <= THIN_STUDIES else ""
        synonyms = names[key][1:]
        also = (f"<p class='region-alias'>Also recorded in the knowledge base as: "
                f"{escape(', '.join(synonyms))}</p>") if synonyms else ""
        notes = "".join(x for x in (flag, thin) if x)
        region_id = _html_id("region", g["region"].iloc[0])
        blocks.append(
            f"<details class='region-evidence' id='{region_id}'><summary>"
            f"<span class='region-title'>{escape(first['region_name'])} <span>({escape(first['side'])})</span></span>"
            f"<span class='region-facts'>{escape(_damage_text(first))} · {len(shown)} distinct finding"
            f"{'s' if len(shown) != 1 else ''}</span>"
            f"<span class='region-notes'>{notes}</span>"
            "<span class='region-action'><span class='when-closed'>Show findings</span>"
            "<span class='when-open'>Hide findings</span></span></summary>"
            f"<div class='region-body'>{also}{_claims(kb, g, target_column='predicts', context=context)}</div></details>")
    html += ("<div class='subsection-heading'><h5>Evidence by damaged region</h5>"
             "<p>Open a region to inspect distinct findings, grouped by outcome. A limited citation base means "
             f"{THIN_STUDIES} citation keys or fewer; it is not a certainty rating.</p></div>" + "".join(blocks))
    return html


def location_coverage(kb, rows, damage):
    """Counts for the location section's introduction."""
    import atlas_mapping
    _, mapped, unmapped = atlas_mapping.load()
    f = kb.findings
    loc = f[(f["source_kind"] == "region") | ((f["source_kind"] == "impairment") & (f["target_kind"] == "region"))]
    names = loc.apply(lambda r: r["source_id"] if r["source_kind"] == "region" else r["target"], axis=1) \
        if len(loc) else pd.Series(dtype=str)
    matched = 0 if rows is None else len(rows)
    return {"findings": int(len(loc)), "unmappable": int(names.isin(list(unmapped)).sum()),
            "undamaged": int(names.isin(list(mapped)).sum()) - matched}


def wab_band(aq):
    return next(label for upper, label in WAB_BANDS if aq <= upper)


MEASURE_LABELS = {"lesion_volume": "Lesion volume", "severity_metric": "Aphasia severity",
                  "age": "Age at stroke", "time_post_onset": "Time since stroke", "sex": "Sex"}


def _value_text(pid, value, days):
    if isinstance(value, dict):
        aq = value.get("value")
        text = f"{value.get('instrument', '')} {aq:g}".strip()
        if value.get("instrument", "").upper().startswith("WAB") and aq is not None:
            text += f" ({wab_band(aq)}, Kertesz bands)"
        if days is not None:
            text += f", measured {days:.0f} days after the stroke"
        return text
    if pid == "lesion_volume":
        return f"{value:.0f} ml (this report's lesion mask)"
    if pid == "time_post_onset":
        return f"{value:.0f} days"
    if pid == "age":
        return f"{value:.0f} years"
    return escape(str(value))


def measures_section(kb, predictors, days=None, min_confidence=None):
    """HTML: one row per measure of the participant that the KB has findings about."""
    f = kb.findings
    f = f[f["source_kind"] == "predictor"]
    if min_confidence:
        order = {"low": 0, "medium": 1, "high": 2}
        f = f[f["confidence"].map(lambda c: order.get(c, 0) >= order.get(min_confidence, 0))]
    directions = {}
    if not kb.predictors.empty and "direction_of_severity" in kb.predictors:
        for _, p in kb.predictors.iterrows():
            if isinstance(p.get("direction_of_severity"), str):
                directions.setdefault(p["id"], p["direction_of_severity"])
    rows = []
    context = _evidence_context(kb)
    for key, value in (predictors or {}).items():
        pid = kb.resolve_aliases([key]).get(key) or key
        # Findings whose target is the measure itself describe how it is
        # predicted (e.g. models estimating WAB-AQ), not what it implies.
        g = f[(f["source_id"] == pid) & (f["target"] != pid)]
        if g.empty:
            continue
        g = g.assign(target_name=g["target"].map(lambda t: _name(kb, t)))
        shown = _distinct_findings(g)
        polarity = {"higher_is_worse": "higher values go with worse language or recovery",
                    "lower_is_worse": "lower values go with worse language or recovery"}.get(directions.get(pid))
        directions_shown = shown["direction"].fillna("not reported")
        counts = ", ".join(f"{n} {DIRECTION_TEXT.get(d, d)}" for d, n in directions_shown.value_counts().items())
        caution = ""
        if pid == "severity_metric" and days is not None and days > 180:
            early = shown[shown["claim"].fillna("").str.contains(EARLY) | (shown["target_kind"] == "prognosis")]
            if len(early):
                caution = (f"<div style='font-size:11px;color:#2b2b3a;border-left:3px solid #f45b69;"
                           f"padding-left:.5rem;margin-top:3px'>⚠ {len(early)} of these findings "
                           "concern severity measured early after the stroke (or recovery from it); this score was "
                           f"measured {days:.0f} days after the stroke, so they apply only loosely.</div>")
        rows.append(
            "<article class='measure-card'>"
            f"<header><h5>{escape(MEASURE_LABELS.get(pid, _name(kb, pid)))}</h5>"
            f"<p>{_value_text(pid, value, days)}</p></header>"
            f"<p>{escape(polarity.capitalize() + '.') if polarity else 'Direction: see each finding.'} "
            f"<span class='secondary'>({len(shown)} distinct findings: {escape(counts)})</span></p>"
            f"<details class='measure-findings'><summary>Show {len(shown)} distinct finding"
            f"{'s' if len(shown) != 1 else ''}</summary>"
            f"{_claims(kb, g, target_column='target', dedupe_target=False, context=context)}</details>{caution}</article>")
    if not rows:
        return "<p style='color:#666'><em>No knowledge-base findings concern this participant's measures.</em></p>"
    return "<div class='measure-cards'>" + "".join(rows) + "</div>"


MAP_LABELS = {"bcb": "BCBToolkit", "deepdisco": "DeepDisco (whole-brain model)"}


def disconnectome_map(study, entry, source, which):
    """Path of the participant's disconnectome map for ``source``, or None."""
    from .study import file_token
    if which not in MAP_LABELS:
        return None
    d = study.dirs(entry)
    token = file_token(source)
    folder = d.get("bcbtoolkit" if which == "bcb" else "deepdisco")
    if folder is None:
        return None
    path = Path(folder) / (f"Disconnectome_{token}.nii.gz" if which == "bcb" else f"DeepDisco_{token}_whole_brain.nii.gz")
    return path if path.is_file() else None


def tract_atlases(all_atlases):
    """``{name: (image, labels)}`` of the tract atlases in the notebook's ALL_ATLASES."""
    return {name: (str(a.maps), dict(a.labels)) for name, a in (all_atlases or {}).items()
            if name in ("JHU", "XTRACT")}


def disconnection_section(kb, rows, disconnection, damage, settings, map_label):
    """HTML: tracts disconnected by the lesion (from a disconnectome map), with their findings.

    ``rows``: ``KnowledgeBase.location_findings`` on ``disconnection``
    (``atlas_mapping.region_disconnection``); ``damage``: direct damage, to
    say which tracts are also hit.
    """
    if map_label is None:
        return ("<p style='color:#666'><em>No disconnectome map for this lesion mask "
                "(run the BCBToolkit or DeepDisco step, or choose another map in the report settings).</em></p>")
    intro = ("<p class='section-intro'>This section shows white-matter tracts that may be interrupted beyond the "
             "visible lesion. Open a tract to inspect the group-level findings linked to it.</p>"
             f"<p class='method-note'>The {escape(map_label)} map gives, for every "
             "voxel, the probability that its fibres pass through the lesion. A tract counts as disconnected when "
             f"&ge;{settings.min_disconnected_pct:g}% of its voxels have a probability above 0.5. This catches tracts "
             "cut by the lesion away from where it lies, which direct overlap misses.</p>")
    if rows is None or rows.empty:
        return intro + "<p style='color:#666'><em>No knowledge-base tract is disconnected above the threshold.</em></p>"
    direct = damage.set_index("region") if damage is not None and len(damage) else None
    rows = rows.assign(target_name=rows["predicts"].map(lambda t: _name(kb, t)),
                       region_name=rows["region"].map(lambda t: _name(kb, t)),
                       anatomy=rows["region"].map(_anatomy_key))
    context = _evidence_context(kb)
    names = {key: g["region_name"].value_counts().index.tolist() for key, g in rows.groupby("anatomy")}
    blocks = []
    for key in rows.groupby("anatomy")["region_pct"].max().sort_values(ascending=False).index:
        g = rows[rows["anatomy"] == key]
        shown = _distinct_findings(g, "predicts")
        first = g.iloc[0]
        hit = ""
        if direct is not None:
            destroyed = direct.reindex(g["region"].unique())["region_pct"].dropna()
            if len(destroyed) and destroyed.max() > 0:
                hit = f" · also directly damaged ({destroyed.max():.0f}% destroyed)"
        studies = g["citation"].dropna().nunique()
        thin = (f"<span class='thin-evidence'>Limited citation base: {studies} citation "
                f"key{'s' if studies != 1 else ''}</span>") if studies <= THIN_STUDIES else ""
        also = (f"<p class='region-alias'>Also recorded in the knowledge base as: "
                f"{escape(', '.join(names[key][1:]))}</p>") if len(names[key]) > 1 else ""
        tract_id = _html_id("tract", g["region"].iloc[0])
        blocks.append(
            f"<details class='region-evidence tract-evidence' id='{tract_id}'><summary>"
            f"<span class='region-title'>{escape(names[key][0])} <span>({escape(first['side'])})</span></span>"
            f"<span class='region-facts'>{first['region_pct']:.0f}% of the tract disconnected{escape(hit)} · "
            f"{len(shown)} distinct finding{'s' if len(shown) != 1 else ''}</span>"
            f"<span class='region-notes'>{thin}</span>"
            "<span class='region-action'><span class='when-closed'>Show findings</span>"
            "<span class='when-open'>Hide findings</span></span></summary>"
            f"<div class='region-body'>{also}{_claims(kb, g, target_column='predicts', context=context)}</div></details>")
    return intro + "".join(blocks)
