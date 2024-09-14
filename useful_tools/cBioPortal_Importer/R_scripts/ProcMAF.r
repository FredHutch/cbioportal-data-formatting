#!/usr/bin/env Rscript

library(CNTools)
library(deconstructSigs)

args = commandArgs(trailingOnly=TRUE)

# Get parameters
maffile=args[1]
tglpipe=args[2]
outdir=args[3]


        
addVAFtoMAF <- function(maf_df, alt_col, dep_col, vaf_header) {

 # print a warning if any values are missing (shouldn't happen), but change them to 0
 if(anyNA(maf_df[[alt_col]]) || anyNA(maf_df[[dep_col]])) {
    print("Warning! Missing values found in one of the count columns")
    maf_df[[alt_col]][is.na(maf_df[[alt_col]])] <- 0
    maf_df[[dep_col]][is.na(maf_df[[dep_col]])] <- 0
 }

 # ensure factors end up as numeric
 maf_df[[alt_col]] <- as.numeric(as.character(maf_df[[alt_col]]))
 maf_df[[dep_col]] <- as.numeric(as.character(maf_df[[dep_col]]))
 
 # ensure position comes after alternate count field
 bspot                  <- which(names(maf_df)==alt_col)
 maf_df                 <- data.frame(maf_df[1:bspot], vaf_temp=maf_df[[alt_col]]/maf_df[[dep_col]], maf_df[(bspot+1):ncol(maf_df)], check.names=FALSE)
 names(maf_df)[bspot+1] <- vaf_header

 # check for any NAs
 if(anyNA(maf_df[[vaf_header]])) {
    print("Warning! There are missing values in the new vaf column")
    maf_df[[vaf_header]][is.na(maf_df[[vaf_header]])] <- 0
 }

 return(maf_df)
}

procVEP <- function(datafile){

 print("--- reading data ---")
 data <- read.csv(datafile, sep="\t", header=TRUE, check.names=FALSE, stringsAsFactors=FALSE)

 print("--- doing some formatting ---")

 # add vaf columns
 print("add tumor_vaf")
 data <- addVAFtoMAF(data, "t_alt_count", "t_depth", "tumor_vaf")
 print("add normal_vaf")
 data <- addVAFtoMAF(data, "n_alt_count", "n_depth", "normal_vaf")

 # clear memory (important when the mafs are huge - will maybe outgrow R if files are millions and millions of lines)
 df_anno <- data
 gc()
 
 # add oncogenic yes or no columns
 print("add oncogenic status")
 df_anno <- transform(df_anno,
    oncogenic_binary = ifelse(oncogenic == "Oncogenic" | oncogenic == "Likely Oncogenic",
                        "YES", "NO")
 )

 # add common_variant yes or no columns
 print("add common variant status")
 df_anno <- transform(df_anno,
    ExAC_common = ifelse(grepl("common_variant", df_anno$FILTER),
                        "YES", "NO")
 )

 # add POPMAX yes or no columns
 print("add population level frequency")
 gnomad_cols <- c("gnomAD_AFR_AF", "gnomAD_AMR_AF", "gnomAD_ASJ_AF", "gnomAD_EAS_AF", "gnomAD_FIN_AF", "gnomAD_NFE_AF", "gnomAD_OTH_AF", "gnomAD_SAS_AF")
 df_anno[gnomad_cols][is.na(df_anno[gnomad_cols])] <- 0
 df_anno[, "gnomAD_AF_POPMAX"] <- apply(df_anno[gnomad_cols], 1, max)


 # caller artifact filters
 print("apply filters")
 df_anno$FILTER <- gsub("^clustered_events$",
                        "PASS",
                        df_anno$FILTER)

 df_anno$FILTER <- gsub("^common_variant$",
                        "PASS",
                        df_anno$FILTER)

 df_anno$FILTER <- gsub(".",
                        "PASS",
                        df_anno$FILTER,
                        fixed=TRUE)

 # some specific filter flags should be rescued if oncogenic (ie. EGFR had issues here)
 print("rescue filter flags if oncogenic")
 df_anno <- transform(df_anno,
  FILTER = ifelse(oncogenic_binary == "YES" &
                 (FILTER == "triallelic_site" | 
                  FILTER == "clustered_events;triallelic_site" |
                  FILTER == "clustered_events;homologous_mapping_event"),
                  "PASS", df_anno$FILTER)
 )

 # Artifact Filter
 print("artifact filter")
 df_anno <- transform(df_anno,
  TGL_FILTER_ARTIFACT = ifelse(FILTER == "PASS",
                      "PASS", "Artifact")
 )

 # ExAC Filter
 print("exac filter")
 df_anno <- transform(df_anno,
  TGL_FILTER_ExAC = ifelse(ExAC_common == "YES" & Matched_Norm_Sample_Barcode == "unmatched",
                      "ExAC_common", "PASS")
 )

 # gnomAD_AF_POPMAX Filter
 print("population frequency filter")
 df_anno <- transform(df_anno,
  TGL_FILTER_gnomAD = ifelse(gnomAD_AF_POPMAX > 0.001 & Matched_Norm_Sample_Barcode == "unmatched",
                      "gnomAD_common", "PASS")
 )

 # VAF Filter
 print("VAF filter")
 df_anno <- transform(df_anno,
  TGL_FILTER_VAF = ifelse(tumor_vaf >= 0.1 | (tumor_vaf < 0.1 & oncogenic_binary == "YES" & ((Variant_Classification == "In_Frame_Del" | Variant_Classification == "In_Frame_Ins") | (Variant_Type == "SNP"))),
                      "PASS", "low_VAF")
 )


 # Mark filters
 print("Mark filters")
 df_anno <- transform(df_anno,
  TGL_FILTER_VERDICT = ifelse(TGL_FILTER_ARTIFACT == "PASS" & TGL_FILTER_ExAC == "PASS" & TGL_FILTER_gnomAD == "PASS" & TGL_FILTER_VAF == "PASS",
                      "PASS",
                       paste(df_anno$TGL_FILTER_ARTIFACT, df_anno$TGL_FILTER_ExAC, TGL_FILTER_gnomAD, df_anno$TGL_FILTER_VAF, sep=";"))
 )

 return(df_anno)
 }        
        
        
# make subdirectories
cbiodir <- paste0(outdir, "/cbioportal_import_data")
suppdir <- paste0(outdir, "/supplementary_data")

print("Processing Mutation data")

# only do the filtering steps if tglpipe is set to TRUE
if (tglpipe) {
  print("tglpipe is set to true, filtering data according to tgl specifications")
  df_cbio_anno <- procVEP(maffile)
  df_cbio_filt <- subset(df_cbio_anno, TGL_FILTER_VERDICT == "PASS")

  # get snvs for dcsigs
  df_snv <- subset(df_cbio_filt, Variant_Type == "SNP")

  # for cbioportal input
  write.table(df_cbio_filt, file=paste0(cbiodir, "/data_mutations_extended.txt"), sep="\t", row.names=FALSE, quote=FALSE)

  # unfiltered data
  write.table(df_cbio_anno, file=paste0(suppdir, "/unfiltered_data_mutations_extended.txt"), sep="\t", row.names=FALSE, quote=FALSE)

 } else {
  df_cbio_filt <- read.csv(maffile, sep="\t", header=TRUE, check.names=FALSE)
  df_snv <- subset(df_cbio_filt, Variant_Type == "SNP")
  write.table(df_cbio_filt, file=paste0(cbiodir, "/data_mutations_extended.txt"), sep="\t", row.names=FALSE, quote=FALSE)
 }

