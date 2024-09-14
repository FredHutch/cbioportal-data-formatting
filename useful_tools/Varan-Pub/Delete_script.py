import os
from Make_meta_and_cases import meta_case_main
from Delete_functions import *
from ValidateFolder import validateFolderlog
from versioning import *
from loguru import logger


def delete_main(oldpath,removelist,destinationfolder):    
    logger.info("Starting delete_main script:")
    logger.info(f"delete_main args [oldpath:{oldpath}, removepath:{removelist}, destinationfolder:{destinationfolder}]")	
    
    if os.path.exists(oldpath):
        logger.info("Original folder found")
    
    if os.path.exists(removelist):
        logger.info("Sample list to remove found")
    
    old_versions=get_version_list(destinationfolder)
    if len(old_versions)<=2:
        logger.warning("Only one version founded!")
    output=create_newest_version_folder(destinationfolder)
    logger.info(f"Creating a new folder: {output}")
    output_caseslists=os.path.join(output,"case_lists")
    os.mkdir(output_caseslists)   

    logger.info("Great! Everything is ready to start")

    os.system("cp "+oldpath+"/*meta* "+output)
    sampleIds=open(removelist,"r").readlines()
    sampleIds=[sample.strip() for sample in sampleIds]

    
    o_clinical_patient=os.path.join(oldpath,"data_clinical_patient.txt")
    if os.path.exists(o_clinical_patient):
        delete_clinical_patient(oldpath,sampleIds,output)
    else:
        logger.warning("data_clinical_patient.txt not found in current folder. Skipping")
    #
    o_clinical_sample=os.path.join(oldpath,"data_clinical_sample.txt")
    if os.path.exists(o_clinical_sample) :
        delete_clinical_samples(o_clinical_sample,sampleIds,output)
    else:
        logger.warning("data_clinical_sample.txt not found in current folder. Skipping")
    
    o_cna_hg19=os.path.join(oldpath,"data_cna_hg19.seg")
    if os.path.exists(o_cna_hg19):
        delete_cna_hg19(o_cna_hg19,sampleIds,output)
    else:
        logger.warning("data_cna_hg19.seg not found in current folder. Skipping")
    
    #
    o_cna=os.path.join(oldpath,"data_cna.txt")
    if os.path.exists(o_cna):
        delete_cna(o_cna,sampleIds,output)
    else:
        logger.warning("data_cna.txt not found in current folder. Skipping")
    
    #
    o_mutations=os.path.join(oldpath,"data_mutations_extended.txt")
    if os.path.exists(o_mutations):
        delete_mutations(o_mutations,sampleIds,output)
    else:
        logger.warning("data_mutations_extended.txt not found in current folder. Skipping")
    #
    o_sv=os.path.join(oldpath,"data_sv.txt")
    if os.path.exists(o_sv):
        delete_sv(o_sv,sampleIds,output)
    else:
        logger.warning("data_sv.txt not found in current folder. Skipping")
    #
    
    o_cases_cna=os.path.join(oldpath,"case_lists/cases_cna.txt")
    if os.path.exists(o_cases_cna):
        delete_caselist_cna(o_cases_cna,sampleIds,output_caseslists)
    else:
        logger.warning("cases_cna.txt not found in 'case_lists' folder. Skipping")
    
    o_cases_sequenced=os.path.join(oldpath,"case_lists/cases_sequenced.txt")
    if os.path.exists(o_cases_sequenced):
        delete_caselist_sequenced(o_cases_sequenced,sampleIds,output_caseslists)
    else:
        logger.warning("cases_sequenced.txt not found in 'case_lists' folder. Skipping")
    #  
    o_cases_sv=os.path.join(oldpath,"case_lists/cases_sv.txt")
    if os.path.exists(o_cases_sv):
        delete_caselist_sv(o_cases_sv,sampleIds,output_caseslists)
    else:
        logger.warning("cases_sv.txt not found in 'case_lists' folder. Skipping")



    cancer,vus=extract_info_from_meta(oldpath)
    meta_case_main(cancer,vus,output)


    logger.info("Starting Validation Folder...")

    validateFolderlog(output)
    
    
    
    if len(old_versions)>1:
        old_version=old_versions[-1]
        compare_version(output,old_version,"delete",output)
    
    
    logger.success("The process ended without errors")
    logger.success("Please, check DeleteScript.log to verify that everything went as expected.")
    logger.success("Successfully deleted sample(s)!")
