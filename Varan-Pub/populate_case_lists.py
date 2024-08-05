import os
import pandas as pd
from configparser import ConfigParser
from versioning import extract_version_str

def populate_cases_sv(cancer, project_name,vus, folder,cases_list_dir,version,logger):
    """
        Function to populate cases_sv file
    Args:
        cancer : cancer type
        vus : Flag to select Vus inclusion
        cases_list_dir : path of case_list output dir
    """
    try:
        data_sv=pd.read_csv(os.path.join(folder,"data_sv.txt"),sep="\t")
    except pd.errors.EmptyDataError:
        logger.error("data_sv.txt is empty, skipping this step!")
        return
    nsamples=len(data_sv.Sample_Id.unique())
    sample_ids=list(data_sv.Sample_Id.unique())
    
    if vus:
        study_id = cancer+project_name+version+"_NoVus"
    else:
        study_id = cancer+project_name+version

    stable_id = study_id+"_sv"
    case_list_name = "Samples with SV data"
    case_list_description = "All samples (+"+str(nsamples)+") samples"
    case_list_category = "all_cases_with_sv_data"
    case_list_ids = "\t".join(sample_ids)

    dictionary_file = {
        "cancer_study_identifier": study_id,
        "stable_id": stable_id,
        "case_list_name": case_list_name,
        "case_list_description": case_list_description,
        "case_list_category": case_list_category,
        "case_list_ids": case_list_ids,
    }
    
    case_sv_file = open(f"{cases_list_dir}/cases_sv.txt", "w")
    for key, value in dictionary_file.items():
        logger.info(f"{key}: {value}", file=case_sv_file)
        print(f"{key}: {value}", file=case_sv_file)
    case_sv_file.close()
#


def populate_cases_cna(cancer, project_name,vus,folder, cases_list_dir,version,logger):
    """
        Function to populate cases_cna file
    Args:
        cancer : cancer type
        vus : Flag to select Vus inclusion
        cases_list_dir : path of case_list output dir
    """
    
    try:
        data_cna=pd.read_csv(os.path.join(folder,"data_cna.txt"),sep="\t")
    except pd.errors.EmptyDataError:
        logger.error("data_cna.txt is empty, skipping this step!")
        return
    
    nsamples=len(data_cna.columns)-1
    sample_ids=list(data_cna.columns)[1:]
    
    if vus:
        study_id = cancer+project_name+version+"_NoVus"
    else:
        study_id = cancer+project_name+version

    stable_id = study_id+"_cna"

    case_list_category = "all_cases_with_cna_data"
    case_list_name = "Samples with CNA data"
    case_list_description = "Samples with CNA data ("+str(nsamples)+ " samples)"
    case_list_ids = "\t".join(sample_ids)

    dictionary_file = {
        "cancer_study_identifier": study_id,
        "stable_id": stable_id,
        "case_list_category": case_list_category,
        "case_list_name": case_list_name,
        "case_list_description": case_list_description,
        "case_list_ids": case_list_ids,
    }

    case_cna_file = open(f"{cases_list_dir}/cases_cna.txt", "w")
    for key, value in dictionary_file.items():
        logger.info(f"{key}: {value}", file=case_cna_file)
        print(f"{key}: {value}", file=case_cna_file)
    case_cna_file.close()


def populate_cases_sequenced(cancer,project_name, vus,folder, cases_list_dir,version,logger):
    """
        Function to populate cases_sequenced file
    Args:
        cancer : cancer type
        vus : Flag to select Vus inclusion
        cases_list_dir : path of case_list output dir
    """

    try:
        data_sequenced=pd.read_csv(os.path.join(folder,"data_mutations_extended.txt"),sep="\t")
    except pd.errors.EmptyDataError:
        logger.error("data_mutations_extended.txt is empty, skipping this step!")
        return
    nsamples=len(data_sequenced["Tumor_Sample_Barcode"].unique())
    sample_ids=list(data_sequenced["Tumor_Sample_Barcode"].unique())


    if vus:
        study_id = cancer+project_name+version+"_NoVus"
    else:
        study_id = cancer+project_name+version

    stable_id = study_id+"_sequenced"

    case_list_category = "all_cases_with_mutation_data"
    case_list_name = "Sequenced Tumors"
    case_list_description = "All sequenced samples (" +str(nsamples)+"samples)"
    case_list_ids = "\t".join(sample_ids)

    dictionary_file = {
        "cancer_study_identifier": study_id,
        "stable_id": stable_id,
        "case_list_category": case_list_category,
        "case_list_name": case_list_name,
        "case_list_description": case_list_description,
        "case_list_ids": case_list_ids,
    }

    meta_file = open(f"{cases_list_dir}/cases_sequenced.txt", "w")
    for key, value in dictionary_file.items():
        logger.info(f"{key}: {value}", file=meta_file)
        print(f"{key}: {value}", file=meta_file)
    meta_file.close()


