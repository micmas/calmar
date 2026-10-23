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


#: KB ``sample.phase`` (schema v2.6, SRRR bands) → the report's recovery stages (aphasia_rules).
SAMPLE_PHASE_STAGES = {"hyperacute": "acute", "acute": "acute", "early_subacute": "subacute",
                       "late_subacute": "subacute", "chronic": "chronic"}


def finding_phases(row):
    """Recovery stages (acute / subacute / chronic) a finding was studied in.

    From the KB's ``phase`` (``sample.phase``, stated or inferred from
    ``time_post_onset`` by aphasia-kb/phase.py). When that is ``mixed``,
    ``longitudinal`` or ``not_reported``, the stages named in the sample
    population text are used (aphasia_rules); empty = unknown.
    """
    import aphasia_rules
    stage = SAMPLE_PHASE_STAGES.get(row.get("phase"))
    if stage:
        return {stage}
    text = " ".join(str(row.get(k) or "") for k in ("population", "time_post_onset"))
    return aphasia_rules.stages_in_population(text)


def _phase_indicator(row, participant_phase):
    """The finding's study phase, with a text warning when it differs from the participant's."""
    phases = finding_phases(row)
    if not phases:
        return "<div><dt>Study phase</dt><dd>Not stated</dd></div>"
    text = "/".join(sorted(phases))
    if participant_phase and participant_phase not in phases:
        return (f"<div><dt>Study phase</dt><dd title='Studied in {escape(text)} stroke; this participant is "
                f"{escape(participant_phase)}'>{escape(text.capitalize())} "
                "<span class='phase-mismatch'>(stage mismatch)</span></dd></div>")
    return f"<div><dt>Study phase</dt><dd>{escape(text.capitalize())}</dd></div>"


def phase_summary(rows, participant_phase):
    """One sentence: the phase mix of the findings shown, against the participant's."""
    if rows is None or rows.empty or not participant_phase:
        return ""
    phases = rows.apply(finding_phases, axis=1)
    same = sum(participant_phase in p for p in phases)
    other = sum(bool(p) and participant_phase not in p for p in phases)
    unknown = sum(not p for p in phases)
    note = (f"<p class='phase-summary'>This participant is in the <b>{escape(participant_phase)}</b> "
            f"phase. Of these {len(rows)} findings, {same} were studied in the same phase, {other} in another phase "
            f"(marked &ldquo;stage mismatch&rdquo;) and {unknown} do not state it.")
    if other > same:
        note += (" Most of this evidence comes from another recovery phase; lesion–symptom associations can differ "
                 "between phases (e.g. hypoperfusion and diaschisis after an acute stroke), so read it with caution.")
    return note + "</p>"


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


def _finding_article(row, context, phase=None):
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
        + _phase_indicator(row, phase) +
        "</dl>"
        + (f"<p class='finding-governance'>{escape(governance)}</p>" if governance else "")
        + _citation_details(citation, context)
        + _finding_more(raw, flat)
        + "</article>")


def _distinct_findings(rows, target_column=None):
    """Apply the report's longstanding claim/citation de-duplication once."""
    subset = [c for c in (target_column, "claim", "citation") if c and c in rows.columns]
    return rows.drop_duplicates(subset=subset) if subset else rows


def _direction_counts(rows):
    """Ordered relationship counts for already de-duplicated finding rows."""
    counts = {
        "Associations": int(rows["direction"].isin(["likely", "likely_responder"]).sum()),
        "Inverse associations": int(rows["direction"].isin(["unlikely", "unlikely_responder"]).sum()),
        "Null findings": int((rows["direction"] == "no_effect").sum()),
        "Mixed results": int((rows["direction"] == "mixed").sum()),
    }
    classified = sum(counts.values())
    if classified < len(rows):
        counts["Other / unclassified"] = len(rows) - classified
    return counts


def _count_items(counts):
    return "".join(f"<span><strong>{escape(label)}</strong> {number}</span>"
                   for label, number in counts.items() if number)


