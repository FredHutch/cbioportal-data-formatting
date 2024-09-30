## Generic Assay: Mutational Signatures 

A Generic Assay is a two-dimensional matrix that records non-gene level measurements for each sample. Instead of genes, it uses "generic entities" for the rows, which could be things like treatment responses or mutational signatures or arm-level copy number alteration as defined by you. For each entity-sample pair, the matrix holds a value, which could be a real number, text, or a binary value, representing the measurement.

| Filename (suggested)    | Filetype    | Requirement| Format  |  
|-------------|-------------|-------------|----------|
| meta_mutational_signature_contribution_SBS.txt | Meta |Required (if including this type of data)| Multi-line text file|
| data_mutational_signature_contribution_SBS.txt | Data |Required (if including this type of data) |Tab-separated file |


### Meta File
**Mutational signature meta files follow the same structure as **Generic Assay Meta** files but with some differences (please read content below)**

1. **cancer_study_identifier**: Same value as specified in meta file of the study

2. **genetic_alteration_type**: GENERIC_ASSAY

3. **generic_assay_type**: MUTATIONAL_SIGNATURE

4. **datatype**: Must be LIMIT_VALUE

5. **stable_id**: Values should end with: \_filetype\_identifier, where:
				  filetype is either contribution, pvalue or counts
                  identifier is consistent between files belonging to the same analysis
                  Multiple signatures can be added to a single study, as long as they have different identifiers in their stable id (e.g., contribution_SBS and contribution_DBS)

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

13. **generic_entity_meta_properties**: A comma separate list of generic entity properties, e.g., "NAME,DESCRIPTION,URL". All meta properties must be defined in the generic_entity_meta_properties field, and each property listed must also appear as a column header in the corresponding data file. The `NAME` value is required, while `DESCRIPTION` and `URL` are optional but could be included for optimal visualization in the OncoPrint and Plots tabs.

### Data Files

Mutational signature data files follow the same format as **Generic Assay Data** files. Each mutational signature collection can have up to three data files, with each data file having their own associate meta file:

1. **Signature Contribution File (Required)**  
   Contains contribution values for each signature-sample pair.  
   - Values must be between `0 ≥ x ≥ 1`.

2. **Signature P-value File (Optional)**  
   Contains p-values for each signature-sample pair.  
   - Values below `0.05` are considered significant.

3. **Mutational Counts Matrix File (Optional)**  
   Contains nucleotide changes for each sample.  
   - Single-base substitutions (96 channels), double-base substitutions (72 channels), and insertion/deletions (83 channels) follow the COSMIC signatures format, but other channel configurations are allowed.
   - Values should be positive integers.

## Reference

For more information on generic assay files, please visit [this link](https://docs.cbioportal.org/file-formats/#generic-assay)
For more information on mutational signature files please visit [this link](https://docs.cbioportal.org/file-formats/#mutational-signature-data)
