# Merge two rsem rds files
library("optparse")

option_list <- list(
  make_option(
    opt_str = "--first_file",
    type = "character",
    help = "first rsem rds file to merge",
  ),
  make_option(
    opt_str = "--second_file",
    type = "character",
    help = "second rsem rds file to merge"
  ),
  make_option(
    opt_str = "--output_fn",
    type = "character",
    help = "What to name the merged file"
  )
)
#parse options
opts <- parse_args(OptionParser(option_list = option_list))

read1 <- readRDS(opts$first_file)
read2 <- readRDS(opts$second_file)

read1_row=rownames(read1)
read2_row=rownames(read2)

columns=Reduce(intersect,list(read1_row,read2_row))
print(class(columns))
common_read1 <- read1[columns,]
common_read2 <- read2[columns,]

merge_data <- cbind(common_read1,common_read2)
print(dim(merge_data))
saveRDS(merge_data, file = opts$output_fn)
