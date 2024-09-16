import csv
import logging
import pandas as pd
import numpy as np

from scipy.stats import norm
from utils import hgnc_lookup

autosomes = [str(a) for a in range(1, 23)]


def aggregate_adjacent(cnv, value_cols=(), stable_cols=(), length_normalized_cols=(), summed_cols=()):
    """ Aggregate adjacent segments with similar copy number state.

    see: https://github.com/amcpherson/remixt/blob/master/remixt/segalg.py

    Args:
        cnv (pandas.DataFrame): copy number table

    KwArgs:
        value_cols (list): list of columns to compare for equivalent copy number state
        stable_cols (list): columns for which values are the same between equivalent states
        length_normalized_cols (list): columns that are width normalized for equivalent states

    Returns:
        pandas.DataFrame: copy number with adjacent segments aggregated
    """

    # Group segments with same state
    cnv = cnv.sort_values(['chr', 'start'])
    cnv['chromosome_index'] = np.searchsorted(np.unique(cnv['chr']), cnv['chr'])
    cnv['diff'] = cnv[['chromosome_index'] + value_cols].diff().abs().sum(axis=1)
    cnv['is_diff'] = (cnv['diff'] != 0)
    cnv['cn_group'] = cnv['is_diff'].cumsum()

    def agg_segments(df):
        a = df[stable_cols].iloc[0]

        a['chr'] = df['chr'].min()
        a['start'] = df['start'].min()
        a['end'] = df['end'].max()
        a['width'] = df['width'].sum()

        for col in length_normalized_cols:
            a[col] = (df[col] * df['width']).sum() / (df['width'].sum() + 1e-16)

        for col in summed_cols:
            a[col] = df[col].sum()

        return a

    aggregated = cnv.groupby('cn_group').apply(agg_segments)

    for col in aggregated:
        aggregated[col] = aggregated[col].astype(cnv[col].dtype)

    return aggregated


def calculate_gene_copy(cnv, genes):
    """ Calculate the copy number segments overlapping each gene

    Args:
        cnv (pandas.DataFrame): copy number table
        genes (pandas.DataFrame): gene table

    Returns:
        pandas.DataFrame: segment copy number for each gene

    The input copy number table is assumed to have columns: 
        'chr', 'start', 'end', 'width', 'copy', 'reads', 'state'

    The input genes table is assumed to have columns:
        'chr', 'gene_start', 'gene_end', 'gene_id'

    The output segment copy number table should have columns:
        'gene_id', 'chr', 'gene_start', 'gene_end', 'start', 'end',
        'width', 'copy', 'reads', 'state'
    where each entry in the output table represents an overlap between
    a gene and a segment.

    """
    data = []

    for chr in cnv['chr'].unique():
        chr_cnv = cnv[cnv['chr'] == chr]
        chr_genes = genes[genes['chr'] == chr]

        # Iterate through segments, calculate overlapping genes
        for idx, row in chr_cnv.iterrows():

            # Subset overlapping genes
            overlapping_genes = chr_genes[~((chr_genes['gene_end'] < row['start']) | (chr_genes['gene_start'] > row['end']))]

            if not overlapping_genes.empty:
                overlapping_genes = overlapping_genes.assign(start = row['start'], end = row['end'], width = row['width'], copy = row['copy'], reads = row['reads'], state = row['state'])

            data.append(overlapping_genes)

    data = pd.concat(data, ignore_index=True)

    return data


def read_copy_data(bins_filename, filter_normal=False):
    """ Read hmmcopy data, filter normal cells and aggregate into segments
    """
    data = pd.read_csv(bins_filename)

    # Filter normal cells that are approximately diploid
    if filter_normal:
        cell_stats = (
            data[data['chr'].isin(autosomes)]
            .groupby('cell_id')['state']
            .agg(['mean', 'std'])
            .reset_index())

        cell_stats['is_normal'] = (
            (cell_stats['mean'] > 1.95) &
            (cell_stats['mean'] < 2.05) &
            (cell_stats['std'] < 0.01))

        data = data.merge(cell_stats[['cell_id', 'is_normal']], how='left')

        data = data[~data['is_normal']]

    # Aggregate cell copy number
    data = (
        data
        .groupby(['chr', 'start', 'end', 'width'])
        .agg({'state': 'median', 'copy': np.nanmean, 'reads': 'sum'})
        .reset_index())

    assert not data.duplicated(['chr', 'start', 'end']).any()

    # Aggregate cell copy number
    data = aggregate_adjacent(
        data,
        value_cols=['state'],
        stable_cols=['state'],
        length_normalized_cols=['copy'],
        summed_cols=['reads'],
    )

    return data


