import pandas as pd
import os
import numpy as np
import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed

"""
This script will convert Gatk seg file to cbio wide format and generate three output files: cnv_discrete, cnv_continuous and cnv_seg files

command line: python3 get_gatk_cnv_long_format.py --config ../STUDY_CONFIGS/pbta_all_treatment_data_processing_config.json --etl_file etl_file.tsv --file_type_key gatk_seg --output_folder merged_cnv/

"""


def define_score_metrix(absolute_CN, gain):
    # Converting score to GITSIC style values
    #
    score_matrix = {0: -absolute_CN}
    for i in range(1, absolute_CN + gain + 1, 1):
        if i < absolute_CN:
            score_matrix[i] = -1
        elif i == absolute_CN:
            score_matrix[i] = 0
        else:
            score_matrix[i] = 1
    return score_matrix


def convert(x, cnv_gain_threshold):
    absolute_CN = 2
    score_metrix = define_score_metrix(absolute_CN, cnv_gain_threshold)
    if x in score_metrix:
        return score_metrix[x]
    else:
        return 2


def get_seg_data(seg):
    # Read seg data and return the data as a list
    seg_data = []
    with open(seg, "r") as f:
        switch_on = "OFF"
        for line in f:
            if "START" in line or switch_on == "ON":
                switch_on = "ON"
                line = line.replace("\n", "")
                line_data = line.split("\t")
                seg_data.append(line_data)
    return seg_data


def map_genes_seg_to_ref(seg_file_data, ref_gene_bed_list):
    # map gene from bed list to seg list
    header = seg_file_data.pop(0)
    ref_genes = []
    for calls in seg_file_data:
        gene = ""
        for ref in ref_gene_bed_list:
            if (
                ref[0] == calls[0]  # chr
                and int(ref[1]) < int(calls[1])  # start
                and int(ref[2]) >= int(calls[2])  # end
            ):
                gene = ref[3]
                break
        ref_genes.append(gene)

    seg_file_data_df = pd.DataFrame(seg_file_data, columns=header)
    seg_file_data_df[header[1]] = seg_file_data_df[header[1]].apply(int)
    seg_file_data_df[header[2]] = seg_file_data_df[header[2]].apply(int)
    seg_file_data_df[header[3]] = seg_file_data_df[header[3]].apply(int)
    seg_file_data_df[header[4]] = seg_file_data_df[header[4]].apply(float)
    seg_file_data_df["gene"] = ref_genes

    return seg_file_data_df


def get_ref_bed_data(ref_file_path):
    # read ref data to map genes returns data as a list

    ref_gene_bed = pd.read_csv(
        ref_file_path, sep="\t", names=["chr", "start", "end", "gene"]
    )
    ref_gene_bed["chr"] = "chr" + ref_gene_bed["chr"]
    ref_gene_bed_list = ref_gene_bed.values.tolist()

    return ref_gene_bed_list


def extract_integer(string_data):
    # change chr format in the seg file to wide format
    return string_data.replace("chr", "")


def prepare_seg_output(seg_data, cbio_ID):
    # seg_data_df=seg_data_df.drop(["CALL"])
    seg_data["CONTIG"] = seg_data["CONTIG"].map(extract_integer)
    seg_data = seg_data.drop(["CALL", "gene"], axis=1)
    seg_data["ID"] = str(cbio_ID)
    seg_data = seg_data.rename(
        columns={
            "CONTIG": "chrom",
            "START": "loc.start",
            "END": "loc.end",
            "NUM_POINTS_COPY_RATIO": "num.mark",
            "MEAN_LOG2_COPY_RATIO": "seg.mean",
        }
    )
    ID_i = seg_data.pop("ID")
    seg_data.insert(0, "ID", ID_i)
    return seg_data


def pick_longest_segment(x):
    # pick the longest segment call when gene is found in gain and loss CNVs
    x["dif_x"] = x["END_x"] - x["START_x"]  # segment length (gain)
    x["dif_y"] = x["END_y"] - x["START_y"]  # segment length (loss)
    if x["dif_x"] > x["dif_y"]:
        x = x[["Hugo_Symbol", "cnv_score_continuous_x", "cnv_score_discrete_x"]]
    elif x["dif_x"] < x["dif_y"]:
        x = x[["Hugo_Symbol", "cnv_score_continuous_y", "cnv_score_discrete_y"]]
    elif abs(x["cnv_score_discrete_x"]) > abs(x["cnv_score_discrete_y"]):
        x = x[["Hugo_Symbol", "cnv_score_continuous_x", "cnv_score_discrete_x"]]
    elif abs(x["cnv_score_discrete_x"]) < abs(x["cnv_score_discrete_y"]):
        x = x[["Hugo_Symbol", "cnv_score_continuous_y", "cnv_score_discrete_y"]]
    else:
        x = x[["Hugo_Symbol", "cnv_score_continuous_x", "cnv_score_discrete_x"]]

    x.index = [
        "Hugo_Symbol",
        "cnv_score_continuous",
        "cnv_score_discrete",
    ]  # reindex series
    return x


