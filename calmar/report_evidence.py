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
DIRECTION_COLOUR = {"association": "#1a3a6b", "inverse association": "#7b3f00",
                    "no association": "#6c757d", "mixed results": "#856404"}
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


def _pill(text):
    colour = DIRECTION_COLOUR.get(text, "#6c757d")
    return (f"<span style='display:inline-block;padding:0 6px;border-radius:3px;background:{colour};"
            f"color:#fff;font-size:10px;white-space:nowrap'>{escape(text)}</span>")


def _claims(rows, *, show_target):
    """One line per finding: direction, (target,) claim, method and citation.
    The same claim from the same paper stored in two KB entries is shown once."""
    rows = rows.drop_duplicates(subset=[c for c in ("predicts", "claim", "citation") if c in rows.columns])
    items = []
    for _, r in rows.iterrows():
        direction = DIRECTION_TEXT.get(r.get("direction"), str(r.get("direction") or "—"))
        target = f"<b>{escape(r['target_name'])}</b>: " if show_target else ""
        method = r.get("method")
        method = ", ".join(method) if isinstance(method, list) else (method or "")
        detail = " · ".join(x for x in (method, r.get("strength") or "") if x)
        items.append(f"<li style='margin:2px 0'>{_pill(direction)} {target}{escape(str(r.get('claim') or ''))} "
                     f"<span style='color:#888'>({escape(detail)}{' · ' if detail else ''}"
                     f"{escape(str(r.get('citation') or ''))})</span></li>")
    return "<ul style='margin:2px 0 0 16px;padding:0;font-size:11.5px'>" + "".join(items) + "</ul>"


def _damage_text(r):
    parts = [f"{r['lesion_pct']:.1f}% of the lesion"]
    if pd.notna(r.get("region_pct")):
        parts.append(f"{r['region_pct']:.0f}% of the region destroyed")
    return " · ".join(parts)


