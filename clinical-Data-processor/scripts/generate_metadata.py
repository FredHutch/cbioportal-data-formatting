# Name:         generate_metadata.py
# Repository:   Data-processor
# Creator:      Mark De Korte
# Description:  This script creates metadata for to adhere to the cBioportal format for datasets using an annotation system to add required metadata.
# Date:         05-07-2021

# Imports
import sys, getopt
import pandas as pd
import numpy as np
import io
import random



# Define functions

# This function parses the variable annotations with tab delimitation and places /n at the end of every annotation line
def write_annotation(df, variables_amount):
    data_string = ''
    for column in df.columns.values:
        # annotation needs to be marked with #
        data_string += '#'
        c = 0
        for variable in df[column]:
            c+=1
            if variables_amount != c:
                data_string += str(variable) + '\t'
            else:
                data_string += str(variable) + '\n'
    return data_string

# This function writes data to .txt files in different formats depending on sample or patient file

def write_data(df, df_annotation, variable_list, file, ispatient):
    # Remove variables not present in the annotation file
    df_annotated_split = df_annotation.loc[df_annotation['Variables'].isin(variable_list)]
    df_annotated_split = df_annotated_split.drop(['Variables', "Sample/patient", "Yes/No"], axis = 1)

    # When patient data is added add annotation for patient ID
    new_row = [] 
    if ispatient:
        new_row.insert(0, {'Variable name cBioportal':'Patient identifier', 'Variable description': 'Patient identifier', 'Data type': 'STRING', 'Priority': 1})
    # When sample data is added both patient ID and sample ID anotation needs to be added
    else:
        new_row.insert(0,{'Variable name cBioportal':'Sample identifier', 'Variable description': 'Sample identifier', 'Data type': 'STRING', 'Priority': 1})
        new_row.insert(1, {'Variable name cBioportal':'Patient identifier', 'Variable description': 'Patient identifier', 'Data type': 'STRING', 'Priority': 1})
    
    # Add generated annotation to annotation file
    df_annotated_split = pd.concat([pd.DataFrame(new_row), df_annotated_split], ignore_index=True)

    # Write clinical data to .txt file with the correct amount of variables
    amount_of_variables = len(df_annotated_split.index)
    clinical_string = write_annotation(df_annotated_split, amount_of_variables)

    # write annotation to file declared in function
    file.write(clinical_string)


    split_df = df[df.columns[df.columns.isin(variable_list)]]

    # Duplicate patient ID's are removed, make sure to add non duplicate ID's only
    if ispatient:
        split_df = split_df.drop_duplicates(subset=['PATIENT_ID'])
    # Add sample ID list to the dataframe
    else:
        split_df.insert(loc = 0, column = 'SAMPLE_ID', value = sample_id_list)

    # Convert data to string seperated by tabs
    data_string = io.StringIO()
    split_df.to_csv(data_string, sep='\t', index=False, na_rep= "")

    # Write final data string to file
    file.write(data_string.getvalue())

# This function transforms given values to another set of values, for example c_values = [0,1] r_values=["Yes", "No"]
def reformat_logical(df, column, c_values, r_values):
    # Make list of dataframe column
    valuelist = df[column].tolist()
    c = 0

    # Loop over list and replace values with new given ones
    for v_01 in valuelist:
        try:
            # These elif statements make sure no value is Null or does not match given sets
            if pd.isnull(v_01) == True or int(v_01) != int(c_values[0]) and int(v_01) != int(c_values[1]):
                valuelist[c] = ''
            # Transform values
            elif int(v_01) == int(c_values[0]):
                valuelist[c] = str(int(v_01)).replace(c_values[0], r_values[0])
            elif int(v_01) == int(c_values[1]):
                valuelist[c] = str(int(v_01)).replace(c_values[1], r_values[1])
        except ValueError:
            valuelist[c] = ''
        c += 1
    # Return transformed values
    df[column] = valuelist
    return df

#get command line arguments
arguments = sys.argv

# Check if all needed flags are present and parse them to a string
try:
    if arguments[1] == '-i':
        inputfile = arguments[2]
    if arguments[3] == '-s':
        sheetname = arguments[4]
    if arguments[5] == '-a':
        annotation_name = arguments[6]