def read_gene_data(gtf):
    data = pd.read_csv(
        gtf,
        delimiter='\t',
        names=['chr', 'gene_start', 'gene_end', 'gene_id'],
        usecols=[0,3,4,8],
        converters={'chr': str},
    )

    data['gene_id'] = data['gene_id'].str.extract('(ENSG\d+)')

    data = data.groupby(['chr', 'gene_id']).agg({'gene_start':'min', 'gene_end':'max'}).reset_index()

    return data


def convert_to_transform_format(data, temp_dir):
    """Hacky way to get data generated
    """ 
    data['median_logr'] = np.log2(data['copy'] / 2)
    data['median_logr'] = data['median_logr'].fillna(np.exp(-8))
    data['num.mark'] = (data['width'] / 500000).astype(int)

    data = data.rename(columns={'start': 'seg_start', 'end': 'seg_end', 'Hugo_Symbol': 'hugo_symbol', 'Entrez_Gene_Id': 'entrez_id'})
    data['placeholder'] = 0
    data = data[['chr', 'seg_start', 'seg_end', 'state', 'placeholder', 'num.mark', 'median_logr', 'gene_id', 'hugo_symbol', 'entrez_id', 'gene_start', 'gene_end']]
    data = data.astype({'seg_start': int, 'seg_end': int, 'state': int})
    data.loc[data['median_logr'] == np.NINF, 'median_logr'] = np.exp(-8)

    # Fix seg ends to align with cBioPortal specifications
    data.loc[(data['chr'] == '1') & (data['seg_end'] == 249500000), 'seg_end'] = 249250621
    data.loc[(data['chr'] == '2') & (data['seg_end'] == 243500000), 'seg_end'] = 243199373
    data.loc[(data['chr'] == '3') & (data['seg_end'] == 198500000), 'seg_end'] = 198022430
    data.loc[(data['chr'] == '4') & (data['seg_end'] == 191500000), 'seg_end'] = 191154276
    data.loc[(data['chr'] == '5') & (data['seg_end'] == 181000000), 'seg_end'] = 180915260
    data.loc[(data['chr'] == '6') & (data['seg_end'] == 171500000), 'seg_end'] = 171115067
    data.loc[(data['chr'] == '7') & (data['seg_end'] == 159500000), 'seg_end'] = 159138663
    data.loc[(data['chr'] == '8') & (data['seg_end'] == 146500000), 'seg_end'] = 146364022
    data.loc[(data['chr'] == '9') & (data['seg_end'] == 141500000), 'seg_end'] = 141213431
    data.loc[(data['chr'] == '10') & (data['seg_end'] == 136000000), 'seg_end'] = 135534747
    data.loc[(data['chr'] == '11') & (data['seg_end'] == 135500000), 'seg_end'] = 135006516
    data.loc[(data['chr'] == '12') & (data['seg_end'] == 134000000), 'seg_end'] = 133851895
    data.loc[(data['chr'] == '13') & (data['seg_end'] == 115500000), 'seg_end'] = 115169878
    data.loc[(data['chr'] == '14') & (data['seg_end'] == 107500000), 'seg_end'] = 107349540
    data.loc[(data['chr'] == '15') & (data['seg_end'] == 103000000), 'seg_end'] = 102531392
    data.loc[(data['chr'] == '16') & (data['seg_end'] == 90500000), 'seg_end'] = 90354753
    data.loc[(data['chr'] == '17') & (data['seg_end'] == 81500000), 'seg_end'] = 81195210
    data.loc[(data['chr'] == '18') & (data['seg_end'] == 78500000), 'seg_end'] = 78077248
    data.loc[(data['chr'] == '19') & (data['seg_end'] == 59500000), 'seg_end'] = 59128983
    data.loc[(data['chr'] == '20') & (data['seg_end'] == 63500000), 'seg_end'] = 63025520
    data.loc[(data['chr'] == '21') & (data['seg_end'] == 48500000), 'seg_end'] = 48129895
    data.loc[(data['chr'] == '22') & (data['seg_end'] == 51500000), 'seg_end'] = 51304566
    data.loc[(data['chr'] == 'X') & (data['seg_end'] == 155500000), 'seg_end'] = 155270560
    data.loc[(data['chr'] == 'Y') & (data['seg_end'] == 59500000), 'seg_end'] = 59373566

    data.to_csv(temp_dir + 'hmmcopy_extract', index=None, sep='\t')


def merge_csv(hmmcopy_files, temp_dir):
    final_df = pd.read_csv(hmmcopy_files.pop(0), dtype=object)
    
    for file in hmmcopy_files:
        df = pd.read_csv(file, dtype=object)
        final_df = pd.concat([df, final_df], axis=0, ignore_index=True)
    
    final_df.to_csv(temp_dir + 'hmmcopy_csv', index=None)


