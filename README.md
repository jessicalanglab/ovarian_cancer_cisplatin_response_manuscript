# Data analysis for cisplatin response in ovarian cancer manuscript

This repository contains the code used in the data analysis presented in our manuscript [TODO: add link to manuscript]. It contains the analysis of two separate datasets, detailed below:

## RNAseq data of HGSC ovarian cancer cell lines

Dataset tag: `220829_VL00320_AAC7WHVM5_AAC5JYKM5_AAC5K32M5`

### Differential gene expression analysis

#### IC50 vs categorical sensitivity

We performed DESeq analysis and gene ontology using IC50 as our variable of interest as well as using categorical assigned sensitivity ratings. The gene ontology yielded more significant results for the categorical analysis, which fits with our understanding that the cell lines are either resistant or not based on certain mechanisms of resistance; the differences in IC50 values between cell lines in the same category thus adds noise to the data.

- [Categorical deseq analysis](220829_VL00320_AAC7WHVM5_AAC5JYKM5_AAC5K32M5_analysis/src/deseq/deseq_analysis_hgsc.Rmd)
- [Additional plots from categorical deseq analysis](220829_VL00320_AAC7WHVM5_AAC5JYKM5_AAC5K32M5_analysis/src/deseq/deseq_platinum_sensitivity_plots.Rmd)
- [IC50 deseq analysis](220829_VL00320_AAC7WHVM5_AAC5JYKM5_AAC5K32M5_analysis/src/deseq/deseq_analysis_hgsc_IC50.Rmd)

#### Partial HGSC data set

To remove confounding variables due to isogenic cell lines existing in this dataset, we recomputed the DESeq analysis using the same dataset, but excluding PEO4, PEO6, and PEA1. Out of the isolines PEA and PEO, only PEO1 and PEA2 remain. Which cell lines to remove from each isogenic line were chosen randomly.

- [Partial dataset deseq analysis](220829_VL00320_AAC7WHVM5_AAC5JYKM5_AAC5K32M5_analysis/src/deseq/deseq_analysis_hgsc-subset.Rmd)

### Comparison to known pathways of cisplatin resistance

We scraped known mechanisms of resistance from [Huang et al, 2021](https://www.nature.com/articles/s41388-021-02055-2#Sec39) Supplemental Table 1. We then compared these known mechanisms of resistance to our differential gene expression results.

- [Comparison to known pathways of resistance](220829_VL00320_AAC7WHVM5_AAC5JYKM5_AAC5K32M5_analysis/src/deseq/known_pathways/prev_literature_resistance_mechanisms.ipynb)

## RNAseq data for 4 isogenic cell lines

Dataset tag: `230324-3way-merge`

### Differential gene expression analysis

For each sensitive-resistant pair of cell lines, DEseq was used to determine genes that were differentially expressed in the resistant cell line as compared to its sensitive counterpart. Gene ontology was performed on these differential genes. We used parameterized Rmd notebooks, in which a generic Rmd file is launched from the original Rmd file, resulting in a generated notebook per sensitive-resistant pair.

- [deseq analysis (single sensitive-resistant pair)](230324-3way-merge_analysis/src/deseq/single-cellline-vs-control.Rmd)
- [deseq analysis (launches each sensitive-resistant pair)](230324-3way-merge_analysis/src/deseq/deseq-analysis.Rmd)
- [deseq analysis (generated notebooks per sensitive-resistant pair)](/Users/Ryan/Projects/ovarian_cancer_cisplatin_response_manuscript/230324-3way-merge_analysis/src/deseq/generated-notebooks)

### Comparison to known pathways of cisplatin resistance

We scraped known mechanisms of resistance from [Huang et al, 2021](https://www.nature.com/articles/s41388-021-02055-2#Sec39) Supplemental Table 1. We then compared these known mechanisms of resistance to our differential gene expression results.

- [Comparison to known pathways of resistance](230324-3way-merge_analysis/src/deseq/specific-pathways/prev_literature_resistance_mechanisms.ipynb)

### Visualizing differential expression for specific sets of genes

We also visualized the differential expression results for specific interesting sets of genes.

- [Differential expression in stemness genes](230324-3way-merge_analysis/src/deseq/specific-pathways/Stemness.Rmd)
- [Differential expression in mitochondrial genes](Users/Ryan/Projects/ovarian_cancer_cisplatin_response_manuscript/230324-3way-merge_analysis/src/deseq/specific-pathways/mitochondrial-genes.Rmd)
- [Differential expression in platinum efflux/influx genes](/Users/Ryan/Projects/ovarian_cancer_cisplatin_response_manuscript/230324-3way-merge_analysis/src/deseq/specific-pathways/PlatinumEffluxInflux.Rmd)

### Identifying potential TF regulators of DEGs

We used MAGIC, a tool presented in [Roopra, 2020](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007800) in order to identify TFs that have increased binding at the promotors of our differentially expressed genes. We ran MAGIC for each sensitive-resistant cell line pair. We used parameterized Rmd notebooks, in which a generic Rmd file is launched from the original Rmd file, resulting in a generated notebook per sensitive-resistant pair.

- [MAGIC analysis (launches each sensitive-resistant pair)](230324-3way-merge_analysis/src/magic/magic-analysis.Rmd)
- [MAGIC analysis (single sensitive-resistant pair)](230324-3way-merge_analysis/src/magic/single-sensitive-resistant-pair-magic-analysis.Rmd)
- [MAGIC analysis (generated notebooks per sensitive-resistant pair)](230324-3way-merge_analysis/src/magic/generated-notebooks)