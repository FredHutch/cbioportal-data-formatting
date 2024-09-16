##### Add label #####

library(BSL)
x <- 262:379 # .factor variables from REDCap
BSL::label_factor_REDCap(var = x, data = data)
label(data[262:270]) # Checking

##### Selecting variables to import to cBioPortal #####

library(epicalc)
use(data)
des()
x <- c(1:15,270,271,273,274,377)
saveRDS(.data[x],"gbm.rds") # File to use in Reformat for cBioPortal.Rmd
