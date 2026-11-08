#!/usr/bin/env python3
"""Validate a BugSigDB curation (JSON, see assets/curation-template.json).

Checks formats and controlled vocabularies that reviewers deduct for. It does
not know the paper, so a clean run means "no format errors", not "correct".

Usage: python scripts/check_curation.py curation.json
Exit code 1 if any ERROR is found.
"""
import json
import re
import sys
from pathlib import Path

VOCAB_FILE = Path(__file__).resolve().parent.parent / "references" / "controlled-vocabularies.md"
SECTIONS = {
    "Study design": "study_design",
    "Location of subjects": "location",
    "Sequencing type": "sequencing_type",
    "Sequencing platform": "sequencing_platform",
    "Data transformation": "data_transformation",
    "Statistical test": "statistical_test",
    "Host species": "host_species",
    "Matched on and Confounders controlled for": "matched_on",
}
ALPHA = {"Pielou", "Shannon", "Chao1", "Simpson", "Inverse Simpson", "Richness", "Faith"}
ALPHA_VALUES = {"increased", "decreased", "unchanged"}
COMMON_ABBR = {"BMI", "CRC", "IBD", "HC", "HIV", "T2D", "T2DM", "NAFLD", "NASH", "COPD", "CKD",
               "LEfSe", "FDR", "HTN", "PD", "AD", "MS", "RA", "UC", "CD", "IBS", "PCOS", "ASD"}


def load_vocab():
    vocab, current = {}, None
    for line in VOCAB_FILE.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            current = SECTIONS.get(line[3:].strip())
            if current:
                vocab[current] = set()
        elif current and line.startswith("- "):
            vocab[current].add(line[2:].strip())
    return vocab


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, where, msg):
        self.items.append((level, where, msg))

    def error(self, where, msg):
        self.add("ERROR", where, msg)

    def warn(self, where, msg):
        self.add("WARN", where, msg)


def as_list(v):
    if v is None or v == "":
        return []
    return v if isinstance(v, list) else [v]


def check_vocab(r, where, field, values, vocab, key):
    allowed = vocab.get(key, set())
    lower = {a.lower(): a for a in allowed}
    for v in as_list(values):
        if v in allowed:
            continue
        if str(v).lower() in lower:
            r.warn(where, f"{field}: '{v}' differs in case from the dropdown value '{lower[str(v).lower()]}'")
        elif key == "matched_on":
            r.warn(where, f"{field}: '{v}' is not in the BugSigDB vocabulary (will be flagged); use an equivalent term if one exists")
        else:
            r.error(where, f"{field}: '{v}' is not a valid dropdown value")


def is_bare_number(s):
    return re.fullmatch(r"\d+(\.\d+)?", str(s).strip()) is not None


def unexpanded_abbr(text):
    """Abbreviations used without an expansion in parentheses somewhere in the text."""
    hits = []
    for tok in set(re.findall(r"\b[A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*\b", text or "")):
        if tok in COMMON_ABBR and f"({tok})" not in text:
            hits.append(tok)
    return hits


# Any upper-case token, not only COMMON_ABBR (31971855: MV, sMV, FLX, SERT, PND slipped through).
# Names that are not abbreviations of something to spell out (cohorts, kits, genes, CST subtypes) are allowed.
# Tokens joined to another by "/" are kit or strain names (GeneXpert CT/NG, BPH/5 mice), not abbreviations to expand.
ABBR_TOKEN = re.compile(r"(?<![\w(/·-])([a-z]?[A-Z]{2,}[0-9]*(?:[-+][A-Za-z0-9]+)*)(?![\w/])")
# Per-study exceptions: "abbreviations_ok": {"RN": "herd series code"} in the study object (40369688).
STUDY_ABBR_OK = set()
ABBR_OK = {"DNA", "RNA", "rRNA", "mRNA", "PCR", "ELISA", "STAMP", "LDA", "ANOVA", "USA", "UK", "II", "III", "IV",
           "GLOWING", "FINRISK", "ZAPPS", "VALENCIA", "METS", "ADVIA", "NIH", "IU"}
ABBR_OK_RE = re.compile(r"^(?:[IVX]+(?:-[A-Z])?|[IVX]+-[IVX]+|[IVX]+[A-C]?\d?-[IVX]+[A-C]?\d?|CD\d+|[A-Z]{2,5}\d+[A-Z]?|[ACGT]{2}|.*-(?:positive|negative|related|like|binding|HR))$", re.I)


