#!/usr/bin/env python3
"""Render a curation JSON as BugSigDB form entries, field by field in on-screen order.

Usage: python scripts/render_forms.py curation.json [--signatures-only] > FORMS.md
       python scripts/render_forms.py curation.json --sheet [--pdf paper.pdf] > experiment_section.md
         (--sheet: per-experiment tables in Create Experiment form order with Value / Conf. /
          Evidence columns, PDF page numbers looked up automatically, notes, and signature blocks)

Signature blocks follow the "Create Signature" form exactly:
    Source / Description / Abundance in Group 1 / NCBI / Form data (Incomplete -> Complete)
Experiment blocks follow Form:Experiment (subjects, lab analysis, statistical analysis,
alpha diversity). Blank fields are shown as "(leave blank)" so nothing is typed by mistake.
NCBI is given as comma-separated integer taxids (BugSigDB bulk entry), followed by a
name check list so each ID can be confirmed after autocomplete resolves it.
"""
import json
import sys
from pathlib import Path

BLANK = "(leave blank)"
STATE_LINE = "Form data: This form's data is:  Complete   (keep \"Incomplete\" while still working)"

EXPERIMENT_FIELDS = [
    ("Location of subjects", "location_of_subjects"),
    ("Host species", "host_species"),
    ("Body site", "body_site"),
    ("Condition", "condition"),
    ("Group 0 name", "group_0_name"),
    ("Group 1 name", "group_1_name"),
    ("Group 1 definition", "group_1_definition"),
    ("Group 0 sample size", "group_0_sample_size"),
    ("Group 1 sample size", "group_1_sample_size"),
    ("Antibiotics exclusion", "antibiotics_exclusion"),
    None,  # Lab analysis
    ("Sequencing type", "sequencing_type"),
    ("16S variable region (lower bound)", "variable_region_lower"),
    ("16S variable region (upper bound - only set if needed)", "variable_region_upper"),
    ("Sequencing platform", "sequencing_platform"),
    None,  # Statistical Analysis
    ("Data transformation", "data_transformation"),
    ("Statistical test", "statistical_test"),
    ("Significance threshold", "significance_threshold"),
    ("MHT correction", "mht_correction"),
    ("LDA Score above", "lda_score_above"),
    ("Matched on", "matched_on"),
    ("Confounders controlled for", "confounders_controlled_for"),
]
SECTION_TITLES = ["Lab analysis", "Statistical Analysis"]
ALPHA = ["Pielou", "Shannon", "Chao1", "Simpson", "Inverse Simpson", "Richness", "Faith"]


def fmt(v):
    if v is None or v == "" or v == []:
        return BLANK
    if isinstance(v, list):
        return "; ".join(str(x) for x in v)
    if isinstance(v, (int, float)) and not isinstance(v, bool) and str(v).isdigit() is False:
        return str(v)
    return str(v)


def render_signature(s):
    taxa = s.get("taxa") or []
    ids = [str(t.get("ncbi_id")) for t in taxa if t.get("ncbi_id")]
    unresolved = [t for t in taxa if not t.get("ncbi_id")]
    lines = [
        "```",
        f"Source:                {fmt(s.get('source'))}",
        f"Description:           {fmt(s.get('description'))}",
        f"Abundance in Group 1:  {fmt(s.get('abundance_in_group_1'))}",
        f"NCBI:                  {', '.join(ids + [str(t.get('name')) for t in unresolved]) or BLANK}",
        "",
        STATE_LINE,
        "```",
    ]
    if taxa:
        lines.append(f"Check after autocomplete ({len(taxa)} {'taxon' if len(taxa) == 1 else 'taxa'}):")
        for t in taxa:
            rank = f", {t['rank']}" if t.get("rank") else ""
            paper = f"; paper: {t['paper_name']}" if t.get("paper_name") and t.get("paper_name") != t.get("name") else ""
            lines.append(f"- {t.get('ncbi_id') or 'no ID: type the name as text'} = {t.get('name')}{rank}{paper}")
    if unresolved:
        lines.append(f"- **{len(unresolved)} taxon(s) without an NCBI ID**: type the name exactly as written above.")
    return "\n".join(lines)


