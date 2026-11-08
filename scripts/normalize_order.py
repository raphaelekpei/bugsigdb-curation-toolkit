#!/usr/bin/env python3
"""Put a curation JSON into BugSigDB form order, in place, without changing any value.

    python scripts/normalize_order.py curation.json [more.json ...]

- Experiment fields follow the live Create Experiment form (Location of subjects ... Alpha diversity,
  then signatures); extra keys (evidence, confidence, notes) go after them.
- Missing form fields are added as null (blank), so a deliberately empty field is explicit.
- Alpha diversity follows Pielou, Shannon, Chao1, Simpson, Inverse Simpson, Richness, Faith.
- Signatures follow Create Signature order (source, description, abundance_in_group_1, taxa), and
  Signature 1 = increased comes before Signature 2 = decreased.

Before writing, it checks that the result holds exactly the same data as the input (apart from the
added nulls and the signature order) and that the file was not changed by someone else meanwhile.
"""
import json
import os
import sys

# Works under `python -I` too, which drops the script's own folder from sys.path.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_curation import ALPHA_ORDER, FORM_ORDER, SIG_ORDER

STUDY_ORDER = ["pmid", "study_design", "citation_mode"]


def ordered(d, order):
    return {**{k: d[k] for k in order if k in d}, **{k: v for k, v in d.items() if k not in order}}


def normalize(data):
    if isinstance(data.get("study"), dict):
        data["study"] = ordered(data["study"], STUDY_ORDER)
    exps = []
    for e in data.get("experiments", []):
        for k in FORM_ORDER:
            if k not in ("id", "signatures"):
                e.setdefault(k, None)
        if isinstance(e.get("alpha_diversity"), dict):
            e["alpha_diversity"] = ordered(e["alpha_diversity"], ALPHA_ORDER)
        sigs = [ordered(s, SIG_ORDER) for s in e.get("signatures", [])]
        rank = {"increased": 0, "decreased": 1}
        e["signatures"] = sorted(sigs, key=lambda s: rank.get(s.get("abundance_in_group_1"), 2))
        exps.append(ordered(e, FORM_ORDER))
    data["experiments"] = exps
    return data


def canonical(data):
    """Order-independent view used to prove no value changed."""
    d = json.loads(json.dumps(data))
    for e in d.get("experiments", []):
        for k in list(e):
            if e[k] is None:
                del e[k]
        e["signatures"] = sorted(e.get("signatures", []), key=lambda s: json.dumps(s, sort_keys=True))
    return json.dumps(d, sort_keys=True)


def main(paths):
    status = 0
    for p in paths:
        before = os.path.getmtime(p)
        raw = open(p, encoding="utf-8").read()
        original = json.loads(raw)
        result = normalize(json.loads(raw))
        if canonical(original) != canonical(result):
            print(f"{p}: ABORTED, normalizing would change values")
            status = 1
            continue
        out = json.dumps(result, indent=1, ensure_ascii=False) + "\n"
        if out.strip() == raw.strip():
            print(f"{p}: already in form order")
            continue
        if os.path.getmtime(p) != before:
            print(f"{p}: SKIPPED, the file changed while it was being read")
            status = 1
            continue
        with open(p, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"{p}: put into form order (values unchanged)")
    return status


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1:]))
