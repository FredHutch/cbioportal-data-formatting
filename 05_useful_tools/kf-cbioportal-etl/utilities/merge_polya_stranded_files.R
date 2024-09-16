library("optparse")
library("dplyr")
#process inputs
option_list <- list(
  make_option(
    opt_str = "--polya",
    type = "character",
    help = "object to gene-expression-rsem-fpkm-collapsed-polya ",
  ),
  make_option(
    opt_str = "--stranded",
    type = "character",
    help = "object to gene-expression-rsem-fpkm-collapsed-stranded"
  ),
  make_option(
    opt_str = "--output_file",
    type = "character",
    help = "Name of the output files with common names"
  )
)
#parse options
opts <- parse_args(OptionParser(option_list = option_list))
message("Reading in rds file ", opts$polya)
polya = readRDS(opts$polya)
message("Reading in rds file ", opts$stranded)
stranded = readRDS(opts$stranded)
polya_row=rownames(polya)
stranded_row=rownames(stranded)
columns=Reduce(intersect,list(polya_row,stranded_row))
common_polya <- polya[columns,]
common_stranded <- stranded[columns,]
total <- rbind(t(common_polya), t(common_stranded))
result <- t(total)
df <- data.table::as.data.table(result)
message("Reading in output file ", opts$output_file)
saveRDS(result, file = opts$output_file)
