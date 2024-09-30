#!/usr/bin/python
"""
Script that can be cleaned up.
Removes entries from a table using a list of banned values.
Usage:
  python subtract_by_id.py <id_list> <colname> <out_flag> <in_file>
  To have no out_flag, provide "SKIP_THIS" as the value
"""

import sys
import pdb

id_list = {}
with open(sys.argv[1]) as rm_list:
    for line in rm_list:
        id_list[line.rstrip('\n')] = 0
colname = sys.argv[2]
out_flag = sys.argv[3]
with open(sys.argv[4]) as in_file:
    head = next(in_file)
    header = head.rstrip('\n').split('\t')
    c_idx = header.index(colname)
    o_idx = None
    if out_flag != "SKIP_THIS":
        out_list = []
        o_idx = header.index(out_flag)
    print(head, end='')
    for line in in_file:
        info = line.rstrip('\n').split('\t')
        if info[c_idx] not in id_list:
            print(line, end='')
        elif o_idx is not None:
            out_list.append(info[o_idx])
if o_idx is not None:
    print("\n".join(list(set(out_list))), file=sys.stderr)