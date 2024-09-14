#!/usr/bin/env python3

import sys
import argparse
import os
import concurrent.futures
import re
import json
import subprocess
import pdb


parser = argparse.ArgumentParser(description='Create cases lists, meta files, and organize data for cbio upload.'
                                ' It is assumed you are at the dir level of all input data files')
parser.add_argument('-o', '--output_dir', action='store', dest='out_dir', help='output directory name')
parser.add_argument('-d', '--dx-file', action='store', dest='dx_file', help='Dx index file with cbio short and long names')
parser.add_argument('-c', '--config', action='store', dest='config_file', help='json config file with meta information; see REFS/case_meta_config.json example')
args = parser.parse_args()

def process_meta_study(meta_data, output_dir, study):
    meta_study = open(output_dir + "meta_study.txt", "w")
    meta_study.write("type_of_cancer: " + study + "\n")
    # default is dx value, otherwise make it "cancer_study_identifier" value from config, in not empty
    canc_study_id = study
    if meta_data["cancer_study_identifier"] != "":
        canc_study_id = meta_data["cancer_study_identifier"]
    canc_study_id += meta_data['dir_suffix']
    meta_study.write("cancer_study_identifier: " + canc_study_id + "\n")
    meta_study.write("reference_genome: " + meta_data["reference_genome"] + "\n")
    name = dx_dict[study]
    if meta_data["name_append"] != "":
        name += " " + meta_data["name_append"]
    meta_study.write("name: " + name + "\n")
    desc = meta_data["description"][0]
    if len(meta_data["description"]) > 1:
        desc += " " + dx_dict[study] + " " + meta_data["description"][1]
    meta_study.write("description: " + desc + "\nshort_name: " + canc_study_id + "\ngroups: " + meta_data["groups"] + "\n")
    meta_study.close()
    return canc_study_id


def process_meta_data(meta_data, output_dir, canc_study_id, study):
    for dtype in meta_data["dtypes"]:
        try:
            # pointer for easier readability and dict key traciing
            cur_data = meta_data["dtypes"][dtype]
            cbio_name = cur_data["cbio_name"]
            parts = cbio_name.split("_")
            attr_dict = cur_data["meta_file_attr"]
            meta_name = "meta_" + "_".join(parts[1:])
            meta_data_file = open(output_dir + meta_name, "w")
            meta_data_file.write("cancer_study_identifier: " + canc_study_id + "\n")
            for mkey in attr_dict:
                meta_data_file.write(mkey + ": " + attr_dict[mkey] + "\n")
            meta_data_file.write("data_filename: " + cbio_name + "\n")
            meta_data_file.close()
            # create data_ links to data
            cmd = "ln -s " + cwd + meta_data["dir"] + "/" + study + "." + cur_data["ext"] + " " + output_dir + cbio_name
            subprocess.call(cmd, shell=True)
        except Exception as e:
            sys.stderr.write(str(e) + " failed processing meta data file\n")
            pdb.set_trace()
            hold = 1


def process_clinical_data(meta_data, output_dir, canc_study_id, study):
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
            cmd = "ln -s " + cwd + meta_data["dir"] + "/" + study + "/" + cbio_name + " " + output_dir  + cbio_name
            subprocess.call(cmd, shell=True)
        except Exception as e:
            sys.stderr.write(str(e) + " failed processing meta data file\n")
            pdb.set_trace()
            hold = 1


def write_case_list(case_key, attr_dict, sample_list, case_dir):
    case_file = open(case_dir + case_key + ".txt", "w")
    case_file.write("cancer_study_identifier: " + canc_study_id + "\n")
    key_list = list(attr_dict)
    case_file.write(key_list[0] + ": " + canc_study_id + "_" + attr_dict[key_list[0]] + "\n")
    for i in range(1, len(key_list), 1):
        to_write = key_list[i] + ": " + attr_dict[key_list[i]]
        if key_list[i] == "case_list_description":
            to_write += " (" + str(len(sample_list)) + ")"
        case_file.write(to_write + "\n")
    case_file.write("case_list_ids: " + "\t".join(sample_list) + "\n")
    case_file.close()

