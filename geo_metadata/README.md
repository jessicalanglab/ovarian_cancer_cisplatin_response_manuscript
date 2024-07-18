# Data used for analysis of cisplatin response in ovarian cancer manuscript

For each experiment, these python notebooks combine the fastq files of the 3 sequencing runs used by creating a symbolic link to the file. Also saves the path names and MD5 checksums so it can be easily copied into the GEO metadata.

Note: This makes symbolic links from the new fastq file names to the original file. Will need to make sure that GEO uploads these properly.

## RNAseq data of HGSC ovarian cancer cell lines

Path to RNAseq output: `/Volumes/kueck/Pipeline/CellLines/RNAseq/220829_VL00320_AAC7WHVM5_AAC5JYKM5_AAC5K32M5`

3 sequencing runs used:

- `/Volumes/kueck/FASTQ/CellLines/RNA-Seq/220824_VL00320_14_AAC7WHVM5`
  - Tagged as `Run220824`
- `/Volumes/kueck/FASTQ/CellLines/RNA-Seq/220825_VL00320_15_AAC5JYKM5`
  - Tagged as `Run220825`
- `/Volumes/kueck/FASTQ/CellLines/RNA-Seq/220826_VL00320_16_AAC5K32M5`
  - Tagged as `Run220826`

## RNAseq data for 4 isogenic cell lines

Path to RNAseq output: `/Volumes/kueck/Pipeline/CellLines/RNAseq/230324-3way-merge`

3 sequencing runs used:

- `230316_VL00320_43_AACJYMYM5`
  - Tagged as `Run230316`
- `230322_VL00320_45_AACJYNCM`
  - Tagged as `Run230322`
- `230323_run`
  - Tagged as `Run230323`
