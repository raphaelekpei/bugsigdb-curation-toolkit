# BugSigDB controlled vocabularies

Pulled from the live bugsigdb.org property pages on 2026-10-15. These are the exact strings the Experiment form dropdowns accept. If a value you need is missing, it may have been added since — check the form on bugsigdb.org, or ask on Zulip for it to be added. Do not invent near-miss spellings.

## Contents
- Study design
- Location of subjects
- Sequencing type
- 16S variable region
- Sequencing platform
- Data transformation
- Statistical test
- MHT correction / Abundance in Group 1 / Alpha diversity
- Host species
- Matched on and Confounders controlled for
- Body site and Condition
- Quality control tags (reviewers only)

## Study design

Multiple designs may be selected (semicolon-delimited) when the paper genuinely contains more than one (e.g. a mouse laboratory experiment plus a human RCT). Otherwise pick the single best fit.

- case-control
- cross-sectional observational, not case-control
- time series / longitudinal observational
- laboratory experiment
- randomized controlled trial
- prospective cohort
- meta-analysis

## Sequencing type

qPCR and RT-qPCR are recorded as **PCR**. ITS/ITS2 is mostly fungal.

- 16S
- 18S
- WMS
- ITS / ITS2
- PCR
- RNA-Seq

## 16S variable region

Dropdown values 1–9 (the form shows the "V" prefix). Lower bound always; upper bound only for a range (V3–V4 → lower 3, upper 4; V4 alone → lower 4, upper blank). Leave blank if the paper does not state it.

## Sequencing platform

Multiple allowed. If the paper does not state the platform and it cannot be determined from the methods (e.g. instrument name like MiSeq/NovaSeq → Illumina), leave it blank rather than guessing.

- DNA-DNA Hybridization
- Human Intestinal Tract Chip
- Illumina
- Ion Torrent
- Mass spectrometry
- Non-quantitative PCR
- PacBio Vega (VS)/Revio (RS)/Sequel II
- PhyloChip
- Roche454
- RT-qPCR
- Sanger
- Nanopore
- BGISEQ-500 Sequencing
- DNBSEQ-G400
- DNBSEQ-T7
- MGISEQ-2000
- HTF-Microbi.Array
- 2b-RAD
- HB-2012A Medical Nucleic Acid Molecular Hybridizer

## Data transformation

Single value. Relative abundances is the default assumption; raw counts for count-model tools (DESeq2, edgeR, negative binomial/Poisson); centered log-ratio for CLR-based methods (ALDEx2, some ANCOM/corncob setups).

- raw counts
- relative abundances
- centered log-ratio
- arcsine square-root
- log transformation
- additive log-ratio

## Statistical test

Multiple allowed — record every test that produced *this* experiment's differential-abundance result (e.g. LEfSe experiments usually also list Kruskal-Wallis only if the paper says so; ANOVA + Post-Hoc Pairwise; Kruskall-Wallis + Dunn's test). Do not list tests used only for alpha/beta diversity or clinical variables. Note the site's own spelling "Kruskall-Wallis".

**ALDEx2 is not an option.** Enter the test ALDEx2 ran: Welch's t → "Welch's T-Test", Wilcoxon → "Mann-Whitney (Wilcoxon)", with data transformation "centered log-ratio", and name ALDEx2 in the signature description (precedent 40087549; 35092013). Paired Welch's still goes in as "Welch's T-Test" (there's no paired option).

- ANCOM
- ANCOM-BC
- ANCOM-BC2
- ANOSIM
- ANOVA
- Beta Binomial Regression
- Chi-Square
- Cox Proportional-Hazards Regression
- Decision Trees (xgBoost, gradient boosting)
- distance-based redundancy analysis (db-RDA)
- Dunn's test
- Dunnett's test
- DESeq2
- edgeR
- Fisher's Exact Test
- Fold-change cutoff
- G-test
- Jonckheere's trend test
- Kolmogorov-Smirnov Test
- Kruskall-Wallis
- LASSO Regression
- LEfSe
- Linear Discriminant Analysis
- Linear Regression or Generalized Linear Modeling (GLM)
- Logistic Regression
- Mann-Whitney (Wilcoxon)
- MaAsLin1
- MaAsLin2
- MaAsLin3
- metagenomeSeq
- Meta-Analysis
- Metastats
- Mixed-Effects Regression
- Negative Binomial Regression
- NLMIXED
- Pearson Correlation
- PERMANOVA
- Permutation Test
- PLS-DA (Partial least square discriminant analysis)
- Poisson Regression
- Post-Hoc Pairwise
- Random Forest Analysis
- Songbird
- Sparse Correlations for Compositional data (SparCC)
- Spearman Correlation
- Structural Equation Modeling (SEM)
- T-Test
- treeDA
- Wald Test
- Welch's T-Test
- Zero-Inflated Beta Regression
- Zero-Inflated Negative Binomial Regression