def create_case_lists(data_dict, output_dir, canc_study_id, study):
    case_dir = output_dir + "case_lists/"
    try:
        os.mkdir(case_dir)
    except:
        sys.stderr.write(case_dir + ' already exists.\n')

    muts_list = []
    cna_list = []
    rna_list = []
    protein_list = []

    muts_fname = output_dir + config_data["merged_mafs"]["dtypes"]["mutation"]["cbio_name"]
    muts_file = open(muts_fname)
    head = next(muts_file)
    head = next(muts_file)
    header = head.rstrip('\n').split('\t')
    s_idx = header.index('Tumor_Sample_Barcode')
    for line in muts_file:
        data = line.rstrip('\n').split('\t')
        muts_list.append(data[s_idx])
    muts_file.close()
    muts_list = [*{*muts_list}]
    if data_dict["merged_cnvs"] == 1:
        cna_fname = output_dir +  config_data["merged_cnvs"]["dtypes"]["linear"]["cbio_name"]
        cna_file = open(cna_fname)
        head = next(cna_file)
        # assumes header is Hugo_symbols\tsample_name1\tsamplename2 etc, if entrez ID, will need to change!
        cna_list = head.rstrip('\n').split('\t')[1:]
        cna_file.close()
    if data_dict["merged_rsem"] == 1:
        # assumes header is Hugo_symbols\tsample_name1\tsamplename2 etc, if entrez ID, will need to change!
        rna_fname = output_dir + config_data["merged_rsem"]["dtypes"]["counts"]["cbio_name"]
        rna_file = open(rna_fname)
        head = next(rna_file)
        rna_list = head.rstrip('\n').split('\t')[1:]
    if data_dict["merged_protein"] == 1:
        # assumes header is Hugo_symbols\tsample_name1\tsamplename2 etc, if entrez ID, will need to change!
        prot_fname = output_dir + config_data["merged_protein"]["dtypes"]["quantification"]["cbio_name"]
        prot_file = open(prot_fname)
        head = next(prot_file)
        prot_list = head.rstrip('\n').split('\t')[1:]

        # fusion_list = rna_list
    # muts_plus_fusion = muts_list + fusion_list
    # muts_plus_fusion = [*{*muts_plus_fusion}]
    all_cases = muts_list
    write_case_list('cases_sequenced', config_data['cases_sequenced'], muts_list, case_dir)
    # write_case_list('cases_sequenced', config_data['cases_sequenced'], muts_list, case_dir)
    if len(cna_list) > 0:
        write_case_list('cases_cna', config_data['cases_cna'], cna_list, case_dir)
        all_cases += cna_list
        muts_plus_cna = list(set(muts_list) & set(cna_list))
        write_case_list('cases_cnaseq', config_data['cases_cnaseq'], cna_list, case_dir)
    if len(rna_list) > 0:
        write_case_list('cases_RNA_Seq_v2_mRNA', config_data['cases_RNA_Seq_v2_mRNA'], rna_list, case_dir)
        all_cases += rna_list

        # loading mutations is a minimum, so if cna exists...3 way file can be made
        if len(cna_list) > 0:
            three_way = list(set(muts_list) & set(cna_list) & set(rna_list))
            write_case_list('cases_3way_complete', config_data['cases_3way_complete'], three_way, case_dir)
    if len(prot_list) > 0:
        write_case_list('cases_rppa', config_data['cases_rppa'], prot_list, case_dir)
        all_cases += prot_list

    all_cases = [*{*all_cases}]
    write_case_list('cases_all', config_data['cases_all'], all_cases, case_dir)


cwd = os.getcwd() + "/"
with open(args.config_file) as f:
    config_data = json.load(f)

dx_file = open(args.dx_file)
dx_dict = {}
head = next(dx_file)
for line in dx_file:
    (ds_dx, cbio_short, cbio_long) = line.rstrip('\n').split('\t')
    dx_dict[cbio_short] = cbio_long
dx_file.close()

out_dir = args.out_dir
if out_dir[-1] != "/":
    out_dir += "/"
try:
    os.mkdir(out_dir)
except:
    sys.stderr.write(out_dir + ' already exists.\n')

for dx in dx_dict:
    try:
        if os.path.isdir(config_data["data_sheets"]["dir"] + "/" + dx):
            cur_dir = ""
            if config_data["study"]["cancer_study_identifier"] == "":
                cur_dir = out_dir + dx
                if config_data['study']['dir_suffix'] != "":
                    cur_dir += config_data['study']['dir_suffix']
            else:
                cur_dir = out_dir + config_data["study"]["cancer_study_identifier"]
            cur_dir += "/"
            try:
                os.mkdir(cur_dir)
            except:
                sys.stderr.write(cur_dir + ' already exists.\n')
            sys.stderr.write("Creating meta study file for " + dx + "\n")
            canc_study_id = process_meta_study(config_data['study'], cur_dir, dx)
            data_keys = {"merged_mafs": 0, "merged_cnvs": 0, "merged_rsem": 0, "merged_protein": 0}
            for key in data_keys:
                if config_data[key]["dir"] != "":
                    data_keys[key] = 1
                    process_meta_data(config_data[key], cur_dir, canc_study_id, dx)
                    sys.stderr.write("Creating meta data files and links for " + key + "\n")
                else:
                    sys.stderr.write("Skipping meta files for " + key + "\n")
            sys.stderr.write("Creating clinical meta sheets and links\n")
            try:
                process_clinical_data(config_data["data_sheets"], cur_dir, canc_study_id, dx)
            except Exception as e:
                sys.stderr.write(str(e) + "\nerror at process_clinical_data step for " + dx + "!\n")
            try:
                create_case_lists(data_keys, cur_dir, canc_study_id, dx)
            except Exception as e:
                sys.stderr.write(str(e) + "\nerror at create_case_lists step for " + dx + "!\n")
        else:
            sys.stderr.write("No datasheets for " + dx + ", skipping!\n")
    except Exception as e:
        sys.stderr.write(str(e) + "\nerror processing files for " + dx + "!\n")
