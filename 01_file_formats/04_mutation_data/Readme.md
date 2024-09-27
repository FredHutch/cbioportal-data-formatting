## Mutation Data

To upload mutation data (these refer specifically to SNV and Indel mutation types) different things need to be considered based on the sequencing methodology employed. 

**Files to prepare:**
| Filename (suggested)    | Filetype    | Requirement| Format  |  
|-------------|-------------|-------------|----------|
| meta_mutations.txt | Meta |Optional| Multi-line text file|
| data_mutations.txt | Data |Optional |Tab-separated file (MAF)|
| meta_gene_panel_matrix.txt | Meta |Optional |Multi-line text file|
| data_gene_panel_matrix.txt| Data |Optional|Tab-separated file|


## Meta Mutation File 

### Required Fields

1. **cancer_study_identifier**: same value as specified in meta_study.txt

2. **genetic_alteration_type**: MUTATION_EXTENDED #Note: Do not change this value

3. **datatype**: MAF #Note: Do not change this value

4. **stable_id**: mutations #Note: Do not change this value

5. **show_profile_in_analysis_tab**: true

6. **profile_name**: A name for the mutation data, e.g., "Mutations".

7. **profile_description**: A description of the mutation data, e.g., "Mutation data from whole exome sequencing.".

8. **data_filename**: your data file

### Optional Fields

