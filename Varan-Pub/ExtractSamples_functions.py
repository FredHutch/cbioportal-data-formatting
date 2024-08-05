import os
import pandas as pd
import re


def extract_clinical_samples(file_path,sample_ids,output_folder):
    """
    Extracts specific clinical information for samples from the original data_clinical_samples.txt and saves the result to a new file.
    
    This function reads a tab-separated CSV file from the given `file_path`, extracts rows
    corresponding to the provided list of `sample_ids`, and saves the extracted data, along with
    the header information, to a new tab-separated file named 'data_clinical_sample.txt' in the
    specified `output_folder`. If some sample identifiers are not found in the DataFrame, a warning
    message is printed.

    Args:
        file_path (str): Path to the original data_clinical_sample.
        sample_ids (list): List of sample identifiers to extract from the file.
        output_folder (str): Path to the output folder where the extracted data will be saved.

    Example:
      >>>  extract_clinical_samples('input_data.csv', ['sample1', 'sample2'], 'output_folder/')
    """
    file=pd.read_csv(file_path,sep="\t")
    header=file.loc[0:3,:]
    file=pd.read_csv(file_path,sep="\t")
    extracted=file[file["Sample Identifier"].astype(str).isin(sample_ids)]
    if not all([sample in file["Sample Identifier"].unique() for sample in sample_ids ]):
        print("[Warning] Some samples names are not present in the DataFrame data_clinical_samples.")
    extracted=pd.concat([header,extracted])
    extracted.to_csv(os.path.join(output_folder,"data_clinical_sample.txt"),index=False,
                   sep="\t")

def extract_clinical_patient(oldpath,sample_ids,output_folder):
    
    """
    Extracts clinical patient data corresponding to specified sample identifiers and saves the result to a new file. 
    
    This function reads the 'data_clinical_patient.txt' file from the original data_clinical_patient, along with the 'data_clinical_sample.txt'
    file that should be present in the same directory. It extracts patient data rows based on the given `sample_ids`, determined by
    matching the '#Patient Identifier' from 'data_clinical_sample.txt'. The extracted patient data, including the header information,
    is saved to a new tab-separated file named 'data_clinical_patient.txt' in the specified `output_folder`. If some sample identifiers
    are not found in the DataFrame, a warning message is printed.

    Args:
        oldpath (str): Path to the folder containing the input 'data_clinical_patient.txt' and 'data_clinical_sample.txt' files.
        sample_ids (list): List of sample identifiers for which patient data will be extracted.
        output_folder (str): Path to the output folder where the extracted patient data will be saved.

    Example:
      >>>  extract_clinical_patient('input_folder/', ['sample1', 'sample2'], 'output_folder/')
    """
    
    file=pd.read_csv(os.path.join(oldpath,"data_clinical_patient.txt"),sep="\t")
    sample=pd.read_csv(os.path.join(oldpath,"data_clinical_sample.txt"),sep="\t")
    patient_ids=list(sample[sample["Sample Identifier"].astype(str).isin(sample_ids)]["#Patient Identifier"])
    header=file.loc[0:3,:]
    extracted=file[file["#Patient Identifier"].astype(str).isin(patient_ids)]
    if not all([patient in file["#Patient Identifier"].unique() for patient in patient_ids]):
        print("[Warning] Some samples names are not present in the DataFrame data_clinical_patient.")
    extracted=pd.concat([header,extracted])    
    extracted.to_csv(os.path.join(output_folder,"data_clinical_patient.txt"),index=False,
                   sep="\t")
   

def extract_cna_hg19(file_path,sample_ids,output_folder):
    """
    Extracts specific samples from a copy number alteration (CNA) data file in hg19 genome format.
    
    This function reads a tab-separated CNA data file specified by 'file_path', extracts the rows
    corresponding to the provided 'sample_ids', and saves the extracted data into a new file named
    'data_cna_hg19.seg' in the 'output_folder'.

    Args:
        file_path (str): Path to the input CNA data file in tab-separated format.
        sample_ids (list): List of sample IDs (as strings) to be extracted from the input file.
        output_folder (str): Path to the directory where the extracted data file will be saved.

    Notes:
        - The input file is expected to have a column named "ID" containing sample IDs.
        - If any sample ID provided in 'sample_ids' is not found in the input file, a warning
          will be printed indicating that some sample names are not present in the DataFrame.
        - The extracted data is saved in the 'data_cna_hg19.seg' file in tab-separated format.

    Example:
        extract_cna_hg19('input_data.tsv', ['sample1', 'sample2'], 'output_folder/')
      >>>  Extracts data for 'sample1' and 'sample2' from 'input_data.tsv' and saves it in 'output_folder/data_cna_hg19.seg'.
    """

    file=pd.read_csv(file_path,sep="\t")
    extracted=file[file["ID"].astype(str).isin(sample_ids)]
    if not all([sample in file["ID"].unique() for sample in sample_ids]):
        print("[Warning] Some samples names are not present in the DataFrame data_cna_hg19.")
    extracted.to_csv(os.path.join(output_folder,"data_cna_hg19.seg"),index=False,
                   sep="\t")
        
    
