#!/bin/bash

PROJECT_PATH="/home/zhaog/signature.significance/"
PYTHON_PATH="/data/tools/anaconda2/envs/mutational_signature/bin/"
DATA_PATH="/home/zhaog/data/"
FASTA_FILE_PATH="/data/zhaog/"
R_LIBRARY="/data/tools/anaconda2/envs/mutational_signature/lib/R/library"
CONVERTER_PATH="/home/zhaog/mutational-signature-converter/"

# initialize conda
# reference: https://github.com/conda/conda/issues/7980#issuecomment-492784093
eval "$(conda shell.bash hook)"

# active environment
conda activate mutational_signature

# get spectrum file
${PYTHON_PATH}python ${PROJECT_PATH}make_spectrum.py ${DATA_PATH}data_mutations_extended.txt ${PROJECT_PATH}msk_impact.tmp ${FASTA_FILE_PATH}hg19.fa

# get output file
Rscript ${PROJECT_PATH}signature.significance.R -i ${PROJECT_PATH}msk_impact.spectrum.txt --signature_file ${PROJECT_PATH}sigProfiler_exome_SBS_signatures.txt -o ${PROJECT_PATH}msk_impact.out -m ${PROJECT_PATH}signature.significance.stan -l ${R_LIBRARY}

# get tabular file
Rscript ${PROJECT_PATH}summ_to_tab.R ${PROJECT_PATH}msk_impact.spectrum.txt ${PROJECT_PATH}msk_impact.out ${PROJECT_PATH}msk_impact_tab.out

# convert file
${PYTHON_PATH}python ${CONVERTER_PATH}converter.py ${PROJECT_PATH}msk_impact_tab.out ${PROJECT_PATH}msk_impact_data.txt

echo data file generated at: ${PROJECT_PATH}msk_impact_data.txt
