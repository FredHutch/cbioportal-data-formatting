# Name:         generate_metadata_modified.py
# Repository:   Data-processor
# Creator:      Mark De Korte
# Description:  This script creates metadata for cBioPortal datasets using an annotation system to add required metadata.
# Date:         09-15-2024
# Edited by:    Sitapriya Moorthi

# Imports
import sys
import pandas as pd
import numpy as np
import io

# Define functions

# This function parses the variable annotations with tab delimitation and places /n at the end of every annotation line
def write_annotation(df, variables_amount):
    data_string = ''
    for column in df.columns.values:
        # annotation needs to be marked with #
        data_string += '#'
        c = 0
        for variable in df[column]:
            c += 1
            if variables_amount != c:
                data_string += str(variable) + '\t'
            else:
                data_string += str(variable) + '\n'
    return data_string

# This function writes data to .txt files in different formats depending on sample or patient file
def write_data(df, df_annotation, variable_list, file, ispatient):
    # Remove variables not present in the annotation file
    df_annotated_split = df_annotation.loc[df_annotation['Variables'].isin(variable_list)]
    df_annotated_split = df_annotated_split.drop(['Variables', "Sample/patient", "Yes/No"], axis=1)

    # Debug print statements to check dataframe status
    print(f"Data annotation split for {'patient' if ispatient else 'sample'} data: \n", df_annotated_split)

    # When patient data is added, add annotation for patient ID
    new_row = [] 
    if ispatient:
        new_row.insert(0, {'Variable name cBioportal': 'Patient identifier', 'Variable description': 'Patient identifier', 'Data type': 'STRING', 'Priority': 1})
    # When sample data is added both patient ID and sample ID annotation needs to be added
    else:
        new_row.insert(0, {'Variable name cBioportal': 'Sample identifier', 'Variable description': 'Sample identifier', 'Data type': 'STRING', 'Priority': 1})
        new_row.insert(1, {'Variable name cBioportal': 'Patient identifier', 'Variable description': 'Patient identifier', 'Data type': 'STRING', 'Priority': 1})
    
    # Add generated annotation to annotation file
    df_annotated_split = pd.concat([pd.DataFrame(new_row), df_annotated_split], ignore_index=True)

    # Write clinical data to .txt file with the correct amount of variables
    amount_of_variables = len(df_annotated_split.index)
    clinical_string = write_annotation(df_annotated_split, amount_of_variables)

    # Debug print to check annotation string
    print(f"Annotation string:\n{clinical_string}")

    # Write annotation to file declared in function
    file.write(clinical_string)

    split_df = df[df.columns[df.columns.isin(variable_list)]]

    # Debugging the content of split_df
    print(f"Split DataFrame for {'patient' if ispatient else 'sample'} data: \n", split_df.head())

    # Duplicate patient IDs are removed, make sure to add non-duplicate IDs only
    if ispatient:
        split_df = split_df.drop_duplicates(subset=['PATIENT_ID'])
    # Add sample ID list to the dataframe
    else:
        split_df.insert(loc=0, column='SAMPLE_ID', value=sample_id_list)

    # Debugging after adding SAMPLE_ID
    print(f"DataFrame after adding SAMPLE_ID (for sample data): \n", split_df.head())

    # Convert data to string separated by tabs
    data_string = io.StringIO()
    split_df.to_csv(data_string, sep='\t', index=False, na_rep="")

    # Write final data string to file
    file.write(data_string.getvalue())

# This function transforms given values to another set of values, for example c_values = [0,1] r_values=["Yes", "No"]
def reformat_logical(df, column, c_values, r_values):
    valuelist = df[column].tolist()
    c = 0
    for v_01 in valuelist:
        try:
            if pd.isnull(v_01) or (int(v_01) not in [int(c_values[0]), int(c_values[1])]):
                valuelist[c] = ''
            elif int(v_01) == int(c_values[0]):
                valuelist[c] = r_values[0]
            elif int(v_01) == int(c_values[1]):
                valuelist[c] = r_values[1]
        except ValueError:
            valuelist[c] = ''
        c += 1
    df[column] = valuelist
    return df

# Get command line arguments
arguments = sys.argv

# Check if all needed flags are present and parse them to a string
try:
    if arguments[1] == '-i':
        inputfile = arguments[2]
    if arguments[3] == '-s':
        sheetname = arguments[4]
    if arguments[5] == '-a':
        annotation_name = arguments[6]
except IndexError:
    print('There seems to be something wrong with your input arguments, format:')
    print("""generate_metadata.py -i '<inputfile>' -s '<sheetname>' -a '<annotation_file_name>'""")
    exit()

input_path = 'data/input/' + inputfile

# Read excel file
try:
    df = pd.read_excel(input_path, sheet_name=sheetname)
except (FileNotFoundError, FileExistsError):
    print('Something went wrong reading the input files. Please make sure the file and sheet name are correct and the file is placed inside the input folder.')
    exit()
# Display DataFrame columns for debugging
print("Columns in DataFrame:", df.columns)

