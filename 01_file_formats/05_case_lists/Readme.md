## Case Lists
Case lists are used to define sample lists that can then be selected on the query page. While some case lists have specific functions, you can also add custom case lists. 

All case list files should be stored in a folder named case_lists, which is placed inside the cancer study folder. 

**Files to prepare:**

| Filename (suggested)    | Filetype    | Requirement
|-------------|-------------|-------------
| cases_all.txt | Meta |Required
| cases_sequenced.txt | Meta |Required when loading mutations data
| cases_cna.txt | Meta |Required when loading discrete copy-number data

### Required Fields

1. **cancer_study_identified**: same value as specified in study meta file

2. **stable_id**:  The stable_id follows a specific naming convention, it must begin with the cancer_study_identifier, followed by an underscore and a relevant suffix (e.g., \_custom). The user interface automatically selects the case lists on the query page based on the stable_id. Additionally, to display sample counts in the data sets widget on the home page and the Data Sets page, the specific naming convention needs to be followed. This also ensures accurate CNA and mutation frequency statistics on the Study view page. Use the following suffixes for the above functionalities to work appropriately
| Profile Type             | Suffix              | Description                                                                                  |
|--------------------------|---------------------|----------------------------------------------------------------------------------------------|
| Sequenced                | `_sequenced`        | Default case list when only a mutation profile is selected. Used in Study Summary to calculate proportion of samples with mutations. |
| CNA                      | `_cna`              | Default case list when only a CNA profile is selected. Used in Study Summary to calculate proportion of samples with CNA. |
| Sequenced and CNA         | `_cnaseq`           | Default case list when both mutation and CNA profiles are selected.                          |
| mRNA (microarray)         | `_mrna`             | Default case list when only a mRNA (microarray) profile is selected.                         |
| mRNA (RNA-Seq)            | `_rna_seq_mrna`     | Default case list when only a mRNA (RNA-Seq) profile is selected.                            |
| mRNA (RNA-SeqV2)          | `_rna_seq_v2_mrna`  | Default case list when only a mRNA (RNA-SeqV2) profile is selected.                          |
| mRNA normal               | `_normal_mrna`      | Used to calculate the number of normal samples on the datasets page.                         |
| microRNA                 | `_microrna`         | Used to calculate the number of microRNA samples on the datasets page.                       |
| Methylation (HM27)        | `_methylation_hm27` | Default case list when only a methylation (HM27) profile is selected.                        |
| RPPA                     | `_rppa`             | Default case list when only a RPPA profile is selected.                                      |
| Sequenced, CNA and mRNA   | `_3way_complete`    | Default case list when mutation, CNA, and mRNA profiles are selected.                        |
| SV                       | `_sv`               | Default case list when a structural variant profile is selected. Used to calculate proportion of samples with fusions in the Study Summary. |
| All                      | `_all`              | If not using the `add_global_case_list` attribute in Study metadata, this case list is needed.|


3. **case_list_name**: A name for the patient list, e.g., "All Tumors".

4. **case_list_description**: A description of the patient list, e.g., "All tumor samples (825 samples).".

5. **case_list_ids**: A tab-delimited list of sample ids from the dataset.

6. **case_list_category**: Optional alternative way of linking your case list to a specific molecular profile. E.g. setting this to all_cases_with_cna_data will signal to the portal that this is the list of samples to be associated with CNA data in some of the analysis. Here is a list of calide case_list_catefory names
	- all_cases_in_study
	- all_cases_with_mutation_data
	- all_cases_with_cna_data
	- all_cases_with_log2_cna_data
	- all_cases_with_methylation_data
	- all_cases_with_mrna_array_data
	- all_cases_with_mrna_rnaseq_data
	- all_cases_with_rppa_data
	- all_cases_with_microrna_data
	- all_cases_with_mutation_and_cna_data
	- all_cases_with_mutation_and_cna_and_mrna_data
	- all_cases_with_gsva_data
	- all_cases_with_sv_data
	- other

## Reference

Fore more information on mutations files, please visit [this link](https://docs.cbioportal.org/file-formats/#case-lists)