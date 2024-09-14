#!/usr/bin/env Rscript

library(CNTools)


args = commandArgs(trailingOnly=TRUE)

# get parameters
fusfile=args[1]
entcon=args[2]
minfusionreads=args[3]
outdir=args[4]

preProcFus <- function(datafile, readfilt, entrfile){

 # function to split and take max value from list of columns
 split_column_take_max <- function(df, columns) {
  for (column in columns) {
   splitup <- as.data.frame(do.call(rbind, strsplit(as.character(df[[column]]), ';')), stringsAsFactors=FALSE)
   splitup[splitup=="None"] <- 0
   splitup[1:ncol(splitup)] <- sapply(splitup[1:ncol(splitup)], as.numeric)
   bspot<-which(names(df)==column)
   df[[column]] <- apply(splitup, 1, max)
  }
   return(df)
 }

 # testing
 #datafile <- "input.fus.txt"
 #entrfile <- "entrez_conversion.txt"
 #readfilt=20

 print("--- reading fusion data ---")
 data <- read.csv(datafile, sep="\t", header=TRUE, check.names=FALSE, stringsAsFactors=FALSE)
 entr <- read.csv(entrfile, sep="\t", header=TRUE, check.names=FALSE, stringsAsFactors=FALSE)

 # reformat the filtering columns to split and take the max value within cell
 columns <- c("contig_remapped_reads", "flanking_pairs", "break1_split_reads", "break2_split_reads", "linking_split_reads")
 data <- split_column_take_max(data, columns)

 # add a column which pulls the correct read support columns
 data$read_support <- ifelse(data$call_method == "contig", data$contig_remapped_reads,
                        ifelse(data$call_method == "flanking reads", data$flanking_pairs,
                             ifelse(data$call_method == "split reads", data$break1_split_reads + data$break2_split_reads + data$linking_split_reads, 0)
                           )
                               )

 # filter by minimum read support
 data <- data[data$read_support > readfilt, ]

 # sort descending read support
 data <- data[order(-data$read_support), ]

 # get unique fusions for each sample
 data$fusion_tuples <- apply(data[, c("gene1_aliases", "gene2_aliases")], 1, function(x) paste0(sort(x), collapse = "-"))

 # add index which is sample, tuple
 data$index <- paste0(data$Sample, data$fusion_tuples)

 # deduplicate
 data_dedup <- data[!duplicated(data$index),]

 # gene1 should not equal gene2
 data_dedup <- data_dedup[data_dedup$gene1_aliases != data_dedup$gene2_aliases, ]

 # merge in entrez gene ids
 data_dedup <- merge(data_dedup, entr, by.x="gene1_aliases", by.y="Hugo_Symbol", all.x=TRUE)
 data_dedup <- merge(data_dedup, entr, by.x="gene2_aliases", by.y="Hugo_Symbol", all.x=TRUE)

 # add some missing columns
 data_dedup$DNA_support <- "no"
 data_dedup$RNA_support <- "yes"
 data_dedup$Center <- "TGL"
 data_dedup$Frame <- "frameshift"
 data_dedup$Fusion_Status <- "unknown"

 # write out the nice header
 header <- c("Hugo_Symbol", "Entrez_Gene_Id", "Center", "Tumor_Sample_Barcode", "Fusion", "DNA_support", "RNA_support", "Method", "Frame", "Fusion_Status")

 # get left gene data
 columns_left <- c("gene1_aliases", "Entrez_Gene_Id.x", "Center", "Sample", "fusion_tuples", "DNA_support", "RNA_support", "tools", "Frame", "Fusion_Status")
 data_left <- data_dedup[columns_left]
 colnames(data_left) <- header

 # get right gene data
 columns_right <- c("gene2_aliases", "Entrez_Gene_Id.y", "Center", "Sample", "fusion_tuples", "DNA_support", "RNA_support", "tools", "Frame", "Fusion_Status")
 data_right <- data_dedup[columns_right]
 colnames(data_right) <- header

 # append it all together
 df_cbio <- rbind(data_left, data_right)

 # remove rows where gene is not known (this still keeps the side of the gene which is known)
 df_cbio <- df_cbio[complete.cases(df_cbio),]

 return(df_cbio)

 }




# make subdirectories
cbiodir <- paste0(outdir, "/cbioportal_import_data")
suppdir <- paste0(outdir, "/supplementary_data")

# function returns list of 3 objects ### TO WRITE
fusion_cbio <- preProcFus(fusfile, minfusionreads, entcon)

# write FUS files
print("writing fus file")
write.table(fusion_cbio, file=paste0(cbiodir, "/data_fusions.txt"), sep="\t", row.names=FALSE, quote=FALSE)

