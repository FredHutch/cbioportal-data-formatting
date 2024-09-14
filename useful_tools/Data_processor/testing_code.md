How to run Data-processor

# Change directory to the folder
cd /Users/smoorthi/github_testing_for_repo/Data-processor/

# Store the example data in the input directory
github_testing_for_repo/Data-processor/data/input/clinical_data_data_processor.xlsx


# Then move to the main folder 
cd /Users/smoorthi/github_testing_for_repo/Data-processor/

# Run the code
./generate_metadata.py -i 'clinical_data_data_processor.xlsx' -s 'sheet_1' -a 

# ERROR
-bash: ./generate_metadata.py: No such file or directory

# Give path to where the generate_metadata.py is stored 
/scripts/generate_metadata.py -i 'clinical_data_data_processor.xlsx' -s 'sheet_1' -a 

# ERROR
-bash: /scripts/generate_metadata.py: No such file or directory

# Go where the script is 
cd scripts
./generate_metadata.py -i 'clinical_data_data_processor.xlsx' -s 'sheet_1' -a 

# This atleast works but throws errors . Maybe i need to tell python to run it 
/generate_metadata.py: line 8: import: command not found
./generate_metadata.py: line 9: import: command not found
./generate_metadata.py: line 10: import: command not found
./generate_metadata.py: line 11: import: command not found
./generate_metadata.py: line 12: import: command not found
./generate_metadata.py: line 19: syntax error near unexpected token `('
./generate_metadata.py: line 19: `def write_annotation(df, variables_amount):'

# Trying this 
python ./generate_metadata.py -i 'clinical_data_data_processor.xlsx' -s 'sheet_1' -a 

# ERROR
Traceback (most recent call last):
  File "./generate_metadata.py", line 9, in <module>
    import pandas as pd
ModuleNotFoundError: No module named 'pandas'

# Looks like i need to install some dependancies 
pip3 install pandas numpy openpyxl


# Trying this 
python3 ./generate_metadata.py -i 'clinical_data_data_processor.xlsx' -s 'sheet_1' -a 

# ERROR
There seems to be something wrong with your input arguments, format:
generate_metadata.py -i '<inputfile>' -s '<sheetname>' -a '<annotation_file_name>'

# Trying this 
python3 ./scripts/generate_metadata.py -i './data/clinical_data_processor.xlsx' -s 'sheet_1' -a ' '

# Okay lets use the example that has been provided. Move that into the input folder
python3 ./scripts/generate_metadata.py -i './data/' -s '' -a

# This seems to work: gave the annotation file name
python3 ./scripts/generate_metadata.py -i 'Example_clinical_datasheet.xlsx' -s 'Sheet1' -a 'Example_clinical_datasheet_annotation.xlsx'












































