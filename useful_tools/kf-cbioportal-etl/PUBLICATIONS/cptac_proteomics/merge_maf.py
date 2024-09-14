#!/usr/bin/env python3
import sys
import os
import argparse
import json
import subprocess
from get_file_metadata_helper  import get_file_metadata
import concurrent.futures


def process_maf(maf_fn, new_maf, maf_exc, tum_id, norm_id, tid_idx, v_idx, eid_idx, n_idx):
    cur_maf = open(maf_fn)
    next(cur_maf)
    next(cur_maf)
    for maf in cur_maf:
        data = maf.rstrip('\n').split('\t')
        if data[v_idx] not in maf_exc and int(data[t_alt_idx]) >= min_alt_ct and int(data[t_depth_index]) >= min_depth_ct:
            data[tid_idx] = tum_id
            data.pop(eid_idx)
            new_maf.write('\t'.join(data) + '\n')
    cur_maf.close()


def process_tbl(cbio_dx, file_meta_dict, tid_idx, v_idx, eid_idx, n_idx, print_head):
    try:
        x = 0
        # project/disease name should be name of directory hosting datasheet
        sys.stderr.write('Processing ' + cbio_dx + ' project' + '\n')
        new_maf = open(out_dir + cbio_dx + ".maf", 'w')
        new_maf.write(print_head)
        for cbio_tum_id in file_meta_dict[cbio_dx]:
            cbio_norm_id = file_meta_dict[cbio_dx][cbio_tum_id]['cbio_norm_id']
            fname = file_meta_dict[cbio_dx][cbio_tum_id]['fname']
            sys.stderr.write('Found relevant maf to process for ' + ' ' + cbio_tum_id + ' ' + cbio_norm_id + ' '
            + file_meta_dict[cbio_dx][cbio_tum_id]['kf_tum_id']  + ' ' + fname + '\n')
            sys.stderr.flush()
            process_maf(maf_dir + fname, new_maf, maf_exc, cbio_tum_id, cbio_norm_id, tid_idx, v_idx, eid_idx, n_idx)
            x += 1
        sys.stderr.write('Completed processing ' + str(x) + ' entries in ' + cbio_dx + '\n')
        new_maf.close()
    except Exception as e:
        print(e)
        sys.exit()


parser = argparse.ArgumentParser(description='Merge and filter mafs using cavatica task info and datasheets.')
parser.add_argument('-t', '--table', action='store', dest='table',
                    help='Table with cbio project, kf bs ids, cbio IDs, and file names')
parser.add_argument('-i', '--header', action='store', dest='header', help='File with maf header only')
parser.add_argument('-m', '--maf-dir', action='store', dest='maf_dir', help='maf file directory')
parser.add_argument('-j', '--config', action='store', dest='config_file', help='json config file with data types and '
                                                                               'data locations')

args = parser.parse_args()
min_alt_ct = 5
min_depth_ct = 30
with open(args.config_file) as f:
    config_data = json.load(f)
# get maf file ext
maf_dir = args.maf_dir
if maf_dir[-1] != '/':
    maf_dir += '/'
file_meta_dict = get_file_metadata(args.table, 'maf')
head_fh = open(args.header)

print_head = next(head_fh)
cur_head = next(head_fh)
cur_header = cur_head.rstrip('\n').split('\t')
eid_idx = cur_header.index('Entrez_Gene_Id')
n_idx = cur_header.index('NCBI_Build')
tid_idx = cur_header.index('Tumor_Sample_Barcode')
t_alt_idx = cur_header.index('t_alt_count')
t_depth_index = cur_header.index('t_depth')
#nid_idx = cur_header.index('Matched_Norm_Sample_Barcode')
v_idx = cur_header.index('Variant_Classification')
cur_header.pop(eid_idx)

head_fh.close()
print_head += '\t'.join(cur_header) + '\n'
maf_exc = {"Silent": 0, "Intron": 0, "IGR": 0, "3'UTR": 0, "5'UTR": 0, "3'Flank": 0, "5'Flank": 0, "RNA": 0}
out_dir = 'merged_mafs/'
try:
    os.mkdir(out_dir)
except:
    sys.stderr.write('output dir already exists\n')

with concurrent.futures.ThreadPoolExecutor(config_data['cpus']) as executor:
    results = {executor.submit(process_tbl, cbio_dx, file_meta_dict, tid_idx, v_idx, eid_idx, n_idx, print_head): cbio_dx for cbio_dx in file_meta_dict}

sys.stderr.write('Done, check logs\n')
