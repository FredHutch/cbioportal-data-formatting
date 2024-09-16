import sys
import argparse
import json
import math
import pdb


def format_desc(entry):
    desc = entry.replace(".", " ")
    return desc

 
def format_colname(entry):
    col_name = entry.replace(".", "_").upper()
    return col_name


def init_list(header_list, entry):
    '''
    Initialize list of list of header entries
    '''
    header_list.append([])
    if h_dict[entry][m_idx] == "":
        header_list[0].append(entry)
    else:
        header_list[0].append(h_dict[entry][m_idx])
    header_list.append([])
    if h_dict[entry][d_idx] == "":
        header_list[1].append(format_desc(entry))
    else:
        header_list[1].append(h_dict[entry][d_idx])
    header_list.append([])
    header_list[2].append(h_dict[entry][t_idx])
    header_list.append([])
    header_list[3].append(h_dict[entry][o_idx])
    header_list.append([])
    if h_dict[entry][0] == "":
        header_list[4].append(format_colname(entry))
    else:
        header_list[4].append(h_dict[entry][0])
    return header_list


def build_header(header_list, entry):
    '''
    Keep adding to existing entries in header list of list
    '''
    if not header_list:
        header_list = init_list(header_list, entry)
    else:
        if h_dict[entry][m_idx] == "":
            header_list[0].append(entry)
        else:
            header_list[0].append(h_dict[entry][m_idx])
        if h_dict[entry][d_idx] == "":
            header_list[1].append(format_desc(entry))
        else:
            header_list[1].append(h_dict[entry][d_idx])
        header_list[2].append(h_dict[entry][t_idx])
        header_list[3].append(h_dict[entry][o_idx])
        if h_dict[entry][m_idx] == "":
            header_list[4].append(format_colname(entry))
        else:
            header_list[4].append(h_dict[entry][m_idx])

    return header_list


parser = argparse.ArgumentParser(description='Script to convert clinical data to cbio clinical data sheets')
parser.add_argument('-f', '--header-file', action='store', dest="head" ,help='tsv file with input file original sample '
                    'names, output sheet flag, and conversion')
parser.add_argument('-o', '--oncotree-map', action='store', dest="onco" ,help='oncotree code mapping file, '
                    ' tsv with oncotree code, KF dx, and oncotree value')
parser.add_argument('-c', '--clinical-data', action='store', dest='clin',
                    help='Input clinical data sheet')

args = parser.parse_args()

# read in header key file to assign some of the clinical data headers to cbio standard ones and to all a data type and sheet location
# File header is: original	MAP TO	description	sample	patient	type	order
h_dict = {}
h_file = open(args.head)

h_head = next(h_file)
h_header = h_head.rstrip('\n').split('\t')
# Get key header loc, shift-1 since fist col used as key
# header cols currently: original	MAP TO	description	sample	patient	type	order
m_idx = h_header.index("MAP TO") - 1
d_idx = h_header.index("description") - 1
s_idx = h_header.index("sample") - 1
p_idx = h_header.index("patient") - 1
t_idx = h_header.index("type") - 1
o_idx = h_header.index("order") - 1
for line in h_file:
    info = line.rstrip('\n').split('\t')
    h_dict[info[0]] = info[1:]

clin_data = open(args.clin)
head = next(clin_data)
"""
Data sheet header format:
["#Patient Identifier\tSample Identifier\tSPECIMEN_ID\tCANCER_TYPE\tCANCER_TYPE_DETAILED\tTUMOR_TISSUE_SITE\tTUMOR_TYPE\tSAMPLE_TYPE\tMATCHED_NORMAL_SAMPLE_ID\tMATCHED_NORMAL_SPECIMEN_ID\tCBTTC_PAIRED_IDS",
    "#Patient identifier\tSample Identifier using external_sample_id\tkfdrc tumor biopsecimen ID\tStudy-defined cancer type\tStudy-defined cancer type detail\ttumor tissue location\tprimary v metastatic tumor designation\tpatient tissue sample or cell line\tmatched normal external_sample_id\tkfdrc matched normal biospecimen ID\tOriginal CBTTC DNA/RNA pair ids, where applicable",
    "#STRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING",
    "#1\t1\t1\t1\t0\t1\t1\t1\t1\t1\t1"
    "PATIENT_ID\tSAMPLE_ID\tSPECIMEN_ID\tCANCER_TYPE\tCANCER_TYPE_DETAILED\tTUMOR_TISSUE_SITE\tTUMOR_TYPE\tSAMPLE_TYPE\tMATCHED_NORMAL_SAMPLE_ID\tMATCHED_NORMAL_SPECIMEN_ID\tCBTTC_PAIRED_IDS\n"],

"""
header = head.rstrip('\n').split('\t')
# name of columns to use to calculate AGE value
age_names = ["Overall.Survival", "Age.at.Last.Known.Clinical.Status"]
outs = {}
sample_out = open("data_clinical_sample.txt", "w")
patient_out = open("data_clinical_patient.txt", "w")
# initialize first entry, as it has all leading "#""
patient_head_list = []
sample_head_list = []
for entry in header:
    if entry in h_dict:
        if h_dict[entry][s_idx] == '1':
            sample_head_list = build_header(sample_head_list, entry)
        if h_dict[entry][p_idx] == '1':
            patient_head_list = build_header(patient_head_list, entry)

