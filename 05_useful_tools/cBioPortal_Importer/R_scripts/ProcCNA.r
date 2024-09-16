#!/usr/bin/env Rscript

library(CNTools)

args = commandArgs(trailingOnly=TRUE)

# Set thresholds
segfile=args[1]
genebed=args[2]
genelist=args[3]
oncolist = args[4]
gain=as.numeric(args[5])
amp=as.numeric(args[6])
htz=as.numeric(args[7])
hmz=as.numeric(args[8])
outdir=args[9]

preProcCNA <- function(segfile, genebed, gain, amp, htz, hmz, oncolist, genelist = NULL){

 # check if genelist is None when preProcCNA.r is calls by pycbio.py and genelist is omitted
 if (genelist == "None") {
     genelist = NULL
     print("genelist is not used during CNA processing")
 } else {
 print("genelist is used during CNA processing") 
 }
 
 # read oncogenes
 oncogenes <- read.delim(oncolist, header=TRUE, row.names=1)

 ## small fix segmentation data
 segData <- read.delim(segfile, header=TRUE) # segmented data already
 segData$chrom <- gsub("chr", "", segData$chrom)

 # thresholds
 print("setting thresholds")
 gain=as.numeric(gain)
 amp=as.numeric(amp)
 htz=as.numeric(htz)
 hmz=as.numeric(hmz)

 # get the gene info
 print("getting gene info")
 geneInfo <- read.delim(genebed, sep="\t", header=TRUE)

 # make CN matrix gene level
 print("converting seg")
 cnseg <- CNSeg(segData)
 print("get segmentation by gene")
 rdByGene <- getRS(cnseg, by="gene", imput=FALSE, XY=FALSE, geneMap=geneInfo, what="median",  mapChrom = "chrom", mapStart = "start", mapEnd = "end")
 print("get reduced segmentation data")
 reducedseg <- rs(rdByGene)

 # some reformatting and return log2cna data
 df_cna <- subset(reducedseg[,c(5, 6:ncol(reducedseg))], !duplicated(reducedseg[,c(5, 6:ncol(reducedseg))][,1]))
 colnames(df_cna) <- c("Hugo_Symbol", colnames(df_cna)[2:ncol(df_cna)])

 # set thresholds and return 5-state matrix
 print("thresholding cnas")
 df_cna_thresh <- df_cna
 df_cna_thresh[,c(2:ncol(df_cna))] <- sapply(df_cna_thresh[,c(2:ncol(df_cna))], as.numeric)

 # threshold data
 for (i in 2:ncol(df_cna_thresh))
 {
     df_cna_thresh[,i] <- ifelse(df_cna_thresh[,i] > amp, 2,
                         ifelse(df_cna_thresh[,i] < hmz, -2,
                             ifelse(df_cna_thresh[,i] > gain & df_cna_thresh[,i] <= amp, 1,
                                 ifelse(df_cna_thresh[,i] < htz & df_cna_thresh[,i] >= hmz, -1, 0)
                           )
                               )
                                   )
 }

 # fix rownames of log2cna data
 rownames(df_cna) <- df_cna$Hugo_Symbol
 df_cna$Hugo_Symbol <- NULL
 df_cna <- signif(df_cna, digits=4)

 # fix rownames of thresholded data
 row.names(df_cna_thresh) <- df_cna_thresh[,1]
 df_cna_thresh <- df_cna_thresh[,-1] # matrix where row names are genes, samples are columns

 # subset of oncoKB genes
 df_cna_thresh_onco <- df_cna_thresh[row.names(df_cna_thresh) %in% rownames(oncogenes),]

 # subset if gene list given
 if (!is.null(genelist)) {
    keep_genes <- readLines(genelist)
    df_cna <- df_cna[row.names(df_cna) %in% keep_genes,]
    df_cna_thresh <- df_cna_thresh[row.names(df_cna_thresh) %in% keep_genes,]
 }

 # return the list of dfs
 CNAs=list()
 CNAs[[1]] <- segData
 CNAs[[2]] <- df_cna
 CNAs[[3]] <- df_cna_thresh
 return(CNAs)

}


# make subdirectories
cbiodir <- paste0(outdir, "/cbioportal_import_data")
suppdir <- paste0(outdir, "/supplementary_data")

print("Processing CNA data")

# function returns list of 3 objects
CNAs <- preProcCNA(segfile, genebed, gain, amp, htz, hmz, oncolist, genelist)

# write cbio files
print("writing seg file")
write.table(CNAs[[1]], file=paste0(cbiodir, "/data_segments.txt"), sep="\t", row.names=FALSE, quote=FALSE)
write.table(data.frame("Hugo_Symbol"=rownames(CNAs[[2]]), CNAs[[2]], check.names=FALSE),
  file=paste0(cbiodir, "/data_log2CNA.txt"), sep="\t", row.names=FALSE, quote=FALSE)
write.table(data.frame("Hugo_Symbol"=rownames(CNAs[[3]]), CNAs[[3]], check.names=FALSE),
  file=paste0(cbiodir, "/data_CNA.txt"), sep="\t", row.names=FALSE, quote=FALSE)

# write the truncated data_CNA file (remove genes which are all zero) for oncoKB annotator
df_CNA <- CNAs[[3]][apply(CNAs[[3]], 1, function(row) !all(row == 0 )),]
write.table(data.frame("Hugo_Symbol"=rownames(df_CNA), df_CNA, check.names=FALSE),
  file=paste0(suppdir, "/data_CNA_short.txt"), sep="\t", row.names=FALSE, quote=FALSE)



