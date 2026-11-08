# Senior reviewer mode: review a local curation before it goes live

**Use when** the user asks to review, check, score or "be the reviewer" for a curation.json (theirs or anyone's) before it's entered on bugsigdb.org or before review is requested. You act as an official BugSigDB mentor grading a Task 2 curation, on the 19-item, 23-point rubric (`rubric-and-review.md`), with the conventions in `mentor-rulings.md` and `mentor-guides.md`.

**What a review can promise:** no avoidable deductions. Every mechanical error caught, every value re-derived from the paper, every rubric item scored the way mentors score it, and every judgment call flagged with the likely reviewer reaction and a drafted defence. **What it can't promise:** a guaranteed 23/23. Mentors disagree (§12 of the rulings), rules change, and some calls have no ruling. Say so in the verdict instead of implying certainty.

**The baseline to beat** (160 official-mentor scorings in waldronlab/BugSigDBcuration, parsed 2026-11-01): mean **20.1/23**, only **22%** perfect. Share of scorings that lost points on each item (all / since 2025-06):

| Item | Lost points in | Item | Lost points in |
|---|---|---|---|
| 18 Signature members | **59% / 53%** | 6 Contrast groups | 23% / 11% |
| 16 Sources | **41% / 29%** | 5 Condition | 21% / 19% |
| 3 Experiments | **31% / 20%** | 17 Direction | 21% / 12% |
| 19 NCBI | **30% / 27%** | 12 Matched on | 16% / 7% |
| 10 Statistical test | 28% / 14% | 11 MHT | 15% / 9% |
| 15 Diversity directions | 26% / 20% | 7 Group 1/0 | 14% / 6% |
| 13 Number of tests | 25% / 17% | 2 Design | 13% / 8% |
| 14 Diversity measures | 24% / 17% | 9 Sequencing; 4 Body site; 8 Antibiotics; 1 States | ≤ 11% |

Spend effort in that order. Item 18 alone decides most reviews.

---

## 1. Independence: review like someone who didn't curate it

A reviewer who reads the curator's reasoning first tends to agree with it. So:
- **Run the review in a fresh agent** whenever the same conversation produced the curation. Give it only: the paper (text, PDF, figures, supplements, authors' code if named), the curation.json, and this skill. Don't pass the curation's VERIFICATION.md, CURATION_SHEET.md or chat reasoning.
- **Blind pass before reading the JSON's values.** Build your own experiment map and signatures from the paper first (§3, phases 1–2), then open the curation and compare.
- The curation's `notes`, `evidence` and `rulings_checked` are the curator's defence. Read them only in phase 3, after you've formed your own view, and judge whether the defence would satisfy a mentor.

## 2. Tools and inputs (get them before judging)

| Need | How |
|---|---|
| Paper text | Local `source/` text; else NCBI efetch (`db=pmc`) or the PMC article page; PMC author manuscripts and some publishers block scripts, so ask the user for files |
| Figures at full resolution | Publisher PDF (embedded images via PyMuPDF), or render and crop with `scripts/rendercrop.swift`; zoom every panel you take taxa from |
| Paper, PDF, figures, supplements | `scripts/fetch_sources.py <PMID> <dir> --browser`: every legitimate route, then the user's browser, then `NEEDED_FILES.md`; `verification.md` "Tips" |
| Authors' code | GitHub repo named in Data Availability; settles models, tests, MHT, coefficient signs |
| Mechanical checks | `scripts/review_curation.py curation.json <paper text/PDF> [supplement text …]` (pass **every** source file the evidence quotes come from, e.g. `paper.txt supp_text.txt`; with the paper alone, quotes from the supplement show as false ERRORs, as in 40304477) (wraps `check_curation.py` and `verify_evidence.py`, resolves every NCBI ID, checks glossary terms, sources and states); `scripts/check_live.py <PMID> curation.json` once entered |
| Precedent | BugSigDB API (`action=ask`) or the export; `verification.md` §6. **Exclude the study under review** from precedent queries (filter out results whose page name starts with its PMID): once it's live, its own pages would answer the question for you |
| Rules | `mentor-rulings.md` (rulings) → `mentor-guides.md` (guides) → `field-guide.md`, `taxonomy.md`, `controlled-vocabularies.md` |

**If a file a value depends on is missing** (e.g. the supplementary table holding the coefficients), don't guess. List it under "Can't verify without", score that item as unverified, and say which file the user must provide.

## 3. Procedure

**Phase 0: mechanical.** Run `review_curation.py`. Every ERROR is a finding. Every WARN needs a decision: a finding, or a deliberate choice backed by a note.

**Phase 1: blind experiment map (item 3, 10, 13).** From Methods, Results, every figure and table legend, and the supplement:
- list every differential-abundance analysis with significant taxa: contrast, groups, body site, timepoint, subgroup/stratum, clinical marker, test, MHT, source;
- one experiment per distinct contrast (body site, timepoint, marker, pairwise comparison, pooled vs subgroup, different test with different taxa: rulings §3);
- curate comparisons the paper presents; table-only comparisons never discussed aren't required; presented secondary analyses are optional with a note (`mentor-guides.md`, presented-comparison test; TheTosin #954/#818);
- no experiment without significant taxa; no interaction terms (#1072: read the model formula first, rulings §1);
- the DA test only (not alpha/beta diversity tests), post hoc combined with its omnibus, dropdown strings exact.

**Phase 2: blind signatures (items 16–19).** For each experiment in your map, re-extract the taxa yourself:
- the paper's significance rule: corrected vs raw p per its MHT, LDA cut-off, colour or asterisk legend;
- every rank the source reports for that contrast, combined in one signature;
- direction relative to Group 1: read signs from effect sizes (positive/negative coefficient relative to the reference level, LDA bar side, fold-change direction), never from prose alone (`ai-assisted-curation.md`);
- the exact source label of every figure panel and table used, combined ("Figure 4A, Table S5").

**Phase 3: compare.** Open the curation. Field by field, experiment by experiment, compare with your map and signatures. Each discrepancy becomes a finding: what's wrong, the evidence (quote with page/figure/table), the fix, the rubric item, and the ruling or guide behind it. Then read the curator's notes and decide whether each defence holds.

**Phase 3b: fixed checklist (every review, whatever the judgment pass found).** Two runs on the same curation don't notice the same small things (§7, round 2), so walk this list explicitly and write "checked" against each:
- every signature description: under ~200 characters, one sentence, no typos, abbreviations in full, says which taxa (not a copy of the caption);
- every condition: the contrast's own term, as specific as the glossary allows (delivery mode, disease subtype, the marker measured);
- every source: exact labels, no stray commas or "and", the same wording style across signatures;
- every group name and definition: capitals, abbreviations expanded once, consistent across experiments, no typos;
- every experiment: same sequencing fields when one run produced them; antibiotics blank unless explicit;
- every taxon: the ID's NCBI name matches the paper's taxon at the same rank.

**Phase 4: score.** Fill the rubric table the way mentors do:
- half points are normal for a partial error (e.g. 0.5 on item 4 when one experiment has a wrong body site);
- item 16: −1 per wrong or missing source, floor 0;
- items 18 and 19: 1 point for a single small error, 0 for more than one; a taxon that truly has no NCBI node isn't an item-19 error if entered as text with a note;
- score the curation as it stands, not as it would be after fixes;
- **calibrate:** split findings into *would cost points* (a mentor would write it as a correction) and *improvements* (valid, but mentors rarely deduct: wording, extra notes, a stricter term than the one used). Score only the first group. In the 2026-11-01 test, scoring everything made the prediction 2.5 points too harsh in 5 of 6 cases (§7).

**Phase 5: report** (format in §5).

## 4. Item-by-item checks, riskiest first

**18 Signature members.**
- Recount every source; compare names one by one (missing, extra, wrong rank, wrong direction).
- Apply the paper's own threshold: if MHT is Yes, only corrected-significant taxa; non-significant rows and taxa only "mentioned" in text are out.
- Supplementary tables named in the text for the same contrast hold taxa that must be included.
- Same feature at two ranks → once; distinct unclassified features → per rulings §12; GTDB suffixes as written.

**16 Sources.**
- Exact panel and table labels, every source used for that signature, consistent wording across signatures.
- Not "Results section" (use "Text; RESULTS: <heading>" for text-only results), no stray commas or quotes ("Table 1, and Table 2" → "Table 1, Table 2"; DocTeedee #1971), and supplementary labels as the paper prints them.
- A supplementary table that only lists taxa without statistics isn't a source; cite the figure or table with the test (annemarie-sharp #1143: "Table S4 alone is a descriptive table with no statistical test… curate only Figure 2A as the source").

**3 Experiments.**
- A three-group figure with pairwise brackets (e.g. healthy, CF, NCFB) holds up to three contrasts: check every pair, not only the ones against controls (missed in test #1197, Fig 3F CF vs NCFB).
- Don't create an experiment from uncorrected "trend" taxa when nothing passes the paper's own correction and the authors call them trends: DocTeedee deleted such an experiment as having "no statistically significant signatures" (#1971, 2026-10). #990 (curate raw-p hits with MHT No) applies when the paper presents those hits as results.
- Your blind map vs theirs: missing contrasts (body sites, timepoints, markers, supplementary tables, pairwise comparisons), extra ones (no significant taxa, interaction terms, duplicates of the same contrast and test).

**19 NCBI.**
- Every ID resolves to the intended taxon at the intended rank. No strain/CAG/isolate node where the paper names a species (annemarie-sharp #1143: "replace Enterocloster bolteae CAG:59 with Enterocloster bolteae (208479)"). No plant, fungal or animal homonym in a bacterial signature (test #1197 found a palm order, a plant genus and two fungi).
- Renamed genera mapped (`taxonomy.md` §5/§9). Homonyms checked.
- Text entries only when NCBI has no node, with a note.

**10 Statistical test / 13 Number of tests.**
- Only the test(s) that produced the differential-abundance result for that experiment.
- Not the alpha/beta tests; not two tests when one experiment came from one.
- Dropdown string exact.

**15 Diversity directions / 14 Diversity measures.**
- Only indices the paper tested for this contrast and level; none it didn't test.
- Direction relative to Group 1 from the figure or p-value.
- "Unchanged" only if tested and not significant.
- Significant at one taxonomic level but not at the level curated → "unchanged" for the curated level, plus a discussion note quoting the paper (annemarie-sharp #1143).
- "All indices indicated higher diversity" in the text → every tested index increased (annemarie-sharp #2050).
- Blank for correlation and one-vs-all experiments.

**6 Contrast groups / 7 Labels.**
- Names start with a capital and expand abbreviations once ("Cystic fibrosis (CF)").
- Group 1 is the case / exposed / outcome / later timepoint.
- Group 1 definition from the paper.
- Final analytic n per group, blank if not reported.
- Correlation experiments get Low/High names and blank n.
- Regression models (MaAsLin2, GLM, mixed models) with a categorical contrast: read the reference level, then the coefficient signs; a negative coefficient means higher in the reference group. A sign misread swaps every taxon between the signatures (DocTeedee #1928: 5 increased and 9 decreased, not 9 and 5).

**5 Condition.**
- The contrast's condition, an EFO term that exists in Category:Condition.
- Not too general (no "treatment outcome measurement", #844), not the paper's topic when the contrast is something else, not a measurement term for a disease.

**17 Direction.** Signature 1 = increased in Group 1. Check effect-size signs against the reference level the model used.

**12 Matched on.** Only true matching (frequency/individual matching in recruitment); adjustment covariates go in confounders.

**11 MHT.** From Methods and the tool's defaults (DESeq2 Yes; LEfSe No unless adjusted; ANCOM Yes; MaAsLin2 reports q).

**2 Design, 9 Sequencing, 4 Body site, 8 Antibiotics, 1 States.**
- Design per `field-guide.md` §3.
- Delivery-mode contrasts: condition "Delivery measurement" or "Delivery method" (#1135), not "Cesarean section" (DocTeedee #1928; the approved page uses "Delivery measurement").
- Same 16S region and platform across all experiments when one sequencing run produced them (DocTeedee #1971: "The V3-V4 16s region is the same for all experiments"); platform only if stated.
- One body site per experiment, most specific UBERON term.
- Antibiotics only from an explicit antibiotic exclusion, else blank.
- Every page Complete.

**Not rubric items, but mentors comment on them** (fix them anyway):
- descriptions concise and specific (#449), abbreviations in full;
- confounders as BugSigDB vocabulary terms (use synonyms such as sex for gender rather than free text that gets flagged);
- discussion notes for every deliberate deviation;
- data transformation matching the test.

## 5. Report format

```
# Review: <PMID> (<title>)
Verdict: READY TO SUBMIT | FIX FIRST (n findings) | BLOCKED (missing files)
Expected score: <x>/23 as it stands; <y>/23 after the fixes below

## Comment as a mentor would post it
Hello @<curator>, well done on this curation. Here are some corrections to consider:
- <one bullet per finding, mentor wording, most costly first>

## Rubric
| # | Item | Max | Points | Why |
(all 19 rows, TOTAL)

## Findings (evidence)
| # | Exp/Sig | Item | Finding | Evidence (quote, figure, table) | Fix | Ruling / guide |

## Judgment calls (a reviewer could go either way)
- <call>: what the curation did, the likely reviewer reaction, the defence to post (with issue numbers)

## Can't verify without
- <file>: which values depend on it
```

Write the mentor comment in the voice mentors use: short imperative bullets ("Change the test to DESeq2 only" (TheTosin #1197); "curate unclassified Lachnospiraceae (Taxonomy ID: 186928)" (annemarie-sharp #2050)), giving the taxon ID or exact value when you know it.

## 6. After the real review arrives

Compare the mentor's review with this pre-review. For every correction the pre-review missed, add the lesson to the skill (SKILL.md Step 9) and log it in the lessons ledger, so the next pre-review catches it. Record the comparison (found / missed / extra) in the curation's VERIFICATION.md.

## 7. How well this works: blind test, 2026-11-01

Six studies mentors had already reviewed were rebuilt as they stood **before** review (BugSigDB page history). Each was given to a fresh reviewer agent running this procedure on a copy of the skill with nothing from those six reviews in it, and its findings were scored against the mentors' real corrections (43 testable; 3 more were untestable because their pages were deleted later).

| Study (issue, mentor) | Group | Mentor corrections found | Predicted vs actual score |
|---|---|---|---|
| 30574320 (#1971, DocTeedee) | clean | 4 of 4 | 15.5 vs 19.5 |
| 34857640 (#1928, DocTeedee) | clean | 2 of 4 (+1 flagged as a judgment call) | 22.5 vs 21 |
| 41697396 (#2050, annemarie-sharp) | clean | 4 of 4 (same four taxon IDs as the mentor) | 16 vs 20 |
| 40686474 (#1143, annemarie-sharp) | rulings knew some answers | 6 of 8 (+1 partial) | 15 vs 18 |
| 38762736 (#1197, TheTosin) | rulings knew some answers | 13 of 14 | 11 vs 13 |
| 41773858 (#1134, annemarie-sharp) | rulings knew some answers; one precedent query saw live values | 9 of 9 | 8.5 vs 12 |

**Overall 38 of 43 found (88%); clean studies 10 of 12 (83%), 11 of 12 counting the flagged call.**
- **Misses:** the Group 0 / reference level in a MaAsLin2 contrast (#1928; the approved page fixed the directions instead), a descriptive supplementary table cited as a source (#1143), and one pairwise contrast in a three-group figure (#1197).
- **Over-correction:** an experiment proposed from uncorrected "trend" taxa, which the mentor deleted (#1971).
- **What changed:** each miss and the over-correction is now a check in §4. Score predictions were too harsh by about 2.5 points, hence the calibration rule in §3 phase 4.

**Round 2, with supplements** (the user downloaded the PMC author-manuscript supplements through their browser, `scripts/fetch_sources.py`): #1971 found 4 of 4 again. For #1928, the direction swap was confirmed from Supplemental Material 4 (exactly the mentor's 5 increased / 9 decreased), and the score prediction moved to 22 vs 21. But two small corrections the first run caught (description length, condition wording) were dropped. Run-to-run variance on small items is real, hence the fixed checklist in §3 phase 3b.

Treat a FIX FIRST verdict as reliable and a predicted score as a lower bound. Re-run this test when the procedure changes: rebuild pre-review versions with `scripts/prereview_snapshot.py` and compare against the mentor's comment.