def _count_text(counts):
    """Compact plain-text relationship counts for cross-references."""
    singular = {
        "Associations": "association",
        "Inverse associations": "inverse association",
        "Null findings": "null finding",
        "Mixed results": "mixed result",
        "Other / unclassified": "other / unclassified",
    }
    return ", ".join(
        f"{number} {singular[label] if number == 1 else label.lower()}"
        for label, number in counts.items() if number)


def _claims(kb, rows, *, target_column=None, dedupe_target=True, context=None, phase=None):
    """Distinct findings, optionally grouped by their outcome."""
    rows = _distinct_findings(rows, target_column if dedupe_target else None)
    context = context or _evidence_context(kb)
    if not target_column or target_column not in rows:
        return "<div class='findings-list'>" + "".join(_finding_article(r, context, phase) for _, r in rows.iterrows()) + "</div>"
    groups = []
    for _, group in rows.groupby(target_column, sort=False):
        name = group["target_name"].iloc[0] if "target_name" in group else _name(kb, group[target_column].iloc[0])
        counts = _count_items(_direction_counts(group))
        groups.append("<section class='outcome-findings'>"
                      f"<h4>{escape(str(name))} <span>{len(group)} finding{'s' if len(group) != 1 else ''}</span></h4>"
                      f"<p class='finding-counts'>{counts}</p>"
                      "<div class='findings-list'>" +
                      "".join(_finding_article(r, context, phase) for _, r in group.iterrows()) +
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


def _display_signal(rules, score):
    stars, label = rules.evidence_strength(score)
    glyphs = "&#9733;" * stars if stars else "&mdash;"
    return (f"<span class='display-signal' title='Project display heuristic; raw score = {score:+.2f}'>"
            f"<span class='display-stars' aria-hidden='true'>{glyphs}</span>"
            f"<span class='display-stars-print'>{stars}/4 stars</span>"
            f"<span class='display-label' aria-hidden='true'>{escape(label)}</span>"
            f"<span class='visually-hidden'>Project-specific display heuristic: {stars} of 4 stars; "
            f"{escape(label)}.</span></span>")


def is_symptom_target(rules, target, kind):
    """Whether a KB target is a symptom-level impairment for this report."""
    if kind != "impairment":
        return False
    target = str(target)
    normalized = re.sub(r"[^a-z0-9]+", "_", target.lower()).strip("_")
    canonical_type = getattr(rules, "canonical_aphasia_type", lambda _: None)
    return not (canonical_type(target) is not None or normalized == "aphasia" or normalized.endswith("_aphasia"))


def _symptom_findings(rows, rules):
    """Location findings whose targets are symptoms, not aphasia types.

    Classical aphasia syndromes are stored as impairments in the knowledge
    base, but displaying them against one participant's lesion reads as a
    diagnostic classification.  Keep the underlying evidence untouched and
    apply this deterministic presentation filter only in the participant
    lesion-location section.
    """
    if rows is None or rows.empty:
        return rows
    keep = rows.apply(lambda row: is_symptom_target(rules, row["predicts"], row["predicts_kind"]), axis=1)
    return rows[keep].copy()


def location_section(kb, rules, rows, damage, coverage, settings, phase=None):
    """HTML for the lesion-location evidence.

    ``rows``: ``KnowledgeBase.location_findings``; ``damage``:
    ``atlas_mapping.region_damage``; ``coverage``: counts of KB location
    findings by reachability (``location_coverage``).
    """
    matched_before_filter = 0 if rows is None else len(rows)
    rows = _symptom_findings(rows, rules)
    intro = (f"<p class='section-intro'>This section connects the participant&rsquo;s lesion location to "
             "published group-level findings about symptoms. Aphasia diagnoses, subtype labels and other non-symptom "
             "targets are excluded: this report does not infer the presence or type of aphasia from a lesion. Start with the symptom "
             "summaries, then open a damaged region to "
             "inspect each supporting, null or mixed finding.</p>"
             f"<p class='method-note'>A region counts as damaged when it holds "
             f"&ge;{settings.min_overlap_pct:g}% of the lesion or &ge;{settings.min_region_pct:g}% of it is destroyed. "
             f"Regions are matched to the knowledge base through the curated atlas mapping "
             f"(<code>aphasia-kb/atlas_mapping/</code>). Of the knowledge base's {coverage['findings']} location "
             f"findings, {matched_before_filter} concern regions this lesion damages before the symptom-only display "
             f"filter; <b>{len(rows)}</b> symptom findings are shown. {coverage['undamaged']} concern "
             f"regions it does not damage, and {coverage['unmappable']} concern regions no atlas can represent "
             f"(e.g. the extreme capsule).</p>")
    intro += laterality_note(damage)
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
        counts = _direction_counts(shown)
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
        count_items = _count_items(counts)
        citation_count = len({citation.strip() for citation in shown["citation"]
                              if isinstance(citation, str) and citation.strip()})
        anatomy_count = g["anatomy"].nunique()
        relevant = (citation_count >= max(1, int(getattr(settings, "min_summary_citations", 2)))
                    and anatomy_count >= max(1, int(getattr(settings, "min_summary_anatomies", 2))))
        symptom_id = _html_id("symptom", target)
        card = (
            f"<article class='outcome-card' id='{symptom_id}'>"
            f"<header><div><p class='outcome-kind'>{escape(str(g['predicts_kind'].iloc[0]))}</p>"
            f"<h3>{escape(g['target_name'].iloc[0])}</h3></div>"
            f"{_display_signal(rules, score)}"
            "</header>"
            f"<p class='matched-findings'>{len(shown)} distinct matched finding"
            f"{'s' if len(shown) != 1 else ''} · group associations, not a participant-level prediction.</p>"
            f"<p class='finding-counts'>{count_items}</p>"
            f"<p class='relevance-basis'>{citation_count} distinct citation key"
            f"{'s' if citation_count != 1 else ''} · {anatomy_count} distinct anatomy mapping"
            f"{'s' if anatomy_count != 1 else ''} (KB synonyms merged)</p>"
            f"<p class='region-preview'><strong>Region preview:</strong> {escape(preview)}</p>"
            f"{region_detail}{sources}"
            "<div class='print-only outcome-print-detail'>"
            f"<p><strong>All implicated regions:</strong> {escape(', '.join(regions))}</p>"
            f"<p><strong>Sources:</strong> {escape(', '.join(cites) or 'None recorded')}</p>"
            "</div></article>")
        summary.append((relevant, abs(score), str(g["target_name"].iloc[0]).casefold(), card))
    summary = sorted(summary, key=lambda x: (-x[1], x[2]))
    signal_note = ("<details class='display-signal-note' id='display-signal-note' data-print-open>"
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
    min_citations = max(1, int(getattr(settings, "min_summary_citations", 2)))
    min_anatomies = max(1, int(getattr(settings, "min_summary_anatomies", 2)))
    main_summary = [item for item in summary if item[0]]
    additional_summary = [item for item in summary if not item[0]]
    criterion = ("<p class='method-note'><strong>Primary display relevance criterion:</strong> a symptom appears "
                 f"in the main list when its matched findings span at least {min_citations} distinct citation key"
                 f"{'s' if min_citations != 1 else ''} and {min_anatomies} distinct anatomy mapping"
                 f"{'s' if min_anatomies != 1 else ''} after KB synonyms are merged. Association, inverse, null, "
                 "mixed and unclassified findings all count toward this display threshold. This is a scanning rule, "
                 "not a certainty threshold; citation keys and anatomical links need not be statistically independent.</p>")
    cards = criterion
    if main_summary:
        cards += ("<div class='outcome-cards primary-outcomes'>" +
                  "".join(item[3] for item in main_summary) + "</div>")
    else:
        cards += ("<p class='empty-primary'><em>No symptom summary meets the primary display criterion. "
                  "The matched summaries remain available below.</em></p>")
    if additional_summary:
        count = len(additional_summary)
        cards += ("<details class='additional-outcomes' data-print-open><summary>Show "
                  f"{count} symptom summar{'ies' if count != 1 else 'y'} below the primary display criterion</summary>"
                  "<div class='outcome-cards'>" + "".join(item[3] for item in additional_summary) + "</div></details>")
    html = intro + signal_note + cards

    # Detail: one block per damaged region. "Main" is a display-only ranking
    # by share of this lesion, then share of the region destroyed. It does not
    # alter which findings contributed to the outcome summaries above.
    blocks = []
    ranked = (rows.groupby("anatomy").agg(_lesion=("lesion_pct", "max"), _region=("region_pct", "max"))
              .fillna(0).sort_values(["_lesion", "_region"], ascending=False))
    order = list(ranked.index)
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
            f"<details class='region-evidence' id='{region_id}' data-print-open><summary>"
            f"<span class='region-title'>{escape(first['region_name'])} <span>({escape(first['side'])})</span></span>"
            f"<span class='region-facts'>{escape(_damage_text(first))} · {len(shown)} distinct finding"
            f"{'s' if len(shown) != 1 else ''}</span>"
            f"<span class='region-notes'>{notes}</span>"
            "<span class='region-action'><span class='when-closed'>Show findings</span>"
            "<span class='when-open'>Hide findings</span></span></summary>"
            f"<div class='region-body'>{also}{_claims(kb, g, target_column='predicts', context=context, phase=phase)}</div></details>")
    limit = max(1, int(getattr(settings, "max_evidence_regions", 8)))
    main_blocks, additional = blocks[:limit], blocks[limit:]
    if additional:
        count = len(additional)
        noun = "regions" if count != 1 else "region"
        more = ("<details class='additional-regions'><summary>Show "
                f"{count} additional qualifying damaged {noun}"
                "</summary><div class='additional-regions-body'>" + "".join(additional) + "</div></details>"
                f"<p class='print-only additional-regions-print'>{count} additional qualifying damaged {noun} "
                f"{'are' if count != 1 else 'is'} available in the interactive HTML report.</p>")
    else:
        more = ""
    html += phase_summary(rows, phase)
    html += ("<div class='subsection-heading'><h3>Evidence by damaged region</h3>"
             f"<p>The {len(main_blocks)} main mapped ROI{'s' if len(main_blocks) != 1 else ''} below are ranked by "
             "the share of this lesion they contain, then by the share of the ROI destroyed. Open one to inspect "
             "distinct findings grouped by outcome. All qualifying regions still contribute to the summaries above; "
             f"a limited citation base means {THIN_STUDIES} citation keys or fewer and is not a certainty rating.</p>"
             "</div>" + "".join(main_blocks) + more)
    return html

def laterality_note(damage):
    """A note when the lesion lies mainly in the right hemisphere: the knowledge
    base is almost entirely about left-hemisphere language regions."""
    if damage is None or damage.empty or "side" not in damage:
        return ""
    by_side = damage[damage["side"].isin(["left", "right"])].groupby("side")["lesion_pct"].max()
    left, right = by_side.get("left", 0.0), by_side.get("right", 0.0)
    if right > 0 and right > 2 * left:
        return ("<p class='laterality-note'><b>Caution:</b> This lesion lies mainly in the "
                "<b>right</b> hemisphere. The knowledge base is almost entirely about left-hemisphere language "
                "regions, so few or no findings apply; an absence of findings here does not mean an absence of "
                "deficits.</p>")
    return ""


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


def measures_section(kb, predictors, days=None, min_confidence=None, phase=None):
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
                           f"padding-left:.5rem;margin-top:3px'><b>Timing note:</b> {len(early)} of these findings "
                           "concern severity measured early after the stroke (or recovery from it); this score was "
                           f"measured {days:.0f} days after the stroke, so they apply only loosely.</div>")
        rows.append(
            "<article class='measure-card'>"
            f"<header><h3>{escape(MEASURE_LABELS.get(pid, _name(kb, pid)))}</h3>"
            f"<p>{_value_text(pid, value, days)}</p></header>"
            f"<p>{escape(polarity.capitalize() + '.') if polarity else 'Direction: see each finding.'} "
            f"<span class='secondary'>({len(shown)} distinct findings: {escape(counts)})</span></p>"
            f"<details class='measure-findings' data-print-open><summary>Show {len(shown)} distinct finding"
            f"{'s' if len(shown) != 1 else ''}</summary>"
            f"{_claims(kb, g, target_column='target', dedupe_target=False, context=context, phase=phase)}</details>{caution}</article>")
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