def extract_cna(file_path,sample_ids,output_folder):
    """
    Extracts specific samples' copy number alteration (CNA) data from the original CNA  file.

    This function reads the original tab-separated CNA data file specified by 'file_path', extracts the columns
    corresponding to the provided 'sample_ids', and saves the extracted data into a new file named
    'data_cna.txt' in the 'output_folder'.
    Args:
        file_path (str): Path to the input CNA data file in tab-separated format.
        sample_ids (list): List of sample IDs (column names) to be extracted from the input file.
        output_folder (str): Path to the directory where the extracted data file will be saved.
    Notes:
        - The input file is expected to have a header row with column names.
        - If any sample ID provided in 'sample_ids' is not found in the input file's columns, a warning
          will be printed indicating that some sample names are not present in the DataFrame.
        - The extracted data is saved in the 'data_cna.txt' file in tab-separated format.

    Example:
      >>> extract_cna('input_data.tsv', ['sample1', 'sample2'], 'output_folder/')
    """
    file=pd.read_csv(file_path,sep="\t")
    columns_to_keep = [sample for sample in sample_ids if sample in file.columns]
    if not all([sample in file.columns for sample in sample_ids]):
        print("[Warning] Some samples names are not present in the DataFrame data_cna.")
    columns_to_keep.insert(0, file.columns[0])
    extracted=file.loc[:,columns_to_keep]
    extracted.to_csv(os.path.join(output_folder,"data_cna.txt"),index=False,
                   sep="\t")
        
def extract_mutations(file_path,sample_ids,output_folder):
    """
    Extracts specific samples' mutation data from the original `data_mutations_extended.txt`
    
    This function reads a tab-separated mutation data file specified by 'file_path', extracts the rows
    corresponding to the provided 'sample_ids', and saves the extracted data into a new file named
    'data_mutations_extended.txt' in the 'output_folder'.
    
    Args:
        file_path (str): Path to the input mutation data file in tab-separated format.
        sample_ids (list): List of sample IDs (Tumor_Sample_Barcode values) to be extracted from the input file.
        output_folder (str): Path to the directory where the extracted data file will be saved.
    Notes:
        - The input file is expected to have a column named "Tumor_Sample_Barcode" containing sample IDs.
        - If any sample ID provided in 'sample_ids' is not found in the input file, a warning
          will be printed indicating that some sample names are not present in the DataFrame.
        - The extracted data is saved in the 'data_mutations_extended.txt' file in tab-separated format.

    Example:
       >>> extract_mutations('input_mutations.tsv', ['sample1', 'sample2'], 'output_folder/')
    """
    
    file=pd.read_csv(file_path,sep="\t")
    extracted=file[file["Tumor_Sample_Barcode"].astype(str).isin(sample_ids)]
    if not all([sample in file["Tumor_Sample_Barcode"].unique() for sample in sample_ids ]):
        print("[Warning] Some samples names are not present in the DataFrame data_mutations_extended .")
    extracted.to_csv(os.path.join(output_folder,"data_mutations_extended.txt"),index=False,
                   sep="\t")
    
def extract_sv(file_path,sample_ids,output_folder):
    """
    Extracts specific samples' structural variation (SV) data from the original `data_sv.txt`.
    
    This function reads a text file specified by 'file_path', extracts the lines
    corresponding to the provided 'sample_ids', and saves the extracted data into a new file named
    'data_sv.txt' in the 'output_folder'.

    Args:
        file_path (str): Path to the input SV data file.
        sample_ids (list): List of sample IDs or keywords to be extracted from the input file.
        output_folder (str): Path to the directory where the extracted data file will be saved.
    Notes:
        - Each line in the input file is assumed to represent an SV record.
        - If any sample ID or keyword provided in 'sample_ids' is found in a line, that line is extracted.
        - The extracted data is saved in the 'data_sv.txt' file.

    Example:
      >>>  extract_sv('input_sv.txt', ['sample1', 'sample2'], 'output_folder/')
    """

    old_file=pd.read_csv(file_path,sep="\t")
    new_file=old_file[old_file["Sample_Id"].isin(sample_ids)]
    new_file.to_csv(os.path.join(output_folder,"data_sv.txt"),sep="\t",index=False)


