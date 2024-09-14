#!/usr/bin/env python3
"""
Helper script to append a maf to an existing  maf file.
Uses filter_entry to filter out undesired calls like in other mafs
"""
import sys
import argparse
import gzip
from rename_filter_maf import process_maf_entry
from rename_filter_maf import populate_id_map
import pdb


parser = argparse.ArgumentParser(
    description="Output fields from maf file based on header - meant to be appended to an existing file!"
)
parser.add_argument(
    "-i", "--header", action="store", dest="header", help="File with maf header only"
)
parser.add_argument(
    "-m", "--maf-file", action="store", dest="maf_file", help="merged maf file to process"
)
parser.add_argument(
    "-t",
    "--table",
    action="store",
    dest="table",
    help="Table with BS ID, assay, cbio id keys",
)
parser.add_argument('-s', '--skip', action='store', dest='skip', default=False,
                    help='Skip typical #version header line')
parser.add_argument('-c', '--cbio', action='store', dest='cbio', default=False,
                    help='cBio file to append to')


args = parser.parse_args()
# populate BS to cbio key table
bs_cbio_key = populate_id_map(args.table)

header_file = open(args.header)
maf_version = next(header_file)
head = next(header_file)
# store header fields as list, will use to get position in new file, if exists
# will output blank if not in new file
header = head.rstrip("\n").split("\t")
try:
    eid_idx = header.index("Entrez_Gene_Id")
    header.pop(eid_idx)
except Exception as e:
    print(e, file=sys.stderr)
    eid_idx = None
h_dict = {}
# dict of classifications to drop
maf_exc = {
    "Silent": 0,
    "Intron": 0,
    "IGR": 0,
    "3'UTR": 0,
    "5'UTR": 0,
    "3'Flank": 0,
    "5'Flank": 0,
    "RNA": 0,
}

for item in header:
    h_dict[item] = None
# Set filler for norm ID
norm_id=""
skipped = 0
maf_fn = args.maf_file
sys.stderr.write("Processing " + maf_fn + "\n")

append_maf = open(args.cbio, 'a')

with (gzip.open if maf_fn.endswith("gz") else open)(maf_fn, "rt", encoding="utf-8") as cur:
    if args.skip:
        maf_version = next(cur)
    m_head = next(cur)
    m_header = m_head.rstrip("\n").split("\t")
    tid_idx = m_header.index("Tumor_Sample_Barcode")
    nid_idx = m_header.index("Matched_Norm_Sample_Barcode")
    v_idx = m_header.index("Variant_Classification")
    h_idx = m_header.index("Hugo_Symbol")

    # need to also pop entrez ID if exists, as process_maf_entry() will do that to data
    try:
        m_header.pop(m_header.index("Entrez_Gene_Id"))
    except Exception as e:
        print(e, file=sys.stderr)
    # bug fix for OpenPedCan, position will be one less after process_maf_entry
    n_ref_ct_idx = m_header.index('n_ref_count')
    n_alt_ct_idx = m_header.index('n_alt_count')    

    for i in range(len(m_header)):
        if m_header[i] in h_dict:
            h_dict[m_header[i]] = i
    # only print items in original header and in same order, else print blank
    for data in cur:
        to_print = []
        datum = process_maf_entry(data, maf_exc, v_idx, h_idx, tid_idx, eid_idx, bs_cbio_key)
        # Set tumor barcode to cBio ID
        try:
            if datum:
                for item in header:
                    if h_dict[item] != None:
                        to_print.append(datum[h_dict[item]])
                    else:
                        to_print.append("")
                # bug fix for maf format in OpenPedCan
                for i in [n_ref_ct_idx, n_alt_ct_idx]:
                    if to_print[i] == "NA":
                        to_print[i] = ""
                print("\t".join(to_print), file=append_maf)
            else:
                skipped += 1
        except Exception as e:
            print (e)
            pdb.set_trace()
            hold = 1
    sys.stderr.write("Processed " + maf_fn + "\n")
    sys.stderr.write("Skipped " + str(skipped) + " entries meeting exclusion criteria\n")

append_maf.close()