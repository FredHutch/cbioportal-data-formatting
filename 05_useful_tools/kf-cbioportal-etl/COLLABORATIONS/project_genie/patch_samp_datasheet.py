import sys
import argparse

parser = argparse.ArgumentParser(description='Add col and replace with CBTN values where applicable')
parser.add_argument('-i', '--id-tbl', action='store', dest='id_tbl', help='Table with PT ID in first col, cid in second col')
parser.add_argument('-d', '--datasheet', action='store', dest='datasheet', help='Sample datasheet to update')

args = parser.parse_args()

pt_cid_tbl = open(args.id_tbl)
id_dict = {}
for line in pt_cid_tbl:
    info = line.rstrip('\n').split('\t')
    id_dict[info[1]] = info[0]

# this col was just ported over from other script, will function basically as an iterator here
dummy_col = ["External Patient Identifier", "Patient ID used by generator of data", "STRING", "1", "EXTERNAL_PATIENT_ID"]
sa_sheet = open(args.datasheet)
for col in dummy_col:
    head = next(sa_sheet)
    sys.stdout.write(head)
#     header = head.rstrip('\n').split('\t')
#     sys.stdout.write(header[0] + "\t" + col + "\t" + "\t".join(header[1:]) + "\n")

for line in sa_sheet:
    info = line.rstrip('\n').split('\t')
    parts = info[0].split('-')
    if parts[2] in id_dict:
        sys.stdout.write(id_dict[parts[2]] + "\t")
    else:
        sys.stdout.write(info[0] + "\t")
    sys.stdout.write("\t".join(info[1:]) + "\n")

