import os 
import sys
import argparse
from loguru import logger 

@logger.catch()
def varan(args):
    logger.info(f"Varan args [input:{args.input}, output_folder:{args.output_folder}, filter_snv:{args.filter_snv}, cancer:{args.Cancer}, \
                            vcf_type:{args.vcf_type},  vus:{args.filterVus}], \
                            update:{args.Update}, extract:{args.Extract}, remove:{args.Remove}")
    #overwrite_output:{args.overWrite},
    if not any([args.Update ,args.Extract , args.Remove]) :       
             
            ###########################
            #        1.  WALK         #
            ###########################
            from walk import walk_folder
            logger.info("Starting preparation study folder")
            if not os.path.exists("./scratch"):
                logger.info("Creating scratch dir")
                os.mkdir("./scratch")
            output_folder=walk_folder(args.input, args.output_folder,  args.vcf_type,args.filter_snv)
            #args.overWrite,
            ###########################
            #       2. FILTER         #
            ###########################
            from filter_clinvar import filter_main
            logger.info("Starting filter") 
            if args.vcf_type =="snv" or (args.vcf_type==None and os.path.exists(os.path.join(args.input,"SNV"))):
                filter_main(output_folder, output_folder, args.filterVus) #args.overWrite

            ############################
            #      3. CONCATENATE      #
            ############################
            from concatenate import concatenate_main
            if args.vcf_type =="snv" or (args.vcf_type==None and os.path.exists(os.path.join(args.input,"SNV"))):
                logger.info("Concatenate mutation file")
                folders=["NoBenign"]
                if args.filterVus:
                    folders.append("NoVus")
                
                for folder in folders:
                    input_folder=os.path.join(output_folder,folder)
                    output_file=os.path.join(input_folder,"data_mutations_extended.txt")
                    concatenate_main(input_folder,"maf",output_file)
            
                if args.filterVus:
                    logger.info("Extracting data_mutations_extended from NoVUS folder") 
                    os.system("cp "+os.path.join(output_folder,os.path.join("NoVus","data_mutations_extended.txt"))+" "+ output_folder )
                else:
                    logger.info("Extracting data_mutations_extended from NoBenign folder") 
                    os.system("cp "+os.path.join(output_folder,os.path.join("NoBenign","data_mutations_extended.txt"))+" "+ output_folder )
                
                
            ###########################################
            #      4. MAKE AND POPULATE TABLES        #
            ###########################################
            from Make_meta_and_cases import meta_case_main
            logger.info("It's time to create tables!")
            meta_case_main(args.Cancer,args.filterVus,output_folder)

            
            ############################
            #      5. VALIDATION       #
            ############################
            from ValidateFolder import validateFolderlog
            logger.info("Starting Validation Folder")
            validateFolderlog(output_folder)
            logger.success("The end! The study is ready to be uploaded on cBioportal")
        
    ############################
    #         UPDATE           #
    ############################

    elif args.Update: 
        from Update_script import update_main 
        logger.info("Starting Update study")
        update_main(args.Path,args.NewPath,args.output_folder)

    ############################
    #         DELETE           #
    ############################

    elif args.Remove:
        from Delete_script import delete_main 
        logger.info("Starting Delete samples from study")  
        delete_main(args.Path,args.SampleList,args.output_folder) #args.overWrite

    ############################
    #         EXTRACT          #
    ############################

    elif args.Extract:
        from ExtractSamples_script import extract_main
        logger.info("Starting Extract samples from study")
        extract_main(args.Path,args.SampleList,args.output_folder) #args.overWrite

#################################################################################################################

class MyArgumentParser(argparse.ArgumentParser):
  """An argument parser that raises an error, instead of quits"""
  def error(self, message):
    raise ValueError(message)


@logger.catch()
def main(): 
    logger.remove()
    logfile="Varan_{time:YYYY-MM-DD_HH-mm-ss.SS}.log"
    logger.level("INFO", color="<green>")
    logger.add(sys.stderr, format="{time:YYYY-MM-DD_HH-mm-ss.SS} | <lvl>{level} </lvl>| {message}",colorize=True, catch=True, backtrace=True, diagnose=True)
    logger.add(os.path.join('Logs',logfile),format="{time:YYYY-MM-DD_HH-mm-ss.SS} | <lvl>{level} </lvl>| {message}",mode="w", backtrace=True, diagnose=True)
    logger.info("Welcome to VARAN")

    parser = MyArgumentParser(add_help=True, exit_on_error=True, usage=None, description='Argument of Varan script')
    

    # WALK BLOCK
    parser.add_argument('-c', '--Cancer', required=False,help='Cancer Name')
    parser.add_argument('-i', '--input', required=False, help='input folder tsv with data or tsv with path of data')
    parser.add_argument('-f', '--filter_snv', required=False,action='store_true',help='Filter out from the vcf the variants wit dot (.) in Alt column')
    parser.add_argument('-t', '--vcf_type', required=False, choices=['snv', 'cnv'],help='Select the vcf file to parse')
   
    # FILTER_CLINVAR BLOCK
    parser.add_argument('-v', '--filterVus', required=False,action='store_true', help='Filter out VUS variants')
    # UPDATE BLOCK
    parser.add_argument('-u', '--Update', required=False,action='store_true',help='Add this argument if you want to concatenate two studies')
    parser.add_argument('-n', '--NewPath', required=False,help='Path of new study folder to add')  
    # DELETE BLOCK
    parser.add_argument('-r', '--Remove', required=False,action='store_true',help='Add this argument if you want to remove samples from a study')
    # EXTRACT BLOCK
    parser.add_argument('-e', '--Extract', required=False,action='store_true', help='Add this argument if you want to extract samples from a study')
    
    # COMMON BLOCK 
    parser.add_argument('-o', '--output_folder', required=True,help='Output folder')
    parser.add_argument('-s', '--SampleList', required=False,help='Path of file with list of SampleIDs')
    parser.add_argument('-p', '--Path', required=False,help='Path of original study folder')
    
   # args = parser.parse_args()
    try:
        args = parser.parse_args()  
    except ValueError :
        logger.critical("Error Argument: Output is required")
        exit(1)



    if args.Update and not all([args.Path,args.NewPath]):
        logger.critical("To update a study, you need to specify both original and new folder paths")
        exit(1)
        
    if args.Extract and not all([args.Path,args.SampleList]):
        logger.critical("To extract samples from a study, you need to specify both original folder path and list samples")
        exit()
    
    if args.Remove and not all([args.Path,args.SampleList]):
        logger.critical("To remove samples from a study, you need to specify both original folder path and list samples")
        exit()
    
    if not any([args.Update ,args.Extract , args.Remove]) and args.Cancer==None:
            logger.critical("Error Argument: Cancer name is required")
            exit()  
    if not any([args.Update ,args.Extract , args.Remove]) and args.input==None:
            logger.critical("Error Argument: Input is required")
            exit()

    varan(args)

if __name__ == '__main__':
    main()