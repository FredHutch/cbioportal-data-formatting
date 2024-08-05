# ZeroDates. Script converts strings from date formats (xx/xx/xxxx) into integer offset (e.g., 12 = 12 days after Day Zero).
# Inputs: folderpath, patient_info_filename, zero_day_column_name
# Outputs: All *_data_*.txt files in the folderpath are copied into "zeroed" subfolder, with all date strings converted to ints for offset days.
import datetime
from pathlib import Path
import os
import sys

# Mandatory
#  folderpath = 'Prostate_TAN'
#  patient_info_filename = "data_clinical_patient.txt"
#  zero_day_column_name =  "DIAGNOSISDATE"   # "FIRST_DATE_OF_METASTASIS"

# Optional
debug_output = False
day_offset_for_errors = -1234 # If this value shows up in output, an error occured (e.g. empty cell)
date_format = '%Y-%m-%d'


# Internal globals
patient_zeros = {}
patient_fails = []


def transform_file(folderpath, filename, output_folder):
    global debug_output
    global day_offset_for_errors
    global column_names
    global patient_zeros
    global patient_fails
    
    is_patient_file = filename == "data_clinical_patient.txt"
    if debug_output:
        print('START transforming ' + filename)
    print('START transforming ' + filename)

    
    data_folder = Path(folderpath)
    file_to_open = data_folder / filename
    print("file_to_open=[" + str(file_to_open) + "]")
    f = open(file_to_open)
    content = f.readlines()


    # Add AGEATDIAGNOSIS column, as calculation of BIRTHDATE (a negative integer,from diagnosis.)
    # e.g., BIRTHDATE=-3650 means age at diagnosis is exactly ABS(BIRTHDATE)/365 = 10 years old.
    # We do it here, rather than upstream in column creation, to avoid duplicating date logic.
    # The "{:-2]" strips the CRLF off the string, so we can add the new column.
    # Do similar to add OS_STATUS and OS_MONTHS columns.
    if is_patient_file:
        print("============= HEADERS original")
        print(str(content[0]))
        print(str(content[1]))
        print(str(content[2]))
        print(str(content[3]))
        print(str(content[4]))
        print(str(content[5]))

        column_names.append("AGEATDIAGNOSIS")
        print("Going to add AGEATDIAGNOSIS to raw_content...")
        content[0] = content[0][:-1] +"\tAGEATDIAGNOSIS" +"\tOS_STATUS" +"\tOS_MONTHS" + "\r\n"
        content[1] = content[1][:-1]  +"\tAGEATDIAGNOSIS" +"\tOS_STATUS" +"\tOS_MONTHS" + "\r\n"
        content[2] = content[2][:-1]  +"\tNUMBER" +"\tSTRING" +"\tNUMBER" + "\r\n"
        content[3] = content[3][:-1]  +"\t1" +"\t1" +"\t1" + "\r\n"
        content[4] = content[4][:-1]  +"\tAGEATDIAGNOSIS" +"\tOS_STATUS" +"\tOS_MONTHS" + "\r\n"

        print("============= HEADERS+1")
        print(str(content[0]))
        print(str(content[1]))
        print(str(content[2]))
        print(str(content[3]))
        print(str(content[4]))
        print(str(content[5]))


    # Build list of columns with dates
    # if column has 'date' in part of row 5, transform it.
    column_names = content[4].rstrip().split('\t')
    if debug_output:
        print(column_names)
    date_idx_list = [i for i, value in enumerate(column_names) if "DATE" in value.upper()]
    print ("Date indices list : " + str(date_idx_list) +"\n")

    if is_patient_file:
        # Find index of BIRTHDATE, to calculate AGEOFDIAGNOSIS later.
        birthdate_index = -1
        # for idx in column_names:
        #     print("idx is...")
        #     print(idx)
        #     if column_names[idx] == "BIRTHDATE":
        #         birthdate_index = idx
        print("column_names is...")
        print(column_names)
        birthdate_index = column_names.index("BIRTHDATE")
        print("birthdate_index = " + str(birthdate_index))
        lastalivedate_index = column_names.index("LASTALIVEDATE")
        print("lastalivedate_index = " + str(lastalivedate_index))
        deathdate_index = column_names.index("DEATHDATE")
        print("deathdate_index = " + str(deathdate_index))
        

    # Run through lines of file. If > 5th line, do transformation.
    for idx, val in enumerate(content):
        row = val.rstrip().split('\t')
        
        if idx < 5:
            # header rows
            # print(val)
            if idx == 2:
                # Turn likely STRING to NUMBER type, as we go from '03/13/20' to an int.
                for i, date_index_val in enumerate(date_idx_list):
                    date_index = date_idx_list[i]                
                    row[date_index] = "NUMBER"
                    row_final = "\t".join(row)+"\n"
                    content[idx] = row_final
                    
        else:
            # data rows
            

            # If Excel doesn't have values for every column,
            # let's stick in empty cells. But should probably be a warning.
            row = row + [""] * (len(column_names) - len(row))
            if debug_output:
                print('row len ' + str(len(row)))
                print('row=('+str(row)+')')
            
            patient_id = row[0]
            zero_day = False
            if patient_id in patient_zeros:
                zero_day = patient_zeros[patient_id]

            # Process each column with "DATE" in its name.
            for i, date_index_val in enumerate(date_idx_list):

                date_index = date_idx_list[i]
                # print('date index for i='+str(i)+' is ' + str(date_index))
                
                raw_date_text = row[date_index]
                

                if zero_day == False:
                    row[date_index] = str(day_offset_for_errors)
                else:
                    try:
                        this_day = zero_day + datetime.timedelta(days=day_offset_for_errors)  # assume bad until string passes checks
                        if (raw_date_text != 'NaT') and (raw_date_text != ''):
                            this_day = datetime.datetime.strptime(raw_date_text, date_format)
                        delta = this_day - zero_day
                        days_as_str = str(delta.days)
                        row[date_index] = days_as_str
                    except Exception as e: 
                        print(str(date_index)+" zero day exception for ["+raw_date_text+"]" )
                        type, value, traceback = sys.exc_info()
                        print('Error ZERO_DAY_EXCEPTION %s: %s' % (value.filename, value.strerror))
                        row[date_index] = str(day_offset_for_errors)

                if date_index == len(row)-1:
                    if debug_output:
                        print("last column, value=",row[date_index])
                    row[date_index] = row[date_index]  # + "\n"

            if is_patient_file:
                # Calculate AGEATDIAGNOSIS, OS_STATUS, OS_MONTHS, put in last 3 columns. One decimal place for age (years), 2 places for OS_MONTHS.
                
                # print("row[birthdate_index] is...")
                # print(str(row[birthdate_index]))
                birthdate_as_number = int(row[birthdate_index])
                # print("birthdate_as_number...")
                # print(birthdate_as_number)
                age_in_years = abs(birthdate_as_number)/365

                row[len(row)-3] = "{:.1f}".format(age_in_years)


                is_dead = str(row[deathdate_index]) != "-1234"
                os_status =  "LIVING"
                if is_dead:
                        os_status = "DECEASED"
                row[len(row)-2] = os_status

                days_last_alive_or_death = max(int(row[deathdate_index]), int(row[lastalivedate_index]))
                os_months = days_last_alive_or_death / 30
                # if days_last_alive_or_death == 0:
                #     os_months = 0.01  # Bit of a hack. KM estimate might not like zero months.
                row[len(row)-1] = "{:.2f}".format(os_months)

            row_final = "\t".join(row)+"\n"
            content[idx] = row_final
            if debug_output:
                print(idx, row_final+"\n")

    # ----------------output_filename = "zerodate_" + filename
    output_data_folder = Path(output_folder)
    file_to_open = output_data_folder / filename

    file2 = open(file_to_open, "w")
    with file_to_open.open("w") as f:
        f.writelines(content)
    
    if debug_output:
        print("DONE transforming     " + filename + "\n\n")


