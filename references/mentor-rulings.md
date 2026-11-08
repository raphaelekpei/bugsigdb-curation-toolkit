# Official mentor rulings: case law for BugSigDB curation

Distilled from **every comment by BugSigDB's eight official mentors** (SvetlanaUP, lwaldron, cmirzayi, jwokaty, annemarie-sharp, Buraah, TheTosin, DocTeedee; list from issue #1274) across waldronlab/BugSigDBcuration and waldronlab/BugSigDB, 2020 to 2026-10-22:
- about 6,800 mentor items were read
- 3,074 were substantive
- 1,557 unique instructions were extracted

The community's "Category_talk:Pages_with_missing_NCBI_ID" crosswalk was also used. Citations read **(mentor, YYYY-MM, #issue)**. "B#" means the main BugSigDB repo; everything else is BugSigDBcuration.

**Guides are kept separately** in `mentor-guides.md`: teaching material (walk-throughs, FAQs, worked scorings) posted by mentors but often written by contributors. Rulings here outrank them.

**How to weigh them:**
- A recent official-mentor ruling overrides older policy wording; several here explicitly update the policy (e.g. "we have updated curation of group as opposed to the curation policy").
- Maintainers (SvetlanaUP, cmirzayi, lwaldron) outrank other mentors.
- Mentors outrank peer reviewers.
- Where mentors disagree or a rule changed over time, §12 lists both sides. Say which one you followed, and add a discussion note.

## Contents
1. Scope: what is and isn't curatable
2. Study page and study design
3. Defining experiments
4. Subjects, body site, condition
5. Groups, names, definitions, sample sizes
6. Antibiotics exclusion
7. Sequencing
8. Statistics: test, transformation, threshold, MHT, LDA
9. Matched on and confounders
10. Alpha diversity
11. Signatures: source, description, direction, members
12. Disagreements and rules that changed over time
13. Workflow, reviews and etiquette
14. Rulings from reviews after the 2026-10-22 harvest

---

## 1. Scope: what is and isn't curatable