def expanded_in(tok, text):
    """True when a bracket holds only abbreviations, e.g. '(MLGs)' or '(CIN1, CIN2 and CIN3)', and one of them is tok.
    '(NSIL, CIN1 and CIN3 combined)' is a group label, not an expansion."""
    for inner in re.findall(r"\(([^()]*)\)", text):
        if not re.search(r"(?<![\w])" + re.escape(tok) + r"s?(?![\w])", inner):
            continue
        if re.match(re.escape(tok) + r"\s*;", inner.strip()):
            return True
        rest = re.sub(r"(?<![\w])[A-Za-z0-9+-]*[A-Z][A-Za-z0-9+-]*(?![\w])", "", inner)
        if not re.sub(r"\b(?:and|or)\b|[,;\s]", "", rest):
            return True
    return False


def check_abbr_form(r, w, e):
    """Warn when an abbreviation is never spelled out in this experiment's names, definition or descriptions,
    and when it is written '(full name, ABBR)' instead of 'full name (ABBR)' (#295, #926, #1050)."""
    fields = {"group_0_name": e.get("group_0_name"), "group_1_name": e.get("group_1_name"),
              "group_1_definition": e.get("group_1_definition")}
    for i, s in enumerate(e.get("signatures") or [], 1):
        fields[f"Signature {i} description"] = s.get("description")
    fields = {k: str(v or "") for k, v in fields.items()}
    everything = " ".join(fields.values())
    seen = set()
    for f, v in fields.items():
        for m in re.finditer(r"\(([A-Za-z][\w /-]*[a-z][\w /-]* [\w /-]+), ([a-z]?[A-Z]{2,}[A-Za-z0-9+-]*)\)", v):
            r.warn(w, f"{f}: write '{m.group(1)} ({m.group(2)})', not '({m.group(1)}, {m.group(2)})'")
        for m in ABBR_TOKEN.finditer(v):
            t = m.group(1)
            base = t.split("-")[0]
            if t in seen or t in ABBR_OK or t in STUDY_ABBR_OK or t in COMMON_ABBR or ABBR_OK_RE.match(t) or expanded_in(t, everything):
                continue
            if base != t and (base in ABBR_OK or base in COMMON_ABBR or base in STUDY_ABBR_OK or expanded_in(base, everything)):
                continue
            seen.add(t)
            r.warn(w, f"{f}: '{t}' is never spelled out in this experiment; write it in full with the abbreviation in brackets after, e.g. 'Full name ({t})', unless it is a proper name (cohort, kit, gene)")


def check_study(r, s, vocab):
    w = "Study"
    pmid = str(s.get("pmid") or "").strip()
    if pmid:
        if not pmid.isdigit():
            r.error(w, f"PMID '{pmid}' must contain digits only (no 'PMID:', no DOI)")
        elif pmid.startswith("0"):
            r.error(w, "PMID must not have leading zeros")
        if s.get("doi") or s.get("uri"):
            r.warn(w, "Do not enter DOI/URI when a PMID is given (Auto mode imports citation data)")
        if s.get("citation_mode", "Auto") != "Auto":
            r.warn(w, "Use citation mode Auto when a PMID is available")
    elif not str(s.get("page_name", "")).startswith("Study_"):
        r.error(w, "No PMID: the page name must start with 'Study_' followed by another identifier (e.g. the DOI without https://doi.org/)")
    designs = as_list(s.get("study_design"))
    if not designs:
        r.error(w, "Study design is empty")
    check_vocab(r, w, "Study design", designs, vocab, "study_design")
    if len(designs) > 1:
        r.warn(w, f"Multiple study designs {designs}: keep only if the paper truly contains each design")


PLACEHOLDERS = re.compile(r"^\s*(not reported|not stated|not specified|n/?a|none|unknown|nil|-|tbd)\s*$", re.I)
QC_NOT_CONFOUNDERS = re.compile(r"decontam|negative control|contaminant|rarefaction|rarefied|sequencing depth normali", re.I)
TEST_NAMES = {"deseq2", "edger", "lefse", "ancom", "ancom-bc", "maaslin2", "maaslin3", "aldex2", "metagenomeseq", "limma", "linda"}


def check_placeholders(r, where, obj):
    for k, v in obj.items():
        if k in ("evidence", "confidence", "signatures", "taxa", "notes"):
            continue
        for item in as_list(v):
            if isinstance(item, str) and PLACEHOLDERS.match(item):
                r.error(where, f"{k} = '{item}': leave the field blank instead of typing a placeholder")