# add at end specially calculated age column
age_header = ["AGE", "Age at which the condition or disease was first diagnosed, in years", "NUMBER", "22", "AGE"]
# add DFS STATUS
dfs_status =  ["DFS_STATUS", "Disease free (months) since initial treatment", "STRING", "17", "DFS_STATUS"]
# add cancer detailed and oncotree code headers
cancer_detailed = ["CANCER_TYPE_DETAILED", "OncoTree translation of diagnosis", "STRING", "30", "CANCER_TYPE_DETAILED"]
oncotree_code = ["ONCOTREE_CODE", "OncoTree alphanumeric code value for CANCER_TYPE_DETAILED", "STRING", "29", "ONCOTREE_CODE"]
for i in range(len(age_header)):
    patient_head_list[i].append(age_header[i])
    patient_head_list[i].append(dfs_status[i])
    sample_head_list[i].append(cancer_detailed[i])
    sample_head_list[i].append(oncotree_code[i])

# output headers to files
for i in range(0, 4, 1):
    sample_out.write("#" + "\t".join(sample_head_list[i]) + "\n")
    patient_out.write("#" + "\t".join(patient_head_list[i]) + "\n")
sample_out.write("\t".join(sample_head_list[-1]) + "\n")
patient_out.write("\t".join(patient_head_list[-1]) + "\n")
# pt dict to track if already seen to avoid duplicate output
pt_id_dict = {}
diagnosis_type_dict = {"Initial CNS Tumor": "primary", "Progressive": "progression", "Recurrence": "recurrence" }

# read in oncotree code info to patch in
onco_dict = {}
onco_file = open(args.onco)
skip = next(onco_file)
for line in onco_file:
    (code, dx, name) = line.rstrip('\n').split('\t')
    onco_dict[dx] = [name, code.lower()]


# iterate through data, calculate field values in special cases
#pdb.set_trace()

for data in clin_data:
    info = data.rstrip('\n').split('\t')
    try:
        pt_id = info[header.index("Kids.First.ID")]
    except Exception as e:
        sys.stderr.write(str(e) + "\n")
        pdb.set_trace()
        hold=1
    if pt_id in pt_id_dict:
        pt_id_dict[pt_id] += 1
    else:
        pt_id_dict[pt_id] = 1

    ovr_surv, age_at_last_known, d_free_mos, cancer_type_detailed, oncotree_code = -1, -1, "NA", "NA", "NA"
    sample_to_print = []
    patient_to_print = []
    for i in range(len(info)):
        value = info[i]
        if h_dict[header[i]][t_idx] == "NUMBER":
            try:
                float(value)
            except ValueError:
                value = "NA"
        if header[i] == "Last.Known.Clinical.Status":
            if value.startswith("Deceased"):
                value = "DECEASED"
            else:
                value = "LIVING"
        elif header[i] == "diagnosis_type":
            if value in diagnosis_type_dict:
                value = diagnosis_type_dict[value]
        elif header[i] == "Overall.Survival" and value != "NA" and value != "Not Reported":
            ovr_surv = int(value)
            value = str(math.floor(float(value)/30.5))
        elif header[i] == "Age.at.Last.Known.Clinical.Status":
            age_at_last_known = int(value)
        elif header[i] == "Progression_Free_Survival":
            if value == "NA":
                if ovr_surv != -1:
                    value = str(math.floor(float(ovr_surv)/30.5))
            else:
                value = str(math.floor(float(value)/30.5))
                d_free_mos = value
        elif header[i] == "diagnosis":
            cancer_type_detailed = onco_dict[value][0]
            oncotree_code = onco_dict[value][1]
        if h_dict[header[i]][s_idx] != '0':
            sample_to_print.append(value)
        if h_dict[header[i]][p_idx] != '0' and pt_id_dict[pt_id] == 1:
            patient_to_print.append(value)
    if pt_id_dict[pt_id] == 1:
        age = float(age_at_last_known)
        if ovr_surv != -1:
            age -= float(ovr_surv) 
        age = str(math.floor(age/365.25))
        patient_to_print.append(age)
        # pdb.set_trace()
        d_free_status = "DiseaseFree"
        try:
            int(d_free_mos)
            d_free_status = "Recurred/Progressed"
        except ValueError:
            pass
        patient_to_print.append(d_free_status)
        patient_out.write("\t".join(patient_to_print) + "\n")
    sample_to_print.append(cancer_type_detailed)
    sample_to_print.append(oncotree_code)
    sample_out.write("\t".join(sample_to_print) + "\n")
    
sample_out.close()
patient_out.close()
