import argparse
import pdb
import sys
import concurrent.futures
import os
import pandas as pd


parser = argparse.ArgumentParser(description='Subset a hisologies file.')
parser.add_argument('-f', '--histologies-file', action='store', dest='hist', help='histologies file to subset')

args = parser.parse_args()

hist_file = pd.read_csv(args.hist, sep="\t", low_memory=False)
#pdb.set_trace()
cohorts = ["PBTA", "GMKF"]
cgs = ["Neuroblastoma", "Acute Myeloid Leukemia"]
# hist_subset1 = hist_file[hist_file['cohort'].isin(cohorts)]
hist_subset1 = hist_file[hist_file['cohort'] == cohorts[0]]
test1 = hist_file['cohort'] == "TARGET"
test2 = hist_file['cancer_group'].isin(cgs)
hist_subset2 = hist_file[test1 & test2]
# fudge parent aliquot ID to be able to use next script

hist_subset2 = hist_subset2.assign(parent_aliquot_id = hist_subset2['Kids_First_Participant_ID'] + "-" + hist_subset2['sample_id'] + "-TARGET")
#pdb.set_trace()
hist_subset3 = hist_file[hist_file['cohort'] == cohorts[1]]
hist_subset3 = hist_subset3.assign(parent_aliquot_id = hist_subset3['Kids_First_Participant_ID'] + "-" + hist_subset3['sample_id'] + "-" + cohorts[1])

hist_subset2 = hist_subset2.append(hist_subset3, ignore_index=True)
hist_subset1.append(hist_subset2, ignore_index=True).to_csv("histologies_subset.tsv", sep='\t', mode='w', index=False)
#hist_subset = hist_subset1.append(hist_subset2, ignore_index=True)
