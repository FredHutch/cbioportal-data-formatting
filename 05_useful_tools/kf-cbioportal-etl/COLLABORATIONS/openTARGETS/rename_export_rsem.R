if(!require(data.table)){install.packages('data.table')}
if(!require(optparse)){install.packages('optparse')}
if(!require(Rcpp)){install.packages('Rcpp')}
if(!require(funr)){install.packages('funr')}
if(!require(readr)){install.packages('readr')}
library("optparse")
library("data.table")
library("Rcpp")
library("funr")
library("readr") #required for write_tsv function
root_dir <- dirname(dirname(dirname(sys.script()))) #extract the base folder
path_cpp_file <- file.path(root_dir, "utilities","compute_zscore.cpp") #path to c++ file
sourceCpp(path_cpp_file) #set path to the cpp file

#process inputs
option_list <- list(
  make_option(
    opt_str = "--rna_rds",
    type = "character",
    help = "openX rsem rds expression object",
  ),
  make_option(
    opt_str = "--map_id",
    type = "character",
    help = "mapping ID file with headers: BS_ID    Sample Type    Cbio ID"
  ),
  make_option(
    opt_str = "--type",
    type = "character",
    help = "study name, like 'openpbta'"
  ),
  make_option(
    opt_str = "--computeZscore",
    type = "character",
    default = "None", 
    help = "Use C++ Method to compute zscore and write file. Usage: C++ or R"
  )
)
#parse options
opts <- parse_args(OptionParser(option_list = option_list))
message("Reading in rds file ", opts$rna_rds)
rna = readRDS(opts$rna_rds)

# Example entry: brain    BS_6H1C1ME9    RNA    7316-2558_460366
message("Reading in sample naming file ", opts$map_id)
map_ids = read.csv(sep = "\t", header=TRUE, opts$map_id)
map_ids = map_ids[map_ids$Sample.Type == "RNA",]
# Subset only on sample present in mapping ID file
subset_rna = rna[,which(colnames(rna) %in% map_ids$BS_ID)]
rownames(subset_rna) = rownames(rna)
# Rename BS IDs to cBio IDs
message("Renaming samples and outputting tpm file")
subset_rna <- as.data.frame(subset_rna)
setnames(subset_rna, old=as.character(map_ids$BS_ID), new=as.character(map_ids$Cbio.ID), skip_absent=TRUE)

write_tsv(data.frame("Hugo_Symbol"=rownames(subset_rna),subset_rna, check.names = FALSE),paste(opts$type, ".rsem_merged.txt", sep=""), escape="none")
# Get z score of log2 tpm with added pseudocount - round to 4 places as added precision not needed

rm(rna) #clean the memory footprint
rm(map_ids)

output_file_name=paste(opts$type, ".rsem_merged_zscore.txt", sep="")
if(opts$computeZscore =="C++"){
    message("Calculating z scores of log2 tmp + 1 with C++")
    #c++ function to compute zscores with 8 threads
    subset_zscore=compute_write_zscore(data.matrix(subset_rna),8)
    rm(subset_rna)
    message("Writing zscore to a file with C++")
  #function in C++ to write matrix into tsv format with name of the file as output_file_name
    write_file(subset_zscore,output_file_name)
} else if(opts$computeZscore =="R") {
    message("Calculating z scores of log2 tmp + 1")
    subset_zscore = round(t(scale(t(log2(subset_rna + 1)))), 4)
    rm(subset_rna)
    message("Writing zscore to a file")
    write_tsv(data.frame("Hugo_Symbol"=rownames(subset_zscore),subset_zscore, check.names = FALSE),output_file_name, escape="none")
} else {
    stop("Either computeZscore flag is not setup or invalid input argument to computeZscore flag. Allowed arguments are C++ or R") 
}
