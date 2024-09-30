#!/usr/bin/env python3

import argparse
import sys
import boto3
import botocore
import concurrent.futures
import urllib3
import os
import pandas as pd
import sevenbridges as sbg
from sevenbridges.http.error_handlers import rate_limit_sleeper, maintenance_sleeper
import pdb


def download_aws(file_type):
    """
    Function to download from AWS to file_type dir if AWS table was given
    """
    for key in key_dict:
        current = key_dict[key]["manifest"]
        dl_client = key_dict[key]["dl_client"]
        sub_file_list = list(current.loc[current["file_type"] == file_type, "s3_path"])
        sys.stderr.write('Grabbing ' + str(len(sub_file_list)) + ' files using key ' + key +'\n')
        for loc in sub_file_list:
            out = file_type + "/" + loc.split("/")[-1]
            if args.overwrite or not os.path.isfile(out):
                parse_url = urllib3.util.parse_url(loc)
                try:
                    dl_client.download_file(
                        Bucket=parse_url.host, Key=parse_url.path.lstrip("/"), Filename=out
                    )
                except Exception as e:
                    sys.stderr.write(str(e) + " could not download from " + loc + " using key " + key + "\n")
                    sys.stderr.flush()
                    err_types['aws download'] += 1
            else:
                sys.stderr.write("Skipping " + out + " it exists and overwrite not set\n")
    sys.stderr.write("Completed downloading files for " + file_type + "\n")
    sys.stderr.flush()


def download_sbg(file_type):
    """
    Function to download from SBG to file_type dir if SBG profile was given
    """
    sub_file_list = list(selected.loc[selected["file_type"] == file_type, "file_id"])
    # Sort of a "trust fall" that if aws bucket exists, skip SBG download
    if args.aws_tbl:
        sub_file_list = list(selected.loc[(selected["file_type"] == file_type) & (selected["s3_path"] == "None"), "file_id"])
    for loc in sub_file_list:
        try:
            sbg_file = api.files.get(loc)
        except Exception as e:
            sys.stderr.write('Failed to get file with id ' + loc + '\n')
            sys.stderr.write(str(e) + '\n')
            err_types['sbg get'] += 1
        out = file_type + "/" + sbg_file.name
        if args.overwrite or not os.path.isfile(out):
            try:
                sbg_file.download(out)
            except Exception as e:
                err_types['sbg download'] += 1
                sys.stderr.write('Failed to download file with id ' + loc + '\n')
                sys.stderr.write(str(e) + '\n')
        else:
            sys.stderr.write("Skipping " + out + " it exists and overwrite not set\n")

    return 0


def mt_type_download(file_type):
    """
    Download files from each desired file type at the same time
    """
    sys.stderr.write("Downloading " + file_type + " files\n")
    sys.stderr.flush()
    try:
        os.mkdir(file_type)
    except Exception as e:
        sys.stderr.write(
            str(e) + " error while making directory for " + file_type + "\n"
        )
    if args.aws_tbl:
        download_aws(file_type)
    if args.sbg_profile:
        download_sbg(file_type)


parser = argparse.ArgumentParser(description="Get all files for a project.")
parser.add_argument(
    "-m",
    "--manifest-list",
    action="store",
    dest="manifest",
    help="csv list of of genomic file location manifests",
)
parser.add_argument(
    "-f",
    "--file-types",
    action="store",
    dest="fts",
    help="csv list of workflow types to download",
)
parser.add_argument(
    "-t", "--aws-tbl", action="store", dest="aws_tbl", help="Table with bucket name and keys to subset on"
)
parser.add_argument(
    "-s", "--sbg-profile", action="store", dest="sbg_profile", help="sbg profile name. Leave blank if using AWS instead"
)
parser.add_argument(
    "-c", "--cbio", action="store", dest="cbio", help="Add cbio manifest to limit downloads"
)
parser.add_argument(
    "-a", "--active-only", default=False, action="store_true", dest="active_only", help="Set to grab only active files. Recommended."
)
parser.add_argument(
    "-d", "--debug", default=False, action="store_true", dest="debug", help="Just output manifest subset to see what would be grabbed"
)
parser.add_argument(
    "-o", "--overwrite", default=False, action="store_true", dest="overwrite", help="If set, overwrite if file exists"
)


