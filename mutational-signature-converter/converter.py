import csv
import pandas as pd
import sys

# read data from  command line
input_file = sys.argv[1]
output_file = sys.argv[2]

# read data from data file
df = pd.read_csv(input_file, sep='\t')

# delete columns (impact_version, Nmut_Mb, signatureInterpretation) 
if 'impact_version' in df:
    del df['impact_version']
if 'Nmut_Mb' in df:
    del df['Nmut_Mb']
if 'signatureInterpretation' in df:
    del df['signatureInterpretation']

# transpose the data
df = df.transpose()

# change first column name to ENTITY_STABLE_ID
df = df.rename({"Tumor_Sample_Barcode": "ENTITY_STABLE_ID"}, axis='index')

# add name, description and statement columns
mutatinoalSignatureDictionaryV2 = {
    "1": "Signature 1, the aging signature, is detected in this case.",
    "2": "Signature 2, the APOBEC signature, is detected in this case.  This signature often coccurs with signature 13, the other APOBEC signature",
    "3": "Signature 3, the signature of Homologous Recombination Repair deficiency is detected in this case.  This signature is most commonly associated with BRCA mutations",
    "4": "Signature 4, the smoking signature is detected in this case",
    "5": "Signature 5 is detected in this case.  We are not confident that we are able to detect signature 5 in the IMPACT cohort.  It is a 'flat' signature--when it is detected it is more likely to be an artefact. In the literature it is associated with age",
    "6": "Signature 6, a MMR signature, is detected in this case.  It is usually associated with high mutational burden.  This signature often co-occurs with other MMR signatures (14, 15, 20, 21 26)",
    "7": "Signature 7, the UV light signature, is detected in this case.",
    "8": "Signature 8 is detected in this case. We are not confident that we are able to detect signature 8 in the IMPACT cohort. It is a 'flat' signature--when it is detected it is more likely to be an artefact. In the literature it is associated with HRD defects",
    "9": "Signature 9 is detected in this case.  We are not confident that we are able to detect signature 9 in the IMPACT cohort.  In the literature it is associated with POLH.",
    "10": "Signature 10, the POLE signature, is detected in this case.  It is associated with functions to the exonucleus domain of the POLE gene and enormous mutational burden.  Oftentimes MMR signatures 6, 14,16, 20,21 and 26 co-occur with the POLE signature.",
    "11": "Signature 11, the Temozolomide (TMZ) signature, is detected in this case.",
    "12": "Signature 12 is detected in this case.  We are not confident that we are able to detect signature 9 in the IMPACT cohort.  In the literature it is found in liver cancer.",
    "13": "Signature 13, the APOBEC signature, is detected in this case.  This signature often coccurs with signature 2, the other APOBEC signature.",
    "14": "Signature 14, the signature of simultaneous MMR and POLE dysfunction is detected in this case.  This signature usually occurs in cases with the POLE signature (signature 10) and other MMR signatures (6, 15, 20, 21 26).",
    "15": "Signature 15, a MMR signature, is detected in this case.  It is usually associated with high mutational burden.",
    "16": "Signature 16 is detected in this case. We are not confident that we are able to detect signature 16 in the IMPACT cohort.  In the literature it is associated with Liver cancer and alcohol consumption.",
    "17": "Signature 17 is detected in this case.  The aetiology of this signature is unknown.  It is predominantly found in gastric cancers.",
    "18": "Signature 18 is detected in this case.  This signature is associated with MUTYH dysfunction and neuroblastoma.",
    "19": "Signature 19 is detected in this case. We are not confident that we are able to detect signature 19 in the IMPACT cohort.",
    "20": "Signature 20 is detected in this case. This signature is associated with MMR and usually occurs in cases with the POLE signature (signature 10) and other MMR signatures (6, 14, 15, 21, 26).",
    "21": "Signature 21 is detected in this case. This signature is associated with MMR and usually co-occurs with other MMR signatures (6, 14, 15, 21, 26).",
    "22": "Signature 22 is detected in this case. We are not confident that we are able to detect signature 22 in the IMPACT cohort. In the literature it is associated with exposure to Aristolochic Acid.",
    "23": "Signature 23 is detected in this case. We are not confident that we are able to detect signature 23 in the IMPACT cohort.",
    "24": "Signature 24 is detected in this case. We are not confident that we are able to detect signature 24 in the IMPACT cohort.  In the literature it is associated with aflatoxin exposure.  In our cohort we believe it is detected by accident in cases with the smoking signature (signature 4).",
    "25": "Signature 25 is detected in this case. We are not confident that we are able to detect signature 25 in the IMPACT cohort.",
    "26": "Signature 26 is detected in this case.  This signature is associated with MMR and usually co-occurs with other MMR signatures (6, 14, 15, 20, 21).",
    "27": "Signature 27 is detected in this case. We are not confident that we are able to detect signature 27 in the IMPACT cohort.",
    "28": "Signature 28 is detected in this case. We are not confident that we are able to detect signature 28 in the IMPACT cohort.  It often co-occurs with signature 28.",
    "29": "Signature 29, the mutational signature of chewing tobacco is detected in this case.",
    "30": "Signature 30 is detected in this case. We are not confident that we are able to detect signature 30 in the IMPACT cohort."
}

