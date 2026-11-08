#!/usr/bin/env python3
"""Check that every evidence quote in a curation JSON appears verbatim in the paper.

Usage: python scripts/verify_evidence.py curation.json paper.(txt|xml|html|pdf) [more source files...]

Evidence lives anywhere in the JSON as {"evidence": "quote"} or {"evidence": ["q1", "q2"]},
or in an "evidence" object {"field_name": "quote", ...}. Quotes can use "..." or an ellipsis
to skip text; each fragment must appear in order-insensitive fashion somewhere in the sources.
Matching ignores case, whitespace, hyphen/dash variants and PDF line-break hyphenation.
Evidence that can't be text-matched is written with a bracketed tag and listed for a manual check:
"[figure] Fig 1E: only Peptoniphilus_A has the asterisk", "[code] …", "[data] Table S1 coef …",
"[glossary] …", "[none] …". These are listed as needing a visual check.
Exit code 1 if any quote is not found.
"""
import html
import json
import re
import sys
import unicodedata
from pathlib import Path


def pdf_text_fallback(p):
    """Extract PDF text without pypdf: pdftotext if installed, else macOS PDFKit via swift."""
    import shutil
    import subprocess
    import tempfile
    if shutil.which("pdftotext"):
        r = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True)
        if r.returncode == 0:
            return r.stdout
    if sys.platform == "darwin" and shutil.which("swift"):
        with tempfile.TemporaryDirectory() as d:
            script = Path(d) / "pdftext.swift"
            script.write_text('import PDFKit\nlet d = PDFDocument(url: URL(fileURLWithPath: CommandLine.arguments[1]))!\nprint(d.string ?? "")\n')
            r = subprocess.run(["swift", str(script), str(p)], capture_output=True, text=True)
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout
    return None


def read_source(path):
    p = Path(path)
    if p.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
            return "\n".join(page.extract_text() or "" for page in PdfReader(str(p)).pages)
        except ImportError:
            text = pdf_text_fallback(p)
            if text is None:
                sys.exit("pypdf is needed for PDF input (pip install pypdf), or pass a .txt export")
            return text
    text = p.read_text(encoding="utf-8", errors="ignore")
    if p.suffix.lower() in (".xml", ".html", ".htm"):
        text = re.sub(r"</?(italic|bold|sup|sub|xref|sc|underline|i|b|em|strong|span|a)\b[^>]*>", "", text)
        text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    else:
        # PMC text dumps keep entities (&lt; &gt;), so quotes with "<" or ">" looked missing (34607559)
        text = html.unescape(text)
    return text


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[ \t]?-\s*\n\s*", "", s)  # PDF hyphenation at line ends ("Hospi-" or "Hospi -")
    s = re.sub(r"[‐-―−]", "-", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*([()\[\],.;:<>=±'/-])\s*", r"\1", s)  # stray spaces from tag stripping / PDF italics ("non -L.iners")  # tag stripping leaves stray spaces around punctuation
    s = s.strip().lower()
    # Some PDF fonts drop ligatures from the text layer ("Affiliated" -> "Afliated",
    # "Thirty" -> "Tirty"); fold them on both sides so the match stays symmetric.
    s = re.sub(r"f[fil]*", "f", s)
    return s.replace("th", "t")


def collect(node, path="", out=None):
    out = [] if out is None else out
    if isinstance(node, dict):
        for k, v in node.items():
            here = f"{path}.{k}" if path else k
            if k == "evidence":
                if isinstance(v, str):
                    out.append((here, v))
                elif isinstance(v, list):
                    out.extend((f"{here}[{i}]", q) for i, q in enumerate(v) if isinstance(q, str))
                elif isinstance(v, dict):
                    for f, q in v.items():
                        for i, qq in enumerate(q if isinstance(q, list) else [q]):
                            if isinstance(qq, str):
                                out.append((f"{here}.{f}" + (f"[{i}]" if isinstance(q, list) else ""), qq))
            else:
                collect(v, here, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            collect(v, f"{path}[{i}]", out)
    return out


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    corpus = norm("\n".join(read_source(p) for p in argv[2:]))
    # PDF text layers often drop the spaces between italic words ("ClostridiumclusterIV");
    # a quote that only matches with all spaces removed still counts as verbatim.
    corpus_nospace = corpus.replace(" ", "")
    quotes = collect(data)
    if not quotes:
        print("No evidence quotes found in the curation JSON. Add \"evidence\" fields so values can be verified.")
        return 1
    missing = 0
    visual = [(w, q) for w, q in quotes if q.strip().startswith("[")]
    quotes = [(w, q) for w, q in quotes if not q.strip().startswith("[")]
    for where, q in visual:
        print(f"VISUAL  | {where} | {q[:140]}")
    for where, q in quotes:
        frags = [f for f in re.split(r"\.\.\.|…", q) if len(f.strip()) >= 6]
        if not frags:
            continue
        found = all(norm(f) in corpus or norm(f).replace(" ", "") in corpus_nospace for f in frags)
        if not found:
            missing += 1
            print(f"MISSING | {where} | {q[:140]}")
    print(f"\n{len(quotes) - missing}/{len(quotes)} text quotes found verbatim in the sources; "
          f"{len(visual)} figure- or code-based item(s) need a manual check (re-zoom the figure / re-open the code).")
    if missing:
        print("Fix each missing quote (wrong wording, figure-only evidence, or an unsupported value) and re-score its confidence.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