def render_experiment(e):
    out, section = ["```"], 0
    for f in EXPERIMENT_FIELDS:
        if f is None:
            out.append(f"\n-- {SECTION_TITLES[section]} --")
            section += 1
            continue
        label, key = f
        val = e.get(key)
        if key == "variable_region_lower" and e.get("sequencing_type") != "16S":
            continue
        if key == "variable_region_upper" and e.get("sequencing_type") != "16S":
            continue
        if key.startswith("variable_region") and val not in (None, ""):
            val = f"V{val}"
        out.append(f"{label + ':':<56}{fmt(val)}")
    out.append("\n-- Alpha Diversity --")
    alpha = e.get("alpha_diversity") or {}
    for a in ALPHA:
        out.append(f"{a + ':':<56}{alpha.get(a, BLANK)}")
    out.append("\n" + STATE_LINE)
    out.append("```")
    return "\n".join(out)


# --sheet mode: Create Experiment form order, with confidence and evidence per field
SHEET_FIELDS = [  # (form label, value key, confidence keys, evidence keys)
    ("Location of subjects", "location_of_subjects", ["location_of_subjects"], ["location_of_subjects"]),
    ("Host species", "host_species", ["host_species"], ["host_species"]),
    ("Body site", "body_site", ["body_site"], ["body_site"]),
    ("Condition", "condition", ["condition"], ["condition"]),
    ("Group 0 name", "group_0_name", ["group_names"], ["group_names"]),
    ("Group 1 name", "group_1_name", ["group_names"], []),
    ("Group 1 definition", "group_1_definition", ["group_1_definition"], ["group_1_definition"]),
    ("Group 0 sample size", "group_0_sample_size", ["sample_sizes"], ["sample_sizes", "n", "n_figure"]),
    ("Group 1 sample size", "group_1_sample_size", ["sample_sizes"], []),
    ("Antibiotics exclusion", "antibiotics_exclusion", ["antibiotics_exclusion"], ["antibiotics_exclusion"]),
    ("Sequencing type", "sequencing_type", ["sequencing_type"], []),
    ("16S variable region (lower bound)", "variable_region_lower", ["variable_region"], []),
    ("16S variable region (upper bound)", "variable_region_upper", ["variable_region"], []),
    ("Sequencing platform", "sequencing_platform", ["sequencing_platform"], []),
    ("Data transformation", "data_transformation", ["data_transformation"], ["data_transformation"]),
    ("Statistical test", "statistical_test", ["statistical_test"], ["statistical_test", "test", "poisson", "model"]),
    ("Significance threshold", "significance_threshold", ["significance_threshold"], ["significance_threshold"]),
    ("MHT correction", "mht_correction", ["mht_correction"], ["mht_correction", "mht"]),
    ("LDA Score above", "lda_score_above", [], []),
    ("Matched on", "matched_on", ["matched_on"], ["matched_on"]),
    ("Confounders controlled for", "confounders_controlled_for", ["confounders_controlled_for"], ["confounders"]),
]


def _pages(pdf):
    if not pdf:
        return None
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    import re
    import unicodedata

    def norm(s):
        s = unicodedata.normalize("NFKC", s)
        s = re.sub(r"[‐-―−]", "-", s).replace("’", "'")
        s = re.sub(r"\s+", " ", s)
        return re.sub(r"\s*([()\[\],;:<>=±-])\s*", r"\1", s).lower()
    pages = [norm(p.extract_text() or "") for p in PdfReader(pdf).pages]
    return pages, norm


def _cite(q, pg):
    q = str(q)
    if q.startswith("["):  # [figure] / [code] / [glossary] notes are printed as-is
        return q
    if not pg:
        return f'"{q}"'
    pages, norm = pg
    frags = [f for f in q.replace("...", "…").split("…") if len(f.strip()) > 5]
    hits = sorted({i + 1 for f in frags for i, p in enumerate(pages) if norm(f) in p})
    where = f" (p.{','.join(map(str, hits))})" if hits else ""
    return f'"{q}"{where}'


def _cites(v, pg):
    return "; ".join(_cite(x, pg) for x in (v if isinstance(v, list) else [v])).replace("|", "\\|")


