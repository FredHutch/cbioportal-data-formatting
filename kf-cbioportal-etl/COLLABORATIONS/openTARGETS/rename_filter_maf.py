import sys
import argparse
import gzip


def populate_id_map(map_fn):
    """
    Use the mapping file to create a BS ID to cBio ID mapping dict
    """
    map_file = open(map_fn)
    head = next(map_file)
    header = head.rstrip('\n').split('\t')
    b_idx = header.index('BS_ID')
    c_idx = header.index('Cbio ID')
    id_dict = {}
    for line in map_file:
        entry = line.rstrip('\n').split('\t')
        id_dict[entry[b_idx]] = entry[c_idx]
    map_file.close()
    return id_dict


def process_maf_entry(data, maf_exc, v_idx, h_idx, tid_idx, eid_idx, map_dict):
    datum = data.rstrip('\n').split('\t')
    if datum[tid_idx] in map_dict:
        # Want to allow TERT promoter as exception to exlcusion rules
        if datum[v_idx] not in maf_exc or (datum[h_idx] == "TERT" and datum[v_idx] == "5'Flank"):
            samp_id = map_dict[datum[tid_idx]]
            datum[tid_idx] = samp_id
            if eid_idx != None:
                datum.pop(eid_idx)
            return datum
    else:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to pre-filter entries on usually removed criteria except TERT promoter, convert BS IDs to cBio names')
    parser.add_argument('-m', '--mapping-file', action='store', dest = 'mapping_file', help='tsv file with header and bs_id, sample type, cbio ID mappings')
    parser.add_argument('-v', '--maf-file', action='store', dest='maf_file',
                        help='openX maf file')
    parser.add_argument('-s', '--skip', action='store', dest='skip', default=False,
                        help='Skip typical #version header line')
    parser.add_argument('-n', '--study', action='store', dest='type',
                        help='study name, like "openpbta"')


    args = parser.parse_args()
    sys.stderr.write("Getting mapping IDs\n")
    map_dict = populate_id_map(args.mapping_file)

    maf_exc = {"Silent": 0, "Intron": 0, "IGR": 0, "3'UTR": 0, "5'UTR": 0, "3'Flank": 0, "5'Flank": 0, "RNA": 0}

    # process header, track key indices and drop entrez ID
    maf_file = gzip.open(args.maf_file)
    maf_out = open(args.type + ".maf", "w")
    if args.skip:
        head = next(maf_file).decode()
        maf_out.write(head)
    else:
        sys.stderr.write('Skip flag not given. Adding typical #version header for best compatibility\n')
        print('#version 2.4', file=maf_out)
    head = next(maf_file).decode()
    header = head.rstrip("\n").split("\t")
    tid_idx = header.index('Tumor_Sample_Barcode')
    v_idx = header.index('Variant_Classification')
    h_idx = header.index('Hugo_Symbol')
    eid_idx = header.index('Entrez_Gene_Id')
    header.pop(eid_idx)
    print("\t".join(header), file=maf_out)

    sys.stderr.write("Filtering entries and renaming samples\n")

    for line in maf_file:
        to_print = process_maf_entry(line.decode(), maf_exc, v_idx, h_idx, tid_idx, eid_idx, map_dict)
        if to_print:
            print("\t".join(to_print), file=maf_out)
    sys.stderr.write("Fin.\n")
    maf_out.close()