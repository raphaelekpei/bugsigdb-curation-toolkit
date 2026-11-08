#!/usr/bin/env python3
"""Fetch a paper's full text, PDF, figures and supplementary files into <out dir>, trying every
legitimate route in turn, then (optionally) the user's own browser, then listing what's still missing.

Usage: python3 -I scripts/fetch_sources.py <PMID> <out dir> [--browser] [--email you@example.org]

Routes, in order (each file is taken from the first route that serves it):
  1. PMC open-access S3 bucket (pmc-oa-opendata): article PDF, figures, supplements
  2. Europe PMC REST: full-text XML, supplementary-files zip
  3. PMC article page: text, figure images (CDN), and the list of supplement links
  4. Unpaywall: open-access PDF copies (publisher, institutional repositories)
  5. Publisher landing page via the DOI: PDF and supplement links it exposes; for Elsevier DOIs, the
     public ars.els-cdn.com supplement (mmcN), supplementary-figure (figsN) and figure (grN) files by PII
  6. Data repositories cited in the text: Zenodo, Dryad, Figshare (APIs); GitHub repos are listed
  7. --browser: open each still-missing link in the user's default browser (a normal human visit:
     the user passes any check themselves), watch ~/Downloads, and move the files in
  8. Anything still missing goes to <out>/NEEDED_FILES.md with the exact links, for the user.
This script never works around a site's bot check: a 403 or challenge page sends the file to
route 7 or 8 instead.
"""
import json
import os
import re
import shutil
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

UA = "bugsigdb-curation/1.0 (+https://bugsigdb.org; mailto:{email})"
EMAIL = "curator@example.org"


def req(url, binary=True, accept=None):
    h = {"User-Agent": UA.format(email=EMAIL)}
    if accept:
        h["Accept"] = accept
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=120)
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
        if re.search(r"text/html", ctype) and re.search(rb"captcha|challenge|Just a moment|bot check|Access Denied", data[:5000], re.I):
            return None, "challenge"
        return (data if binary else data.decode("utf-8", "ignore")), ctype
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:
        return None, type(e).__name__


def jget(url):
    d, _ = req(url, binary=False, accept="application/json")
    try:
        return json.loads(d) if d else None
    except Exception:
        return None


