## Generic Assay: Arm-level Copy Number Alteration (CNA)

A Generic Assay is a two-dimensional matrix that records non-gene level measurements for each sample. Instead of genes, it uses "generic entities" for the rows, which could be things like treatment responses or mutational signatures or arm-level copy number alteration as defined by you. For each entity-sample pair, the matrix holds a value, which could be a real number, text, or a binary value, representing the measurement.

| Filename (suggested)    | Filetype    | Requirement| Format  |  
|-------------|-------------|-------------|----------|
| meta_armlevel_CNA.txt | Meta |Optional| Multi-line text file|
| data_armlevel_CNA.txt | Data |Optional |Tab-separated file |


## Meta File 

1. **cancer_study_identifier**: Same value as specified in meta file of the study

2. **genetic_alteration_type**: GENERIC_ASSAY

3. **generic_assay_type**: ARMLEVEL_CNA
4. **datatype**: Can assume one of these three types of data LIMIT-VALUE, CATEGORICAL or BINARY
				- **LIMIT-VALUE**: Used for numerical data, allowing continuous numbers. Values may be prefixed with '>' or '<' to indicate thresholds (e.g., '>8.00'). 
				- **CATEGORICAL**: For categorical data, allowing any text. 
				- **BINARY**: For binary data, only accepts specific text values like "true", "false", "yes", or "no". 

				If the value for a generic entity in a sample is not available or cannot be measured, use 'NA' or leave the cell blank.

5. **stable_id**: Any unique identifier using a combination of alphanumeric characters, _ and -. This should be unique across all the metafiles in the study.

6. **profile_name**: A name describing the analysis.

7. **profile_description**: A description of the data processing done.

8. **data_filename**: A generic assay data filename

9. **show_profile_in_analysis_tab**: true (or false if you don't want to show this profile in any analysis tab)

10. **pivot_threshold_value**: A threshold value beyond which a generic assay data is considered effective. The **pivot_threshold_value** sets a critical boundary to distinguish important from unimportant values in a generic assay profile. It affects visualizations like heatmaps and waterfall plots by highlighting significant data. In heatmaps, values equal to the threshold are white, "important" values are dark blue, and "unimportant" ones are dark red. In waterfall plots, it separates upward and downward trends. If no clear boundary exists, the **pivot_threshold_value** should be omitted, causing all values to appear as shades of blue in heatmaps and deflections around zero in waterfall plots. Whether smaller values should be considered more important or larger values you should use the value_sort_order variable (see below).

11. **value_sort_order**: A flag that determines whether samples with smaller generic assay data values are displayed first or last; can be 'ASC' for smaller values first, 'DESC' for smaller values last. The value_sort_order field specifies whether smaller or larger values are considered more important.

		ASC (ascending): Smaller values are more "important".
		DESC (descending): Larger values are more "important".
		The default is ASC (smaller values are considered important).

		Usage:
		Oncoprint: When multiple samples are aggregated for a patient, ASC will display the sample with the smallest value, while DESC will display the one with the largest value.

		Heatmap: In the results view, smaller values appear as darker blue with ASC, and larger values appear as darker blue with DESC.

		Waterfall plot: The x-axis is oriented to show important observations on the left. ASC arranges smaller values on the left, and DESC arranges larger values on the left.

12. **patient_level**: false (or true if your data is patient level data). Generic Assay data will be considered sample_level data if the patient_level property is missing or set to false. I

13. **generic_entity_meta_properties**: A comma separate list of generic entity properties, e.g., "NAME,DESCRIPTION,URL". All meta properties must be defined in the generic_entity_meta_properties field, and each property listed must also appear as a column header in the corresponding data file. It is highly recommended to include the NAME, DESCRIPTION, and an optional URL for optimal visualization in the OncoPrint and Plots tabs.


## Data File 

The data file for a generic assay is a tab-separated format, where each column represents a sample, and each row represents a generic entity. Each cell contains the measurement for the entity-sample combination. 

### Required columns (in order):
1. **ENTITY_STABLE_ID**: A unique identifier (alphanumeric, `_`, or `-`).
2. One column for each **generic_entity_meta_properties** listed in the metafile (e.g., 'NAME', 'DESCRIPTION', 'URL').
3. One column for each sample, using the **sample ID** as the column header.

Each **generic entity** (row) is associated with its **ENTITY_STABLE_ID**, **generic_entity_meta_properties** (like name, description, URL), and the measured values for each sample.

## Arm-level Copy Number Alteration

Arm-level copy-number data is a specific subtype of Generic Assay Data. 

The allowed values are:
- **Loss**
- **Gain**
- **Unchanged**

If the value is missing or not available, use **NA** or leave the cell blank.


## Reference

Fore more information on generic assay files, please visit [this link](https://docs.cbioportal.org/file-formats/#generic-assay)
For more information on generic assay files, specifically arm level copy number data please visit [this link](https://docs.cbioportal.org/file-formats/#arm-level-cna-data)