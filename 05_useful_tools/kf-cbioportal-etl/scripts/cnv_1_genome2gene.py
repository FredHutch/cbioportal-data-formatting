#!/usr/bin/env python3
import sys
import os
import argparse
import json
import subprocess
import concurrent.futures


def process_cnv(cpath):
    try:
        if cpath != "":
            bedtools = config_data["bedtools"]
            cnv_cp_only = config_data["cp_only_script"]
            bed_file = config_data["bed_genes"]
            hugo_tsv = config_data["hugo_tsv"]
            sys.stderr.write("Processing " + cpath + "\n")
            root = os.path.basename(cpath).split(".")[0]
            limit = config_data["cnv_min_len"]
            temp_len = root + ".CNVs_" + str(limit) + "_filtered.bed"
            len_fh = open(out_dir + temp_len, "w")
            in_cnv = open(cpath)
            skip = next(in_cnv)
            for cnv in in_cnv:
                ct_dict["total_cnvs"] += 1
                cnv_data = cnv.rstrip("\n").split("\t")
                if int(cnv_data[2]) - int(cnv_data[1]) >= limit:
                    len_fh.write("\t".join(cnv_data[0:5]) + "\n")
                else:
                    ct_dict["short_cnvs"] += 1
                    # sys.stderr.write("Entry too short " + cnv)
            len_fh.close()
            temp = root + ".CNVs.Genes"
            to_genes_cmd = (
                bedtools
                + " intersect -a "
                + out_dir
                + temp_len
                + " -b "
                + bed_file
                + " -wb > "
                + out_dir
                + temp
            )
            subprocess.call(to_genes_cmd, shell=True)
            out_gene_cnv_only = (
                "perl "
                + cnv_cp_only
                + " "
                + hugo_tsv
                + " "
                + out_dir
                + temp
                + " > "
                + out_dir
                + temp
                + ".copy_number"
            )
            check = subprocess.call(out_gene_cnv_only, shell=True)
            if check:
                sys.stderr.write('Error using to geens script. Check log\n')
                sys.exit(1)
            rm_tmp = "rm " + out_dir + temp + " " + out_dir + temp_len
            subprocess.call(rm_tmp, shell=True)
    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(1)


parser = argparse.ArgumentParser(
    description="Convert controlFreeC cnv genome coords to gene level"
)
parser.add_argument(
    "-d",
    "--cnv-dir",
    action="store",
    dest="cnv_dir",
    help="cnv as genome coords file directory",
)
parser.add_argument(
    "-j",
    "--config",
    action="store",
    dest="config_file",
    help="json config file with data types and " "data locations",
)

args = parser.parse_args()
with open(args.config_file) as f:
    config_data = json.load(f)

limit = config_data["cnv_min_len"]
suffix = config_data["dna_ext_list"]["copy_number"]
f_cmd = "find " + args.cnv_dir + ' -name "*.' + suffix + '"'
sys.stderr.write("Getting cnv list " + f_cmd + "\n")
flist = subprocess.check_output(f_cmd, shell=True)
out_dir = "converted_cnvs/"
try:
    os.mkdir(out_dir)
except:
    sys.stderr.write("output dir already exists\n")

ct_dict = {"total_cnvs": 0, "short_cnvs": 0}
with concurrent.futures.ThreadPoolExecutor(config_data["cpus"]) as executor:
    results = {
        executor.submit(process_cnv, cpath): cpath
        for cpath in flist.decode().split("\n")
    }
sys.stderr.write(str(ct_dict["total_cnvs"]) + " total cnv calls processed\n")
sys.stderr.write(
    str(ct_dict["short_cnvs"])
    + " calls dropped for not meeting min bp size "
    + str(limit)
    + "\n"
)
sys.stderr.write("Done, check logs\n")
