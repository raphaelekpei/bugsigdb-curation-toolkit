# Mentor-posted guides: teaching material, not rulings

**Read this before every curation**, together with `mentor-rulings.md`.

## Guide or ruling?

| | Ruling (`mentor-rulings.md`) | Guide (this file) |
|---|---|---|
| What it is | A mentor's decision on a specific curation question: a review correction, an answer on an issue, a clean-up instruction | General teaching material posted for everyone: walk-throughs, FAQs, task pages, checklists, worked scoring examples |
| Who wrote it | An official mentor (#1274 list) | Often a contributor, posted or endorsed by a mentor; sometimes a mentor |
| Weight | Settles the question; recent maintainer rulings outrank older policy wording | Shows the expected *approach*. Its worked *values* may describe a draft, not the reviewed record |

**Order of authority:**
1. The live Curation Policy and Help pages.
2. Official mentor rulings (maintainers SvetlanaUP, cmirzayi and lwaldron outrank the other mentors).
3. Guides in this file.
4. Peer reviewers.

When a guide conflicts with a ruling, follow the ruling and say so in a note. Cite a guide as "guide posted by <who>, <date>, #issue", never as "<mentor> ruled".

**Verified caveat:** both 2026-09 curation guides below differ from the reviewed records of their own example studies. Use them for method, never as precedent for a specific value.

Collected 2026-11-01 from every issue and comment in waldronlab/BugSigDBcuration (2,145 issues, 19,086 comments) and waldronlab/BugSigDB (356 issues, 1,875 comments). 6,984 items were by official mentors; 291 were screened by length and wording as possible guides, and the ones below were read in full. Zulip has no public text, so it isn't covered. The bugsigdb.org pages Help:Needs review and Project:Review score were checked and have no guidance text.

---

## G1. "BugSigDB Curation Guide: Approaching Microbiome Papers" (#910)

Posted by **SvetlanaUP, 2026-09-09**, on the issue for PMID 38740280. No author is named. It describes the **pre-review** curation: its Signature 2 ("Streptococcus, Prevotella, Veillonella, Fusobacterium", source "Figure 2B and Results text") is the signature DocTeedee told the curator to remove on 2026-01-20 ("Figure 2B is not curatable"). The live, reviewed record has Signature 1 = 6 IDs and Signature 2 = 1 ID, both sourced from Figure 3B. So the guide is most likely the contributor's write-up, which SvetlanaUP posted as an example.

**Method it teaches** (consistent with the rulings unless noted):
1. **Study design:** read the enrollment and follow-up timeline (prospective 2-year follow-up → longitudinal observational).
2. **Population:** country from the institutions; use the **final analytic n** (126), not screened (200) or recruited (159). Matches the policy and annemarie-sharp #1452.
3. **Experiments:** "Do not force multiple experiments — only curate distinct, clear comparisons… Supplementary analyses (examining differences by NTM species or cavitary status) are exploratory secondary work… Stick to what the paper actually presents as the main finding. Forcing multiple experiments from secondary analyses waters down the curation."
4. **Groups:** Group 0 = reference / negative state; Group 1 = the outcome state you're characterizing.
5. **Condition:** the underlying disease from EFO, not the measured variable ("progression") and not a measurement term ("microbiome measurement").
6. **Antibiotics:** only antibiotic exclusions are recorded; other exclusions (TB, malignancy, HIV, pregnancy) are not.
7. **Sequencing:** body site, 16S vs shotgun, region, platform, all from Methods.
8. **Statistics:** curate the **primary** differential-abundance test, not every feature-selection method used (LEfSe was one of six methods → no LDA). MHT No when no correction is mentioned for the main analysis.
9. **Alpha diversity:** record only the reported indices; leave the rest blank.
10. **Confounders:** "Only model adjustment (regression) or stratification count as 'controlling for'… Bivariate tests cannot adjust for confounders." Balanced baseline tables don't count.
11–12. **Signatures:** one per direction; lowest reported rank; NCBI ID via BugSigDB autocomplete first, then the NCBI Taxonomy Browser.
13. **Source and description:** name the figure or table; the guide adds "biological context" to descriptions. That's in tension with the rulings (concise descriptions, not pasted paragraphs, SvetlanaUP #449), so follow the rulings.

It ends with a pitfalls list (Group 0/1 swaps, measurement terms as conditions, including non-significant taxa, forcing experiments, forgetting decreased signatures, unverified NCBI IDs, misidentified primary test) and a 19-item checklist.

## G2. "Curation Walk-through for Experiment 1" (#861)

Written by **Nina Takang (Outreachy contributor), 2025-10-21**; posted by **SvetlanaUP, 2026-09-09**. Example: PMID 40999363, rat FMT. The live record differs from the walk-through: both signatures are sourced from Table 2 only (the walk-through says "Figure 3, Table 2"), with 11 increased and 7 decreased taxa (the walk-through lists 8 and 8).

**Method it teaches:**
- Read Methods, Results and figure legends; focus on grouping, sequencing and which taxa were significant.
- Use the n after exclusions (7/7 after outlier removal).
- Write Group 1 definitions from the paper's context.
- **Document every interpretation choice in a note** ("Sample sizes were confirmed after exclusion of outliers…").
- Final consistency check: group labels and n match across sections, statistics are consistent, every signature has a description and verified taxa.
- "Think like a reviewer: ask whether someone unfamiliar with the paper could replicate your curation from your notes."

## G3. Outreachy FAQ (#96)

Posted by **cmirzayi, 2023-10-02**, updated 2026-09-30. Summarized in `workflow-and-community.md` ("Outreachy FAQ"): one Task 2 paper at a time, quality over quantity, grading takes up to a week, original and revised scores are both recorded, what to do while waiting, questions go to Zulip or the issue.

## G4. Task pages with the grading rubric (#1, #94)

Posted by **cmirzayi** (#1 2023-03-03; #94 2023-10-02, edited 2026-10-18). The 19-item, 23-point rubric and the Task 2 steps are in `rubric-and-review.md` and `workflow-and-community.md`.

## G5. AI-assisted curation (#1274)

Posted by **SvetlanaUP, 2026-04-12**, "BugSigDB curation supported by claude.ai", with the AI Curation Team slides. Covered in `ai-assisted-curation.md`.

## G6. Worked rubric scorings by mentors

Mentors sometimes post the full rubric table with points per item. Read these to see how deductions are actually applied before self-scoring (`rubric-and-review.md`):
- annemarie-sharp: #884 (2025-10-10), #908 (2025-10-24), #2011 (2026-10-15)
- Buraah: #800 (2025-10-22)

## G7. Database clean-up issues by SvetlanaUP

These are maintainer instructions, so they're treated as **rulings** and recorded in `mentor-rulings.md`. Listed here so they aren't searched for twice:
- #843 (2025-08-28): uniform antibiotics wording ("1 month", "3 months"); no exclusion → blank; active use → "currently on antibiotics". In rulings §6.
- #844 (2025-08-28): "treatment outcome measurement" is "too general"; correct it to the study-specific condition. In rulings §4, where it overrides Buraah #799.

---

## Skill tests derived from guides (not mentor-reviewed)

### Presented-comparison test (from G1 step 3)

Built from G1's "don't force experiments" plus the rulings "We curate all reported significantly abundant microbiome results" (SvetlanaUP #974) and "always check the supplement" (#941, #1134, #1272). **Its weight is a guide's, not a ruling's:** the source text is a guide posted by SvetlanaUP, not her own decision on a study.

1. Curate a comparison only if the paper presents it in the Results text, a main or supplementary figure, or a text pointer to a table ("Additional significant correlations are provided in Table S1").
2. For a presented comparison, take **every** significant taxon for that model from the supplement, not only the ones named in the text (42059388 Exp 9).
3. Comparisons that exist only as supplementary-table rows and are never discussed aren't curated.
4. When the text names the wrong group, follow the table labels and figure colours, cite the presenting figure, and add a note (42059388 Exp 12).
5. **A ruling limits step 1:** presented but secondary, off-focus analyses (covariate screening, side correlations) are **optional**, provided you write a note on the exclusion: "If you choose not to curate, kindly write a note on this exclusion" (TheTosin, 2025-12, #954; 2025-08, #818; `mentor-rulings.md` §1). So the test only *excludes* table-only comparisons. A presented comparison is required only when it's part of the study's question; otherwise including it is the curator's choice, and the decision goes in a note (precedent: 40366801 left out its covariate-screening tables S4–S6 and S11–S13 with a note).

**Applied in 42059388** (Table S1 "Fig.5 Microbes ELISAs"): 3 presented comparisons kept, 6 table-only ones dropped (versions archived in `curations/42059388/archive-20261101-review/`).

**Counter-precedent:** a supplementary-only BMI correlation was kept in a study reviewed by SvetlanaUP (36566315 Exp 3, `mentor-rulings.md` §7). If a reviewer asks for table-only comparisons, add them back.
