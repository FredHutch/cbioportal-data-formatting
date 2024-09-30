import os
import sys
from Update_functions import *
from loguru import logger
from ValidateFolder import validateFolderlog
from versioning import *
from Make_meta_and_cases import meta_case_main
from shutil import copy

def update_main(path,newpath,output):
    
    logger.info("Starting update_main script:")
    logger.info(f"update_main args [oldpath:{path}, newpath:{newpath}, output_folder:{output}]")	

    if os.path.exists(path):    
        logger.info("Old folder found")

    if os.path.exists(newpath):
        logger.info("New folder found")
    

    old_versions=get_version_list(output)
    if len(old_versions)<=2:
        logger.warning("Only one version founded!")

    output=create_newest_version_folder(output)
    version=extract_version_str(output)
    
    logger.info(f"Creating a new folder: {output}")
    output_caseslists=os.path.join(output,"case_lists")
    os.mkdir(output_caseslists)   

    logger.info("Great! Everything is ready to start")      

    os.system("cp "+ path+"/*meta* "+output)
    
    o_clinical_sample=os.path.join(path,"data_clinical_sample.txt")
    n_clinical_sample=os.path.join(newpath,"data_clinical_sample.txt")
    if os.path.exists(o_clinical_sample) and os.path.exists(n_clinical_sample):
        update_clinical_samples(o_clinical_sample,n_clinical_sample,output)
    elif os.path.exists(o_clinical_sample) and not os.path.exists(n_clinical_sample):
        logger.warning("data_clinical_sample.txt copied from old folder")
        copy(o_clinical_sample,output)
    elif not os.path.exists(o_clinical_sample) and os.path.exists(n_clinical_sample):
        logger.warning("data_clinical_sample.txt copied from new folder")
        copy(n_clinical_sample,output)
    else:
        logger.warning("data_clinical_sample.txt not found in current folders. Skipping")

    o_clinical_patient=os.path.join(path,"data_clinical_patient.txt")
    n_clinical_patient=os.path.join(newpath,"data_clinical_patient.txt")
    if os.path.exists(o_clinical_patient) and os.path.exists(n_clinical_patient):
        update_clinical_patient(o_clinical_patient,n_clinical_patient,output)
    elif os.path.exists(o_clinical_patient) and not os.path.exists(n_clinical_patient):
        logger.warning("data_clinical_patient.txt copied from old folder")
        copy(o_clinical_patient,output)
    elif not os.path.exists(o_clinical_patient) and os.path.exists(n_clinical_patient):
        logger.warning("data_clinical_patient.txt copied from new folder")
        copy(n_clinical_patient,output)
    else:
        logger.warning("data_clinical_patient.txt not found in current folders. Skipping")
    #
    o_cna_hg19=os.path.join(path,"data_cna_hg19.seg")
    n_cna_hg19=os.path.join(newpath,"data_cna_hg19.seg")
    if os.path.exists(o_cna_hg19) and os.path.exists(n_cna_hg19):
        update_cna_hg19(o_cna_hg19,n_cna_hg19,output)
    else:
        logger.warning("data_cna_hg19_seg.txt not found in current folders. Skipping")
    #
    o_cna=os.path.join(path,"data_cna.txt")
    n_cna=os.path.join(newpath,"data_cna.txt")
    if os.path.exists(o_cna) and os.path.exists(n_cna):
        update_cna(o_cna,n_cna,output)
    elif os.path.exists(o_cna) and not os.path.exists(n_cna):
        logger.warning("data_cna.txt copied from old folder")
        copy(o_cna,output)
    elif not os.path.exists(o_cna) and os.path.exists(n_cna):
        logger.warning("data_cna.txt copied from new folder")
        copy(n_cna,output)
    else:
        logger.warning("data_cna.txt not found in current folders. Skipping")
    #
    o_mutations=os.path.join(path,"data_mutations_extended.txt")
    n_mutations=os.path.join(newpath,"data_mutations_extended.txt")
    if os.path.exists(o_mutations) and os.path.exists(n_mutations):
        update_mutations(o_mutations,n_mutations,output)
    elif os.path.exists(o_mutations) and not os.path.exists(n_mutations):
        logger.warning("data_mutations_extended.txt copied from old folder")
        copy(o_mutations,output)
    elif not os.path.exists(o_mutations) and os.path.exists(n_mutations):
        logger.warning("data_mutations_extended.txt copied from new folder")
        copy(n_mutations,output)
    else:
        logger.warning("data_mutations_extended.txt not found in current folders. Skipping")
    
    o_sv=os.path.join(path,"data_sv.txt")
    n_sv=os.path.join(newpath,"data_sv.txt")
    if os.path.exists(o_sv) and os.path.exists(n_sv):
        update_sv(o_sv,n_sv,output)
    elif os.path.exists(o_sv) and not os.path.exists(n_sv):
        logger.warning("data_sv.txt copied from old folder")
        copy(o_sv,output)
    elif not os.path.exists(o_sv) and os.path.exists(n_sv):
        logger.warning("data_sv.txt copied from new folder")
        copy(n_sv,output)
    else:
        logger.warning("data_sv.txt not found in current folders. Skipping")
  
    o_cases_cna=os.path.join(path,"case_lists/cases_cna.txt")
    n_cases_cna=os.path.join(newpath,"case_lists/cases_cna.txt")
    if os.path.exists(o_cases_cna) and os.path.exists(n_cases_cna):
        update_caselist_cna(o_cases_cna,n_cases_cna,output_caseslists)
    elif os.path.exists(o_cases_cna) and not os.path.exists(n_cases_cna):
        logger.warning("cases_cna.txt copied from old folder")
        copy(o_cases_cna,output_caseslists)
    elif not os.path.exists(o_cases_cna) and os.path.exists(n_cases_cna):
        logger.warning("cases_cna.txt copied from new folder")
        copy(n_cases_cna,output_caseslists)
    else:
        logger.warning("cases_cna.txt not found in 'case_lists' folders. Skipping")

    #
    o_cases_sequenced=os.path.join(path,"case_lists/cases_sequenced.txt")
    n_cases_sequenced=os.path.join(newpath,"case_lists/cases_sequenced.txt")
    if os.path.exists(o_cases_sequenced) and os.path.exists(n_cases_sequenced):
        update_caselist_sequenced(o_cases_sequenced,n_cases_sequenced,output_caseslists)
    elif os.path.exists(o_cases_sequenced) and not os.path.exists(n_cases_sequenced):
        logger.warning("cases_sequenced.txt copied from old folder")
        copy(o_cases_sequenced,output_caseslists)
    elif not os.path.exists(o_cases_sequenced) and os.path.exists(n_cases_sequenced):
        logger.warning("cases_sequenced.txt copied from new folder")
        copy(n_cases_sequenced,output_caseslists)
    else:
        logger.warning("cases_sequenced.txt not found in 'case_lists' folders. Skipping")

    o_cases_sv=os.path.join(path,"case_lists/cases_sv.txt")
    n_cases_sv=os.path.join(newpath,"case_lists/cases_sv.txt")
    if os.path.exists(o_cases_sv) and os.path.exists(n_cases_sv):
        update_caselist_sv(o_cases_sv,n_cases_sv,output_caseslists)
    elif os.path.exists(o_cases_sv) and not os.path.exists(n_cases_sv):
        logger.warning("cases_sv.txt copied from old folder")
        copy(o_cases_sv,output_caseslists)
    elif not os.path.exists(o_cases_sv) and os.path.exists(n_cases_sv):
        logger.warning("cases_sv.txt copied from new folder")
        copy(n_cases_sv,output_caseslists)
    else:
        logger.warning("cases_sv.txt not found in 'case_lists' folders. Skipping")

    logger.info("Starting Validation Folder...")



    cancer,vus=extract_info_from_meta(path)
    meta_case_main(cancer,vus,output)

    validateFolderlog(output)
  
    if len(old_versions)>1:
        compare_version(newpath,path,"update",output)

    logger.success("The process ended without errors")
    logger.success("Successfully updated study!")