# Give appropriate error messaging when input is wrong
except IndexError:
    print('There seems to be something wrong with your input arguments, format:')
    print("""generate_metadata.py -i '<inputfile>' -s '<sheetname>' -a '<annotation_file_name>'""")
    exit()
# Parse input file location
input_path = 'data/input/' + inputfile

# Read excel file
try:
    df = pd.read_excel(input_path, sheet_name=sheetname)
except (FileNotFoundError, FileExistsError) as e:
    print('Something went wrong reading the input files.')
    print('Please make sure the file and sheet name are correct and the file is placed inside the input folder.')
    exit()

# Create annotation sheet
variables = df.columns
df_annotation = pd.DataFrame(columns = ['Variables', 'Variable name cBioportal', 'Variable description', 'Data type', 'Priority', 'sample/patient', 'Yes/No'])
df_annotation['Variables'] = variables

# Create metadata sheet
df_meta = pd.DataFrame(columns = ['Variable', 'Description'])
df_meta['Variable'] = ['type of cancer:','cancer study identifier:', 'name:', 'short name:', 'description:','add global case list:', 'group:']

# Give default values
df_meta['Description'] = ['','','','','', 'true', 'PUBLIC']
df_meta_p = pd.DataFrame(columns = ['Variable', 'Description'])
df_meta_s = pd.DataFrame(columns = ['Variable', 'Description'])

# Check if annotation file is present, create one when needed
try:
    f = open("data/input/" + annotation_name)
except IOError:
    # When file is not found create new annotation Excel files with functions
    print("Annotation file doesn't exist yet, creating...")
    with pd.ExcelWriter(('data/input/' + annotation_name), mode= 'w') as writer:
        df_annotation.to_excel(writer, sheet_name='Annotation', index=False)
        df_meta.to_excel(writer, sheet_name='Meta study', index=False)
    exit()

# Let user know when annotation is found and read the files found
print("Annotation file found, checking contents...")
df_annotated_variables = pd.read_excel (('data/input/' + annotation_name), 'Annotation')

# Convert all variable names to uppercase
df_annotated_variables['Variables'] = list(map(str.upper, list(df_annotated_variables['Variables'])))

# Read annotation and amount of variables
df_meta_info = pd.read_excel (('data/input/' + annotation_name), 'Meta study')
amount_of_variables = len(df_annotated_variables["Variables"])

# Check if annotation os complete, let user know when it's not and exit script
if df_annotated_variables.isnull().values.any() == False and df_meta_info.isnull().values.any() == False:
    print("Variable annotation found and complete, continuing...")
else:
    print("Variable annotation incomplete, please completely annotate the variables")
    exit()


# Create all neccessary data and meta .txt files with correct write rights
output_file_loc = "data/output/"
meta_study= open(output_file_loc + "meta_study.txt", "w+")
meta_clinical_patient= open(output_file_loc + "meta_clinical_patient.txt", "w+")
data_clinical = open(output_file_loc + "data_clinical_patient.txt", "w+")
meta_clinical_sample= open(output_file_loc + "meta_clinical_sample.txt", "w+")
data_clinical_sample= open(output_file_loc + "data_clinical_sample.txt", "w+")
data_type_cancer = open(output_file_loc + "cancer_type.txt", "w+")
meta_type_cancer = open(output_file_loc + "meta_cancer_type.txt", "w+")

#Write study and parse values from annotation
meta_study_list = df_meta_info['Description']
meta_study.write(
"""type_of_cancer: %s
cancer_study_identifier: %s
name: %s
short_name: %s
description: %s
add_global_case_list: %s
groups: %s""" % (meta_study_list[0], meta_study_list[1], meta_study_list[2], meta_study_list[3], meta_study_list[4], meta_study_list[5], meta_study_list[6]))

# Write patient meta file and parse values from annotation
meta_clinical_patient.write(
    """cancer_study_identifier: %s
genetic_alteration_type: CLINICAL
datatype: PATIENT_ATTRIBUTES
data_filename: data_clinical_patient.txt""" % (meta_study_list[1])
)

