#!/usr/bin/env python3
import sys
import os
import argparse
import json
import concurrent.futures
import pandas as pd
import re
from get_file_metadata_helper import get_file_metadata


def process_cnv(cnv_fn, cur_cnv_dict, samp_id):
    for entry in open(cnv_fn):
        (gene, gid, value) = entry.rstrip("\n").split("\t")
        if gene not in cur_cnv_dict:
            cur_cnv_dict[gene] = {}
        if samp_id in cur_cnv_dict[gene]:
            sys.stderr.write(
                "ERROR: Sample ID "
                + samp_id
                + " already processed.  Back to the drawing board!"
            )
            exit(1)
        else:
            cur_cnv_dict[gene][samp_id] = value
    return cur_cnv_dict


def get_ploidy(obj):
    info = open(obj)
    for datum in info:
        datum = datum.rstrip("\n")
        try:
            if datum.startswith("Output_Ploidy"):
                (key, value) = datum.split("\t")
                return value
        except Exception as e:
            sys.stderr.write("WARN: " + str(e) + " entry could not be split\n")
    return "2"  # default if ploidy can't be found


def process_table(cbio_dx, file_meta_dict):
    try:
        # project/disease name should be name of directory hosting datasheet
        sys.stderr.write("Processing " + cbio_dx + " project" + "\n")
        new_cnv = open(out_dir + cbio_dx + ".predicted_cnv.txt", "w")
        cur_cnv_dict = {}
        s_list = []
        ploidy_dict = {}
        for cbio_tum_id in file_meta_dict[cbio_dx]:
            orig_fname = file_meta_dict[cbio_dx][cbio_tum_id]["fname"]
            kf_bs_id = file_meta_dict[cbio_dx][cbio_tum_id]["kf_tum_id"]
            parts = re.search("^(.*)\." + orig_suffix, orig_fname)
            gene_fname = parts.group(1) + w_gene_suffix
            sys.stderr.write(
                "Found relevant cnv to process "
                + " "
                + file_meta_dict[cbio_dx][cbio_tum_id]["kf_tum_id"]
                + " "
                + file_meta_dict[cbio_dx][cbio_tum_id]["kf_norm_id"]
                + " "
                + gene_fname
                + "\n"
            )
            sys.stderr.flush()
            s_list.append(cbio_tum_id)
            if manifest is not None:
                ploidy = get_ploidy(
                    info_dir + "/" + manifest.loc[kf_bs_id]["File_Name"]
                )
                ploidy_dict[cbio_tum_id] = ploidy
            else:
                ploidy_dict[cbio_tum_id] = "2"
            cur_cnv_dict = process_cnv(cnv_dir + gene_fname, cur_cnv_dict, cbio_tum_id)
        new_cnv.write("Hugo_Symbol\t" + "\t".join(s_list) + "\n")
        for gene in cur_cnv_dict:
            new_cnv.write(gene)
            for samp in s_list:
                if samp in cur_cnv_dict[gene]:
                    new_cnv.write("\t" + cur_cnv_dict[gene][samp])
                else:
                    # pdb.set_trace()
                    new_cnv.write("\t" + ploidy_dict[samp])
            new_cnv.write("\n")
        new_cnv.close()
        return 0, cbio_tum_id
    except Exception as e:
        print(e, file=sys.stderr)
        return 1, cbio_tum_id



parser = argparse.ArgumentParser(
    description="Merge cnv files using cavatica task info and datasheets."
)
parser.add_argument(
    "-t",
    "--table",
    action="store",
    dest="table",
    help="Table with cbio project, kf bs ids, cbio IDs, and file names",
)
parser.add_argument(
    "-n",
    "--cnv-dir-gene",
    action="store",
    dest="cnv_dir",
    help="cnv as gene file directory",
)
parser.add_argument(
    "-i",
    "--info_dir",
    action="store",
    dest="info_dir",
    help="If info files available, provide here",
)
parser.add_argument(
    "-j",
    "--config",
    action="store",
    dest="config_file",
    help="json config file with data types and data locations",
)


args = parser.parse_args()
with open(args.config_file) as f:
    config_data = json.load(f)
cnv_dir = args.cnv_dir
info_dir = args.info_dir
if cnv_dir[-1] != "/":
    cnv_dir += "/"
manifest = None
if info_dir is not None:
    manifest = pd.read_csv(args.table, sep="\t")
    manifest.set_index(["T_CL_BS_ID"], inplace=True)
    manifest = manifest.loc[manifest["File_Type"] == "info"]

else:
    sys.stderr.write("No info file given, will assume ploidy 2\n")
orig_suffix = config_data["dna_ext_list"]["copy_number"]
w_gene_suffix = ".CNVs.Genes.copy_number"
out_dir = "merged_cnvs/"
try:
    os.mkdir(out_dir)
except:
    sys.stderr.write("output dir already exists\n")
file_meta_dict = get_file_metadata(args.table, "cnv")
with concurrent.futures.ProcessPoolExecutor(config_data["cpus"]) as executor:
    results = { executor.submit(process_table, cbio_dx, file_meta_dict): cbio_dx for cbio_dx in file_meta_dict }
    for result in concurrent.futures.as_completed(results):
        if result.result()[0]:
            print("Failed processing " + result.result()[1], file=sys.stderr)
            exit(1)

# for cbio_dx in file_meta_dict:
#     process_table(cbio_dx, file_meta_dict)
# sys.stderr.write("Done, check logs\n")
