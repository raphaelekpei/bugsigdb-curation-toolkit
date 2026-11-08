#!/usr/bin/env python3
"""Audit a curation as it is LIVE on bugsigdb.org (what reviewers actually see).

Usage: python scripts/check_live.py <PMID or page name> [curation.json]

Catches data-entry errors that a correct local curation can't:
  - NCBI fields holding taxon NAMES instead of numeric IDs (typed without autocomplete,
    so stored as plain text and not linked to the NCBI taxonomy)
  - duplicate signatures (same source, direction and taxa) within an experiment
  - pages left "Incomplete"
  - stray characters from copy-paste (quotes, commas, brackets at the end of values)
  - with curation.json: fields whose live value differs from the curation
Needs network access to https://bugsigdb.org.
"""
import json
import re
import sys
import urllib.parse
import urllib.request

API = "https://bugsigdb.org/w/api.php"


def call(**params):
    params.update(format="json", formatversion=2)
    req = urllib.request.Request(f"{API}?{urllib.parse.urlencode(params)}", headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=30))


def fields(wikitext):
    out = {}
    for part in wikitext.split("\n|")[1:]:
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip().rstrip("}").strip()
    return out


def norm_name(n):
    """Compare taxon names loosely: case, underscores and hyphens vs spaces."""
    return re.sub(r"[\s_-]+", " ", str(n)).strip().lower()


