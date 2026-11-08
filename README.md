# BugSigDB curation toolkit

My personal toolkit for curating and reviewing microbiome studies for [BugSigDB](https://bugsigdb.org). I built it while contributing to [waldronlab/BugSigDBcuration](https://github.com/waldronlab/BugSigDBcuration) in 2026.

It's an **AI-assisted** curation setup. Following the community's guidance in [#1274](https://github.com/waldronlab/BugSigDBcuration/issues/1274) ("BugSigDB curation supported by claude.ai"), I use Claude to help draft curations, and this toolkit is how I verify every value against the paper before anything goes live. `SKILL.md` is the Claude skill that ties it together. The scripts and reference files also work on their own.

## What's here

| Path | What it is |
|---|---|
| `references/mentor-rulings.md` | About 1,550 rulings and corrections from mentors' review threads, grouped by topic (scope, experiment splitting, every form field, taxonomy, MHT) and cited by issue number. |
| `references/mentor-guides.md` | Walkthroughs, FAQs and worked rubric scorings posted by mentors, kept apart from the rulings because they carry less weight. |
| `references/taxonomy.md` | NCBI lookup rules: renamed taxa, homonyms, unclassified/uncultured/placeholder labels, SILVA/Greengenes/GTDB quirks. |
| `references/controlled-vocabularies.md` | Exact dropdown values and condition/body-site terms, with fallbacks used in past curations. |
| `references/field-guide.md`, `rubric-and-review.md`, `reviewer.md`, `verification.md` | How each field is filled, the 23-point rubric, a review procedure and a verification pass. |
| `references/ai-assisted-curation.md` | Failure modes the community reported for AI curations (#1274) and how each one is checked. |
| `lessons-ledger.md` | What each curation taught me and where that lesson was added. These are my own notes and haven't been reviewed by mentors. |

## Scripts

All plain Python 3 (standard library only, except optional PDF text extraction).

| Script | What it checks |
|---|---|
| `check_curation.py curation.json` | Format and vocabulary errors reviewers deduct for: thresholds, LDA, antibiotics wording, empty signatures, unexpanded abbreviations, taxon name formats. |
| `verify_evidence.py curation.json paper.pdf` | That every quoted piece of evidence really appears in the paper. |
| `check_live.py <PMID> [curation.json]` | The curation as it is live on bugsigdb.org, read through the wiki API: names stored instead of NCBI IDs, duplicate signatures, Incomplete pages, differences from the local file. |
| `review_curation.py curation.json [paper]` | A first-pass review: runs the checks above, resolves every NCBI ID, confirms condition and body-site terms exist, and groups findings by rubric item. |
| `fetch_sources.py <PMID> <dir>` | Collects the paper, figures and supplements from open sources (PMC, Europe PMC, Unpaywall, Zenodo/Dryad/Figshare). It never bypasses bot checks. |
| `normalize_order.py`, `render_forms.py` | Put a curation JSON into BugSigDB form order, and print it field by field for data entry. |
| `prereview_snapshot.py` | Rebuilds a study as it stood at a given time, used to test the review procedure against real mentor reviews. |
| `rendercrop.swift` | macOS helper that renders a zoomed crop of a PDF page for reading small figure labels. |

## Caveats

- The rulings are my own summaries of public review threads. If a summary and the original thread disagree, the thread wins.
- Notes marked "skill note, not yet mentor-reviewed" are my own judgment calls, not official policy.
- BugSigDB's policies change. Always check the [curation policy](https://bugsigdb.org/Help:Contents) and recent mentor comments.

BugSigDB data are CC BY 4.0. This toolkit isn't an official BugSigDB or Waldron Lab project.
