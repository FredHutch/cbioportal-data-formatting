# Data Formatting for cBioportal

Welcome to the Data Formatting for cBioportal GitHub repository! 

This repository provides publicly available helpful scripts to transform your data into a format compatible with cBioportal. 


## Repository Structure

### Format your data

This part of the repository is organized by cBioportal file format and includes the following:

  `scripts/` – Contains scripts that will help with transforming your data from an unformatted version to a cBioportal-compatible format. 
  
  `example/` – Contains example test data for testing the functionality of the scripts and for testing upload

  ``_example_unformatted.txt`` - An example test dataset that is unformatted. This is an example of data in a format you may usually start with. 
  
  ``_example_formatted.txt`` – The example test data that is cBioportal-compatible formatted 

### Validate your formatted data

### Upload your formatted data into a local instance of cBioportal

## Helpful links

### cBioportal documentation

Expected file formats for different data types for cBioportal: https://docs.cbioportal.org/file-formats/

Overview of what a completed data "package" would look like for upload into cBioportal: https://github.com/cBioPortal/cbioportal/blob/master/docs/Data-Loading.md#preparing-study-data















#### tg-cbioportal-data

Use the following link for instructions of file validation and uploading:
https://docs.cbioportal.org/5.1-data-loading/data-loading/using-the-dataset-validator

Use the following link for instructions on data formatting and management:
https://docs.cbioportal.org/5.1-data-loading/data-loading/file-formats#data-files

Link for oncotree portal - useful for knowing what cancer types and their documentation is present for cbioportal:
http://oncotree.mskcc.org/#/home


#### Test validation using example dataset

```

git clone https://github.com/cBioPortal/cbioportal.git
cd cbioportal
CBIO=$(pwd)

# Then run
$CBIO/core/src/main/scripts/importer/validateData.py -s $CBIO/core/src/test/scripts/test_data/study_es_0/ -u http://cbioportal.fredhutch.org -v


# Fails due to not having the Gene panels in first.  So go put in gene panels!

$CBIO/core/src/main/scripts/importGenePanel.pl --data $CBIO/core/src/test/scripts/test_data/study_es_0/data_gene_panel_testpanel1.txt
$CBIO/core/src/main/scripts/importGenePanel.pl --data $CBIO/core/src/test/scripts/test_data/study_es_0/data_gene_panel_testpanel2.txt

# Amy's fails b/c JAVA is not set upright yet/perl scripts are not fully set up right either. Try via Docker?
```

```
cd <local version of tg-cbioportal-data repo>
VALIDDATA=$(pwd) ## example: /github/public/tg-cbioportal-data/Pag-Validation-Data/filesForUpload

$CBIO/core/src/main/scripts/importer/validateData.py -s $VALIDDATA -u http://cbioportal.fredhutch.org -v

$CBIO/core/src/main/scripts/importer/validateData.py -s $VALIDDATA -u http://cbioportal.org -v
```


