## Cancer Type 

If the type_of_cancer that you have specified in your meta_study.txt file does not exist in the cBioportal [database] (https://github.com/FredHutch/tg-cbioportal-data/resources/type_of_cancer.txt) then you are required to provide two files describing the cancer type from which the your data is being generated.

| Filename (suggested)    | Filetype    | Requirement| Format  |  
|-------------|-------------|-------------|----------|
| meta_cancer_type.txt | Meta |Required (conditional)| Multi-line text file|
| cancer_type.txt | Data |Required (conditional)| Tab-separated file |


## Meta file 

1. **genetic_alteration_type**: CANCER_TYPE
*Note: Do not alter this*

2. **datatype**: CANCER_TYPE
*Note: Do not alter this*

3. **data_filename**: name of the accompanying data file with your cancer-type specific information


## Data file 

1. **type_of_cancer**: The cancer type abbreviation, e.g., "brca".

2. **name**: The name of the cancer type, e.g., "Breast Invasive Carcinoma".

3. **dedicated_color**: CSS color name of the color associated with this cancer study, e.g., "HotPink". See [this list](https://www.w3.org/TR/css-color-3/#svg-color) for supported names, and follow the [awareness ribbons](https://en.wikipedia.org/wiki/List_of_awareness_ribbons) color schema. This color is associated with the cancer study on various web pages within the cBioPortal.

4. **parent_type_of_cancer**: Provide the subtype that the type_of_cancer field is, e.g., "Breast". If this is a completely new type of cancer then you can set this field to "tissue". This will place the given cancer type at "root" level in the "studies oncotree" that will be generated in the homepage (aka query page) of the portal.

## Reference 
Fore more information, please visit [this link](https://docs.cbioportal.org/file-formats/#cancer-type)