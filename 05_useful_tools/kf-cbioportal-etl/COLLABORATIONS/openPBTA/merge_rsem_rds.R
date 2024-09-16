library("optparse")

option_list <- list(
  make_option(
    opt_str = "--stranded",
    type = "character",
    help = "stranded rsem rds",
  ),
  make_option(
    opt_str = "--polya",
    type = "character",
    help = "polya rsem rds"
  )
)
#parse options
opts <- parse_args(OptionParser(option_list = option_list))

read1 <- readRDS(opts$stranded)
read2 <- readRDS(opts$polya)

read1_row=rownames(read1)
read2_row=rownames(read2)

columns=Reduce(intersect,list(read1_row,read2_row))
print(class(columns))
common_read1 <- read1[columns,]
common_read2 <- read2[columns,]

merge_data <- cbind(common_read1,common_read2)
print(dim(merge_data))
saveRDS(merge_data, file = "pbta-gene-expression-rsem-fpkm-collapsed.rds")
