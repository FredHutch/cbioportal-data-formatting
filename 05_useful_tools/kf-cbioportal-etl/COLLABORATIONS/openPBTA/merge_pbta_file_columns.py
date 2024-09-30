#!/usr/bin/python3
"""
Merges openPBTA files to complete input
"""
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Merges openPBTA  files to complete input')
parser.add_argument('-1', '--first', action='store', dest = 'first', help='first file. like  pbta-snv-consensus-mutation.maf.tsv.gz or consensus_seg_annotated_cn_autosomes.tsv.gz')
parser.add_argument('-2', '--second', action='store', dest='second',
                    help='second file. likely named pbta-snv-scavenged-hotspots.maf.tsv.gz or consensus_seg_annotated_cn_x_and_y.tsv.gz')
parser.add_argument('-o', '--output', action='store', dest='output',
                    help='output file name')


args = parser.parse_args()

first = pd.read_csv(args.first, sep='\t')
second = pd.read_csv(args.second, sep='\t')

print(first.shape)
print(second.shape)

first_col=first.columns
second_col=second.columns

common_cols = first_col.intersection(second_col)

first_common=first[common_cols]
second_common=second[common_cols]

frames = [first_common, second_common]
  
result = pd.concat(frames)

result.to_csv(args.output, sep='\t', index=False, compression="gzip")
