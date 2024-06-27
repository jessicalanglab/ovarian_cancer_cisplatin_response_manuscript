# Ovarian cancer subtype classification

The goal of this project is to perform subtype classification, using techniques similar to [CASCAM](https://pubmed.ncbi.nlm.nih.gov/38198519/). We want to perform subtype classification on our datasets using public data sets as reference.

We have paused working on this because we were not able to effectively batch correct the public data sets in a way that left subtypes clustered.

## Datasets

### GSE189553

- Aligned to GRCh38
- The gene-level expression values (counts and TPM) were estimated by RSEM version 1.3.1 with default paramters.
- `GSE189553_raw_count_matrix.txt`: raw counts
  - Ensembl ID, gene symbol
  - HGSC_i samples are labeled SC_i
- `GSE189553_gene_TPM_matrix.txt`: TPM
- `GSE189553_series_matrix.txt`: info about samples
  - Clear cell ovarian cancer
    - CCC_i for i in [1, 11]
  - High Grade Serous cancer
    - HGSC_i for i in [1, 8]
  - Endometriod cancer
    - EC_i for i in [1, 4]

### GSE160692

- Aligned to GRCh37 (hg19)
- Normalization of reads was performed using De-Seq method in Strand
- `GSE160692_OVA_UTE_Raw_Transcripts_GEO.txt`: raw read counts
  - Entrez ID, Gene Symbol, Ensembl ID
- `GSE160692_series_matrix.txt`: info about samples
  - OVAi RNA-seq for i in 1:11
    - Ovarian clear cell carcinoma
  - UTEi RNA-seq for i in 1:5
    - Uterine clear cell carcinoma -- won't use these

### GSE157153

- Aligned to GRCh37 (hg19)
- Normalized abundance measurements for each sample, normalized via DEseq2
- `GSE157153_series_matrix.txt`: info about samples
  - note: endometriosis are noncancerous
  - endometriosis_i for i in 1:9
  - atypical endometriosis_i for i in 1:18
  - adjacent endometriosis to clear cell ovarian carcinoma_i for i in 1:7
  - adjacent endometriosis to endometrioid ovarian carcinoma_i for i in 1:3
  - clear cell ovarian carcinoma_i for i in 1:17
  - endometrioid ovarian carcinoma_i for i in 1:12
- `GSE157153_endometriosis_associated`: gene counts (normalized abundance measurements)
  - Gene symbol
- TODO: not sure if we should include this since it's already normalized. For now not including

### GSE121103

- RNA-seq aligned to GRCh38
- Read counts generated
- `GSE121103_series_matrix`: info about samples
  - Clear cell ovarian cancer
    - CCOC-1: KL01-NEBindex1_S1_R1_001
    - CCOC-2: KL02-NEBindex2_S2_R1_001
    - CCOC-3: KL03-NEBindex3_S3_R1_001
    - CCOC-4: KL04-NEBindex4_S4_R1_001
    - CCOC-5: KL05-NEBindex5_S5_R1_001
  - Endometriod ovarian cancer
    - EnOC-1: KL06-NEBindex6_S6_R1_001
    - EnOC-2: KL07-NEBindex7_S7_R1_001
    - EnOC-4: KL08-NEBindex8_S8_R1_001
    - EnOC-5: KL09-NEBindex9_S9_R1_001
  - High-grade serous ovarian cancer
    - HGSOC-1: KL10-NEBindex10_S10_R1_001
    - HGSOC-2: KL11-NEBindex11_S11_R1_001
    - HGSOC-3: KL12-NEBindex12_S12_R1_001
    - HGSOC-4: KL13-NEBindex13_S13_R1_001
    - HGSOC-5: KL14-NEBindex14_S14_R1_001
  - Mucinous ovarian cancer
    - MOC-1: KL15-NEBindex15_S15_R1_001
    - MOC-2: KL15-NEBindex16_S16_R1_001
    - MOC-3: KL15-NEBindex17_S18_R1_001
    - MOC-4: KL15-NEBindex18_S19_R1_001
    - MOC-5: KL15-NEBindex20_S19_R1_001
- `GSE121103__counts.txt`: gene counts (read counts)
  - Geneid in ENSG format

### GSE101108

- Aligned with GRCh37/hg19
- Raw read counts
- `GSE101108_series_matrix.txt`
  - Tumor_OV106
  - Tumor_OV131
  - Tumor_OV135
  - Tumor_OV151
  - Tumor_OV152
  - Tumor_OV155
  - Tumor_OV162
  - Tumor_OV163
  - Tumor_OV169
  - Tumor_OV170
  - Tumor_OV172
  - Tumor_OV177
  - Tumor_OV178
  - Tumor_OV185
  - Tumor_OV188
  - Tumor_OVi for i in [201, 207]
  - Tumor_OV301
  - Tumor_OVi for i in [303, 315]
  - Tumor_OV317
  - Tumor_OV318
  - Tumor_OV321
  - Tumor_OVi for i in [323, 329]
  - Tumor_OVi for i in [331, 333]
  - Tumor_OVi for i in [335, 349]
  - Tumor_OV352
  - Tumor_OV353
  - Tumor_OVi for i in [355, 360]
  - Tumor_OVi for i in [362, 366]
  - Tumor_OV368
  - Tumor_OVi for i in [370, 373]
  - Tumor_OVi for i in [375, 378]
  - Tumor_OV380
  - Tumor_OVi for i in [382, 385]
  - Tumor_OVi for i in [387, 391]
- `GSE101108_OV106-391_counts`: raw reads
  - ENSG format for gene name
- `GSE101108-26225-1014527-1-SP.xlsx`: labeled with histotypes
  - Downloaded from Supplementary table 3 of [their paper](https://www-ncbi-nlm-nih-gov.ezproxy.library.wisc.edu/pmc/articles/PMC6205557/#SD6)

### EGAD00001006441

- In FASTQ format
  - Align to human genome using `src/preprocessing/run_rnaseq_EGAD_data.ipynb`
- `delimited_maps/Run_Sample_meta_info`: ID associated with histotype
  - All are LGSC

### TCGA dataset (Ovarian cancer)

- Downloaded ["HTSeq - Counts" for ovarian cancer](https://xenabrowser.net/datapages/?cohort=GDC%20TCGA%20Ovarian%20Cancer%20(OV)&removeHub=https%3A%2F%2Fxena.treehouse.gi.ucsc.edu%3A443) from Xena Browser
- `TCGA-OV.htseq_counts.tsv`: RNAseq data
  - log2(count+1)
  - Ensembl ID
  - Sample labels of the form `TCGA-23-1022-01A`
- Types present:
  - cystadenocarcinoma, nos 1
  - papillary serous cystadenocarcinoma 4
  - serous cystadenocarcinoma, nos 417
  - Just using the serous cystadenocarcinoma since we have enough of them
- Sample considered an HGSC candidate if it's a TP53 mutant (including deletions) and not a KRAS mutant (including deletions)
  - TP53 is correlated with HGSC and KRAS is correlated with LGSC
- Data cleanup and subsetting performed in `src/preprocessing/scrape_tcga_data.ipynb`

### TCGA dataset (All cancers)

- Downloaded each GDC TCGA dataset from [Xena Browser datasets](https://xenabrowser.net/datapages/)
- Formatting is the same as the OV TCGA dataset

### CCLE dataset

TODO: Should I be including the CCLE dataset from DepMap?
No, not confident in their classification. But could use for testing if we can classify

### Our dataset

TODO: bring in our datasets (30 something celllines)

## Preprocessing

- Keep genes found only in GRCh38 and GrCh37 (hg19)
  - Create this list using `src/preprocessing/merge_grch38_grch37.ipynb`
- Format data consistently using `src/preprocessing/format_rnaseq_data.ipynb`

## Batch correction

- Boxplots show strong batch effects
- UMAP also shows strong effects

### pyComBat

- We use pyComBat for batch correction between datasets from different labs
  - Attempted to use [inmoose version](https://github.com/epigenelabs/inmoose/) since pycombat says that it is deprecated in favor of this, but it did not do a good job correcting the batch effects (according to UMAP and boxplots), so used deprecated [pycombat](https://github.com/epigenelabs/pyComBat)
- Using log transform expression as input based on [this paper](https://www.biorxiv.org/content/10.1101/2020.03.17.995431v2.full): "However, a prior log-transformation of the data is necessary to use ComBat." But it is poorly documented.
- Pycombat resulted in negative expression values in the corrected data, which I changed to 0. This appears to be a [known issue](https://github.com/jtleek/sva-devel/issues/37)
- Batch effects accounted for by pycombat

- Tried running pyComBat using all of the TCGA tumor data (non-ovarian cancers included) in the hopes that this would prevent batch correcting from really just correcting for subtype differences since each subtype is largely from a different dataset. This did not cluster by subtype any better than when using only ovarian cancer tumors.

### Celligner

- Celligner normalization for batch correction between celllines and tumors was successful in [this CASCAM paper](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011754#sec011)
  - Many issues with celligner import in python (tried on Mac, Linux, and Windows) and could not get celligner to work effectively
- TODO: Try aligning with Celligner's pre-made alignment based on full TCGA and cellline cancer dataset (as in CASCAM)

## Differential expression

- Differential expression analysis was performed to support feature selection to reduce the number of genes under consideration by our SVM
  - DESeq usually expects replicates, which we don't have in the standard sense
  - Can't use [pydeseq2](https://pydeseq2.readthedocs.io/en/latest/auto_examples/plot_minimal_pydeseq2_pipeline.html#sphx-glr-auto-examples-plot-minimal-pydeseq2-pipeline-py) since it doesn't have LRT implemented, so using R
- Note that even after selecting differential genes, UMAP does not show strong clustering by type

## Subtype prediction

- Attempted to build a model to predict subtype using `src/subtype_prediction/svm_subtype_prediction.ipynb`
  - Tried with and without feature selection
  - Tried with and without stratification
    - Does not perform well across all categories