def set_longest_segment_call(tmp_df):
    # this function picks longest segment call among duplicate gene calls (#only loss or only gain cnvs)
    tmp_df["dif"] = tmp_df["END"] - tmp_df["START"]
    concat_df = pd.DataFrame(
        columns=[
            "START",
            "END",
            "Hugo_Symbol",
            "cnv_score_continuous",
            "cnv_score_discrete",
            "dif",
        ]
    )
    unique_gene = set(tmp_df["Hugo_Symbol"])
    for gene in unique_gene:
        tmp_pick = (
            tmp_df[tmp_df["Hugo_Symbol"] == gene]
            .sort_values("dif", ascending=False)
            .drop_duplicates(subset="Hugo_Symbol", keep="first")
        )
        concat_df = pd.concat([concat_df, tmp_pick])
    concat_df = concat_df.drop(["dif"], axis=1)

    return concat_df


def prepare_gat_cnv_from_seg_file(
    seg_file, sample_ID, ref_gene_bed_list, map_cbio_BS_IDs, cnv_gain_threshold
):
    # prepare data in wide format for per seg file
    seg_data = get_seg_data(seg_file)
    seg_data_df = map_genes_seg_to_ref(seg_data, ref_gene_bed_list)
    seg_data_df = seg_data_df.convert_dtypes()

    cbio_ID_list = map_cbio_BS_IDs[map_cbio_BS_IDs["T_CL_BS_ID"] == sample_ID][
        "Cbio_Tumor_Name"
    ].values
    if len(cbio_ID_list) > 0:
        cbio_ID = cbio_ID_list[0]
    else:
        print(
            "cbio tumor id not found for ", sample_ID, "therefore ignoring this sample"
        )
        return []

    seg_processing = seg_data_df.copy()
    seg_output = prepare_seg_output(seg_processing, cbio_ID)

    seg_data_df["cnv_score_continuous"] = round(
        pow(2, seg_data_df["MEAN_LOG2_COPY_RATIO"])
    )
    seg_data_df["cnv_score_discrete"] = seg_data_df["cnv_score_continuous"].apply(
        convert, cnv_gain_threshold=cnv_gain_threshold
    )
    seg_data_df = seg_data_df.drop(
        ["MEAN_LOG2_COPY_RATIO", "CALL", "NUM_POINTS_COPY_RATIO", "CONTIG"],
        axis=1,
    )
    seg_data_df = seg_data_df[seg_data_df["gene"].astype(bool)]
    cnv_per_sample = seg_data_df
    cnv_per_sample.rename(columns={"gene": "Hugo_Symbol"}, inplace=True)

    df_without_duplicate_gene = cnv_per_sample[
        cnv_per_sample["Hugo_Symbol"].duplicated(keep=False) == False
    ]  # dropping all the duplicate genes

    df_duplicate_genes = cnv_per_sample[
        cnv_per_sample["Hugo_Symbol"].duplicated(keep=False) == True
    ]  # extracting duplicate genes
    df2_loss_cnv = df_duplicate_genes[
        df_duplicate_genes["cnv_score_discrete"] < 0
    ]  # criteria for loss
    df2_gain_cnv = df_duplicate_genes[
        df_duplicate_genes["cnv_score_discrete"] > 0
    ]  # creteria for gain

    # remove duplicate and pick longesr segment or high magnitude
    df2_loss_cnv = set_longest_segment_call(df2_loss_cnv.copy())
    df2_gain_cnv = set_longest_segment_call(df2_gain_cnv.copy())

    # check for common gene is gain and loss cnv
    inner = pd.merge(df2_gain_cnv, df2_loss_cnv, on=["Hugo_Symbol"], how="inner")

    gain_plus_loss = pd.concat([df2_loss_cnv, df2_gain_cnv])
    gain_plus_loss = gain_plus_loss.drop_duplicates(subset=["Hugo_Symbol"], keep=False)
    gain_plus_loss = gain_plus_loss.drop(["START", "END"], axis=1)
    df_without_duplicate_gene = df_without_duplicate_gene.drop(["START", "END"], axis=1)

    if not inner.empty:
        inner = inner.apply(pick_longest_segment, axis=1)
    else:
        inner = pd.DataFrame(
            columns=["Hugo_Symbol", "cnv_score_continuous", "cnv_score_discrete"]
        )

    df_without_duplicate_gene = pd.concat(
        [df_without_duplicate_gene, gain_plus_loss, inner]
    )  # Add duplicate gene back

    cnv_discrete_per_sample = df_without_duplicate_gene.drop(
        ["cnv_score_continuous"], axis=1
    )  # prepare df for discrete scores
    cnv_discrete_per_sample = cnv_discrete_per_sample.rename(
        columns={"cnv_score_discrete": str(cbio_ID)}
    )
    cnv_continuous_per_sample = df_without_duplicate_gene.drop(
        ["cnv_score_discrete"], axis=1
    )  # prepare df for continuous scores
    cnv_continuous_per_sample["cnv_score_continuous"] = cnv_continuous_per_sample[
        "cnv_score_continuous"
    ].astype("int")
    cnv_continuous_per_sample = cnv_continuous_per_sample.rename(
        columns={"cnv_score_continuous": str(cbio_ID)}
    )

    return [cnv_discrete_per_sample, cnv_continuous_per_sample, seg_output]


