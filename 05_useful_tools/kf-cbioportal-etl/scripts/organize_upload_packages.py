#!/usr/bin/env python3
"""
This is an organization script to organize data in final upload format.
This includes creating soft links to all data files as well as meta files to describe data files and case lists to describe number of samples of each data type
"""
import sys
import argparse
import os
import json
import subprocess


def process_meta_study(meta_data, output_dir):
    study = meta_data["cancer_study_identifier"]
    # fields where key matches and value is just value of dict entry
    matched_fields = ["type_of_cancer", "short_name", "reference_genome", "description", "groups", "citation", "pmid"]
    with open (output_dir + "meta_study.txt", "w") as meta_study:
        print("{}: {}".format("cancer_study_identifier",study), file=meta_study)
        print("{}: {}".format("name", meta_data["display_name"]), file=meta_study)
        for key in matched_fields:
            if key in meta_data:
                print("{}: {}".format(key, meta_data[key]), file=meta_study)
    return study


def process_meta_data(meta_data, output_dir, canc_study_id):
    for dtype in meta_data["dtypes"]:
        try:
            # pointer for easier readability and dict key traciing
            cur_data = meta_data["dtypes"][dtype]
            cbio_name = cur_data["cbio_name"]
            parts = cbio_name.split("_")
            attr_dict = cur_data["meta_file_attr"]
            meta_name = "meta_" + "_".join(parts[1:])
            if attr_dict["datatype"] == "FUSION":
                meta_name = "meta_" + attr_dict["datatype"] + ".txt"
            meta_data_file = open(output_dir + meta_name, "w")
            meta_data_file.write("cancer_study_identifier: " + canc_study_id + "\n")
            for mkey in attr_dict:
                meta_data_file.write(mkey + ": " + attr_dict[mkey] + "\n")
            meta_data_file.write("data_filename: " + cbio_name + "\n")
            meta_data_file.close()
            # create data_ links to data
            cmd = (
                "ln -s "
                + cwd
                + meta_data["dir"]
                + "/"
                + canc_study_id
                + "."
                + cur_data["ext"]
                + " "
                + output_dir
                + cbio_name
            )
            subprocess.call(cmd, shell=True)
        except Exception as e:
            sys.stderr.write(str(e) + " failed processing meta data file\n")


def process_clinical_data(meta_data, output_dir, canc_study_id):
    for dtype in meta_data["dtypes"]:
        # pointer for easier readability and dict key tracing
        try:
            cur_data = meta_data["dtypes"][dtype]
            cbio_name = cur_data["cbio_name"]
            parts = cbio_name.split("_")
            meta_name = "meta_" + "_".join(parts[1:])
            meta_data_file = open(output_dir + meta_name, "w")
            meta_data_file.write("cancer_study_identifier: " + canc_study_id + "\n")
            attr_dict = cur_data["meta_file_attr"]
            for mkey in attr_dict:
                meta_data_file.write(mkey + ": " + attr_dict[mkey] + "\n")
            meta_data_file.write("data_filename: " + cbio_name + "\n")
            meta_data_file.close()
            # create data_ links to data
            cmd = (
                "ln -s "
                + cwd
                + meta_data["dir"]
                + "/"
                + cbio_name
                + " "
                + output_dir
                + cbio_name
            )
            subprocess.call(cmd, shell=True)
        except Exception as e:
            sys.stderr.write(str(e) + " failed processing meta data file\n")
            pdb.set_trace()
            hold = 1


def write_case_list(case_key, attr_dict, sample_list, case_dir):
    """
    Simple helper function to write case lists based on data type being described
    """
    case_file = open(case_dir + case_key + ".txt", "w")
    case_file.write("cancer_study_identifier: " + canc_study_id + "\n")
    key_list = list(attr_dict)
    case_file.write(
        key_list[0] + ": " + canc_study_id + "_" + attr_dict[key_list[0]] + "\n"
    )
    for i in range(1, len(key_list), 1):
        to_write = key_list[i] + ": " + attr_dict[key_list[i]]
        if key_list[i] == "case_list_description":
            to_write += " (" + str(len(sample_list)) + ")"
        case_file.write(to_write + "\n")
    case_file.write("case_list_ids: " + "\t".join(sample_list) + "\n")
    case_file.close()