def zero_dates(folderpath, patient_info_filename = "data_clinical_patient.txt", zero_day_column_name =  "DIAGNOSISDATE", output_folder="." ):
    global debug_output
    global column_names
    global patient_zeros
    global patient_fails

    zero_day_column = -1
    with open(folderpath + "/" + patient_info_filename, 'r', newline='\r\n') as f:
        content = f.readlines()
        column_names = content[4].rstrip().split('\t')
        zero_day_column = column_names.index(zero_day_column_name)

    print("zero_day_column in " + patient_info_filename + " is " + str(zero_day_column))
    if zero_day_column < 0 :
        raise "Zero day column missing!"
    
    patient_zeros = {}  # dict where key=patientId, value=datetime object of zero day.
    patient_fails = []  # list of patientIds without a zero day value.

    # Find zero day for each patient.
    for x in range(5,len(content)): 
        row = content[x].rstrip().split('\t')
        patient_id = row[0]
        zero_day_string = row[zero_day_column]
        try:
            zero_date = datetime.datetime.strptime(zero_day_string, date_format) #   '%m/%d/%Y')
            #    new_row = patient_id, zero_date
            patient_zeros[patient_id] = zero_date
        except Exception as e: 
            patient_fails.append(patient_id)

    print('patient_zeros, count=' + str(len(patient_zeros)))
    print('patient_fails, count=' + str(len(patient_fails)))

    files = os.listdir(folderpath)
    print('Files to transform dates in:')
    #print('SAMPLE ONLY=========')
    for file in files:
        if file.startswith("data") and file.endswith(".txt"):
            print(file) #(os.path.join(root, file))
    print("--START--")

    for filename in files:
        if filename.startswith("data") and filename.endswith(".txt"):
            transform_file(folderpath, filename, output_folder)

    print("--END--")
    print("Look for output files, with the prefix 'zerodate_'.")

