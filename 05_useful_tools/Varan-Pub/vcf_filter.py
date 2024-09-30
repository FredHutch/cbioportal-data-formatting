#funzione per filtrare le colonne ALT e FILTER di un file vcf e creare un nuovo
#vcf filtrato

import argparse
import pandas as pd

def parsing_vcf(file_input,file_output):
    
    #lista contenente i dati da #CHROM in poi (no meta-information)
    with open (file_input) as f:
        correct_data=[line.strip().split("\t") for line in f if not line.startswith("##")]

    #creazione dataframe contenente i dati
    data=pd.DataFrame(correct_data[1:],columns=correct_data[0])
    
    #filtro per dati in cui ALT!="."
    data=data[data["ALT"]!="."]

    #filtro per dati in cui FILTER == "PASS"
    data=data[data["FILTER"]=="PASS"]
    # print(type(data))
    #per salvare il file così filtrato
    data.to_csv(file_output,sep="\t", mode="a", index=False)


def write_header_lines(input_vcf, output_vcf):
    with open(input_vcf, 'r') as f_in, open(output_vcf, 'w') as f_out:
        for line in f_in:
            if line.startswith("##"):
                f_out.write(line)



def main(INPUT, OUTPUT):
    write_header_lines(INPUT,OUTPUT)
    parsing_vcf(INPUT,OUTPUT)

