# Some possible invokes


chromosome 2
```
ENSG00000155657 = TTN Titin	Cardiomyopathy & Myopathy	Autosomal Dominant,# Autosomal recessive	49# (53%)	7837# (37%)
```


chromosome 19   NC_000019.10
```
ENSG00000105329	TGFB1	CED, DPD1, IBDIMDE, LAP, TGF-beta1, TGFB, TGFbeta	transforming growth factor beta 1	transforming growth factor beta-1 proprotein|TGF-beta-1|latency-associated peptide|prepro-transforming growth factor beta-1|transforming growth factor beta1	19q13.2	19	NC_000019.10	41330323	41353922	minus	7	190180
ENSG00000090339	ICAM1	BB2, CD54, P3.58	intercellular adhesion molecule 1	intercellular adhesion molecule 1|ICAM-1|cell surface glycoprotein P3.58|epididymis secretory sperm binding protein|intercellular adhesion molecule 1 (CD54), human rhinovirus receptor|major group rhinovirus receptor	19p13.2	19	NC_000019.10	10271120	10286615	plus	7	147840
ENSG00000196218 = RYR1 ryanodine receptor 1	Neuromuscular disease	Autosomal Dominant,# Autosomal recessive	36# (53%)	2118# (42%)
```

```
ENSG00000094914 = AAAS aladin WD repeat nucleoporin
ENSG00000008710 = PKD1 polycystin 1	Kidney disease	Autosomal Dominant	57# (41%)	794# (33%)
ENSG00000092054 = MYH7 Myosin heavy chain 7	Cardiomyopathy & Myopathy	Autosomal Dominant	34# (42%)	1740# (50%)
ENSG00000134571 = MYBPC3 Myosin binding protein C3	Cardiomyopathy	Autosomal Dominant,# Autosomal recessive	28# (30%)	1136# (40%)
ENSG00000198691 = ABCA4 ATP binding cassette # subfamily A member 4	Retinal degeneration	Autosomal recessive	29# (31%)	815# (30%)
ENSG00000128591 = FLNC Filamin C	Cardiomyopathy & Myopathy	Autosomal Dominant	38# (86%)	1587# (50%)
ENSG00000042781 = USH2A # Usherin	Usher syndrome	Autosomal recessive	40# (38%)	1696# (31%)
ENSG00000183638 = RP1L1 # RP1-like protein 1	Retinal degeneration	Autosomal Dominant, # Autosomal recessive	24 # (86%)	313 # (37%)
ENSG00000164199 = ADGRV1 # Adhesion G protein-coupled# receptor V1	Usher syndrome	Autosomal Dominant, # Autosomal recessive	30 # (67%)	1665 # (48%)
```

The VEP fields in their original JSON

```json
{
   "input": "1 1918090 test1 A G . . .",
   "id": "test1",
   "seq_region_name": "1",
   "start": 1918090,
   "end": 1918090,
   "strand": 1,
   "allele_string": "A/G",
   "most_severe_consequence": "missense_variant",
   "colocated_variants": [
     {
       "id": "COSV57068665",
       "seq_region_name": "1",
       "start": 1918090,
       "end": 1918090,
       "strand": 1,
       "allele_string": "COSMIC_MUTATION"
     },
     {
       "id": "rs28640257",
       "seq_region_name": "1",
       "start": 1918090,
       "end": 1918090,
       "strand": 1,
       "allele_string": "A/G/T",
       "minor_allele": "G",
       "minor_allele_freq": 0.352,
       "frequencies": {
         "G": {
           "amr": 0.5072,
           "gnomade_sas": 0.369,
           "gnomade": 0.4541,
           "gnomade_oth": 0.4611,
           "gnomade_asj": 0.3909,
           "gnomade_nfe": 0.4944,
           "gnomade_afr": 0.103,
           "afr": 0.053,
           "gnomade_amr": 0.5641,
           "gnomade_fin": 0.474,
           "sas": 0.3906,
           "gnomade_eas": 0.4598,
           "eur": 0.4901,
           "eas": 0.4623
         }
       }
     }
   ],
   "transcript_consequences": [
     {
       "variant_allele": "G",
       "consequence_terms": [
         "missense_variant"
       ],
       "gene_id": "ENSG00000178821",
       "transcript_id": "ENST00000310991",
       "strand": -1,
       "cdna_start": 436,
       "cdna_end": 436,
       "cds_start": 422,
       "cds_end": 422,
       "protein_start": 141,
       "protein_end": 141,
       "codons": "aTg/aCg",
       "amino_acids": "M/T",
       "polyphen_prediction": "benign",
       "polyphen_score": 0.001,
       "sift_prediction": "tolerated",
       "sift_score": 0.22,
       "hgvsp": "ENSP00000311122.3:p.Met141Thr",
       "hgvsc": "ENST00000310991.8:c.422T>C"
       }
   ],
   "regulatory_feature_consequences": [
     {
       "variant_allele": "G",
       "consequence_terms": [
         "regulatory_region_variant"
       ],
       "regulatory_feature_id": "ENSR00000000255"
     }
   ]
 }
```

