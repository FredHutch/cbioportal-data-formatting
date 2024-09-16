#!/usr/bin/env python3
import sys
import os
import argparse
import json
import subprocess
from get_file_metadata_helper  import get_file_metadata
import concurrent.futures
import pdb


def process_file(samp_id):
    try:
        samp_list.append(samp_id)
        cur = open(cnv_dir + short[samp_id]['fname'])
        head = next(cur)
        header = head.rstrip("\n").split("\t")
        g_idx = header.index("gene")
        l_idx = header.index("log2")
        for info in cur:
            data = info.rstrip("\n").split("\t")
            names = data[g_idx].split(",")
            for name in names:
                if name in gene_dict:
                    bf_tbl[name][samp_id] = data[l_idx]
        cur.close()
        return 0
    except Exception as e:
        sys.stderr.write(str(e) + "\nError processing sample " + samp_id + "\n")
        exit(1)



parser = argparse.ArgumentParser(description='Custom merge of cnvkit files based on protemics work.')
parser.add_argument('-t', '--table', action='store', dest='table',
                    help='Table with cbio project, kf bs ids, cbio IDs, and file names')
parser.add_argument('-g', '--genes', action='store', dest='genes', help='Gene list from publication/collaborator data')
parser.add_argument('-c', '--cnv-dir', action='store', dest='cnv_dir', help='cnvkit file directory')

args = parser.parse_args()
project = "cptac_published"
cnv_dir = args.cnv_dir
if cnv_dir[-1] != '/':
    cnv_dir += '/'
out_dir = 'merged_cnvs/'
try:
    os.mkdir(out_dir)
except:
    sys.stderr.write('output dir already exists\n')
file_meta_dict = get_file_metadata(args.table, 'cnv')
short = file_meta_dict[project]
gene_list = []
gene_dict = {}
bf_tbl = {}
for gene in open(args.genes):
    gene = gene.rstrip("\n")
    gene_dict[gene] = 0
    gene_list.append(gene)
    bf_tbl[gene] = {}
samp_list = []

x = 1
m = 25

with concurrent.futures.ThreadPoolExecutor(16) as executor:
    results = {executor.submit(process_file, samp_id): samp_id for samp_id in short}
    for result in concurrent.futures.as_completed(results):
        if x % m == 0:
            sys.stderr.write('Processed ' + str(x) + ' samples\n')
            sys.stderr.flush()
        x += 1

out = open(out_dir + project + ".discrete_cnvs.txt", "w")
out.write("Hugo_Symbol\t" + "\t".join(samp_list) + "\n")
for gene in gene_list:
    out.write(gene)
    for samp in samp_list:
        if samp in bf_tbl[gene]:
            out.write("\t" + bf_tbl[gene][samp])
        else:
            out.write("\t1.0")
    out.write("\n")
out.close()