mutatinoalSignatureDictionaryV3 = {
    "SBS1": "Signature SBS1 is clock-like in that the number of mutations in most cancers and normal cells correlates with the age of the individual.",
    "SBS2": "SBS2 is usually found in the same samples as SBS13. It has been proposed that activation of AID/APOBEC cytidine deaminases in cancer may be due to previous viral infection, retrotransposon jumping, or tissue inflammation.",
    "SBS3": "SBS3 is strongly associated with germline and somatic BRCA1 and BRCA2 mutations and BRCA1 promoter methylation in breast, pancreatic, and ovarian cancers.",
    "SBS4": "Although tobacco smoking causes multiple cancer types in addition to lung and head and neck, SBS4 has not been detected in many of these. SBS29 is found in cancers associated with tobacco chewing and appears different from SBS4.",
    "SBS5": "SBS5 is clock-like in that the number of mutations in most cancers and normal cells correlates with the age of the individual.",
    "SBS6": "SBS6 is one of seven mutational signatures associated with defective DNA mismatch repair (with microsatellite instability, MSI) and is often found in the same samples as other MSI associated signatures: SBS14, SBS15, SBS20, SBS21, SBS26, and SBS44.",
    "SBS7a": "SBS7a/SBS7b/SBS7c/SBS7d are found in cancers of the skin from sun exposed areas and are thus likely to be due to exposure to ultraviolet light. SBS7a may possibly be the consequence of just one of the two major known UV photoproducts, cyclobutane pyrimidine dimers or 6-4 photoproducts.",
    "SBS7b": "SBS7a/SBS7b/SBS7c/SBS7d are found in cancers of the skin from sun exposed areas and are likely to be due to exposure to ultraviolet light. SBS7b may possibly be the consequence of just one of the two major known UV photoproducts, cyclobutane pyrimidine dimers or 6-4 photoproducts.",
    "SBS7c": "SBS7a/SBS7b/SBS7c/SBS7d are found in cancers of the skin from sun exposed areas and are likely to be due to exposure to ultraviolet light.",
    "SBS7d": "SBS7a/SBS7b/SBS7c/SBS7d are found in cancers of the skin from sun exposed areas and are likely to be due to exposure to ultraviolet light.",
    "SBS8": "Unknown.",
    "SBS9": "Chronic lymphocytic leukaemias that possess immunoglobulin gene hypermutation (IGHV-mutated) have elevated numbers of mutations attributed to SBS9 compared to those that do not have immunoglobulin gene hypermutation.",
    "SBS10a": "SBS10a/SBS10b usually generate large numbers of somatic mutations (>100 mutations per MB) and samples with these signatures have been termed hypermutators.",
    "SBS10b": "Signature SBS10a/SBS10b usually generate large numbers of somatic mutations (>100 mutations per MB) and samples with these signatures have been termed hypermutators.",
    "SBS11": "SBS11 usually generates large numbers of somatic mutations (>10 mutations per MB).",
    "SBS12": "SBS12 usually contributes a small percentage (<20%) of the mutations observed in liver cancer samples.",
    "SBS13": "SBS13 is usually found in the same samples as SBS2. It has been proposed that activation of AID/APOBEC cytidine deaminases in cancer may be due to previous viral infection, retrotransposon jumping, or tissue inflammation.",
    "SBS14": "SBS14 mutations are present in very high numbers in all samples in which it has been observed. SBS14 is one of seven mutational signatures associated with defective DNA mismatch repair (MSI) and is often found in the same samples as other MSI associated signatures: SBS6, SBS15, SBS20, SBS21, SBS26 and SBS44.",
    "SBS15": "SBS15 is one of seven mutational signatures associated with defective DNA mismatch repair (MSI) and is often found in the same samples as other MSI associated signatures: SBS6, SBS14, SBS20, SBS21, SBS26, and SBS44.",
    "SBS16": "In addition to lower levels of nucleotide excision repair on the untranscribed strands of genes, elevated levels of DNA damage on untranscribed strands (compared to the remainder of the genome) may contribute to SBS16. Contamination by SBS16 may still be present in the current version of SBS5.",
    "SBS17a": "Unknown.",
    "SBS17b": "SBS17b has similarities to SBS28 and these two signatures can be mistaken for one another.",
    "SBS18": "Similar in profile to SBS36 which is associated with defective base excision repair due to MUTYH mutations.",
    "SBS19": "Unknown.",
    "SBS20": "SBS20 is one of seven mutational signatures associated with defective DNA mismatch repair (MSI) and is often found in the same samples as other MSI associated signatures: SBS6, SBS14, SBS15, SBS21, SBS26, and SBS44.",
    "SBS21": "SBS21 is one of seven mutational signatures associated with defective DNA mismatch repair (MSI) and is often found in the same samples as other MSI associated signatures: SBS6, SBS14, SBS15, SBS20, SBS26, and SBS44.",
    "SBS22": "Aristolochic acid exposure. Found in cancer samples with known exposures to aristolochic acid and the pattern of mutations exhibited by the signature is consistent with that observed in experimental systems of aristolochic acid exposure.",
    "SBS23": "Unknown.",
    "SBS24": "Aflatoxin exposure. SBS24 has been found in cancer samples with known exposures to aflatoxin and the pattern of mutations exhibited by the signature is consistent with that observed in experimental systems exposed to aflatoxin.",
    "SBS25": "This signature has only been identified in Hodgkin's cell lines. Data is not available from primary Hodgkin lymphomas.",
    "SBS26": "SBS26 is one of seven mutational signatures associated with defective DNA mismatch repair (MSI) and is often found in the same samples as other MSI associated signatures: SBS6, SBS14, SBS15, SBS20, SBS21, and SBS44.",
    "SBS27": "Possible sequencing artefact.",
    "SBS28": "SBS28 has similarities to SBS17b and these two signatures can be mistaken for one another. Signature SBS28 is found in most samples with SBS10a/SBS10b where it contributes very high numbers of mutations. In contrast, SBS28 contributes much smaller number of mutations in samples lacking SBS10a/SBS10b.",
    "SBS29": "The pattern of C>A mutations in SBS29 appears different from the pattern of mutations due to tobacco smoking reflected by SBS4.",
    "SBS30": "SBS30 is due to deficiency in base excision repair due to inactivating mutations in NTHL1.",
    "SBS31": "SBS31 exhibits a pattern of mutations similar to components of SBS35 and both may be due to platinum drug treatment.",
    "SBS32": "Prior treatment with azathioprine to induce immunosuppression.",
    "SBS33": "Unknown.",
    "SBS34": "Unknown.",
    "SBS35": "SBS35 exhibits a pattern of mutations that encompasses SBS31 and both may be due to platinum drug treatment.",
    "SBS36": "Similar to SBS18, which has been proposed to be due to reactive oxygen species induced DNA damage.",
    "SBS37": "Unknown.",
    "SBS38": "Unknown. Found only in ultraviolet light associated melanomas suggesting potential indirect damage from UV-light.",
    "SBS39": "Unknown.",
    "SBS40": "Numbers of mutations attributed to SBS40 are correlated with patients' ages for some types of human cancer.",
    "SBS41": "Unknown",
    "SBS42": "Occupational exposure to haloalkanes.",
    "SBS43": "Unknown. Possible sequencing artefact.",
    "SBS44": "SBS44 is one of seven mutational signatures associated with defective DNA mismatch repair (MSI) and is often found in the same samples as other MSI associated signatures: SBS6, SBS14, SBS15, SBS20, SBS21, and SBS26.",
    "SBS45": "Possible artefact due to 8-oxo-guanine introduced during sequencing.",
    "SBS46": "Signature SBS46 was found commonly in colorectal cancers from early releases of TCGA (data released prior 2013).",
    "SBS47": "SBS47 was found in cancer samples that were subsequently blacklisted for poor quality of sequencing data.",
    "SBS48": "SBS48 was found in cancer samples that were subsequently blacklisted for poor quality of sequencing data.",
    "SBS49": "Possible sequencing artefact.",
    "SBS50": "SBS50 was found in cancer samples that were subsequently blacklisted for poor quality of sequencing data.",
    "SBS51": "Possible sequencing artefact.",
    "SBS52": "Possible sequencing artefact.",
    "SBS53": "Signature SBS53 was found in cancer samples that were subsequently blacklisted for poor quality of sequencing data.",
    "SBS54": "Possible sequencing artefact. Possible contamination with germline variants.",
    "SBS55": "Possible sequencing artefact.",
    "SBS56": "Possible sequencing artefact.",
    "SBS57": "Possible sequencing artefact.",
    "SBS58": "Potential sequencing artefact.",
    "SBS59": "Possible sequencing artefact.",
    "SBS60": "Possible sequencing artefact.",
}