## MHT correction

Boolean dropdown: **Yes** / **No** / blank. Blank only when no traditional significance testing was used (Bayesian, effect-size cutoff).

## Abundance in Group 1

- increased
- decreased

## Alpha diversity

Fields: Pielou, Shannon, Chao1, Simpson, Inverse Simpson, Richness, Faith. Each takes **increased / decreased / unchanged** (Group 1 relative to Group 0), or blank when that index was not tested for this contrast. Observed features / observed OTUs / observed species / ACE map to **Richness** (reviewer convention). Evenness indices map to **Pielou**.

## Location of subjects

Country names exactly as listed (pulled 2026-10-15). Common trap: the US is **United States of America**, never "United States" or "USA" (1,670 experiments use it and 0 use "United States", even though mentors sometimes write "United States" informally). Check every country spelling against this list.

- Afghanistan
- Albania
- Algeria
- Andorra
- Angola
- Antigua and Barbuda
- Argentina
- Armenia
- Australia
- Austria
- Azerbaijan
- Bahamas
- Bahrain
- Bhutan
- Bolivia
- Bangladesh
- Barbados
- Belarus
- Belgium
- Belize
- Benin
- Bosnia and Herzegovina
- Botswana
- Brazil
- Brunei Darussalam
- Bulgaria
- Burkina Faso
- Burundi
- Cabo Verde
- Cambodia
- Cameroon
- Canada
- Central African Republic
- Chad
- Chile
- China
- Colombia
- Comoros
- Congo
- Cook Islands
- Costa Rica
- Croatia
- Cuba
- Cyprus
- Czechia
- Côte d'Ivoire
- Democratic Republic of the Congo
- Denmark
- Djibouti
- Dominica
- Dominican Republic
- Ecuador
- Egypt
- El Salvador
- Equatorial Guinea
- Eritrea
- Estonia
- Eswatini
- Ethiopia
- Faroe Islands
- Fiji
- Finland
- France
- Gabon
- Gambia
- Georgia
- Germany
- Ghana
- Greece
- Grenada
- Guatemala
- Guinea
- Guinea-Bissau
- Guyana
- Haiti
- Honduras
- Hungary
- Iceland
- India
- Indonesia
- Iran
- Iraq
- Ireland
- Israel
- Italy
- Jamaica
- Japan
- Jordan
- Kazakhstan
- Kenya
- Kiribati
- Kuwait
- Kyrgyzstan
- Laos
- Latvia
- Lebanon
- Lesotho
- Liberia
- Libya
- Lithuania
- Luxembourg
- Madagascar
- Malawi
- Malaysia
- Maldives
- Mali
- Malta
- Marshall Islands
- Mauritania
- Mauritius
- Mexico
- Micronesia
- Monaco
- Mongolia
- Montenegro
- Morocco
- Mozambique
- Myanmar
- Namibia
- Nauru
- Nepal
- Netherlands
- New Zealand
- Nicaragua
- Niger
- Nigeria
- Niue
- North Korea
- North Macedonia
- Norway
- Oman
- Pakistan
- Palau
- Panama
- Papua New Guinea
- Paraguay
- Peru
- Philippines
- Poland
- Portugal
- Qatar
- Republic of Korea
- Republic of Moldova
- Romania
- Russian Federation
- Rwanda
- Saint Kitts and Nevis
- Saint Lucia
- Saint Vincent and the Grenadines
- Samoa
- San Marino
- Sao Tome and Principe
- Saudi Arabia
- Senegal
- Serbia
- Seychelles
- Sierra Leone
- Singapore
- Slovakia
- Slovenia
- Solomon Islands
- Somalia
- South Africa
- South Korea
- South Sudan
- Spain
- Sri Lanka
- Sudan
- Suriname
- Sweden
- Switzerland
- Syrian Arab Republic
- Taiwan
- Tajikistan
- Thailand
- Timor-Leste
- Togo
- Tokelau
- Tonga
- Trinidad and Tobago
- Tunisia
- Turkey
- Turkmenistan
- Tuvalu
- Uganda
- Ukraine
- United Arab Emirates
- United Kingdom
- United Republic of Tanzania
- United States of America
- Uruguay
- Uzbekistan
- Vanuatu
- Venezuela
- Viet Nam
- Yemen
- Zambia
- Zimbabwe
- United States-Mexico Border

