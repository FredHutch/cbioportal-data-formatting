## Structural Variants 

cBioPortal can load all kinds of structural variant data however only fusions are displayed. 

| Filename (suggested)    | Filetype    | Requirement| Format  |  
|-------------|-------------|-------------|----------|
| meta_sv.txt | Meta |Optional| Multi-line text file|
| data_sv.txt | Data |Optional |Tab-separated file |

## Meta File 

### Required Fields

1. **cancer_study_identifier**: same value as specified in meta_study.txt file

2. **genetic_alteration_type**: STRUCTURAL_VARIANT

3. **datatype**: SV

4. **stable_id**: structural_variants

5. **show_profile_in_analysis_tab**: true.

6. **profile_name**: A name for the fusion data, e.g., "Structural Variants".

7. **profile_description**: A description of the structural variant data.

8. **data_filename**: your datafile (e.g. data_sv.txt)


### Optional Fields

1. **gene_panel**:  gene panel stable id


## Data File 
To ensure structural variants display correctly in the interface, each structural variant will be a single row. 

At a minimum, include:

- `Sample_Id`
- Either `Site1_Hugo_Symbol`/`Site1_Entrez_Gene_Id` or `Site2_Hugo_Symbol`/`Site2_Entrez_Gene_Id`
- `SV_Status`

For the **structural variant tab visualization** (currently in development), you also need:

- `Site1_Ensembl_Transcript_Id`
- `Site2_Ensembl_Transcript_Id`
- `Site1_Region`
- `Site2_Region`

Other fields, like `Class`, `Annotation`, and `Event_Info`, will be displayed on different pages of the website. These columns are especially prominent in several key areas of the site.

**Note:** We highly recommend including all of the fields mentioned to ensure smooth and proper visualization across the site. 


### Required Fields
Here is the table reformatted with numbered rows and **bold** for the field names:

1. **Sample_ID**: Should be the same as in other data files in the same study.
   
2. **SV_Status**: SOMATIC or GERMLINE  

3. **Site1_Hugo_Symbol**: [HUGO](http://www.genenames.org/) gene symbol of gene 1. One might call this the left site (3’) as well. (strongly recommended field)

4. **Site2_Hugo_Symbol**: [HUGO](http://www.genenames.org/) gene symbol of gene 2. One might call this the right site (5’) as well.  

### Strongly Recommended Fields

1. **Site1_Entrez_Gene_Id**: [Entrez Gene](http://www.ncbi.nlm.nih.gov/gene) identifier of gene 1.
   
2. **Site1_Region_Number**: Number of Site 1 region e.g. exon 2.

3. **Site1_Region**: We advise using one of these {5_Prime_UTR, 3_Prime_UTR, Promoter, Exon, Intron}, but it is free text.

4. **Site1_Chromosome**: Chromosome of Gene 1. 

5. **Site1_Contig**: The contig of Site 1. 

6. **Site1_Position**: Genomic position of breakpoint of Gene 1. 

7. **Site2_Entrez_Gene_Id**: [Entrez Gene](http://www.ncbi.nlm.nih.gov/gene) identifier of gene 2.  

8. **Site2_Region_Number**: Number of Site 2 region e.g. exon 4.

9. **Site2_Region**: We advise using one of these {5_PRIME_UTR, 3_PRIME_UTR, PROMOTER, EXON, INTRON}, but it is free text.  

10. **Site2_Chromosome**:  Chromosome of Gene 2.
 
11.  **Site2_Contig**:The contig of Site 2.

12.  **Site2_Position**: Genomic position of breakpoint of Gene 2.  

### Optional Fields

1. **Site1_Ensembl_Transcript_Id**: Ensembl transcript ID of gene 1.

2. **Site1_Description**: Description of this event at Site 2. This could be the location of the 2nd breakpoint in case of a fusion event.

3. **Site2_Description**: Description of this event at Site 1. This could be the location of the 1st breakpoint in case of a fusion event.

4. **Site2_Effect_On_Frame**: The effect on frame reading in gene 2. Frame_Shift or InFrame, but it is free text.

5. **NCBI_Build**: GRCh37 or GRCh38. Only one assembly per study can be used.
    
6. **Class**:  We advise using one of these terms [DELETION, DUPLICATION, INSERTION, INVERSION, TRANSLOCATION], but it is free text.  

7.  **Tumor_Split_Read_Count**: The number of split reads of the tumor tissue that support the call. [Tumor Split Read Count is the same as “Junction Reads”.]

8. **Tumor_Paired_End_Read_Count**: The number of paired-end reads of the tumor tissue that support the call. [Tumor Paired End Read Count is the same as “Spanning Fragments”.]  

9. **Event_Info**: Description of the event.Allowed values Antisense fusion, Deletion within transcript: mid-exon, Duplication of 1 exon: in frame  
    
10. **Connection_Type**: Which direction the connection is made (3' to 5', 5' to 3', etc). Allowed Values: 3to5, 5to3, 5to5, 3to3  

11. **Breakpoint_Type**: PRECISE or IMPRECISE, which explain the resolution. Fill in PRECISE if the breakpoint resolution is known down to the exact base pair. Allowed Values: PRECISE, IMPRECISE  
    
12. **Annotation**: Free text description of the gene or transcript rearrangement.

13. **DNA_Support**: Fusion detected from DNA sequence data.Allowed Values: Yes, No    
   
14. **RNA_Support**: Fusion detected from RNA sequence data. Allowed Values: Yes, No     

15. **SV_Length**: Length of the structural variant in number of bases.  

16. **Normal_Read_Count**: The total number of reads of the normal tissue.  

17. **Tumor_Read_Count**: The total number of reads of the tumor tissue.

18. **Normal_Variant_Count**: The number of reads of the normal tissue that have the variant/allele. 

19. **Tumor_Variant_Count**: The number of reads of the tumor tissue that have the variant/allele.  

20. **Normal_Paired_End_Read_Count**: The number of paired-end reads of the normal tissue that support the call.  

21. **Normal_Split_Read_Count**: The number of split reads of the normal tissue that support the call.  

22. **Comments**:  Any comments/free text.
    

## Reference

Fore more information on mutations files, please visit [this link](https://docs.cbioportal.org/file-formats/#structural-variant-data)