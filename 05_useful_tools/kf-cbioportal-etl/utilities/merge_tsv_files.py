import pandas as pd
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="File to merge two tsv files based on common columns. It will only retain common columns in the output file")

    parser.add_argument('-1','--first_file',help="First file to merge")
    parser.add_argument('-2','--second_file',help="Second file to merge")
    parser.add_argument('-o','--output_file',help="Name of output file")

    args=parser.parse_args()

    consensus = pd.read_csv(args.first_file, sep='\t')
    scavenged = pd.read_csv(args.second_file, sep='\t')

    #print(consensus.shape)
    #print(scavenged.shape)

    consensus_col=consensus.columns
    scavenged_col=scavenged.columns

    common_cols = consensus_col.intersection(scavenged_col)

    consensus_common=consensus[common_cols]
    scavenged_common=scavenged[common_cols]

    frames = [consensus_common, scavenged_common] 
    result = pd.concat(frames)

    with open(args.output_file,'w') as write_tsv:
        write_tsv.write(result.to_csv(sep='\t', index=False))
