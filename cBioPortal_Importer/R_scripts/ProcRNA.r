#!/usr/bin/env Rscript

library(CNTools)


args = commandArgs(trailingOnly=TRUE)

# get parameters
gepfile=args[1]
enscon=args[2]
genelist=args[3]
outdir=args[4]


# preprocess function
preProcRNA <- function(gepfile, enscon, genelist = NULL){
 
 # check if genelist is None when preProcRNA.r is calls by pycbio.py and genelist is omitted
 if (genelist == "None") {
     genelist = NULL
     print("genelist is not used during RNA processing")
 } else {
 print("genelist is used during RNA processing") 
 }
 
 # read in data
 gepData <- read.csv(gepfile, sep="\t", header=TRUE, check.names=FALSE)
 ensConv <- read.csv(enscon, sep="\t", header=FALSE)

 # rename columns
 colnames(ensConv) <- c("gene_id", "Hugo_Symbol")

 # merge in Hugo's, re-order columns, deduplicate
 df <- merge(x=gepData, y=ensConv, by="gene_id", all.x=TRUE)
 df <- subset(df[,c(ncol(df),2:(ncol(df)-1))], !duplicated(df[,c(ncol(df),2:(ncol(df)-1))][,1]))
 row.names(df) <- df[,1]
 df <- df[,-1]

 # subset if gene list given
 if (!is.null(genelist)) {
	keep_genes <- readLines(genelist)
	df <- df[row.names(df) %in% keep_genes,]
 }

 # return the data frame
 return(df)
}

# simple zscore function
compZ <- function(df) {

 # scale row-wise
 df_zscore <- t(scale(t(df)))

 # NaN (when SD is 0) becomes 0
 df_zscore[is.nan(df_zscore)] <- 0

 # we want a dataframe
 df_zscore <- data.frame(signif(df_zscore, digits=4), check.names=FALSE)

 return(df_zscore)
}


# make subdirectories
cbiodir <- paste0(outdir, "/cbioportal_import_data")
suppdir <- paste0(outdir, "/supplementary_data")

print("Processing RNASEQ data")

# get list of samples in study
study_samples <- readLines(paste0(outdir, "/gep_study.list"))

# preprocess the full data frame
df <- preProcRNA(gepfile, enscon, genelist)

print("getting STUDY-level data")

# subset data to STUDY level data for cbioportal
df_study <- df[study_samples]

# write the raw STUDY data
write.table(data.frame(Hugo_Symbol=rownames(df_study), df_study, check.names=FALSE),
         file=paste0(cbiodir, "/data_expression.txt"), sep="\t", row.names=FALSE, quote=FALSE)

# z-scores STUDY
df_zscore <- compZ(df_study) # z-score
write.table(data.frame(Hugo_Symbol=rownames(df_zscore), df_zscore, check.names=FALSE),
        file=paste0(cbiodir, "/data_expression_zscores.txt"), sep="\t", row.names=FALSE, quote=FALSE)

