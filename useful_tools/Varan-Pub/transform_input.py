
import os 
import pandas as pd
import argparse




def transform_input(tsv,output_folder):
    os.mkdir(output_folder)
    os.mkdir(output_folder+"/temp")
    os.mkdir(os.path.join(output_folder,"temp","SNV"))
    os.mkdir(os.path.join(output_folder,"temp","CNV"))
    os.mkdir(os.path.join(output_folder,"temp","CombinedOutput"))


    os.system("cp "+tsv +" "+os.path.join(output_folder,"temp"))

    tsv_file=pd.read_csv(tsv,sep="\t",dtype="string")

    for _,row in tsv_file.iterrows():
        res_folder="/data/data_storage/novaseq_results"
        snv_path=os.path.join(res_folder,row["RunID"],"Results",row["PatientID"],row["SampleID"],row["SampleID"]+"_MergedSmallVariants.genome.vcf")
        cnv_path=os.path.join(res_folder,row["RunID"],"Results",row["PatientID"],row["SampleID"],row["SampleID"]+"_CopyNumberVariants.vcf")
        combout=os.path.join(res_folder,row["RunID"],"Results",row["PatientID"],row["PatientID"]+"_CombinedVariantOutput.tsv")
    
        if os.path.exists(combout):
            os.system("cp "+combout + " "+os.path.join(output_folder,"temp","CombinedOutput"))
        else:
            print(combout," non trovato")

        if os.path.exists(snv_path):
            os.system("cp "+snv_path + " "+os.path.join(output_folder,"temp","SNV"))
        else:
            print(snv_path," non trovato")

        if os.path.exists(cnv_path):
            os.system("cp "+cnv_path + " "+os.path.join(output_folder,"temp","CNV"))
        else:
            print(cnv_path," non trovato")


if __name__ == '__main__':
         
	# parser variable
	parser = argparse.ArgumentParser(description='transform input')

	# arguments
	parser.add_argument('-i', '--input', required=True,
											help='input tsv')
	parser.add_argument('-o', '--output_folder', required=True,
												help='output_folder')
	
	args = parser.parse_args()

	transform_input(args.input,args.output_folder)
