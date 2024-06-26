# To be run from the src folder

# Only make directory if it doesn't already exist
function mkdir_safe() {
    local directory=$1
    if [ ! -d "$directory" ]; then
        mkdir "$directory"
    fi
}

# Assumes this is being run on a Mac with the research drive loaded. Adjust path as necessary
rd_path="/Volumes/kueck"
project_rd_path="$rd_path/Pipeline/CellLines/RNAseq/220829_VL00320_AAC7WHVM5_AAC5JYKM5_AAC5K32M5"

# Copy star salmon output
mkdir_safe "../data/rnaseq_output"
star_salmon_local_folder="../data/rnaseq_output/star_salmon"
mkdir_safe $star_salmon_local_folder
star_salmon_rd_path="$project_rd_path/star_salmon/salmon.merged.gene_counts.tsv"
cp "$star_salmon_rd_path" "$star_salmon_local_folder"
star_salmon_rd_path="$project_rd_path/star_salmon/salmon.merged.gene_tpm.tsv"
cp "$star_salmon_rd_path" "$star_salmon_local_folder"

# Copy metadata for HGSC lines
metadata_HGSC_rd_path="$project_rd_path/SecondaryAnalysis/metadataHGSC.xlsx"
metadata_HGSC_local_folder="deseq/metadata"
cp "$metadata_HGSC_rd_path" "$metadata_HGSC_local_folder"
mv "$metadata_HGSC_local_folder/metadataHGSC.xlsx" "$metadata_HGSC_local_folder/metadata_HGSC.xlsx"

# Create deseq data folders
mkdir_safe "../data/deseq"
mkdir_safe "../data/deseq/Rdata"
mkdir_safe "../data/deseq/output"