#!/usr/bin/env python3
import sys
import os
import argparse
import json
from get_file_metadata_helper import get_file_metadata
import concurrent.futures
import pdb


def filter_entry(entry, tum_id, norm_id, tid_idx, nid_idx, v_idx, h_idx, maf_exc):
    """
    Only output entries not in exclusion list while dropping ENTREZ ID, but keeping TERT promoter hits
    """
    data = entry.rstrip("\n").split("\t")
    # Want to allow TERT promoter as exception to exclusion rules
    if data[v_idx] not in maf_exc or (
        data[h_idx] == "TERT" and data[v_idx] == "5'Flank"
    ):
        data[tid_idx] = tum_id
        data[nid_idx] = norm_id
        return data
    else:
        return None


def process_maf(maf_fn, new_maf, maf_exc, tum_id, norm_id):
    """
    Iterate over maf file, skipping header lines since the files are being merged.
    With possiblility of mixed source, search headers
    """
    cur_maf = open(maf_fn)
    next(cur_maf)
    head = next(cur_maf)

    cur_header = head.rstrip('\n').split('\t')
    h_dict = {}
    for item in print_header:
        if item in cur_header:
            h_dict[item] = cur_header.index(item)
        else:
            h_dict[item] = None

    tid_idx = cur_header.index("Tumor_Sample_Barcode")
    nid_idx = cur_header.index("Matched_Norm_Sample_Barcode")
    v_idx = cur_header.index("Variant_Classification")
    h_idx = cur_header.index("Hugo_Symbol")

    with concurrent.futures.ThreadPoolExecutor(16) as executor:
        results = {
            executor.submit(
                filter_entry, entry, tum_id, norm_id, tid_idx, nid_idx, v_idx, h_idx, maf_exc
            )
            for entry in cur_maf
        }
        for result in concurrent.futures.as_completed(results):
            filtered = result.result()
            if filtered != None:
                to_print = []
                for item in print_header:
                    if h_dict[item] != None:
                        to_print.append(filtered[h_dict[item]])
                    else:
                        to_print.append("")

                new_maf.write("\t".join(to_print) + "\n")
    cur_maf.close()


def process_tbl(cbio_dx, file_meta_dict, print_head):
    """
    Probaby a less likely scenario, but can split out into multiple projects based on dict
    """
    try:
        x = 0
        # project/disease name should be name of directory hosting datasheet
        sys.stderr.write("Processing " + cbio_dx + " project" + "\n")
        new_maf = open(out_dir + cbio_dx + ".maf", "w")
        new_maf.write(print_head)
        for cbio_tum_id in file_meta_dict[cbio_dx]:
            cbio_norm_id = file_meta_dict[cbio_dx][cbio_tum_id]["cbio_norm_id"]
            fname = file_meta_dict[cbio_dx][cbio_tum_id]["fname"]
            print("Found relevant maf to process for {} {} {} {} {}".format(
                cbio_tum_id, cbio_norm_id, file_meta_dict[cbio_dx][cbio_tum_id]["kf_tum_id"], file_meta_dict[cbio_dx][cbio_tum_id]["kf_norm_id"], fname),
                file=sys.stderr)
            process_maf(maf_dir + fname, new_maf, maf_exc, cbio_tum_id, cbio_norm_id)
            x += 1
        sys.stderr.write(
            "Completed processing " + str(x) + " entries in " + cbio_dx + "\n"
        )
        new_maf.close()
    except Exception as e:
        print(e)
        sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Merge and filter mafs using cavatica task info and datasheets."
    )
    parser.add_argument(
        "-t",
        "--table",
        action="store",
        dest="table",
        help="Table with cbio project, kf bs ids, cbio IDs, and file names",
    )
    parser.add_argument(
        "-i", "--header", action="store", dest="header", help="File with maf header only"
    )
    parser.add_argument(
        "-m", "--maf-dirs", action="store", dest="maf_dirs", help="comma-separated list of maf file directories"
    )
    parser.add_argument(
        "-j",
        "--config",
        action="store",
        dest="config_file",
        help="json config file with data types and " "data locations",
    )
    parser.add_argument(
        "-f",
        "--dgd-status",
        action="store",
        dest="dgd_status",
        help="Flag to determine load will have pbta/kf + dgd(both), kf/pbta only(kf), dgd-only(dgd)",
        default="both",
        const="both",
        nargs="?",
        choices=["both", "kf", "dgd"],
    )


    args = parser.parse_args()
    with open(args.config_file) as f:
        config_data = json.load(f)
    # Create symlinks to mafs in one place for ease of processing
    maf_dir = "MAFS/"
    maf_dirs_in = args.maf_dirs
    print("Symlinking maf files from {} to {}".format(maf_dirs_in, maf_dir), file=sys.stderr)
    os.makedirs("MAFS", exist_ok=True)
    for dirname in maf_dirs_in.split(","):
        abs_path = os.path.abspath(dirname)
        for fname in os.listdir(dirname):
            try:
                src = os.path.join(abs_path, fname)
                dest = os.path.join(maf_dir, fname)
                os.symlink(src, dest)
            except Exception as e:
                print(e, file=sys.stderr)
                print("Could not sym link {} in {}".format(fname, dirname))
    # If DGD maf only, else if both, dgd maf wil be handled separately, or not at all if no dgd and kf only

    file_meta_dict = get_file_metadata(args.table, "DGD_MAF")
    if args.dgd_status != "dgd":
        file_meta_dict = get_file_metadata(args.table, "maf")
    head_fh = open(args.header)

    print_head = next(head_fh)
    cur_head = next(head_fh)
    print_header = cur_head.rstrip("\n").split("\t")
    eid_idx = print_header.index("Entrez_Gene_Id")
    print_header.pop(eid_idx)

    head_fh.close()
    print_head += "\t".join(print_header) + "\n"
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
    out_dir = "merged_mafs/"
    try:
        os.mkdir(out_dir)
    except:
        sys.stderr.write("output dir already exists\n")

    for cbio_dx in file_meta_dict:
        process_tbl(
            cbio_dx, file_meta_dict, print_head
        )

    sys.stderr.write("Done, check logs\n")
