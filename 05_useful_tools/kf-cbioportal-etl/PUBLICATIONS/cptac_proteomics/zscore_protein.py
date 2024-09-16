#!/usr/bin/env python3

import sys
import argparse
import os
import pandas as pd
from scipy import stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Caculate z score of protein values.')
    parser.add_argument('-f', '--file', action='store', dest='in_file',
                    help='log2 transformed protein expression values')
    parser.add_argument('-l', '--label', action='store', dest='label',
                    help='ID column name')
    parser.add_argument('-o', '--out-suffix', action='store',
                    dest='out', help='Output filename desc')

    args = parser.parse_args()
    master_tbl = pd.read_csv(args.in_file, sep="\t")
    
    master_tbl.set_index(args.label, inplace=True)
    gene_sym_list = master_tbl.index
    sample_list=list(master_tbl.columns.values)
    sys.stderr.write('Calculating z scores\n')
    sys.stderr.flush()

    z_scored = stats.zscore(master_tbl, axis = 1)
    del master_tbl
    master_zscore_log = pd.DataFrame(z_scored, index=gene_sym_list, columns=sample_list)
    master_zscore_log.fillna(0, inplace=True)
    master_zscore_log.to_csv("data_" + args.out + "_Zscores.txt", sep='\t', mode='w', index=True, float_format='%.4f')
