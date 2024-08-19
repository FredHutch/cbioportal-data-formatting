# Data Formatting for cBioportal

Welcome to the Data Formatting for cBioportal GitHub repository! 

This repository provides helpful scripts and instructions to transform your data into a format compatible with cBioportal. 

## Repository Structure

#### format_your_data

There are two types of data files that are uploaded within a study:

1. **meta files**: These files are usually a multi-line text file containing information about the data (meta to the data). You can create this file using any text editor (e.g., Notepad, VS Code). Each field should be filled based on your study's details.

2. **data files**: These files contain the actual data that is to be uploaded
   
This part of the repository is organized by cBioportal file format and includes the following:

  `scripts/` – Contains scripts that will help with transforming your data from an unformatted version to a cBioportal-compatible format. 
  
  `example/` – Contains example data and file formats that can be used for testing the functionality of the scripts as well as testing upload

  ``_example_unformatted.txt`` - An example test dataset that is unformatted. This is an example of data in a format you may usually start with. You can use the scripts to test how to convert files from a raw format to cBioportal-compatible format.
  
  ``_example_formatted.txt`` – Example file that is cBioportal-compatible formatted. This is what the example data should look like once you have used the scripts to process the example unformatted data files. 

#### validate_your_study

#### launch_local_cbioportal_instance

## A few things to keep in mind as you prepare your study for upload

There are just a few rules to follow:

- meta_study, meta_clinical and respective clinical data file are the only mandatory files.
  
- cancer type files can be mandatory if the study is referring to a cancer type that does not yet exist in the DB.
  
- meta files can be named anything, as long as it starts or ends with name 'meta'. E.g. meta_test, meta.test, test.meta are all fine; metal_test and metastudy are wrong.
  
- data files can be named anything and are referenced by a property data_filename set in the meta file.


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