def _measured_disconnections(disconnection):
    """Map-derived tract rows with a usable disconnection measurement."""
    required = {"region", "side", "region_pct"}
    if disconnection is None or disconnection.empty or not required.issubset(disconnection.columns):
        return pd.DataFrame()
    rows = disconnection.copy()
    if "measured" in rows:
        rows = rows[rows["measured"].fillna(False).astype(bool)]
    rows["region_pct"] = pd.to_numeric(rows["region_pct"], errors="coerce")
    return rows[rows["region_pct"].notna()].copy()


def _qualifying_disconnections(disconnection, threshold):
    """Map-derived tract rows at or above the report threshold."""
    rows = _measured_disconnections(disconnection)
    rows = rows[rows["region_pct"] >= threshold].copy() if not rows.empty else rows
    if not rows.empty:
        rows["anatomy"] = rows["region"].map(_anatomy_key)
    return rows


def _anatomical_tract_blocks(kb, disconnection, evidence_anatomies, damage):
    """Describe disconnected tracts even when the KB has no symptom finding."""
    if disconnection.empty:
        return ""
    direct = (damage.groupby("region")["region_pct"].max()
              if damage is not None and len(damage) and {"region", "region_pct"}.issubset(damage.columns)
              else None)
    blocks = []
    ranked = disconnection.groupby("anatomy")["region_pct"].max().sort_values(ascending=False, kind="stable")
    for key in ranked.index:
        if key in evidence_anatomies:
            continue
        group = disconnection[disconnection["anatomy"] == key]
        first = group.loc[group["region_pct"].idxmax()]
        names = list(dict.fromkeys(_name(kb, region) for region in group["region"]))
        aliases = (f"<p class='region-alias'>Also represented as: {escape(', '.join(names[1:]))}</p>"
                   if len(names) > 1 else "")
        hit = ""
        if direct is not None:
            destroyed = direct.reindex(group["region"].unique()).dropna()
            if len(destroyed) and destroyed.max() > 0:
                hit = f" · also directly damaged ({destroyed.max():.0f}% destroyed)"
        tract_id = _html_id("tract", first["region"])
        blocks.append(
            f"<details class='region-evidence tract-evidence tract-anatomy-only' id='{tract_id}' data-print-open>"
            "<summary>"
            f"<span class='region-title'>{escape(names[0])} <span>({escape(str(first['side']))})</span></span>"
            f"<span class='region-facts'>{first['region_pct']:.0f}% of the tract disconnected{escape(hit)}</span>"
            "<span class='tract-direction'><span><strong>Anatomical result only</strong></span></span>"
            "<span class='region-notes'><span class='secondary'>No linked symptom-level finding</span></span>"
            "<span class='region-action'><span class='when-closed'>Show context</span>"
            "<span class='when-open'>Hide context</span></span></summary>"
            f"<div class='region-body'>{aliases}<p>The disconnectome map derived from this participant&rsquo;s lesion crosses the report "
            "threshold for this tract, but the current knowledge base has no eligible symptom-level literature "
            "finding linked to it. The tract is therefore reported as anatomical context only; absence of a linked "
            "finding is not evidence that it has no functional importance.</p></div></details>"
        )
    return "".join(blocks)


