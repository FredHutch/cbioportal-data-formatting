#!/bin/bash

#############################################################
# This script is more of a guide on how to export all the   #
# necessary clinical files and manifests from D3b Warehouse #
#############################################################

# CBTN Genomic files manifest
psql -h d3b-warehouse-aurora-prd.d3b.io -U brownm28 postgres -c "SET search_path TO bix_workflows; COPY(select * from \"sd_bhjxbdqk-genomics_file_manifest\" where file_type in ('RSEM_gene','annofuse_filtered_fusions_tsv','annotated_public_outputs','ctrlfreec_pval','ctrlfreec_info','ctrlfreec_bam_seg')) TO STDOUT WITH CSV HEADER DELIMITER E'\t'" > cbtn_genomics_file_manifest.txt
# PNOC Genomic files manifest
psql -h d3b-warehouse-aurora-prd.d3b.io -U brownm28 postgres -c "SET search_path TO bix_workflows; COPY(select * from \"sd_8y99qzjj-genomics_file_manifest\" where file_type in ('RSEM_gene','annofuse_filtered_fusions_tsv','annotated_public_outputs','ctrlfreec_pval','ctrlfreec_info','ctrlfreec_bam_seg')) TO STDOUT WITH CSV HEADER DELIMITER E'\t'" > pnoc_genomics_file_manifest.txt
# DGD Genomic files manifest
psql -h d3b-warehouse-aurora-prd.d3b.io -U brownm28 postgres -c "SET search_path TO welshm3_dev_schema; COPY(select biospecimen_id,trim(trailing from sample_type) as sample_type,participant_id,case_id,normal_id,tumor_id,family_id,file_name,trim(trailing from file_type) as file_type,trim(trailing from workflow_type) as workflow_type,trim(trailing from experiment_strategy) as experiment_strategy,volume_name,s3_path,aws_account,aws_role from genomics_file_manifest where file_type in ('DGD_MAF', 'DGD_FUSION')) TO STDOUT WITH CSV HEADER DELIMITER E'\t'" > dgd_genomics_file_manifest.txt
# Genomics metadata file: often the -t arg input
psql -h d3b-warehouse-aurora-prd.d3b.io -U brownm28 postgres -c "SET search_path TO prod_cbio; COPY(select * from pbta_all_genomics_etl_file) TO STDOUT WITH CSV HEADER DELIMITER E'\t'" > cbio_file_name_id.txt
# Data clinical sample sheet - until a better function is written, need to output header lines first, then append data
psql -h d3b-warehouse-aurora-prd.d3b.io -U brownm28 postgres -c "SET search_path TO bix_workflows; COPY(select * from data_clinical_sample_header) TO STDOUT WITH CSV DELIMITER E'\t'" > datasheets/data_clinical_sample.txt
psql -h d3b-warehouse-aurora-prd.d3b.io -U brownm28 postgres -c "SET search_path TO prod_cbio; COPY(select * from pbta_all_data_clinical_sample) TO STDOUT WITH CSV HEADER DELIMITER E'\t'" >> datasheets/data_clinical_sample.txt
# Data clinical patient sheet - same notes as sample
psql -h d3b-warehouse-aurora-prd.d3b.io -U brownm28 postgres -c "SET search_path TO bix_workflows; COPY(select * from data_clinical_patient_header) TO STDOUT WITH CSV DELIMITER E'\t'" > datasheets/data_clinical_patient.txt
psql -h d3b-warehouse-aurora-prd.d3b.io -U brownm28 postgres -c "SET search_path TO prod_cbio; COPY(select * from pbta_all_data_clinical_patient) TO STDOUT WITH CSV HEADER DELIMITER E'\t'" >> datasheets/data_clinical_patient.txt
# Data gene matrix
psql -h d3b-warehouse-aurora-prd.d3b.io -U brownm28 postgres -c "SET search_path TO prod_cbio; COPY(select * from pbta_all_data_gene_matrix) TO STDOUT WITH CSV HEADER DELIMITER E'\t'" > datasheets/data_gene_matrix_CHOP.txt
# Sequencing Center Resource File
psql -h d3b-warehouse-aurora-prd.d3b.io -U brownm28 postgres -c "SET search_path TO prod_cbio; COPY(select * from pbta_all_sq_info_etl_resource) TO STDOUT WITH CSV HEADER DELIMITER E'\t'" > seq_center_resource.txt