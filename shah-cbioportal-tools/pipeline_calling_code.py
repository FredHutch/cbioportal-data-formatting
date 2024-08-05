import click
import gzip
import yaml

from filter_vcfs import filter_vcfs
from generate_outputs import extract, transform, load
from merge_outputs import merge_all_data as merge_outputs
from pathlib import Path


def generate_outputs(gtf_file, hgnc_file, titan_igv, titan_segs, sample_id, output_dir): 
    extracted_file = extract(gtf_file, hgnc_file, titan_igv, titan_segs)
    gene_dict, seg_dict = transform(extracted_file, show_missing_hugo=False, show_missing_entrez=False, show_missing_both=False)
    load(gene_dict, seg_dict, sample_id, output_dir, output_gistic_gene=True, output_integer_gene=False, output_log_seg=True, output_integer_seg=False)


@click.command()
@click.argument('input_yaml')
@click.argument('temp_dir')
def main(input_yaml, temp_dir):
    if not temp_dir.endswith('/'):
        temp_dir = temp_dir + '/'

    Path(temp_dir).mkdir(parents=True, exist_ok=True)

    with open(input_yaml) as file:
        yaml_file = yaml.full_load(file)
        hgnc_file = yaml_file['id_mapping']
        gtf_file = yaml_file['gtf']
        
        create_study(yaml_file['patients'], path_to_output_study)

        for _, doc in yaml_file['patients'].items():
            for sample, doc in doc.items():
                museq_filtered = filter_vcfs(sample, doc['museq_vcf'], doc['strelka_vcf'], temp_dir)
                '''
                HERE: convert museq_filtered and strelka_indel
                vcfs into .mafs (pass sample into vcf2maf as
                --tumor-id argument)
                '''
                with gzip.open(doc['titan_igv'], 'rt') as titan_igv, gzip.open(doc['titan_segs'], 'rt') as titan_segs:
                    generate_outputs(gtf_file, hgnc_file, titan_igv, titan_segs, sample, temp_dir)        
        
    merge_outputs(temp_dir, path_to_output_study)    


if __name__ == '__main__':
    main()