# Check if a specific column exists to filter patient and sample data
# Modify this part to use the correct column for filtering
if 'PATIENT_ID' in df.columns and '#SAMPLE_ID' in df.columns:
    # Assume all data in df is relevant; if you have specific columns or conditions, apply them here
    df_patient = df[df['PATIENT_ID'].notna()]
    df_sample = df[df['#SAMPLE_ID'].notna()]
else:
    print("Error: Required columns are missing from the DataFrame.")
    exit()

# Create annotation sheet
variables = df.columns
df_annotation = pd.DataFrame(columns=['Variables', 'Variable name cBioportal', 'Variable description', 'Data type', 'Priority', 'Sample/patient', 'Yes/No'])
df_annotation['Variables'] = variables

# Create metadata sheet
df_meta = pd.DataFrame(columns=['Variable', 'Description'])
df_meta['Variable'] = ['type of cancer:', 'cancer study identifier:', 'name:', 'short name:', 'description:', 'add global case list:', 'group:']
df_meta['Description'] = ['', '', '', '', '', 'true', 'PUBLIC']

# Check if annotation file is present, create one when needed
try:
    f = open("data/input/" + annotation_name)
except IOError:
    print("Annotation file doesn't exist yet, creating...")
    with pd.ExcelWriter('data/input/' + annotation_name, mode='w') as writer:
        df_annotation.to_excel(writer, sheet_name='Annotation', index=False)
        df_meta.to_excel(writer, sheet_name='Meta study', index=False)
    exit()

print("Annotation file found, checking contents...")
df_annotated_variables = pd.read_excel('data/input/' + annotation_name, 'Annotation')
df_annotated_variables['Variables'] = df_annotated_variables['Variables'].str.upper()
df_meta_info = pd.read_excel('data/input/' + annotation_name, 'Meta study')

if df_annotated_variables.isnull().values.any() or df_meta_info.isnull().values.any():
    print("Variable annotation incomplete, please completely annotate the variables")
    exit()

# Create all necessary data and meta .txt files with correct write rights
output_file_loc = "data/output/"
meta_study = open(output_file_loc + "meta_study.txt", "w+")
meta_clinical_patient = open(output_file_loc + "meta_clinical_patient.txt", "w+")
data_clinical_patient = open(output_file_loc + "data_clinical_patient.txt", "w+")
meta_clinical_sample = open(output_file_loc + "meta_clinical_sample.txt", "w+")
data_clinical_sample = open(output_file_loc + "data_clinical_sample.txt", "w+")
data_type_cancer = open(output_file_loc + "cancer_type.txt", "w+")
meta_type_cancer = open(output_file_loc + "meta_cancer_type.txt", "w+")

# Write study meta
meta_study_list = df_meta_info['Description']
meta_study.write(
"""type_of_cancer: %s
cancer_study_identifier: %s
name: %s
short_name: %s
description: %s
add_global_case_list: %s
groups: %s""" % tuple(meta_study_list)
)

# Write patient meta file
meta_clinical_patient.write(
"""cancer_study_identifier: %s
genetic_alteration_type: CLINICAL
datatype: PATIENT_ATTRIBUTES
data_filename: data_clinical_patient.txt""" % meta_study_list[1]
)

# Write sample meta file
meta_clinical_sample.write(
"""cancer_study_identifier: %s
genetic_alteration_type: CLINICAL
datatype: SAMPLE_ATTRIBUTES
data_filename: data_clinical_sample.txt""" % meta_study_list[1]
)

# Write cancer type data
data_type_cancer.write("idc_test\tInvasive Ductal Carcinoma test\tbreast,breast invasive\tHotPink\tBreast\n")
meta_type_cancer.write(
"""genetic_alteration_type: CANCER_TYPE
datatype: CANCER_TYPE
data_filename: cancer_type.txt"""
)

# Generate patient/sample lists
sample_id_names = []
patient_id_name = ''
for index, value_v in enumerate(df_annotated_variables['Variables']):
    value_yn = df_annotated_variables['Yes/No'][index]
    if '*' in value_v:
        patient_id_name = value_v.replace('*', '')
        df_annotated_variables.loc[index, 'Variables'] = patient_id_name
    if '#' in value_v:
        sample_id_name = value_v.replace('#', '')
        sample_id_names.append(sample_id_name)
        df_annotated_variables.loc[index, 'Variables'] = sample_id_name

df_patient = df[df["SAMPLE_TYPE"] == 'patient']
df_sample = df[df["SAMPLE_TYPE"] == 'sample']
sample_id_list = list(df_sample["SAMPLE_ID"].unique())

# Write patient and sample data to files
write_data(df_patient, df_annotated_variables, list(df_patient.columns), data_clinical_patient, True)
write_data(df_sample, df_annotated_variables, list(df_sample.columns), data_clinical_sample, False)

# Close all files
meta_study.close()
meta_clinical_patient.close()
data_clinical_patient.close()
meta_clinical_sample.close()
data_clinical_sample.close()
data_type_cancer.close()
meta_type_cancer.close()

# Let user know script ran successfully
print("File conversion successful! Files can be found in the /data/output directory")
