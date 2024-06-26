library(stringr)

# this is specific to run 230324-3way-merge
# Expects a run id, a path to an input file
# The input file should have format of a salmon.merged.gene_counts.tsv file
# ----------
create_rna_seq_sample_file <- function() {
    # parse input
    # args <- commandArgs(trailingOnly = TRUE)
    # if (length(args) != 3) {
    #     stop("Please provide a run id, a path to an input file", call. = FALSE)
    # }
    # run_id <- args[1]
    # input_file <- args[2]
    run_id <- "230324-3way-merge"
    input_file <- "../../star_salmon/salmon.merged.gene_counts.tsv"
    # data frame to store our metadata
    output_table <- data.frame(
        ShortName = character(),
        IsoLine = character(),
        CellLine = character(),
        Replicate = character(),
        LongName = character(),
        IsogenicRank = character()
    )

    # verify input file exists
    if (!file.exists(input_file)) {
        stop("Input file does not exist")
    }
    input_table <- as.data.frame(read.table(input_file, sep = "\t", header = FALSE))
    # read input file and verify that the input file has the proper format
    for (i in 3:ncol(input_table)) {
        sample_name <- input_table[1, i]
        
        # Read in isogenic line
        iso_line <- ""
        if (str_detect(sample_name, "PEO")) {
          iso_line <- "PEO"
        } else if (str_detect(sample_name, "PEA")) {
          iso_line <- "PEA"
        } else if (str_detect(sample_name, "OVCAR3")) {
          iso_line <- "OVCAR3"
        } else if (str_detect(sample_name, "OVCAR4")) {
          iso_line <- "OVCAR4"
        } else {
          stop(str_interp("No isogenic line properly specified in ${sample_name}"))
        }
        
        # Read in cell line
        cell_line <- ""
        if (str_detect(sample_name, "PEO1")) {
            cell_line <- "PEO1"
            isogenic_rank <- 1
        } else if (str_detect(sample_name, "PEO4")) {
            cell_line <- "PEO4"
            isogenic_rank <- 2
        } else if (str_detect(sample_name, "PEO6")) {
          cell_line <- "PEO6"
          isogenic_rank <- 3
        } else if (str_detect(sample_name, "PEA1")) {
            cell_line <- "PEA1"
            isogenic_rank <- 1
        } else if (str_detect(sample_name, "PEA2")) {
            cell_line <- "PEA2"
            isogenic_rank <- 2
        } else if (str_detect(sample_name, "OVCAR3_")) {
            cell_line <- "OVCAR3"
            isogenic_rank <- 1
        } else if (str_detect(sample_name, "OVCAR3ResA")) {
            cell_line <- "OVCAR3A"
            isogenic_rank <- 2
        } else if (str_detect(sample_name, "OVCAR3ResB")) {
            cell_line <- "OVCAR3B"
            isogenic_rank <- 3
        } else if (str_detect(sample_name, "OVCAR4_")) {
            cell_line <- "OVCAR4"
            isogenic_rank <- 1
        } else if (str_detect(sample_name, "OVCAR4ResA")) {
            cell_line <- "OVCAR4A"
            isogenic_rank <- 2
        } else if (str_detect(sample_name, "OVCAR4ResB")) {
            cell_line <- "OVCAR4B"
            isogenic_rank <- 3
        } else {
            stop(str_interp("No cell line properly specified in ${sample_name}"))
        }

        # Replicate Number
        replicate <- -1
        if (str_detect(sample_name, regex("rep."))) {
            replicate_string <- substr(sample_name, nchar(sample_name), nchar(sample_name))
            replicate <- as.numeric(replicate_string)
        } else {
            stop(str_interp("Replicate number unclear for ${sample_name}"))
        }
        short_name <- str_interp("${cell_line}_R${replicate}")

        # write to output metadata table
        next_out_row_index <- nrow(output_table) + 1
        output_table[next_out_row_index, ] <- list(
            short_name,
            iso_line,
            cell_line,
            replicate,
            sample_name,
            isogenic_rank,
        )
    }

    # Create output structure
    # output_folder_top_level <- str_interp("/project/rnaseq/${run_id}/analysis/")
    # if (!file.exists(output_folder_top_level)) {
    #     dir.create(output_folder_top_level)
    # }
    # output_folder <- str_interp("${output_folder_top_level}/deseq")
    # if (!file.exists(output_folder)) {
    #     dir.create(output_folder)
    # }
    # output_path <- str_interp("${output_folder}/metadata.csv")
    output_path <- "metadata.csv"

    write.table(output_table,
        file = output_path, sep = ",",
        row.names = FALSE, col.names = TRUE, quote = FALSE
    )

    print(str_interp(str_interp("Wrote metadata to ${output_path}")))
}

create_rna_seq_sample_file()
