import click
import glob
import numpy as np
import os
import pandas as pd

from collections import Counter


# merge multiple gistic OR integer gene data text files
def merge_gistic_gene_data(input_dir, output_dir):
    files_to_merge = [fn for fn in glob.glob(input_dir + '*.txt')]
    
    if not files_to_merge:
        print('No .txt files found. Please add some and rerun.')
        return

    files_to_merge = sorted(files_to_merge)
    files_with_issues = []
    dfs_to_merge = []

    for file in files_to_merge:
        data_frame = pd.read_csv(file, delimiter='\t', dtype=str)
        
        if list(data_frame)[0] != 'Hugo_Symbol' or list(data_frame)[1] != 'Entrez_Gene_Id':
            files_with_issues.append(file)
            continue
        
        dfs_to_merge.append(data_frame)

    if files_with_issues:
        print('The following list contains gistic gene data files that could not be merged:')
        print(files_with_issues)
        print('Please fix or remove them and rerun the merge script.')
        return

    merged_file = dfs_to_merge.pop(0)
    
    while dfs_to_merge:
        merged_file = pd.merge(merged_file, dfs_to_merge.pop(), on=['Hugo_Symbol', 'Entrez_Gene_Id'], how='outer')

    merged_file[['Entrez_Gene_Id']] = merged_file[['Entrez_Gene_Id']].replace(np.nan, '')
    merged_file = merged_file.replace(np.nan, 'NA')
    merged_file.to_csv(output_dir + 'data_CNA.txt', index=None, sep='\t')


def merge_log_seg_data(input_dir, output_dir):
    files_to_merge = [fn for fn in glob.glob(input_dir + '*.seg')]
    
    if not files_to_merge:
        print('No .seg files found. Please add some and rerun.')
        return
    
    files_to_merge = sorted(files_to_merge)
    
    with open(output_dir + 'data_cna_hg19.seg', 'w+') as outfile:
        with open(files_to_merge.pop(0)) as infile:
            outfile.write(infile.read())
        
        for file in files_to_merge:
            with open(file) as infile:
                # skip 1 line in each file after the first
                next(infile)
                outfile.write(infile.read())


def merge_maf_data(input_dir, output_dir):
    files_to_merge = [fn for fn in glob.glob(input_dir + '*.maf')]
    
    if not files_to_merge:
        print('No .maf files found. Please add some and rerun.')
        return

    files_to_merge = sorted(files_to_merge)
    dfs_to_merge = []
    
    for file in files_to_merge:
        data_frame = pd.read_csv(file, delimiter='\t', dtype=str)
        
        dfs_to_merge.append(data_frame)

    merged_file = dfs_to_merge.pop(0)
    
    while dfs_to_merge:
        merged_file = pd.concat([merged_file, dfs_to_merge.pop()])

    merged_file.to_csv(output_dir + 'data_mutations_extended.maf', index=None, sep='\t')


def merge_all_data(input_dir, output_dir):
    merge_maf_data(input_dir, output_dir)


@click.command()
@click.option('--file_types', '-ft', type=click.Choice(['all', 'gistic_gene', 'log_seg', 'maf']), multiple=True, default=['all'])
@click.option('--input_dir', default='')
@click.option('--output_dir', default='')
def main(file_types, input_dir, output_dir):
    if 'all' in file_types or Counter(file_types) == Counter(['gistic_gene', 'log_seg', 'maf']):
        merge_all_data(input_dir, output_dir)
        return
    
    if 'gistic_gene' in file_types:
        merge_gistic_gene_data(input_dir, output_dir)

    if 'log_seg' in file_types:
        merge_log_seg_data(input_dir, output_dir)

    if 'maf' in file_types:
        merge_maf_data(input_dir, output_dir)


if __name__ == '__main__':
    main()
