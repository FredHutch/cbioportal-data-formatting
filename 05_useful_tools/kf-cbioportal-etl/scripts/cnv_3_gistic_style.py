#!/usr/bin/env python3

import sys
import argparse
import json
import subprocess
import re
from get_file_metadata_helper import get_file_metadata
import pandas as pd
import numpy as np
import pdb

parser = argparse.ArgumentParser(
    description="Convert merged cnv values to discrete coded values."
)
parser.add_argument(
    "-d",
    "--merged_cnv_dir",
    action="store",
    dest="merged_cnv_dir",
    help="merged cnv dir",
)
parser.add_argument(
    "-j",
    "--config",
    action="store",
    dest="config_file",
    help="json config file with data types and " "data locations",
)
parser.add_argument(
    "-i",
    "--info_dir",
    action="store",
    dest="info_dir",
    help="If info files available, provide here",
)
parser.add_argument(
    "-t",
    "--table",
    action="store",
    dest="table",
    help="Table with cbio project, kf bs ids, cbio IDs, and file names",
)


def mt_adjust_cn(obj):
    try:
        # If there is a info file manifest, get ploidy. Else skip and assume ploidy 2
        checkpoint = obj
        if manifest is not None:
            info = args.info_dir + "/" + manifest.loc[obj]["File_Name"]
        else:
            bs_id = obj
        samp_id = bs_cbio_dict[obj]
        ploidy = 2
        if manifest is not None:

            for datum in info:
                datum = datum.rstrip("\n")
                try:
                    if datum.startswith("Output_Ploidy"):
                        (key, value) = datum.split("\t")
                        ploidy = int(value)
                        break
                except Exception as e:
                    sys.stderr.write("WARN: " + str(e) + " entry could not be split\n")
        data[samp_id] = data[samp_id] - ploidy
        min_cn = ploidy * -1
        # adjust discrete low range only in ploidy > 2
        if min_cn != -2:
            data[samp_id] = np.where(
                data[samp_id].between((min_cn + 1), -2), -1, data[samp_id]
            )
            data[samp_id] = np.where(data[samp_id] == min_cn, -2, data[samp_id])
        data[samp_id] = np.where(data[samp_id].between(2, high_gain), 1, data[samp_id])
        data[samp_id] = np.where(data[samp_id] > high_gain, 2, data[samp_id])
        return [0, checkpoint]

    except Exception as E:
        sys.stderr.write(str(E) + "\n")
        sys.stderr.write("Error processing sample entry for " + checkpoint + "\n")
        return [1, checkpoint]


args = parser.parse_args()
with open(args.config_file) as f:
    config_data = json.load(f)


flist = subprocess.check_output(
    "find " + args.merged_cnv_dir + " -name *.predicted_cnv.txt", shell=True
)

fname_list = flist.decode().split("\n")
file_meta_dict = get_file_metadata(args.table, "cnv")

manifest = None
if args.info_dir is not None:
    manifest = pd.read_csv(args.table, sep="\t")
    manifest.set_index(["T_CL_BS_ID"], inplace=True)
    manifest = manifest.loc[manifest["File_Type"] == "info"]

else:
    sys.stderr.write("No info file given, will assume ploidy 2\n")

if fname_list[-1] == "":
    fname_list.pop()
for fname in fname_list:
    parts = re.search("^" + args.merged_cnv_dir + "/(.*).predicted_cnv.txt", fname)
    cbio_dx = parts.group(1)
    try:
        data = pd.read_csv(fname, sep="\t")
    except Exception as e:
        print(e, file=sys.stderr)
    data.set_index("Hugo_Symbol")
    # sample list would be cbio ids
    samp_list = list(data.columns)[1:]
    bs_cbio_dict = {}
    for samp_id in samp_list:
        bs_id = file_meta_dict[cbio_dx][samp_id]["kf_tum_id"]
        bs_cbio_dict[bs_id] = samp_id
    high_gain = config_data["cnv_high_gain"]

    x = 1
    m = 50

    for bs_id in bs_cbio_dict:
        exit_code, object = mt_adjust_cn(bs_id)
        if exit_code == 1:
            sys.stderr.write("Had trouble processing object " + object + "\n")
            sys.exit(1)
        if x % m == 0:
            sys.stderr.write("Processed " + str(x) + " samples\n")
            sys.stderr.flush()
        x += 1

    sys.stderr.write("Conversion completed.  Writing results to file\n")
    new_fname = cbio_dx = (
        args.merged_cnv_dir + "/" + parts.group(1) + ".discrete_cnvs.txt"
    )
    data.to_csv(new_fname, sep="\t", mode="w", index=False)
