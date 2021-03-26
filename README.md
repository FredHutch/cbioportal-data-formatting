# tg-cbioportal-data

Use the following link for instructions of file validation and uploading:
https://docs.cbioportal.org/5.1-data-loading/data-loading/using-the-dataset-validator

Use the following link for instructions on data formatting and management:
https://docs.cbioportal.org/5.1-data-loading/data-loading/file-formats#data-files

Link for oncotree portal - useful for knowing what cancer types and their documentation is present for cbioportal:
http://oncotree.mskcc.org/#/home


## Test validation using example dataset

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
```

#### General links to docs
Overview of what a data "package" would look like for upload into cbioportal:
https://github.com/cBioPortal/cbioportal/blob/master/docs/Data-Loading.md#preparing-study-data

Note here that file names don't have to START with "meta" but do have to have it at the beginning or end.  

Consider making our format `clinical.meta` and `clinical_data.txt` to make them show up in alphabetical order together in the OS UI.  


Bunch of info about the data formats that need to be used:
https://github.com/cbioportal/cbioportal/blob/master/docs/File-Formats.md#introduction
