## Clinical data


Clinical data files are used to capture clinical attributes associated with the genomic data from patients and/or samples.

Clinical data files are used to do 2 things within cBioportal:

1. Add clinical attributes at both the patient level and the sample level to the genomic data

2. Capture the mapping between samples and patients. This is especially important when dealing with multiple samples from the same patient. 

**Files to prepare:**
| Filename (suggested)    | Filetype    | Requirement| Format  |  
|-------------|-------------|-------------|----------|
| meta_clinical_sample.txt | Meta |Required| Multi-line text file|
| data_clinical_sample.txt | Data |Required |Tab-separated file|
| meta_clinical_patient.txt | Meta |Optional |Multi-line text file|
| data_clinical_patient.txt | Data |Optional|Tab-separated file|

## Meta Clinical Sample File 

### Required Fields

1. **cancer_study_identifier**: This links the file to the cancer study and must have the same value specified in **meta_study.txt**

2. **genetic_alteration_type**: CLINICAL

3. **datatype** : SAMPLE_ATTRIBUTES

4. **data_filename**: your datafile


## Data Clinical Sample File

This file is a 2-dimensional matrix (tab separated) with clinical attributes of the sample. 

### Required Fields
#### Note: To give your clinical data header please refer to [this](https://github.com/cBioPortal/clinical-data-dictionary/blob/master/docs/resource_uri_to_clinical_attribute_mapping.txt) to find appropriate column names. This allows the variables to be used for comparison across multiple studies

The file begins with tab-delimited metadata describing the clinical attributes in the file. 

The rows for the metadata **have to start with a "#" symbol** and the following **four rows** are required:

1. **Attribute display name**: The **1st row** must have the display name for each clinical attribute. Consecutive attribute display names should be separated by a tab.

    _**Required columns**_
   
    Clinical sample data files have **two required** columns:

- **PATIENT_ID** : A patient ID that can only contain numbers, letters, points, underscores and hyphens. This will allow cBioportal to map samples to the patient and allows multiple samples to be associated with a single patient. For example, a single patient may have had multiple biopsies, each of which has been genomically profiled.

- **SAMPLE_ID**: A sample ID that can only contain numbers, letters, points, underscores and hyphens.

2. **Attribute description**: The **2nd row** should have a longer description of the clinical attribute in the same order as the attribute display name. Consecutive attribute descriptions should be separated by a tab.

3. **Attribute datatype**: The **3rd row** describes the type of data that will be found for clinical attribute. Data can assume only one of three formats; strings (letters), numbers, or boolean (True or False). Consecutive dataype should be separated by a tab and be in the same order as the attribute display name. 

4. **Attribute priority**: The **4th row** is a numerical value for each clinical attribute to be displayed on relevant pages like the Study view page. By default, 20 clinical charts are displayed. Higher-priority attributes will be shown more prominently, closer to the left-top of the page. Consecutive priority numbers should be separated by a tab and be in the same order as the attribute display name.

   - **Default priority** scores are set to 1. 

   - To make sure a chart is **visible** in the study view give it a high priority number.

   - **To hide a chart** set the priority to 0.

   - For combination charts (a chart that is made with more than one clinical attribute) if the priority of any one clinical attribute is 0 the chart will be hidden.

- To **disable** a chart set the priority to -1. Currently this diable function only works for single attribute charts.

   Some charts have **default** priority values, unless you explicity reassign priorty values for those specific attributes (values other than 1):
   
| Attribute    | Priority    | Notes    
|-------------|-------------|-------------
| CANCER_TYPE | 3000 |
| CANCER_TYPE_DETAILED | 2000 | 
| Overall survival plot | 400 |This is combination of OS_MONTH and OS_STATUS 
|  Disease Free Survival Plot | 300 |This is combination of DFS_MONTH and DFS_STATUS
| Mutation Count vs. CNA Scatter Plot| 200| 
|Mutated Genes Table | 90| 
| CNA Genes Table|80 | 
|study_id |70 | 
|# of Samples Per Patient |40 | 
| With Mutation Data Pie Chart| 60| 
|With CNA Data Pie Chart |50 | 
| Mutation Count Bar Chart| 30| 
|CNA Bar Chart| 20|
|GENDER| 9|
|SEX| 9|
|AGE| 8|

