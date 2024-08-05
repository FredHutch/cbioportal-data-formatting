## Data-processor
This script is made to convert existing clinical datasets to the clinical data format [required by cBioportal.](https://docs.cbioportal.org/5.1-data-loading/data-loading/file-formats#clinical-data).

### Usage
* The generate_metadata.py script works by using terminal input. Terminal input looks like this: `./generate_metadata.py -i 'your_dataset_file.xlsx' -s 'sheet_name' -a 'Your_annotation_file.xlsx'`
* The "-i" flag is the name of the Excel clinical data file which needs to be placed in the in the /data/input folder included in this repository.
* The "-s" flag is the sheet name of the the Excel data sheet which is especially usefull when using clinical data files with multiple sheets.
* The "-a" flag is the name of the annotation file, the first time the script is ran for a new dataset, this flag can be left empty like this: `./generate_metadata.py -i 'your_dataset_file.xlsx' -s 'sheet_name' -a`. 

* The script will generate an annotation file, usage is described below. The data folder contains the in- and output folder. The script expects an Excel file in the "input" folder and writes the data files with metadata to the "output" folder.

### Annotation file

#### Formatting
* The script expects a clinical Excel datafile with the first row as variable names. Because cBioportal has special treatment for certain variables these variables can be formatted and used by the script. 

* 2This script assumes every patient has one corresponding sample. 

* cBioportal needs a unique (non-dupiclate) sample and patient ID. This script regcognizes the patient_ID variable by a "\*" placed in front of the variable in the dataset. 

* For example: if you want the variable T_nr to be the patient_ID used in cBioportal rename the column variable name to "\*T_nr". The same works for the sample ID, but with "#". 

* For the Sample ID it is possible to mark multiple column names with "#" which combines the variables in these columns to a sample ID with a "-" connecting the values.


The script will generate an Excel file called "Annotation_file.xlsx", this file consists of 2 sheets "Annotation" and "Meta study". Rows in the "Annotation" sheet can be deleted to remove variables from the final data files.

#### Annotation sheet
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

#### Conversion
* When the above annotation file is filled out the annotation file name can be given in the terminal command after the -a flag. The script checks the annotation file for errors and missing values and it will give output when missing or wrong values are found. 

* cBioportal has several other variable names which are treated in a special way: OS_STATUS, OS_MONTHS, DFS_STATUS, DFS_MONTHS, GENDER or SEX, AGE and TUMOR_SITE. When these variables are present in the datafile you want to convert be sure to change the variable names to exactly match the names mentioned above. 

* OS_STATUS and DFS_STATUS are expected to be either 0 or 1. Gender is 1 for male and 2 for female.


* Otherwise it will convert the dataset to several text files containing data and metadata. If the script is finished the output folder will contain the study files which can be used directly by the MetaImport.py script [provided by cBioportal.](https://docs.cbioportal.org/5.1-data-loading/data-loading/using-the-metaimport-script)