def norm_list(v):
    """Multi-value fields: the site joins with ', ' or '; '. Compare as a sorted set of parts."""
    return sorted(p.strip().lower() for p in re.split(r"\s*[;,]\s*", str(v)) if p.strip())


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    base = argv[1]
    titles = [p["title"] for p in call(action="query", list="allpages", apprefix=base, aplimit=500)["query"]["allpages"]
              if p["title"] == base or p["title"].startswith(base + "/")]
    if not titles:
        print(f"No pages found for {base}")
        return 1
    pages = {t: fields(call(action="parse", page=t, prop="wikitext").get("parse", {}).get("wikitext", "")) for t in titles}
    cur = json.load(open(argv[2])) if len(argv) > 2 else None
    # Taxa the curation deliberately enters as text (no NCBI node: SILVA groups, GTDB splits, placeholders).
    text_taxa = set()
    for e in (cur or {}).get("experiments", []):
        for sg in e.get("signatures", []):
            for x in sg.get("taxa", []):
                if not x.get("ncbi_id"):
                    text_taxa.update(norm_name(n) for n in (x.get("name"), x.get("paper_name")) if n)
    issues = []
    for t, f in pages.items():
        if f.get("State", "").lower() != "complete":
            issues.append(("ERROR", t, f"State is '{f.get('State', '')}', not Complete"))
        for k, v in f.items():
            if k in ("Description",):
                continue
            if re.search(r'["“”]\s*,?\s*$|,\s*$|^\s*[",]', v):
                issues.append(("ERROR", t, f"{k} has stray characters: {v!r}"))
        if "/Signature" in t:
            for tok in [x.strip() for x in f.get("NCBI", "").split(",") if x.strip()]:
                if tok.isdigit():
                    continue
                if norm_name(tok) in text_taxa:
                    issues.append(("INFO", t, f"NCBI entry '{tok}' is text, as intended in curation.json (no NCBI node); keep a discussion note"))
                else:
                    issues.append(("ERROR", t, f"NCBI entry '{tok}' is text, not a numeric ID: paste the taxid so it links to NCBI"))
    # duplicate signatures within an experiment
    sigs = {}
    for t, f in pages.items():
        m = re.match(r"(.*/Experiment \d+)/Signature \d+$", t)
        if m:
            key = (m.group(1), f.get("Source", ""), f.get("Abundance in Group 1", ""), ",".join(sorted(x.strip() for x in f.get("NCBI", "").split(","))))
            sigs.setdefault(key, []).append(t)
    for key, ts in sigs.items():
        if len(ts) > 1:
            issues.append(("ERROR", ", ".join(ts), "duplicate signatures: request deletion of the extra one(s) on GitHub (give the full URL)"))
    dirs = {}
    for t, f in pages.items():
        m = re.match(r"(.*/Experiment \d+)/Signature \d+$", t)
        if m:
            dirs.setdefault(m.group(1), []).append(f.get("Abundance in Group 1", ""))
    for exp, ds in dirs.items():
        if len(ds) != len(set(ds)):
            issues.append(("ERROR", exp, f"two signatures share a direction ({ds}): at most one increased and one decreased"))
    # compare with the local curation
    if cur is not None:
        # every Experiment form field (42857727: comparing only 9 fields hid live differences in
        # transformation, threshold, confounders and alpha diversity)
        keymap = {"Location of subjects": "location_of_subjects", "Host species": "host_species", "Body site": "body_site",
                  "Condition": "condition", "Group 0 name": "group_0_name", "Group 1 name": "group_1_name",
                  "Group 1 definition": "group_1_definition", "Group 0 sample size": "group_0_sample_size",
                  "Group 1 sample size": "group_1_sample_size", "Antibiotics exclusion": "antibiotics_exclusion",
                  "Sequencing type": "sequencing_type", "16S variable region (lower bound)": "variable_region_lower",
                  "16S variable region (upper bound)": "variable_region_upper", "Sequencing platform": "sequencing_platform",
                  "Data transformation": "data_transformation", "Statistical test": "statistical_test",
                  "Significance threshold": "significance_threshold", "MHT correction": "mht_correction",
                  "LDA Score above": "lda_score_above", "Matched on": "matched_on",
                  "Confounders controlled for": "confounders_controlled_for"}
        alpha = ["Pielou", "Shannon", "Chao1", "Simpson", "Inverse Simpson", "Richness", "Faith"]
        for e in cur.get("experiments", []):
            t = f"{base}/Experiment {e['id']}"
            live = pages.get(t)
            if live is None:
                issues.append(("WARN", t, "in curation.json but not on the site"))
                continue
            for lk, ck in keymap.items():
                lv = live.get(lk, "")
                cv = e.get(ck)
                cv = "; ".join(map(str, cv)) if isinstance(cv, list) else ("" if cv is None else str(cv))
                if lk == "MHT correction":
                    lv = {"yes": "Yes", "no": "No", "true": "Yes", "false": "No"}.get(lv.lower(), lv)
                if norm_list(lv) != norm_list(cv):
                    issues.append(("WARN", t, f"{lk}: site={lv!r} vs curation={cv!r}"))
            for a in alpha:
                lv, cv = live.get(a, ""), (e.get("alpha_diversity") or {}).get(a) or ""
                if lv.lower() != cv.lower():
                    issues.append(("WARN", t, f"{a}: site={lv!r} vs curation={cv!r}"))
            for j, s in enumerate(e.get("signatures", []), 1):
                ids = sorted(str(x["ncbi_id"]) if x.get("ncbi_id") else norm_name(x.get("name", "")) for x in s.get("taxa", []))
                match = [tt for tt, f in pages.items() if tt.startswith(t + "/Signature") and f.get("Abundance in Group 1") == s["abundance_in_group_1"]]
                if not match:
                    issues.append(("WARN", t, f"no {s['abundance_in_group_1']} signature on the site"))
                    continue
                live_ids = sorted(x.strip() if x.strip().isdigit() else norm_name(x) for x in pages[match[0]].get("NCBI", "").split(",") if x.strip())
                if live_ids != ids:
                    issues.append(("WARN", match[0], f"NCBI differs: site={live_ids} vs curation={ids}"))
                if pages[match[0]].get("Source", "") != s.get("source", ""):
                    issues.append(("WARN", match[0], f"Source: site={pages[match[0]].get('Source', '')!r} vs curation={s.get('source')!r}"))
    print(f"{len(pages)} live pages checked for {base}")
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    for lvl, where, msg in sorted(issues, key=lambda x: (order[x[0]], x[1])):
        print(f"{lvl:5} | {where} | {msg}")
    print(f"\n{sum(1 for i in issues if i[0] == 'ERROR')} error(s), {sum(1 for i in issues if i[0] == 'WARN')} warning(s).")
    return 1 if any(i[0] == "ERROR" for i in issues) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