However, priority isn’t the only factor. A layout algorithm tries to arrange charts in a grid layout. Charts are placed from left to right, top to bottom in order of priority. 

For example, a pie chart, by default, takes 1 block/grid space and bar chart uses two blocks/grid spaces. To prevent misalignment if a chart does not fit a particular row then by default its priority is changed and the priority of the next chart that will fit is increased. 


More information on how Study View uses priority data to adjust views can be found here : [https://docs.cbioportal.org/deployment/customization/studyview/] 

5. **Attribute name for the database**: This name is the column names that will be see on the row above where the data fields actually start. For example, when the data are downloaded and viewed these will be secondary column headers of sorts. Consecutive priority numbers should be separated by a tab and be in the same order as the attribute display name.
   
6. **Data**: This will be the first row where the data will be found. Consecutive priority numbers should be separated by a tab and be in the same order as the attribute display name.

### Optional columns
1. **CANCER_TYPE**: Cancer Type (required for pan-cancer summary statistics tab)

2. **CANCER_TYPE_DETAILED**: Cancer Type Detailed, a sub-type of the specified (required for pan-cancer summary statistics tab) CANCER_TYPE

The following columns affect the header of the patient view by adding text to the samples in the header:

3. **SAMPLE_DISPLAY_NAME**: displayed in addition to the ID

4. **SAMPLE_CLASS**: Can only contain values [“Tumor”, “Cell Line”, “Xenograft”, “Organoid”]

5. **METASTATIC_SITE or PRIMARY_SITE**: Override TUMOR_SITE (patient level attribute) depending on sample type

The following columns additionally affect the Timeline data visualization:

6. **SAMPLE_TYPE, TUMOR_TISSUE_SITE or TUMOR_TYPE**: gives sample icon in the timeline a color. Can only contain values [`Primary`, `Metastasis`, `Recurrence`]
- If set to recurrence, recurred, progression or progressed: orange
- If set to metastatic or metastasis: red
- If set to primary or otherwise: black

7. There is also a list of columns with special functionalities that can be found (here)[https://docs.cbioportal.org/file-formats/#columns-with-specific-functionality]
   

## Meta Clinical Patient File 

### Required Fields

1. **cancer_study_identifier**: This links the file to the cancer study and must have the same value specified in **meta_study.txt**

2. **genetic_alteration_type**: CLINICAL

3. **datatype** : PATIENT_ATTRIBUTES

4. **data_filename**: your datafile


## Data Clinical Patient File 
#### Note: To give your clinical data header please refer to [this](https://github.com/cBioPortal/clinical-data-dictionary/blob/master/docs/resource_uri_to_clinical_attribute_mapping.txt) to find appropriate column names. This allows the variables to be used for comparison across multiple studies
This file contains information regarding the patient level information. 

### Required columns

1. **Attribute display name**: The **1st row** must have the display name for each clinical attribute. Consecutive attribute display names should be separated by a tab.

    _**Required**_
   
- **PATIENT_ID** : A patient ID that can only contain numbers, letters, points, underscores and hyphens. This will allow cBioportal to map samples to the patient and allows multiple samples to be associated with a single patient. For example, a single patient may have had multiple biopsies, each of which has been genomically profiled.


2. **Attribute description**: The **2nd row** should have a longer description of the clinical attribute in the same order as the attribute display name. Consecutive attribute descriptions should be separated by a tab.

3. **Attribute datatype**: The **3rd row** describes the type of data that will be found for clinical attribute. Data can assume only one of three formats; strings (letters), numbers, or boolean (True or False). Consecutive dataype should be separated by a tab and be in the same order as the attribute display name. 

4. **Attribute priority**: The **4th row** is a numerical value for each clinical attribute to be displayed on relevant pages like the Study view page. By default, 20 clinical charts are displayed. Higher-priority attributes will be shown more prominently, closer to the left-top of the page. Consecutive priority numbers should be separated by a tab and be in the same order as the attribute display name.

   - **Default priority** scores are set to 1. 

   - To make sure a chart is **visible** in the study view give it a high priority number.

   - **To hide a chart** set the priority to 0.

   - For combination charts (a chart that is made with more than one clinical attribute) if the priority of any one clinical attribute is 0 the chart will be hidden.

- To **disable** a chart set the priority to -1. Currently this diable function only works for single attribute charts.

   Some charts have **default** priority values, unless you explicity reassign priorty values for those specific attributes (values other than 1):
   
| Attribute    | Priority    | Notes    
|-------------|-------------|-------------
| CANCER_TYPE | 3000 |
| CANCER_TYPE_DETAILED | 2000 | 
| Overall survival plot | 400 |This is combination of OS_MONTH and OS_STATUS 
|  Disease Free Survival Plot | 300 |This is combination of DFS_MONTH and DFS_STATUS
| Mutation Count vs. CNA Scatter Plot| 200| 
|Mutated Genes Table | 90| 
| CNA Genes Table|80 | 
|study_id |70 | 
|# of Samples Per Patient |40 | 
| With Mutation Data Pie Chart| 60| 
|With CNA Data Pie Chart |50 | 
| Mutation Count Bar Chart| 30| 
|CNA Bar Chart| 20|
|GENDER| 9|
|SEX| 9|
|AGE| 8|

However, priority isn’t the only factor. A layout algorithm tries to arrange charts in a grid layout. Charts are placed from left to right, top to bottom in order of priority. 

For example, a pie chart, by default, takes 1 block/grid space and bar chart uses two blocks/grid spaces. To prevent misalignment if a chart does not fit a particular row then by default its priority is changed and the priority of the next chart that will fit is increased. 


More information on how Study View uses priority data to adjust views can be found here : [https://docs.cbioportal.org/deployment/customization/studyview/] 

5. **Attribute name for the database**: This name is the column names that will be see on the row above where the data fields actually start. For example, when the data are downloaded and viewed these will be secondary column headers of sorts. Consecutive priority numbers should be separated by a tab and be in the same order as the attribute display name.
   
6. **Data**: This will be the first row where the data will be found. Consecutive priority numbers should be separated by a tab and be in the same order as the attribute display name.

### Optional columns

1. **[PREFIX]_STATUS** and  **[PREFIX]_MONTHS**: To generate **survival** plots, two columns describing the patient status (STATUS) and months (MONTHS) at which the status data was collected must be provided. To use a pair of columns the same prefix should be used._

  _Note:The values of the survival status must be prefixed with 0: or 1._

Examples:

| Column name    | Values    
|-------------|-------------
| OS_STATUS | 0:LIVING or 1:DECEASED
|OS_MONTHS | Overall survival in months since initial diagnosis
| DFS_STATUS | 0:DiseaseFree or 1:Recurred/Progressed
|DFS_MONTHS| Disease-free survival in months since treatment

These columns will be used to create the survival plots in the study view and will form header columns in the patient view.

_Note: Include the reference dates for Survival Data in the attribute description in the associate meta file._

2. **PATIENT_DISPLAY_NAME**: Patient display name (string)

3. **SEX**: Gender or sex of the patient (string). Can only assume values FEMALE/MALE (with capitalization). No F/M allowed. 

4. **AGE**: Age at which the condition or disease was first diagnosed, in years (number)

5. **TUMOR_SITE**: The location of the tumor (string)

6. Custom columns in the clinical data files are allowed however must follow the same

7. There is also a list of columns with special functionalities that can be found here: [https://docs.cbioportal.org/file-formats/#columns-with-specific-functionality]
 

### Banned column names

MUTATION_COUNT and FRACTION_GENOME_ALTERED are auto populated clinical attributes, and should therefore not be present in clinical data files.


## Reference

Fore more information, please visit: [https://docs.cbioportal.org/file-formats/#cancer-study](https://docs.cbioportal.org/file-formats/#clinical-data)