```
# tax_id	Org_name	GeneID	CurrentID	Status	Symbol	Aliases	description	other_designations	map_location	chromosome	genomic_nucleotide_accession.version	start_position_on_the_genomic_accession	end_position_on_the_genomic_accession	orientation	exon_count	OMIM
# 9606	Homo sapiens	348	0	live	APOE	AD2, APO-E, ApoE4, LDLCQ5, LPG	apolipoprotein E	apolipoprotein E|apolipoprotein E3	19q13.32	19	NC_000019.10	44905796	44909393	plus	6	107741
# 9606	Homo sapiens	7515	0	live	XRCC1	RCC, SCAR26	X-ray repair cross complementing 1	DNA repair protein XRCC1|X-ray repair complementing defective repair in Chinese hamster cells 1|X-ray repair cross-complementing protein 1	19q13.31	19	NC_000019.10	43543311	43575527	minus	17	194360
# 9606	Homo sapiens	3949	0	live	LDLR	FH, FHC, FHCL1, LDLCQ2	low density lipoprotein receptor	low-density lipoprotein receptor|LDL receptor|low-density lipoprotein receptor class A domain-containing protein 3	19p13.2	19	NC_000019.10	11089463	11133820	plus	19	606945
# 9606	Homo sapiens	581	0	live	BAX	BCL2L4	BCL2 associated X, apoptosis regulator	apoptosis regulator BAX|BCL2 associated X protein|BCL2-associated X protein omega|Baxdelta2(G8)-RFS protein|Baxdelta2G9|Baxdelta2G9omega|Baxdelta2omega|bcl-2-like protein 4|bcl2-L-4	19q13.33	19	NC_000019.10	48954875	48961798	plus	7	600040
# 9606	Homo sapiens	9518	0	live	GDF15	GDF-15, HG, MIC-1, MIC1, NAG-1, PDF, PLAB, PTGFB	growth differentiation factor 15	growth/differentiation factor 15|NRG-1|NSAID (nonsteroidal anti-inflammatory drug)-activated protein 1|NSAID-activated gene 1 protein|NSAID-regulated gene 1 protein|PTGF-beta|macrophage inhibitory cytokine 1|non-steroidal anti-inflammatory drug-activated gene-1|placental TGF-beta|placental bone morphogenetic protein|prostate differentiation factor	19p13.11	19	NC_000019.10	18386158	18389176	plus	2	605312
# 9606	Homo sapiens	282617	0	live	IFNL3	IFN-lambda-3, IFN-lambda-4, IL-28B, IL-28C, IL28B, IL28C	interferon lambda 3	interferon lambda-3|cytokine Zcyto22|interferon, lambda 4|interleukin-28B|interleukin-28C	19q13.2	19	NC_000019.10	39243455	39245250	minus	6	607402
# 9606	Homo sapiens	2068	0	live	ERCC2	COFS2, EM9, TFIIH, TTD, TTD1, XPD	ERCC excision repair 2, TFIIH core complex helicase subunit	general transcription and DNA repair factor IIH helicase subunit XPD|BTF2 p80|CXPD|DNA 5'-3' helicase XPD|DNA excision repair protein ERCC-2|DNA repair protein complementing XP-D cells|TFIIH 80 kDa subunit|TFIIH basal transcription factor complex 80 kDa subunit|TFIIH basal transcription factor complex helicase XPB subunit|TFIIH basal transcription factor complex helicase XPD subunit|TFIIH basal transcription factor complex helicase subunit|TFIIH p80|TFIIH subunit XPD|basic transcription factor 2 80 kDa subunit|excision repair cross-complementation group 2|excision repair cross-complementing rodent repair deficiency, complementation group 2|xeroderma pigmentosum complementary group D|xeroderma pigmentosum group D-complementing protein	19q13.32	19	NC_000019.10	45349837	45370573	minus	25	126340
# 9606	Homo sapiens	56729	0	live	RETN	ADSF, FIZZ3, RENT1, RSTN, XCP1, RETN	resistin	resistin|C/EBP-epsilon regulated myeloid-specific secreted cysteine-rich protein precursor 1|adipose tissue-specific secretory factor|c/EBP-epsilon-regulated myeloid-specific secreted cysteine-rich protein|cysteine-rich secreted protein A12-alpha-like 2|cysteine-rich secreted protein FIZZ3|found in inflammatory zone 3|resistin delta2	19p13.2	19	NC_000019.10	7669049	7670455	plus	4	605565
# 9606	Homo sapiens	2067	0	live	ERCC1	COFS4, RAD10, UV20	ERCC excision repair 1, endonuclease non-catalytic subunit	DNA excision repair protein ERCC-1|excision repair cross-complementation group 1|excision repair cross-complementing rodent repair deficiency, complementation group 1 (includes overlapping antisense sequence)	19q13.32	19	NC_000019.10	45407334	45451547	minus	13	126380
# 9606	Homo sapiens	682	0	live	BSG	5F7, CD147, EMMPRIN, EMPRIN, HAb18G, OK, TCSF	basigin (Ok blood group)	basigin|OK blood group antigen|collagenase stimulatory factor|extracellular matrix metalloproteinase inducer|hepatoma-associated antigen|leukocyte activation antigen M6|tumor cell-derived collagenase stimulatory factor	19p13.3	19	NC_000019.10	571283	583493	plus	10	109480
# 9606	Homo sapiens	1786	0	live	DNMT1	ADCADN, AIM, CXXC9, DNMT, HSN1E, MCMT, m.HsaI	DNA methyltransferase 1	DNA (cytosine-5)-methyltransferase 1|CXXC-type zinc finger protein 9|DNA (cytosine-5-)-methyltransferase 1|DNA MTase HsaI|DNA methyltransferase HsaI	19p13.2	19	NC_000019.10	10133346	10194953	minus	41	126375
# 9606	Homo sapiens	3643	0	live	INSR	CD220, HHF5	insulin receptor	insulin receptor|IR	19p13.2	19	NC_000019.10	7112265	7294414	minus	22	147670
# 9606	Homo sapiens	718	0	live	C3	AHUS5, ARMD9, ASPa, C3b, CPAMD1, HEL-S-62p, C3	complement C3	complement C3|C3 and PZP-like alpha-2-macroglobulin domain-containing protein 1|C3a anaphylatoxin|acylation-stimulating protein cleavage product|complement component 3|complement component C3a|complement component C3b|epididymis secretory sperm binding protein Li 62p|prepro-C3	19p13.3	19	NC_000019.10	6677704	6720650	minus	41	120700
# 9606	Homo sapiens	5329	0	live	PLAUR	CD87, U-PAR, UPAR, URKR	plasminogen activator, urokinase receptor	urokinase plasminogen activator surface receptor|monocyte activation antigen Mo3|u-plasminogen activator receptor form 2|urokinase-type plasminogen activator (uPA) receptor	19q13.31	19	NC_000019.10	43646095	43670169	minus	9	173391
# 9606	Homo sapiens	811	0	live	CALR	CALR1, CRT, HEL-S-99n, RO, SSA, cC1qR	calreticulin	calreticulin|CRP55|ERp60|HACBP|Sicca syndrome antigen A (autoantigen Ro; calreticulin)|calregulin|endoplasmic reticulum resident protein 60|epididymis secretory sperm binding protein Li 99n|grp60	19p13.13	19	NC_000019.10	12938609	12944489	plus	9	109091
# 9606	Homo sapiens	6794	0	live	STK11	LKB1, PJS, hLKB1	serine/threonine kinase 11	serine/threonine-protein kinase STK11|liver kinase B1|polarization-related protein LKB1|renal carcinoma antigen NY-REN-19|serine/threonine-protein kinase 11|serine/threonine-protein kinase LKB1	19p13.3	19	NC_000019.10	1205778	1228431	plus	12	602216
# 9606	Homo sapiens	1994	0	live	ELAVL1	ELAV1, HUR, Hua, MelG	ELAV like RNA binding protein 1	ELAV-like protein 1|ELAV (embryonic lethal, abnormal vision, Drosophila)-like 1 (Hu antigen R)|Hu antigen R|Human antigen R|embryonic lethal, abnormal vision, drosophila, homolog-like 1|hu-antigen R	19p13.2	19	NC_000019.10	7958573	8005641	minus	7	603466
# 9606	Homo sapiens	4854	0	live	NOTCH3	CADASIL, CADASIL1, CASIL, IMF2, LMNS	notch receptor 3	neurogenic locus notch homolog protein 3|Notch homolog 3|notch 3	19p13.12	19	NC_000019.10	15159038	15200995	minus	33	600276
# 9606	Homo sapiens	57817	0	live	HAMP	HEPC, HFE2B, LEAP1, PLTR	hepcidin antimicrobial peptide	hepcidin|hepcidin preproprotein|liver-expressed antimicrobial peptide 1|putative liver tumor regressor	19q13.12	19	NC_000019.10	35282528	35285143	plus	3	606464
# 9606	Homo sapiens	354	0	live	KLK3	APS, KLK2A1, PSA, hK3	kallikrein related peptidase 3	prostate-specific antigen|P-30 antigen|gamma-seminoprotein|kallikrein-3|semenogelase|seminin	19q13.33	19	NC_000019.10	50854915	50860764	plus	5	176820
# 9606	Homo sapiens	268	0	live	AMH	MIF, MIS	anti-Mullerian hormone	muellerian-inhibiting factor|Mullerian inhibiting factor|Mullerian inhibiting substance|anti-Muellerian hormone|muellerian-inhibiting substance	19p13.3	19	NC_000019.10	2249323	2252073	plus	5	600957
# 9606	Homo sapiens	1050	0	live	CEBPA	C/EBP-alpha, CEBP	CCAAT enhancer binding protein alpha	CCAAT/enhancer-binding protein alpha|CCAAT/enhancer binding protein (C/EBP), alpha	19q13.11	19	NC_000019.10	33299934	33302534	minus	1	116897
# 9606	Homo sapiens	26291	0	live	FGF21		fibroblast growth factor 21	fibroblast growth factor 21	19q13.33	19	NC_000019.10	48755524	48758330	plus	4	609436
# 9606	Homo sapiens	6597	0	live	SMARCA4	BAF190, BAF190A, BRG1, CSS4, MRD16, OTSC12, RTPS2, SNF2, SNF2-beta, SNF2L4, SNF2LB, SWI2, hSNF2b	SWI/SNF related BAF chromatin remodeling complex subunit ATPase 4	transcription activator BRG1|ATP-dependent helicase SMARCA4|BRG1-associated factor 190A|BRM/SWI2-related gene 1|SNF2-like 4|SWI/SNF related, matrix associated, actin dependent regulator of chromatin, subfamily a, member 4|brahma protein-like 1|global transcription activator homologous sequence|homeotic gene regulator|mitotic growth and transcription activator|nuclear protein GRB1|protein BRG-1|protein brahma homolog 1|sucrose nonfermenting-like 4	19p13.2	19	NC_000019.10	10961030	11062273	plus	40	603254
# 9606	Homo sapiens	5300	0	live	PIN1	DOD, UBL5	peptidylprolyl cis/trans isomerase, NIMA-interacting 1	peptidyl-prolyl cis-trans isomerase NIMA-interacting 1|PPIase Pin1|parvulin PIN1|protein (peptidyl-prolyl cis/trans isomerase) NIMA-interacting 1|protein interacting with never in mitosis A1|rotamase Pin1	19p13.2	19	NC_000019.10	9835318	9849689	plus	6	601052
# 9606	Homo sapiens	5566	0	live	PRKACA	CAFD1, PKACA, PPNAD4	protein kinase cAMP-activated catalytic subunit alpha	cAMP-dependent protein kinase catalytic subunit alpha|PKA C-alpha|protein kinase A catalytic subunit|protein kinase, cAMP-dependent, alpha catalytic subunit|protein kinase, cAMP-dependent, catalytic, alpha	19p13.12	19	NC_000019.10	14091688	14117762	minus	12	601639
# 9606	Homo sapiens	7137	0	live	TNNI3	CMD1FF, CMD2A, CMH7, RCM1, TNNC1, cTnI	troponin I3, cardiac type	troponin I, cardiac muscle|cardiomyopathy, dilated 2A (autosomal recessive)|troponin I type 3 (cardiac)	19q13.42	19	NC_000019.10	55151767	55157732	minus	8	191044
# 9606	Homo sapiens	30835	0	live	CD209	CDSIGN, CLEC4L, DC-SIGN, DC-SIGN1, hDC-SIGN	CD209 molecule	CD209 antigen|C-type lectin domain family 4 member L|HIV gpl20-binding protein|dendritic cell-specific ICAM-3-grabbing non-integrin 1|dendritic cell-specific intercellular adhesion molecule-3-grabbing non-integrin|dendritic cell-specific intracellular adhesion molecules (ICAM)-3 grabbing non-integrin	19p13.2	19	NC_000019.10	7739993	7747534	minus	6	604672
# 9606	Homo sapiens	9817	0	live	KEAP1	INrf2, KLHL19	kelch like ECH associated protein 1	kelch-like ECH-associated protein 1|KEAP1 delta C|cytosolic inhibitor of Nrf2|kelch-like family member 19|kelch-like protein 19	19p13.2	19	NC_000019.10	10486125	10503356	minus	7	606016
# 9606	Homo sapiens	23476	0	live	BRD4	CAP, CDLS6, FSHRG4, HUNK1, HUNKI, MCAP	bromodomain containing 4	bromodomain-containing protein 4|chromosome-associated protein|female sterile homeotic related gene 4|mitotic chromosome-associated protein	19p13.12	19	NC_000019.10	15235519	15332539	minus	26	608749
# 9606	Homo sapiens	94025	0	live	MUC16	CA125	mucin 16, cell surface associated	mucin-16|CA125 ovarian cancer antigen|cancer antigen 125|ovarian cancer-related tumor marker CA125|ovarian carcinoma antigen CA125	19p13.2	19	NC_000019.10	8848844	9065751	minus	92	606154
# 9606	Homo sapiens	6261	0	live	RYR1	CCO, CMYO1A, CMYO1B, CMYP1A, CMYP1B, KDS, MHS, MHS1, PPP1R137, RYDR, RYR, RYR-1, SKRR	ryanodine receptor 1	ryanodine receptor 1|central core disease of muscle|protein phosphatase 1, regulatory subunit 137|ryanodine receptor 1 (skeletal)|sarcoplasmic reticulum calcium release channel|skeletal muscle calcium release channel|skeletal muscle ryanodine receptor|type 1-like ryanodine receptor	19q13.2	19	NC_000019.10	38433691	38587564	plus	106	180901
# 9606	Homo sapiens	3661	0	live	IRF3	IIAE7	interferon regulatory factor 3	interferon regulatory factor 3	19q13.33	19	NC_000019.10	49659572	49665857	minus	10	603734
# 9606	Homo sapiens	898	0	live	CCNE1	CCNE, pCCNE1	cyclin E1	G1/S-specific cyclin-E1	19q12	19	NC_000019.10	29811991	29824312	plus	12	123837
# 9606	Homo sapiens	1555	0	live	CYP2B6	CPB6, CYP2B, CYP2B7, CYP2B7P, CYPIIB6, EFVM, IIB1, P450	cytochrome P450 family 2 subfamily B member 6	cytochrome P450 2B6|1,4-cineole 2-exo-monooxygenase|cytochrome P450 IIB1|cytochrome P450, family 2, subfamily B, polypeptide 6|cytochrome P450, subfamily IIB (phenobarbital-inducible), polypeptide 6	19q13.2	19	NC_000019.10	40991282	41018398	plus	9	123930
# 9606	Homo sapiens	558	0	live	AXL	ARK3, JTK11, Tyro7, UFO, AXL	AXL receptor tyrosine kinase	tyrosine-protein kinase receptor UFO|AXL oncogene|AXL transforming sequence/gene	19q13.2	19	NC_000019.10	41219223	41261766	plus	21	109135
# 9606	Homo sapiens	407018	0	live	MIR27A	MIR27, MIRN27A, mir-27a	microRNA 27a	hsa-mir-27a	19p13.12	19	NC_000019.10	13836440	13836517	minus	1	612153
# 9606	Homo sapiens	1548	0	live	CYP2A6	CPA6, CYP2A, CYP2A3, CYPIIA6, P450C2A, P450PB	cytochrome P450 family 2 subfamily A member 6	cytochrome P450 2A6|1,4-cineole 2-exo-monooxygenase|coumarin 7-hydroxylase|cytochrome P450 IIA3|cytochrome P450(I)|cytochrome P450, family 2, subfamily A, polypeptide 6|cytochrome P450, subfamily IIA (phenobarbital-inducible), polypeptide 6|flavoprotein-linked monooxygenase|xenobiotic monooxygenase	19q13.2	19	NC_000019.10	40843541	40850447	minus	9	122720
```