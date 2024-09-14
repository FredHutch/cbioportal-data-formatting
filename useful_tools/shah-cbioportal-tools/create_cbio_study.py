import os
import sys
import click
import hmmcopy
import pandas as pd
import remixt
import yaml
import logging

from convert_vcf_to_maf import generate_mafs, get_vcf_data, write_allele_counts, write_vcf
from merge_outputs import merge_all_data as merge_outputs
from os import path
from pathlib import Path
from shutil import copyfile
from utils import add_counts_to_maf, filter_vcfs

LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

def create_study_metadata(study_info, path_to_output_study):
    type_of_cancer = study_info['type_of_cancer']
    cancer_study_identifier = study_info['cancer_study_identifier']
    name = study_info['name']
    description = study_info['description']
    short_name = study_info['short_name']
    
    meta_study = open(path_to_output_study + 'meta_study.txt', 'w+')
    meta_study.write('type_of_cancer: ' + type_of_cancer + '\n' \
                    + 'cancer_study_identifier: ' + cancer_study_identifier + '\n' \
                    + 'name: ' + name + '\n' \
                    + 'description: ' + description + '\n' \
                    + 'short_name: ' + short_name + '\n' \
                    + 'add_global_case_list: true\n')

    meta_mutations_extended = open(path_to_output_study + 'meta_mutations_extended.txt', 'w+')
    meta_mutations_extended.write('cancer_study_identifier: ' + cancer_study_identifier + '\n' \
                    + 'genetic_alteration_type: MUTATION_EXTENDED\n' \
                    + 'datatype: MAF\n' \
                    + 'stable_id: mutations\n' \
                    + 'show_profile_in_analysis_tab: true\n' \
                    + 'profile_name: Mutations\n' \
                    + 'profile_description: Mutation data.\n' \
                    + 'data_filename: data_mutations_extended.maf\n')

    meta_CNA = open(path_to_output_study + 'meta_CNA.txt', 'w+')
    meta_CNA.write('cancer_study_identifier: ' + cancer_study_identifier + '\n' \
                    + 'genetic_alteration_type: COPY_NUMBER_ALTERATION\n' \
                    + 'datatype: DISCRETE\n' \
                    + 'stable_id: gistic\n' \
                    + 'show_profile_in_analysis_tab: true\n' \
                    + 'profile_name: Copy-number values\n' \
                    + 'profile_description: Copy-number values for each gene.\n' \
                    + 'data_filename: data_CNA.txt\n')
    
    meta_cna_seg = open(path_to_output_study + 'meta_cna_seg.txt', 'w+')
    meta_cna_seg.write('cancer_study_identifier: ' + cancer_study_identifier + '\n' \
                    + 'genetic_alteration_type: COPY_NUMBER_ALTERATION\n' \
                    + 'datatype: SEG\n' \
                    + 'reference_genome_id: hg19\n' \
                    + 'description: CNA data.\n' \
                    + 'data_filename: data_cna_hg19.seg\n')
    
    meta_clinical_sample = open(path_to_output_study + 'meta_clinical_sample.txt', 'w+')
    meta_clinical_sample.write('cancer_study_identifier: ' + cancer_study_identifier + '\n' \
                    + 'genetic_alteration_type: CLINICAL\n' \
                    + 'datatype: SAMPLE_ATTRIBUTES\n' \
                    + 'data_filename: data_clinical_sample.txt\n')
    
    data_clinical_sample = open(path_to_output_study + 'data_clinical_sample.txt', 'w+')
    data_clinical_sample.write('#Patient Identifier\tSample Identifier\tCancer Type\n' \
                    + '#Patient Identifier\tSample Identifier\tCancer Type description\n' \
                    + '#STRING\tSTRING\tSTRING\n' \
                    + '#1\t1\t1\n' \
                    + 'PATIENT_ID\tSAMPLE_ID\tCANCER_TYPE\n')
    
    case_list_ids = []
    for patient, patient_data in study_info['patients'].items():
        for sample, _ in patient_data.items():
            data_clinical_sample.write(patient + '\t' + sample + '\t' + type_of_cancer.upper() + '\n')
            case_list_ids.append(sample)
    
    Path(path_to_output_study + 'case_lists/').mkdir(parents=True, exist_ok=True)

    cases_cna = open(path_to_output_study + 'case_lists/cases_cna.txt', 'w+')
    cases_cna.write('cancer_study_identifier: ' + cancer_study_identifier + '\n' \
                    + 'stable_id: ' + cancer_study_identifier + '_cna\n' \
                    + 'case_list_name: Samples profiled for mutations\n' \
                    + 'case_list_description: Samples profiled for mutations\n' \
                    + 'case_list_ids: ')

    cases_cnaseq = open(path_to_output_study + 'case_lists/cases_cnaseq.txt', 'w+')
    cases_cnaseq.write('cancer_study_identifier: ' + cancer_study_identifier + '\n' \
                    + 'stable_id: ' + cancer_study_identifier + '_cnaseq\n' \
                    + 'case_list_name: Sequenced samples profiled for mutations\n' \
                    + 'case_list_description: Sequenced samples profiled for mutations\n' \
                    + 'case_list_ids: ')

    cases_sequenced = open(path_to_output_study + 'case_lists/cases_sequenced.txt', 'w+')
    cases_sequenced.write('cancer_study_identifier: ' + cancer_study_identifier + '\n' \
                    + 'stable_id: ' + cancer_study_identifier + '_sequenced\n' \
                    + 'case_list_name: All sequenced samples\n' \
                    + 'case_list_description: All sequenced samples\n' \
                    + 'case_list_ids: ')

    for sample_id in case_list_ids[:-1]:
        cases_cna.write(sample_id + '\t')
        cases_cnaseq.write(sample_id + '\t')
        cases_sequenced.write(sample_id + '\t')
    
    for f in [cases_cna, cases_cnaseq, cases_sequenced]:
        f.write(case_list_ids[-1] + '\n')

        
