_Note: This readme is adapted from the original repository reaedme. Original repository: https://github.com/MJKorte/Data-processor_

## Data Processor 

This tool is used to convert clinical data files from multi-tab excel files into files that can be uploaded into cBioportal. These include the data_clinical_patient.txt or data_clinical_sample.txt files and their respective meta files. 

### Folder structure 

1. **data**: This folder has two sub-folders called **input** and **output**. 
*Note: Do not delete*

2. **requirements.txt**: This has the list of software dependancies that are needed to run this tool. 

3. **scripts**: The scripts required to run this tool
*Note: Do not delete*

4. **example**: The example study that can be used to test the script

5. **testing**: Folder with testing examples for internal use.


### Loading the dependancies

1. Make sure you have a local copy of this repository

2. Make sure you have all the dependancies installed (see requirements.txt)

You can install these using either of these two commands in a terminal window
	
	`pip3 install pandas numpy openpyxl`
	

	`python install pandas numpy openpyxl`

3. Have an excel file with your input clinical data (see instructions below on how to prepare your excel files)

### Preparing your excel files, things to consider


1. The script expects a clinical Excel datafile with the first row as variable names. 
 *Note: Because cBioportal has special treatment for certain variables. You can name your clinical variables names using [this table](https://github.com/cBioPortal/clinical-data-dictionary/blob/master/docs/resource_uri_to_clinical_attribute_mapping.txt)*

2. This script assumes every patient has atleast one corresponding sample. 
*Note: cBioportal needs a unique (non-dupiclate) sample and patient ID.* 

3. The patient ID column header is recogonized "\*" is placed before it. 

4. The sample ID column header is recogonized "#" is placed before it. 
*Note: For the Sample ID it is possible to mark multiple column names with "#" which combines the variables in these columns to a sample ID with a "-" connecting the values.*


For example: if you want the column PATIENT_ID to be the patient_ID used in cBioportal rename the column variable name to "\*PATIENT_ID".

5. If your excel file has multiple tabs it is recommended to name the sheets with unique and useful names. 


#### How to run the Data_processor

1. **STEP 1**: Copy your excel file into the input directory inside the Data_processor folder: path/to/Data-processor/data/input/your_excel_file.xlsx
 
2. **STEP 2**: Change directory to the folder

```
cd /path/to/Data-processor/

```

3. **STEP 3**: Run the script to create the annotation file 

The script will generate an annotation file in the input folder. Remember the script expects an Excel file in the "input" folder.

Run this in terminal
```
python3 ./scripts/generate_metadata.py -i 'your_excel_file.xlsx' -s 'Sheet_1' -a 'your_excel_file_annotation.xlsx'

```

* The "-i" flag is the name of the Excel clinical data file which needs to be placed in the in the /data/input folder included in this repository.
* The "-s" flag is the sheet name of the the Excel data sheet which is especially usefull when using clinical data files with multiple sheets.
* The "-a" flag is the name of the annotation file. It looks like you need to give a name for the script to work.

4. **STEP 4**: Update the annotation file

The script above will generate an Excel file called "your_excel_file_annotation.xlsx" in the input folder of the data folder.

This file consists of 2 sheets "Annotation" and "Meta study". 

*Note: Rows in the "Annotation" sheet can be deleted to remove variables from the final data files.*

 The Annotation sheet has 6 columns:

* Variables:                  The original variable names in the clinical datafile.
* Variable name Cbioportal:   The display variable name the variable will get when uploaded to cBioportal.
* Variable description:       A description of the variable visible in cBioportal.
* Datatype:                   Either "STRING" or "NUMBER" this has to be "STRING" for letters and "NUMBER" for numbers.
* Priority:                   The priority from 1-9 with 1 being top-priority, values with a high priority will be favored variables shown in the generated cBioportal dashboard.
* sample/patient:             This value is either "patient" or "sample" and will decide if the value is under patient data or sample data.
* Yes/No:                     The script has a function to transform 0 and 1 values to yes(1) and no(0) this gives better visualizations in cBioportal. If this is required fill in a "TRUE" and when a value doesn't need transformation fill in false. 
* Note that the Datatype has to be STRING when this "TRUE" is used.

The Meta study sheet has 2 columns "Variable" and "Description", the "Variables" column is filled in with:
* type of cancer:             Here a cancer type is required, for example "IDC", "mixed" for multiple cancer types.
* cancer study identifier:    A short "code" as study identifier.
* name:                       Name of the study.
* short name:                 Short name of the study.
* description:                Description of the study.
* add global case list:       Read the cBioportal clinical format linked above, default is "true".
* group:                      When working with specific group acces you can define which group has acces to the study, "PUBLIC" (default) means all groups can see the study.

5. **STEP 5**: Re-run the script to generate files
* When the above annotation file is filled out the annotation file name can be given in the terminal command after the -a flag. The script checks the annotation file for errors and missing values and it will give output when missing or wrong values are found. 

* cBioportal has several other variable names which are treated in a special way: OS_STATUS, OS_MONTHS, DFS_STATUS, DFS_MONTHS, GENDER or SEX, AGE and TUMOR_SITE. When these variables are present in the datafile you want to convert be sure to change the variable names to exactly match the names mentioned above. 

* OS_STATUS and DFS_STATUS are expected to be either 0 or 1. Gender is 1 for male and 2 for female.


* Otherwise it will convert the dataset to several text files containing data and metadata. 

If the script is finished the output folder will contain the study files which can be used directly by the MetaImport.py script [provided by cBioportal.](https://docs.cbioportal.org/5.1-data-loading/data-loading/using-the-metaimport-script)