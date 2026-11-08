# Verification pass and confidence scores

Curators often submit graded work (Outreachy, mentor review), so every drafted value gets a second, independent check against the source and a confidence score before the curator enters it. The point is to tell the curator **where to spend their checking time**. A high score means "I re-read the source and it says exactly this". A low score means "a reviewer could reasonably disagree, so look at it yourself or ask on Zulip".

## Contents
1. Confidence scale
2. How to run the verification pass
3. High-risk items to re-derive from scratch
4. Report format
5. Expected rubric score
6. Checking precedent in the BugSigDB export

## 1. Confidence scale

Score each value on this scale. Scores are calibrated judgments, not probabilities from a model, so don't use in-between numbers to look precise.

| Score | Label | Meaning | Curator action |
|---|---|---|---|
| **95** | Verified | The source states it explicitly (verbatim quote, printed number, a legend you've read) and it maps one-to-one onto a BugSigDB field or vocabulary term | Spot-check |
| **85** | Strong | Explicit evidence plus one documented BugSigDB rule (e.g. "Houston, Texas" → United States of America; "OTUs" → Richness; "within the last month" → 1 month) | Quick check |
| **70** | Probable | A reasonable interpretation that most reviewers would accept, but the paper is indirect or a convention is involved (e.g. which glossary term to use, case-control vs cross-sectional for a matched study) | Check the reasoning |
| **50** | Judgment call | Defensible options exist and reviewers could go either way (merge vs split experiments, MHT for tools without explicit correction, optional analyses) | Decide yourself or ask on Zulip **before entering** |
| **30** | Weak | Little support. Included only so it isn't forgotten | Don't enter without confirmation |

Rules:
- A value is never scored above **70** unless you **re-opened the source during this pass** (re-read the sentence, re-zoomed the figure, re-read the table row). Memory from the drafting pass doesn't count.
- A taxid scores 95 only if it was looked up on NCBI **in this session** and the name and rank match. If it's unverified, it scores at most 50 and is marked `ID: verify`.
- A taxa list scores 95 only if you **counted** the taxa in the source and the count matches. Write both numbers.
- Don't score a value 50 as a "judgment call" until you've searched `mentor-rulings.md` for it. If a ruling settles it, apply the ruling and score 70 with the issue numbers cited (see SKILL.md, "Needs your judgment"). If none does, record the search in `rulings_checked` for that field; `check_curation.py` flags low scores that lack it.
- If the text, a caption, and a table disagree, score the value no higher than 70 and say which source you followed and why.
- Blank fields get scores too. "Blank because not tested" can be 95 (e.g. alpha diversity in a correlation experiment) or 50 (e.g. "platform not stated", where it may be in the supplement).

## 2. How to run the verification pass

Do this after drafting and **before** presenting the final curation. Treat it as a fresh read, as if you were the reviewer.

1. **Quotes.** For every field, check that the evidence quote appears verbatim in the paper. With code execution, put the evidence in the curation JSON and run `scripts/verify_evidence.py curation.json paper.txt` (it accepts .txt, .xml, .html, or .pdf). Any quote it can't find must be corrected or the value re-scored. Evidence that comes from the authors' code or a tool's source is written as `"[code] …"`. Evidence that exists only inside a figure image (an asterisk, a bracketed n, a black vs gray p-value) is written as `"[figure] Fig 2E: brackets [50] [18] [17]"`. The script lists these as needing a visual check, so re-zoom each one. When the PDF reports MISSING for quotes that are plainly in the paper (line breaks and hyphenation in PDF text extraction), re-run against the PMC OA `.txt` (pmc-oa-opendata S3 `PMC<id>.<v>/PMC<id>.<v>.txt`) or the JATS XML; in 33847206 the PDF gave 57/75 and the .txt 75/75.
2. **Numbers.** Re-read each sample size, threshold, LDA value, and p-value at its source (figure label, table cell, methods sentence). Make sure the n is the **analytic** n for that specific analysis (subsets in regressions often differ from the cohort n).
3. **Figures.** Re-open every source figure. Zoom into significance markers (asterisks, black vs gray p-values, bold rows), group labels, color legends, and bracketed n. Re-derive the direction for each signature from the legend.
4. **Supplement.** Cross-check figure values against the supplementary tables. Matching coefficients reveal the real test and covariates.
5. **Vocabulary.** Check every dropdown value against `controlled-vocabularies.md`, and every body site and condition against the BugSigDB glossary (search bugsigdb.org if you can).
6. **Taxids.** Look up each one on NCBI and record the name and rank.
7. **Wording.** Re-read names and definitions against the paper. Don't add details the paper doesn't state (e.g. a recruitment site that only applies to one group).
   In the JSON, each study, experiment, or signature object can carry `"evidence": {field: quote or [quotes]}` and `"confidence": {field: score}` (see `assets/curation-template.json`).
8. **Run `scripts/check_curation.py`.** It warns about any value with a confidence below 70, and about missing confidence scores.

Report every correction the pass found ("Changed: …, because …"). Finding nothing is fine, but say what you checked.

## 3. High-risk items to re-derive from scratch

These carry the most rubric points. For each one, re-derive it independently instead of re-reading your draft:
- the experiment list (rebuild the map from the figure and table list, then compare)
- the taxa in each signature (count them in the source)
- the direction of each signature (from the legend or the coefficient sign, relative to Group 1)
- Group 0 vs Group 1 assignment and the matching sample sizes
- MHT per experiment (find the exact words in the methods)
- which alpha-diversity indices were tested for each contrast

## 4. Report format

```
## Verification report: <PMID>
Checked against: <full text / PDF pages / figures / supplementary files>, on <date>
Corrections made in this pass: <list, or "none">

| Exp | Field | Value | Confidence | Evidence (verbatim + location) | Note |
|---|---|---|---|---|---|

### Values below 70: check these yourself
1. ...

### Expected rubric score
<range out of 23, and which items are at risk>
```

Keep the "below 70" list short and actionable, so the curator knows exactly what to look at.

## 5. Expected rubric score

Map the low-confidence items onto the 23-point rubric (`rubric-and-review.md`). For example: "Item 3 (experiments) is at risk because of the merge vs split question for Exps 1–3. Item 11 (MHT) is at risk for the ANCOM experiment." Give a realistic range, not a promise. If all values are 85 or above, a range like 21–23 is reasonable. Each judgment call on a rubric item lowers the bottom of the range.

## 6. Checking precedent in the BugSigDB export (raises or lowers confidence)

For a convention call (16S region for long-read data, MHT for a given tool, sample sizes or alpha diversity in correlation experiments, which glossary term was used for a condition), check what BugSigDB already contains. The hourly export is public:

```
https://raw.githubusercontent.com/waldronlab/BugSigDBExports/devel/full_dump.csv
```

It has one row per signature. Skip the first `# BugSigDB …` line, then deduplicate by (Study, Experiment) to count experiments. Useful columns: Location of subjects, Body site, Condition, Statistical test, MHT correction, 16S variable region (e.g. `123456789` = V1–V9), Sequencing platform, Group 1 name, the sample sizes, and the alpha-diversity columns. Existing pages can also be read through the wiki API (`ai-assisted-curation.md` §7).

How to use it:
- **≥ 80% of comparable experiments agree:** the convention is established, so the value can score 85.
- **50–80%:** keep it at 70 and mention the split.
- **No precedent:** keep it at 70 or below and suggest asking on Zulip.

Quote the numbers in the report, e.g. "66 of 77 PacBio experiments are coded 1–9". Recount them yourself; never copy statistics from an earlier draft (one draft's figures here were wrong when rechecked).

Precedent checks also catch **invalid values**. A value that appears 0 times while its neighbor appears 1,670 times (e.g. "United States" vs "United States of America") is almost certainly not a dropdown option.

## Tips from real curations (2026-10)
- **Recompute the test from per-sample counts when text and figure disagree** (41398357, skill note). If the supplement has per-sample read counts, compute relative abundance (reads / sample total) and rerun the paper's own test (e.g. two-sided Mann-Whitney). When the group means reproduce the figure bars and the p-values reproduce the asterisks, the figure is that data: take the direction from it (medians for rank tests), and use raw-vs-adjusted p agreement to settle MHT. Example: the text said Peptostreptococcaceae_256921 was 'higher in UC' because one UC sample had more than 5,000 reads, but 6 of 11 UC samples were zero (median 0 vs 1.38%, p = 0.020) → decreased. When two columns could be the plotted feature (f__Lachnospiraceae;__;__ vs f__Lachnospiraceae;g__;s__), pick the one whose means and p match the figure. A top-N species table can't rebuild phylum or genus tests (aggregates won't match), so keep the text and figures for those ranks.
- **Supplement numbering and legacy .xls** (41398357). Springer 'Supplementary Material 1/2' may not match the text's 'Supplementary Table 1/2' numbering, so open every file. macOS `textutil` can't read BIFF .xls; install `xlrd` (and scipy) into the scratchpad with `pip --target` and run with `python3 -I`.

- **MDPI supplements as .pptx** (35565271). The Europe PMC `supplementaryFiles` zip can hold a nested zip with a PowerPoint file. Read the captions from `ppt/slides/slideN.xml` (`<a:t>` runs, via `zipfile`) and the figures from `ppt/media/`. The main-text figures come as `*-g00N.jpg` in the outer zip (about 730–800 px wide; crop and enlarge them with `sips -c H W --cropOffset Y X`).

- **PLOS figures and supplements** (30332459). Full-size figures: `https://journals.plos.org/plosone/article/figure/image?size=original&id=<DOI>.g00N` (a TIFF, roughly 1600–1800 px; convert it with `sips -s format png`). `size=large` returns a PNG up to 4000 px wide, which the Read tool can view directly (28178310). Supplements: `.../article/file?type=supplementary&id=<DOI>.s001`. A Word `.doc` supplement holds its figures as embedded PNGs. `textutil` drops them, so extract them by scanning the file for the PNG signature (`\x89PNG` … `IEND`). The `.s00N` file number doesn't always match the label: when S1 File is a PDF appendix, s002 is S1 Fig (32369505). Map files to labels with the supplement captions in the full-text XML. Without PIL, crop with `sips -c <h> <w> --cropOffset <y> <x>`.

- **Figures too small to read** (e.g. a cladogram legend with 180+ labels). PMC images are often only about 700 px wide. Springer/BMC journals publish full-size versions at `https://media.springernature.com/full/springer-static/image/art%3A<DOI with / encoded as %2F>/MediaObjects/<file>_HTML.png` (about 1600 px), which can be cropped and enlarged to read every label. If you can't get a legible image, ask the user for a screenshot rather than guessing.
- **A summary table vs the figure it summarises.** When a supplementary "summary" table puts taxa at the wrong rank (families listed as orders, plants listed as classes), curate from the complete figure legend and enter each taxon at its true NCBI rank. Note the table's errors (PMID 40797356).
- **NCBI renamed many higher taxa.** Autocomplete will show the new name for the paper's old one. Common cases:
  - Clostridiales → Eubacteriales 186802
  - Ruminococcaceae → Oscillospiraceae 216572
  - Bacillales → Caryophanales 1385
  - Planococcaceae → Caryophanaceae 186818
  - Rhizobiales → Hyphomicrobiales 356
  - Rhodobacteraceae → Paracoccaceae 31989
  - Xanthomonadaceae → Lysobacteraceae 32033
  - Leuconostocaceae → Lactobacillaceae 33958

  Record the paper's name as `paper_name`. Watch for homonyms: *Rhodococcus* 1827 is the bacterium, while 1661425 is an insect genus. More renames and homonyms are in `taxonomy.md` §9.
- **LDA cutoff stated two ways** (caption "> 3", Results "> 3.5"): measure the shortest bar against the axis ticks. Decode the PNG with zlib, since PIL isn't installed, then measure the colour runs that touch the zero line, in px per LDA unit from the tick labels. If every bar clears both cutoffs, enter the caption's criterion and say so in a note (40615853: minimum bars 3.6 / 3.1 / 3.6, so 3 in all three figures). The pixel count of bars per colour also confirms the label transcription.
- **Find the test the authors actually ran by recomputing p-values** from the printed means, SDs/SEs and n:
  - Welch's t reproduces the p-values while the Methods name only LEfSe or ANOVA (32504527)
  - exact two-sided Mann-Whitney p-values while the Methods say Welch's t (33891612)
  - every p an exact multiple of 1/(number of permutations) and Fisher-type p (0.0625, 0.125, 0.25) for sparse taxa → Metastats (39901379)
  - "F, DFn = 2, DFd = 21" in captions → GraphPad one-way ANOVA output, even when the Methods say Kruskal-Wallis (36082082)
  If the paper names **no** test, curate the inferred one with a discussion note (#1190, #842). If it names a test the numbers contradict, no ruling settles it yet: offer both, lean towards the stated test, and note the evidence.
- **Check that supplementary blocks carry the labels they claim.** In 34267209, a "Healthy vs PCOS-LB" block's "Healthy" column held PCOS-HB means. Weighting the subgroup means by n to rebuild the pooled mean in the main table exposed it. Derive directions from the true columns and add a note.
- **Springer/BMC image files can be numbered differently from the paper's figures** (40275186: `Fig2_HTML` = paper Fig 3). Map files to figures through the full-text XML, and cite the paper's labels. Wiley files in PMC can be fully scrambled (32702151: `g001` = graphical abstract, `g003` = Fig 1, `g005` = Fig 2, `g004` = Fig 3, `g002` = Fig 4). Supplement files too (35092013: `s004` = Table S5, `s008` = Table S4, `s005` = Table S3; `g001` = Fig 2). Read each file's title row, not its number.
- **Europe PMC `supplementaryFiles` zips and the BugSigDB export can arrive truncated** when curl times out (35092013: zip "End-of-central-directory signature not found"; export cut at 3,958 of 16,446 rows). Retry with `--max-time 300` or more and check `unzip -l` / the row count. Compare the file size with `curl -sI … | grep -i content-length` and finish a partial file with `curl -C -` rather than starting over (34607559, 2026-11-01: first pass stopped at 22.6 of 37.0 MB, 10,328 of 16,538 signatures, with no curl error). Don't switch user agents to fetch PMC `/bin/` files; that's treated as bot-check circumvention.
- **Find the analytic n from percentage denominators and per-sample supplements.** When the paper repeats "22 and 22" but a footnote says "1 control missing data", recompute the percentages (5 discordant pairs = 24% → 5/21) and check the per-sample metadata table for rows with no microbiome data. Fig 3 also showed that participant's bar as "Missing" (34537015).
- **When two supplementary tables list the same subjects (e.g. one per body site), compare each sample ID's group label across them.** In 40304477, WC33 is CIN in Table S1 (secretions) but NC in Table S2 (tissue), so the tissue n is 25/33 as printed or 24/34 if S1 is right. Parse the xlsx (sheet XML + sharedStrings) instead of eyeballing it. Curate the table as printed for that body site and add a note giving both sizes (skill note, not yet mentor-reviewed).
- **Correlation heatmaps with asterisks: scan them by pixel.** Find the heatmap block from the saturated-colour mask, divide it into the row × column grid, assign each dark-pixel component to a cell by its centroid, and read each cell's median colour. Then check the result against a visual read and the Results text (32702151: 49 starred cells across 17 traits; script in `curations/32702151/source/figs/fig2b_pixel_scan.py`). Counting components per cell doesn't tell "*" from "**", because asterisks fragment.
- **Are heatmap stars nominal P or FDR?** Compare starred cells with the colour bins. With n subjects, nominal P < 0.05 needs |rho| ≥ 1.96/√(n−1). If almost every cell in the bin just above that value is starred, the stars are nominal, even when the Methods mention FDR. BH over many tests would leave many unstarred cells in that bin (32702151; see mentor-rulings.md §8).
- **Mapping heatmap cells onto a colour bar** (34607559 Fig 3B). Sample the bar away from its tick marks; −3/0/+3 ticks are dark lines that pull samples towards grey, which made pale cells look like −3. Take the grid pitch from the outer borders and check that the last row lands on the last label (a 0.5 px pitch error shifted every row after row 10). Re-derive the lists by script and diff them against the JSON (`curations/34607559/src/figs/verify_figs.py`, colour-bar lookup in `lda_cells.py`).
- **Row-scaled (z-score) heatmaps with pairwise star rows** (39198832 Fig 3d: 18 genera × IS/SIF/MIF, one star row per pairwise test). Read each star's colour by pixel class as well as by eye, and the direction for a pair from the two cells' colour-bar z-scores (area-averaged). Each column's z-scores should sum to about 0. If the two cells have identical RGB, the direction can't be determined: leave the taxon out with a note (#1124, #820).
- **Springer `static-content.springer.com/esm/...` downloads can be silently truncated** (39198832: the S4 PNG had the right size header but Pillow said "image file is truncated", and the Read tool couldn't decode it). Open every downloaded image with Pillow before relying on it, and fall back to the Europe PMC `supplementaryFiles` zip copy.
- **NCBI E-utilities return HTTP 429** after a few rapid esearch calls. Verify known IDs in **one** batched `esummary.fcgi?db=taxonomy&id=a,b,c` call instead of one search per name (34607559).
- **The publisher PDF often embeds figures at higher resolution than PMC.** In 32702151 the Wiley PDF held Fig 2 at 1371 px against 709 px on PMC. When the curator supplies the PDF, pull the raw image with PyMuPDF (`doc.extract_image(xref)`) rather than rendering the page, and rescan. At the higher resolution, "*" and "**" separate by glyph width. Expect `verify_evidence.py` on a PDF to miss quotes broken by line-end hyphens or with Greek letters encoded as Latin ("α" → "a"); confirm those against the XML. MDPI PDFs (26287241) also swap ± → ˘, × → ˆ and ≥ → ě in the text layer, so pass the PDF and the XML text to `verify_evidence.py` together.
- **Read colours and asterisks by pixel when an image is small.** Sample the RGB of each bar or dot and compare it with the legend swatch, and measure bracket ends against bar centres (34934118, 40951128, 42075812). If a bracket still can't be assigned to one pair, leave that alpha-diversity value blank with a note.
- **Start with `scripts/fetch_sources.py <PMID> source --browser`.** It tries the PMC open-access bucket, Europe PMC, the PMC page, Unpaywall's open copies, the publisher and cited data repositories. Files behind a bot check (PMC author-manuscript supplements, most publisher sites) are opened in the user's own browser and collected from ~/Downloads. Anything left is listed in `source/NEEDED_FILES.md` with exact links; ask the user for those and don't guess their contents.
- **Supplements on Dryad or Zenodo usually can't be downloaded by script** (30534630, 40366801). Ask the user for the files, and score anything they hold at 50 or below until you have them.
- **PMC author manuscripts (NIHMS, not open access) put figures and supplements behind a bot check** (403 from both PMC and Europe PMC; 40377699). The full text still comes from NCBI efetch (`db=pmc`, XML). List the exact figures and supplementary files the curation needs and ask the user to save them into `source/`; the publisher PDF usually covers the main figures. Authors' code on GitHub (named in Data Availability) can be fetched and often settles the model (40377699: time as a scaled trend).
  - Zenodo's API (`https://zenodo.org/api/records/<id>`) does serve files. For a large zip, fetch only its last ~100 kB with `curl -r` and parse the central directory to list it, then range-fetch the one member you need (40304477: 224 MB appendix). Check that the sample IDs match the paper's before using any table: that appendix's species table was pipeline example data (CC/HS/LS/NC samples, not the study's WA/WC).
- **Open-access PMC files come fastest from the `pmc-oa-opendata` S3 bucket**: list `https://pmc-oa-opendata.s3.amazonaws.com/?list-type=2&prefix=PMC<id>`, then fetch `PMC<id>.1/<file>` (PDF, figures, supplements). The Europe PMC `supplementaryFiles` zip took more than 2 minutes for the same files (40304477). PMC **author manuscripts** (NIHMS) are in the bucket as `.txt`/`.xml`/`.json` only, with no figure files (27441565: PMC6941171), so their figures need the curator to open PMC in a browser.
- **The publisher PDF often embeds full-resolution figures** (40304477: 3039 px vs 760 px PMC JPGs). Extract them with PyMuPDF (`Pixmap(doc, xref)`). The PDF can print figures out of order (Fig 6 before Fig 5), so map each image to the caption on its page.
- **Bubble diagrams of group relative abundance** (OmicStudio "bubble" plots after Mann-Whitney; no fold change printed): read direction by measuring each bubble's diameter and area by pixel (fill holes, label components, compare per row). A missing bubble means the taxon is absent in that group. Score near-ties (≤1 px) at 70 or below (40304477).
- **Cross-check directions with any correlation against a 0/1 group variable.** Pearson r with a binary indicator has the sign of the group mean difference, so a heatmap of taxa vs "HPV status" (or case status) computed on the same two groups confirms every direction independently. In 40304477 it agreed for 55 of 56 taxa, and the exception was the 1-px near-tie. It only works when the variable separates exactly the experiment's two groups.
- **LEfSe plots that look unlabelled: render the publisher PDF page before concluding the labels are lost** (41174559). The Springer full-size PNGs had black label areas (pure 0,0,0) and colour-inverted legends (cyan/magenta/yellow for red/green/blue), but the figures embedded in the publisher PDF were intact. Rendering pages 6 and 8 at 4x (Swift PDFKit, or PyMuPDF where available) made every label legible. The labelled figure then showed that the Results text reverses several directions (Fig 1F, 2F) and puts a GF taxon in GM (Fig 2G); the figure was followed (#812, #1051), and Fig 1B/2B phylum boxplots confirmed it. Only if the PDF render is also unreadable, curate just the taxa the text names (TheTosin #970; SvetlanaUP #757): set `expected_taxa_count` to the named count, note "N named of M bars", score members at most 70, and skip a class when the text names more taxa than it has bars.
- **Text-only one-vs-all LEfSe tables** (taxa listed per group, no LDA values; 37696898 Table 3). Parse the cells from the full-text XML and recount them from a second conversion. Springer XML puts thin spaces (U+2009) inside cells like "< 6", so normalise whitespace before matching keys. Superscript marks in such tables can be annotations (37696898: `*`/`+` marked which specimen detected a taxon first), not significance; read the footnotes. Watch for one taxon listed twice in a cell, and for a species epithet split from its genus by a comma ("Bifidobacterium, Pseudocatenulatum").
- **The LEfSe bar plot tells you the class structure.** Bars on both sides of zero (negative LDA for one class) mean a two-class run, so the experiment is pairwise. All bars positive with three or more legend classes means a multi-class run, so it is one-vs-all (#231). Useful when the caption says "among the X and Y groups" but a third group exists (41174559).
- **A text claim about an unlabelled LEfSe bar can contradict another figure on the same contrast.** 41174559 said Proteobacteria was LEfSe-enriched in GDM neonates, while its own boxplot showed it **** lower. Since LEfSe ranks the same relative abundances, leave it out and add a note at 50 (open; no ruling yet).
- **The abstract, Results and Discussion can disagree with each other**, not only with the figures. Common forms:
  - a taxon called significant only in the abstract (30988706)
  - a Discussion list longer than the figure's (36082082, 42404072)
  - a text list marked partial with "among others" (37805634)
  - prose model numbers shifted by one relative to the table (39747960)
  Follow the data, and record each conflict in a discussion note.
- **Vector figures with no poppler/PyMuPDF installed (macOS).** If the PDF's figures are vector graphics (labels absent from extracted image XObjects, and figure text partly in content streams), render the page with PDFKit from a small Swift script (`PDFDocument(url:)`, `page.draw(with:.mediaBox, to:)` into an `NSBitmapImageRep` at 6×, with a crop rectangle). That makes 79 tiny LEfSe labels legible from a 709 px PMC image (30908851). Wiley's site returns 403 to scripts; use the PMC OA bucket PDF.
- **pypdf is installed for `/usr/local/bin/python3.13` (no Pillow, so no image extraction).** Use it for supplement text, and render figure pages with `curations/29643500/scripts/render.swift <pdf> <page0> <scale> <out.png>` (PDFKit). pypdf glues superscript footnote marks onto table cells: in 29643500 Table S4 every OTU ID gained a trailing 1/2/4 (one per PC), and Table S5 IDs differ from Table S3 for the same taxon. Don't match rows across tables by ID; parse rows with a regex and re-derive the signatures by script (29643500: 22 + 30 + 6 rows, all matched).
- **Long LEfSe bar plots in a supplementary PDF with no text layer** (40377305: Fig S8 has 226 bars, about 4 pt per bar). The embedded images were 1,100–3,800 px, so cropping the page with `scripts/rendercrop.swift` (`swiftc -O rendercrop.swift -o rendercrop; ./rendercrop file.pdf <pageIndex> 6 x0 y0 x1 y1 out.png`, top-left page points) made every label legible. Render overlapping strips (60 pt high, 58 pt step), number the bars top to bottom while reading, and record each entry's bar numbers in `paper_name`. Then assert in the build script that bars 1..N are each covered exactly once by an entry or a stated exclusion, and that N equals the paper's count (Table 2 there). Labels longer than the crop width are cut, so widen the crop or read the neighbouring same-LDA bar (S9A: `..._Clostridium_sensu_stricto_1[3]`). A strip loop that stops before the page bottom misses the last bars; check the axis is in the final strip (the first pass found 224 of 226).
- **Count samples from read totals to find which timepoint a comparison uses.** Total reads / mean reads per sample = number of sequenced samples (30908851: 1,617,140 / 57,755 = 28 = 10 RE pre + 10 RE post + 8 non-RE), which shows the controls had one sample each. Record it in the notes when the paper doesn't say which timepoint a between-group comparison used.
- **Two sources giving slightly different correlations: find the sample set by recomputing p from r** (t = r·√((n−2)/(1−r²))). In 38898981, Table S8 reproduced at n ≈ 1411 (all samples) and the Fig 3C source data at n ≈ 1391 (VALENCIA-retained), which explained one taxon starred only in the figure (p = 0.044 vs 0.052). The same recomputation shows whether reported p are nominal when the Methods name BH.
- **LEfSe panels whose axis doesn't reach the stated cutoff:** measure the bars against the panel's own tick pitch (`sips -s format bmp` and then read the BMP bytes when PIL is missing). 38898981 Fig S5B EDO/PCOS bars were ≈ 3.6 under a stated LDA > 4.
- **Check correlation heatmap colours against the text's r signs.** In 33804345 Fig 3, two starred cells (soybean) were green (positive) while the text printed negative r; all other cells matched. Pixel-sample each starred cell's G−R against the colour bar, and when the text and figure disagree, flag it at 50 and follow the figure (trust the data).
- **Tables where significance is shown only by bold type:** read the `<bold>` tags from the JATS XML (PMC/Europe PMC), since text extraction drops the formatting; ignore bolded legend/colour-scale cells (35595739 Table 2).
- **Reusable heatmap scanner:** `curations/41174559/scripts/heatmap_scan.py image.bmp x0 y0 x1 y1 nrows ncols` finds the coloured block, splits the grid, and reports starred cells (dark-pixel count) with their median RGB. Convert PNGs with `sips -s format bmp` when PIL is missing, and map pale cells onto the panel's colour bar before calling a sign. Note: `sips -c H W --cropOffset` ignores the offset on some macOS versions, so view the whole figure scaled down (`sips -Z`) instead.

- **Stars on dark fills** (42857727): an absolute darkness cutoff (max channel < 70–90) misses black asterisks on dark-red cells (Dielma fastidiosa * was missed). `curations/42857727/scripts/hm.py file.bmp nrows ncols_per_block` counts pixels darker than 0.45 × the cell's own median, finds the Prevalence/Abundance (or any gap-separated) blocks itself, and prints `block row col dark sign rgb`. Fig 2A/2B at 12x render: empty 0, * 21–37, ** 44–72; a 1425 px raster supplement: * 15–20, ** 30–39. `scripts/crop.py` crops a BMP without PIL. Generate signatures straight from the scan files in a build script (`curations/42857727/scripts/build.py`) and cross-check every taxon the Results name.
- **Excel supplements with no openpyxl/pandas installed** (40859402). An .xlsx file is a zip archive, so read it with `zipfile` and `xml.etree`. Load `xl/sharedStrings.xml`, map sheets through `xl/workbook.xml` and `xl/_rels/workbook.xml.rels`, and turn the cell refs into columns; write one TSV per sheet. Script: `curations/40859402/scripts/xlsx2tsv.py <file.xlsx> <outdir>` (run it with `python3 -I`). Then filter the FDR column with `awk` and re-derive every signature by script against the JSON.
- **Re-checking an older draft: diff its calls against the rules added since its date** (26287241, re-checked 2026-10-31). A draft from 2026-10-25 still had antibiotics "During pregnancy", although the 2026-10-30 note (mentor-rulings §6) says "9 months". It also had a placeholder taxon at 50 that the 2026-10-31 #630 settlement had since raised to 70, and an MHT citation (#826) that turned out to be a test-mapping example rather than an MHT ruling. Rebuild the experiment map from the paper before opening the draft. Then grep `lessons-ledger.md` and the reference files for every rule dated after the draft, and re-verify each cited issue number against the line it is cited for. Skill note.
- **Majorbio extended-error-bar plots with no legend (95% CI panel + "Pvalue" column): identify the test from the p-values** (37178109). With small n, a two-sided Wilcoxon rank-sum (normal approximation with continuity correction, R `wilcox.test` default with ties) gives fixed values: 5 vs 5 → 0.01219 (U = 0, complete separation), 0.02157 (U = 1), 0.03671 (U = 2); tie-adjusted rows land nearby (0.01116–0.01193, 0.007495 with many zeros). Exact Mann-Whitney would give 0.0079/0.0159/0.0317, and Welch's t gives arbitrary values. The match also proves the p-values are uncorrected (MHT No). The dot colour in the CI panel is the group with the higher mean; check it against the bars on every row. Apply the same test to the paper's other plots of that type (human cohort, same pipeline) at 85. Skill note.
- **Elsevier supplements and figures without the PDF** (37178109): `fetch_sources.py` now resolves the PII through Crossref and downloads `ars.els-cdn.com/content/image/1-s2.0-<PII>-mmcN.<ext>`, `-figsN_lrg.jpg` (supplementary figures, about 2500 px) and `-grN_lrg.jpg`, which serve plain requests even when the journal site returns 403. Supplementary-figure legends are usually not in these files, so the article PDF is still needed for captions and Methods.
- **Random-forest directions from a stepped-palette heatmap** (31971855 Fig 2d). Render the vector PDF page with rendercrop at 4x, convert with `sips -s format bmp`, and average each cell (inset 4–8 px) for the two columns being compared; `curations/31971855/scripts/hm2d.py` does this without PIL. The palette is discrete, so even a gap of ~17 in summed RGB is a different colour step. Confirm every call against the per-group median bars if the paper also plots them (all 28 agreed there).
- **Find the analysis unit from the ANOVA degrees of freedom** (31971855): F1,60 and F1,92 = 64 and 96 observations, i.e. repeated samples (animals × timepoints), not the 32 animals. Record this in the sample-size note when you enter animal n.
- **Check every source in a signature actually shows that signature's taxa** (31971855 senior review): Exp 3 Sig 1 listed 'Figure 2e, Supplementary Figure 2c' although only Sig 2's Odoribacter came from S2c. Cite per signature, not per experiment.