# Live Create Experiment / Create Signature form order (bugsigdb.org, Oct 2026)
FORM_ORDER = ["id", "location_of_subjects", "host_species", "body_site", "condition", "group_0_name",
              "group_1_name", "group_1_definition", "group_0_sample_size", "group_1_sample_size",
              "antibiotics_exclusion", "sequencing_type", "variable_region_lower", "variable_region_upper",
              "sequencing_platform", "data_transformation", "statistical_test", "significance_threshold",
              "mht_correction", "lda_score_above", "matched_on", "confounders_controlled_for",
              "alpha_diversity", "signatures"]
ALPHA_ORDER = ["Pielou", "Shannon", "Chao1", "Simpson", "Inverse Simpson", "Richness", "Faith"]
SIG_ORDER = ["source", "description", "abundance_in_group_1", "taxa"]


def check_order(r, w, e):
    keys = [k for k in e if k in FORM_ORDER]
    if keys != [k for k in FORM_ORDER if k in e]:
        r.error(w, "fields are not in Create Experiment form order; run scripts/normalize_order.py")
    missing = [k for k in FORM_ORDER if k not in e]
    if missing:
        r.error(w, f"missing form fields {missing}; use null for a blank field (scripts/normalize_order.py adds them)")
    alpha = list((e.get("alpha_diversity") or {}).keys())
    if alpha != [k for k in ALPHA_ORDER if k in alpha]:
        r.error(w, f"alpha diversity not in form order (Pielou, Shannon, Chao1, Simpson, Inverse Simpson, Richness, Faith): {alpha}; run scripts/normalize_order.py")
    dirs = [s.get("abundance_in_group_1") for s in e.get("signatures", [])]
    if dirs not in (["increased"], ["decreased"], ["increased", "decreased"], []):
        r.error(w, f"signatures must be Signature 1 = increased, Signature 2 = decreased (at most one each); got {dirs}")
    for s in e.get("signatures", []):
        sk = [k for k in s if k in SIG_ORDER]
        if sk != [k for k in SIG_ORDER if k in s]:
            r.error(w, "signature fields are not in Create Signature form order (source, description, abundance_in_group_1, taxa); run scripts/normalize_order.py")