def create_case_lists(data_dict, output_dir):
    """
    Function to iterate through config file, determine data types available, and initialize relevant sample lists for each data type and data type combo
    """
    case_dir = output_dir + "case_lists/"
    try:
        os.mkdir(case_dir)
    except:
        sys.stderr.write(case_dir + " already exists.\n")

    muts_list = []
    cna_list = []
    rna_list = []
    fusion_list = []

    if data_dict["merged_mafs"]:
        # Get samples from merged maf file
        muts_fname = (
            output_dir + config_data["merged_mafs"]["dtypes"]["mutation"]["cbio_name"]
        )
        muts_file = open(muts_fname)
        head = next(muts_file)
        head = next(muts_file)
        header = head.rstrip("\n").split("\t")
        s_idx = header.index("Tumor_Sample_Barcode")
        for line in muts_file:
            data = line.rstrip("\n").split("\t")
            muts_list.append(data[s_idx])
        muts_file.close()
        muts_list = [*{*muts_list}]
        write_case_list("cases_sequenced", config_data["cases_sequenced"], muts_list, case_dir)
    # Initialize all cases with muts list, even if empty
    all_cases = muts_list
    if data_dict["merged_cnvs"] == 1:
        # Get samples from merged cnv file
        cna_fname = (
            output_dir + config_data["merged_cnvs"]["dtypes"]["linear"]["cbio_name"]
        )
        cna_file = open(cna_fname)
        head = next(cna_file)
        # assumes header is Hugo_symbols\tsample_name1\tsamplename2 etc, if entrez ID, will need to change!
        cna_list = head.rstrip("\n").split("\t")[1:]
        cna_file.close()
        write_case_list("cases_cna", config_data["cases_cna"], cna_list, case_dir)
        all_cases += cna_list
        # Create case list for samples with muts and cnv data
        muts_plus_cna = list(set(muts_list) & set(cna_list))
        write_case_list("cases_cnaseq", config_data["cases_cnaseq"], muts_plus_cna, case_dir)

    if data_dict["merged_rsem"] == 1:
        # Get samples from merged rsem file - is a simple gene by sample table
        rna_fname = (
            output_dir + config_data["merged_rsem"]["dtypes"]["counts"]["cbio_name"]
        )
        rna_file = open(rna_fname)
        head = next(rna_file)
        rna_list = head.rstrip("\n").split("\t")[1:]
        write_case_list("cases_RNA_Seq_v2_mRNA", config_data["cases_RNA_Seq_v2_mRNA"], rna_list, case_dir)
        all_cases += rna_list

    if "merged_fusion" in data_keys and data_keys["merged_fusion"] == 1:
        # Get samples from merge fusion file
        fusion_fname = (
            output_dir + config_data["merged_fusion"]["dtypes"]["fusion"]["cbio_name"]
        )
        fusion_file = open(fusion_fname)
        head = next(fusion_file)
        header = head.rstrip("\n").split("\t")
        # Flag to get samples names depending if source is legacy or current
        sample_id_colname = "Sample_Id"
        if args.legacy:
            sample_id_colname = "Tumor_Sample_Barcode"
        s_idx = header.index(sample_id_colname)
        for line in fusion_file:
            data = line.rstrip("\n").split("\t")
            fusion_list.append(data[s_idx])
        fusion_file.close()
        fusion_list = [*{*fusion_list}]
        write_case_list("cases_sv", config_data["cases_sv"], fusion_list, case_dir)
        all_cases += fusion_list

        # loading mutations is a minimum, so if cna exists...3 way file can be made
        if len(cna_list) > 0:
            three_way = list(set(muts_list) & set(cna_list) & set(rna_list))
            write_case_list(
                "cases_3way_complete",
                config_data["cases_3way_complete"],
                three_way,
                case_dir,
            )
    all_cases = [*{*all_cases}]
    write_case_list("cases_all", config_data["cases_all"], all_cases, case_dir)


parser = argparse.ArgumentParser(
    description="Create cases lists, meta files, and organize data for cbio upload."
    " It is assumed you are at the dir level of all input data files"
)
parser.add_argument(
    "-o", "--output_dir", action="store", dest="out_dir", help="output directory name"
)
parser.add_argument(
    "-c",
    "--config",
    action="store",
    dest="config_file",
    help="json config file with meta information; see REFS/case_meta_config.json example",
)
parser.add_argument(
    "-l",
    "--legacy",
    default=False,
    action="store_true",
    dest="legacy",
    help="If set, will run legacy fusion output",
)

args = parser.parse_args()

cwd = os.getcwd() + "/"
with open(args.config_file) as f:
    config_data = json.load(f)

out_dir = args.out_dir
if out_dir[-1] != "/":
    out_dir += "/"
try:
    os.mkdir(out_dir)
except:
    sys.stderr.write(out_dir + " already exists.\n")

try:
    study_id = config_data["study"]["cancer_study_identifier"]
    if os.path.isdir(config_data["data_sheets"]["dir"]):
        cur_dir = out_dir + config_data["study"]["cancer_study_identifier"] + "/"
        try:
            os.mkdir(cur_dir)
        except:
            sys.stderr.write(cur_dir + " already exists.\n")
        sys.stderr.write("Creating meta study file for " + study_id + "\n")
        canc_study_id = process_meta_study(config_data["study"], cur_dir)
        data_keys = {
            "merged_mafs": 0,
            "merged_cnvs": 0,
            "merged_rsem": 0,
            "merged_fusion": 0,
        }
        for key in data_keys:
            if key in config_data and config_data[key]["dir"] != "":
                data_keys[key] = 1
                process_meta_data(config_data[key], cur_dir, canc_study_id)
                sys.stderr.write("Creating meta data files and links for " + key + "\n")
            else:
                sys.stderr.write("Skipping meta files for " + key + "\n")
        sys.stderr.write("Creating clinical meta sheets and links\n")
        process_clinical_data(config_data["data_sheets"], cur_dir, canc_study_id)
        create_case_lists(data_keys, cur_dir)
    else:
        sys.stderr.write("No datasheets for " + study_id + ", skipping!\n")
except Exception as e:
    sys.stderr.write(str(e) + "\nerror processing files for " + study_id + "!\n")