## Host species

"Not specified" is the form default; leave host blank/not specified for environmental studies. If the host is missing, ask an administrator on Zulip to add it.

- Not specified
- Acrocephalus sechellensis
- Acropora cervicornis
- Aedes aegypti
- Ailuropoda melanoleuca
- Ailurus fulgens
- Allenopithecus nigroviridis
- Amolops chunganensis
- Anas acuta
- Anas platyrhynchos
- Anas poecilorhyncha
- Anas querquedula
- Anas strepera
- Anolis carolinensis
- Anopheles coluzzii
- Anopheles funestus
- Anopheles gambiae
- Anser indicus
- Apis mellifera
- Apodemus speciosus
- Apodemus argenteus
- Arabidopsis thaliana
- Argyrosomus regius
- Aves
- Aythya ferina
- Bison bison bison
- Bos grunniens
- Bos taurus
- Branta canadensis
- Buxus sempervirens
- Caenorhabditis elegans
- Calonectris borealis
- Canis latrans
- Canis lupus
- Canis lupus familiaris
- Capra hircus
- Cebus capucinus
- Cercopithecus neglectus
- Cervus nippon kopschi
- Chlorocebus pygerythrus
- Circus aeruginosus
- Colobus angolensis
- Coturnix japonica
- Danio rerio
- Desmodus rotundus
- Drosophila melanogaster
- Duttaphrynus melanostictus
- Elephas maximus
- Eptesicus fuscus
- Equus caballus
- Equus hemionus hemionus
- Eulemur flavifrons
- Felis catus
- Fukomys damarensis
- Fulmarus glacialis
- Gallus gallus
- Gallus gallus domesticus
- Glossina palpalis palpalis
- Glossophaga soricina
- Grus grus
- Halcyon smyrnensis
- Hapalemur griseus
- Hirundo rustica
- Hoolock tianxing
- Homo sapiens
- Ixodes ricinus
- Lasioglossum malachurum
- Lemur catta
- Leptobrachella liui
- Macaca assamensis
- Macaca fascicularis
- Macaca mulatta
- Mauremys reevesii
- Mesocricetus auratus
- Mirza coquereli
- Molossus molossus
- Monodelphis domestica
- Moschus berezovskii
- Motacilla citreola
- Mus musculus
- Myodes rufocanus
- Myotis
- Myotis chinensis
- Myotis lucifugus
- Netta rufina
- Nomascus hainanus
- Nomascus concolor
- Ornithorhynchus anatinus
- Oryctolagus cuniculus
- Ovis aries
- Pan troglodytes
- Pelophylax nigromaculatus
- Perimyotis subflavus
- Phacochoerus africanus
- Phascolarctos cinereus
- Phoenicopterus roseus
- Pipistrellus
- Pipistrellus pipistrellus
- Pithecia pithecia
- Potamochoerus porcus
- Premnas biaculeatus
- Ptychadena mascareniensis
- Rana pipiens
- Rattus norvegicus
- Rhacophorus minimus
- Rhinolophus
- Rhinolophus ferrumequinum
- Rodentia
- Salmo salar
- Saxicola torquatus
- Schistura fasciolata
- Strongylocentrotus purpuratus
- Sturnira lilium
- Sus scrofa domesticus
- Symphalangus syndactylus
- Theloderma rhododiscus
- Theobroma cacao
- Theropithecus gelada
- Trachypithecus obscurus
- Tringa ochropus
- Tscherskia triton
- Ursus arctos
- Ursus maritimus
- Ursus thibetanus
- Vanellus malabaricus
- Varecia rubra
- Vulpes corsac
- Vulpes vulpes
- Xenopus laevis
- Xenopus tropicalis

