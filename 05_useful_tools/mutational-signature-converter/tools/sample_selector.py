import csv
import pandas as pd
import sys

# read data from  command line
input_file = sys.argv[1]
output_file = sys.argv[2]
sample_file = sys.argv[3]

# get samples
f = open(sample_file)
samplesString = f.readline()
f.close()

samples = samplesString.split(",")

# read data from data file
df = pd.read_csv(input_file, sep='\t')

df = df[samples]

# write the output file
out = df.to_csv(output_file, sep='\t', header=False)

