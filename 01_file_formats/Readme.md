## File formats

This part of the repository provides helpful instructions to prepare your data into a format that can be "read" into cBioportal. In this part of the repository you will find different sub-directories for the different file formats. Each sub-directory has its own Readme with detailed instructions on how to prepare you files. It also has examples/templates that you can copy for the different files needed which you can use to prepare your own study files


## File types 

To upload a study into cBioportal, data is presented (usually) as two file types:

1. **data files**: that contain the actual data that is to be uploaded. These are tab-delimited files in a specific format

2. **meta files**: that contain information about the data files. These are multi-line text file with information about the data files. You can create this file using any text editor (e.g., Notepad, VS Code). Each field should be filled with study specific information.

   
## Before you begin

There are just a few things to consider before you begin preparing your files for upload into cBioportal:

- **Mandatory files**: For any study to be uploaded there are is a minimal set of files you need to be uploaded. These are the meta_study, meta_clinical and the data_clinical files.
  
*Note*: cancer_type file can be mandatory if the study is referring to a cancer subtype that does not yet exist in the cBioportal database. To know if they type of cancer your data comes from is present in the database please see the list here:<enter relevant URL>. If the cancer type your data is generated from is not in this list please make sure to prepare and upload the cancer_type file. 
  
- **Naming the files**: Meta files can be named anything, as long as it starts or ends with name 'meta'. E.g. meta_test, meta.test, test.meta are all fine; metal_test and metastudy are wrong. Additionally, data files can be named anything as long as they are referenced to appropriately in the field data_filename set in the meta file.


## Helpful links

### cBioportal documentation

See here for detailed information of the expected file formats for cBioportal: https://docs.cbioportal.org/file-formats/

Overview of what a completed data "package" would look like for upload into cBioportal: https://github.com/cBioPortal/cbioportal/blob/master/docs/Data-Loading.md#preparing-study-data