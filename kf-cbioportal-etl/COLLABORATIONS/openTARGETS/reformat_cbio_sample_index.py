"""
Reformat a table with headers "BS_ID	Sample Type	Cbio ID" for use the existing RNA fusion coversion script.
This is to reduce repeat work
"""
import argparse

parser = argparse.ArgumentParser(
    description="Reformat sample table to fit unput required for other scripts."
)
parser.add_argument(
    "-t",
    "--table",
    action="store",
    dest="table",
    help="Table with BS ID, sample type, cBio ID",
)
parser.add_argument(
    "-n",
    "--name",
    action="store",
    dest="name",
    help="Project name",
)

args = parser.parse_args()

header = "\t".join(["Cbio_project","T_CL_BS_ID","File_Type","Cbio_Tumor_Name","File_Name","Cbio_Matched_Normal_Name","Norm_BS_ID"])
print(header)
table = open(args.table)
skip = next(table)
for line in table:
    info = line.rstrip('\n').split('\t')
    if info[1] == "RNA":
        info[1] = "rsem"
    print("\t".join([args.name, info[0], info[1], info[2], "File_Name", "Cbio_Matched_Normal_Name", "Norm_BS_ID"]))