def check_experiment(r, e, vocab, idx):
    w = f"Experiment {e.get('id', idx)}"
    check_placeholders(r, w, e)
    check_order(r, w, e)
    for v in as_list(e.get("confounders_controlled_for")):
        if QC_NOT_CONFOUNDERS.search(str(v)):
            r.error(w, f"'{v}' is a quality-control step, not a confounder")
    dt = str(e.get("data_transformation") or "")
    if dt.lower() in TEST_NAMES:
        r.error(w, f"Data transformation '{dt}' is a statistical test; use raw counts / relative abundances / centered log-ratio etc.")
    sigs_ = e.get("signatures") or []
    g0 = str(e.get("group_0_name", "")).lower()
    # one-vs-all LEfSe has only an increased signature by design (#231)
    one_vs_all = re.search(r"\ball other|\bothers? combined|\bthe rest\b", g0)
    if len(sigs_) == 1 and "negative correlation" not in g0 and not one_vs_all:
        r.warn(w, "Only one signature: confirm the paper reports no significant taxa in the other direction (a missing Signature 2 is a common AI error)")
    for f in ("body_site", "condition", "group_0_name", "group_1_name"):
        if not e.get(f):
            r.error(w, f"{f} is empty")
    bs = e.get("body_site")
    if isinstance(bs, list) and len(bs) > 1 or (isinstance(bs, str) and ";" in bs):
        r.error(w, "Body site must be a single site per experiment (split into separate experiments)")
    for f in ("body_site", "condition"):
        for v in as_list(e.get(f)):
            if v and v[:1].islower():
                r.warn(w, f"{f} '{v}': enter it as the glossary autocomplete shows it, with a capital first letter (e.g. '{v[:1].upper() + v[1:]}')")
    cond = str(e.get("condition", ""))
    groups = f"{e.get('group_0_name') or ''} {e.get('group_1_name') or ''}"
    if cond == "Microbiome" and re.search(r"\bCST\b|community state", groups, re.I):
        # CST-vs-rest contrasts: SvetlanaUP-reviewed 32719372 and 35250962 use "Microbiome"
        r.warn(w, "Condition 'Microbiome' for a community state type contrast follows the reviewed CST precedents (32719372, 35250962); add a note")
    elif "microbiome" in cond.lower():
        r.error(w, "Condition is almost never a microbiome measurement; use the contrast's condition")
    for f in ("group_0_name", "group_1_name"):
        v = str(e.get(f) or "")
        if v and v[0].isalpha() and v[0].islower():
            r.warn(w, f"{f} '{v}' should start with a capital letter")
        if v.startswith("(") and v.endswith(")"):
            r.warn(w, f"{f} should not be wrapped in parentheses")
        for a in unexpanded_abbr(v):
            r.warn(w, f"{f}: abbreviation '{a}' should be written in full first, e.g. 'Full name ({a})'")
    for a in unexpanded_abbr(e.get("group_1_definition", "")):
        r.warn(w, f"group_1_definition: expand abbreviation '{a}' on first use")
    check_abbr_form(r, w, e)

    n0, n1 = e.get("group_0_sample_size"), e.get("group_1_sample_size")
    for f, n in (("group_0_sample_size", n0), ("group_1_sample_size", n1)):
        if n not in (None, "") and not str(n).isdigit():
            r.error(w, f"{f} must be an integer (or blank if not reported)")
    g0 = str(e.get("group_0_name", "")).lower()
    if "negative correlation" in g0 and (n0 or n1):
        r.warn(w, "Correlation experiment: sample sizes are normally left blank")

    ab = str(e.get("antibiotics_exclusion") or "").strip()
    if ab:
        if re.fullmatch(r"\d+(\.\d+)?[a-zA-Z]+", ab):
            r.error(w, f"Antibiotics exclusion '{ab}' needs a space between number and unit")
        m = re.fullmatch(r"(\d+)\s*weeks?", ab)
        if m and int(m.group(1)) % 4 == 0:
            r.warn(w, f"Antibiotics '{ab}': reviewers convert whole-month weeks to months ({int(m.group(1))//4} month{'s' if int(m.group(1))>4 else ''})")
        if not re.fullmatch(r"\d+(\.\d+)?\s+(day|days|week|weeks|month|months|year|years)", ab) and ab != "currently on antibiotics":
            r.warn(w, f"Antibiotics '{ab}' is not 'X <unit>' or 'currently on antibiotics'; keep only if it is the paper's antibiotic criterion verbatim, with no extra notes")

    check_vocab(r, w, "Location of subjects", e.get("location_of_subjects"), vocab, "location")
    st = e.get("sequencing_type")
    if st:
        check_vocab(r, w, "Sequencing type", st, vocab, "sequencing_type")
    lo, hi = e.get("variable_region_lower"), e.get("variable_region_upper")
    if st == "16S":
        if lo in (None, ""):
            r.warn(w, "16S without a variable region: OK only if the paper does not state it")
        if hi not in (None, "") and lo not in (None, "") and int(hi) <= int(lo):
            r.error(w, "16S upper bound must be greater than lower bound; for a single region (e.g. V4) leave upper blank")
    elif lo or hi:
        r.error(w, "Variable region set but sequencing type is not 16S")
    check_vocab(r, w, "Sequencing platform", e.get("sequencing_platform"), vocab, "sequencing_platform")
    if e.get("data_transformation"):
        check_vocab(r, w, "Data transformation", e["data_transformation"], vocab, "data_transformation")
    tests = as_list(e.get("statistical_test"))
    if not tests:
        r.warn(w, "Statistical test is empty (should be extremely rare)")
    check_vocab(r, w, "Statistical test", tests, vocab, "statistical_test")
    if e.get("host_species"):
        check_vocab(r, w, "Host species", e["host_species"], vocab, "host_species")

    thr = e.get("significance_threshold")
    if thr not in (None, "") and not is_bare_number(thr):
        r.error(w, f"Significance threshold '{thr}' must be a bare number like 0.05")
    mht = e.get("mht_correction")
    if mht not in (None, "", "Yes", "No"):
        r.error(w, f"MHT correction must be Yes, No or blank, not '{mht}'")
    lda = e.get("lda_score_above")
    if lda not in (None, ""):
        if not is_bare_number(lda):
            r.error(w, f"LDA score '{lda}' must be numeric only (no >, <)")
        elif re.fullmatch(r"\d+\.0+", str(lda)):
            r.warn(w, f"LDA score '{lda}': reviewers write it without trailing zeros (e.g. '2')")
        if "LEfSe" not in tests:
            r.error(w, "LDA score is only for LEfSe experiments")
    if "LEfSe" in tests and mht == "Yes":
        r.warn(w, "LEfSe does not correct for MHT by default; Yes only if the paper adjusted the p-values")
    if "DESeq2" in tests and mht == "No":
        r.warn(w, "DESeq2 applies MHT correction by default; check that No is right")
    if "DESeq2" in tests and e.get("data_transformation") not in (None, "", "raw counts"):
        r.warn(w, "DESeq2 normally works on raw counts")

    bivariate = {"T-Test", "Welch's T-Test", "Mann-Whitney (Wilcoxon)", "Kruskall-Wallis", "LEfSe", "Chi-Square", "Fisher's Exact Test"}
    conf = as_list(e.get("confounders_controlled_for"))
    if conf and tests and set(tests) <= bivariate and "stratif" not in str(e.get("notes", "")).lower():
        r.error(w, "Confounders cannot be adjusted with only bivariate tests; remove them unless results were stratified")
    check_vocab(r, w, "Matched on", e.get("matched_on"), vocab, "matched_on")
    check_vocab(r, w, "Confounders controlled for", conf, vocab, "matched_on")
    for v in as_list(e.get("matched_on")) + conf:
        if re.fullmatch(r"[A-Z]{2,5}", str(v)):
            r.error(w, f"'{v}' is an abbreviation; use the full term (e.g. 'body mass index')")
        if str(v).lower() == "gender":
            r.warn(w, "Use 'sex' instead of 'gender'")
    overlap = set(as_list(e.get("matched_on"))) & set(conf)
    if overlap:
        r.warn(w, f"{sorted(overlap)} listed as both matched and adjusted; matching and adjustment are different things")

    alpha = e.get("alpha_diversity") or {}
    for k, v in alpha.items():
        if k not in ALPHA:
            hint = " (observed features/OTUs/species and ACE map to Richness; evenness maps to Pielou)" if re.search(r"observ|ace|even", k, re.I) else ""
            r.error(w, f"Alpha diversity index '{k}' is not a BugSigDB field ({', '.join(sorted(ALPHA))}){hint}")
        if v not in ALPHA_VALUES:
            r.error(w, f"Alpha diversity {k} = '{v}' must be increased/decreased/unchanged (omit if not tested)")
    if alpha and "negative correlation" in g0:
        r.warn(w, "Correlation experiment: alpha diversity is normally left blank")

    sigs = e.get("signatures") or []
    if not sigs:
        r.error(w, "No signatures: an experiment without significant taxa should not exist")
    dirs = [s.get("abundance_in_group_1") for s in sigs]
    if len(sigs) > 2:
        r.error(w, f"{len(sigs)} signatures: at most one increased and one decreased")
    if len(set(dirs)) != len(dirs):
        r.error(w, "Two signatures share the same direction: merge them")
    for j, s in enumerate(sigs, 1):
        check_signature(r, s, f"{w} / Signature {j}")