#Write sample meta file and parse values from annotation
meta_clinical_sample.write(
"""cancer_study_identifier: %s
genetic_alteration_type: CLINICAL
datatype: SAMPLE_ATTRIBUTES
data_filename: data_clinical_sample.txt""" % (meta_study_list[1])
)

# Write study metadata and parse values from annotation
data_type_cancer.write("idc_test\tInvasive Ductal Carcinoma test\tbreast,breast invasive\tHotPink\tBreast\n")
meta_type_cancer.write(
"""genetic_alteration_type: CANCER_TYPE
datatype: CANCER_TYPE
data_filename: cancer_type.txt""")


# Create lists for values marked in the annotation as "sample" on patient/sample column and/or "TRUE" on yes/no column
sample_id_names = []
list_01 = []
for index in range(len(df_annotated_variables['Variables'])):
    value_v = df_annotated_variables['Variables'][index]
    value_yn = df_annotated_variables['Yes/No'][index]
    # Find Patient ID column
    if '*' in value_v:
        patient_id_name = value_v.replace('*', '')
        df_annotated_variables['Variables'][index] = patient_id_name
        value_v = patient_id_name
    # Find column(s) for sample ID
    if '#' in value_v:
        sample_id_name = value_v.replace('#', '')
        sample_id_names.append(sample_id_name)
        df_annotated_variables['Variables'][index] = sample_id_name
    if value_yn == True:
        list_01.append(value_v)

# Remove "#" from patient ID name
patient_id_name = patient_id_name.replace('#', '')
df.columns = [cname.upper() for cname in df.columns]


df= df[list(df_annotated_variables['Variables'])]
df.columns = list(df_annotated_variables['Variables'])

sample_id_list = []
sample_id_generated = False

for column in df:
    # Check if variable has a generated sample ID
    if column in sample_id_names and sample_id_generated == False:
        # Remove values forbidden in sample IDs and parse multiple marked columns
        if len(sample_id_names) > 1:
            for i in range(len(df[column])):
                sample_id = str(list(df[sample_id_names[0]])[i]) + "-" + str(list(df[sample_id_names[1]])[i]).replace(' ', '_').replace(',','').replace('(', '').replace(')','')
                sample_id_list.append(sample_id)
        # Remove values forbidden in sample IDs and parse single marked column
        elif len(sample_id_names) == 1:
            sample_id_list = [sample_name.replace(' ', '_').replace(',','').replace('(', '').replace(')','') for sample_name in df[column].tolist()]
        if len(sample_id_list) == len(df.index):
            sample_id_generated = True

        # Rename patient ID column
        if column == patient_id_name:
            df = df.rename(columns={patient_id_name:'PATIENT_ID'})
    try:
        # Transform values to male/female
        if column == "SEX":
            df = reformat_logical(df, column, c_values = ['1', '2'], r_values = ['Male', 'Female'])

        # Transform values to adhere to cBioportal format
        if column == 'OS_STATUS':
            df = reformat_logical(df, column, c_values = ['0', '1'], r_values = ['0:LIVING', '1:DECEASED'])
        # Transform values to adhere to cBioportal format
        if column == 'DFS_STATUS':
            df = reformat_logical(df, column, c_values = ['0', '1'], r_values = ['No', 'Yes'])
    except IndexError:
        print("Unfortunately, some values could not be converted")
        

# Round of decimals to 2 decimals behind the comma
df = df.round(decimals=2)

patient_vlist = []
sample_vlist = []
sample_vlist.append("PATIENT_ID")
counter = 0
for spv in df_annotated_variables['Sample/patient']:
    if spv == 'patient':
        patient_vlist.append(df.columns.values[counter])
    if spv == 'sample':
        sample_vlist.append(df.columns.values[counter])
    counter += 1

# write data to files
write_data(df, df_annotated_variables, patient_vlist, data_clinical, ispatient=True)
write_data(df, df_annotated_variables, sample_vlist, data_clinical_sample, ispatient=False)

# Close all open files
f.close()
data_clinical.close()
meta_study.close()
meta_clinical_patient.close()
meta_clinical_sample.close()
data_clinical_sample.close()
data_type_cancer.close()
meta_type_cancer.close()
# Let user know script ran succesfully
print("File conversion succesfull! Files can be found in the /data/output directory")