## Matched on and Confounders controlled for

Both fields share this vocabulary (the Confounders page transcludes it). Use full terms, never abbreviations ("body mass index", not "BMI"). Prefer an existing term that means the same thing ("sex" rather than "gender") — values outside the list get flagged. Do not substitute a term with a different meaning ("sequence read depth" ≠ "sequencing batch"; "anxiety disorder" ≠ "mood disorder"); if no equivalent exists, enter it as reported.

- abdominalhernia
- abnormal glucose tolerance
- accute-on-chronic liver failure
- acetaldehyde
- acute graft vs. host disease
- acute lymphoblastic leukemia
- acute myeloid leukemia
- adenoma
- age
- AIDS
- air pollution
- alcohol consumption measurement
- alcohol drinking
- allergic rhinitis
- alzheimer's disease
- anal intercourse
- anorexia nervosa
- antibiotic
- antibiotic exposure
- antibiotic therapy
- antimicrobial agent
- antimicrobial agent during labor
- antiretroviral therapy
- anxiety disorder
- aortic valve insufficiency
- arthritis
- ascites
- asthma
- atopic asthma
- atopic eczema
- attention deficit hyperactivity disorder
- autism
- behcet's syndrome
- bipolar disorder
- birth country
- birth weight
- bladder calculus
- bladder disease
- blood pressure
- body height
- body mass index
- body odor measurement
- body weight
- breast cancer
- breast carcinoma
- breast feeding
- breast milk measurement
- breastfeeding duration
- bronchitis
- cannabis dependence
- cannabis use
- cellulitis
- cervical cancer
- cervical cerclage
- cervical glandular intraepithelial neoplasia
- cervical intraepithelial neoplasia
- cesarean section
- chemotherapy
- chlamydia trachomatis infectious disease
- chorioamnionitis
- chronic fatigue syndrome
- chronic hepatitis B virus infection
- chronic hepatitis C virus infection
- chronic kidney disease
- chronic obstructive pulmonary disease
- chronic pancreatitis
- cirrhosis of liver
- class/grade level
- coeliac
- colorectal cancer
- comorbidity
- constipation
- contraception
- cough
- COVID-19
- COVID-19 or sequela
- crohn disease
- cystitis
- date
- decreased circulating HDL cholesterol level
- delivery procedure
- demographics
- dental caries
- dental enamel hypoplasia
- diabetes mellitus
- diabetic retinopathy
- diet
- digestive system cancer
- digestive system infectious disease
- drug dependence
- EC 3.6.3.10 (H(+)/K(+)-exchanging ATPase) inhibitor
- eczema
- education level
- egg allergy
- encephalomyelitis
- end stage renal disease
- endometrial cancer
- epilepsy
- equol
- esophageal cancer
- esophageal carcinoma
- esophageal squamous cell carcinoma
- ethical considerations
- ethnic group
- extrahepatic cholestasis
- family history of cancer
- feeding practices
- female reproductive organ cancer
- food allergy
- formula feeding
- gangrene
- gastric adenocarcinoma
- gastric cancer
- gastric carcinoma
- geographic area
- gestational age
- gestational diabetes
- gingival disease
- gingivitis
- graft versus host disease
- graves disease
- graves ophthalmopathy
- hashimoto's thyroiditis
- HDL cholesterol change measurement
- head and neck carcinoma
- head and neck malignant neoplasia
- head and neck squamous cell carcinoma
- health
- health trait
- Helicobacter pylori
- Helicobacter pylori infectious disease
- Henoch-Schoenlein purpura
- hepatitis
- hepatitis, alcoholic
- hepatocellular carcinoma
- high fat diet
- history of GI
- HIV infection
- HIV/AIDS pre-exposure prophylaxis
- HLA match
- homelessness
- household income
- hp infection
- human papilloma virus infection
- huntington disease
- hygiene
- hyperlipidemia
- hyperplastic polyp
- hypertension
- hypertriglyceridemia
- idiopathic rapid eye movement
- immunosuppressant use measurement
- immunodeficiency 74, COVID-19-related, X-linked
- inflammatory bowel disease
- intake of diabetes medication
- iron deficiency anemia
- irritable bowel syndrome
- kidney stone
- leukemia
- leukocyte
- life style
- lung cancer
- lymphoma
- major depressive disorder
- marijuana
- marital status
- maternal age
- medical procedure
- medroxyprogesterone acetate
- menopause
- metabolic syndrome
- methamphetamine dependence
- milk allergic reaction
- mode of birth
- multiple myeloma
- multiple organ failure
- multiple sclerosis
- necrotizing enterocolitis
- neonatal jaundice
- neurogenic bladder
- neuromyelitis optica
- nicotine dependence
- non-alcoholic fatty liver
- non-alcoholic fatty liver disease
- non-hodgkins lymphoma
- non-small cell lung carcinoma
- number of sex partners
- number of teeth measurement
- nutritional supplement exposure measurement
- obesity
- obsessive-compulsive disorder
- opioid dependence
- oral candidiasis
- oral halitosis
- oral hygiene
- oral leukoplakia
- oral mucositis
- oral squamous cell carcinoma
- orthocoronavirinae infectious disease
- osteoarthritis
- otitis media with effusion
- ovarian cancer
- pancreatic carcinoma
- parity
- parkinson's disease
- pemphigus vulgaris
- peptic esophagitis
- peri-implantitis
- peridontal microbiome
- periodontal disease
- periodontal pocket
- periodontitis
- phenylketonuria
- physical activity
- pneumonia
- polycystic ovary syndrome
- polyp
- post-traumic stress disorder
- postpartum
- pre-exposure prophylaxis
- premature birth
- preterm premature rupture of the membranes
- primary care clinic
- probiotics during pregnancy
- prostate cancer
- proton-pump inhibitor
- psoriasis
- psoriatic arthritis
- psychosis
- pulmonary tuberculosis
- pyelonephritis
- race
- receptive anal intercourse frequency
- region
- region of residence
- renal cell carcinoma
- response to allogeneic hematopoietic stem cell transplant
- response to antineoplastic agent
- response to cancer immunotherapy
- rheumatoid arthritis
- salmonella gastroenteritis
- salmonellosis
- schizophrenia
- sepsis
- sequela of COVID-19
- sessile serrated adenoma
- severe aplastic anemia
- sex
- sex design
- sexual preference
- sexually transmitted infection
- sjogren's syndrome
- socioeconomic status
- smoking behavior
- smoking status
- spontaneous abortion
- squamous cell carcinoma
- staphylococcus skin infection
- status asthmaticus
- stimulus or stress design
- substance related disorder
- substance use
- syncope
- thyroid carcinoma
- time
- time from diagnosis
- titanium dioxide nanoparticles
- tongue neoplasm
- tonsillitis
- total cholesterol measurement
- transplant conditioning
- triglycerides
- tuberculosis
- type I diabetes mellitus
- type II diabetes mellitus
- ulcerative colitis
- unipolar depression
- urinary tract infection
- vaginal pH
- vital capacity
- vulvovaginitis
- waist circumference
- watching tv
- wilson disease
- diabetic neuropathy
- prediabetes syndrome
- vitiligo
- endometriosis
- life style
- sequence read depth

