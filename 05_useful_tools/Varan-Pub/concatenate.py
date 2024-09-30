import os
import argparse
from loguru import logger
import sys


def concatenate_files(file_list, output_file):
    with open(output_file, 'w') as out_file:
        for i, file_name in enumerate(file_list):
            with open(file_name) as in_file:
                lines = in_file.readlines()
                if i > 0:
                    lines = lines[1:]
                out_file.write("".join(lines))
                
    if not os.path.exists(output_file):
        logger.critical(f"Something went wrong while writing {output_file}.")
    
    logger.info(f"#{len(file_list)} maf file(s) concatenated")
    
def get_files_by_ext(folder, ext):
    file_list = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(ext):
                file_list.append(os.path.join(root, file))
    if len(file_list)==0:
        logger.warning(f"No files found with .{ext} extension in {folder}")
    else:
        logger.info(f"#{len(file_list)} {ext} file(s) found: {file_list}")
    return file_list



def concatenate_main(folder, ext, output_file):
        
    logger.info("Starting concatenate_main script:")
    logger.info(f"concatenate_main args [folder:{folder}, extension:{ext}, output_file:{output_file}]") 
    
    if os.path.isdir(output_file):
        logger.critical(f"It seems that the inserted output_file '{output_file}' is not a file, but a folder! Check your '-o/--output_file' field")
        exit()
    if not output_file.endswith('txt'):
        logger.critical(f"It seems that the inserted output_file '{output_file}' has the wrong extension! Output file must be have a .txt extension.")
        exit()
        
    file_list = get_files_by_ext(folder, ext)

    concatenate_files(file_list, output_file)
    
    logger.success("Concatenate script completed!\n")
