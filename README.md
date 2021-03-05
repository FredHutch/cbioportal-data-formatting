# tg-cbioportal-data

Use the following link for instructions of file validation and uploading:
https://docs.cbioportal.org/5.1-data-loading/data-loading/using-the-dataset-validator

Use the following link for instructions on data formatting and management:
https://docs.cbioportal.org/5.1-data-loading/data-loading/file-formats#data-files


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
