## File formats

This part of the repository provides helpful instructions to prepare your data into a format that can be "read" into cBioPortal. In this part of the repository, you will find different sub-directories for the different file formats. Each sub-directory has its own README with detailed instructions on how to prepare your files. It also includes examples/templates that you can copy to prepare your own study files.

## File types

To upload a study into cBioPortal, data is presented in two main file types:

1. **Data files** — These contain the actual data to be uploaded (e.g., mutations, clinical info). These are typically **tab-delimited `.txt` files**.
2. **Meta files** — These provide metadata about the data files (e.g., data type, version, source). These are **multi-line text files**. Each field must be manually filled in using a text editor like Notepad or VS Code.

## Before you begin

Here are a few tips before you start preparing your files:

- **Mandatory files**: Every study must include a minimum of these three files:
  - `meta_study.txt`
  - `meta_clinical_sample.txt`
  - `data_clinical_sample.txt`

> 📝 *Note: If you're working with a new cancer type not in cBioPortal's database, you'll need to include a `cancer_type.txt` and `meta_cancer_type.txt` file. See [public cBioPortal documentation](https://docs.cbioportal.org/file-formats/#cancer-type) for formatting guidance.

- **Naming your files**:
  - **Meta files** must include the word `meta`. Acceptable examples: `meta.txt`, `meta_clinical.txt`, `clinical_meta.txt`
  - **Data files** can be named freely, but must match the `data_filename` specified in the associated meta file.

---

## Helpful links

### 📚 Official Documentation

- [cBioPortal File Format Guide](https://docs.cbioportal.org/file-formats/)
- [How to package a complete study](https://github.com/cBioPortal/cbioportal/blob/master/docs/Data-Loading.md#preparing-study-data)

### 📦 Required and Optional Files Overview

| Type                                        | Requirement | Filename Example                           | Required Format                 | Purpose                                                              | Detailed Instructions                                                                                                                                        | Example                                                                                               |
|---------------------------------------------|-------------|-------------------------------------------|---------------------------------|----------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| Cancer Study                                | Required    | meta_study.txt                            | Text file                       | Overall information about the study                                  | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/01_cancer_study)                                               | [Example](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/01_cancer_study/meta_study.txt) |
| Cancer Type                                 | Optional    | meta_cancer_type.txt                      | Text file                       | A meta file with information about the file with new cancer type. Required if your cancer type does not exist in the database. | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/02_cancer_type)                                            | [Example](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/02_cancer_type/meta_cancer_type.txt) |
| Cancer Type                                 | Optional    | cancer_type.txt                           | Tab Separated Value (TSV)      | Details about a new cancer type not found in the cBioPortal database. Required if your cancer type does not exist in the database. | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/02_cancer_type)                                            | [Example](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/02_cancer_type/cancer_type.txt) |
| Clinical Sample                             | Required    | meta_clinical_sample.txt                  | Text file                       | A meta file with information about the clinical samples              | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/03_clinical_data)                                               | [Example](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/03_clinical_data/meta_clinical_sample.txt) |
| Clinical Sample                             | Required    | data_clinical_sample.txt                  | Tab Separated Value (TSV)      | File with the sample-level clinical covariates/metadata              | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/03_clinical_data)                                               | [Example](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/03_clinical_data/data_clinical_sample.txt) |
| Clinical Patient                            | Optional    | meta_clinical_patient.txt                 | Multi-line text file            | A meta file with information about the clinical patient             | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/03_clinical_data)                                               | [Example](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/03_clinical_data/meta_clinical_patient.txt) |
| Clinical Patient                            | Optional    | data_clinical_patient.txt                 | Tab Separated Value (TSV)      | File with the sample-level clinical covariates/metadata             | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/03_clinical_data)                                               | [Example](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/03_clinical_data/data_clinical_patient.txt) |
| Panel                                       | Optional    | meta_gene_panel_matrix.txt                | Multi-line text file            | A meta file for describing the gene panel matrix file              | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/04_mutation_data)                                               | [Example](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/04_mutation_data/meta_gene_panel_matrix.txt) |
| Panel                                       | Optional    | data_gene_panel_matrix.txt                | Tab Separated Value (TSV)      | Sample level details of the gene panel used for the different samples | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/04_mutation_data)                                               | [Example](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/04_mutation_data/data_gene_panel_matrix.txt) |
| Mutation                                    | Optional    | meta_mutations.txt                        | Multi-line text file            | A meta file describing information about the mutation file.          | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/04_mutation_data)                                               | [Example](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/04_mutation_data/meta_mutations.txt) |
| Mutation                                    | Optional    | data_mutations.txt                        | Tab Separated Value (TSV)      | File with mutation data                                             | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/04_mutation_data)                                               | [Example](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/04_mutation_data/data_mutations.txt) |
| Case Lists                                  | Required    | case_lists/cases_sequenced.txt           | Multi-line text file            | Helps cBioPortal identify which samples have data. Required if uploading data files beyond clinical data.               | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/05_case_lists)                                               | [Example](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/05_case_lists/case_lists/cases_sequenced.txt) |
| Structural Variant                          | Optional    | meta_sv.txt                               | Multi-line text file            | A meta file for describing the structural variant data file        | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/06_structural_variants)                                          | [Example](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/06_structural_variants/meta_sv.txt) |
| Structural Variants                         | Optional    | data_sv.txt                               | Tab Separated Value (TSV)      | File with structural variant data                                   | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/06_structural_variants)                                          | [Example](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/06_structural_variants/data_sv.txt) |
| Generic Assays: Arm-level CNA               | Optional    | meta_armlevel_CNA.txt                     | Multi-line text file            | A meta file for arm-level copy number alteration data              | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/07_generic_assay_arm_level_cna)                                   | [Example](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/07_generic_assay_arm_level_cna/meta_armlevel_CNA.txt) |
| Generic Assays: Arm-level CNA               | Optional    | data_armlevel_CNA.txt                     | Tab Separated Value (TSV)      | Arm-level copy number alteration data                               | [Readme](https://github.com/FredHutch/cbioportal-data-formatting/tree/main/01_file_formats/07_generic_assay_arm_level_cna)                                   | [Example](https://git

> 📝 *Note: As of Version 6, cBioPortal requires at least one non-clinical data file. If your study is purely clinical.*