displayNameDictionary = {
    "mean": "contribution",
    "confidence": "confidence"
}

def rowFuncForNameColumn(row):
    if row.name == "ENTITY_STABLE_ID":
        return "NAME"
    if row.name == "Nmut":
        return "Number of mutations"
    return row.name.split('_')[1]

def rowFuncForDescriptionColumn(row):
    if row.name == "ENTITY_STABLE_ID":
        return "DESCRIPTION"
    if row.name == "Nmut":
        return "Number of mutations"
    return displayNameDictionary[row.name.split('_')[0]] + " data for mutational signature " + row.name.split('_')[1]

def rowFuncForUrlColumn(row):
    if row.name == "ENTITY_STABLE_ID":
        return "URL"
    if row.name == "Nmut":
        return "NA"
    return "https://cancer.sanger.ac.uk/cosmic/signatures/SBS/" + row.name.split('_')[1] + ".tt"

def rowFuncForConfidenceStatementColumn(row):
    if row.name == "ENTITY_STABLE_ID":
        return "CONFIDENCE_STATEMENT"
    if row.name == "Nmut":
        return "NA"
    return mutatinoalSignatureDictionaryV3[row.name.split('_')[1]]

df['NAME'] = df.apply(rowFuncForNameColumn, axis = 1)
df['DESCRIPTION'] = df.apply(rowFuncForDescriptionColumn, axis = 1)
df['URL'] = df.apply(rowFuncForUrlColumn, axis = 1)
df['CONFIDENCE_STATEMENT'] = df.apply(rowFuncForConfidenceStatementColumn, axis = 1)

# get a list of columns
cols = list(df)

# move the column to head of list using index, pop and insert
cols.insert(0, cols.pop(cols.index('NAME')))
cols.insert(1, cols.pop(cols.index('DESCRIPTION')))
cols.insert(2, cols.pop(cols.index('URL')))
cols.insert(3, cols.pop(cols.index('CONFIDENCE_STATEMENT')))

# reorder
df = df.loc[:, cols]

# write the output file
out = df.to_csv(output_file, sep='\t', header=False)
