import argparse
import math
import pandas as pd
import os

def is_positive(number, SAMPLE):
	"""
	Questa funzione prende in input un numero 
	e restituisce True se il numero è positivo, False altrimenti.
	"""
	if number >= 0:
		return True
	else:
		n = open('negative_FC.log', 'a')
		n.write('[WARINIG] the sample '+SAMPLE+' has a Fold change in CNV with negative value\n')
		n.close()
		return False


def vcf_to_table(vcf_file, table_file, SAMPLE, MODE):
	if os.path.exists(table_file):
		MODE="a"
	else:
		MODE="w"
	with open(vcf_file, 'r') as vcf, open(table_file, MODE) as table:
		if MODE == 'a':
			pass
		else:
			table.write('ID\tchrom\tloc.start\tloc.end\tnum.mark\tseg.mean\n')
		SAMPLE=SAMPLE
		for line in vcf:
			# Skip commented lines
			if line.startswith('#'):
				continue

			# Split the line by tabs
			fields = line.strip().split('\t')

			# Extract the data we want to keep
			chrom = fields[0].strip('chr')
			start = fields[1]
			Id = fields[2]
			ref = fields[3]
			alt = fields[4]
			qual = fields[5]
			filt = fields[6]
			info = fields[7].split(';')
			if len(info) == 2:
				end = info[0].split('=')[1]
				gene =info[1].split('=')[1]
			else:
				end = info[1].split('=')[1]
				gene =info[2].split('=')[1]
			fc = float(fields[9])

			# check negatile Fold change values
			# if a negative fold chenge is found
			# the Fold change value is changed in 0.0001
			if is_positive(fc, SAMPLE):
				log2fc = math.log(fc,2)
			else:
				fc = 0.0001
				log2fc = math.log(fc,2)
			# Write the data to the table file
			# segmentated data example
			# ID<TAB>chrom<TAB>loc.start<TAB>loc.end<TAB>num.mark<TAB>seg.mean
			table.write(f'{SAMPLE}\t{chrom}\t{start}\t{end}\t{qual}\t{log2fc}\n')
			#print(f'{SAMPLE}\t{chrom}\t{start}\t{end}\t{qual}\t{fc}\n')

def vcf_to_table_fc(vcf_file, table_file, SAMPLE, MODE):
	
	if os.path.exists(table_file):
		MODE="a"
	else:
		MODE="w"
	with open(vcf_file, 'r') as vcf, open(table_file, MODE) as table:
		if MODE == 'a':
			pass
		else:
			table.write('ID\tchrom\tloc.start\tloc.end\tnum.mark\tseg.mean\tgene\tdiscrete\n')
		SAMPLE=SAMPLE
		for line in vcf:
			#print(line)
			# Skip commented lines
			if line.startswith('#'):
				continue

			# Split the line by tabs
			fields = line.strip().split('\t')

			# Extract the data we want to keep
			chrom = fields[0].strip('chr')
			start = fields[1]
			Id = fields[2]
			ref = fields[3]
			alt = fields[4]
			qual = fields[5]
			filt = fields[6]
			info = fields[7].split(';')
			if len(info) == 2:
				end = info[0].split('=')[1]
				gene =info[1].split('=')[1]
			else:
				end = info[1].split('=')[1]
				gene =info[2].split('=')[1]
			fc = float(fields[9])
			if is_positive(fc, SAMPLE):
				log2fc = math.log(fc,2)
			else:
				fc = 0.0001
				log2fc = math.log(fc,2)

			########################
			# manage discrete data #
			########################

			if alt == '<DUP>':
				discr = '2'
			elif alt == '<DEL>':
				discr = '-2'
			else:
				discr = '0'

			# Write the data to the table file
			# segmentated data example
			# ID<TAB>chrom<TAB>loc.start<TAB>loc.end<TAB>num.mark<TAB>seg.mean
			table.write(f'{SAMPLE}\t{chrom}\t{start}\t{end}\t{qual}\t{fc}\t{gene}\t{discr}\n')
			#print(f'{SAMPLE}\t{chrom}\t{start}\t{end}\t{qual}\t{fc}\n')



def load_table(file_path):
	"""
	Load a table from a file into a Pandas DataFrame object.

	Parameters:
	file_path (str): path to the file containing the table.

	Returns:
	pandas.DataFrame: the loaded table.
	"""
	df = pd.read_csv(file_path, sep='\t',header=0)
	return df


def main(INPUT, OUTPUT, SAMPLE, MODE):

	vcf_to_table(INPUT, OUTPUT, SAMPLE, MODE)
	vcf_to_table_fc(INPUT, OUTPUT, SAMPLE, MODE)

