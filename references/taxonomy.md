# Taxa and NCBI taxonomy in BugSigDB

BugSigDB stores **NCBI Taxonomy IDs** and displays the current NCBI name. A taxon entered as plain text that never matched an NCBI ID is just text: it isn't linked to the taxonomy and doesn't count in cross-study analyses. Getting IDs right is worth 2 rubric points, and getting the member list right is worth another 2.

Tags: **[Policy]** = Curation Policy, **[Reviewer]** = mentor and maintainer conventions from 2025–2026 reviews.

## Contents
1. How entry works
2. Lookup procedure
3. Rank rules
4. Name-form rules (unclassified, sp., uncultured, bacterium, groups, OTU/ASV/SGB, HOT)
5. Renamed taxa, synonyms, brackets
6. Closely related taxa (slash names)
7. Non-microbial and junk entries
8. Worked examples from recent reviews
9. Crosswalk from skill curations (unreviewed)

## 1. How entry works  [Policy]

- Autocomplete only knows names **already in BugSigDB**. If autocomplete doesn't find the name, look it up in the NCBI Taxonomy Browser (https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi) and enter the **integer taxid**.
- A useful trick: type genus and higher names **in lowercase**. If autocomplete turns it into the capitalized form, it matched. If it stays lowercase, it didn't match and would be stored as plain text.
- **[Peer review]** The most common live-site error is a taxon **name** stored in the NCBI field (e.g. "Dialister" instead of `39948`). It happens when the name is typed and saved before autocomplete resolves it. **Paste numeric taxids** (comma-separated), then reopen the saved page and confirm each one shows as a linked name. `scripts/check_live.py` flags any non-numeric NCBI entry.
- Red-flagged taxa on a saved signature page have no NCBI match. **[Reviewer]** Try to resolve every red flag. If NCBI really doesn't have it, keep it exactly as written in the paper, with the capitalization the paper uses (e.g. "Ruminococcaceae G2", not "g2").

## 2. Lookup procedure (for Claude)

1. Normalize what the paper prints: expand abbreviated genera ("F. nucleatum" → "Fusobacterium nucleatum"), replace underscores with spaces, and remove rank prefixes (`g__`, `s__`, `f_`).
2. Search NCBI Taxonomy for the exact name. If you have web access, fetch `https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?name=<name>` or use the NCBI E-utilities (`esearch.fcgi?db=taxonomy&term=<name>`). Record the **taxid, the NCBI scientific name, and the rank**.
3. Check that the NCBI **rank matches the paper's rank** (see §3). This is where most errors come from.
4. If you can't verify an ID, **don't produce one from memory.** Output the name as written and mark `ID: verify`. Common IDs you're confident about are still worth a quick check, because NCBI does reorganize.

## 3. Rank rules

- **[Policy]** Curate taxa at **all** ranks reported as differentially abundant (phylum through strain). A signature can mix ranks when the paper presents them together for the same contrast.
- **[Policy]** Enter each taxon at the **lowest rank the paper gives for it**. For a genus-level result, enter the genus; for a species, the species.
- **[Reviewer]** Don't add parent ranks that only appear as part of a lineage string. For `k__Archaea;p__Euryarchaeota;c__Methanobacteria;o__Methanobacteriales;f__Methanobacteriaceae;g__Methanobrevibacter`, curate only *Methanobrevibacter*.
- **[Policy]** Differential abundance of a species doesn't imply it for the genus. Never "round up" a species result to the genus.
- **[Reviewer]** If the paper reports at species level (e.g. in a supplementary table), curate the species even when the main figure shows only genera.
- **[Reviewer]** Watch for NCBI names whose rank differs from the paper's. "Lachnospiraceae bacterium" (taxid 1898203) is a **species**-rank node. If the paper reports at **genus** level an unnamed Lachnospiraceae genus, it isn't that node. Record the genus-level placeholder as the paper gives it. **[Mentor]** SvetlanaUP, 2026-07, #1155: the paper reported at genus level, so "Lachnospiraceae sp. should be recorded as the genus lacking species level", not as Lachnospiraceae bacterium 1898203.

## 4. Name-form rules

