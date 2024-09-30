# cBioPortal Importer

Script pycbio.py is used to generate an import folder with all the data and metadata files required for uploading data to cBioPortal.

The script is available as a module:

```module load cbioportal-importer```

The module will also load accessory tools in the environment required for processing and annotating mutations.

Currently, data accepted for CbioPortal uploads are maf files from the VEP workflow, .seg files from sequenza, .genes.results files from the rsem workflow and .tab from the mavis workflow.

The data should be organized in a comma-separated map.csv file with the following information:

`patient_id,sample_id,maf_file.maf.gz,seg_file.seg,rsem.genes.results,mavis.tab`

Options, including path the output directory, path to the mapping file and filters can be specified in the config file

Generate the import folder with the following command: 

```cbio_importer generate -cf /path/to/config```


By default, the only clinical sample information that is required are the patient and sample identifiers which are extracted from the mapping file.
It is possible to add user-defined clinical fields using an optional tab-delimited clinical file. The first two columns should be labeled Patient and Sample and must contain the same patient and sample identifiers as in the map.csv file. Any other column names are valid but each column must contain a single data type (eg, boolean, string or number). The column names provided in the clinical information file will be displayed in cBioPortal. 

```cbio_importer generate -cf /path/to/config -cl /path/to/clinical_information```


Data uploaded to cBioPortal will replace any data already on the server. To add new data without replacing the existing data it is possible to merge data from existing import folder to new data. The raw data from the existing folder will be added to and processed with the new data to generate a new import folder. This allows to 1) upload data for which the original files have been deleted, 2) add data incrementally to cBioPortal. 

```cbio_importer generate generate -cf /path/to/config/ --append -mid /path/to/previous/outputdirectory```

Note that the `/path/to/previous/outputdirectory` is the outdir in the config file used to generate the previous import folder. Its it not the import folder itself.

Example command:

```cbio_importer generate -cf /.mounts/labs/gsiprojects/gsi/gsiusers/rjovelin/cbiportal_importer_dev/config_cbioportal_batch2.ini --append -mid /.mounts/labs/gsiprojects/gsi/gsiusers/rjovelin/cbiportal_importer_dev/batch1/out/```


Parameters

| argument | purpose | required/optional                                    |
| ------- | ------- | ------------------------------------------ |
| -cf | Path to configuration file  | required              |
| -cl | Path to sample clinical information file   | optional              |
| --append | Flag to indicate that data will be merged with data from a previous import folder | optional              |
| -mid | Path to the output directory (outdir in the config) of a previous import folder for which data will be merged   | optional              |



