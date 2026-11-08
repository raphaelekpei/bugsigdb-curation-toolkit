# Rubric, self-check, and reviewing others

## The official grading rubric (23 points)

Source: waldronlab/BugSigDBcuration issue #94 (Outreachy guidance, updated 2026-09-30). Mentors post this table on every reviewed GitHub issue, including half points (0.5) for partial credit.

| # | Item | Max | What reviewers actually check |
|---|---|---|---|
| 1 | All elements marked "Needs review" (none "Incomplete") | 1 | Study, **every** experiment and **every** signature set to Complete |
| 2 | Correct study design | 1 | §3 of field-guide; multiple designs only when they really exist |
| 3 | Entered all relevant experiments and no irrelevant experiments | 1 | Missing pairwise comparisons, body sites, timepoints, strata, supplementary contrasts; extra experiments with no significant taxa |
| 4 | Body site correctly identified (doesn't include multiple sites) | 1 | One UBERON site, the most specific one |
| 5 | Condition entered according to contrast (correct EFO ontology) | 1 | The experiment's contrast, not the paper's topic; an EFO term |
| 6 | Contrast groups correctly identified | 1 | The right two groups, names, definitions, sample sizes |
| 7 | Groups correctly labeled as 1 and 0 (1 = cases, 0 = controls) | 1 | Not swapped; severity low→0, high→1; earlier time→0 |
| 8 | Antibiotic exclusion correctly identified | 1 | Format "X months"; blank when absent; "currently on antibiotics" |
| 9 | Correctly identified sequencing details | 2 | 1 point for type + 16S region, 1 point for platform |
| 10 | Identified correct statistical test | 1 | The DA test(s) from the dropdown |
| 11 | Identified MHT correction | 1 | Yes/No consistent with methods and the test's defaults |
| 12 | Correctly recorded matched-on variables | 1 | Only true matching; not confounders |
| 13 | Entered correct number of statistical tests per experiment | 1 | No extra tests (diversity or clinical) and none missing (post-hoc) |
| 14 | All diversity measures identified | 1 | Every reported index present; none that weren't tested |
| 15 | Diversity results correctly entered as increased/decreased/unchanged | 1 | Direction relative to Group 1; "unchanged" only if tested |
| 16 | All signature sources correctly identified (−1 for each error) | 2 | Exact figure/table/text heading; all combined sources listed |
| 17 | Abundance direction correctly selected | 1 | Signature 1 = increased in Group 1, Signature 2 = decreased |
| 18 | Members of signatures identified correctly | 2 | 1 point for a single small error, 0 for more. Missing or extra taxa count as errors |
| 19 | Correct use of NCBI taxonomy | 2 | 1 point for one error, 0 for several. No deduction if the taxon really can't be found in NCBI |
| | **Total** | **23** | |

Scores are recorded for both the original and the revised submission (issue #94: "we will record both your original and revised score"), so getting it right **before** first review matters.

## Review states on bugsigdb.org

- **Needs review**: every page set to Complete, not yet reviewed (rubric item 1 wants all pages here, none "Incomplete").
- **Reviewed** / **Incorrect**: the two values a reviewer can set on the Review form ("Incorrect" = flagged for review). Reviewers can also add quality-control tags.
- **Stale review**: a page edited *after* it was reviewed needs re-review. This is one reason not to edit after requesting an official review (maintainer, #1960: "we do not make any changes, once we ask for an official review").

## Pre-submission self-check

Go through this checklist and report anything that fails.

**Structure**
- [ ] Each experiment matches a row in the experiment map, and each row has significant taxa
- [ ] All pairwise comparisons in multi-group figures are covered
- [ ] Separate experiments for each body site, timepoint, and stratum
- [ ] Supplementary tables and figures checked, and their contrasts curated or merged as sources
- [ ] At most one signature per direction per experiment

**Per experiment** (in Create Experiment form order)
- [ ] Location of subjects is the exact dropdown country (e.g. "United States of America"); Host species is from the dropdown
- [ ] One Body site, and the Condition describes this contrast. Both are entered as the glossary autocomplete shows them (capital first letter, e.g. "Vagina")
- [ ] Group 0 name / Group 1 name: Group 0 is control/low/earlier and Group 1 is case/high/later. Names start with a capital letter, abbreviations are expanded, there are no typos, and names aren't wrapped in parentheses
- [ ] Group 1 definition is a precise sentence
- [ ] Group 0 / Group 1 sample sizes match the groups (not swapped), are the analytic n, and are blank for correlation experiments
- [ ] Antibiotics exclusion: "X months" with a space, or "currently on antibiotics", or blank
- [ ] Lab analysis: Sequencing type, 16S lower/upper bound (only when 16S), and Sequencing platform are entered, or blank if unknown
- [ ] Data transformation matches the test family
- [ ] Statistical test: only DA tests listed; post-hoc tests included where used
- [ ] Significance threshold is a bare number; MHT correction is consistent; LDA Score above is a bare number and only for LEfSe
- [ ] Matched on applies only to the matched contrast; Confounders controlled for only where there's a regression or stratification
- [ ] Alpha Diversity (Pielou → Faith) only for tested indices, with direction relative to Group 1
**Per signature** (in Create Signature form order)
- [ ] Source: exact figure / table / "Text; RESULTS: <heading>", with all combined sources listed and no page numbers
- [ ] Description: one plain sentence, abbreviations expanded, with no "Description:" prefix
- [ ] Abundance in Group 1: direction re-derived for Group 1 from the figure legend, colors or coefficient sign; at most one signature per direction
- [ ] NCBI: the taxon count equals the count in the source (state both numbers); every taxon at the paper's rank; each NCBI ID verified or flagged; no unclassified-genus round-ups; no plant or host entries
- [ ] Form data: set to Complete when the signature is finished
**Finish**
- [ ] Every page set to Complete
- [ ] Discussion notes for judgment calls (implied tests, author caveats, ambiguous figures)

## Reviewing someone else's curation

For a full pre-submission review (yours or anyone's), use `reviewer.md`: it adds the blind pass, `scripts/review_curation.py`, deduction frequencies from 160 mentor scorings, calibrated scoring and the report format. The table below is the one mentors post.

When the user asks you to review a curation (theirs or a peer's):

1. Check it against the **paper**, not just for internal consistency. Rebuild the experiment map from the paper first, then compare.
2. Write feedback the way mentors do: a short positive opener, general corrections, then **per-experiment and per-signature bullet points**, each concrete and actionable ("Exp 2/Sig 1: Remove *Porphyromonas*; curate *Porphyromonas* sp. HMT 285 as it is"). Quote the paper sentence that settles each disputed point.
3. Give precise counts: "You're missing 6 taxa in signature 1 (Figure 3 shows 21, 15 curated)".
4. End with the scoring table in this exact markdown form:

```
| Item | Description | max | points |
|---|---|---|---|
| 1 | All elements marked "Needs review" (none "Incomplete") | 1 | |
| 2 | Correct study design | 1 | |
| 3 | Entered all relevant experiments and no irrelevant experiments | 1 | |
| 4 | Body site correctly identified (i.e. does not include multiple sites) | 1 | |
| 5 | Condition entered according to contrast (correct EFO ontology) | 1 | |
| 6 | Contrast groups correctly identified | 1 | |
| 7 | Groups correctly labeled as 1 and 0 (1=cases, 0=controls) | 1 | |
| 8 | Antibiotic exclusion correctly identified | 1 | |
| 9 | Correctly identified sequencing details | 2 | |
| 10 | Identified correct statistical test | 1 | |
| 11 | Identified MHT correction | 1 | |
| 12 | Correctly recorded matched on factors | 1 | |
| 13 | Entered correct number of statistical tests per experiment | 1 | |
| 14 | All diversity measures identified | 1 | |
| 15 | Diversity results correctly entered as increased/decreased/unchanged | 1 | |
| 16 | All signature sources correctly identified (-1 for each error) | 2 | |
| 17 | Abundance direction correctly selected | 1 | |
| 18 | Members of Signatures identified correctly | 2 | |
| 19 | Correct use of NCBI taxonomy | 2 | |
|  | TOTAL | 23 | |
```

5. Remind the curator: don't edit while the review is pending; make the corrections, ask peers on Zulip (#bsdb-peer-reviews) for a check, then ask the reviewer for a second review on the issue.
6. When you request deletions, use full links in the form `https://bugsigdb.org/<PMID>/Experiment_<n>/Signature_<m>` (see workflow-and-community.md).

## The most frequent deductions (2026 reviews)

1. Missing taxa or wrong counts in signatures (often the supplement was missed, or not every LEfSe bar was curated)
2. Experiments missing (extra pairwise or timepoint contrasts, supplementary contrasts) or irrelevant ones kept (no significant taxa)
3. Alpha diversity: untested indices filled in, results copied to the wrong contrasts, or missing indices (Pielou/evenness, Richness from "observed")
4. Direction swapped between signatures, or groups or sample sizes swapped
5. MHT wrong (FDR or adjusted p overlooked; LEfSe marked Yes)
6. Matched-on vs confounders confused; confounders entered for bivariate tests
7. Sources vague ("Results section", page numbers) or incomplete
8. Taxon naming: underscores, wrong case, a genus curated where the paper gives the species, SILVA group names "corrected" away, unresolved red flags
9. Abbreviations not expanded in names, definitions, and descriptions
10. Antibiotics exclusion: format ("3months", "4 weeks" vs "1 month"), extra notes, or filled when nothing was stated

## Responding to peer or mentor review

When a curator shares review comments, check **every** point before acting. Don't accept or reject any of them by default.
1. **Check the live site first** (`scripts/check_live.py <PMID> curation.json`). Many comments are about data-entry errors (duplicates, names in place of IDs, stray characters, Incomplete pages) that the local curation doesn't have.
2. Check each content claim against the paper, the figure (including colours) and the supplementary tables. Reviewers' numbers can be right while their conclusion is wrong (e.g. a "within RA" result that the table labels `:Control`).
3. **Official mentor rulings outrank peer suggestions.** If a peer suggestion contradicts a mentor ruling or strong BugSigDB precedent (e.g. sample sizes for correlation experiments), keep the value and reply with the ruling and the numbers.
4. Sort the comments into: **correct** (fix it), **partly right** (adopt the valid part, e.g. a different glossary term), **disagree with evidence** (polite reply citing the ruling), and **suggestions** (check completeness, e.g. all significant taxa, not only the highlighted one).
5. Give the curator a ready-to-post GitHub deletion request (full URLs) and a short reply to the reviewers, then update `curation.json` → regenerate the derived files → re-run `check_live.py` until only the intended differences remain.