def outer_merge_list(df_list, on_header):
    merged_list = df_list[0]
    for i in range(1, len(df_list), 1):
        merged_list = pd.merge(merged_list, df_list[i], how="outer", on=on_header)
    return merged_list


def run_process_pool(cpu_workers):
    process = []
    results = []
    print("Setting pool threads with max CPUs:", cpu_workers)

    # prepare a list with sample ID and file name for multi process
    run_loop_list = etl_data[[biospecimen_header, "File_Name"]].values.tolist()

    with ProcessPoolExecutor(max_workers=cpu_workers) as executor:
        for entry in run_loop_list:
            file_path = segfiles_folder_path + "/" + entry[1]
            sample_ID = entry[0]
            print("firing a process for:", sample_ID, "=", file_path)
            if os.path.isfile(file_path) and file_path.endswith(".seg"):
                process.append(
                    executor.submit(
                        prepare_gat_cnv_from_seg_file,
                        file_path,
                        sample_ID,
                        ref_gene_bed_list,
                        etl_data,
                        cnv_gain_threshold,
                    )
                )
        print("Waiting for processes to finish and collecting outputs")
        for active_cpu in as_completed(process):
            result_per_process = active_cpu.result()
            if len(result_per_process) > 0:
                results.append(result_per_process)

    return results


if __name__ == "__main__":
    # Instantiate the parser
    parser = argparse.ArgumentParser(
        description="Prepare gatk seg file for cbio portal wide format. Output file: continuous, discrete, & seg CNVs"
    )

    # Required positional argument
    parser.add_argument("--config", help="Seg file for cnv ")
    parser.add_argument(
        "--etl_file",
        help="Table with cbio project, kf bs ids, cbio IDs, and file names",
    )
    parser.add_argument(
        "--file_type_key", help="Provide file type key to recognize gatk seg files"
    )
    parser.add_argument(
        "--output_folder", help="Provide output folder path relative to current folder"
    )
    args = parser.parse_args()

    # Opening JSON file
    with open(args.config) as json_file:
        json_dict = json.load(json_file)

    # read variables from json dict
    segfiles_folder_path = json_dict["file_loc_defs"]["cnvs"]["gatk_seg"]
    gene_bed_ref_filename = json_dict["bed_genes"]
    cpu_workers = json_dict["cpus"]
    cnv_gain_threshold = json_dict["cnv_high_gain"]

    etl = args.etl_file
    output_folder_path = os.getcwd() + "/" + args.output_folder  # output dir

    biospecimen_header = "T_CL_BS_ID"
    file_type = args.file_type_key
    if not os.path.isfile(etl):
        raise TypeError("Cannot find given manifest file")
    else:
        print("Reading etl file:", etl)
        etl_data = pd.read_csv(etl, sep="\t", header=0)

    etl_data = etl_data[etl_data["File_Type"] == file_type]
    etl_data = etl_data[etl_data[biospecimen_header].duplicated() == False]

    ref_gene_bed_list = get_ref_bed_data(
        gene_bed_ref_filename
    )  # used for gene mapping to seg calls

    # read & process files using multi process to resturn results
    results = run_process_pool(int(cpu_workers))

    # code to split results list into 2 separate lists
    discrete_list, continous_list, seg_list = map(list, zip(*results))
    df_discrete = outer_merge_list(discrete_list, "Hugo_Symbol")
    df_discrete = df_discrete.convert_dtypes()
    df_discrete = df_discrete.replace(np.nan, 0, regex=True)  # fill nans
    df_discrete = df_discrete.sort_values("Hugo_Symbol")

    # flatten continuous list of list
    df_continous = outer_merge_list(continous_list, "Hugo_Symbol")
    df_continous = df_continous.convert_dtypes()
    df_continous = df_continous.replace(np.nan, 2, regex=True)  # fill nans
    df_continous = df_continous.sort_values("Hugo_Symbol")

    # flatten seg list of list
    df_seg = pd.concat(seg_list)
    df_seg = df_seg.replace(np.nan, "", regex=True)  # fill nans
    df_seg = df_seg.sort_values(["ID", "chrom", "loc.start"])

    # write output files
    df_continous.to_csv(
        os.path.join(output_folder_path, "cnv_continous.txt"), sep="\t", index=False
    )
    df_discrete.to_csv(
        os.path.join(output_folder_path, "cnv_discrete.txt"), sep="\t", index=False
    )
    df_seg.to_csv(
        os.path.join(output_folder_path, "cnv_seg.txt"), sep="\t", index=False
    )