def calculate_counts(counts_files, sample_id, temp_dir):
    usecols = ['chrom','coord','ref','alt', 'ref_counts', 'alt_counts']
    final_df = pd.DataFrame(columns=usecols)
    
    for counts_file in counts_files:
        for df in pd.read_csv(counts_file, chunksize=1e6, usecols=usecols):
            final_df = pd.concat([df, final_df], axis=0, ignore_index=True)
            final_df = final_df.groupby(['chrom','coord','ref','alt'], as_index=False).agg('sum')

    final_df = final_df.rename(columns={'ref_counts': 't_ref_count', 'alt_counts': 't_alt_count'})
    final_df.to_csv(temp_dir + sample_id + '_tumour_counts.csv', index=None, sep='\t')


def calculate_weighted_average(ensembl_dict, column_to_use):
    calculated_values = {}
    for ensembl_id in ensembl_dict:
        # find start and end points for all the segments gene is in
        seg_starts = [start for start in ensembl_dict[ensembl_id][0]]
        seg_ends = [end for end in ensembl_dict[ensembl_id][1]]
        values_to_use = [val for val in column_to_use[ensembl_id]]
        segs_to_remove = []
        
        # if ensembl_id gene is only present in one segment, add
        # associated copy number to calculated_values
        if len(seg_starts) == 1:
            calculated_values[ensembl_id] = values_to_use[0]
            continue

        gene_start = ensembl_dict[ensembl_id][4]
        gene_end = ensembl_dict[ensembl_id][5]
        
        denominator_start = (min(seg_ends) - gene_start) / (min(seg_ends) - min(seg_starts))
        denominator_end = ((max(seg_ends) - max(seg_starts)) - (max(seg_ends) - gene_end)) / (max(seg_ends) - max(seg_starts))
        numerator_start = denominator_start * values_to_use[seg_starts.index(min(seg_starts))] 
        numerator_end = denominator_end * values_to_use[seg_starts.index(max(seg_starts))]
        
        # remove calculation values from used segs
        values_to_remove = [values_to_use[seg_starts.index(min(seg_starts))], values_to_use[seg_starts.index(max(seg_starts))]]
        for value in values_to_remove:
            values_to_use.remove(value)
        
        # remove min and max segment start and end coordinates
        # this is to easily iterate over remaining segments
        seg_starts.remove(min(seg_starts)), seg_starts.remove(max(seg_starts))
        seg_ends.remove(min(seg_ends)), seg_ends.remove(max(seg_ends))
        
        # determine remaining required information for calculation
        denominator_rest = 1 * len(seg_starts)
        numerator_rest = 0  
        for value in seg_starts:
            numerator_rest = numerator_rest + values_to_use[seg_starts.index(value)]

        # perform final weighted average calculation
        calculated_values[ensembl_id] = (numerator_start + numerator_rest + numerator_end) / (denominator_start + denominator_rest + denominator_end)

    return calculated_values


