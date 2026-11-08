# Workflow, GitHub, and community practice

## Where things live

- **bugsigdb.org**: the wiki where curations are entered (Study → Experiment → Signature forms). Request an account at Special:RequestAccount.
- **github.com/waldronlab/BugSigDBcuration/issues**: papers to curate, claims, review feedback, and deletion requests. Labels include `paper to curate`, `assigned`, `needs review`, `needs 2nd review`, `reviewed`, `first contribution` (good for newcomers), `second contribution` (harder), `possible duplicate`, `duplicate`, and cohort labels such as `outreachy dec2026`.
- **github.com/waldronlab/BugSigDB/issues**: bugs on the website itself (e.g. duplicated signatures after an undelete, or PMID change requests).
- **Zulip** (community-bioc.zulipchat.com; sign up via chat.bioconductor.org): `#bugsigdb` for announcements and policy discussions, `#bsdb-questions` for task and process questions, `#bsdb-peer-reviews` for peer review requests, `#bsdb-introductions`. Don't use #general or #random, and don't DM mentors directly. Office hours are Thursdays at 9 AM US Eastern.
- Video tutorials: the BugSigDB YouTube playlist (PLIUETfW6tVu2OGgZcIxqI7DbUBReHVdIq). For an example of a complete curation, see https://bugsigdb.org/Study_600

## Lifecycle of a curation

