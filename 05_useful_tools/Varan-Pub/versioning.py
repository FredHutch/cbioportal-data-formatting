import os 
import re 


def extract_version_str(foldername):
    version=extract_version_int(foldername)
    versionname="_v"+str(version)
    return versionname

def extract_version_int(foldername):
    version=re.search(r'_v(\d+)$', foldername).group(1)
    return int(version)


def get_version_list(output_folder):
    foldername=output_folder.split("_v")[0]
    outputfolderpath=os.path.dirname(output_folder)
    if outputfolderpath=="":
        outputfolderpath="./"
    old_versions=[file for file in os.listdir(os.path.dirname(outputfolderpath)) if foldername+"_v" in file ]
    versioni_n=[extract_version_int(version) for version in old_versions ]
    sorted_version=sorted(versioni_n,key=int)
    version_name_ordered=list(map(lambda x: foldername+"_v"+str(x),sorted_version))
    return version_name_ordered

def get_newest_version(output_folder):
    outputfolderpath=os.path.dirname(output_folder)
    if outputfolderpath=="":
        outputfolderpath="./"
    old_versions=[file for file in os.listdir(os.path.dirname(outputfolderpath)) if output_folder.split("/")[-1]+"_v" in file ]
    #if len(old_versions)>0: 
    old_versions_number=list(map(extract_version_int,old_versions))
    version="_v"+str(max(old_versions_number)+1)
    output_folder_version=output_folder+version
    return output_folder_version


def create_newest_version_folder(outputfolder):
    version="_v1"
    output=outputfolder+version
    if not os.path.exists(output):
        os.mkdir(output)
        return output
    else:
        outputfolder_newest_version=get_newest_version(outputfolder)
        os.mkdir(outputfolder_newest_version)
        return outputfolder_newest_version
    


def extract_info_from_meta(folder):
    file_meta=os.path.join(folder,"meta_study.txt")
    vus=False
    with open(file_meta,'r') as meta:
        for line in meta:
            if line.startswith("type_of_cancer"):
                cancer=line.split(" ")[1]
            if line.startswith("cancer_study_identifier"):
                if "NoVus" in line:
                    vus=True
                    
    return cancer.strip(),vus 
        
        
def extract_sample_list(filecase):
    with open(filecase,'r') as meta:
        for line in meta:
            if line.startswith("case_list_ids:"):
               sample_part=line.split(":")[1]
               samples=sample_part.split("\t")
               sample_list=[sample.strip() for sample in samples]
    return sample_list       
        
        

def compare_sample_file(file1,file2,filename,action,outputfolder):
    
    summary_file= open(f"{outputfolder}/summary.txt", "a")
    if os.path.exists(file1) and os.path.exists(file2):
        samples_file1=extract_sample_list(file1)  
        samples_file2=extract_sample_list(file2)
        new_samples=[sample for sample in samples_file1 if not sample in samples_file2 and sample!=""]
        removed_samples=[sample for sample in samples_file2 if not sample in samples_file1 and sample!=""]
        
        if len(new_samples)>0:
            print(f" {len(new_samples)} new samples in {filename} : {new_samples}  ")
            print(f" {len(new_samples)} new samples in {filename} : {new_samples}  ",file=summary_file)
        if action!="update":
            if len(removed_samples)>0:
                print(f" {len(removed_samples)} removed samples in {filename} : {removed_samples}  ")
                print(f" {len(removed_samples)} removed samples in {filename} : {removed_samples}  ",file=summary_file)
    else:   
        if not os.path.exists(file1):
            print(f"{file1} does not exist")
            print(f"{file1} does not exist",file=summary_file)
        if not os.path.exists(file2):
            print(f"{file2} does not exist")
            print(f"{file2} does not exist",file=summary_file)
    summary_file.close()
    
        
def compare_version(folder1,folder2,action,outputfolder):
    case_list1=os.path.join(folder1,"case_lists")
    case_list2=os.path.join(folder2,"case_lists")
    
    
    # Compare case_list_cna
    cna_1=os.path.join(case_list1,"cases_cna.txt")
    cna_2=os.path.join(case_list2,"cases_cna.txt")

    compare_sample_file(cna_1,cna_2,"cases_cna",action,outputfolder)
    
    # Compare case_list_sequenced
    sequenced_1=os.path.join(case_list1,"cases_sequenced.txt")
    sequenced_2=os.path.join(case_list2,"cases_sequenced.txt")
    compare_sample_file(sequenced_1,sequenced_2,"cases_sequenced",action,outputfolder)
    
    # Compare case_list_sv
    sv_1=os.path.join(case_list1,"cases_sv.txt")
    sv_2=os.path.join(case_list2,"cases_sv.txt")
    compare_sample_file(sv_1,sv_2,"cases_sv",action,outputfolder)
    
    