## Body site and Condition

These are not fixed dropdowns; they autocomplete from BugSigDB glossary terms (MediaWiki page titles, so the first letter is always capitalized; the lowercase rule on "How to standardize property values" is for admins adding *new* glossary terms), which map to ontologies:

- **Body site** → UBERON (https://www.ebi.ac.uk/ols4/ontologies/uberon). Enter it the way the form's autocomplete shows the glossary term, which has a capital first letter (e.g. "Vagina", "Feces", "Rheumatoid arthritis"): BugSigDB stores "Vagina" in 256 experiments and never "vagina" (export 2026-10-21). Select the suggestion rather than free-typing. Pick the most specific site the samples actually came from ("dental plaque" over "oral cavity"; "tongue" over "dorsum of tongue" when that is the glossary term). Stool samples → **feces**. Vaginal swabs → **vagina**. Remember synonyms (mouth / oral cavity).
- **Condition** → EFO (https://www.ebi.ac.uk/ols4/ontologies/efo). Glossary term with a capital first letter, as autocomplete shows it. The condition is what *this experiment's* contrast differs on, not the paper's overall topic. Search existing curated studies on the same topic to see which EFO term was used before. Common patterns: "Response to <drug>" for treatment-vs-no-treatment or response contrasts, but "<drug> dose measurement" or the drug term itself (e.g. "Methotrexate") for dose correlations, "response to diet", "response to transplant", "ethnic group", "diet", "smoking status measurement", "<X> measurement" for continuous traits (e.g. "high density lipoprotein cholesterol measurement"), "opioid use measurement". Never "microbiome measurement".

Each glossary term page lists **aliases** (synonyms). A typed condition or body site is matched to its canonical term through them (e.g. "MTX" → methotrexate). If autocomplete doesn't find a word, try a synonym.

### Fallback terms used in skill curations (unreviewed unless a precedent is named)

When the exact concept has no glossary term, these were the nearest selectable terms (#1965 nearest-parent rule). Check that each one autocompletes, and cite the precedent in a note.

| Concept in the paper | Term used | Precedent / PMID |
|---|---|---|
| Malondialdehyde, superoxide dismutase | Oxidative Stress | precedent 37789856; 36082082, 42075812 |
| Glutathione (GSH) | Glutathione | 36082082, 42075812 |
| Probiotic supplement (e.g. Bifico capsules in pregnancy) | **The study's disease** (e.g. Preeclampsia), with the supplement described in the Group 1 definition. SvetlanaUP-reviewed probiotic experiments do this (37836514 Exp 14–15 one-vs-all Bifidobacterium formulation → Constipation; 35956415 preterm-infant probiotics → Premature birth; 37225124, 39861457, 36228569), consistent with #844. "Nutraceutical" is only in peer-reviewed 26238090, 36678227, 30711862; "Diet" (#494) is the fallback when no disease applies; "Bifidobacterium" is a selectable Condition page with 0 uses (SMW query 2026-11-01) | 41199330 (changed from Nutraceutical 2026-11-01) |
| Direct or total bilirubin | Bilirubin measurement | 38384504, 32702151 (export: 4 earlier TBIL/DBIL experiments) |
| Bile acids, serum total bile acid (TBA) | Blood metabolite measurement (not "Serum metabolite measurement", 0 uses) | 33225888, 32702151 |
| OGTT 0 h / 1 h / 2 h glucose | Glucose tolerance test; fasting glucose at enrollment → Fasting blood glucose measurement | export precedent (9 OGTT experiments); 32702151 |
| Fructosamine, blood urea nitrogen | Fructosamine measurement, Blood urea nitrogen measurement (both exist and are selectable) | 32702151 |
| Tissue or ferrous iron | Iron biomarker measurement | 36082082 |
| Vaginal H2O2 | Hydrogen peroxide (CHEBI:16240) | 39641435 |
| Number of sexual partners | Sexual behavior | 39641435 |
| Controlled wood smoke exposure (pre vs post) | Air pollution (30 precedents, incl. wood smoke 31753468 and pre- vs post-smog 30804895; EFO has no wood-smoke term) | 40377699 |
| Vaginal pH | no term: ask on Zulip | 39641435 |
| Parity (nulliparous vs parous) | Parous; for multi-level parity, Number of pregnancies measurement | precedent 32468338; 37760279 |
| Primary vs secondary infertility | Female infertility | precedent 39868783; 38424540 |
| Abnormal placental growth defined only by low placental growth factor (PlGF/PIGF) MoM | Placenta growth factor measurement (EFO:0010626; selectable, 0 earlier uses); "Placental insufficiency" is the selectable alternative | 34607559 |
| Preeclampsia and abnormal placentation pooled as one "abnormal pregnancy" group | Pregnancy disorder (MONDO:0024575; selectable) | 34607559 |
| Urine protein score or concentration (correlation) | Proteinuria (HP:0000093; selectable); EFO has no urine-protein measurement term | 34607559 |
| Acupuncture or electroacupuncture | Treatment | precedent 32827699; 36082082 |
| Herbal formula vs disease model (rodents) | Traditional Chinese medicine type | reviewed precedent 34289209; 42075812 |
| High-salt gavage | Sodium chloride | 32504527 |
| Curcumin in feed | Curcumin | precedent 36467550; 42404072 |
| Android fat % | Body fat distribution | precedent 40059170; 40275186 |
| Food-group intake (grain, dairy) | Diet | precedent 42202778; 40275186 |
| Breastfed vs formula | Response to diet (not "Breastfeeding duration") | precedent 30173873; 27746239 |
| Quartile 4 vs quartile 1 of a dietary principal component (PCA of nutrient intake) | Diet (reviewed precedent 30355393, fibre-intake quartiles, DESeq2; 40914795 Q1 vs Q4 diet). Name the PC and its main loadings in Group 1 definition | 29643500 |
| Quartiles of total white blood cell (WBC) count | Leukocyte count (Category:Condition, checked 2026-10-31); export alternatives "Leukocyte" (1, reviewed 39438708), "Complete blood cell count" (2) | 29643500 |
| Personal or vaginal lubricant use during sex | Sexual behavior (no lubricant term in EFO or glossary, 2026-10-30) | 34537015 |
| Uterine lavage fluid (body site) | Endometrial cavity | precedent 31327470; 38424540 |
| Endometrial fluid aspirated by catheter at embryo transfer (body site) | Endometrial cavity (no earlier endometrial-fluid experiment; "Endometrium" is used for tissue) | 39198832 |
| Embryo implantation success vs failure after IVF-ET (single or multiple failures) | Female infertility (EFO has no implantation-failure term, OLS 2026-10-30) | reviewed precedent 35413875 (RIF); 39198832 |
| "Fetal membrane" specimen that is chorion only, amnion stripped (body site) | Chorion membrane (UBERON_0003124); "Fetal membrane" (UBERON_0005630) exists for amnion + chorion together | 37696898 |
| Maternal peripheral blood (body site) | Blood (28 experiments; "Peripheral blood" has no glossary page, "Venous blood" 1) | 37696898 |
| Duration of membrane rupture (condition) | **open**: "Premature rupture of membranes" (HP_0001788) used at 50; "Time" is the generic alternative; precedent 38311451 (short vs long rupture duration) left Condition blank. Ask on Zulip | 37696898 |
| Radiation enteritis (RE vs non-RE, or RE grade) | Radiation-induced gastrointestinal mucositis (EFO:1001914); EFO has no radiation-enteritis/enteropathy term (OLS 2026-10-30) | 30908851 |
| Pre- vs post-radiotherapy samples in the same patients | Response to radiation (GO:0009314; 3 BugSigDB precedents) | 30908851 |
| Fecal acetate (continuous, Low/High) | Acetate measurement (EFO_0010112; selectable) | 42857727 |
| Fecal butyrate, propionate or valerate (continuous) | Fatty acid measurement (no butyrate/propionate/valerate measurement pages, 2026-11-03; "Butyrate" and "Propionic acid" pages are CHEBI chemicals). SvetlanaUP-reviewed 35573767 Exp 15 used it for fecal butyric acid | 42857727 |
| Country or research-site contrast along a development/urbanisation gradient (site vs reference country) | Environmental factor (SvetlanaUP-reviewed 39944406, village vs urban); "Lifestyle measurement" is the KateRasheed-reviewed alternative (40819064, rural/urban/Italy vs Burkina Faso). Location of subjects = the two countries compared | 42857727 |
| Confounder "site" (multi-country cohort) | geographic area (closest list term); SCFAs entered as reported ("acetate", "butyrate"…), no list terms | 42857727 |

### Cytokine and CRP conditions (checked against Category:Condition 2026-11-01, PMID 40859402)

Selectable:
- "C-reactive protein measurement"
- "Macrophage inflammatory protein 1b measurement" (MIP-1β, CCL4)
- "Granulocyte colony-stimulating factor measurement" (G-CSF)
- "Chemokine (C-C motif) ligand 27 measurement" (CTACK, CCL27)
- "Interleukin 17 measurement" (used in 36059521)
- the generic "Cytokine measurement" and "Inflammatory biomarker measurement"

**No page exists for:** "C-C motif chemokine 4/27 measurement", "Granulocyte colony stimulating factor measurement" (unhyphenated), "Chemokine measurement" or "C-reactive protein". For other chemokines, search for the "Chemokine (C-C motif) ligand N" / "(C-X-C motif)" wording before falling back to a generic term.

### When a glossary term won't autocomplete

The Body site and Condition boxes only offer glossary pages that are **in Category:Body site / Category:Condition**. A page can exist with the right `Section=` and still be missing from the category if it hasn't been refreshed since it was created (e.g. "Methotrexate": Section=Condition, but no categories since 2025-02-26). Check:
`https://bugsigdb.org/w/api.php?action=query&titles=<Term>&prop=categories&format=json`
Query **one title per call**. With several `titles=A|B|C`, the category list is truncated (default `cllimit` 10 across all pages), so selectable terms falsely show no categories (32702151).
If the category is missing, the curator can open the term's page and use **Refresh** in the page-tools menu (or ask in Zulip #bsdb-questions for an admin to fix it), or choose the closest term that *is* selectable and explain why in the review reply.

The **"Find a term"** link beside the field opens the EFO/UBERON ontology browser for looking up the official name. It doesn't fill the box. Only glossary terms can be selected, by typing a few letters and clicking a dropdown suggestion.

## Quality control tags (reviewers only)

- Retracted paper
- Contamination issues suspected
- Batch effect issues suspected
- Uncontrolled confounding suspected
- Results are suspect (various reasons)

**Fallback conditions (38898981, OLS4 2026-10-31; skill note, not yet mentor-reviewed):** serum prolactin → "Amount of prolactin" (OBA:1000952; no prolactin measurement term in EFO or the export); intrauterine adhesion → "Asherman syndrome" (MONDO:0015299, synonym intrauterine adhesions); premature ovarian insufficiency → "Primary ovarian insufficiency" (6 experiments in the export).

**Liver / TIPS conditions (40615853, bugsigdb.org category check 2026-10-31; skill note, not yet mentor-reviewed):** hepatic encephalopathy → "Encephalopathy" (HP:0001298, the HP parent; no "Hepatic encephalopathy" page); change in blood ammonia → "Blood metabolite measurement" (no "Ammonia measurement" page; "Hyperammonemia" exists but is a state, not a rise); before vs after TIPS → "Response to surgery" (reviewed pre/post precedent 38037123; alternative "Therapeutic Procedure").

**Perinatal-factor conditions (40377305, export 2026-10-25; skill note):** neonatal sex → "Biological sex" (27 uses; in 30 of 35 sex contrasts Group 0 is male; no mentor ruling on the order); maternal age → "Age" (as in 37199635, 38384504, 30332459); delivery mode → "Cesarean section" (63 uses; US spelling, not "Caesarean"), Group 1 = cesarean; gestational weight gain categories → "Gestational weight gain measurement" (15 uses); birth weight classes → "Birth weight" (EFO:0004344); pre-pregnancy BMI classes → "Body mass index".

**Food-frequency conditions (33804345, bugsigdb.org title check 2026-10-31):** only "Fish consumption measurement" and "Alcohol consumption measurement" exist as food-specific glossary pages; fruit, egg, nut, soybean and meat intake use "Diet measurement" (fallback precedent 40275186) with the food named in the group names. Skill note, not yet mentor-reviewed.

**Nutrient-intake conditions (34579172, bugsigdb.org title check 2026-10-31):** existing pages: Energy intake, Fat intake measurement, Protein intake measurement, Carbohydrate intake measurement, Fish consumption measurement, Alcohol consumption measurement, Diet measurement. No page for SFA/MUFA/PUFA, dietary cholesterol, fiber, glycemic index or Healthy Eating Index: fat subtypes → Fat intake measurement, the rest → Diet measurement, with the nutrient in the group names. Skill note, not yet mentor-reviewed.

**Antidepressant / stress / reproductive-period conditions in rodents (31971855, export 2026-11-03; skill note, not yet mentor-reviewed):** fluoxetine vs vehicle → "Response to antidepressant" (SvetlanaUP-reviewed 38378622; the unreviewed 38877103 typed "Fluoxetine"); early life stress (maternal separation) vs control handling → "Response to stress" (GO:0006950; 33655759 maternal separation, 4 reviewed uses; alternative "Stress-related disorder"), 70; gestation vs lactation in the same animals → "Postpartum" (36563663, human, SvetlanaUP) or "Pregnancy" (30154758, sow, SvetlanaUP, the closest animal precedent), 70 either way.