@click.command()
@click.argument('input_yaml')
@click.argument('path_to_output_study')
@click.argument('temp_dir')
def main(input_yaml, path_to_output_study, temp_dir):
    if not path_to_output_study.endswith('/'):
        path_to_output_study = path_to_output_study + '/'
    if not temp_dir.endswith('/'):
        temp_dir = temp_dir + '/'

    Path(path_to_output_study).mkdir(parents=True, exist_ok=True)
    Path(temp_dir).mkdir(parents=True, exist_ok=True)

    with open(input_yaml) as f:
        input_info = yaml.full_load(f)

        gene_locations_filename = input_info.get('gene_locations', 'gene_data/gene_locations.csv.gz')
        gene_locations = pd.read_csv(gene_locations_filename)

        vcf_files = {}
        gistic_files = {}
        seg_files = {}
        
        logging.info('creating study metadata')
        create_study_metadata(input_info, path_to_output_study)

        logging.info('processing patients')
        for patient_id, patient_data in input_info['patients'].items():
            for sample, sample_data in patient_data.items():
                logging.info(f'processing patient {patient_id}, sample {sample}')

                if sample_data['datatype'] == 'WGS':
                    if 'maf' not in sample_data:
                        vcf_files[sample] = []

                        if 'museq_vcf' in sample_data and 'strelka_vcf' in sample_data:
                            museq_filtered = filter_vcfs(sample, sample_data['museq_vcf'], sample_data['strelka_vcf'], temp_dir)
                            vcf_files[sample].append(museq_filtered)
                        
                        if 'strelka_indel_vcf' in sample_data:
                            vcf_files[sample].append(sample_data['strelka_indel_vcf'])

                    else:
                        copyfile(sample_data['maf'], temp_dir + sample + '.maf')
                        maf = pd.read_csv(temp_dir + sample + '.maf', dtype=str, sep='\t', skiprows=1)
                        maf['Tumor_Sample_Barcode'] = sample
                        maf.to_csv(temp_dir + sample + '.maf', index=None, sep='\t')

                    if 'remixt' in sample_data:
                        cn_data, stats_data = remixt.load_data(sample, sample_data)
                        aggregated_cn_data = remixt.generate_aggregated_cn(cn_data)
                        genes_cn_data = remixt.generate_genes_cn(aggregated_cn_data, gene_locations)
                        amp_data = remixt.generate_amp(genes_cn_data, stats_data, gene_locations)
                        hdel_data = remixt.generate_hdel(genes_cn_data, gene_locations)

                        amp_data['sample'] = sample
                        hdel_data['sample'] = sample
                        aggregated_cn_data['sample'] = sample

                        gistic_files[sample] = os.path.join(temp_dir, f'{patient_id}_{sample}.gistic')
                        seg_files[sample] = os.path.join(temp_dir, f'{patient_id}_{sample}.segs')

                        remixt.generate_gistic_outputs(gistic_files[sample], amp_data, hdel_data)
                        remixt.generate_seg_outputs(seg_files[sample], aggregated_cn_data, stats_data)

                elif sample_data['datatype'] == 'SCWGS':
                    hmmcopy_list = []
                    snv_counts = []
                    vcf_files[sample] = []

                    for library_id, library_data in sample_data.items():
                        if library_id == 'datatype':
                            continue

                        if 'museq_vcf' in library_data:
                            vcf_files[sample].append(library_data['museq_vcf'])
                        
                        if 'strelka_vcf' in library_data:
                            vcf_files[sample].append(library_data['strelka_vcf'])
                        
                        if 'strelka_indel_vcf' in library_data:
                            vcf_files[sample].append(library_data['strelka_indel_vcf'])

                        hmmcopy_list.append(library_data['hmmcopy_csv'])  
                        
                        if 'snv_counts_csv' in library_data:
                            snv_counts.append(library_data['snv_counts_csv'])

                    hmmcopy.merge_csv(hmmcopy_list, temp_dir)
                    
                    if snv_counts:
                        hmmcopy.calculate_counts(snv_counts, sample, temp_dir)
                    
                    cnv = hmmcopy.read_copy_data(temp_dir + 'hmmcopy_csv', filter_normal=False)
                    
                    overlapping = hmmcopy.calculate_gene_copy(cnv, gene_locations)
                    hmmcopy.convert_to_transform_format(overlapping, temp_dir)

                    hmmcopy_extract = open(temp_dir + 'hmmcopy_extract', 'r')
                    gene_dict, seg_dict = hmmcopy.transform(hmmcopy_extract)
                    hmmcopy.load(gene_dict, seg_dict, sample, temp_dir)

                else:
                    raise ValueError(f'unrecognized data type {sample_data["datatype"]}')
        
        if vcf_files:
            logging.info('generating mafs')

            vcf_outputs = {sample: path.join(temp_dir, '{}.vcf'.format(sample)) for sample in vcf_files}
            csv_outputs = {sample: path.join(temp_dir, '{}.csv'.format(sample)) for sample in vcf_files}
            maf_outputs = {sample: path.join(temp_dir, '{}.maf'.format(sample)) for sample in vcf_files}

            for sample, sample_vcf_files in vcf_files.items():
                vcfdata = get_vcf_data(sample_vcf_files)
                write_vcf(vcf_outputs[sample], sample_vcf_files, vcfdata, temp_dir, sample)
                write_allele_counts(csv_outputs[sample], vcfdata)

            generate_mafs(vcf_files, temp_dir, maf_outputs, vcf_outputs)

        logging.info('adding counts to mafs')
        for patient_id, patient_data in input_info['patients'].items():
            for sample, _ in patient_data.items():
                n_file = Path(temp_dir + sample + '.csv')
            
                maf = Path(temp_dir + sample + '.maf')
                if n_file.is_file() and maf.is_file():
                    add_counts_to_maf(sample, temp_dir)

    logging.info('merging patient data')
    merge_outputs(temp_dir, path_to_output_study)


if __name__ == '__main__':
    logging.basicConfig(format=LOGGING_FORMAT, stream=sys.stderr, level=logging.INFO)
    main()