def transform(extracted_file, show_missing_hugo=False, show_missing_entrez=False, show_missing_both=False):
    '''
    perform weighted average calculations, and transformations
    
    ensembl_dict will store information for calculations
    gene_dict will store information for gene data output
    seg_dict will store information for segment data output
    '''
    
    ensembl_dict, gene_dict, seg_dict  = {}, {}, {}
    homd_segs, missing_hugo_symbol, missing_entrez_id, missing_both = [], [], [], []
    next(extracted_file)
    file_reader = csv.reader(extracted_file, delimiter='\t')
    for line in file_reader:    
        # if line has an associated ensembl_id and
        # segment doesn't have a length of zero
        if line[7] and line[1] != line[2]:
            # if gene is missing hugo_symbol or entrez_id
            if line[8] != '' or line[9] != '':
                if line[8] == '':
                    missing_hugo_symbol.append(line[7])
                if line[9] == '':
                    missing_entrez_id.append(line[7])
                
                # ensembl_id: [entrez_id, hugo_symbol]
                gene_dict[line[7]] = [line[9], line[8]]
                
                # set up a key-value pair where the key is
                # an ensembl id and the value is a list containing
                # the associated segment start points, end points,
                # copy numbers, titan states, gene start point, and
                # gene end point
                if line[7] not in ensembl_dict:
                    ensembl_dict[line[7]] = [[], [], [], [], 0, 0]
                try:
                    ensembl_dict[line[7]][0].append(int(line[1]))
                except:
                    raise Exception(line)
                ensembl_dict[line[7]][1].append(int(line[2]))
                ensembl_dict[line[7]][2].append(int(line[3]))
                ensembl_dict[line[7]][3].append(int(line[4]))
                ensembl_dict[line[7]][4] = int(line[10])
                ensembl_dict[line[7]][5] = int(line[11])

            # if gene is missing hugo_symbol and entrez_id
            if line[8] == '' and line[9] == '':
                missing_both.append(line[7])

        # (seg_start, seg_end): [chr, num.mark, titan_state, median_logr]
        seg_dict[(line[1], line[2])] = [line[0], line[5], line[4], line[6]]

    copy_numbers = {}
    for ensembl_id in ensembl_dict:
        # key: ensembl_id, value: associated copy number(s)
        copy_numbers[ensembl_id] = ensembl_dict[ensembl_id][2]

    calculated_cns = calculate_weighted_average(ensembl_dict, copy_numbers)
    
    titan_states = {}
    for ensembl_id in ensembl_dict:
        # key: ensembl_id, value: associated titan state(s)
        titan_states[ensembl_id] = ensembl_dict[ensembl_id][3]

    calculated_tss = calculate_weighted_average(ensembl_dict, titan_states)

    for ensembl_id in calculated_cns:
        # append weighted average of calculated copy number and
        # titan state, for each ensembl_id
        gene_dict[ensembl_id].append(str(calculated_cns[ensembl_id]))
        # remember to round to nearest integer for integer data
        gene_dict[ensembl_id].append(str(round(calculated_tss[ensembl_id])))

    # create a baseline (mu) for gene copy number transformation
    calc_cn_list = [calculated_cns[key] for key in calculated_cns]
    mu, _ = norm.fit(calc_cn_list)

    # perform required gene transformations on copy number
    for ensembl_id in calculated_cns:
        cn = calculated_cns[ensembl_id]
        
        if cn < 1:
            gene_dict[ensembl_id][2] = '-2'
            if cn < 0:
                logging.warning(f'{ensembl_id} has a calculated cn value lesser than 0')
        elif 1 <= cn <= mu-1:
            gene_dict[ensembl_id][2] = '-1'
        elif mu-1 < cn < mu+1:
            gene_dict[ensembl_id][2] = '0'
        elif mu+1 <= cn < 6:
            gene_dict[ensembl_id][2] = '1'
        elif cn >= 6:
            gene_dict[ensembl_id][2] = '2'

    if show_missing_hugo:
        print('Ensembl IDs missing HUGO symbols:')
        print(missing_hugo_symbol)
    if show_missing_entrez:
        print('Ensembl IDs missing Entrez IDs:')
        print(missing_entrez_id)
    if show_missing_both:
        print('Ensembl IDs missing both HUGO symbols and Entrez IDs:')
        print(missing_both, '\n')
    
    return gene_dict, seg_dict


def load(gene_dict, seg_dict, sample_id, output_dir, output_gistic_gene=True, output_integer_gene=False, output_log_seg=True, output_integer_seg=False):
    '''
    split generated file into four outputs

    gene_dict contains key-value pairs of
    ensembl_id:
    [entrez_id, hugo_symbol, transformed_calc_cn, calc_titan_state]
    
    seg_dict contains key-value pairs of
    (seg_start, seg_end):
    [chr, num.mark, titan_state, median_logr]
    '''
    
    gene_header = 'Hugo_Symbol\tEntrez_Gene_Id\t' + sample_id + '\n'
    segment_header = 'ID\tchrom\tloc.start\tloc.end\tnum.mark\tseg.mean\n'
    
    if output_gistic_gene:
        gistic_gene_data = open(output_dir + sample_id + '_gistic_gene_data.txt', 'w+')
        gistic_gene_data.write(gene_header)
        
        for ensembl_id in gene_dict:
            gistic_gene_data.write(gene_dict[ensembl_id][1] + '\t' + gene_dict[ensembl_id][0] + '\t' + gene_dict[ensembl_id][2] + '\n')
    
    if output_integer_gene:
        integer_gene_data = open(output_dir + sample_id + '_integer_gene_data.txt', 'w+')
        integer_gene_data.write(gene_header)

        for ensembl_id in gene_dict:
            integer_gene_data.write(gene_dict[ensembl_id][1] + '\t' + gene_dict[ensembl_id][0] + '\t' + gene_dict[ensembl_id][3] + '\n')
    
    if output_log_seg:
        log_seg_data = open(output_dir + sample_id + '_log_seg_data.seg', 'w+')
        log_seg_data.write(segment_header)

        for seg_length in seg_dict:
            log_seg_data.write(sample_id + '\t' + seg_dict[seg_length][0] + '\t' + seg_length[0] + '\t' + seg_length[1] + '\t' + seg_dict[seg_length][1] + '\t' + seg_dict[seg_length][3] + '\n')
    
    if output_integer_seg:
        integer_seg_data = open(output_dir + sample_id + '_integer_seg_data.seg', 'w+')
        integer_seg_data.write(segment_header)

        for seg_length in seg_dict:
            integer_seg_data.write(sample_id + '\t' + seg_dict[seg_length][0] + '\t' + seg_length[0] + '\t' + seg_length[1] + '\t' + seg_dict[seg_length][1] + '\t' + seg_dict[seg_length][2] + '\n')
