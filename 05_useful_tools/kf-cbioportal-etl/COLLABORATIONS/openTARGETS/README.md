# OpenPedCan
This project is organized much like OpenPBTA in which all genomics data for each assay-type are collated into one giant table.
In general, this fits cBioPortal well.
A summary example run script can be found [here](COLLABORATIONS/openTARGETS/example_run.sh), with example file download list [here](COLLABORATIONS/openTARGETS/dl_list.txt)

See `https://pedcbioportal.kidsfirstdrc.org/study/summary?id=openpedcan_v12` for final product.

## Inputs
Inputs are located in the old D3b AWS account (`684194535433`) in this general bucket location: `s3://d3b-openaccess-us-east-1-prd-pbta/open-targets/`.
Clinical data with cBio names are obtained from the `histologies-formatted-id-added.tsv` file, as noted in [Prep Work section](#prep-work).
Genomic data generally obtained as such:
 - Somatic variant calls: merged maf
 - Copy number: tsv file with copy number, ploidy, and GISTIC-style information in maf-like format (each call is a row)
 - RNA expression: tpm values from rsem stored an `.rds` object
 - RNA fusion: annoFuse output
For example, for v14, bucket s3://d3b-openaccess-us-east-1-prd-pbta/open-targets/v14/:
```
consensus_wgs_plus_cnvkit_wxs_plus_freec_tumor_only.tsv.gz
fusion-dgd.tsv.gz
fusion-putative-oncogenic.tsv
gene-expression-rsem-tpm-collapsed.rds
tcga_gene-expression-rsem-tpm-collapsed.rds
gtex_gene-expression-rsem-tpm-collapsed.rds
snv-consensus-plus-hotspots.maf.tsv.gz
snv-mutect2-tumor-only-plus-hotspots.maf.tsv.gz
```

### Prep work
The histologies file needs `formatted_sample_id` added and likely a blacklist from the D3b Warehouse or some other source to suppress duplicate RNA libraries from different sequencing methods.
Since we are not handling `Methylation` yet, it is recommended those entries be removed ahead of time.
To create the histologies file, recommended method is to:
1. `docker pull pgc-images.sbgenomics.com/d3b-bixu/open-pedcan:latest` OR if you have R installed locally, ensure the following libraries are installed:
    ```R
    library("optparse")
    library("tidyverse")
    library("readr")
    library("tidyr")
    ```

1. Pull the OpenPedCan repo (warning, it's 12GB ): https://github.com/PediatricOpenTargets/OpenPedCan-analysis, or just download the script from `analyses/pedcbio-sample-name/pedcbio_sample_name_col.R`
1. Export from D3b Warehouse the latest existing cBio IDs to use for population. Ensure that the output is csv double-quoted. Currently that can be obtained using the sql command:
    ```sql
    with custom as (
    select participant_id, formatted_sample_id, specimen_id, analyte_types, normal_bs_id, normal_sample_id
    from prod_cbio.aml_sd_pet7q6f2_2018_cbio_sample
    union
    select participant_id, formatted_sample_id, specimen_id, analyte_types, normal_bs_id, normal_sample_id
    from prod_cbio.bllnos_sd_z6mwd3h0_2018_cbio_sample
    union
    select participant_id, formatted_sample_id, specimen_id, analyte_types, normal_bs_id, normal_sample_id
    from prod_cbio.x01_fy16_nbl_maris_cbio_sample
    union
    select participant_id, formatted_sample_id, specimen_id, analyte_types, normal_bs_id, normal_sample_id
    from prod_cbio.cbtn_cbio_sample
    union
    select participant_id, formatted_sample_id, specimen_id, analyte_types, normal_bs_id, normal_sample_id
    from prod_cbio.dgd_cbio_sample
    union
    select participant_id, formatted_sample_id, specimen_id, analyte_types, normal_bs_id, normal_sample_id
    from prod_cbio.pnoc_cbio_sample
    union
    select participant_id, formatted_sample_id, specimen_id, analyte_types, normal_bs_id, normal_sample_id
    from prod_cbio.oligo_nation_cbio_sample
    union
    select participant_id, formatted_sample_id, specimen_id, analyte_types, normal_bs_id, normal_sample_id
    from prod_cbio.os_sd_zxjffmef_2015_cbio_sample
	  union
    select participant_id, formatted_sample_id, specimen_id, analyte_types, normal_bs_id, normal_sample_id
    from prod_cbio.chdm_sd_7spqtt8m_cbio_sample
	  union
    select participant_id, formatted_sample_id, specimen_id, analyte_types, normal_bs_id, normal_sample_id
    from prod_cbio.chdm_phs001643_2018_cbio_sample
    union
    select participant_id, formatted_sample_id, specimen_id, analyte_types, normal_bs_id, normal_sample_id
    from prod_cbio.pbta_mioncoseq_cbio_sample
    )
    select * from custom

    ```
1. Get a blacklist from D3b Warehouse, exporting table `bix_workflows.cbio_hide_reasons`

### Run as standalone
1. Download from https://github.com/PediatricOpenTargets/OpenPedCan-analysis the `analyses/pedcbio-sample-name/pedcbio_sample_name_col.R` or run from repo if you have it
1. Run `Rscript --vanilla pedcbio_sample_name_col.R -i path-to-histologies-file.tsv -n path-to-cbio-names.csv -b 'Methylation,Phospho-Proteomics,Whole Cell Proteomics,miRNA-Seq'`
OR
### Run in repo
1. Either run an interactive docker or using your local R, and ensure to mount a volume that will have the repo and whatever input histologies file you end up using, i.e. `docker run -it --mount type=bind,source=/home/ubuntu,target=/WORK pgc-images.sbgenomics.com/d3b-bixu/open-pedcan:latest /bin/bash`
1. In that container, go to the location of `analyses/pedcbio-sample-name/pedcbio_sample_name_col.R`
1. Run `pedcbio-sample-name/pedcbio_sample_name_col.R -i ../molecular-subtyping-integrate/results/histologies.tsv -b Methylation`. Results will be in `results` as `histologies-formatted-id-added.tsv`

### RNA rsem input prep
TCGA data are kept in a seprate matrix from everything else. We need to merge those. It is collapsed on common genes:
```sh
Rscript COLLABORATIONS/openTARGETS/merge_rsem_rds.R --first_file gene-expression-rsem-tpm-collapsed.rds --second_file tcga-gene-expression-rsem-tpm-collapsed.rds --output_fn gene_tcga_expression_common_merge.rds
```
UPDATE: GTEx is also in a seprate matrix, so run again currently to make the "final" merge before conversion
```sh
Rscript COLLABORATIONS/openTARGETS/merge_rsem_rds.R --first_file gene_tcga_expression_common_merge.rds --second_file gtex_gene-expression-rsem-tpm-collapsed.rds --output_fn gene_tcga_gtex_expression_common_merge.rds
```
```

### File Transformation
It's recommended to put datasheets in a dir called `datasheets`, downloaded files in it's own dir (in v12 it's `GF_INPUTS`) and the rest of the processed outputs into it's own dir (`study_build` for v12) to keep things sane and also be able to leverage existing study build script in `scripts/organize_upload_packages.py`
#### 1. COLLABORATIONS/openTARGETS/clinical_to_datasheets.py
 ```
usage: clinical_to_datasheets.py [-h] [-f HEAD] [-c CLIN] [-s CL_SUPP]

Script to convert clinical data to cbio clinical data sheets

optional arguments:
  -h, --help            show this help message and exit
  -f HEAD, --header-file HEAD
                        tsv file with input file original sample names, output
                        sheet flag, and conversion
  -b BLACKLIST, --blacklist BLACKLIST
                        because every club needs a bouncer. Headered tsv file with BS ID and reason
  -c CLIN, --clinical-data CLIN
                        Input clinical data sheet
  -s CL_SUPP, --cell-line-supplement CL_SUPP
                        supplemental file with cell line meta data - bs
                        id<tab>type. optional
 ```
 - `-f` Header file example can be found here: `COLLABORATIONS/openTARGETS/header_desc.tsv`
 - `-s` cell line supplemental file here: `REFS/cell_line_supplemental.txt`
 - `-b` blacklist exported from D3b Warehouse
 - `-c` `histologies-formatted-id-added.tsv`

 Outputs a `data_clinical_sample.txt` and `data_clinical_patient.txt` for the cBio package, and a `bs_id_sample_map.txt` mapping file to link BS IDs to gnerated cBioPortal IDs based on the rules for creating a proper somatic event using column `parent_aliquot_id`

Example run:
`python3 COLLABORATIONS/openTARGETS/clinical_to_datasheets.py -f COLLABORATIONS/openTARGETS/header_desc.tsv -c histologies-formatted-id-added.tsv -b cbio_hide_reasons.tsv 2> clin.errs`

#### 2. COLLABORATIONS/openTARGETS/rename_filter_maf.py

Rename IDs in `Tumor_Sample_Barcode`
```
usage: rename_filter_maf.py [-h] [-m MAPPING_FILE] [-v MAF_FILE]

Script to pre-filter entries on usually removed criteria except TERT
promoter, convert BS IDs to cBio names

optional arguments:
  -h, --help            show this help message and exit
  -m MAPPING_FILE, --mapping-file MAPPING_FILE
                        tsv file with header and bs_id, sample type, cbio ID mappings
  -v MAF_FILE, --maf-file MAF_FILE
                        openX maf file
  -s SKIP, --skip SKIP  Skip typical #version header line
  -n TYPE, --study TYPE
                        study name, like "openpbta"
```
_NOTE_ for v11 input, I ran the following command `zcat snv-dgd.maf.tsv.gz | perl -e '$skip = <>; $skip= <>; while(<>){print $_;}' | gzip -c >> snv-consensus-plus-hotspots.maf.tsv.gz` to add DGD data

_NOTE_ for v15 input,I would have following command `python3 ~/tools/kf-cbioportal-etl/COLLABORATIONS/openTARGETS/append_maf_to_existing.py -i /home/ubuntu/tools/kf-cbioportal-etl/COLLABORATIONS/openTARGETS/maf_openpedcan_v15_header.txt -c openpedcan_v15.maf -t ../INPUT_PREP/bs_id_sample_map.txt -m ../INPUTS/snv-mutect2-tumor-only-plus-hotspots.maf.tsv.gz` to add tumor-only data, which is more robust

Example run:
`python3 COLLABORATIONS/openTARGETS/rename_filter_maf.py -m bs_id_sample_map.txt -v snv-consensus-plus-hotspots.maf.tsv.gz -s 1 -n openpedcan_v12`

#### 3. COLLABORATIONS/openTARGETS/cnv_to_tables.py
Convert cnv table to cBio format - genes as rows, samples as cols, one for absolute CN, another for GISTIC-style
```
usage: cnv_to_tables.py [-h] [-m MAPPING_FILE] [-c CNV_TBL]

Script to convert openX cnv table to cBio format

optional arguments:
  -h, --help            show this help message and exit
  -m MAPPING_FILE, --mapping-file MAPPING_FILE
                        tsv file with header and bs_id, sample type, cbio ID mappings
  -c CNV_TBL, --copy-number CNV_TBL
                        openX table
  -s TYPE, --study TYPE
                        study name, like "openpbta"
```

Example run:
`python3 COLLABORATIONS/openTARGETS/cnv_to_tables.py -m bs_id_sample_map.txt  -c consensus_wgs_plus_cnvkit_wxs.tsv.gz -s openpedcan_v11`

#### 4. COLLABORATIONS/openTARGETS/rename_export_rsem.R
Note, I merged the tcga into the main rds. I also needed an instance with _64GB ram_ in order to calc z scores. Update: Can also achieve by setting up 32GB swap space 
Additionally,can also use C++ implementation to speed up zscore computation and save memory. Note: writing in C++ is slower than write_tsv function in R but have less memory footprint.
```
Usage: /home/ubuntu/tools/kf-cbioportal-etl/COLLABORATIONS/openTARGETS/rename_export_rsem.R [options]


Options:
	--rna_rds=RNA_RDS
		openX rsem rds expression object

	--map_id=MAP_ID
		mapping ID file with headers: BS_ID	Sample Type	Cbio ID

	--type=TYPE
		study name, like 'openpbta'

	--computeZscore=R/C++
		Implementation to use C++ or R to compute zscore and write a tsv file

	-h, --help
		Show this help message and exit
```
Example run:
`Rscript COLLABORATIONS/openTARGETS/rename_export_rsem.R --rna_rds gene_tcga_gtex_expression_common_merge.rds --map_id bs_id_sample_map.txt --type openpedcan_v15 --computeZscore R 2> rna_convert.errs`

#### 5. scripts/convert_fusion_as_sv.py

Before running, to leverage an existing fusion conversion, I first ran:
`COLLABORATIONS/openTARGETS/reformat_cbio_sample_index.py -t bs_id_sample_map.txt -n openpedcan_v12 > fusion_sample_name_input.txt`
to reformat the sample name index.
```
usage: convert_fusion_as_sv.py [-h] [-t TABLE] [-f FUSION_RESULTS] [-o OUT_DIR] -m MODE

Convert openPBTA fusion table OR list of annofuse files to cbio format.

optional arguments:
  -h, --help            show this help message and exit
  -t TABLE, --table TABLE
                        Table with cbio project, kf bs ids, cbio IDs, and file names
  -f FUSION_RESULTS, --fusion-results FUSION_RESULTS
                        annoFuse results dir OR openX merged fusion file
  -o OUT_DIR, --out-dir OUT_DIR
                        Result output dir. Default is merged_fusion
  -m MODE, --mode MODE  describe source, openX or kfprod
```
Example run:
`python3 ~/tools/kf-cbioportal-etl/scripts/convert_fusion_as_sv.py -t fusion_sample_name_input.txt -f fusion-putative-oncogenic.tsv -o ./ -m openX`
If DGD fusions are to be added, run again with `-a` flag like so:
`python3 ~/tools/kf-cbioportal-etl/scripts/convert_fusion_as_sv.py -t fusion_sample_name_input.txt -f fusion-dgd.tsv.gz -o ./ -m dgd -a`

#### 6. scripts/organize_upload_packages.py
Leverage the existing meta config and package organizer from kids first to create all relevant meta and case files...except for the added case lists achieved by the next step
```
Create cases lists, meta files, and organize data for cbio upload. It is assumed you are at the dir level of all input data files

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_DIR, --output_dir OUT_DIR
                        output directory name
  -c CONFIG_FILE, --config CONFIG_FILE
                        json config file with meta information; see REFS/case_meta_config.json example
```
Example run:
`python3 scripts/organize_upload_packages.py -o processed -c COLLABORATIONS/openTARGETS/openpedcan_v12_case_meta_config.json`

#### 7. COLLABORATIONS/openTARGETS/case_list_from_datasheet.py
Last step before validation and upload
```
usage: case_list_from_datasheet.py [-h] [-d DATASHEET] [-s STUDY_ID]

Generate extra cases lists based on cBio datasheet

optional arguments:
  -h, --help            show this help message and exit
  -d DATASHEET, --datasheet DATASHEET
                        cBio sample datasheet
  -s STUDY_ID, --study-id STUDY_ID
                        cBio cancer_study_identifier
  -c COHORTS, --cohort-csv COHORTS
                        add a special case for a cohort-specific case list using a csv list and omit from hist split
  -m SAMP_MIN, --min-sample SAMP_MIN
                        min number of samples a cohort must have to generate a case list for. recommend 3
```

Example run:
`python3 COLLABORATIONS/openTARGETS/case_list_from_datasheet.py -d data_clinical_sample.txt -s openpedcan_v12 -c GTEx -m 3`
