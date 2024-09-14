# create dir to house downloaded files
mkdir GF_INPUTS && cd GF_INPUTS
# Use file name list to grab from release bucket. May need to change version
cat dl_list.txt | xargs -IFN -P 8 aws s3 cp --no-sign-request s3://d3b-openaccess-us-east-1-prd-pbta/open-targets/v12/FN .
# Merge expression file and TCGA-specific expression file
Rscript ~/tools/kf-cbioportal-etl/COLLABORATIONS/openTARGETS/merge_rsem_rds.R --first_file gene-expression-rsem-tpm-collapsed.rds --second_file tcga-gene-expression-rsem-tpm-collapsed.rds --output_fn gene_tcga_expression_common_merge.rds
# add existing cbio names to script (see README)
cd ../ && Rscript --vanilla /home/ubuntu/tools/kf-cbioportal-etl/COLLABORATIONS/openTARGETS/pedcbio_sample_name_col.R -i GF_INPUTS/histologies.tsv -n cbio_sample_ids.csv -b Methylation &> format.log
# convert histologies to data_clinical sheets
python3 ~/tools/kf-cbioportal-etl/COLLABORATIONS/openTARGETS/clinical_to_datasheets.py -f ~/tools/kf-cbioportal-etl/COLLABORATIONS/openTARGETS/header_desc.tsv -c histologies-formatted-id-added.tsv -b cbio_hide_reasons.txt 2> clin.errs
mkdir datasheets && mv data_clinical_* datasheets
mkdir study_build && cd study_build
# Create merged maf
python3 ~/tools/kf-cbioportal-etl/COLLABORATIONS/openTARGETS/rename_filter_maf.py -m ../bs_id_sample_map.txt -v ../GF_INPUTS/snv-consensus-plus-hotspots.maf.tsv.gz -n openpedcan_v12 2> ../maf.errs &
# Create merged cnv
python3 ~/tools/kf-cbioportal-etl/COLLABORATIONS/openTARGETS/cnv_to_tables.py -m ../bs_id_sample_map.txt  -c ../GF_INPUTS/consensus_wgs_plus_cnvkit_wxs.tsv.gz -s openpedcan_v12 2> ../cnv.errs &
# Create merged expression. This one takes a while!
Rscript ~/tools/kf-cbioportal-etl/COLLABORATIONS/openTARGETS/rename_export_rsem.R --rna_rds ../GF_INPUTS/gene_tcga_expression_common_merge.rds --map_id ../bs_id_sample_map.txt --type openpedcan_v12 --computeZscore C++ 2> ../rsem.errs &
# Reformat to sample ID map to fit requirements of existing SV script and run SV conversion for fusions
python3 ~/tools/kf-cbioportal-etl/COLLABORATIONS/openTARGETS/reformat_cbio_sample_index.py -t ../bs_id_sample_map.txt -n openpedcan_v12 > ../fusion_sample_name_input.txt
python3 ~/tools/kf-cbioportal-etl/scripts/convert_fusion_as_sv.py -t ../fusion_sample_name_input.txt -f ../GF_INPUTS/fusion-putative-oncogenic.tsv -o ./ -m openX 2> ../fusion.errs &
python3 ~/tools/kf-cbioportal-etl/scripts/convert_fusion_as_sv.py -t ../fusion_sample_name_input.txt -f ../GF_INPUTS/fusion-dgd.tsv.gz -o ./ -m dgd -a 2>> ../fusion.errs
# Create load packages
cd ../ && python3 ~/tools/kf-cbioportal-etl/scripts/organize_upload_packages.py -o processed -c ~/tools/kf-cbioportal-etl/COLLABORATIONS/openTARGETS/openpedcan_v12_case_meta_config.json
# Create added case lists
cd processed/openpedcan_v12/case_lists && python3 ~/tools/kf-cbioportal-etl/COLLABORATIONS/openTARGETS/case_list_from_datasheet.py -d ../data_clinical_sample.txt -s openpedcan_v12 -c GTEx -m 3 2> ../../../cases.log
# Validate project
cd ../../ && /home/ubuntu/tools/cbioportal/core/src/main/scripts/importer/validateData.py -s openpedcan_v12 -n -v 2> v5_validator.errs > v5_validator.out &
# Upload to bucket
aws s3 cp openpedcan_v12 s3://kf-cbioportal-studies/public/openpedcan_v12/ --recursive --profile saml