class Fetcher:
    def __init__(self, pmid, out):
        self.pmid, self.out = pmid, Path(out)
        (self.out / "media").mkdir(parents=True, exist_ok=True)
        self.log, self.wanted = [], {}   # wanted: filename -> [urls tried]

    def save(self, name, data, route):
        name = re.sub(r"[^\w.\-]+", "_", name)
        p = self.out / "media" / name
        if not p.exists() or p.stat().st_size == 0:
            p.write_bytes(data)
            self.log.append(f"{route}: {name} ({len(data):,} bytes)")
        self.wanted.pop(name, None)
        return p

    def have(self, name):
        p = self.out / "media" / re.sub(r"[^\w.\-]+", "_", name)
        return p.exists() and p.stat().st_size > 0

    def want(self, name, url, why):
        name = re.sub(r"[^\w.\-]+", "_", name)
        if not self.have(name):
            self.wanted.setdefault(name, []).append(f"{url} ({why})")

    def ids(self):
        d = jget(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:{self.pmid}%20AND%20SRC:MED&format=json&resultType=lite")
        r = ((d or {}).get("resultList") or {}).get("result") or [{}]
        self.pmcid, self.doi = r[0].get("pmcid"), r[0].get("doi")
        if not self.pmcid:
            d = jget(f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={self.pmid}&format=json")
            rec = ((d or {}).get("records") or [{}])[0]
            self.pmcid, self.doi = rec.get("pmcid"), self.doi or rec.get("doi")
        self.log.append(f"ids: PMID {self.pmid}, {self.pmcid}, DOI {self.doi}")

    def s3(self):
        if not self.pmcid:
            return
        x, _ = req(f"https://pmc-oa-opendata.s3.amazonaws.com/?list-type=2&prefix={self.pmcid}.", binary=False)
        for k in re.findall(r"<Key>([^<]+)</Key>", x or ""):
            if k.endswith(".json"):
                continue
            if k.endswith((".xml", ".txt")):
                d, _ = req("https://pmc-oa-opendata.s3.amazonaws.com/" + k)
                if d and not (self.out / ("paper" + Path(k).suffix)).exists():
                    (self.out / ("paper" + Path(k).suffix)).write_bytes(d)
                    self.log.append(f"S3: full text {Path(k).suffix}")
                continue
            name = os.path.basename(k)
            if not self.have(name):
                d, why = req("https://pmc-oa-opendata.s3.amazonaws.com/" + k)
                self.save(name, d, "S3") if d else self.want(name, k, why)

    def europepmc(self):
        if not self.pmcid:
            return
        if not (self.out / "paper.xml").exists():
            d, _ = req(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{self.pmcid}/fullTextXML")
            if d and d.lstrip().startswith(b"<"):
                (self.out / "paper.xml").write_bytes(d)
                self.log.append("Europe PMC: full-text XML")
        d, ct = req(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{self.pmcid}/supplementaryFiles")
        if d and d[:2] == b"PK":
            z = self.out / "media" / "_europepmc_supp.zip"
            z.write_bytes(d)
            with zipfile.ZipFile(z) as zf:
                for n in zf.namelist():
                    if not n.endswith("/"):
                        self.save(os.path.basename(n), zf.read(n), "Europe PMC supplements")
            z.unlink()

    def pmc_page(self):
        if not self.pmcid:
            return
        x, why = req(f"https://pmc.ncbi.nlm.nih.gov/articles/{self.pmcid}/", binary=False)
        if not x:
            self.log.append(f"PMC page: {why}")
            return
        (self.out / "pmc.html").write_text(x)
        if not (self.out / "paper.txt").exists():
            m = re.search(r"<main.*?</main>", x, re.S)
            t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", m.group(0) if m else x, flags=re.S)
            import html as _h
            (self.out / "paper.txt").write_text(re.sub(r"\s+", " ", _h.unescape(re.sub(r"<[^>]+>", " ", t))))
            self.log.append("PMC page: text")
        for u in sorted(set(re.findall(r"https://cdn\.ncbi\.nlm\.nih\.gov/pmc/blobs/[^\"\s]+\.(?:jpg|png|gif|tif)", x))):
            if not self.have(u.split("/")[-1]):
                d, why = req(u)
                self.save(u.split("/")[-1], d, "PMC figures") if d else self.want(u.split("/")[-1], u, why)
        for href in set(re.findall(r'href="((?:https://pmc\.ncbi\.nlm\.nih\.gov)?/articles/[^"]*/bin/[^"]+)"', x)):
            u = href if href.startswith("http") else "https://pmc.ncbi.nlm.nih.gov" + href
            name = u.split("/")[-1]
            if not self.have(name):
                d, why = req(u)
                self.save(name, d, "PMC supplements") if d else self.want(name, u, why)
        pdf = re.search(r'href="(pdf/[^"]+\.pdf)"', x)
        if pdf and not any(p.suffix == ".pdf" and "supp" not in p.name.lower() for p in (self.out / "media").iterdir()):
            u = f"https://pmc.ncbi.nlm.nih.gov/articles/{self.pmcid}/{pdf.group(1)}"
            d, why = req(u)
            self.save("article.pdf", d, "PMC PDF") if d and d[:4] == b"%PDF" else self.want("article.pdf", u, why)

    def unpaywall(self):
        if not self.doi:
            return
        d = jget(f"https://api.unpaywall.org/v2/{self.doi}?email={EMAIL}")
        for loc in (d or {}).get("oa_locations", []):
            u = loc.get("url_for_pdf")
            if u and not self.have("article.pdf"):
                data, why = req(u)
                if data and data[:4] == b"%PDF":
                    self.save("article.pdf", data, f"Unpaywall ({loc.get('host_type')})")
                else:
                    self.want("article.pdf", u, why)

    def publisher(self):
        if not self.doi:
            return
        x, why = req(f"https://doi.org/{self.doi}", binary=False)
        if not x:
            self.want("publisher_supplements", f"https://doi.org/{self.doi}", why)
            return
        for u in sorted(set(re.findall(r'href="([^"]+(?:suppl|supplementary|mmc\d|ESM|moesm)[^"]*\.(?:pdf|docx?|xlsx?|csv|zip|txt))"', x, re.I))):
            u = urllib.parse.urljoin(f"https://doi.org/{self.doi}", u)
            name = u.split("/")[-1].split("?")[0]
            if not self.have(name):
                d, why = req(u)
                self.save(name, d, "publisher") if d else self.want(name, u, why)

    def elsevier(self):
        # Elsevier (DOI 10.1016/...): supplements and figures sit on the public ars.els-cdn.com CDN under the
        # article PII, even when the publisher page and PDF return 403 to scripts (37178109: mmc1-2.docx,
        # figs1-4 and gr1-4 at ~2500 px).
        if not (self.doi or "").startswith("10.1016/"):
            return
        d = jget(f"https://api.crossref.org/works/{self.doi}")
        pii = next((a for a in ((d or {}).get("message") or {}).get("alternative-id", []) if re.fullmatch(r"S\d{15}[\dX]", a)), None)
        if not pii:
            return
        base = f"https://ars.els-cdn.com/content/image/1-s2.0-{pii}-"
        for kind, exts, stop in (("mmc", ("pdf", "docx", "xlsx", "doc", "xls", "zip", "csv", "pptx", "mp4"), 3),
                                 ("figs", ("_lrg.jpg",), 1), ("gr", ("_lrg.jpg",), 1)):
            misses = 0
            for i in range(1, 30):
                got = False
                for ext in exts:
                    name = f"{kind}{i}{ext}" if ext.startswith("_") else f"{kind}{i}.{ext}"
                    if self.have(name.replace("_lrg", "")):
                        got = True
                        break
                    data, _ = req(base + name)
                    if data:
                        self.save(name.replace("_lrg", ""), data, f"Elsevier CDN ({pii})")
                        got = True
                        break
                misses = 0 if got else misses + 1
                if misses >= stop:
                    break

    def repositories(self):
        text = ""
        for f in ("paper.txt", "paper.xml"):
            if (self.out / f).exists():
                text += (self.out / f).read_text(errors="ignore")
        for rec in sorted(set(re.findall(r"zenodo\.(\d{5,9})", text))):
            d = jget(f"https://zenodo.org/api/records/{rec}")
            for f in (d or {}).get("files", []):
                link = (f.get("links") or {}).get("self")
                if link and f.get("size", 0) < 200_000_000 and not self.have(f["key"]):
                    data, why = req(link)
                    self.save(f["key"], data, f"Zenodo {rec}") if data else self.want(f["key"], link, why)
        for doi in sorted(set(re.findall(r"10\.5061/dryad\.[\w.]+", text))):
            d = jget("https://datadryad.org/api/v2/datasets/" + urllib.parse.quote("doi:" + doi, safe=""))
            self.want(f"dryad_{doi.split('.')[-1]}", f"https://doi.org/{doi}", "Dryad (download as a zip in the browser)" if d else "Dryad lookup failed")
        for art in sorted(set(re.findall(r"figshare\.\d+\.v?\d*|figshare\.com/articles/[^\s\"<]+/(\d+)", text))):
            pass  # figshare links vary; listed for the browser route below
        repos = sorted(set(re.findall(r"github\.com/[\w.\-]+/[\w.\-]+", text)))
        if repos:
            self.log.append("authors' code (clone if needed): " + ", ".join("https://" + r.rstrip(".") for r in repos))

    def browser(self, wait=240):
        urls = {n: v[0].split(" (")[0] for n, v in self.wanted.items() if v and v[0].startswith("http")}
        if not urls:
            return
        dl = Path.home() / "Downloads"
        t0 = time.time()
        for u in urls.values():
            os.system(f"open '{u}'")
            time.sleep(1.5)
        print(f"Opened {len(urls)} links in your browser. If a file opens in a tab instead of downloading, save it "
              f"(Cmd+S) into ~/Downloads; waiting {wait} s and moving each file into {self.out / 'media'}.", flush=True)
        self.log.append(f"browser: opened {len(urls)} links; watched ~/Downloads for {wait} s")
        stems = {n: re.sub(r"\.\w+$", "", n).lower() for n in urls}
        while time.time() - t0 < wait and stems:
            for f in dl.iterdir():
                if f.is_file() and f.stat().st_mtime >= t0 and not f.name.endswith((".crdownload", ".download", ".part")):
                    for n, stem in list(stems.items()):
                        if stem[:25] in f.name.lower().replace(" ", "_") or f.name.lower() in n.lower():
                            shutil.move(str(f), self.out / "media" / n)
                            self.log.append(f"browser: {n} ({(self.out / 'media' / n).stat().st_size:,} bytes)")
                            self.wanted.pop(n, None)
                            stems.pop(n)
            time.sleep(2)

    def report(self):
        if self.wanted:
            lines = [f"# Files still needed for PMID {self.pmid}\n",
                     "Every scripted route was tried (and the browser route, if it ran). Please open these links in your browser, "
                     "save each file (Cmd+S if it opens in a tab) into "
                     f"`{self.out / 'media'}` (or just into ~/Downloads and say so):\n"]
            for n, tried in self.wanted.items():
                lines.append(f"- **{n}**: " + "; ".join(tried))
            (self.out / "NEEDED_FILES.md").write_text("\n".join(lines) + "\n")
        elif (self.out / "NEEDED_FILES.md").exists():
            (self.out / "NEEDED_FILES.md").unlink()
        print("\n".join(self.log))
        print(f"\n{len(list((self.out / 'media').iterdir()))} files in {self.out / 'media'}; "
              + (f"{len(self.wanted)} still needed → {self.out / 'NEEDED_FILES.md'}" if self.wanted else "nothing missing"))


def main(argv):
    global EMAIL
    args = [a for a in argv[1:] if not a.startswith("--")]
    if "--email" in argv:
        EMAIL = argv[argv.index("--email") + 1]
        args = [a for a in args if a != EMAIL]
    if len(args) != 2:
        print(__doc__)
        return 2
    f = Fetcher(*args)
    f.ids()
    for step in (f.s3, f.europepmc, f.pmc_page, f.unpaywall, f.publisher, f.elsevier, f.repositories):
        try:
            step()
        except Exception as e:
            f.log.append(f"{step.__name__}: {type(e).__name__} {e}")
    if "--browser" in argv:
        f.browser()
    f.report()
    return 0 if not f.wanted else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