def render_sheet_experiment(e, pg):
    ev, cf = e.get("evidence") or {}, e.get("confidence") or {}
    used = {"signature"}
    seq = ev.get("sequencing")
    seq = seq if isinstance(seq, list) else ([seq] if seq else [])
    if seq:
        used.add("sequencing")
    rows = ["| Field | Value | Conf. | Evidence |", "|---|---|---|---|"]
    for label, key, ckeys, ekeys in SHEET_FIELDS:
        if key.startswith("variable_region") and e.get("sequencing_type") != "16S":
            continue
        val = e.get(key)
        if key.startswith("variable_region") and val not in (None, ""):
            val = f"V{val}"
        conf = next((str(cf[k]) for k in ckeys if k in cf), "")
        quotes = []
        if key == "sequencing_type":
            quotes = seq[:1]
        elif key == "variable_region_lower":
            quotes = seq[:1]
        elif key == "sequencing_platform":
            quotes = seq[1:]
        for k in ekeys:
            if k in ev and k not in used:
                used.add(k)
                quotes += ev[k] if isinstance(ev[k], list) else [ev[k]]
        rows.append(f"| {label} | **{fmt(val)}** | {conf} | {_cites(quotes, pg) if quotes else ''} |")
    alpha = e.get("alpha_diversity") or {}
    first = next((a for a in ALPHA if a in alpha), "Pielou")
    for a in ALPHA:
        cell, conf = "", ""
        if a == first:
            conf = str(cf.get("alpha_diversity", ""))
            if "alpha_diversity" in ev:
                used.add("alpha_diversity")
                cell = _cites(ev["alpha_diversity"], pg)
        rows.append(f"| {a} | **{alpha.get(a, BLANK)}** | {conf} | {cell} |")
    other = [k for k in ev if k not in used]
    out = "\n".join(rows)
    if e.get("notes") or other:
        out += "\n\n**Notes**\n" + "\n".join(f"- {n}" for n in e.get("notes", []))
        out += "".join(f"\n- Evidence ({k}): {_cite(v, pg) if not isinstance(v, list) else '; '.join(_cite(x, pg) for x in v)}" for k, v in ((k, ev[k]) for k in other))
    return out


def render_sheet_signature(s, ev_sig, pg):
    block = render_signature(s).split("Check after autocomplete")[0].rstrip()
    taxa = s.get("taxa") or []
    rows = [f"\n{len(taxa)} {'taxon' if len(taxa) == 1 else 'taxa'} (check each ID after autocomplete):\n",
            "| NCBI | Name to enter | Rank | As in paper | Evidence |", "|---|---|---|---|---|"]
    for t in taxa:
        rows.append(f"| {t.get('ncbi_id') or '—'} | {t.get('name')} | {t.get('rank', '')} | {t.get('paper_name', t.get('name'))} | {t.get('evidence', '')} |")
    return block + "\n" + "\n".join(rows)


def main_sheet(data, pdf):
    pg = _pages(pdf)
    for e in data.get("experiments", []):
        name = f"{e.get('group_0_name', '?')} vs {e.get('group_1_name', '?')}"
        print(f"### Experiment {e.get('id')}: {name}\n")
        print("*Fields in Create Experiment form order.*\n")
        print(render_sheet_experiment(e, pg) + "\n")
        sig_ev = (e.get("evidence") or {}).get("signature")
        if sig_ev:
            print("Signature evidence: " + ("; ".join(_cite(x, pg) for x in sig_ev) if isinstance(sig_ev, list) else _cite(sig_ev, pg)) + "\n")
        for j, s in enumerate(e.get("signatures") or [], 1):
            print(f"#### Experiment {e.get('id')}, Signature {j} ({s.get('abundance_in_group_1')})\n")
            print(render_sheet_signature(s, sig_ev, pg) + "\n")
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    # The JSON path may come before or after the flags; skip the value that follows --pdf.
    args = [a for i, a in enumerate(argv[1:], 1) if not a.startswith("--") and argv[i - 1] != "--pdf"]
    if not args:
        print(__doc__)
        return 2
    data = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    if "--sheet" in argv:
        pdf = argv[argv.index("--pdf") + 1] if "--pdf" in argv else None
        return main_sheet(data, pdf)
    sig_only = "--signatures-only" in argv
    st = data.get("study", {})
    print(f"# BugSigDB form entries: {st.get('pmid') or st.get('page_name', '')}\n")
    if not sig_only:
        print("## Study (Add a Study form)\n```")
        print(f"{'PMID:':<22}{st.get('pmid', BLANK)}")
        print(f"{'Mode:':<22}{st.get('citation_mode', 'Auto')}")
        print(f"{'study design:':<22}{fmt(st.get('study_design'))}")
        print("\n" + STATE_LINE)
        print("```\n")
    for e in data.get("experiments", []):
        name = f"{e.get('group_0_name', '?')} vs {e.get('group_1_name', '?')}"
        print(f"## Experiment {e.get('id')}: {name}\n")
        if not sig_only:
            print(render_experiment(e) + "\n")
        for j, s in enumerate(e.get("signatures") or [], 1):
            print(f"### Experiment {e.get('id')}, Signature {j} ({s.get('abundance_in_group_1')})\n")
            print(render_signature(s) + "\n")
    print("Set the form state switch to **Complete** on the study, every experiment and every signature when finished.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