def disconnection_section(kb, rules, rows, disconnection, damage, settings, map_label, phase=None,
                          *, map_name=None, mask_label=None, lesion_rows=None):
    """HTML: tracts disconnected by the lesion (from a disconnectome map), with their findings.

    ``rows``: ``KnowledgeBase.location_findings`` on ``disconnection``
    (``atlas_mapping.region_disconnection``); ``damage``: direct damage, to
    say which tracts are also hit.
    """
    if map_label is None:
        return ("<p style='color:#666'><em>No disconnectome map for this lesion mask "
                "(run the BCBToolkit or DeepDisco step, or choose another map in the report settings).</em></p>")
    matched_before_filter = 0 if rows is None else len(rows)
    disconnection_available = not _measured_disconnections(disconnection).empty
    qualifying = _qualifying_disconnections(disconnection, settings.min_disconnected_pct)
    source = escape(mask_label or "selected lesion")
    filename = f" (<code>{escape(map_name)}</code>)" if map_name else ""
    intro = ("<p class='section-intro'>This section shows white-matter tracts that may be interrupted beyond the "
             "visible lesion. Open a tract to inspect its anatomical context and any group-level findings linked "
             "to it.</p>"
             f"<p class='method-note'>The {escape(map_label)} map gives, for every "
             "voxel, the probability that its fibres pass through the lesion. A tract counts as disconnected when "
             f"&ge;{settings.min_disconnected_pct:g}% of its voxels have a probability above 0.5. This catches tracts "
             "cut by the lesion away from where it lies, which direct overlap misses. Relationship counts summarise "
             "the stored group findings for each tract: association means a group-level study reported a relationship; "
             "inverse association means the stored relationship runs in the opposite direction; null means the study "
             "did not find the association; mixed means results were inconsistent; and other / unclassified means no "
             "display direction was assigned. A cross-reference means the same symptom target also has direct-damage "
             "evidence from a different anatomy in this participant&rsquo;s lesion-location section. It is not independent "
             "or additive evidence and does not predict the participant&rsquo;s symptoms.</p>"
             "<details class='evidence-path' data-print-open><summary>Where this evidence comes from</summary><div><ol>"
             f"<li>The participant-specific <b>{source}</b> mask is the input.</li>"
             f"<li>CALMaR reads its <b>{escape(map_label)}</b> probability map{filename}.</li>"
             "<li>That map is overlapped with the JHU and XTRACT tract atlases using the threshold above.</li>"
             "<li>Literature claims come from the tract/region entries in <code>aphasia-kb/</code>, linked through "
             "the curated <code>aphasia-kb/atlas_mapping/</code>; each finding retains its citation and review details.</li>"
             "</ol><p>The participant map calculation and the literature claims are separate provenance layers. "
             "Group associations do not predict this participant&rsquo;s outcome.</p></div></details>")
    rows = _symptom_findings(rows, rules)
    evidence_anatomies = (set() if rows is None or rows.empty
                          else set(rows["region"].map(_anatomy_key)))
    anatomy_only = _anatomical_tract_blocks(kb, qualifying, evidence_anatomies, damage)
    if rows is None or rows.empty:
        if matched_before_filter:
            message = ("Disconnectome-matched tracts were found, but their knowledge-base records contain no "
                       "symptom-level targets eligible for this report. Their anatomical disconnection is still "
                       "listed below.")
        elif not disconnection_available:
            message = "No tract-disconnection measurements were available for this map."
        elif qualifying.empty:
            message = "No mapped tract reached the disconnection threshold."
        else:
            message = ("No symptom-level knowledge-base findings matched these tracts. Their map-derived "
                       "disconnection is still listed below as anatomical context.")
        return intro + f"<p class='method-note'><em>{message}</em></p>" + anatomy_only
    lesion_rows = _symptom_findings(lesion_rows, rules)
    if lesion_rows is not None and not lesion_rows.empty:
        lesion_rows = lesion_rows.assign(anatomy=lesion_rows["region"].map(_anatomy_key))
    direct = (damage.groupby("region")["region_pct"].max()
              if damage is not None and len(damage) and {"region", "region_pct"}.issubset(damage.columns)
              else None)
    rows = rows.assign(target_name=rows["predicts"].map(lambda t: _name(kb, t)),
                       region_name=rows["region"].map(lambda t: _name(kb, t)),
                       anatomy=rows["region"].map(_anatomy_key))
    context = _evidence_context(kb)
    names = {key: g["region_name"].value_counts().index.tolist() for key, g in rows.groupby("anatomy")}
    blocks = []
    for key in rows.groupby("anatomy")["region_pct"].max().sort_values(ascending=False, kind="stable").index:
        g = rows[rows["anatomy"] == key]
        shown = _distinct_findings(g, "predicts")
        count_items = _count_items(_direction_counts(shown))
        first = g.iloc[0]
        hit = ""
        if direct is not None:
            destroyed = direct.reindex(g["region"].unique()).dropna()
            if len(destroyed) and destroyed.max() > 0:
                hit = f" · also directly damaged ({destroyed.max():.0f}% destroyed)"
        studies = g["citation"].dropna().nunique()
        thin = (f"<span class='thin-evidence'>Limited citation base: {studies} citation "
                f"key{'s' if studies != 1 else ''}</span>") if studies <= THIN_STUDIES else ""
        also = (f"<p class='region-alias'>Also recorded in the knowledge base as: "
                f"{escape(', '.join(names[key][1:]))}</p>") if len(names[key]) > 1 else ""
        tract_id = _html_id("tract", g["region"].iloc[0])
        shared = []
        if lesion_rows is not None and not lesion_rows.empty:
            for target in sorted(set(g["predicts"]), key=lambda value: _name(kb, value).lower()):
                elsewhere = lesion_rows[(lesion_rows["predicts"] == target) &
                                        lesion_rows["anatomy"].map(lambda value: value != key)]
                if elsewhere.empty:
                    continue
                tract_target = _distinct_findings(g[g["predicts"] == target], "predicts")
                direct_target = _distinct_findings(elsewhere, "predicts")
                shared.append((target, _count_text(_direction_counts(tract_target)),
                               _count_text(_direction_counts(direct_target))))
        shared_preview = ", ".join(escape(_name(kb, target)) for target, _, _ in shared[:3])
        if len(shared) > 3:
            shared_preview += f" <span class='secondary'>(+{len(shared) - 3} more in the details)</span>"
        shared_line = (f"<span class='shared-symptoms screen-only'><strong>Same symptom target"
                       f"{'s' if len(shared) != 1 else ''} also listed under direct damage elsewhere:</strong> "
                       f"{shared_preview}</span>") if shared else ""
        shared_detail = ""
        if shared:
            items = "".join(
                f"<li><a href='#{_html_id('symptom', target)}'>{escape(_name(kb, target))}</a> "
                f"<span class='secondary'>(this tract: {escape(tract_counts)}; direct damage elsewhere: "
                f"{escape(direct_counts)})</span></li>"
                for target, tract_counts, direct_counts in shared)
            shared_detail = ("<div class='shared-symptom-detail'><p><strong>Same symptom targets elsewhere in "
                             "the direct-damage evidence</strong></p><ul>" + items + "</ul>"
                             "<p class='secondary'>These links cross-reference target labels; they do not make the "
                             "two evidence paths independent or additive.</p></div>")
        blocks.append(
            f"<details class='region-evidence tract-evidence' id='{tract_id}' data-print-open><summary>"
            f"<span class='region-title'>{escape(names[key][0])} <span>({escape(first['side'])})</span></span>"
            f"<span class='region-facts'>{first['region_pct']:.0f}% of the tract disconnected{escape(hit)} · "
            f"{len(shown)} distinct finding{'s' if len(shown) != 1 else ''}</span>"
            f"<span class='tract-direction'>{count_items}</span>"
            f"<span class='region-notes'>{thin}</span>"
            f"{shared_line}"
            "<span class='region-action'><span class='when-closed'>Show findings</span>"
            "<span class='when-open'>Hide findings</span></span></summary>"
            f"<div class='region-body'>{also}{shared_detail}"
            f"{_claims(kb, g, target_column='predicts', context=context, phase=phase)}</div></details>")
    anatomical_note = ("<p class='method-note'><strong>Additional disconnected tracts:</strong> the entries below "
                       "cross the same map threshold but have no eligible symptom-level finding in the current "
                       "knowledge base.</p>" + anatomy_only) if anatomy_only else ""
    return intro + phase_summary(rows, phase) + "".join(blocks) + anatomical_note