def check_signature(r, s, w):
    if s.get("abundance_in_group_1") not in ("increased", "decreased"):
        r.error(w, "Abundance in Group 1 must be 'increased' or 'decreased'")
    src = str(s.get("source") or "").strip()
    if not src:
        r.error(w, "Source is empty")
    elif re.search(r"\bpage\b|\bp\.\s*\d", src, re.I):
        r.error(w, "Source should not cite page numbers; use figure/table or 'Text; RESULTS: <heading>'")
    elif re.fullmatch(r"(the )?results( section)?", src, re.I):
        r.error(w, "'Results section' is too vague; cite the figure/table or 'Text; RESULTS: <heading>'")
    desc = str(s.get("description") or "")
    if desc.lower().startswith("description:"):
        r.error(w, "Remove the 'Description:' prefix")
    for a in unexpanded_abbr(desc):
        r.warn(w, f"Description: expand '{a}' on first use")

    taxa = s.get("taxa") or []
    if not taxa:
        r.error(w, "Signature has no taxa")
    exp = s.get("expected_taxa_count")
    if exp is not None and exp != len(taxa):
        r.error(w, f"Taxon count {len(taxa)} does not match the {exp} taxa in the source")
    seen = set()
    for t in taxa:
        name = str(t.get("name") or "")
        tid = str(t.get("ncbi_id") or "").strip()
        label = name or t.get("paper_name", "?")
        key = tid or name.lower()
        if key in seen:
            r.error(w, f"Duplicate taxon '{label}'")
        seen.add(key)
        if re.fullmatch(r"[A-Z][a-z]+_(?:[A-Z]{1,2}(?:_\d+)?|\d+)", name):
            # GTDB names (Peptoniphilus_A, Clostridium_AQ, Klebsiella_724518): mentors curate as written (#741, #860)
            if not tid:
                r.warn(w, f"'{name}': GTDB suffix name with no NCBI node; curate as written and add a discussion note")
        elif "_" in name and not tid:
            # NCBI strain names keep their underscores ("Bacteroides sp. 3_1_19"); only text entries are respaced
            r.error(w, f"'{name}': replace underscores with spaces")
        if re.match(r"^[a-z]__", name):
            r.error(w, f"'{name}': remove the rank prefix")
        if re.search(r"\bunclassified\b", name, re.I):
            r.warn(w, f"'{name}': current mentor practice keeps distinct unclassified features as written with lowercase 'unclassified' (#937, #1189); prefix strings like g_unclassified_f_X become the named taxon; see mentor-rulings.md section 12")
        if re.search(r"sensu stricto", name, re.I):
            r.warn(w, f"'{name}': reviewers curate 'Clostridium sensu stricto 1' as Clostridium")
        if re.search(r"\b(OTU|ASV)\s*\d+", name) and not re.fullmatch(r"(OTU|ASV)\s*\d+", name.strip()):
            r.warn(w, f"'{name}': drop the OTU/ASV tag when a taxon name is assigned")
        if re.search(r"chloroplast|mitochondri|streptophyta", name, re.I):
            r.error(w, f"'{name}': non-microbial entry; remove it")
        # NCBI environmental-clone nodes are lowercase by design ("rumen bacterium YS2" 209265, 32702151)
        ncbi_clone = tid.isdigit() and re.match(r"^[a-z][a-z ]* (bacterium|archaeon)\b", name)
        if name and name[0].islower() and not ncbi_clone and not name.startswith(("uncultured", "unclassified", "metagenome")):
            r.warn(w, f"'{name}': genus and higher names are capitalized")
        if tid:
            if not tid.isdigit():
                r.error(w, f"'{label}': NCBI ID '{tid}' must be an integer")
        elif not t.get("verify"):
            r.warn(w, f"'{label}': no NCBI ID; resolve it or mark it plain text and verify")