def location_section(kb, rules, rows, damage, coverage, settings):
    """HTML for the lesion-location evidence.

    ``rows``: ``KnowledgeBase.location_findings``; ``damage``:
    ``atlas_mapping.region_damage``; ``coverage``: counts of KB location
    findings by reachability (``location_coverage``).
    """
    intro = (f"<p style='font-size:12px;color:#555;margin:4px 0 8px 0'>A region counts as damaged when it holds "
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
    # One name per anatomy: the KB entry with most findings here; synonyms listed.
    names = {key: g["region_name"].value_counts().index.tolist() for key, g in rows.groupby("anatomy")}
    rows["region_name"] = rows["anatomy"].map(lambda k: names[k][0])

    # Summary: what the damaged regions point to.
    summary = []
    for target, g in rows.groupby("predicts", sort=False):
        assoc = g[g["direction"].isin(["likely", "likely_responder"])]
        other = g.drop(assoc.index)
        score = g["contribution"].sum()
        counts = f"{len(assoc)} association" + ("s" if len(assoc) != 1 else "")
        if len(other):
            counts += " · " + ", ".join(f"{n} {DIRECTION_TEXT.get(d, d)}" for d, n in other["direction"].value_counts().items())
        regions = ", ".join(sorted({n for n in g["region_name"]}))
        cites = ", ".join(sorted({c for c in g["citation"] if isinstance(c, str)}))
        summary.append((abs(score), f"<tr><td style='padding:4px 8px'><b>{escape(g['target_name'].iloc[0])}</b>"
                                    f" <small style='color:#888'>[{escape(str(g['predicts_kind'].iloc[0]))}]</small></td>"
                                    f"<td style='padding:4px 8px;font-size:12px'>{escape(counts)}</td>"
                                    f"<td style='padding:4px 8px'>{_stars(rules, score)}</td>"
                                    f"<td style='padding:4px 8px;font-size:11px'>{escape(regions)}</td>"
                                    f"<td style='padding:4px 8px;font-size:11px;color:#666'>{escape(cites)}</td></tr>"))
    summary = sorted(summary, key=lambda x: -x[0])[: settings.top_n * 2]
    head = ("<table style='border-collapse:collapse;width:100%;font-size:13px'><tr style='background:#eee'>"
            "<th style='text-align:left;padding:4px 8px'>Damage to these regions was associated with</th>"
            "<th style='text-align:left;padding:4px 8px'>Findings</th><th style='text-align:left;padding:4px 8px'>Evidence</th>"
            "<th style='text-align:left;padding:4px 8px'>Damaged regions involved</th>"
            "<th style='text-align:left;padding:4px 8px'>Citations</th></tr>")
    html = intro + head + "".join(r for _, r in summary) + "</table>"

    # Detail: one block per damaged region, largest damage first.
    blocks = []
    order = (rows.assign(_d=rows["region_pct"].fillna(rows["lesion_pct"]))
             .groupby("anatomy")["_d"].max().sort_values(ascending=False).index)
    review = damage.set_index("region")["review"]
    for key in order:
        g = rows[rows["anatomy"] == key]
        first = g.iloc[0]
        flag = (" <span title='Mapped to the atlas by a judgement call (aphasia-kb/atlas_mapping/README.md)'"
                " style='color:#856404'>⚑</span>") if review.reindex(g["region"].unique()).fillna(False).any() else ""
        studies = g["citation"].dropna().nunique()
        thin = (f" <span title='Few studies: this area is listed in aphasia-kb/atlas_mapping/EVIDENCE_GAPS.md "
                f"or needs more evidence' style='color:#856404;font-size:11px'>⚠ based on {studies} "
                f"stud{'y' if studies == 1 else 'ies'}</span>") if studies <= THIN_STUDIES else ""
        synonyms = names[key][1:]
        also = (f"<div style='font-size:11px;color:#888;margin-left:16px'>Also recorded in the knowledge base as: "
                f"{escape(', '.join(synonyms))}</div>") if synonyms else ""
        blocks.append(f"<details style='margin:4px 0'><summary style='cursor:pointer;font-size:12.5px'>"
                      f"<b>{escape(first['region_name'])}</b> ({escape(first['side'])}){flag}{thin} · "
                      f"{escape(_damage_text(first))} · {len(g)} finding{'s' if len(g) != 1 else ''}</summary>"
                      f"{also}{_claims(g, show_target=True)}</details>")
    html += ("<p style='font-size:12px;color:#555;margin:10px 0 2px 0'><b>Evidence by damaged region</b> "
             "(click a region to see each finding; ⚠ marks regions whose evidence comes from "
             f"{THIN_STUDIES} studies or fewer):</p>" + "".join(blocks))
    return html


def _stars(rules, score):
    stars, label = rules.evidence_strength(score)
    return (f"<span title='raw score {score:+.2f}' style='color:#f0a500'>{'&#9733;' * stars or '&#8212;'}</span> "
            f"<small style='color:#666'>{escape(label)}</small>")


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
    for key, value in (predictors or {}).items():
        pid = kb.resolve_aliases([key]).get(key) or key
        # Findings whose target is the measure itself describe how it is
        # predicted (e.g. models estimating WAB-AQ), not what it implies.
        g = f[(f["source_id"] == pid) & (f["target"] != pid)]
        if g.empty:
            continue
        g = g.assign(target_name=g["target"].map(lambda t: _name(kb, t)))
        polarity = {"higher_is_worse": "higher values go with worse language or recovery",
                    "lower_is_worse": "lower values go with worse language or recovery"}.get(directions.get(pid))
        counts = ", ".join(f"{n} {DIRECTION_TEXT.get(d, d)}" for d, n in g["direction"].value_counts().items())
        caution = ""
        if pid == "severity_metric" and days is not None and days > 180:
            early = g[g["claim"].fillna("").str.contains(EARLY) | (g["target_kind"] == "prognosis")]
            if len(early):
                caution = (f"<div style='font-size:11px;color:#856404;margin-top:3px'>⚠ {len(early)} of these findings "
                           "concern severity measured early after the stroke (or recovery from it); this score was "
                           f"measured {days:.0f} days after the stroke, so they apply only loosely.</div>")
        rows.append(
            f"<tr><td style='padding:6px 8px;vertical-align:top;width:22%'><b>{escape(MEASURE_LABELS.get(pid, _name(kb, pid)))}</b>"
            f"<div style='font-size:12px'>{_value_text(pid, value, days)}</div></td>"
            f"<td style='padding:6px 8px;vertical-align:top'>"
            f"<div style='font-size:12px'>{escape(polarity.capitalize() + '.') if polarity else 'Direction: see each finding.'} "
            f"<span style='color:#666'>({len(g)} findings: {escape(counts)})</span></div>"
            f"<details><summary style='cursor:pointer;font-size:11.5px;color:#1a3a6b'>Show the findings</summary>"
            f"{_claims(g, show_target=True)}</details>{caution}</td></tr>")
    if not rows:
        return "<p style='color:#666'><em>No knowledge-base findings concern this participant's measures.</em></p>"
    return ("<table style='border-collapse:collapse;width:100%;font-size:13px'><tr style='background:#eee'>"
            "<th style='text-align:left;padding:4px 8px'>Measure (this participant)</th>"
            "<th style='text-align:left;padding:4px 8px'>What the evidence says</th></tr>"
            + "".join(rows) + "</table>")


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
    intro = (f"<p style='font-size:12px;color:#555;margin:4px 0 8px 0'>The {escape(map_label)} map gives, for every "
             "voxel, the probability that its fibres pass through the lesion. A tract counts as disconnected when "
             f"&ge;{settings.min_disconnected_pct:g}% of its voxels have a probability above 0.5. This catches tracts "
             "cut by the lesion away from where it lies, which direct overlap misses.</p>")
    if rows is None or rows.empty:
        return intro + "<p style='color:#666'><em>No knowledge-base tract is disconnected above the threshold.</em></p>"
    direct = damage.set_index("region") if damage is not None and len(damage) else None
    rows = rows.assign(target_name=rows["predicts"].map(lambda t: _name(kb, t)),
                       region_name=rows["region"].map(lambda t: _name(kb, t)),
                       anatomy=rows["region"].map(_anatomy_key))
    names = {key: g["region_name"].value_counts().index.tolist() for key, g in rows.groupby("anatomy")}
    blocks = []
    for key in rows.groupby("anatomy")["region_pct"].max().sort_values(ascending=False).index:
        g = rows[rows["anatomy"] == key]
        first = g.iloc[0]
        hit = ""
        if direct is not None:
            destroyed = direct.reindex(g["region"].unique())["region_pct"].dropna()
            if len(destroyed) and destroyed.max() > 0:
                hit = f" · also directly damaged ({destroyed.max():.0f}% destroyed)"
        studies = g["citation"].dropna().nunique()
        thin = (f" <span style='color:#856404;font-size:11px'>⚠ based on {studies} "
                f"stud{'y' if studies == 1 else 'ies'}</span>") if studies <= THIN_STUDIES else ""
        also = (f"<div style='font-size:11px;color:#888;margin-left:16px'>Also recorded in the knowledge base as: "
                f"{escape(', '.join(names[key][1:]))}</div>") if len(names[key]) > 1 else ""
        blocks.append(f"<details style='margin:4px 0'><summary style='cursor:pointer;font-size:12.5px'>"
                      f"<b>{escape(names[key][0])}</b> ({escape(first['side'])}){thin} · "
                      f"{first['region_pct']:.0f}% of the tract disconnected{escape(hit)} · "
                      f"{len(g)} finding{'s' if len(g) != 1 else ''}</summary>{also}{_claims(g, show_target=True)}</details>")
    return intro + "".join(blocks)