args = parser.parse_args()
# concat multiple possible manifests
sys.stderr.write("Concatenating manifests\n")
sys.stderr.flush()
manifest_list = args.manifest.split(",")
manifest_df_list = []
for manifest in manifest_list:
    sys.stderr.write("Processing " + manifest + "\n")
    manifest_df_list.append(pd.read_csv(manifest, sep=None))
# In the event that s3_path is empty, replace with str to trigger later sbg download
manifest_concat = pd.concat(manifest_df_list, ignore_index=True)
manifest_concat.s3_path = manifest_concat.s3_path.fillna('None')
file_types = args.fts.split(",")
# subset concatenated manifests
sys.stderr.write("Subsetting concatenated manifest\n")
sys.stderr.flush()
# change col names to lower case for input compatibility
manifest_concat.columns = manifest_concat.columns.str.lower()
selected = manifest_concat[manifest_concat["file_type"].isin(file_types)]
# if active only flag set, further subset
if args.active_only:
    sys.stderr.write('active only flag given, will limit to that\n')
    selected = selected[selected["status"] == 'active']
# if cbio manifest given, limit to that
if args.cbio:
    sys.stderr.write('cBio manifest provided, limiting downloads to matching IDs\n')
    cbio_data = pd.read_csv(args.cbio, sep=None)
    specimen_list = cbio_data.T_CL_BS_ID.unique()
    selected = selected[selected["biospecimen_id"].isin(specimen_list)]
# remove vcfs as we only want mafs
pattern_del = ".vcf.gz"
filter = selected["file_name"].str.contains(pattern_del)
selected = selected[~filter]

out_file = "manifest_subset.tsv"
selected.to_csv(out_file, sep="\t", mode="w", index=False)
if args.debug:
    sys.stderr.write('Debug flag given. No downloads actually happen, just a manifest subset to preview\n')
    exit(1)
err_types = { 'aws download': 0, 'sbg get': 0, 'sbg download': 0 }
# download files by type
check = 0
if args.aws_tbl is not None:
    check = 1
    # from https://stackoverflow.com/questions/66041582/connection-pool-is-full-warning-while-reading-s3-objects-via-multiple-threads
    client_config = botocore.config.Config(
    max_pool_connections=128
)
    # setting up a key dict that, for each aws key, has an associated sesion and manifest to download with
    key_dict = {}
    bucket_errs = 0
    with open(args.aws_tbl) as kl:
        for line in kl:
            (bucket, key) = line.rstrip('\n').split('\t')
            if key not in key_dict:
                key_dict[key] = {}
                key_dict[key]['manifest'] = selected[selected['s3_path'].str.contains(bucket)]
                key_dict[key]['session'] = boto3.Session(profile_name=key)
                key_dict[key]['dl_client'] = key_dict[key]['session'].client("s3", config=client_config)
            else:
                key_dict[key]['manifest'] = pd.concat([key_dict[key]['manifest'], selected[selected['s3_path'].str.startswith(bucket)]], ignore_index=True)
            # Test bucket access with that key, if it fails, print error then kill to not waste time
            parse_url = urllib3.util.parse_url(bucket)
            try:
                key_dict[key]['dl_client'].list_objects(Bucket=parse_url.host)
            except Exception as e:
                bucket_errs = 1
                print(e, file=sys.stderr)
                print("Bucket access ERROR: {}\t{}".format(bucket, key), file=sys.stderr)
    if bucket_errs:
        exit(1)
if args.sbg_profile is not None:
    check = 1
    config = sbg.Config(profile=args.sbg_profile)
    api = sbg.Api(config=config, error_handlers=[rate_limit_sleeper, maintenance_sleeper])
if not check:
    sys.stderr.write("Please provide at least one of aws_tbl or sbg_profile\n")
    exit(1)

with concurrent.futures.ThreadPoolExecutor(16) as executor:
    results = {executor.submit(mt_type_download, ftype): ftype for ftype in file_types}

# I leave this here for debugging
# for ftype in file_types:
#     mt_type_download(ftype)

flag = 0
for key in err_types:
    if err_types[key]:
        flag += err_types[key]
        sys.stderr.write("ERROR: " + str(err_types[key]) + " " + key + " failure(s) occurred\n")
if flag:
    exit(1)