def extract_caselist_cna(file_path,sample_ids,output_folder):
    """
    Extracts specific cases' CNA data from the CNA case list file.
    
    This function reads a text file specified by 'file_path', extracts the case list IDs
    corresponding to the provided 'sample_ids', and saves the modified case list file in the 'output_folder'.

    Args:
        file_path (str): Path to the input case list file.
        sample_ids (list): List of case IDs to be extracted from the case list.
        output_folder (str): Path to the directory where the modified case list file will be saved.
    
    Notes:
        - The case list file is assumed to have sections starting with "case_list_ids" and "case_list_description".
        - The function first identifies the relevant case IDs based on 'sample_ids' and modifies the case list
          description and IDs accordingly.
        - The modified case list is saved in a new file named 'cases_cna.txt' in the 'output_folder'.

    Example:
        >>> extract_caselist_cna('input_case_list.txt', ['case1', 'case2'], 'output_folder/')
    """
    with open(file_path,"r") as file:
        for line in file:
            line=line.strip()
            if line.startswith("case_list_ids"):
                samples=line.split(":")[1].split("\t")
                samples=list(map(str.strip, samples))
                extracted=[elem for elem in samples if elem in sample_ids]
        
        with open(os.path.join(output_folder,"cases_cna.txt"),"w") as filtered:
                file.seek(0)
                for line in file:
                    if line.startswith("case_list_description"):
                        n_old_samples=re.findall(r'\d+',line)[0]
                        line=line.replace(n_old_samples,str(len(extracted)))
                        
                    if line.startswith("case_list_ids"):
                        line="case_list_ids:"+"\t".join(extracted)
                    filtered.write(line)
        

def extract_caselist_sequenced(file_path,sample_ids,output_folder):
    """
    Extracts specific cases' sequenced data from the original sequenced case list file.
   
    This function reads a text file specified by 'file_path', extracts the case list IDs
    corresponding to the provided 'sample_ids', and saves the modified case list file in the 'output_folder'.

    Args:
        file_path (str): Path to the input case list file.
        sample_ids (list): List of case IDs to be extracted from the case list.
        output_folder (str): Path to the directory where the modified case list file will be saved.
    Notes:
        - The case list file is assumed to have sections starting with "case_list_ids" and "case_list_description".
        - The function first identifies the relevant case IDs based on 'sample_ids' and modifies the case list
          description and IDs accordingly.
        - The modified case list is saved in a new file named 'cases_sequenced.txt' in the 'output_folder'.
    
    Example:
        >>> extract_caselist_sequenced('input_case_list.txt', ['case1', 'case2'], 'output_folder/')
    """
    with open(file_path,"r") as file:
        for line in file:
            line=line.strip()
            if line.startswith("case_list_ids"):
                samples=line.split(":")[1].split("\t")
                samples=list(map(str.strip, samples))
                extracted=[elem for elem in samples if elem in sample_ids]
        
        with open(os.path.join(output_folder,"cases_sequenced.txt"),"w") as filtered:
                file.seek(0)
                for line in file:
                    if line.startswith("case_list_description"):
                        n_old_samples=re.findall(r'\d+',line)[0]
                        line=line.replace(n_old_samples,str(len(extracted)))
                        
                    if line.startswith("case_list_ids"):
                        line="case_list_ids:"+"\t".join(extracted)
                    filtered.write(line)
    
    
def extract_caselist_sv(file_path,sample_ids,output_folder):
    """
    Extracts specific cases of structural variation (SV) data from the original SV case list file.
    
    This function reads a text file specified by 'file_path', extracts the case list IDs
    corresponding to the provided 'sample_ids', and saves the modified case list file in the 'output_folder'.

    Args:
        file_path (str): Path to the input case list file.
        sample_ids (list): List of case IDs to be extracted from the case list.
        output_folder (str): Path to the directory where the modified case list file will be saved.
  
    Notes:
        - The case list file is assumed to have sections starting with "case_list_ids" and "case_list_description".
        - The function first identifies the relevant case IDs based on 'sample_ids' and modifies the case list
          description and IDs accordingly.
        - The modified case list is saved in a new file named 'cases_sv.txt' in the 'output_folder'.

    Example:
        >>> extract_caselist_sv('input_case_list.txt', ['case1', 'case2'], 'output_folder/')
    """
    with open(file_path,"r") as file:
        for line in file:
            line=line.strip()
            if line.startswith("case_list_ids"):
                samples=line.split(":")[1].split("\t")
                samples=list(map(str.strip, samples))
                extracted=[elem for elem in samples if elem in sample_ids]
        
        with open(os.path.join(output_folder,"cases_sv.txt"),"w") as filtered:
                file.seek(0)
                for line in file:
                    if line.startswith("case_list_description"):
                        n_old_samples=re.findall(r'\d+',line)[0]
                        line=line.replace(n_old_samples,str(len(extracted)))
                        
                    if line.startswith("case_list_ids"):
                        line="case_list_ids:"+"\t".join(extracted)
                    filtered.write(line)