| Paper says | Do | Source |
|---|---|---|
| Unclassified species with genus given (e.g. "unclassified *Prevotella*", "*Prevotella* unclassified") | **Exclude it.** Don't curate it as the genus. The same applies to an unclassified genus within a family, and so on. | Policy |
| "Unknown *Subdoligranulum*" / unknown species of a known genus | Use the NCBI "*Genus* sp." node if it exists (e.g. *Subdoligranulum* sp., 2053618) | Policy |
| A species known only to family or order level | Search "<Family> bacterium" or "<Order> bacterium" in NCBI (e.g. Clostridiales bacterium, 1898207), **only if the paper reports it at species level** | Policy |
| Unresolvable odd label (e.g. *Prevotella* KQ959344_s) | Enter it exactly as reported (it may be a strain) | Policy |
| "*Genus* OTU 29" / "*Genus* ASV 12" (named) | Drop the tag and curate the genus: *Coprococcus* OTU 29 → *Coprococcus* | Policy |
| "*Lactobacillus* OTU23, with 100% similarity to *Lactobacillus iners*" (the paper assigns the OTU to a species) | **Open.** The Policy row above was written for OTUs named only to genus. Leaned to the species the paper names (*L. iners* 147802), with the genus as the alternative; scored 50. No ruling or export precedent | 35565271 (skill note) |
| "ASV 233" (no name) | Curate it as reported | Policy |
| "*Bacteroides uniformis* SGB1234" | Drop the SGB tag when the species is clearly identified: *Bacteroides uniformis* | Policy |
| Several SGBs of one species (e.g. *P. copri* SGB1234 and *P. copri* SGB5678), or an SGB above species rank (Clostridia SGB9012) | **Keep** the SGB tags | Policy |
| SILVA-style groups: "Lachnospiraceae NK4A136 group", "Eubacterium coprostanoligenes group", "Rikenellaceae RC9 gut group", "Christensenellaceae R-7 group", "Prevotellaceae NK3B31 group" | **Keep the group name as is.** Use the NCBI node if it exists, otherwise plain text. Don't convert it to a species ("Lachnospiraceae bacterium NK4A136") or to "uncultured bacterium". **[Reviewer]** This is an update to older advice. | Reviewer |
| Underscores / hyphens in labels: "Ruminococcaceae_UCG_002", "UCG-002", "Selenomonas_sp._HOT_15" | Use spaces: "Ruminococcaceae UCG 002", "Selenomonas sp. HOT 15". Keep internal codes exact ("NK3B31", not "NK 3B31") | Reviewer |
| "Clostridium sensu stricto 1" | Curate as *Clostridium* | Reviewer |
| "Prevotella 1", "Coprococcus 3", "Ruminococcus 2" (numbered SILVA genera) | **Current practice (`mentor-rulings.md` §12):** keep the number only if the same genus appears more than once in the signature (e.g. *Prevotella* 2 and *Prevotella* 9 together); otherwise enter the plain genus (SvetlanaUP via TheTosin #617, #961, #857). The older rule "always keep the number" (annemarie-sharp #908, #1153) is superseded. Applied in 41174559 (Prevotella_9 alone → *Prevotella* 838) | mentor-rulings §12 |
| "uncultured bacterium" | Include it (77133) when the paper lists it as a significant taxon | Reviewer |
| "uncultured *Betaproteobacteriales*", "uncultured Mollicutes RF39", "uncultured Eggerthellaceae" | Keep the "uncultured <taxon>" form the paper uses. Don't drop "uncultured", and don't add "bacterium" if the paper doesn't | Reviewer |
| "metagenome" as a label for an unresolved feature | Use NCBI "metagenome" (256318) when that's what the paper reports | Reviewer |
| CAG bins: "Firmicutes bacterium CAG:56", "CAG:352" | Resolve to the NCBI node (e.g. CAG:352 → 1262798). This includes the SILVA genus label "CAG-352" / "g__CAG-352" / "CAG.352", even though 1262798 is a species-rank node: reviewers have consistently used 1262798 (KateRasheed #535, #644, #671, #756; fiddyhamma #1085, #1171; AleruDivine #354), and 39 BugSigDB signatures use it. Don't type "CAG-352" as text (40828589) | Reviewer |
| Strain-tagged species in the paper ("*Enterocloster bolteae* CAG:59", "*Bacteroides fragilis* CAG:47") where the reviewer wanted the species | Curate the species (*Enterocloster bolteae* 208479, *Bacteroides fragilis* 817), unless distinct strains are reported separately | Reviewer |
| Oral taxa "HOT 810" / "HMT 285" | HOT = human oral taxon. Search "<Genus> sp. oral taxon 810" in NCBI (e.g. *Atopobium* sp. oral taxon 810, 712158). If not found, keep it as reported ("*Porphyromonas* sp. HMT 285") | Reviewer |
| GTDB / Greengenes2 split-genus suffixes ("Peptoniphilus_A", "Romboutsia_A", "Phocaeicola_A_858004") | **Official mentor practice: curate exactly as written** (TheTosin, 2025-05, #741, after checking previous curations; annemarie-sharp, 2025-10, #860). NCBI has no such nodes, so the entry shows red/missing-ID; that is expected. Add a discussion note. Mapping to the parent genus (e.g. *Peptoniphilus* 162289) is the older fallback; use it only if a mentor asks. | mentor-rulings.md §12 |
| Greengenes 13_8 placeholder genera ("SMB53", "WAL_1855D", "rc4-4", "02d06", "1-68", "ph2") | Check the community crosswalk first (bugsigdb.org Category_talk:Pages_with_missing_NCBI_ID). It resolves WAL_1855D to *Sporobacterium* sp. WAL 1855D (507843). Otherwise type the name as text, as earlier curations did (e.g. "SMB53" in 30459320 and 31206804), and add a note | Crosswalk; export 2026-10-23 |
| Greengenes 13_8 families NCBI files under another name: "[Mogibacteriaceae]" (the paper may also say "Clostridium Family XIII Incertae Sedis"), "Ruminococcaceae" | Mogibacteriaceae has no NCBI node; use **Anaerovoracaceae (543314)**, whose NCBI synonyms include "Clostridiales Family XIII. Incertae Sedis" (133 BugSigDB signatures use it). Ruminococcaceae is an NCBI synonym of **Oscillospiraceae (216572)**; BugSigDB displays it as Oscillospiraceae. Add a note giving the paper's name | Skill note (PMID 29069100; NCBI efetch 2026-10-25) |
| Greengenes bracketed genera ("[Ruminococcus]", "[Eubacterium]", "[Prevotella]") | The brackets mark a genus that Greengenes placed outside its type family, so the NCBI genus of the same name is a different lineage. "[Ruminococcus] torques"-style species have their own NCBI IDs (33039); bracketed *genera* have none. Use the plain genus at low confidence with a note, or type the bracketed name as text; ask on Zulip if graded | Skill note (PMID 38384504) |
| Composite features ("non-*L. iners* *Lactobacillus*", "other Lactobacillus spp.") | Not a single taxon. Either curate the genus and explain in the description, or leave it out. Flag it for the curator either way. | Judgment |
| SILVA numbered genera written with underscores ("Prevotella_6", "Corynebacterium_1") | When the number is kept (see the numbered-genera row above: only if the genus repeats in the signature), use a space: "Prevotella 6", "Corynebacterium 1". Check whether autocomplete already has the entry | Reviewer |
| MSP / metagenomic species-pangenome numbering ("Ruminococcus bromii 2", "Faecalibacterium prausnitzii 6/9") | Resolve to the species taxid. When several numbered clusters of one species appear in one signature, keep the number in plain text so they stay distinct (same logic as the SGB rule) | Community output, #1274; confirm on Zulip |
| Genome assembly labels ("Alistipes putredinis DSM 17216, GCF_000154465.1") | The strain designation belongs to the assembly lineage, not the version, so .1/.2/.3 doesn't matter. Resolve to the strain node if NCBI has one, otherwise to the species | Mentor discussion, issue #1245 |
| Named strain in the paper that NCBI lists as a strain (e.g. "Corynebacterium sp. SN15") | Curate **as is**. Don't replace it with a named species it might belong to (e.g. *Corynebacterium provencense*) | Mentor, #2021 (2026-10-15) |
| Probe-based labels ("*Fusobacterium* Genus probe 4") | Keep as reported | Reviewer |
| "Incertae sedis" | Curate as "Bacteria incertae sedis" when that's the context | Reviewer |
| A species that NCBI lists only as a basionym or a subspecies (e.g. *Fusobacterium nucleatum* subsp. *animalis*, 76859) | Use the matching NCBI node at the rank the paper reports | Reviewer |

## 5. Renamed taxa, synonyms, and brackets

- **[Policy]** Search results may land on a synonym. That's fine: the ID covers both the current name and the synonym (e.g. *Bacteroides symbiosus* → [*Clostridium*] *symbiosum*).
- **[Policy]** Square brackets in NCBI names (e.g. [*Ruminococcus*] *torques*) mean the genus placement is pending. That's fine, so use the ID.
- **[Reviewer]** You may curate a basionym or a homotypic or heterotypic synonym **if it's at the same rank** as the paper's taxon.
- **[Reviewer]** Phylum names have changed in NCBI. Use the current node whatever name the paper uses: Firmicutes → **Bacillota**, Proteobacteria → **Pseudomonadota**, Bacteroidetes → **Bacteroidota**, Actinobacteria (phylum) → **Actinomycetota**, Fusobacteria → **Fusobacteriota** (32066), Verrucomicrobia → **Verrucomicrobiota**, Deferribacteres → **Deferribacterota** (200930). Watch the rank: "Actinobacteria" at **class** level is a different node from the phylum.
- **[Reviewer]** When the paper uses a name NCBI has reassigned (e.g. *Otoolea* → [*Clostridium*] *symbiosum* 1512, "Anaerobutyricum hallii" printed in the paper but the analysis label was "Eubacterium hallii group"), **curate the taxon as the paper's analysis labeled it**, resolving to the matching NCBI node. When in doubt, flag it.
- **[Reviewer]** *Raoultella* has been proposed for transfer back into *Klebsiella*. When this kind of change matters, add an explanatory note rather than silently changing it.

## 6. Closely related taxa (slash names)  [Reviewer, Zulip "How to curate closely related taxa"]

When taxonomies treat two genera or orders as one ambiguous unit, curate them with a **slash**, as BugSigDB has them:
- *Methylobacterium*/*Methylorubrum*
- Peptostreptococcales/Tissierellales
- Veillonellales/Selenomonadales
- *Escherichia*/*Shigella* (labels like "Escherichia-Shigella", "Escherichia_Shigella")

Check whether a slash entry already exists in BugSigDB autocomplete before entering it.

**Species-level slash labels** from pplacer/vaginal reference sets ("Anaerococcus prevotii/tetradius", "Peptoniphilus grossensis/harei", "Fusobacterium equinum/gonidiaformans"): no slash node exists, so enter **both species**, with a note. SvetlanaUP-reviewed 35928983 entered A. prevotii + A. tetradius in the same signature. Count bars and IDs separately ("9 bars = 11 IDs"). Skill note, PMID 33354707.

## 7. Non-microbial and junk entries  [Reviewer]

- Remove plant or chloroplast hits (e.g. Streptophyta, "unclassified Streptophyta"), mitochondria, and host reads.
- SILVA 16S labels that name a plant, animal or other non-microbe are the same junk class: *Pinus jeffreyi* (pine) and "*Vicia faba* fava bean" at s/g/f ranks (chloroplast), *Syphacia muris* (a rodent pinworm, NCBI division "nematodes"), and f__Mitochondria. Check the NCBI division before entering any odd species; remove them and say so in the signature notes (40377305; Syphacia removal was a curator decision, skill note).
- **Placeholder merges that would cross directions.** When an `uncultured_bacterium_<rank>_X` bar is entered at its named taxon X (#630), check that X is not already in the *other* signature of the same experiment. If it is (40377305 Fig S8: `s__uncultured_bacterium_g_Caulobacter` vaginal vs `g__Caulobacter` cesarean), leave the placeholder bar out and note it, rather than putting X in both signatures (#982). Skill note, not yet mentor-reviewed.
- Remove taxa not in the cited figure or table, and double-check near-miss spellings (e.g. "UBA1891" vs "UBA1819", "Ruminoococcaceae").
- A blank taxon on the saved page means an ID didn't resolve. Find which entry caused it.

## 8. Worked examples from recent reviews

- "Lachnospiraceae bacterium" in a species-level table → resolve the exact strain the paper gives ("Lachnospiraceae bacterium 2_1_58FAA", 658082). Don't use the generic node if a specific one is printed.
- *Treponema*, *Fretibacterium* reported as unnamed species → *Treponema* sp. (166), *Fretibacterium* sp. (2699746), not the bare genus.
- *Veillonella* at genus level plus *Veillonella* sp. → curate both (genus and sp.). Remove "unclassified Veillonellaceae".
- "Actinomycetes" mislabeled as a class → the appropriate class node, e.g. Acidimicrobiia (84992), when that's what the paper's class-level result means. Flag it if unsure. ⚠️ NCBI's class formerly named Actinobacteria is **Actinomycetes 1760**; Acidimicrobiia is a different class (see `mentor-rulings.md` §12). Don't copy 84992 by default.
- Methanogens reported as a group across classes → the reviewer curated the phylum (28890, Euryarchaeota), because they don't share a class. Flag it as a judgment call.

## 9. Crosswalk from skill curations (unreviewed)

Lessons from the curations in `curations/<PMID>/`, tagged by PMID. These are applications the skill worked out; no mentor has reviewed them yet. Every ID was re-checked on NCBI on 2026-10-30.

**Renamed taxa and synonyms** (enter the ID; BugSigDB shows the NCBI name, so keep the paper's name in `paper_name`):

| Paper name | NCBI node | Source |
|---|---|---|
| *Bacteroides coprophilus* | *Phocaeicola coprophilus* 387090 (species) | 29370410 |
| *Phocea* | *Merdimmobilis* 3028852 (genus; synonym Phocea) | 39901379 |
| Corynebacteriales | Mycobacteriales 85007 (order) | 41160784 |
| *Clostridium cocleatum* | *Thomasclavelia cocleata* 69824 (species) | 37805634 |
| "Mobilincus", "Peptinophilus" (author misspellings; no NCBI hit) | *Mobiluncus* 2050, *Peptoniphilus* 162289 (genera); add a note naming the misspelling | 35329834 |
| Greengenes S24-7 | Muribaculaceae 2005473 (family) | 37805634 |
| Phylum TM7 | *Candidatus* Saccharimonadota 95818 (phylum; NCBI synonym "*Candidatus* Saccharibacteria"; crosswalk entry for Study_300). 1-68 and ph2 (Greengenes genera in the same paper) have no node: text. NCBI "bacterium PH2" (239775) is a lineage-less "unclassified Bacteria" entry with nothing tying it to Greengenes ph2, so it doesn't count as the clone node; neither label appears in the export (2026-11-01) | 34607559 |
| SILVA Spirosomaceae | Spirosomataceae 2896860 (family) | 34934118 |
| SILVA Family_XI (Ezakiella, Peptoniphilus, Anaerococcus…) | Peptoniphilaceae 1570339 (family) | 33891612 |
| SILVA c__unidentified_Actinobacteria (class) | Actinomycetes 1760 (class; synonym Actinobacteria) | 33891612 |
| MetaPhlAn3 g_Erysipelatoclostridium | Thomasclavelia 3025755 (genus; NCBI rename) | 40615853 |
| MetaPhlAn3 f_Leuconostocaceae | Lactobacillaceae 33958 (merged). If f_Lactobacillaceae is also significant in the **opposite** direction, leave both out (opposite-direction rule below); same direction → enter 33958 once | 40615853 |
| Greengenes [Mogibacteriaceae] / "Clostridium Family XIII Incertae Sedis" | Anaerovoracaceae 543314 (family) | 29069100 |
| Bacteroidetes_unclassified repeated at order, class, family and genus | unclassified Bacteroidota 37452, entered once | 39901379 |
| *Prevotella colorans* (misspelt "Prevotella coloratum" in the same paper) | *Hallella colorans* 1703337 (species; NCBI synonym Prevotella colorans; also in BugSigDB 33596245). Plain-name esearch for the old name returns nothing, so search BugSigDB or the species epithet | 41174559 |
| Desulfobacterota (SILVA phylum) | Thermodesulfobacteriota 200940 (phylum); "Desulfobacterota" is not an NCBI name | 41174559 |
| *Pelomonas* | *Roseateles* 93681 (genus; esearch on "Pelomonas" returns 93681, scientific-name search returns nothing) | 39198832 |
| "Sediminibacter" and "Sediminibacterium" in the same paper (Greengenes) | Two different NCBI genera: *Sediminibacter* 379072 (Flavobacteriaceae) and *Sediminibacterium* 504481 (Chitinophagaceae). Curate each as printed and add a note that the shorter label may be a truncation | 39198832 |
| *Roseomonas lacus* | *Neoroseomonas lacus* 287609 (species); plain esearch for the old name returns nothing | 37696898 |
| *Chryseobacterium hispanicum* | *Epilithonimonas hispanica* 358687 (species) | 40377305 |
| *Chryseobacterium* sp. FF12 | *Chryseobacterium senegalense* 1608584 (species; synonym) | 40377305 |
| *Bifidobacterium vaginale* (GTDB / Greengenes2) | *Gardnerella vaginalis* 2702 (species; homotypic GTDB transfer, NCBI has no "Bifidobacterium vaginale"; no BugSigDB precedent as of 2026-11-01, so confidence 70) | 42059388 |
| *Prevotella buccalis* | *Hoylesella buccalis* 28127 (species; plain scientific-name esearch for the old name returns nothing, use [All Names]) | 42059388 |
| Bogoriellaceae | Allobogoriellaceae 145358 (family) | 40377305 |
| Phormidiaceae | Oscillatoriaceae 1892254 (family; synonym) | 40377305 |
| *Lactobacillus paraplantarum* | *Lactiplantibacillus paraplantarum* 60520 (species) | 40377305 |
| Acidobacteriales / Acidobacteriia (SILVA 128) | Terriglobales 204433 (order) / Terriglobia 204432 (class) | 40377305 |
| Xanthomonadales | Lysobacterales 135614 (order) | 40377305 |
| *Moraxella osloensis* | *Faucicola osloensis* 34062 (species) | 40377305 |
| SILVA c__Melainabacteria (class) | *Candidatus* Melainabacteria 1798710, which NCBI files as a **phylum**; rank mismatch noted, 70 | 40377305 |
| SILVA "s__bacterium_GC452011" | "bacterium GC45(2011)" 948171 (SILVA stripped the parentheses); 70 | 40377305 |
| SILVA c__Saccharimonadia / g__Candidatus_Saccharimonas / f__Saccharimonadaceae | *Candidatus* Saccharimonadia 2093818 / Saccharimonas (SeqCode) 1331051 / Saccharimonadaceae (SeqCode) 2171986 | 40377305 |
| SILVA f__Family_X (no parent shown) | **Open.** Unlike Family_XI and Family_XIII there is no crosswalk; entered as text at 50 (alternative: leave out, #791) | 40377305 |
| *Moraxella osloensis* | *Faucicola osloensis* 34062 (species) | 37696898 |
| *Phycicoccus aerophilus* | *Pedococcus aerophilus* 436356 (species) | 37696898 |
| SILVA "Blastocatellaceae (Subgroup 4)" / "Blastocatellaceae Subgroup4" | Blastocatellaceae 1748772 (family) | 37696898 |
| SILVA species placeholder "<Genus> estrogen degrading bacterium" | *<Genus>* sp. (e.g. *Filimonas* sp. 1954253). NCBI "estrogen-degrading bacterium" is a synonym of the generic "bacterium" 1869227: never use it | 37696898 |
| SILVA chloroplast labels named after a plant ("Brassica nigra black mustard") | Remove (§7); esearch resolves them to the plant (3710, division eudicots) | 37696898 |
| "Lacticaseibacillus iners / crispatus / jensenii" (Greengenes-based 5R/SMURF labels; these species were never moved to *Lacticaseibacillus*) | *Lactobacillus iners* 147802 / *crispatus* 47770 / *jensenii* 109790; 20 BugSigDB signatures use 147802 | 40304477 |
| *Atopobium vaginae* | *Fannyhessea vaginae* 82135 | 40304477 |
| *Labrenzia aggregata* | *Roseibium aggregatum* 187304 | 40304477 |
| *Arcobacter marinus* | *Malaciobacter marinus* 505249 | 40304477 |
| *Actinomyces neuii* | *Winkia neuii* 33007; plain esearch for the old name returns nothing | 40304477 |
| *Prevotella timonensis* / *Prevotella copri* | *Hoylesella timonensis* 386414 / *Segatella copri* 165179; plain esearch for the old names returns nothing | 40304477 |
| *Haemophilus parainfluenzae* | *Parahaemophilus parainfluenzae* 729 (species; same ID, NCBI renamed it; 207 BugSigDB signatures already use 729) | 29643500 |
| Greengenes phylum SR1 | *Candidatus* Absconditibacteriota 221235 (phylum); esearch "candidate division SR1" finds it, "Absconditabacteria" returns nothing, and "SR1 bacteria" returns a stick-insect genus (629395). 10 BugSigDB signatures use 221235 | 29643500 |
| Greengenes "Unclass. Clostridiales" at family **and** genus rank (Sci Rep forest plot) | unclassified Eubacteriales 39779 (no rank), entered once, as for Bacteroidetes_unclassified (39901379); #1189/#937 keep distinct unclassified features. 0 earlier BugSigDB uses, so 70. An OTU whose lowest Greengenes annotation is order Clostridiales is entered as the order (Eubacteriales 186802) | 29643500 |
| *Ochrobactrum intermedium* | *Brucella intermedia* 94625 | 40304477 |
| *Bacillus flexus* / *B. humi* / *B. firmus* | *Priestia flexa* 86664 / *Ferdinandcohnia humi* 263474 / *Cytobacillus firmus* 1399 | 40304477 |
| Greengenes2 2024.09 'Unclassified Peptostreptococcaceae_256921' (f__Peptostreptococcaceae_256921;__;__) | unclassified Peptostreptococcaceae 1411023 (no rank), under #2050; the GTDB family suffix is dropped because NCBI's family contains it. Alternative: text 'unclassified Peptostreptococcaceae 256921' as in unreviewed 40312795. Scored 70; blind senior review agreed | 41398357 |
| Greengenes2 'Ruminococcus_E sp003438075' (GTDB placeholder species) | Representative genome GCA_003438075.1 = *Eubacterium* sp. OM08-24 2292352, **not** type material, so the 40859402 route doesn't apply. Entered as text 'Ruminococcus E sp003438075' (#741/#860; unreviewed precedents 41747725, 40312795 type GTDB placeholders as text), 50, with 2292352 named in the discussion note | 41398357 |
| Greengenes2 Faecousia / Vescimonas / Methanobacteriota | Faecousia 2840588, Vescimonas 2892396 (genera); Methanobacteriota 28890 (phylum: NCBI's current name for the former Euryarchaeota node; esearch 'Euryarchaeota' now returns nothing) | 41398357 |
| Greengenes 13_8 (QIIME 1.9.1, RDP) 'UC X' labels (UC = unclassified) | NCBI 'unclassified X' nodes (#2050): UC Christensenellaceae 1917874, UC [Mogibacteriaceae] → unclassified Anaerovoracaceae 3030911, UC Desulfovibrionaceae 231685, UC Peptococcaceae 208050, UC Enterobacteriaceae 36866, UC Erysipelotrichaceae 544447, UC Lachnospiraceae 186928, UC Clostridiales → unclassified Eubacteriales 39779 | 31971855 |
| QIIME '<Order>; other' / '<Class>; other' (next rank assigned an empty name) | The lowest named rank: 'Clostridiales; other' → Eubacteriales 186802 (order), 'Clostridia; other' → Clostridia 186801 (class). Keep them separate from 'UC Clostridiales' (39779) when both are printed as distinct features. Scored 70 | 31971855 |
| Greengenes family RF16 (order Bacteroidales), 'UC RF16' | No NCBI node (esearch 0 hits, 0 export uses): text 'unclassified RF16' at 50; fallback Bacteroidales 171549 if a mentor asks. Senior review agreed | 31971855 |
| *Bosea thiooxidans* | *Allobosea thiooxidans* 53254 | 40304477 |
| "Escherichia/Shigella flexneri" (species-level slash label) | "Escherichia/Shigella sp." 1940338, applying TheTosin #952 at 70; the alternative *Shigella flexneri* 623 keeps the epithet. Open: no ruling on the species-level form | 40304477 |

**Homonyms** (the first name hit is not a bacterium). Check the NCBI *Division* field ("Bacteria"):

| Name | Use | Not |
|---|---|---|
| *Bacillus* | 1386 | 55087 (insect) |
| *Proteus* | 583 | 210425 (salamander) |
| *Bosea* | 85413 *Allobosea* (synonym "Bosea Das et al. 1996") | 169215 (plant) |
| k__Bacteria | 2 (domain) | 629395 (insect genus "Bacteria Latreille") |
| *Rhodococcus* | 1827 | 1661425 (insect) |
| *Rothia* | 32207 | 1380124 (moth), 508215 (plant); 41199330 |
| *Labrys* | 204476 | 2066135 (nematode) |
| *Rhodobium* | 34016 | 869314 (aphid) |
| *Paracoccus* | 265 | 249411 (scale insect); 40377305 |
| *Gordonia* | 2053 | 79255 (plant, Theaceae); NCBI esearch returns both, plant first; 35329834 |
| *Nitrospira* (genus label) | 1234 (genus) | 203693 Nitrospiria (class), which esearch also returns |

**One taxon reported several times.** Enter it once and say so in the notes:
- the same label at several ranks with identical values (e.g. "Bacteroidetes_unclassified" at four ranks), or a genus and its "s__un_g_<genus>" twin with identical means (34267209, 39901379)
- the same label as a family and a genus ("Clostridia UCG-014"), or two paper names that resolve to one NCBI node (Ruminococcaceae + Oscillospiraceae) (40366801)
- OTUs or ASVs with the same name in the same direction (35993728, 40369688). Opposite directions → leave out of both signatures (33225888)

**Greengenes orders named after a clone: use the clone node (mentor-reviewed precedent).** o__YS2 (class 4C0d-2) → "rumen bacterium YS2" **209265**; o__CW040 (class TM7-3) → "TM7 phylum sp. oral clone CW040" **163601**. SvetlanaUP reviewed 209265 in 24828543, 26962942, 35476894, 36388691 and 39470189, and 163601 in 35476894 and 38946731 (curated by TheTosin); there are no text entries in the export (2026-10-30). Both nodes are species rank, so note the rank mismatch. Before typing any Greengenes placeholder as text, search the export's `MetaPhlAn taxon names` column for the label (32702151; supersedes the text choice for YS2 in 37805634).

**No NCBI node: type it as text and add a note.** Greengenes F16, [Paraprevotellaceae], [Prevotella], [Ruminococcus] (37805634); SILVA "Mollicutes RF39", "Ruminococcaceae UCG 014", "Oscillospirales UCG-010" (an existing BugSigDB entry), "UCG-010" (33891612, 37760279, 39901379). Check whether autocomplete already has a hyphenated form ("UCG-001") before typing the spaced form.

**Majorbio Cloud "g__norank_f__<Family>" genus labels → the family itself** (e.g. g__norank_f__Lachnospiraceae → Lachnospiraceae 186803, g__norank_f__Atopobiaceae → Atopobiaceae 1643824; PMID 40828589, re-decided 2026-10-31). The maintainer ruled on this exact label format: SvetlanaUP, 2025-04, #630: "we skip unclassified/uncultured/norank… and record the first/lowest meaningful" name (`s_unclassified_g__norank_f__norank_o__Clostridia_UCG-014 → Clostridia_UCG-014`). TheTosin applied it in #822 (2025-07, citing #630). The same g_norank_f_ format was ruled family-level three more times: annemarie-sharp, 2025-05, #759 ("norank_f__Muribaculaceae, curate as 'Muribaculaceae'"); TheTosin, 2026-03, #1054 ("Curate g_norank_f_Bacillaceae and g_unclassified_f_Bacillaceae as 'Bacillaceae' once with ID: 186817"); and the live #630 page 37960154, where g__norank_f__Erysipelotrichaceae is Erysipelotrichaceae 128827 in Exp 5 Sig 1 (re-checked 2026-10-31). The only "unclassified" outcomes are #1284 (fiddyhamma, a peer reviewer, 2026-05: norank SBR1031 → unclassified SBR1031, an order-level placeholder) and the opposing precedent is annemarie-sharp's #798 review (2025-10: norank S24-7 → unclassified Muribaculaceae 2006847). Maintainers outrank other mentors, so mention #798 only as the alternative in a discussion note. #937/#1189 ("keep 'unclassified X' as written") apply only when the paper prints "unclassified X", not "norank". Read the mentor comments on the issue itself before calling rulings conflicting; the distilled summary had merged #630 into a row about "unclassified" labels. Applied ruling; the application to 40828589 is not yet mentor-reviewed.

**Open: Majorbio/SILVA "<Taxon>_unclassified" suffix labels** (genus-level row whose only name is a higher taxon, e.g. "Cyanobacteria_unclassified"). The 2026-10-31 norank settlement (#630) doesn't close this one, because the label says "unclassified". The skill's own precedents disagree. 39901379 kept the NCBI "unclassified <Phylum>" node (Bacteroidetes_unclassified → unclassified Bacteroidota 37452), following #937/#1189. 26287241 folded "Cyanobacteria_unclassified" into the phylum 1117, already listed in the same direction, following #630 and #822 (unclassified Cyanobacteriota 1983111 kept as the alternative). Pick one per paper, score 70, and put the alternative in the discussion note. No-rank "unclassified X" nodes don't appear in the export's NCBI ID column (37452 and 1983111: 0 hits, 2026-10-31), so the export can't settle it. Skill note, not yet mentor-reviewed.

**Open question, ask on Zulip: GTDB placeholder species from MetaPhlAn4 → GTDB conversion** (e.g. "CAG-41 sp900066215", "Lawsonibacter sp014287875"). Option A: map to the NCBI node of the representative genome when NCBI has a specific species node, otherwise text. Option B: type every GTDB name as written (as the GTDB-suffix ruling #741/#860 does for genera). PMID 41196050 used A at confidence 50.
- **A data point for Option A (40859402).** Check the representative assembly in NCBI Datasets (`/genome/accession/<GCF>/dataset_report` or `/genome/taxon/<taxid>/dataset_report`, field `type_material`). If it is the **type-material assembly** of a named species, the GTDB placeholder is that species under an interim name. Example: Allobacillus sp007559425 → GCF_007559425.1 = type material of *Allobacillus salarius* SKP4-8 → 1955272, scored 70. The GTDB API (api.gtdb.ecogenomic.org) was unreachable on 2026-11-01, but NCBI Datasets was enough.
- **Greengenes2/GTDB *named* species whose genus carries a suffix** ("Bacteroides_H thetaiotaomicron", "Ruminococcus_B gnavus", "Alistipes_A_871400 senegalensis", "Gemmiger_A_73129 qucibialis"): enter the NCBI species (818; *Mediterraneibacter gnavus* 33038, whose NCBI synonym is *Ruminococcus gnavus*; 1288121; 2997294). The suffix ruling (#741/#860) covers genus-level labels, and the authors usually write the plain binomial in their prose. Precedent 41196050 (Slackia_A isoflavoniconvertens → 572010). Scored 85; the senior review accepted it (40859402). Skill note, not yet mentor-reviewed.

**Greengenes 13_8 LEfSe labels printed as bare species epithets** ("nitroreducens", "coprosuis", "multivorum"; 30908851). Resolve each epithet's genus from the Greengenes 13_8 97% taxonomy (`qiime_default_reference/gg_13_8_otus/taxonomy/97_otu_taxonomy.txt.gz` in biocore/qiime-default-reference on GitHub) by counting OTUs per `g__…; s__<epithet>` lineage; never guess. Results: nitroreducens → *Pseudomonas* (14 of 15), coprosuis → *Bacteroides*, multivorum → *Sphingobacterium*, biforme → [Eubacterium] → *Holdemanella biformis* 1735, sordellii → [Clostridium] → *Paraclostridium sordellii* 1505, s__p-1630-c5 is a *Bulleidia* species (text "Bulleidia p-1630-c5"). Underscored labels in the plot ("_Prevotella_", "_Clostridium_") are the bracketed Greengenes genera; g__[Clostridium] sits in Peptostreptococcaceae, so it is not *Clostridium* 1485. Skill note, not yet mentor-reviewed.

**More renames and placeholder text forms (30908851, NCBI 2026-10-30):** *Coprococcus catus* → *Pseudocoprococcus catus* 116085; Epulopiscium → *Candidatus Epulonipiscium* 2383; Verrucomicrobiae → Verrucomicrobiia 203494; "Phenybacterium" (typo) → *Phenylobacterium* 20. Text forms with BugSigDB precedent: "Clostridiaceae SMB53", "Clostridiaceae 02d06" (35298505), "Peptococcaceae rc4-4 sp." (27912057; the genus-level form "Peptococcaceae rc4-4" was used here), "Mollicutes RF39" (22 wiki hits); without precedent: "Tissierellaceae GW-34", "Tissierella/Soehngenia" (slash rule, #573).

**BVAB1 reported as a genus** (27441565: "Bvab1" under Genera in Table 2, from a BVAB-modified Greengenes 13_8 RDP classifier; Results: "a bacterial vaginosis associated genus known as BVAB1"). NCBI now has the genus *Candidatus* Lachnocurva 3397567, whose only species is *Ca.* Lachnocurva vaginae 699240 (= Clostridiales genomosp. BVAB1). By the §3 [Policy] rank rule, a genus-level BVAB1 result → 3397567. Precedent conflicts: every BugSigDB study naming BVAB1 (25073854, 32719372, 33046723, 39479902, 39998243; export 2026-10-25) uses the species 699240. Check whether the paper reports BVAB1 as a species (→ 699240) or a genus (→ 3397567), and note the alternative in the discussion. BVAB2 has no genus node: Clostridiales genomosp. BVAB2 stays the species. Skill note, PMID 27441565; not yet mentor-reviewed.

**NCBI 'Includes' strains, synonym merges and duplicate strain nodes (28873967, NCBI 2026-10-31).** An old strain placeholder that NCBI lists under a species' "Includes" goes in as that species (*Coprobacillus* sp. 29_1 → *C. cateniformis* 100884; Peptostreptococcaceae bacterium OBRC8 → *Peptoanaerobacter stomatis* 796937); check efetch OtherNames, and note the paper's name. Two paper species that NCBI has merged (*Megamonas rupellensis* is a synonym of *M. funiformis* 437897) go in once per signature. When a strain name matches two nodes ("*Clostridium* sp. L2-50" 411489 vs "sp. L2_50" 2860053), pick the one that existed when the paper's reference database was built (efetch CreateDate: 2006 vs 2021; reference genomes May 2015). Skill note, not yet mentor-reviewed.

**Genus 'Atopobium' vs 'Fannyhessea' in vaginal studies: follow the label the paper's analysis printed** (38898981, 2026-10-31). NCBI *Atopobium* 1380 no longer contains the vaginal species (*Fannyhessea* 2767327), but enter the genus the analysis output prints (taxonomy §5 [Reviewer]; annemarie-sharp #1143: a reclassified genus substituted for the printed name was corrected back), and note any other label the authors use (SvetlanaUP #1000). SvetlanaUP-reviewed precedent follows the printed label both ways: 40925897 prints only 'Atopobium' → *Atopobium*; 41914628 prints only 'Fannyhessea' → *Fannyhessea* (export 2026-10-25: g__Atopobium 30 vaginal studies, 22 Reviewed; g__Fannyhessea 4). When one paper uses both (38898981: Fig 3C/Table S8 'Atopobium', Fig 1D display/Discussion 'Fannyhessea'), use the analysis tables' label. Skill note built on mentor rulings; the genus-specific application is not yet mentor-reviewed.

**Homonym trap: SILVA genus 'Paludicola' (Oscillospiraceae) has no bacterial NCBI node.** NCBI's only 'Paludicola' (2729669) is a red alga (Rhodophyta, Batrachospermaceae), and BugSigDB 37978347 already entered it in error. Type the bacterial genus as text with a note (41174559). The same applies to any genus whose single NCBI hit has a non-bacterial lineage: check the `division` field in esummary.

**SILVA '<Family>_genus' / '<group>_genus' labels** (41174559): use the NCBI 'unclassified <Family>' node where it exists (Victivallaceae_genus → 573637, Erysipelotrichaceae_genus → 544447; this follows the curator's norank decision on 33804345). Otherwise type the placeholder as text (Clostridia vadinBB60 group, UCG-010, F082, S0134 terrestrial group, WCHB1-41, p-2534-18B5 gut group). Don't use species-rank strain nodes such as 'Lachnospiraceae bacterium NK3A20' or 'Clostridiales bacterium CHKCI001' for genus labels (#1155), even though existing BugSigDB entries do. Anaeroglobus is filed by NCBI under Megasphaera 906. Skill note, not yet mentor-reviewed.

**"Unclassified X" in the text, family-only in the figure** (33847206; skill note, not yet mentor-reviewed). annemarie-sharp #2050 (NCBI "unclassified X" nodes) covers *features printed as unclassified* in the figure or table. When the text says "Unclassified Enterobacteriaceae" but the LEfSe figure prints only `f_Enterobacteriaceae`, the curated feature is the family: follow the figure (#812, #1051) and add a note. Don't apply #2050.

**Table rows "Family X; Unclassified genus"** (26600277, Greengenes 13_8 + RDP, Table I "Family Comamonadaceae; Unclassified genus"): a distinct printed feature, so use NCBI's "unclassified X" node under §12 current practice (#2050, #1189, #937): unclassified Comamonadaceae **83494** (no rank, parent 80864; 0 earlier BugSigDB uses, scored 70). The older #630 reading gives the family (80864). Skill note, not yet mentor-reviewed; senior review agreed.

**SILVA 138.2 placeholder genera with an NCBI strain node** (42857727, NCBI + export 2026-11-03; skill note, not yet mentor-reviewed). Use the node the export already uses, by analogy with the CAG rule: Ruminococcaceae DTU089 → Clostridiales bacterium DTU089 **1671661** (12 signatures); Gastranaerophilaceae Zag_111 → Candidatus Gastranaerophilales bacterium Zag_111 **1906167**; Oscillospiraceae UCG-005 → Ruminococcaceae bacterium UCG-005 **3068309** (73); Muribaculaceae CAG-873 → *Prevotella* sp. CAG:873 **1262936** (19); Lachnospiraceae CAG-56 → Firmicutes bacterium CAG:56 **1263031** (31). No node (text with spaces): Oscillospiraceae UCG 002/003, Erysipelotrichaceae UCG 003, Lachnospiraceae UCG 004, Family XIII UCG 001, Butyricicoccaceae UCG 008, Lachnospiraceae GCA-900066575, Family XIII AD3011 group, Christensenellaceae R-7 group, Lachnospiraceae FCS020 group (bacterium FCS020 1451755 is a strain, not the group), and the bracketed SILVA groups ([Eubacterium] coprostanoligenes/eligens/ventriosum group, [Clostridium] innocuum group). Renames: *Massiliomicrobiota timonensis* → *Massiliimicrobium timonense* 1776392; *Fournierella* → *Allofournierella* 1940255. DADA2 `addSpecies` "Genus sp." labels (no unique 100% species match) → the NCBI "Genus sp." node (Romboutsia sp. 1965302, Eubacterium sp. 142586, Megasphaera sp. 2023260, Paeniclostridium sp. 2023274).

**ID-from-memory trap: *Paenibacillus* is 44249.** 55080 is *Brevibacillus* (26600277: a remembered ID was caught only by the efetch check). Always look the ID up, even for common genera.

**Majorbio SILVA 138 extended-error-bar plots across ranks (37178109; skill note, not yet mentor-reviewed).**
- **One feature printed at several ranks has identical p-values.** Use that to merge: class "KD4-96", order "norank_c__KD4-96" and family "norank_o__norank_c__KD4-96" (all p = 0.038) → one text entry "KD4-96" at its named rank (#630); genus "UBA1819" and species "uncultured_organism_g_UBA1819" (both p = 0.002), genus *Bilophila* and species "uncultured_bacterium_g__Bilophila" (both 0.014) → the genus once. Different p-values mean different features (species row "Fusicatenibacter" p = 0.035 vs genus 0.032): there the species row was folded into the genus at 50, alternative *F. saccharivorans* 1150298.
- **Species-level rows printed as a bare family name** ("Lachnospiraceae", "Ruminococcaceae" under "Species level") → the Policy row "species known only to family" (§4): *Lachnospiraceae bacterium* 1898203; "Ruminococcaceae bacterium" resolves to **Oscillospiraceae bacterium 2485925**. Scored 70.
- **"norank_o_Oscillospirales" (family row) → Oscillospirales, which NCBI files as a synonym of Eubacteriales 186802** (esearch "Oscillospirales" returns 186802). If Eubacteriales is already in the same signature, enter it once; if in the opposite one, leave both out (#982).
- IDs looked up 2026-11-03: Desulfovibrionia 3031449 (class); *Shuttleworthia* → *Shuttleworthella* 177971; Campilobacterota → Campylobacterota 29547; "unclassified_k__norank_d__Bacteria" → unclassified Bacteria 49928 (#2050 form); "unclassified_p__Firmicutes" → unclassified Bacillota 84086; unclassified Dialister 2638756; unclassified Bacteroidales 185291; unclassified Eggerthellaceae 1720314. No NCBI node (text, with existing BugSigDB text precedent): Ethanoligenenaceae (no precedent), UBA1819 (130 wiki hits; don't use the species MAG node *Faecalibacterium* sp. UBA1819 for the genus label, #1155), KD4-96, "Eubacterium xylanophilum group", "Coriobacteriaceae UCG-002", "Lachnospiraceae UCG-006", "Burkholderia/Caballeronia/Paraburkholderia" (slash form, 18 wiki hits; #573).