1. **Find a paper**: an open issue labeled `paper to curate`, or add your own using the issue template "BugSigDB study curation by DOI" (a GitHub Action fills in title, author, year, and PMID from Crossref). When adding a paper, comment on why: mentors prefer that you focus on a topic you care about.
2. **Claim it**: comment on the issue (e.g. "I am up for this paper to curate") and **wait to be assigned** (the `assigned` label). Don't start before you're assigned, and claim only one paper at a time until it's graded.
3. **Pre-curation** [Policy]: read the Curation Policy, download the PDF, read and annotate it, and save it as `<PMID>.pdf`.
4. **Curate** on bugsigdb.org. Set pages to Incomplete while working.
5. **Peer check**: ask in #bsdb-peer-reviews before requesting the official review.
6. **Mark Complete** on all pages, deposit the annotated PDF (the Dropbox link is on Zulip; **not required for Outreachy applicants**, SvetlanaUP #859/#2014), and comment on the GitHub issue that it's ready for review (maintainers apply `needs review`).
7. **Freeze**: no edits after requesting review until the reviewer posts feedback.
8. **Revise**: address every bullet, then ask the reviewer for a second review on the issue.
9. If someone stops working on an assigned paper, they should give the team a heads-up so the paper can be reassigned.

## Requesting deletions or changes

Curators can't delete pages or renumber experiments and signatures. Ask maintainers on the GitHub issue, and **always give full canonical links**, one per line:

```
Please delete:
https://bugsigdb.org/40461820/Experiment_4
https://bugsigdb.org/40461820/Experiment_5/Signature_2
```

- Use `/` between levels, never `#`, and never the `Special:FormEdit/...?returnto=` edit URLs.
- If you're deleting all signatures of an experiment, ask for the experiment itself to be deleted.
- Say exactly what should go ("all experiments and signatures" if that's what you mean).
- Numbering gaps after deletions are fine.

## Scope and red flags (check before curating)

- **Journal moratorium**: maintainers aren't curating papers from **"Frontiers in Microbiology" and related journals** because of "repeated cases of potentially fraudulent and/or extremely low quality research reports" (SvetlanaUP, #2012, 2026-10-18; first announced May 2026 on Zulip #bugsigdb, topic "Journal Moratorium: Frontiers in Microbiology"). Treat other Frontiers titles (e.g. Frontiers in Cellular and Infection Microbiology) as "related" and ask on Zulip before curating one.
- **Preprint vs published**: if a peer-reviewed version exists, curate that one, using its PMID.
- **Suspect papers**: maintainers have halted curation of papers that look fabricated or AI-written (repetitive or nonsensical methods, analyses that don't match the methods, sample sizes that don't add up). If you see these signs, raise it on the issue or Zulip instead of curating. Reviewers can apply quality-control tags such as "Results are suspect (various reasons)".
  - **Quick checks that catch them** (from PMID 41214659, 2026-10-23):
    - compare per-sample sequencing tables for **identical rows** across groups
    - look for implausibly uniform read depths
    - check that the same variable has the same value in every table
    - look for template text such as "(if applicable)"
    - check that every cited figure or supplementary table actually exists
    - check whether claimed differential-abundance results come with any table, fold changes or q-values
    - **count the points in jittered box plots and scatter plots** against the stated n per group, and check that ordination sample labels (prefixes such as A12, B30) match the group colours. In PMID 41199330, Fig 2a showed about 7/33/40 points for 15/15/15 infants at one timepoint, and PCoA labels A2–A60 were spread across all three colours (skill note, not yet mentor-reviewed)
    - look for timepoint residue ("on day 3" in a single-timepoint study; 41199330)
  - Save the evidence in a `SCREENING.md` and post a short, factual comment on the issue asking the maintainer how to proceed. Don't accuse anyone.
- **Already curated?** Search bugsigdb.org by PMID or title. The form says "must be unique" if the PMID page exists. Also look for `Study_` pages for the same paper, which maintainers merge. Mark duplicates on GitHub with `possible duplicate`.
- **Commentary vs paper**: make sure the issue's DOI is the research article, not a commentary or erratum.
- **Meta-analyses / systematic reviews**: curatable but harder. Sample sizes and lab methods may be pooled or unclear.
- **Nothing significant**: comment that the paper isn't curatable, quoting the sentence (e.g. "Probiotic supplementation does not alter vaginal microbial community"). Maintainers suggest checking papers that cite it for a curatable alternative.
- **Missing details**: curators sometimes email authors for clarification, and maintainers have posted author replies on issues. Record what you learn in a discussion note.

## Writing good issue comments

- Ready for review: "@<reviewer> this curation is complete and marked Needs review: https://bugsigdb.org/<PMID>. Peer-reviewed by @<peer> on Zulip."
- Question: quote the exact paper sentence and the figure or table, state the options you're weighing, and ask on Zulip #bsdb-questions first, so everyone benefits.
- Keep it short and factual, and link to the specific experiment or signature.

## Other BugSigDB resources

- BugSigDBExports (hourly data exports), the Zenodo stable releases, the `bugsigdbr` Bioconductor package, and BugSigDBStats.
- The reference paper is Geistlinger et al., *Nature Biotechnology* 2023 (doi:10.1038/s41587-023-01872-y).

## Outreachy FAQ (issue #96, updated 2026-09-30)

- **One second contribution at a time.** Claim one article and make it "as perfect as possible", because it's used to assess you: "quality over quantity". Claim another only after the first is graded.
- **You don't need task 1 approved** before claiming a task 2 paper. Submitting the Qualtrics mini-curation is enough.
- **Grading** usually takes up to a week. Both your original and revised scores are recorded, so get it right before you submit.
- **While waiting:** peer-review other applicants' curations (post on their GitHub issue), try resolving taxa in https://bugsigdb.org/Category:Pages_with_missing_NCBI_ID (most can't be solved, and that's fine), or see Help:Contents.
- **Recording contributions:** on the Outreachy site, link the survey (task 1) or your GitHub issue (task 2).
- **Questions** go in Zulip #bsdb-questions (or the task's GitHub issue), never as DMs to mentors. Mentors are on US Eastern and Central European time.
- **Official mentors** (#1274): SvetlanaUP, lwaldron, cmirzayi, jwokaty, annemarie-sharp, Buraah, TheTosin, DocTeedee. Other reviewers are peers: their comments are valuable, but they don't overrule a mentor.