- We curate only statistically significant differential abundance between groups. "We curate all reported significantly abundant microbiome results" (SvetlanaUP, 2025-11, #974). "We curate all significant taxa represented in a comparison" (TheTosin, 2026-03, #1130). "We only want statistically significant results, not all results" (cmirzayi, 2023-06, #8).
- **Not curatable:**
  - relative abundance or composition plots without a test (Buraah, 2024-09, #431; SvetlanaUP, 2024-03, #123)
  - prevalence (SvetlanaUP, 2024-10, #452)
  - Firmicutes/Bacteroidetes (B/F) ratios (SvetlanaUP, 2025-04, #715)
  - genes or functional results (annemarie-sharp, 2025-06, #689; Buraah, 2025-06, #766)
  - indicator analysis (DocTeedee, 2025-12, #956)
  - an overall multi-group test with no post-hoc or pairwise result (cmirzayi, 2026-04, #1160)
    - The same thread settles the "compare the group means" workaround: TheTosin had advised reading direction from each group's mean in a 4-group table (2026-03-28); cmirzayi then ruled the table not curatable (2026-04-02) and SvetlanaUP deleted the experiments built that way. So means or medians quoted in the Results don't rescue an omnibus-only result.
    - Skill note, not yet mentor-reviewed (36552306): a Majorbio "Kruskal-Wallis H test bar plot" with only one p-value column (no pairwise marks, no post-hoc CI panel) and Methods naming no post hoc is exactly this case. Directional prose citing the omnibus p ("more abundant in M than in the other groups") is a reading of the mean bars, not a pairwise result; #1160 rejected comparing means. Score the screening 85.
  - tables that don't show direction (TheTosin, 2025-12, #785)
  - **interaction effects** (SvetlanaUP, 2026-03, #1072)
    - Skill note, not yet mentor-reviewed (42059388): check the model formula before applying #1072. `y ~ covariates + group:x` **without** `x` and `group` main effects (R prints `groupA:x`, `groupB:x`) gives one slope per group, each tested against zero. That's a within-group (subgroup) association, curated as its own experiment per group (#726), even when the authors call it an "interaction" model. Only a term that tests the *difference* between groups (`x + group + group:x`, or a moderation analysis as in #1072) is an interaction effect. Passing this check makes the rows *curatable*, not *required*: apply the presented-comparison test in `mentor-guides.md`.
  - review papers (SvetlanaUP, 2026-04, #1257)
  - papers with no statistical analysis (SvetlanaUP, 2024-03, #144)
  - figures too unclear to read direction (annemarie-sharp, 2026-04, #1124; Buraah, 2025-08, #820)
- **Curatable:**
  - Spearman/Pearson heatmaps with significance marks (TheTosin, 2026-03, #1054 and #1151)
  - random forest results (TheTosin, 2026-01, #1002; annemarie-sharp, 2025-10, #898)
  - one-vs-all LEfSe (cmirzayi, 2024-04, #231)
  - clinical-marker figures (TheTosin, 2026-03, #1151; DocTeedee, 2026-04, #1154)
  - viral and phage signatures (SvetlanaUP, 2024-05, #384; cmirzayi, 2023-09, #73)
  - fungal (ITS) signatures (SvetlanaUP, 2024-05, #384)
  - data from a peer-review file, if relevant (SvetlanaUP, 2026-09, #1531)
- **Always check the supplementary material.** Supplementary tables are frequently the missed curatable source (TheTosin, 2025-11, #941; annemarie-sharp, 2026-04, #1134; SvetlanaUP, 2026-04, #1272).
- **Preprints:** curate the peer-reviewed published version (SvetlanaUP, 2026-02, #1077 and 2025-08, #566). If a curation moves to the published PMID, edit the PMID field rather than renaming the page (lwaldron, 2025-08, B#279).
- **Journal moratorium:** "Frontiers in Microbiology" and related journals (SvetlanaUP, 2026-10, #2012; cmirzayi, 2026-02, #1032 started it).
- **Meta-analyses:** "a study of studies… we curate the pooled/combined results of selected original research reports" (SvetlanaUP, 2025-10, #890).
  - Skill note, not yet mentor-reviewed (39197689, literature meta-analysis of published 16S case-control studies, pooled WMD forest plots): one experiment per pooled contrast (CRC vs HC, AD vs HC, CRC vs AD), all ranks combined (#1051). Test "Meta-Analysis" (SvetlanaUP-reviewed 32557853 Exp 11), relative abundances, threshold from the stated alpha, MHT No unless a correction is named. Sample sizes = total included subjects per group (32557853 Exp 11, 37399128), with the per-rank study subsets in a note. Location = every country in the included-studies table. 16S region = span of the studies' regions (SvetlanaUP-reviewed 29373083 coded V1-V5). Antibiotics blank when the windows differ between studies or some state none (#843). Confounders blank: meta-regression explores heterogeneity and doesn't adjust the pooled estimates. Meta-regression, leave-one-out sensitivity and publication-bias tests aren't curated. A summary significance heatmap (here Fig 6B) is the best member count check; it exposed Results text that labelled two CRC vs AD estimates "CRC vs HC". Blind senior review: 23/23.
- **Very large result sets** (e.g. 344 species): record the main table and add the note "For a comprehensive listing… please see Supplemental Table X" (SvetlanaUP, 2025-04, #735). A study can be "theoretically curatable but not practically" (SvetlanaUP, 2025-01, #297).
- **Secondary, off-focus analyses** (e.g. a side Spearman figure): optional. "If you choose not to curate, kindly write a note on this exclusion" (TheTosin, 2025-12, #954; 2025-08, #818).
- **Microbiota-derived community types** (C1–C3 "community types" that the authors cluster from Bray-Curtis/PCO) are unsupervised clusters, so LEfSe across them isn't curated; neither is the prevalence of a condition across them (#452). Note the exclusion (skill note, PMID 35565271; not yet mentor-reviewed).
- **LEfSe whose community-type (subclass) correction removes every taxon:** when the authors still show the uncorrected LEfSe figure as their result (e.g. tumor vs adjacent tissue, Fig 2C) and say that "no taxa were identified when correction for community type was applied", curate the figure (#974, #990) with a note. This is in tension with lwaldron #26 (prefer the adjusted analysis); scored 70 (skill note, PMID 35565271; not yet mentor-reviewed).
- **Not curatable after all?** Report it on the GitHub issue; "your effort will be recorded" and you pick another paper (SvetlanaUP, 2024-03, #144; cmirzayi, 2024-03, #136). If every signature in an experiment is deleted, delete the experiment too (SvetlanaUP, 2025-10, #888).
- **Don't contact authors** to interpret a paper; "The paper should be interpreted by the curator as it is written" (SvetlanaUP, 2024-04, #123). Information that authors volunteer can be used (SvetlanaUP, 2024-04, #173).

## 2. Study page and study design

- **Study page:** enter the PMID, choose **Auto**, and clear any pasted DOI or URI (annemarie-sharp, 2026-10, #2011). With no PMID, leave the PMID box blank; on the next page use `Study_` plus the DOI without "https://doi.org/" (SvetlanaUP, 2026-08, #1979; cmirzayi, 2025-11, B#143). Never type a DOI or URL into the PMID field (SvetlanaUP, 2026-02, B#316).
- **Authors often mislabel their own design:** "it's not rare that authors define their own study design incorrectly" (SvetlanaUP, 2023-10, #70).
- **Disease vs healthy → case-control.** "Several discussion from the most recent office hours mentioned to prioritize this and curate as case control" (TheTosin, 2025-12, #798; also #804, #935; Buraah, 2025-10, #882).
  - Exception: participants grouped by existing characteristics rather than selected as cases and controls can be cross-sectional. ⚠️ In #1381 TheTosin first said cross-sectional for spontaneous vs IVF pregnancy (2026-10-20), then reverted to **case-control** on 2026-10-22: "Chloe did mention retaining the initial study design as 'case control' as she considers Pregnancy to be a disease related term". Pregnancy-related contrasts → case-control.
    - Skill note, not yet mentor-reviewed (37696898): **counter-precedent** 38036587 (#1219, SvetlanaUP-reviewed 2026-04; peer fiddyhamma: "cross-sectional as all participants are pregnant women and the difference is delivery time and complications", including a PTB with vs without PROM experiment). For a whole cohort regrouped by a measured pregnancy variable (duration of membrane rupture), the two conflict; leaned case-control at 50 (newer maintainer stance, plus the authors' "secondary analysis of a case–control study"). Don't cite #1381 as support for cross-sectional: its final outcome is case-control.
    - Skill note, not yet mentor-reviewed (31417292): **non-pregnant vs each trimester** (separate women, one stool each) → case-control at 70 under #1381. The older precedent 36467732 coded the same design cross-sectional; it predates #1381, so mention it only as the alternative in a discussion note. The first draft of 31417292 (2026-10-31) followed 36467732 and was corrected on 2026-11-01.
  - **Newborns or infants grouped by a maternal disease** (e.g. GDM): case-control. Mentor-reviewed precedent: 36154141 (GDM meconium, SvetlanaUP 2024-10). Older cross-sectional codings (24223144, 2021; 30042470, an antibiotic exposure rather than a disease) predate the 2025–2026 office-hours guidance (skill note, PMID 30332459).
  - Some mentors add "cross-sectional" when the paper also has further cross-sectional comparisons (annemarie-sharp, 2025-06, #704 and #776).
- **Same people before and after → time series / longitudinal**, even if the paper says case-control (Buraah, 2025-04, #753; annemarie-sharp, 2025-05, #552).
- **Non-human animals → laboratory experiment**: "Any studies of non-humans… are almost certainly laboratory experiments" (cmirzayi, 2023-11, #111). This includes lab-housed mosquitoes, even if randomly picked (SvetlanaUP and TheTosin, 2025-07, #415).
  - Add "laboratory experiment" alongside the human design when a paper has both (cmirzayi, 2025-10, #846; annemarie-sharp, 2026-09, #1367; TheTosin, 2026-01, #926).
- **Animals that weren't experimentally manipulated** (farm cows grouped by parity, captive birds, equids under standard husbandry) are a recurring judgment call (skill note; ask on Zulip if graded). #111 says non-human studies are almost always laboratory experiments, but the export is split: farm animals have 16 lab-experiment studies vs 9 cross-sectional; the bird precedents 41209719 and 41375452 are cross-sectional. Animals sampled before an event and followed to the outcome (ewes before artificial insemination → pregnant or not) fit prospective cohort, as in the mentor-reviewed cow precedent 32238772. Give the precedent counts in the note (33499942, 33891612, 37760279, 40369688).
- **Prospective cohort vs cross-sectional:** cohorts followed for outcomes are prospective cohort (cmirzayi, 2023-11, #118 and #126; 2023-10, #101).

## 3. Defining experiments

- **Each distinct contrast is an experiment.** Examples:
  - each diet component column (cmirzayi, 2025-09, #849: "This figure actually has seven experiments")
  - each clinical marker (TheTosin, 2026-03, #1151; annemarie-sharp, 2025-10, #884)
  - each body site (TheTosin, 2024-10, #477; 2026-04, #1197)
  - each cohort (Buraah, 2025-10, #879)
  - each pairwise comparison
  - each timepoint (cmirzayi, 2025-10, #846)
    - Skill note, not yet mentor-reviewed (40377699): read the model before splitting by timepoint. If time enters a mixed model as **one numeric or scaled trend** (e.g. `sam$time` = 0/1/2 for pre, 6 h and 24 h, then `scale(time)`), there is one exposure coefficient across all visits, not separate "6 h vs pre" and "24 h vs pre" contrasts: curate one experiment. Group framing is open (no ruling found): lean "Pre-exposure" vs "Post exposure (6 h and 24 h)" with a note that time was a scaled 0/1/2 trend (precedent 30804895, pre- vs post-smog); the alternative is "Low/High time since exposure". Also check whether the authors' results table keeps rows significant for *any* fixed term (e.g. `padj < 0.05` on covariates too), and curate only the rows for the exposure term.
- **Don't force experiments** (guide, not a ruling): "If it's not a distinct comparison, don't curate it separately… Forcing multiple experiments from secondary analyses waters down the curation" (guide posted by SvetlanaUP, 2026-09, #910; see `mentor-guides.md` G1, and its **presented-comparison test**, applied in 42059388).
- **Different tests on the same contrast** → separate experiments when the significant taxa differ, or when only one test adjusted for confounders. This was confirmed with cmirzayi (TheTosin, 2026-01, #960; annemarie-sharp, 2025-10, #722; Buraah, 2025-01, #542).
  - A multi-group test followed by its own post-hoc pairwise test → combine both tests in one experiment (TheTosin, 2026-01, #960).
  - **Two-way (factorial) ANOVA with Tukey post hoc, run separately per period** (e.g. fluoxetine × early life stress within pregnancy and within lactation, bars with brackets for four named pairs): one experiment per **bracketed pair per period**, test 'ANOVA' + 'Post-Hoc Pairwise', MHT Yes (#808), '#' (p < 0.1) brackets left out. Main effects (one factor pooled over the other) have no pairwise marks and their direction would come from the four group bars (#1160), so they were left out with a study note listing each one (curator decision; the 35565271 note in §9 curated a main effect instead, so a mentor may ask for them). Interaction terms are out (#1072). Animal precedent for the pairwise route: SvetlanaUP-reviewed 38378622 (multi-group fluoxetine bar plots as pairwise experiments). Skill note, PMID 31971855; blind senior review agreed; not yet mentor-reviewed.
  - One panel that overlays two analyses, e.g. a LEfSe LDA-score heatmap per pair with white asterisks from a separate "t test followed by FDR correction" (34607559 Fig 3B): each pair gets a LEfSe experiment (all coloured cells) and a t-test experiment (asterisked cells only), because the lists differ (#960). The text's "N genera with significant differences" usually counts only the asterisks; curate the LEfSe cells too (#1194) (skill note, PMID 34607559; not yet mentor-reviewed).
- **Same contrast, test and details at different taxonomic levels** (e.g. a phylum table plus a genus table, or a figure plus a table) → **one experiment**; combine ranks in one signature (TheTosin, 2026-03, #1051; annemarie-sharp, 2025-12, #722; lwaldron, 2023-03, #26).
- **Pooled analysis vs subgroup analysis** → separate experiments (Buraah, 2025-07, #726).
- **Compact letter displays** (a / b / ab): "a vs b, b vs c, a vs c, a vs bc is curatable. While a vs ab, a vs ac, b vs ab, b vs bc are not curatable… curate as separate pairwise experiments" (TheTosin, 2025-12, #811). Groups that share a letter aren't significantly different (TheTosin, 2025-12, #811, Exp 6–7).
- **One-vs-all LEfSe:** one experiment per group. Group 1 is that group, Group 0 is all the others combined, and there's one *increased* signature each. Leave alpha diversity blank (cmirzayi, 2024-04, #231 and 2023-11, #111; annemarie-sharp, 2025-11, #899; Buraah, 2025-10, #882; TheTosin, 2026-01, #740). Misreading one-vs-all as pairwise "caused many duplicated signatures" (SvetlanaUP, 2024-11, #306).
  - A multi-class LEfSe where only two classes have significant features is drawn two-sided (negative bars), like a two-class plot. If the caption and text describe the same multi-class analysis (40377305 Fig S5C: "insufficient weight gain did not show significant taxa"), still curate one-vs-all, one experiment per class with bars (skill note).
  - A class with no LEfSe features (legend: "No feature was found for BEM samples") gets no experiment. The remaining classes are still one-vs-all, with Group 0 combining all the other classes, including the empty one (skill note, PMID 32369505; not yet mentor-reviewed).
  - Skill note, not yet mentor-reviewed (41199330): in the export, one-vs-all Group 0 is named "Other …" or lists the combined groups. When Group 1 is the healthy group, reviewed precedents keep the disease as the condition (36995230 Exp 5, 40827923 Exp 2).
- **Within-person before/after** comparisons are pre/post experiments, not pairwise between groups (cmirzayi, 2025-12, #966).
- **Different group names but the same test → a new experiment** (TheTosin, 2025-12, #943). Identical results for different comparisons are still recorded separately (SvetlanaUP, 2024-05, #214).
- **Dietary principal components contrasted by quartile** (DESeq2, quartile 4 vs quartile 1 of each diet PC): one experiment per PC, by analogy with "each diet component column" (#849). Group 0 "Quartile 1 of diet principal component N (PCN)", Group 1 "Quartile 4 …", the PC's main loadings in the Group 1 definition, direction from the Q4-vs-Q1 log2FD, and sample sizes blank when quartile n isn't printed. Don't copy alpha-diversity results from continuous-PC regressions into the quartile experiments. The same pattern applies to quartiles of a blood marker (CRP, WBC; #1151). When the Results discuss only FDR < 5% hits but the table lists the paper's default FDR < 10%, curate the table at 0.1 (#608) and record the 5% subset (skill note, PMID 29643500; not yet mentor-reviewed).
- **Sensitivity analyses presented only as a replication check** (e.g. "Four out of the five… were replicated with ANCOM-BC2", plus subgroup and extra-covariate tables): leave them out with a note, under #954/#818 (optional secondary analyses) and the primary-test guidance (#910 guide). Keep a contingency draft for #960 (different test, different taxa). In ANCOM-BC2 output, count only rows with `passed_ss` = 1; rows with 0 fail its own sensitivity filter. Skill note, PMID 40859402; senior review agreed; not yet mentor-reviewed.
- **Experiments made only from alpha diversity** shouldn't be created; alpha diversity is added information on a signature experiment (SvetlanaUP, 2025-01, #399; 2024-05, #368).

## 4. Subjects, body site, condition

- **Location:** check author affiliations or study sites (e.g. "Republic of Korea", TheTosin, 2025-11, #842). Use the exact dropdown country.
- **Host species:** only one can be recorded. "Please record one bat species and the rest with an explanation… in the discussion notes" (SvetlanaUP, 2024-12, #540). Different species reported separately → separate experiments (Buraah, 2026-04, #1148). Host names must match NCBI taxonomy (lwaldron, 2023-10, #123).
- **Body site: the most specific site actually sampled, one per experiment.**
  - caecum contents → Caecum, not feces (annemarie-sharp, 2025-05, #759; TheTosin, 2026-02, #974)
  - subgingival plaque → Subgingival dental plaque, not oral cavity (Buraah, 2026-04, #1128)
  - "Mucosa" is too vague; use the named mucosa (TheTosin, 2026-03, #1130)
  - nose swabs → nasal cavity (cmirzayi, 2023-11, #118)
  - large intestine is close but feces is right for stool (cmirzayi, 2024-04, #149)
  - stool metagenomics stays Feces even when the groups are defined by urine findings (annemarie-sharp, 2025-10, #893)
  - meconium experiments → meconium (annemarie-sharp, 2026-01, #838)
  - rectal swabs → Rectum: all 3 BugSigDB studies that describe rectal swabs use it (export 2026-10-23), by the same "most specific site" rule, even when the paper calls them "fecal samples"
- **Lesion vs adjacent normal tissue in the same patients** (tumor vs para-tumor, metaplastic vs unaffected mucosa): the condition is the disease, Group 0 is the adjacent tissue, and the body site is the single organ. The design is usually case-control (38 of 71). Reviewed precedent: Colorectal cancer 18, Gastric cancer 9 (export 2026-10-31). Paired Wilcoxon signed-rank → "Mann-Whitney (Wilcoxon)" with a note. The "Sampling site" condition is for different body sites, not this case (skill note, PMID 32369505).
- **Condition = what *this experiment* contrasts, not the whole study** (SvetlanaUP, 2026-10, #1381; lwaldron, 2023-04, #30: "not one that was shared by everyone"; annemarie-sharp, 2026-06, #1102).
  - Never "Gut/Vaginal microbiome measurement" (SvetlanaUP, 2026-05, #1272; cmirzayi, 2024-10, #494; TheTosin, 2026-02, #930).
  - Community state type (CST) contrasts (one CST vs the rest, or CST vs CST) use Condition "Microbiome": every CST experiment in the export does (17 experiments), including the SvetlanaUP-reviewed 32719372 and 35250962 (export 2026-10-25). Skill note, PMID 38898981; the precedent is mentor-reviewed, the generalisation is not.
  - "Healthy control" can't be a condition; Crohn's plus ulcerative colitis versus controls → Inflammatory bowel disease (Buraah, 2025-10, #882).
  - HPV / cervical lesion studies: "Human papilloma virus infection" for HPV+ vs HPV− (70 experiments), "Cervical intraepithelial neoplasia" for CIN vs either control. The older "Cervical glandular intraepithelial neoplasia" is a legacy mapping; 36269135 and 38755259 use the current term. Skill note, PMID 40304477; not yet mentor-reviewed
- **Specificity:**
  - use the closest specific term for severe disease (e.g. "chronic periodontitis", TheTosin, 2026-04, #1106 and #1110)
  - but don't go broader than the paper ("Meningioma" rather than "benign brain neoplasm", TheTosin, 2026-01, #1019)
  - induced disease in animals → "Experimental arthritis", not rheumatoid arthritis (annemarie-sharp, 2025-11, #977)
- **Lab values** use EFO measurement terms named after Group 1: "High density lipoprotein cholesterol measurement", "serum gamma-glutamyl transferase measurement", "Fasting blood insulin measurement", "estradiol measurement" (TheTosin, 2026-04, #1136; 2025-12, #918; 2025-09, #817).
  - "Body weight" when both loss and gain are compared (Buraah, 2025-04, #658)
  - "Increased body weight" for a high-weight Group 1 (TheTosin, 2025-05, #741; 2025-08, #820)
- **Treatments:**
  - "Response to transplant" (TheTosin, 2026-01, #1023)
  - "Response to antiviral drug" for post-ART comparisons, "HIV infection" for HIV status (TheTosin, 2026-01, #984)
  - "Response to antibiotics" rather than a drug name (DocTeedee, 2026-04, #1142)
    - Intrapartum antibiotic prophylaxis (IAP, e.g. penicillin for GBS): the reviewed export precedents use the glossary spelling **"Response to antibiotic"** (31534227, 40175554, 40813371); the older 26971496 and 28789705 used "Antimicrobial agent". Vaginal GBS+ vs GBS− without an antibiotic contrast uses "Streptococcal infection" (36544085, 40713506, case-control). Skill note, PMID 28178310 (export 2026-11-01); not yet mentor-reviewed.
  - ~~"Treatment outcome measurement" (Buraah, 2025-08, #799)~~ **Superseded:** SvetlanaUP's clean-up issue #844 (2025-08-28) calls "treatment outcome measurement" "too general" and asks for "the study specific condition" (e.g. type 1 diabetes, kidney transplant, colorectal cancer, smoking status measurement). A maintainer outranks; don't use it.
  - "Delivery method" (DocTeedee, 2026-03, #1135)
  - **Probiotic or supplement groups:** use the study's disease as the condition, not "Nutraceutical" or "Diet", when the contrast is set in a disease population. SvetlanaUP-reviewed precedents: 37836514 Exp 14–15 (one-vs-all Bifidobacterium formulation → Constipation), 35956415 (preterm infants given probiotics → Premature birth), 37225124, 39861457, 36228569; #844 asks for the study-specific condition. Found with the bugsigdb.org SMW query `[[Group 1 name::~*robiotic*]]|?Condition|?Reviewer` (skill note, PMID 41199330; the precedent is mentor-reviewed, the generalisation is not)
  - fecal transplant studies are about response to FMT, not the donor's condition (cmirzayi, 2023-11, #111)
  - **Mother vs infant** (and infant timepoints): Condition "Age", Mother = Group 0 (the earlier sample and usually the paper's reference), infant = Group 1. Reviewed precedent 38589361 (Mothers vs Infants, Age); infant timepoints 40742167, 23339708, 27827448 also use Age (skill note, PMID 33847206; not yet mentor-reviewed)
  - **Semen-parameter contrasts in infertility-clinic men** (skill note, PMID 35329834; the precedents are SvetlanaUP-reviewed, the generalisation is not): morphology → "Abnormal sperm morphology" (40915037 Exp 2); count or concentration → "Sperm measurement" (38212576 Exp 3; no oligozoospermia or sperm-count glossary page); motility → "Reduced sperm motility" (38212576 Exp 2). Men sampled once and grouped afterwards by their own semen parameters → "cross-sectional observational, not case-control" (both precedents).
  - **Culture-positive vs culture-negative** samples: culture-negative = Group 0 (36544085, SvetlanaUP). Condition = the infection; for bacteriospermia (positive spermoculture) no specific term exists, so the nearest parent "Bacterial disease" (#1965) at 70 (skill note, PMID 35329834).
  - **Induced endometriosis in mice** (intraperitoneal donor-uterus injection): Condition "Endometriosis", design laboratory experiment. 7 mouse experiments in the export use it, incl. cmirzayi-reviewed 29462324; there is no "experimental endometriosis" term, so #977 ("Experimental arthritis") has no analogue here. Skill note, PMID 37178109; not yet mentor-reviewed.
- **When no exact term exists:** "We use defined EFO terms and if the term is not in there we can not add it" (SvetlanaUP, 2025-05, #748). Search related terms, then use the nearest parent (SvetlanaUP, 2026-10, #1965). "Diet" is a fallback for supplements and prebiotics (cmirzayi, 2024-10, #494); "Diet measurement" when "Diet outcome measurement" doesn't exist (Buraah, 2025-06, #773).

## 5. Groups, names, definitions, sample sizes

- **Purpose:** "our goal here is not just to extract the information as written but to create something that someone looking at the curation can understand without having to look at the original paper" (cmirzayi, 2023-10, #106).
- **Group 0** = control, unexposed, lower severity, non-responder (TheTosin, 2025-02, #591; annemarie-sharp, 2025-10, #808). **Group 1** = the case or outcome group (guide posted by SvetlanaUP, 2026-09, #910; `mentor-guides.md` G1).
  - For one-vs-all and species comparisons, keep a consistent choice across experiments (TheTosin, 2026-02, #974).
  - If groups were swapped, "just switch the abundance, no need to curate the taxa all over" (TheTosin, 2026-01, #811).
- **Names:**
  - start with a capital letter (TheTosin, 2026-01, #679 and #960; annemarie-sharp, 2025-10, #884)
  - write abbreviations in full, with the abbreviation in brackets after (SvetlanaUP, 2025-02, #295: "No Antibiotics (Abx)"; TheTosin, 2026-01, #926: "Chronic Kidney disease (CKD) patients"; DocTeedee, 2026-04, #1050)
  - don't wrap the whole name in parentheses (cmirzayi, 2025-11, #846)
  - match the paper's wording ("Food allergic children", Buraah, 2025-04, #763; figure labels, Buraah, 2025-10, #800)
  - spell carefully (TheTosin, 2026-04, #1054)
- **Group 1 definition:** describe the group itself (its diagnostic criteria or intervention), not the experiment or the signature source (Buraah, 2024-11, #469; 2025-01, #542; TheTosin, 2025-01, #542 and 2025-12, #885).
  - Describe what was actually done, without interpretation (annemarie-sharp, 2025-10, #883).
  - Write more than the group name repeated (annemarie-sharp, 2026-10, #1960).
  - Keep it identical across experiments that share the same Group 1 (annemarie-sharp, 2025-10, #908).
  - Use "≥", not ">", when the paper does (annemarie-sharp, 2026-09, #1367); "5 x 10^5" for superscripts (annemarie-sharp, 2025-10, #655).
- **Sample sizes:**
  - the final analytic n per group (guide posted by SvetlanaUP, 2026-09, #910: "126, not the initial screening number of 200"; annemarie-sharp, 2026-09, #1452: 18 after QC, not 19)
  - leave blank if not reported (TheTosin, 2024-12, #524; Buraah, 2025-06, #749)
  - leave blank for correlation experiments (TheTosin, 2025-05, #741)
  - leave blank when the paper gives *samples* rather than subjects, e.g. "153 fecal samples" of birds (DocTeedee, 2025-12, #695)
  - matched pairs: "81 pairs" means 81 in each group (Buraah, 2025-06, #775)
  - never swap the two groups (TheTosin, 2024-11, #439)
  - mouse studies often don't report n (cmirzayi, 2025-10, #846)

## 6. Antibiotics exclusion

- **Only antibiotic exclusions are recorded**, for standardisation: "Antibiotics significantly alter microbiota composition, making this the most critical exclusion criterion" (guide posted by SvetlanaUP, 2026-09, #910; the rule itself is policy and SvetlanaUP #843).
- **Format:** a number, a space, and a lowercase unit: "1 month", "3 months" (TheTosin, 2026-07, #1501 and 2026-01, #1019; annemarie-sharp, 2025-10, #893). Normalise "3 Months" and "1 Month" to lowercase (SvetlanaUP, 2025-08, #843).
  - Weeks become months when they convert exactly: 8 weeks → "2 months" (SvetlanaUP, 2026-03, #1153), 4 weeks → "1 month" (TheTosin, 2025-02, #555).
  - Give a number rather than prose like "last year" (SvetlanaUP, 2024-12, #462).
  - Windows defined by an event rather than a duration: convert to the number of days or months before sampling when the paper gives both ends. "Antibiotics on or after the day of delivery" excluded, samples at postpartum day 4 → "4 days", with a discussion note giving the derivation; not "currently on antibiotics", because recent use isn't current use (#1381) (skill note, PMID 29069100, derived from #462 and #1381; not yet mentor-reviewed)
- **Uniform phrases:** "currently on antibiotics" for active use (SvetlanaUP, 2025-09, #836 and 2026-05, #1118; TheTosin, 2025-08, #828 rejected "Currently taking antibiotics"). "Recent antibiotic use is not equivalent to current use; it should be curated exactly as reported" (SvetlanaUP, 2026-10, #1381).
- **Leave blank** when there's no exclusion (SvetlanaUP, 2025-08, #843; TheTosin, 2026-03, #1080). Never write "Not reported" (Buraah, 2026-04, #1148), and don't add notes or sentences (annemarie-sharp, 2025-11, #899; TheTosin, 2024-10, #477).
- **Antibiotics during pregnancy** (infant or meconium studies): "9 months". All 5 reviewed precedents use it (24223144, 28932201, 30633889, 35387603, 37813882); "During pregnancy" appears only in unreviewed studies (export 2026-10-30). This follows #462 (a number, not prose). Skill note, PMID 30332459; not yet mentor-reviewed.
- **Not exclusions:**
  - "samples were collected before any antibiotic treatment": this is about when samples were taken, not who was excluded, so leave the field blank (skill note, PMID 41157277)
  - an *inclusion* criterion, e.g. "no antibiotics for a month to be included" (TheTosin, 2025-04, #657)
  - animals that were *given* antibiotics (Buraah, 2025-10, #800)
  - animal studies rarely have this criterion (cmirzayi, 2025-10, #846)
- **"28 days" → "1 month"**: 28 days is exactly 4 weeks, so #555 (4 weeks → 1 month) and #893 apply; export 2026-11-01: "1 month" 1,141 experiments vs "28 days" 2. Scored 70; the literal "28 days" is the alternative (Buraah #1137 kept "30 days"). Skill note, PMID 26600277; not yet mentor-reviewed.
- **Open: a cohort statement rather than a criterion**, e.g. "No women in this study were taking antibiotics at the time of surgery or in the 3 weeks prior to surgery" (not in the exclusion list). There's no ruling (#910, #843, #1080, #657 checked). Entered "3 weeks" at 50 (29 uses in the export); the alternative is blank. Ask on Zulip (skill note, PMID 35565271).
- **Open: windows that differ by group** (UC patients 12 weeks, healthy controls 6 months; 41398357). The format rulings (#843, #462, #899, #477) rule out a two-window sentence. Entered '3 months' (12 weeks per #1153/#555), which is the window every participant met and Group 1's own criterion, at 70. The alternative is '6 months'. Qualified live forms ('3 months for controls only', 38792606) are unreviewed. No ruling found; blind senior review agreed. Skill note, not yet mentor-reviewed.

## 7. Sequencing

- **Use the method behind the curated result.** Examples: 16S for the main experiments (Buraah, 2024-09, #431); metatranscriptomics or GA-map when that's what produced the result (cmirzayi, 2023-11, #99 and #80). RT-qPCR with gene-specific primers isn't microbiome sequencing (SvetlanaUP, 2025-06, #744).
- **Platform:** only if it's stated, otherwise leave blank (SvetlanaUP, 2025-06, #744; TheTosin, 2026-01, #1002). A platform stated only for the human part doesn't carry over to animals (TheTosin, 2025-03, #662). Ask for missing platforms to be added to the list (TheTosin, 2025-12, #837: DNBSEQ-G400; 2025-05, #549: whole exome sequencing).
- **Variable region:** for qPCR, no region (TheTosin, 2025-11, #882). Non-contiguous primer sets: don't record a misleading range like V2–V9; add a note naming the primer sets instead (SvetlanaUP, 2025-04, #767). Add a note when the region is inferred (DocTeedee, 2025-12, #971: "16S, V1-9").
  - Stated region narrower than the primers (e.g. "V4" with 515F/909R, which span V4–V5): enter the region the paper states and add a note naming the primers. Reviewed precedent: 29665823 states "V4 region" with 515F/907R and is coded V4. The 9 reviewed 515F/907R studies coded V4–V5 stated V4–V5 or named only the primers (skill note, PMID 30332459)
  - **Side correlations with maternal or clinical variables**, even supplementary ones, are curated when they're few: 36566315 Exp 3 (pregestational BMI, Table S1, reviewed by SvetlanaUP) (skill note, PMID 30332459)
  - Five-region "5R" 16S (LC-Bio / SMURF pipeline, Nejman et al. 2020; NovaSeq 2×150): regions V2, V3, V5, V6, V8 are non-contiguous, so apply #767: leave both bounds blank and name the five regions in a note. The export has no non-contiguous region code (checked 2026-10-30). Taxa come as Greengenes 13_8 species labels, several of them outdated names (taxonomy.md §9). Skill note, PMID 40304477; not yet mentor-reviewed

- **Platform stated only in a cited methods paper** ("as previously described [16]"): open the cited paper. If it names the instrument for the same samples, enter the platform at 70 with a note; #744/#1002 say platform only if stated. FINRISK 2002 shallow shotgun (UCSD, 2017) = Illumina HiSeq 4000 (Salosensaari 2021, PMC8113604); the reviewed FINRISK studies 40214782 and 37119735 are coded Illumina. Skill note, PMID 40859402; not yet mentor-reviewed.

## 8. Statistics: test, transformation, threshold, MHT, LDA

- **Only the test that produced the differential-abundance result.** "We only want the specific one that was used for Differential abundance test… record only DESeq2. You can remove the rest" (Buraah, 2026-04, #1127; 2026-03, #1137; lwaldron, 2023-03, #26; cmirzayi, 2023-10, #112).
- **Test mappings:**
  - **Cladogram → LEfSe** (TheTosin, 2026-04, #1190).
  - **Kruskal-Wallis + Dunn's** when both were used (cmirzayi, 2023-10, #84: missing Dunn's cost a point).
  - **ANOVA + Post-Hoc Pairwise**: post-hoc pairwise is never a standalone test, and MHT is Yes. This was confirmed by cmirzayi (TheTosin, 2025-10, #808).
  - **DESeq2 Wald test → DESeq2.** If unavailable, negative binomial regression is the model (cmirzayi, 2025-01, #361).
  - "Negative binomial model" → Negative Binomial Regression (TheTosin, 2026-05, #1315).
    - Skill note, not yet mentor-reviewed (40377699): an NBZIMM negative-binomial mixed model (`mms(..., random = ~ 1 | subject, method = "nb")`) → Negative Binomial Regression (4 NBMM precedents in the export), data transformation "raw counts" (count model with an offset); the `fixed` covariates other than the exposure (sex, BMI, age, asthma) go in confounders.
  - ANCOVA isn't in the dropdown: request it, otherwise use ANOVA (DocTeedee, 2026-04, #1154).
  - Other real cases: Songbird (TheTosin, 2025-07, #415), METASTATS (#826), zero-inflated beta regression (#887), random forest with centered log-ratio (TheTosin, 2026-01, #1002), permutation test (annemarie-sharp, 2025-12, #722).
  - **PLS-DA / VIP selection:** "PLS-DA (Partial least square discriminant analysis)". Take direction from the paper's group-mean heat strip or loadings. There are no p-values, so use threshold 0.05 (22 of 27 PLS-DA experiments in the export) and MHT No. Keep it as its own experiment if the paper also ran a test on the same contrast with different taxa (#960).
  - **Random forest:** "Random Forest Analysis" (annemarie-sharp, 2025-10, #898). Take direction from the paper's mean-abundance plot of the top features, not from importance scores. Export defaults across 35 random-forest-only experiments: relative abundances (29), threshold 0.05 (32), MHT No (21). Use centered log-ratio only when the paper says so (TheTosin, 2026-01, #1002).
    - **Meta-Signer** (ensemble of four machine-learning models ranking taxa; no dropdown entry): entered as "Random Forest Analysis" by analogy with #898, with the top-N set as the signature and directions from the paper's mean-abundance statement; taxa without a stated or readable direction are left out (skill note, PMID 35032499; open, ask on Zulip).
    - **Random forest selection followed by a test on the selected features** (e.g. varSelRF picks 8 OTUs, then Wilcoxon + BH finds 4 significant): when the two lists differ, make two experiments (#960): a "Random Forest Analysis" experiment with the final selected set (direction from the abundance plot or the paper's direction column), and a test experiment with only the features that pass the paper's threshold. Curate the final selected set, not the full importance ranking table. Several OTUs that resolve to the same taxon in the same direction are entered once. If random forest is a stated aim of the paper, it isn't a "secondary analysis" under #910 (skill note, PMID 29069100; not yet mentor-reviewed).
  - If the test isn't stated but the figure implies it (e.g. Mann-Whitney), curate it and add a discussion note (TheTosin, 2026-04, #1190; 2025-11, #842).
  - SPSS "paired sample mean test" (a translation of the paired-samples t-test) → "T-Test", with a note; there is no separate paired option (skill note, PMID 33847206; not yet mentor-reviewed)
- **Data transformation defaults:**
  - DESeq2 and edgeR → **raw counts**. "DESeq2 uses a negative binomial model which requires counts" (SvetlanaUP, 2024-05, #395; cmirzayi, 2023-10, #90; TheTosin, 2025-10, #848).
  - MaAsLin2 → **log transformation** (TheTosin, 2026-01, #736; 2026-05, #610; annemarie-sharp, 2025-11, #854).
  - Mann-Whitney / t-test → **relative abundances** unless the paper says it log-transformed (Buraah, 2025-06, #786 and #677).
  - ANCOM-BC → log transformation (TheTosin, 2025-06, #726; unconfirmed).
  - An explicit "log2 transformed" or "log10 CFU" → log transformation, even for DESeq2 (Buraah, 2026-04, #1127; TheTosin, 2025-12, #903).
- **Significance threshold:**
  - **Never leave it blank.** "The default significance threshold… when not stated in the paper is 0.05… Without knowing the significance threshold, taxa cannot be curated" (TheTosin, 2026-04, #1106; 2026-01, #1019; 2025-12, #785).
  - Use the paper's own cutoff: "p < 0.001" → 0.001 (SvetlanaUP, 2024-10, #442); FDR < 0.1 → 0.1 (TheTosin, 2025-12, #608); "20% FDR" → 0.2 (TheTosin, 2026-04, #1156).
  - **Two-tier significance marks** (e.g. red star P < 0.05, pink star P < 0.1) where the authors call taxa "differentially enriched" at P < 0.1: use 0.1 and curate both tiers, by the paper's-own-cutoff rule above. Record the 0.05-only alternative (taxa per direction) in the verification report and discussion note (skill note, PMID 39198832; not yet mentor-reviewed)
  - Curate only taxa under it, using the FDR column when MHT applies (Buraah, 2025-06, #747; TheTosin, 2026-03, #1051 and #1160).
  - **Omnibus test fails correction, post-hoc passes:** if the multi-group test for a taxon is not significant after the paper's own correction (e.g. ANOVA FDR 0.066), don't curate its post-hoc pairwise "hits" either, even if the text presents them as findings. Explain this in a discussion note (skill note, PMID 34548031).
  - A typo like 0.5 instead of 0.05 cost a point (cmirzayi, 2023-03, #43).
- **MHT correction:**
  - always Yes or No: "We should always input yes or no for MHT" (TheTosin, 2026-01, #1019 and #938)
  - Yes for q-values, FDR, or "adjusted p-value" (Buraah, 2024-09, #328; TheTosin, 2025-02, #555; cmirzayi, 2023-11, #104)
  - No when nothing adjusted is mentioned (TheTosin, 2026-10, #2021 and 2025-12, #785)
  - DESeq2 corrects by default, LEfSe doesn't (TheTosin, 2025-03, #393)
  - ANCOM: "ANCOM with MHT correction" (KateRasheed, 2024-12, #474; a peer, but consistent with the code)
  - when you choose p-values over q-values, add a note (DocTeedee, 2025-12, #956; TheTosin, 2026-03, #1051)
  - Methods say a correction was applied, but the Results give only raw p for one analysis (e.g. phyla) while reporting q for others: curate that analysis as reported with **MHT No** and a discussion note (#990, #956), as its own experiment, separate from the corrected experiment on the same contrast (#960). Don't compute q yourself to drop it (skill note, PMID 29069100; not yet mentor-reviewed)
  - **No taxon survives the authors' FDR, but significant raw p-values are reported:** curate them with **MHT No**. "I suggest to curate significant results reported and record MHT correction: no" (SvetlanaUP, 2025-11-24, #990), overruling a "not curatable" call by TheTosin, who had relied on the authors' "not significant after correction" statement. Applied to 35092013 (only *Lactobacillus*, p = 0.01, FDR 0.33, still reported as higher in fluid in Results and Discussion).
  - **Tool defaults that decide MHT** (skill notes, not yet mentor-reviewed; say which default you relied on in a discussion note):
    - LEfSe in **microeco**: FDR-adjusts the Kruskal-Wallis p-values by default → Yes (40526755)
    - LEfSe where the **Methods explicitly state** a Benjamini-Hochberg FDR q-value cutoff for LEfSe → Yes (explicit statement overrides #393's default). `check_curation.py` still warns; that's expected (41199330)
    - LEfSe in **MicrobiomeAnalyst**: FDR by default (`pvalOpt="fdr"`), but 2,134 of 2,663 LEfSe experiments in BugSigDB are coded No → judgment call, lean No with a note (40951128)
    - A Methods sentence such as "The false discovery rate was calculated using the Benjamini and Hochberg method" that follows a list of analyses (LEfSe, Wilcoxon signed-rank, balance tree) but is not tied to LEfSe, when only LEfSe results are shown → No, with a note (skill note, 40377305)
    - **STAMP** prints "p-value (corrected)" even when no correction was chosen → No, unless the paper names a method (40170042)
    - **STAMP extended error bar plot** ('Means in groups', 'Difference between groups', 95% CI) with no test named for that panel: curate **Welch's T-Test** (STAMP's two-group default) under the implied-test rule (#1190, #842). Export 2026-10-30: 10 of 17 STAMP experiments use Welch's T-Test (30908851)
    - Kruskal-Wallis + **Dunn's in GraphPad Prism** reports multiplicity-adjusted p-values → Yes; 49 of 75 KW + Dunn's experiments in the export are Yes (39641435)
    - **MaAsLin2** run with q-values but the paper selects and reports only nominal P → No (41196050)
    - **Spearman heatmap whose Methods name FDR but whose caption marks "*P < 0.05"**, and whose colour bins show the stars fall at the nominal-P |rho| cutoff: curate as shown with **MHT No** and a discussion note, by analogy with #990, #956 and #1051 (32702151)
    - **MaAsLin1**: data transformation defaults to arcsine square-root (10 of 12 MaAsLin1 experiments in the export). Take the q cutoff from what the authors call significant, not the 0.25 default (27746239)
    - **MaAsLin3** (skill note, 42857727): transformation "log transformation" (TSS then log2 by default; both earlier MaAsLin3 studies, 42384640 and J.gutmic.2026.100018, use it); MHT Yes when q-values are used. Its default `max_significance` is **0.1**: when the Methods say "q < 0.05" but the heatmap stars mark q < 0.1 (*) and q < 0.01 (**) and the Results name single-star taxa as findings, use 0.1 and curate both tiers (#608, #1156); the 0.05 list can't be rebuilt because q between 0.05 and 0.1 isn't printed. MaAsLin3 heatmaps have separate **Prevalence** and **Abundance** blocks: curate only the Abundance block, since the prevalence model is presence/absence (Curation Policy; prevalence #452), and list the prevalence-only taxa in a note. One model per covariate set: the same contrast re-run with extra covariates (e.g. + SCFAs) is its own experiment when the taxa differ (#960). A "top 50" heatmap is a partial list: curate as shown with a note (#735)
    - **A generic BH/FDR sentence** in a Statistical analysis paragraph that names other tools (MaAsLin2, Pearson) but not LEfSe, with LEfSe results reported as "P < 0.05" only → **No** under #393, at 70. Contrast 41199330, where the Methods tie BH to LEfSe (40615853)
    - **Two tests reported jointly in one Results sentence** ("ANCOM and LEfSe approaches demonstrated that…", p < 0.05, no figure or table separating them): one experiment listing both tests, MHT **No**, LDA 2 (#872), relative abundances, following SvetlanaUP-reviewed 41922387 (ANCOM;LEfSe;… coded MHT No, LDA 2, relative abundances in all 5 experiments). #960 can't be applied because the per-test lists aren't reported (skill note, PMID 35329834)
- **LDA score:** LEfSe only; remove it for any other test (TheTosin, 2026-01, #952 and #938; Buraah, 2025-04, #658). Enter a whole number, e.g. "2", not "2.0" (annemarie-sharp, 2025-10, #908). The default when unstated is 2 (annemarie-sharp, 2025-10, #872).
  - If the stated cutoff (e.g. > 4) contradicts the plotted bars (which start at 2), curate the figure's cutoff and add a note (annemarie-sharp, 2026-10, #1986).
  - An LDA *heatmap* whose pale cells read below the stated cutoff on the figure's own colour bar (34607559: caption "> 3", cells ≈ 1.7–2.7): **apply #1986 at 70**. Enter 2 (#872) and curate every coloured cell (#1194); give the alternative (3, pale cells removed) in the discussion note. This was first left open at 50, but #1986 governs any stated-cutoff-vs-plot conflict, and the plot type doesn't change that. Confirm the colour-bar reading with two independent pixel passes first (re-check 2026-11-01; skill note, PMID 34607559, not yet mentor-reviewed).
- **Why thresholds and not values:** BugSigDB records yes/no membership plus the thresholds used, not p-values or effect sizes (lwaldron, 2020-03, B#6).

## 9. Matched on and confounders

- **Matched on:** only factors on which controls were explicitly matched, and only for the matched contrast.
  - Remove matching from contrasts between subgroups of cases (annemarie-sharp, 2026-04, #1146).
  - "No statistical difference" between groups isn't matching (TheTosin, 2025-03, #650).
  - "You cannot match on a condition" (cmirzayi, 2023-10, #84).
  - Matching that applies to only part of the controls is still recorded (TheTosin, 2025-08, #809; 2025-12, #617).
  - "sibling pair" is a valid matched-on value (annemarie-sharp, 2025-06, #774).
  - Lab experiments: "We do not record matched on or confounders controlled for a laboratory experiment" (cmirzayi, 2023-10, #90 and 2023-11, #114).
- **Confounders:** only variables the DA model was "adjusted for" or "controlled for" (SvetlanaUP, 2024-10, #442). Confounders used only in the alpha-diversity model don't count (cmirzayi, 2024-04, #179). "LEfSe does not control for confounders" (TheTosin, 2025-12, #939; cmirzayi, 2023-11, #126). "Age- and sex-matched" belongs in Matched on, not confounders, and vice versa (cmirzayi, 2025-09, #849; TheTosin, 2026-06, #1479).
  - LEfSe run "while correcting for community type" (a LEfSe subclass) → confounders blank: LEfSe doesn't adjust (#939, #126), and community type is derived from the microbiota (skill note, PMID 35565271; not yet mentor-reviewed).
  - Two-way ANOVA with a second factor (e.g. cancer × obesity): the curated main effect is adjusted for the other factor, so enter it as a confounder ("body mass index" for lean/obese BMI categories; #442). Don't curate the interaction term (#1072) (skill note, PMID 35565271; not yet mentor-reviewed).
- **Wording:**
  - write the variable as the paper does: "age quintile", the antibiotics wording, spelled-out subtype names (TheTosin, 2026-03, #1141; annemarie-sharp, 2026-03, #1143)
  - resolve yellow-flagged terms with true synonyms from the list ("gender" → "sex"; "alcohol consumption" → "alcohol consumption measurement") (annemarie-sharp, 2026-04, #1134; Buraah, 2025-10, #879)
  - never substitute a different concept ("sequencing batch" isn't "sequence read depth") (annemarie-sharp, 2026-04, #1064)
  - "sex design" isn't a confounder (Buraah, 2025-10, #879; TheTosin, 2026-01, #926)

## 10. Alpha diversity

- **Only indices tested between *this experiment's* groups**; leave the rest blank, not "unchanged" (cmirzayi, 2025-09, #849; 2023-11, #85). Leave all of it blank when the test was across all groups or for other contrasts (TheTosin, 2026-01, #870; Buraah, 2025-10, #879; 2024-09, #328; annemarie-sharp, 2025-10, #898).
- **Blank for:** one-vs-all and combination-vs-all analyses (TheTosin, 2026-01, #740 and #1019; Buraah, 2025-10, #882), correlation experiments (TheTosin, 2025-05, #741), and figures whose significance can't be read (annemarie-sharp, 2025-10, #929, with a note).
- **"Unchanged" when tested and not significant**, including "NS" on a figure (TheTosin, 2026-03, #1054 and #1151; 2025-02, #555). A significance bar with asterisks across both boxplots marks a significant difference (annemarie-sharp, 2026-01, #838).
- **Index mapping:**
  - Observed / observed species / observed features / ACE → Richness (cmirzayi, 2023-11, #81; annemarie-sharp, 2026-04, #1133; 2025-10, #798)
  - PD whole tree / Faith PD → Faith (TheTosin, 2025-09, #797; 2025-02, #580)
  - Evenness → Pielou (DocTeedee, 2025-12, #971)
  - Inverse Simpson ≠ Simpson (annemarie-sharp, 2026-04, #1064)
- **Direction is Group 1 relative to Group 0.** Reversed directions are a classic error (cmirzayi, 2023-10, #102).
- **Rank-specific results:** "for orders, families, genera, and species… not statistically significant" → unchanged for a species-level experiment (annemarie-sharp, 2026-03, #1143).
- **Results and Discussion give opposite alpha-diversity directions and no figure shows it** (35329834: Results "negative spermocultures presented statistically lower alpha diversity"; Discussion "in samples with positive cultures, alpha diversity was found to be lower"): leave blank with a note quoting both, at 50, by analogy with #929 (direction can't be read). #812/#1051 (follow the figure) can't apply without a figure. Skill note, not yet mentor-reviewed; the alternative is to follow the Results section.

## 11. Signatures: source, description, direction, members

- **Source:** "We want to be as specific as possible" (TheTosin, 2026-03, #1144).
  - Cite every figure and table referenced together for the same result (TheTosin, 2026-04, #1156: "Figure 2C, Table 5A, Supplemental Figure 3").
  - Include source-data files (TheTosin, 2026-04, #1141: "Figure 2F, Source Data. Fig 2; 2F").
  - Use "Additional file 1: Figure S1d and S1e" style labels (TheTosin, 2025-08, #820).
  - Disambiguate "Fig. 3D & **Supplementary Figure** S3" from Table S3 (Buraah, 2025-06, #766).
  - Exclude panels from another test (TheTosin, 2026-03, #1054) and figures without significance (TheTosin, 2025-12, #861 and #922).
  - Text sources use "Text; RESULTS: <heading>" with no page numbers (SvetlanaUP, 2026-02, #1000).
  - Prefer the adjusted analysis over crude supplementary results (lwaldron, 2023-03, #26).
  - When an unreadable figure has a readable supplementary version, use that (cmirzayi, 2024-04, #121).
- **Description:**
  - concise and specific, not pasted paragraphs (SvetlanaUP, 2024-11, #449)
  - name the clinical indicator for marker experiments (TheTosin, 2025-12, #918; 2025-05, #741)
  - say "taxa", not "species", when ranks are mixed (TheTosin, 2026-03, #1125)
  - abbreviations in full (TheTosin, 2025-12, #954: spell out LEfSe)
  - no surrounding quotation marks (TheTosin, 2026-04, #1132)
  - word Signature 1 and Signature 2 consistently (TheTosin, 2026-04, #1139)
  - build it from the figure caption, trimmed to one sentence (test, body site, rank, groups), not a paraphrase. A peer curator asked for this on 39198832 (2026-11); it agrees with DocTeedee's #1928 example and with #449. Keep the specific group pair when the caption covers more groups than the experiment does (skill note, not mentor-reviewed)
- **Direction and order:**
  - Signature 1 = increased in Group 1, Signature 2 = decreased: "for best practices, signature 1 should be the increase abundance" (TheTosin, 2025-12, #969); curate increased first (TheTosin, 2026-04, #1139; 2024-11, #439)
  - if all taxa are decreased, a single decreased signature is fine (annemarie-sharp, 2026-04, #1064)
  - "Signatures should not be identical for increase and decrease" (cmirzayi, 2023-10, #110); no taxon in both signatures (annemarie-sharp, 2025-12, #982)
  - the same name on two OTUs: if both go the same way, enter it once; if they go opposite ways, leave it out of both signatures and add a discussion note (skill note, PMID 33225888)
  - read direction from colour keys and legends (DocTeedee, 2026-01, #950; annemarie-sharp, 2025-06, #776), the middle line or arrow in plots (TheTosin, 2026-03, #1080; 2026-01, #952), and the sign of log2 fold change (annemarie-sharp, 2026-04, #1064; cmirzayi, 2023-11, #104)
  - when text and figure disagree, follow the figure and add a note (TheTosin, 2025-07, #812; 2026-03, #1051)
  - check each panel's own title against the caption: captions sometimes swap panel letters (e.g. PMID 41157277, Fig 1f/1g). Cite the panels as drawn and add a note
  - **[Skill note, open; 30908851]** A grouped bar chart whose legend colours contradict both the bar order used in the sibling panels and the text/abstract (Fig 5D: legend RE1 = white, but the text's RE1-enriched genera are tallest in the first, black bar). Curated per text + abstract + left-to-right order at 50, with a note giving both readings. No ruling covers it (#812, #950, #1124, #540 checked); ask on Zulip if graded
  - only curate a taxon in the direction the paper states (TheTosin, 2025-01, #540)
- **Members:**
  - **count them**: "There are 14 significant taxa in this figure but you curated 19. The number of taxa should match" (cmirzayi, 2025-10, #849)
  - curate only taxa with significance marks: asterisks or coloured bars (TheTosin, 2026-10, #1970; lwaldron, 2023-04, #34; Buraah, 2025-07, #726)
  - every bar in a LEfSe cladogram or histogram is significant (TheTosin, 2026-04, #1194)
  - each colour has its own p-value, so don't merge (TheTosin, 2026-01, #1019)
  - if the text claims more taxa than it lists, use the full figure or table (TheTosin, 2024-12, #524)
  - zoom into tiny figures; if one is truly unreadable, curate what the text gives and note the low-quality figure (TheTosin, 2025-12, #970; SvetlanaUP, 2025-04, #757)
- **Taxon names (see taxonomy.md for the full rules):**
  - Majorbio `g__norank_f__X` → family X, not "unclassified X" (#630, #759, #1054; §12 row "unclassified X")
  - SILVA genus "CAG-352" → *Clostridium* sp. CAG:352 (1262798), not text (reviewers KateRasheed, 2025, #535, #644, #671, #756; fiddyhamma, 2026-06, #1085, #1171; 39 signatures in the export). Not official-mentor rulings, but uncontested
  - genus-level unnamed Lachnospiraceae printed as "Lachnospiraceae sp." → genus placeholder, not Lachnospiraceae bacterium 1898203 (SvetlanaUP, 2026-07, #1155)

## 12. Disagreements and rules that changed over time

Follow the **current** practice in the right column, and add a discussion note when you choose.

| Topic | Older or minority view | Current practice |
|---|---|---|
| **Closely related genera** ("Peptostreptococcales_Tissierellales") | No slash: "Veillonellales Selenomonadales as is (Remove the slash)" (TheTosin, 2026-04, #1189) | **Slash**: "in the case of closely related taxa we report both with '/' in between" (SvetlanaUP, 2025-02, #573 and 2025-04, #653; corrected to the slash form 2026-02, #1000; Zulip "How to curate closely related taxa"). Escherichia/Shigella → "Escherichia/Shigella sp." (1940338) (TheTosin, 2026-01, #952) |
| **SILVA groups** (NK4A136 group, coprostanoligenes group) | Convert to species or uncultured bacterium (2024) | **As is**: "we have updated curation of group as opposed to the curation policy" (TheTosin, 2026-04, #1070); "It should stay as Lachnospiraceae NK4A136 group" (cmirzayi, 2025-10, #937) |
| **"unclassified X"** | Skip unclassified/uncultured and record the first meaningful rank for every printed "unclassified X" (SvetlanaUP, 2025-04, #630, applied broadly); the policy says exclude unclassified species of a known genus | **Keep distinct unclassified features as written, lowercase "u"** ("unclassified Muribaculaceae", "unclassified Leptotrichia") (TheTosin, 2026-04, #1189; cmirzayi, 2025-10, #937: "No joining… These are distinct unclassified genera… important to preserve"). Prefix strings like `g_unclassified_f_X` or `f_unclassified_p_Firmicutes` → the named taxon at its rank, without "unclassified" (TheTosin, 2025-07, #822; 2025-12, #798). "unclassified Family" with no name → remove (Buraah, 2025-06, #791). **Majorbio "norank" labels are a separate case, and #630 is still current for them:** `g__norank_f__X` → the family X (SvetlanaUP, 2025-04, #630, maintainer; annemarie-sharp, 2025-05, #759: "norank_f__Muribaculaceae, curate as 'Muribaculaceae'"; TheTosin, 2026-03, #1054: "g_norank_f_Bacillaceae… as 'Bacillaceae' once with ID: 186817"; live 37960154: norank_f__Erysipelotrichaceae → 128827). Minority: unclassified-family node (annemarie-sharp, 2025-10, #798; fiddyhamma, a peer reviewer, 2026-05, #1284). See taxonomy.md §9 |
| **GTDB suffixes** (Romboutsia_A, Phocaeicola_A_858004, Campylobacter_A) | Map to the parent NCBI genus (this skill's earlier rule) | **Curate exactly as written** (TheTosin, 2025-05, #741, after checking previous curations; annemarie-sharp, 2025-10, #860). NCBI has no such nodes, so they show red. Add a discussion note |
| **Numbered genera and OTUs** (Prevotella 9, Coprococcus 3, Fusobacterium nucleatum 1) | Always keep the number (annemarie-sharp, 2025-10, #908; 2026-03, #1153: Coprococcus sp. → Coprococcus3) | **Keep the number only if the same taxon appears more than once**, otherwise use the plain genus or species (SvetlanaUP via TheTosin, 2025-12, #617, #961, #857). Remove "msp" prefixes ("msp 1351 Clostridium celatum" → Clostridium celatum, TheTosin, 2026-01, #926) |
| **Class "Actinobacteria"** | Mentors have repeatedly curated **Acidimicrobiia (84992)** (TheTosin, 2026-02, #999; 2025-12, #954; annemarie-sharp, 2026-10, #1986; 2025-06, #757 and #407) or "Actinobacteriia" (Buraah, 2025-06, #751) | ⚠️ In NCBI, the class formerly named Actinobacteria is **Actinomycetes (1760)**; Acidimicrobiia is a *different* class. Use 1760 and add a note citing NCBI, or ask on Zulip. Don't copy 84992 blindly. Phylum Actinobacteria → Actinomycetota (201174) is uncontested |
| **Rank conflicts** | "Curate only the lowest rank" figure; skip phylum/family supplements (TheTosin, 2024-11, #472 and #439) | **Curate every rank reported as significant, combining ranks for the same contrast** (SvetlanaUP, 2026-03, #1139; 2025-03, #656) |
| **Antibiotics "30 days"** | Keep "30 days" because 1 month ≠ 30 days (Buraah, 2026-03, #1137) | "1 month" (annemarie-sharp, 2025-10, #893); 4 weeks → 1 month (TheTosin, 2025-02, #555) |
| **Correlation group names** | "Negative/Positive correlation with X" (common up to 2025; 328 experiments in total) | **"Low X" (Group 0) / "High X" (Group 1)** is now dominant: 209 vs 76 in 2026 curations; mentors use it (TheTosin, 2026-03, #1054 and #1151; DocTeedee, 2026-04, #1154; annemarie-sharp, 2025-10, #884). Both are accepted; sample sizes blank either way |
| **Annotated PDF deposit** | Curation Policy post-curation step | **Outreachy applicants don't annotate or deposit the PDF** (SvetlanaUP, 2025-10, #859; 2026-10, #2014) |
| **Preprints** | Policy: preprints allowed | **Curate the published, peer-reviewed version** (SvetlanaUP, 2026-02, #1077) |

## 13. Workflow, reviews and etiquette

- **One study at a time, said to this curator directly:** "Kindly be advised that studies are curated individually, one at a time" (SvetlanaUP, 2026-10-27, #1649, to raphaelekpei while #1241 was still open). When a request overlaps an open one, SvetlanaUP suggests collaborating with peers instead (2026-10-29, #1559; 2026-04, #1155). Before claiming a new paper, check how many of your issues are still `needs review`.
- **Before posting "please review":** run `scripts/check_live.py <PMID> curation.json`. In the 2026-10-30 audit, 3 of 11 submitted studies still had Study, Experiment or Signature pages set to Incomplete (35993728, 38752784, 41029586), which loses rubric item 1. One had a field missing on the site (38752784, Canada), and a requested deletion was still pending (42059388) (skill note).
- **Assignment first:** comment "I am up for this paper", wait for the `assigned` label, then start (SvetlanaUP, 2026-04, #1301 and #1307; 2026-03, #1104). Pick issues without the `assigned` or `needs review` labels (SvetlanaUP, 2025-09, #827). Make one assignment request at a time (SvetlanaUP, 2025-03, #655), and finish your previous curation first (SvetlanaUP, 2026-03, #980). Use the "BugSigDB Study curation by DOI" template, and don't add labels yourself (SvetlanaUP, 2025-03, #675).
- **Before review:** peer review on Zulip, then tell the issue it's ready for review (cmirzayi, 2025-09, #849). Select the "needs review" and "second contribution" labels when asked (SvetlanaUP, 2024-10, #479).
- **During review:** "after a review request, we do not make any changes. Only when we get the feedback" (SvetlanaUP, 2026-10, #1960; 2026-04, #1194; 2024-03, #184). Don't edit curations labelled "Reviewed" (SvetlanaUP, 2024-04, #154). Corrections after an official review are made **by the original curator** (SvetlanaUP, 2025-03, #636); "the mentor who gives the feedback is guiding corrections" (SvetlanaUP, 2026-03, #1080). Record your changes on the issue (SvetlanaUP, 2024-12, #545). A revised score is recorded too (SvetlanaUP, 2026-03, #1080).
- **Deletion requests:** always give full links in the form `https://bugsigdb.org/<PMID>/Experiment_N/Signature_M`, with a forward slash and not "#" (SvetlanaUP, many times 2025–2026). Experiment numbers can't be edited and gaps are fine (SvetlanaUP, 2026-03, #1051 and #1135). Deleted pages can be checked by typing the URL (SvetlanaUP, 2026-04, #1097).
- **Discussion pages:** "meant to store only key details for future use rather than full step-by-step curation workflows" (annemarie-sharp, 2026-10, #2011; exemplar https://bugsigdb.org/Talk:40676500). Use them for judgment calls: an inferred test, p-values versus q-values, excluded figures, author caveats, curated W-statistic thresholds (Buraah, 2026-04, #1128), discrepancies between text and figure.
- **Collaboration:** give a heads-up if you step away from an assigned task (SvetlanaUP, 2026-06, #1303). Don't be competitive when supporting others (SvetlanaUP, 2025-10, #925). Ask questions on Zulip rather than by DM.
- **AI use:** "Be aware that you should check the AI output" (SvetlanaUP, 2026-03, #1111).

## 14. Rulings from reviews after the 2026-10-22 harvest

Collected 2026-11-01 while testing the reviewer (`reviewer.md` §7). Each is quoted from the mentor's review comment; the section it belongs to is in brackets.

- [§3] An experiment whose taxa aren't significant is deleted: "Experiment 4 has no statistically significant signatures. I recommend deleting it… I meant to delete the entire experiment 4 because the adjusted p-values for all the taxa are higher than 0.05" (DocTeedee, 2026-10-26, #1971, PMID 30574320). **This conflicts with #990**, where SvetlanaUP (maintainer) said to curate raw-p hits with MHT No although the authors stated nothing survived correction. DocTeedee's stated reason is the adjusted p alone; the comments don't say the authors called the hits trends (an earlier version of this note claimed that, unverified, corrected 2026-11-01 on 35092013). Follow #990 (maintainer outranks), score MHT and item 3 at 70, add a discussion note quoting #990, and say this to the curator as a known reviewer risk.
- [§11] Members follow the corrected p-value: "There are more taxa you have not added. Please check again using the corrected p-value" (DocTeedee, 2026-10, #1971).
- [§11] Sources: no stray punctuation, e.g. "Table 1, and Table 2" ("Remove the comma from the source", DocTeedee, 2026-10, #1971).
- [§7] "The V3-V4 16s region is the same for all experiments" (DocTeedee, 2026-10, #1971): fill the region in every experiment from the same sequencing run.
- [§10] Read alpha diversity from the figure: "Shannon was reduced in group 1, according to Figure 2a" (DocTeedee, 2026-10, #1971). When the text says all indices were higher in Group 1, every tested index is increased (annemarie-sharp, 2026-10, #2050).
- [§4] Delivery-mode contrasts: "Cesarean Section as the condition is not bad, but 'Mode of delivery' fits better" (DocTeedee, 2026-10, #1928). "Mode of delivery" has no glossary page; the approved page uses **"Delivery measurement"** (live 34857640, checked 2026-11-01); "Delivery method" (#1135) is the other selectable term.
- [§5/§11] MaAsLin2 coefficient signs: "increased abundance in Cesarean delivery would have a negative coefficient, while decreased abundance would have a positive coefficient… So you would have 5 taxa as increased and 9 taxa as decreased" (DocTeedee, 2026-10, #1928). Read the reference level before assigning directions; the approved page kept Vaginal delivery as Group 0 and fixed the directions.
- [§11] Descriptions: "too long. You could say 'Microbiome Multivariable Association with Linear Models (MaAsLin2) of neonatal gut microbial genera identifying differentially abundant taxa with respect to delivery mode'" (DocTeedee, 2026-10, #1928).
- [§12, unclassified X] Distinct "_unclassified" features are curated with NCBI's "unclassified X" nodes: "curate unclassified Lachnospiraceae (Taxonomy ID: 186928), unclassified Muribaculaceae (Taxonomy ID: 2006847), unclassified Bacillota (Taxonomy ID: 84086), Unclassified Oscillospiraceae (Taxonomy ID: 473772)" (annemarie-sharp, 2026-10, #2050, PMID 41697396). Adds weight to the "keep distinct unclassified features" side of §12.
- [§6] Antibiotics: "should be left blank as it was not specified in the article" (annemarie-sharp, 2026-10, #2050); not "Not specified".
