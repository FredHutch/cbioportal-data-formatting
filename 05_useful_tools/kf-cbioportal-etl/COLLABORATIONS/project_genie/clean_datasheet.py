import sys
import argparse
import pdb

parser = argparse.ArgumentParser(description='Blank out values where a string is in a place where a number is supposed to be')
parser.add_argument('-d', '--datasheet', action='store', dest='datasheet', help='Datasheet to update')
args = parser.parse_args()


def test_num(value):
    try:
        float(value)
        return value
    except:
        return ""

in_data = open(args.datasheet)
for i in range(0,2,1):
    head = next(in_data)
    sys.stdout.write(head)
head = next(in_data)
header = head.rstrip('\n').split('\t')
num_list = []
for i in range(len(header)):
    if header[i] == "NUMBER":
        num_list.append(i)
sys.stdout.write(head)
head = next(in_data)
sys.stdout.write(head)
head = next(in_data)
sys.stdout.write(head)
for data in in_data:
    datum = data.rstrip('\n').split('\t')
    for i in num_list:
        datum[i] = test_num(datum[i])
    print("\t".join(datum))