1. **gene_panel**: gene panel stable id. See [Gene panels](#Gene-panels) section below for more details.

2. **swissprot_identifier**: accession or name, indicating the type of identifier in the SWISSPROT column

3. **variant_classification_filter**: List of Variant_Classifications values to be filtered out. See [Variant Classification Filter](#Variant-Classification-Filter) section below for more details. 

4. **namespaces**: Comma-delimited list of namespaces to import. See [Namespace](#Namespaces) section below for more information

## Data Mutation File 

The data file to represent mutations should be in the [Mutation Annotation Format](https://docs.gdc.cancer.gov/Data/File_Formats/MAF_Format/) (MAF). There are ways to modify/create your MAF files described [here]()

### Required Fields
1. **Hugo_Symbol**: A HUGO gene symbol.

2. **NCBI_Build<sup>1</sup>**: The Genome Reference Consortium Build is used by a variant calling software. It must be "GRCh37" or "GRCh38" for a human, and "GRCm38" for a mouse.

3. **Chromosome**: A chromosome number, e.g., "7".

4. **Variant_Classification**: Translational effect of variant allele, e.g. Missense_Mutation, Silent, etc.

5. **Reference_Allele**: The plus strand reference allele at this position.

6. **Tumor_Seq_Allele2**: Primary data genotype.

7. **Tumor_Sample_Barcode**: This is the sample ID. Either a TCGA barcode (patient identifier will be extracted), or for non-TCGA data, a literal SAMPLE_ID as listed in the clinical data file.

8. **HGVSp_Short**: Amino Acid Change, e.g. p.V600E.

### Optional Fields
1. **Entrez_Gene_Id** (recommended): A Entrez Gene identifier.

2. **Center**: The sequencing center.

3. **Start_Position** (recommended for additional features such as Cancer Hotspots annotations): Start position of event.

4. **End_Position** (recommended for additional features such as Cancer Hotspots annotations): End position of event.

5. **Strand**: We assume that the mutation is reported for the + strand.

6. **Variant_Type<sup>1</sup>**: Variant Type, e.g. SNP, DNP, etc.

7. **Tumor_Seq_Allele1<sup>1</sup>**: Primary data genotype. Read about [Tumor Seq Allele Ambiguity](#Tumor-Seq-Allele-Ambiguity) section below

8. **dbSNP_RS<sup>1</sup>**: Latest dbSNP rs ID.

9. **dbSNP_Val_Status<sup>1</sup>**: dbSNP validation status.

10. **Matched_Norm_Sample_Barcode<sup>1</sup>**: The sample ID for the matched normal sample.

11. **Match_Norm_Seq_Allele1**: Primary data.

12. **Match_Norm_Seq_Allele2**: Primary data.

13. **Tumor_Validation_Allele1**: Secondary data from orthogonal technology.

14. **Tumor_Validation_Allele2**: Secondary data from orthogonal technology.

15. **Match_Norm_Validation_Allele1<sup>1</sup>**: Secondary data from orthogonal technology.

16. **Match_Norm_Validation_Allele2<sup>1</sup>**: Secondary data from orthogonal technology.

17. **Verification_Status<sup>1</sup>**: Second pass results from independent attempt using same methods as primary data source. "Verified", "Unknown" or "NA".

18. **Validation_Status**: Second pass results from orthogonal technology. "Valid", "Invalid", "Untested", "Inconclusive", "Redacted", "Unknown" or "NA".

19. **Mutation_Status**: "Somatic" or "Germline" are supported by the UI in Mutations tab. "None", "LOH" and "Wildtype" will not be loaded. Other values will be displayed as text.

20. **Sequencing_Phase<sup>1</sup>**: Indicates current sequencing phase.

21. **Sequence_Source<sup>1</sup>**: Molecular assay type used to produce the analytes used for sequencing.

22. **Validation_Method<sup>1</sup>**: The assay platforms used for the validation call.

23. **Score<sup>1</sup>**: Not used.

24. **BAM_File<sup>1</sup>**: Not used.

25. **Sequencer<sup>1</sup>**: Instrument used to produce primary data.

26. **t_alt_count**: Variant allele count (tumor). 

27. **t_ref_count**: Reference allele count (tumor).

28. **n_alt_count**: Variant allele count (normal).

29. **n_ref_count**: Reference allele count (normal).

#### Custom driver annotations: It is possible to manually add columns for defining custom driver annotations. These annotations can be used to complement or replace default driver annotation resources OncoKB and HotSpots.

30. **cbp_driver**: "Putative_Driver", "Putative_Passenger", "Unknown", "NA" or "" (empty value). This field must be present if the cbp_driver_annotation is also present in the MAF file. 

31. **cbp_driver_annotation**: Description field for the cbp_driver value (limited to 80 characters). This field must be present if the cbp_driver is also present in the MAF file. This field is free text. Example values for this field are: "Pathogenic" or "VUS".

32. **cbp_driver_tiers**: Free label/category that marks the mutation as a putative driver such as "Driver", "Highly actionable", "Potential drug target". . This field must be present if the cbp_driver_tiers_annotation is also present in the MAF file. In the OncoPrint view's Mutation Color dropdown menu, these tiers are ordered alphabetically. This field is free text and limited to 20 characters. For mutations without a custom annotation, leave the field blank or type "NA".

33. **cbp_driver_tiers_annotation**: Description field for the cbp_driver_tiers value (limited to 80 characters). This field must be present if the cbp_driver_tiers is also present in the MAF file. This field can not be present when the cbp_driver_tiers field is not present. 

<sup>**1**</sup> These columns are currently not shown in the Mutation tab and Patient view.

#### Allele specific copy number (ASCN) annotations: Allele specific copy number (ASCN) annotation is also supported and may be added using namespaces, described [below](#Namespaces). If ASCN data is present in the cBioPortal mutation data file, the deployed cBioPortal instance will display additional columns in the mutation table showing ASCN data.

**The ASCN columns below are optional by default. If `ascn` is a defined namespace in `meta_mutations_extended.txt`, then these columns are ALL required.**

34. **ASCN.ASCN_METHOD**: Method used to obtain ASCN data e.g "FACETS".

35. **ASCN.CCF_EXPECTED_COPIES**: Cancer-cell fraction if mutation exists on major allele. 

36. **ASCN.CCF_EXPECTED_COPIES_UPPER**: Upper error for CCF estimate.

37. **ASCN.EXPECTED_ALT_COPIES**: Estimated number of copies harboring mutant allele.

38. **ASCN.CLONAL**: "Clonal", "Subclonal", or "Indeterminate". 

39. **ASCN.TOTAL_COPY_NUMBER**: Total copy number of the gene.

40. **ASCN.MINOR_COPY_NUMBER**: Copy number of the minor allele.

41. **ASCN.ASCN_INTEGER_COPY_NUMER**: Absolute integer copy-number estimate.

## Filtered mutations
A special case for **Entrez_Gene_Id=0** and **Hugo_Symbol=Unknown**: when this combination is given, the record is parsed in the same way as **Variant_Classification=IGR** and therefore filtered out.


## Gene panels

The gene_panel attribute allows you to annotate **all samples** in your maf file with information about which gene panel was used to sequence the samples. Only a single gene panel can be specified when using the meta file above by entering its value in the variable gene_panel. 

Checkout the tg-cbioportal-data/02_resources/available_gene_panels.txt to check the latest available gene panels in the FH instance of cBioPortal. If you do not find the gene panel relavent to your study please email us so we can add this.

You should consider using this when:

- Data contains samples that are profiled but no mutations are called. Also please add these samples to the sequenced case list.

- Multiple gene panels are used to profile the samples in the MAF file.

In order to use this annotation in your mutation files you need to :
1. Ensure that the gene panels you are refering to are present in the cBioPortal database 

2. Create two additional files: 

### Meta Gene Panel Matrix File

1. cancer_study_identifier: same value as specified in study meta file

2. genetic_alteration_type: GENE_PANEL_MATRIX #Note: Do not change this value

3. datatype: GENE_PANEL_MATRIX #Note: Do not change this value

4. data_filename: your datafile


### Data Gene Panel Matrix File

1. SAMPLE_ID : These should match the sample IDs in your mutation files. 

2. A column for each profile in the study using the stable_id as the column header. This should match those provided in the respective meta files. Use NA for samples that were not profiled using the gene panel. 

## Variant Classification Filter

The variant_classification_filter field is used to filter out specific mutations in cBioPortal. It should contain a comma-separated list of Variant_Classification values. By default, cBioPortal filters out mutations Silent, Intron, IGR, 3'UTR, 5'UTR, 3'Flank and 5'Flank, except for TERT promoter mutations.

Fill out this variable as follows based on your use-case

- For no filtering include the field in the metadata file but leave it empty.
- For default Filtering omit this field in the metadata file.

Allowed values for filtering include Frame_Shift_Del, Frame_Shift_Ins, In_Frame_Del, In_Frame_Ins, Missense_Mutation, Nonsense_Mutation, Silent, Splice_Site, Translation_Start_Site, Nonstop_Mutation, 3'UTR, 3'Flank, 5'UTR, 5'Flank, IGR, Intron, RNA, Targeted_Region, De_novo_Start_InFrame, De_novo_Start_OutOfFrame, Splice_Region and Unknown. Look [here](https://docs.cbioportal.org/file-formats/#gene-panels-for-mutation-data) for more details on other variant annotations

## Namespaces

The namespaces field is used to add extra information when importing mutation data into cBioPortal. This field lists any extra columns you want to include, separated by commas.

Each column you add should start with a label (called a "namespace") followed by a period, like this: ASCN.total_copy_number or ASCN.minor_copy_number. The ASCN part is the namespace, and everything that starts with it will be imported.

If you don’t need to import any extra columns, you can leave this field blank. Only the required columns will be imported, and any extra ones will be ignored.

## Tumor Seq Allele Ambiguity 
In MAF data, there can be confusion about whether Tumor_Seq_Allele1 or Tumor_Seq_Allele2 represents the variant allele when importing new mutation records into cBioPortal. To resolve this, the preference is given to the tumor allele that contains a valid nucleotide sequence (^[ATGC]\*$) rather than a null, empty value, or "-".

For example:

If Reference_Allele = "G", Tumor_Seq_Allele1 = "-", and Tumor_Seq_Allele2 = "A", preference will go to Tumor_Seq_Allele2.
If Tumor_Seq_Allele1 = "T", and it doesn't match the Reference_Allele, it will be preferred.
To avoid ambiguity, leave Tumor_Seq_Allele1 empty if this information is not available in your data source.

## Reference

Fore more information on mutations files, please visit [this link](https://docs.cbioportal.org/file-formats/#mutation-data)
For more information on gene panel data, please visit [this link](https://docs.cbioportal.org/file-formats/#gene-panel-data)