def check_confidence(r, data):
    """Confidence scores live in "confidence": {"field": score} objects (see verification.md)."""
    found = []

    def walk(node, where):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "confidence" and isinstance(v, dict):
                    checked = node.get("rulings_checked") or {}
                    for f, s in v.items():
                        found.append((where, f, s, checked.get(f)))
                else:
                    walk(v, where if k not in ("signatures",) else where)
        elif isinstance(node, list):
            for i, v in enumerate(node, 1):
                label = where
                if isinstance(v, dict) and "id" in v:
                    label = f"Experiment {v['id']}"
                elif isinstance(v, dict) and "abundance_in_group_1" in v:
                    label = f"{where} / Signature {i}"
                walk(v, label)

    walk(data, "Study")
    if not found:
        r.warn("Study", "No confidence scores: run the verification pass (references/verification.md) and score each value")
        return
    for where, f, s, checked in found:
        if not isinstance(s, (int, float)) or not 0 <= s <= 100:
            r.error(where, f"Confidence for {f} must be a number from 0 to 100, not '{s}'")
        elif s < 70:
            r.warn(where, f"LOW CONFIDENCE ({s}) for {f}: curator must check this or ask on Zulip before entering")
            # A call may only go back to the curator after mentor-rulings.md was searched for it.
            if not (isinstance(checked, str) and checked.strip()):
                r.warn(where, f"RULINGS NOT CHECKED for {f}: search references/mentor-rulings.md, then record "
                              f'"rulings_checked": {{"{f}": "<issue numbers consulted, or terms searched with no ruling found>"}}. '
                              "If a ruling settles it, apply it and score 70 instead of handing it back")


def main(path):
    vocab = load_vocab()
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    r = Report()
    STUDY_ABBR_OK.update((data.get("study") or {}).get("abbreviations_ok") or {})
    check_study(r, data.get("study", {}), vocab)
    exps = data.get("experiments") or []
    if not exps:
        r.error("Study", "No experiments")
    for i, e in enumerate(exps, 1):
        check_experiment(r, e, vocab, i)
    check_confidence(r, data)
    errors = [i for i in r.items if i[0] == "ERROR"]
    warns = [i for i in r.items if i[0] == "WARN"]
    for level, where, msg in errors + warns:
        print(f"{level:5} | {where} | {msg}")
    print(f"\n{len(errors)} error(s), {len(warns)} warning(s). "
          + ("Format checks passed. Still verify content against the paper." if not errors else "Fix errors before submitting."))
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
