import sys
import argparse
import pdb

parser = argparse.ArgumentParser(description='Add col and replace with CBTN values where applicable')
parser.add_argument('-i', '--data', action='store', dest='data_tbl', help='Input data table to subset')
parser.add_argument('-s', '--src-col-num', action='store', dest='src_col', help='0-based column number to use hash IDs from source')
parser.add_argument('-c', '--column-number', action='store', dest='col_num', help='0-based column number to use to search for IDs')
parser.add_argument('-d', '--datasheet', action='store', dest='datasheet', help='Sample datasheet to to index')

args = parser.parse_args()

samp_sheet = open(args.datasheet)
sid_dict = {}
s = 1
if args.src_col:
    s = int(args.src_col)
if args.src_col:
    for i in range(0,5,1):
        skip = next(samp_sheet)
for line in samp_sheet:
    info = line.rstrip('\n').split('\t')
    sid_dict[info[s]] = 0
samp_sheet.close()
col_num = int(args.col_num)
data_tbl = open(args.data_tbl)
head = next(data_tbl)
sys.stdout.write(head)
for line in data_tbl:
    info = line.rstrip('\n').split('\t')
    #pdb.set_trace()
    if info[col_num] in sid_dict:
        sys.stdout.write(line)
data_tbl.close()
 