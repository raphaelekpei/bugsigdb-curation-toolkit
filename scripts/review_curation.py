#!/usr/bin/env python3
"""Mechanical half of a senior-reviewer pass on a local curation.json (see references/reviewer.md).

Usage: python3 -I scripts/review_curation.py curation.json [paper.txt|paper.pdf ...] [--offline]

Runs check_curation.py and verify_evidence.py, then adds the checks a mentor makes on the
live site: every NCBI ID resolved against NCBI (name, rank, strain/CAG IDs where a species is
meant), text taxa looked up for a missing ID, condition and body site confirmed as selectable
glossary terms (Category:Condition / Category:Body site), vague or punctuated sources, and
page states. Every finding is mapped to its rubric item (1-19) and printed as a table, so the
reviewer starts the judgment pass from a complete mechanical list.
Needs network access to NCBI and bugsigdb.org unless --offline.
"""
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEMS = {1: "All elements Needs review / Complete", 2: "Study design", 3: "All relevant experiments, none irrelevant",
         4: "Body site", 5: "Condition (EFO, per contrast)", 6: "Contrast groups (names, definitions, n)",
         7: "Groups labelled 1 / 0", 8: "Antibiotics exclusion", 9: "Sequencing details", 10: "Statistical test",
         11: "MHT correction", 12: "Matched on", 13: "Number of statistical tests", 14: "Diversity measures identified",
         15: "Diversity directions", 16: "Signature sources", 17: "Abundance direction", 18: "Signature members",
         19: "NCBI taxonomy", 0: "Not a rubric item (format, description, confounders, transformation)"}

# message keyword -> rubric item, first match wins
ROUTES = [(r"study design", 2), (r"[Bb]ody site", 4), (r"[Cc]ondition", 5), (r"group_[01]_|Group [01]|sample size|definition", 6),
          (r"[Aa]ntibiotic", 8), (r"16S|[Ss]equencing|platform|variable region", 9), (r"MHT", 11), (r"[Mm]atched", 12),
          (r"[Ss]tatistical test|LEfSe does not|DESeq2", 10), (r"[Aa]lpha diversity", 14), (r"No signatures", 3), (r"Only one signature", 18), (r"signatures?:|Signature 1|same direction", 17),
          (r"NCBI|taxid|taxon|underscore", 19), (r"[Ss]ource", 16), (r"Incomplete|State", 1)]


def route(msg):
    for pat, item in ROUTES:
        if re.search(pat, msg):
            return item
    return 0


