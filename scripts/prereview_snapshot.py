#!/usr/bin/env python3
"""Rebuild a BugSigDB study as it stood at a given moment (e.g. just before a mentor's review).

Usage: python3 -I scripts/prereview_snapshot.py <PMID> <ISO time, e.g. 2026-10-26T12:45:36Z> <out dir>

Writes <out>/pages.json (the latest revision of every page at that time), <out>/curation.json in
this skill's format (taxa resolved to NCBI names and ranks), and <out>/paper/paper.txt from PMC.
Used to test the reviewer (references/reviewer.md §7): give a fresh agent the snapshot and the
paper, then compare its findings with the mentor's comment.
Limits: pages deleted since then have no public history and are missing; PMC author manuscripts
and some publishers block scripted downloads of figures and supplements, so ask the user for them.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://bugsigdb.org/w/api.php"
UA = {"User-Agent": "Mozilla/5.0 (bugsigdb-curation snapshot)"}
VOCAB = Path(__file__).resolve().parent.parent / "references" / "controlled-vocabularies.md"


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()


def call(**p):
    p.update(format="json", formatversion=2)
    return json.loads(get(API + "?" + urllib.parse.urlencode(p)))


def fields(w):
    out = {}
    for part in w.split("\n|")[1:]:
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip().rstrip("}").strip()
    return out


def designs():
    vals, head = [], ""
    for line in VOCAB.read_text().splitlines():
        if line.startswith("## "):
            head = line
        elif line.startswith("- ") and re.search(r"[Ss]tudy design", head):
            vals.append(line[2:].strip())
    return vals


def split_list(v):
    return [x.strip() for x in v.split(",") if x.strip()] if v else []


def split_designs(v, known):
    # dropdown values contain commas ("cross-sectional observational, not case-control"): match known values first
    out, rest = [], v or ""
    for k in sorted(known, key=len, reverse=True):
        if k in rest:
            out.append(k)
            rest = rest.replace(k, "")
    return out + split_list(rest.strip(", "))


def main(argv):
    if len(argv) != 4:
        print(__doc__)
        return 2
    pmid, when, out = argv[1:]
    os.makedirs(out, exist_ok=True)
    titles = [p["title"] for p in call(action="query", list="allpages", apprefix=pmid, aplimit=500)["query"]["allpages"]
              if p["title"] == pmid or p["title"].startswith(pmid + "/")]
    pages, later = {}, []
    for t in titles:
        r = call(action="query", prop="revisions", titles=t, rvlimit=1, rvprop="timestamp|content|user", rvslots="main", rvdir="older", rvstart=when)
        revs = r["query"]["pages"][0].get("revisions", [])
        if revs:
            pages[t] = {"timestamp": revs[0]["timestamp"], "user": revs[0]["user"], "wikitext": revs[0]["slots"]["main"]["content"]}
        else:
            later.append(t)
    json.dump(pages, open(f"{out}/pages.json", "w"), indent=1)
    ids = sorted({x for t, p in pages.items() if "/Signature" in t for x in split_list(fields(p["wikitext"]).get("NCBI", "")) if x.isdigit()})
    names = {}
    for i in range(0, len(ids), 150):
        r = json.loads(get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=taxonomy&retmode=json&id=" + ",".join(ids[i:i + 150])))["result"]
        names.update({k: (r[k].get("scientificname"), r[k].get("rank")) for k in ids[i:i + 150] if k in r})
        time.sleep(0.4)
    st = fields(pages.get(pmid, {"wikitext": ""})["wikitext"])
    cur = {"study": {"pmid": pmid, "study_design": split_designs(st.get("study design", ""), designs()), "state": st.get("State", "")}, "experiments": []}
    km = {"Location of subjects": "location_of_subjects", "Host species": "host_species", "Body site": "body_site", "Condition": "condition",
          "Group 0 name": "group_0_name", "Group 1 name": "group_1_name", "Group 1 definition": "group_1_definition",
          "Group 0 sample size": "group_0_sample_size", "Group 1 sample size": "group_1_sample_size", "Antibiotics exclusion": "antibiotics_exclusion",
          "Sequencing type": "sequencing_type", "16S variable region (lower bound)": "variable_region_lower",
          "16S variable region (upper bound)": "variable_region_upper", "Sequencing platform": "sequencing_platform",
          "Data transformation": "data_transformation", "Statistical test": "statistical_test", "Significance threshold": "significance_threshold",
          "MHT correction": "mht_correction", "LDA Score above": "lda_score_above", "Matched on": "matched_on",
          "Confounders controlled for": "confounders_controlled_for"}
    listy = {"location_of_subjects", "sequencing_platform", "statistical_test", "matched_on", "confounders_controlled_for"}
    for n in sorted({re.match(r".*/Experiment (\d+)", t).group(1) for t in pages if "/Experiment" in t}, key=int):
        t = f"{pmid}/Experiment {n}"
        if t not in pages:
            continue
        f = fields(pages[t]["wikitext"])
        e = {"id": int(n)}
        for k, ck in km.items():
            v = f.get(k, "")
            e[ck] = split_list(v) if ck in listy else (v or None)
        e["alpha_diversity"] = {a: f[a] for a in ("Pielou", "Shannon", "Chao1", "Simpson", "Inverse Simpson", "Richness", "Faith") if f.get(a)}
        e["state"], e["signatures"] = f.get("State", ""), []
        for s in sorted([x for x in pages if x.startswith(t + "/Signature")], key=lambda x: int(x.split()[-1])):
            g = fields(pages[s]["wikitext"])
            taxa = [{"name": names.get(x, (None, None))[0], "rank": names.get(x, (None, None))[1], "ncbi_id": x} if x.isdigit()
                    else {"name": x, "rank": None, "ncbi_id": ""} for x in split_list(g.get("NCBI", ""))]
            e["signatures"].append({"page": s, "source": g.get("Source", ""), "description": g.get("Description", ""),
                                    "abundance_in_group_1": g.get("Abundance in Group 1", ""), "taxa": taxa, "state": g.get("State", "")})
        cur["experiments"].append(e)
    json.dump(cur, open(f"{out}/curation.json", "w"), indent=1, ensure_ascii=False)
    os.makedirs(f"{out}/paper", exist_ok=True)
    try:
        pmc = json.loads(get(f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={pmid}&format=json"))["records"][0].get("pmcid")
        x = get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={pmc}").decode("utf-8", "ignore")
        txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))
        open(f"{out}/paper/paper.txt", "w").write(txt)
    except Exception as ex:
        pmc, txt = None, ""
    print(f"{pmid} at {when}: {len(pages)} pages, {len(cur['experiments'])} experiments; created later (excluded): {len(later)}; "
          f"PMC {pmc}, text {len(txt)} chars{' (abstract only? fetch the article page or ask the user)' if 0 < len(txt) < 10000 else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
