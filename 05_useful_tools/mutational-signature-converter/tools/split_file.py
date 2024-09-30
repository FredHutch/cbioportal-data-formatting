import csv
import pandas as pd
import sys

# read data from  command line
input_file = sys.argv[1]
output_file = sys.argv[2]

# read data from data file
df = pd.read_csv(input_file, sep='\t')

# number of mutation file
rows1 = [0]
df1 = df.iloc[rows1].copy()

# prepare the second file for mean data
df2 = df.loc[df['ENTITY_STABLE_ID'].str.contains('mean')].copy()

def rowFuncForTmpColumn(row):
    if len(row["ENTITY_STABLE_ID"].split("_")) >= 2 :
        return row["ENTITY_STABLE_ID"].split("_")[1]

def rowFuncToOverrideStableIdColumnContribution(row):
    if len(row["ENTITY_STABLE_ID"].split("_")) >= 2 :
        return "mutational_signature_contribution_" + row["ENTITY_STABLE_ID"].split("_")[1]

def rowFuncToOverrideStableIdColumnConfidence(row):
    if len(row["ENTITY_STABLE_ID"].split("_")) >= 2 :
        return "mutational_signature_confidence_" + row["ENTITY_STABLE_ID"].split("_")[1]

df2['tmp'] = df2.apply(rowFuncForTmpColumn, axis = 1)
df2['ENTITY_STABLE_ID'] = df2.apply(rowFuncToOverrideStableIdColumnContribution, axis = 1)
df2['tmp'] = pd.to_numeric(df2['tmp'], errors='coerce')
df2 = df2.sort_values('tmp')

if 'tmp' in df2:
    del df2['tmp']

# prepare the third file for confidence data
df3 = df.loc[df['ENTITY_STABLE_ID'].str.contains('confidence')].copy()

df3['tmp'] = df3.apply(rowFuncForTmpColumn, axis = 1)
df3['ENTITY_STABLE_ID'] = df3.apply(rowFuncToOverrideStableIdColumnConfidence, axis = 1)
df3['tmp'] = pd.to_numeric(df3['tmp'], errors='coerce')
df3 = df3.sort_values('tmp')

if 'tmp' in df3:
    del df3['tmp']

# write the output file
out1 = df1.to_csv(output_file + "_Nmut.txt", sep='\t', header=True, index=False)
out2 = df2.to_csv(output_file + "_Contribution.txt", sep='\t', header=True, index=False)
out3 = df3.to_csv(output_file + "_Confidence.txt", sep='\t', header=True, index=False)