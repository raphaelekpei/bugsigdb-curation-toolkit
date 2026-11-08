# What the BugSigDB community learned about AI-assisted curation

These lessons come from waldronlab/BugSigDBcuration issue **#1274**, "BugSigDB curation supported by claude.ai" (April–May 2026). That's where the Outreachy AI Curation Team (16 contributors plus mentors) published their two-step prompt and their findings. Other material comes from about 20 individual "AI-assisted curation report" comments posted on curation issues in April 2026, which compared Claude, Gemini, ChatGPT, Grok, Perplexity, DeepSeek, and SciSpace against manual curations. The related Zulip threads (#bsdb-questions "When do you use an AI tool in your curation?" and "Claude.ai curation") weren't publicly readable.

What maintainers say about AI use: it's welcome, and Claude is the preferred tool. The one fixed rule is **"carefully review and verify the AI-generated results, as they may contain inaccuracies."** The verification pass in `verification.md` exists to meet that rule.

## Contents
1. Failure modes the community observed, and the countermeasure for each
2. Staged mode (for complex papers)
3. "Known facts" from the curator
4. Reading direction from effect sizes
5. What community prompts got wrong (don't copy these)
6. The reference example study (30641975), with caveats
7. Wiki field names

## 1. Failure modes and countermeasures

These are the AI Curation Team's "Limitations and challenges" slides plus the individual reports, with how this skill handles each one.

| Failure mode (as reported) | What it looked like | Countermeasure in this skill |
|---|---|---|
| **Missed experiments** | One experiment curated where there were several; strata, subgroups or supplementary contrasts dropped | Experiment map first (SKILL Step 3). Rebuild it independently in the verification pass. |
| **Incomplete taxa lists** | "It did not include a few taxa"; "the statistically significant taxa tables/figures were missing" | Count the taxa in the source and state "N in source / N curated". Read the supplements. Ask for figure images if the figures can't be read (§2). |
| **Extra taxa** | "It reported some taxa that should not be curated": non-significant taxa, network or correlation members, functional features | Curate only taxa with a significance marker or a value below the threshold. Network, co-occurrence and functional results are out of scope. |
| **Sorting errors** (direction) | Increased and decreased swapped; Signature 2 missing | Derive direction from Group 1's point of view using §4. Re-derive it in the verification pass. |
| **Text bias** | Using the Results prose instead of the figures and tables. Text often names only a subset, or overstates ("ANCOM identified…" when only one taxon is starred) | "Trust the data over the text" (SKILL Step 1). Every signature comes from a figure, table or supplement. |
| **Incorrect IDs** | Fabricated or outdated NCBI taxids (e.g. *Agathobacter rectale* vs the old *Eubacterium rectale* ID) | Never produce an ID from memory. Look it up live, or mark it `ID: verify`. |
| **Misclassification** | Wrong study design, condition, or group assignment | Decision rules in `field-guide.md` §3 and §5. Confidence scores flag the calls that are open to argument. |
| **Rule bypassing** | The model "knows" a rule but ignores it (e.g. lists beta diversity, enters "Not reported") | `check_curation.py` enforces the format rules mechanically. Rules live in references, not only in a prompt. |
| **Study design flaws** | Copying the paper's self-description ("cross-sectional") instead of applying BugSigDB definitions | Apply the field-guide §3 definitions and quote the recruitment sentence. |
| **Complexity scaling** | Fine for one experiment, falls apart at 10+ ("with this prompt there would be a lot more errors if it were to curate a complex study") | Staged mode (§2). |
| **Query instability / overload** | Asking everything at once gave about 50% accuracy; splitting into steps raised it to 85–90% | Staged mode, and curating one experiment at a time for large papers. |
| **Data transformation missed or wrong** | Missed even when stated; the test name entered as the transformation ("edgeR") | Field-guide §7: the transformation is the data form (raw counts, relative abundances, CLR), never the test. |
| **Invented confounders** | "Added diet to confounders" with no supporting model; decontam or negative controls listed as confounders | Confounders only come from a stated regression model or from stratification. Quality-control steps are never confounders. |
| **Thin group definitions** | Definitions "plain" with no diagnostic criteria | Group 1 definition = the paper's criteria for Group 1, in full sentences. |
| **Free-tier limits** | Truncated outputs on long papers | Staged mode keeps each response small. |

What worked best in the community's tests:
- A two-step split (metadata and experiments first, then taxa), with the taxa step run separately.
- **Pasting or uploading the specific figure or table** for the taxa step.
- Asking the model to **say "I am not sure"** instead of guessing (about 90% accuracy reported).
- Pausing for review after each experiment (one contributor reported 99.7%).

## 2. Staged mode (for complex papers)

Use staged mode when the paper has **more than 4 candidate experiments, more than about 40 significant taxa, multiple body sites or timepoints, or multi-panel figures you can't read clearly**. Also use it whenever the user asks for it.

1. **Stage 1: screening, study fields, experiment map.** Present them and **stop**. Ask the curator to confirm or edit the map, and to supply any figure or table images you couldn't read well (crop or screenshot is fine). Don't extract taxa yet.
2. **Stage 2: one experiment at a time.** Give the fields and signatures for that experiment (with confidence scores), then stop and let the curator check before you move to the next one. If a figure is illegible (small fonts, dense heatmaps, colors you can't tell apart), **ask for a zoomed image rather than guessing.**
3. **Stage 3: verification pass** over the whole curation (`verification.md`), then the final deliverable.

For simple papers (1–3 experiments, legible figures), one pass is fine. Still show the experiment map first.

## 3. "Known facts" from the curator

Invite the curator to give any facts they've already checked by hand. This idea comes from a community member's revised prompt. Treat these facts as constraints, and **never silently disagree** with them:

```
Known facts (optional):
- Expected total significant taxa: 13 (9 increased in Group 1, 4 decreased)
- Sources to prioritize: Figure 2, Supplementary Figures S9–S10
- Exclude: Alistipes, Bilophila (from network analysis)
- Other: genus level only; FDR q < 0.05
```

If your count differs from an expected count, say so explicitly, list every source you checked, and show both lists. Don't quietly force your result to match theirs.

## 4. Reading direction from effect sizes

Direction is always **relative to Group 1**. Signature 1 means higher in Group 1, and Signature 2 means lower in Group 1. Check which group the paper used as its reference before reading signs.

| Statistic | Increased in Group 1 when… | Watch out for |
|---|---|---|
| log2 fold change (DESeq2, edgeR, ANCOM-BC, LinDA) | > 0 **with Group 0 as the reference level** | Some papers set the case group as the reference, which flips the sign |
| LEfSe LDA bar / cladogram | The bar or node is colored for Group 1 | The sign of LDA only encodes which class; map colors through the legend |
| Regression coefficient (taxon ~ group) | Coefficient on the Group 1 indicator > 0 | Logistic models predicting case status: a positive coefficient for the taxon means higher in cases |
| Correlation (Spearman/Pearson) with a variable | r > 0 → Group 1 ("Positive correlation with X") | Use the correlation experiment naming in `field-guide.md` §4 |
| Cliff's delta, effect size d | Positive in the paper's stated direction | Read the methods for which group is "first" |
| "Enriched in X / depleted in Y" text | Map X and Y to Group 1 or Group 0 | Text can name only a subset, so use it to confirm, not as the source |
| Heatmap with significance stars | Color scale direction plus legend | Spearman heatmaps are **curatable** as correlation experiments. Co-occurrence networks are not. |

## 5. What community prompts got wrong (don't copy these)

Some prompts that circulated contain instructions that conflict with the policy or with mentor practice:
- **"Do NOT include correlation analyses"** (in one Gemini prompt). Mentors do curate correlations with a variable as "Low X / High X" (current) or "Negative/Positive correlation with X" (older) experiments, and the AI team listed recognizing Spearman heatmaps as an improvement. Only co-occurrence or network analyses are excluded.
- **"Write 'Not reported' if not stated."** Never type "Not reported", "NA", or "unknown" into a BugSigDB field. Leave it **blank** (MHT is the exception: "No" when there's no evidence of correction).
- **"Do NOT split experiments based on labels unless separate statistical tests were performed."** That's wrong. Separate contrasts, body sites, timepoints and strata are always separate experiments.
- **Sequencing type "16S rRNA amplicon sequencing", platform "Illumina MiSeq".** These must be the dropdown values ("16S", "Illumina").
- **Body site via ENVO.** Body sites use **UBERON** through the BugSigDB glossary.
- **Mixing body sites in one experiment** ("Vagina, Follicular fluid, Penis, Semen"). Use one body site per experiment.

## 6. The reference example study: bugsigdb.org/30641975

The community prompts point Claude at this study as "an example curated study". It's a useful format reference: one experiment, adjusted edgeR on income-based socioeconomic status, two signatures. It's **not a perfect model**, though:
- Group 1 name is lowercase ("lower SES…")
- the source has a typo ("Tabel 2")
- the description is a pasted figure caption, where mentors now prefer a short plain sentence with abbreviations expanded

Use it to see structure, and use `field-guide.md` for the rules.

## 7. Wiki field names (what the forms store)

These are useful when reading existing curations through the API or when a curator pastes wikitext.

- `{{Study}}`: study design, Mode, PMID, DOI, URI, State
- `{{Experiment}}`: Location of subjects, Host species, Body site, Condition, Group 0 name, Group 1 name, Group 1 definition, Group 0 sample size, Group 1 sample size, Antibiotics exclusion, Sequencing type, 16S variable region (lower bound), 16S variable region (upper bound), Sequencing platform, Data transformation, Statistical test, Significance threshold, MHT correction, LDA Score above, Matched on, Confounders controlled for, Pielou, Shannon, Chao1, Simpson, Inverse Simpson, Richness, Faith, State
- `{{Signature}}`: Source, Description, Abundance in Group 1, NCBI (comma-separated taxids), State

Existing curations can be read with `https://bugsigdb.org/w/api.php?action=parse&page=<PMID>/Experiment_1&prop=wikitext&format=json`. This is handy for checking how similar studies coded a condition or test.
