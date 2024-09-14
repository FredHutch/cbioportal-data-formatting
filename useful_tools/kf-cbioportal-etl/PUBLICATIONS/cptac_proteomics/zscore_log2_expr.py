#!/usr/bin/env python3

import sys
import argparse
import os
import concurrent.futures
import pandas as pd
from scipy import stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate Z score of already processed data.')
    parser.add_argument('-f', '--file', action='store', dest='in_file',
                    help='log2 transformed fpkm valuesFPKM values')

    args = parser.parse_args()

    master_tbl = pd.read_csv(args.in_file, sep="\t")
    
    master_tbl.set_index('Hugo_Symbol', inplace=True)
    gene_sym_list = master_tbl.index
    sample_list=list(master_tbl.columns.values)
    sys.stderr.write('Calculating z scores\n')
    sys.stderr.flush()

    z_scored = stats.zscore(master_tbl, axis = 0)
    del master_tbl
    master_zscore_log = pd.DataFrame(z_scored, index=gene_sym_list, columns=sample_list)
    master_zscore_log.fillna(0, inplace=True)
    master_zscore_log.to_csv("brain.zscore.log2_fpkm.tsv", sep='\t', mode='w', index=True, float_format='%.4f')