def get_json(url, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (bugsigdb-review)"})
            return json.load(urllib.request.urlopen(req, timeout=60))
        except Exception:
            time.sleep(2.0 * (i + 1))
    return None


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return (p.stdout or "") + (p.stderr or "")


def ncbi_checks(cur, findings):
    taxa = [(e.get("id"), j, t) for e in cur.get("experiments", []) for j, s in enumerate(e.get("signatures", []), 1) for t in s.get("taxa", [])]
    ids = sorted({str(t.get("ncbi_id")) for _, _, t in taxa if str(t.get("ncbi_id") or "").isdigit()})
    info, failed = {}, set()
    for i in range(0, len(ids), 150):
        chunk = ids[i:i + 150]
        r = get_json("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=taxonomy&retmode=json&id=" + ",".join(chunk))
        res = (r or {}).get("result", {})
        if res.get("uids"):
            info.update({k: res[k] for k in chunk if k in res})
        else:
            # E-utilities' docsum backend sometimes returns an empty result instead of an error: fall back to NCBI Datasets
            d = get_json("https://api.ncbi.nlm.nih.gov/datasets/v2/taxonomy/taxon/" + ",".join(chunk))
            for n in (d or {}).get("taxonomy_nodes", []):
                t = n.get("taxonomy") or {}
                if t.get("tax_id"):
                    info[str(t["tax_id"])] = {"scientificname": t.get("organism_name", ""), "rank": (t.get("rank") or "").lower()}
            if not d:
                failed.update(chunk)
        time.sleep(0.35)
    if failed:
        findings.append((19, "WARN", "NCBI", f"lookup failed for {len(failed)} IDs (network or rate limit); re-run before trusting item 19"))
    for eid, sig, t in taxa:
        w = f"Exp {eid} / Sig {sig}"
        tid, name = str(t.get("ncbi_id") or ""), (t.get("name") or "").strip()
        pname = (t.get("paper_name") or "").strip()
        if tid.isdigit():
            if tid in failed:
                continue
            r = info.get(tid)
            if not r or r.get("error"):
                findings.append((19, "ERROR", w, f"NCBI {tid} ({name}) doesn't resolve in NCBI Taxonomy"))
                continue
            sci, rank = r.get("scientificname", ""), r.get("rank", "")
            if name and sci and name.lower() not in sci.lower() and sci.lower() not in name.lower():
                findings.append((19, "WARN", w, f"NCBI {tid} is '{sci}' ({rank}), but the curation calls it '{name}'; confirm it's a synonym, not a wrong ID"))
            if rank in ("strain", "isolate", "serotype") or re.search(r"\bCAG[: ]?\d|\bstr\.|\bATCC\b|\bDSM\b", sci):
                if not (pname and re.search(r"\bCAG[: ]?\d|\bstr\.|strain", pname, re.I)):
                    findings.append((19, "WARN", w, f"NCBI {tid} '{sci}' is a strain/CAG node; if the paper names the species, use the species ID"))
        else:
            if not name:
                continue
            q = re.sub(r"^(unclassified|uncultured|unidentified)[ _]+", "", name, flags=re.I).replace("_", " ")
            r = get_json("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=taxonomy&retmode=json&term=" + urllib.parse.quote(q + "[All Names]"))
            time.sleep(0.35)
            hit = (r or {}).get("esearchresult", {}).get("idlist", [])
            if hit:
                findings.append((19, "WARN", w, f"'{name}' entered as text, but NCBI has '{q}' (ID {hit[0]}); use the ID unless the text is deliberate (GTDB suffix, placeholder) and noted"))


def glossary_checks(cur, findings):
    API = "https://bugsigdb.org/w/api.php?"
    seen = {}
    for e in cur.get("experiments", []):
        for field, cat, item in (("condition", "Category:Condition", 5), ("body_site", "Category:Body site", 4)):
            v = (e.get(field) or "").strip()
            # body site is multi-valued ("Endometrium, Endometrial cavity"): check each term
            terms = [t.strip() for t in v.split(",") if t.strip()] if field == "body_site" else ([v] if v else [])
            for v in terms:
                if v not in seen:
                    r = get_json(API + urllib.parse.urlencode({"action": "query", "titles": v, "prop": "categories", "redirects": 1, "format": "json", "formatversion": 2}))
                    p = ((r or {}).get("query", {}).get("pages") or [{}])[0]
                    seen[v] = "missing" if p.get("missing") else ("ok" if cat in [c["title"] for c in p.get("categories", [])] else "not-selectable")
                    time.sleep(0.2)
                if seen[v] != "ok":
                    findings.append((item, "ERROR" if seen[v] == "missing" else "WARN", f"Exp {e.get('id')}",
                                     f"{field} '{v}' {'has no glossary page' if seen[v] == 'missing' else 'is not in ' + cat + ' (the form may not offer it)'}"))


def source_and_state_checks(cur, findings):
    st = (cur.get("study") or {}).get("state")
    if st and st.lower() != "complete":
        findings.append((1, "ERROR", "Study", f"State '{st}', not Complete"))
    for e in cur.get("experiments", []):
        w = f"Exp {e.get('id')}"
        if e.get("state") and e["state"].lower() != "complete":
            findings.append((1, "ERROR", w, f"State '{e['state']}', not Complete"))
        for j, s in enumerate(e.get("signatures", []), 1):
            ws, src = f"{w} / Sig {j}", (s.get("source") or "").strip()
            if s.get("state") and s["state"].lower() != "complete":
                findings.append((1, "ERROR", ws, f"State '{s['state']}', not Complete"))
            if not src:
                findings.append((16, "ERROR", ws, "Source is empty"))
            elif re.fullmatch(r"(Results?( section)?|Text|Main text|Discussion|Paper)\.?", src, re.I):
                findings.append((16, "ERROR", ws, f"Source '{src}' is too broad; name the exact figure/table, or 'Text; RESULTS: <heading>'"))
            elif re.search(r"[,;.:]\s*$|^\s*[,;\"']|\"", src):
                findings.append((16, "WARN", ws, f"Source '{src}' has stray punctuation"))
            if len(s.get("description") or "") > 250:
                findings.append((0, "WARN", ws, f"Description is {len(s['description'])} characters; mentors ask for concise descriptions (#449)"))


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    path, sources = args[0], args[1:]
    cur = json.load(open(path))
    findings = []
    out = run([sys.executable, "-I", str(HERE / "check_curation.py"), path])
    for line in out.splitlines():
        m = re.match(r"(ERROR|WARN)\s*\|\s*(.*?)\s*\|\s*(.*)", line)
        if m and not re.search(r"form order|missing form fields|LOW CONFIDENCE|confidence|rulings_checked", m.group(3)):
            findings.append((route(m.group(3)), m.group(1), m.group(2), m.group(3)))
    if sources and any("evidence" in e for e in cur.get("experiments", [])):
        out = run([sys.executable, "-I", str(HERE / "verify_evidence.py"), path, *sources])
        for line in out.splitlines():
            if line.startswith(("MISSING", "NOT FOUND")):
                findings.append((0, "ERROR", "evidence", line))
    source_and_state_checks(cur, findings)
    if "--offline" not in argv:
        ncbi_checks(cur, findings)
        glossary_checks(cur, findings)
    print(f"# Mechanical review: {path}\n")
    print("| Item | Rubric item | Errors | Warnings |\n|---|---|---|---|")
    for i in list(range(1, 20)) + [0]:
        e = sum(1 for f in findings if f[0] == i and f[1] == "ERROR")
        wn = sum(1 for f in findings if f[0] == i and f[1] == "WARN")
        if e or wn or i:
            print(f"| {i or '-'} | {ITEMS[i]} | {e} | {wn} |")
    print()
    for i in list(range(1, 20)) + [0]:
        fs = [f for f in findings if f[0] == i]
        if fs:
            print(f"## Item {i or '-'}: {ITEMS[i]}")
            for _, lvl, w, msg in fs:
                print(f"- {lvl} | {w} | {msg}")
            print()
    print("Mechanical checks only. Items 3, 6, 7, 10, 13-18 need the judgment pass in references/reviewer.md.")
    return 1 if any(f[1] == "ERROR" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
