# OpenPBTA
Quite similar to OpenPedCan with some caveats

## Prep Work
1. Obtain files from `s3://d3b-openaccess-us-east-1-prd-pbta/data/release-xxx`, with the `xxx` being a release version of interest.
  Files to get includes:
  ```
  pbta-histologies.tsv
  consensus_seg_annotated_cn_x_and_y.tsv.gz
  consensus_seg_annotated_cn_autosomes.tsv.gz
  pbta-snv-consensus-mutation.maf.tsv.gz
  pbta-snv-scavenged-hotspots.maf.tsv.gz
  pbta-gene-expression-rsem-fpkm-collapsed.polya.rds
  pbta-gene-expression-rsem-fpkm-collapsed.stranded.rds
  pbta-fusion-putative-oncogenic.tsv.gz
  pbta-cnv-consensus.seg.gz
  ```
1. Create complete maf:
  `python3 COLLABORATIONS/openPBTA/merge_pbta_file_columns.py -1 pbta-snv-consensus-mutation.maf.tsv.gz -2 pbta-snv-scavenged-hotspots.maf.tsv.gz -o pbta-snv-consensus-plus-hotspots.maf`
1. Create complete rsem rds:
  `Rscript COLLABORATIONS/openPBTA/merge_rsem_rds.R --stranded pbta-gene-expression-rsem-fpkm-collapsed.stranded.rds --polya pbta-gene-expression-rsem-fpkm-collapsed.polya.rds`
1. Create complete cnv tsv:
  `python3 COLLABORATIONS/openPBTA/merge_pbta_file_columns.py -1 consensus_seg_annotated_cn_autosomes.tsv.gz -2 consensus_seg_annotated_cn_x_and_y.tsv.gz -o consensus_seg_annotated_cn.tsv`
## Create study
Uses many of the same scripts as open targets
### 1. Create clinical data sheets
Histologies file is parsed and scplit into `data_clinical_sample.txt` and `data_clinical_patient.txt`
```sh
python3 COLLABORATIONS/openPBTA/clinical_to_datasheets.py -h
usage: clinical_to_datasheets.py [-h] [-f HEAD] [-c CLIN] [-b BLACKLIST] [-p PBTA_DS]

Script to convert clinical data to cbio clinical data sheets

optional arguments:
  -h, --help            show this help message and exit
  -f HEAD, --header-file HEAD
                        tsv file with input file original sample names, output sheet flag, and conversion
  -c CLIN, --clinical-data CLIN
                        Input clinical data sheet
  -b BLACKLIST, --blacklist BLACKLIST
                        because every club needs a bouncer. Headered tsv file with BS ID and reason
  -p PBTA_DS, --pbta-all-data-sample-sheet PBTA_DS
                        pbta_all sample sheet to use as sample name source
```
Example: `python3 ~/tools/kf-cbioportal-etl/COLLABORATIONS/openPBTA/clinical_to_datasheets.py -f ~/tools/kf-cbioportal-etl/COLLABORATIONS/openPBTA/header_desc.tsv -c pbta-histologies.tsv -p /home/ubuntu/mount/pbta_all/processed/pbta_all/data_clinical_sample.txt -b cbio_hide_reasons_subset.tsv 2> clin2.err`
cBio hide reasons table is exported from D3b warehouse
### 2. Rename and filter maf file
Filter out Silent, Intron, IGR, 3'UTR, 5'UTR, 3'Flank, 5'Flank, RNA and rename samples to cBio IDs
```sh
python3 COLLABORATIONS/openTARGETS/rename_filter_maf.py -h
usage: rename_filter_maf.py [-h] [-m MAPPING_FILE] [-v MAF_FILE] [-s SKIP] [-n TYPE]

Script to pre-filter entries on usually removed criteria except TERT promoter, convert BS IDs to cBio names

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
Example: `python3 /home/ubuntu/tools/kf-cbioportal-etl/COLLABORATIONS/openTARGETS/rename_filter_maf.py -m ../bs_id_sample_map.txt -v ../pbta-snv-consensus-plus-hotspots.maf.tsv -n openpbta`
Mapping file is an output from step 1
### Convert CNV to cBio CNV tables
Predicted: Just plain copy number, discrete: GISTIC-style assignment
```sh
python3 ~/tools/kf-cbioportal-etl/COLLABORATIONS/openTARGETS/cnv_to_tables.py -h
usage: cnv_to_tables.py [-h] [-m MAPPING_FILE] [-c CNV_TBL] [-s TYPE]

Script to convert openX cnv table to cBio format

optional arguments:
  -h, --help            show this help message and exit
  -m MAPPING_FILE, --mapping-file MAPPING_FILE
                        tsv file with header and bs_id, sample type, cbio ID mappings
  -c CNV_TBL, --copy-number CNV_TBL
                        openX tables, listed as csv since they tend to seprate autosomes, xy
  -s TYPE, --study TYPE
                        study name, like "openpbta"
```
Example: `python3 COLLABORATIONS/openTARGETS/cnv_to_tables.py -m ../bs_id_sample_map.txt -c ../consensus_seg_annotated_cn.tsv -s openpbta`
### Rename rsem
Mostly just rename samples and export as text. Also z score output
```sh
Rscript COLLABORATIONS/openTARGETS/rename_export_rsem.R --help
Loading required package: data.table
Loading required package: optparse
Loading required package: Rcpp
Loading required package: funr
Loading required package: readr
Usage: COLLABORATIONS/openTARGETS/rename_export_rsem.R [options]


Options:
        --rna_rds=RNA_RDS
                openX rsem rds expression object

        --map_id=MAP_ID
                mapping ID file with headers: BS_ID    Sample Type    Cbio ID

        --type=TYPE
                study name, like 'openpbta'

        --computeZscore=COMPUTEZSCORE
                Use C++ Method to compute zscore and write file. Usage: C++ or R

        -h, --help
                Show this help message and exit
```
Example: `Rscript COLLABORATIONS/openTARGETS/rename_export_rsem.R --rna_rds ../pbta-gene-expression-rsem-fpkm-collapsed.rds --map_id ../bs_id_sample_map.txt --computeZscore C++ --type openpbta`
### Convert fusion as SV
cBio has a "new" format  with a richer SV input. More data can be ported over.
For compatibility, since standard study conversion script is used, first run: `python3 COLLABORATIONS/openTARGETS/reformat_cbio_sample_index.py -t ../bs_id_sample_map.txt -n openpbta > fusion_sample_table.txt`
Then:
```sh
python3 scripts/convert_fusion_as_sv.py -h
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
  Example: `python3 /home/ubuntu/tools/kf-cbioportal-etl/scripts/convert_fusion_as_sv.py -t fusion_sample_table.txt -f ../pbta-fusion-putative-oncogenic.tsv -m openX`
### Organize and create links
This script creates meta files and case lists needed for cBio loading
```sh
python3 scripts/organize_upload_packages.py -h
usage: organize_upload_packages.py [-h] [-o OUT_DIR] [-c CONFIG_FILE] [-l]

Create cases lists, meta files, and organize data for cbio upload. It is assumed you are at the dir level of all input data files

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_DIR, --output_dir OUT_DIR
                        output directory name
  -c CONFIG_FILE, --config CONFIG_FILE
                        json config file with meta information; see REFS/case_meta_config.json example
  -l, --legacy          If set, will run legacy fusion output
  ```
  Example: `python3 /home/ubuntu/tools/kf-cbioportal-etl/scripts/organize_upload_packages.py -o processed -c /home/ubuntu/tools/kf-cbioportal-etl/COLLABORATIONS/openPBTA/openpbta_case_meta_config.json`