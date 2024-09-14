# Compare current versus build
This documentation addresses a [QC script](../scripts/diff_studies.py) for clinical metadata. It streamlines the process of identifying and summarizing changes slated to be made.

```sh
python3 scripts/diff_studies.py --help
usage: diff_studies.py [-h] [-u URL] [-s STUDY] [-t TOKEN] [-d DATA_DIR]

Compare local clinical data to server

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     url to search against
  -s STUDY, --study STUDY
                        Cancer study ID to compare on server
  -t TOKEN, --token TOKEN
                        Token file obtained from Web API
  -d DATA_DIR, --datasheet-dir DATA_DIR
                        Directory containing data_clinical_*.txt
```

## INPUTS:
 - `-u, --url`: cBioportal api deployment site. Default: https://pedcbioportal.kidsfirstdrc.org/api/v2/api-docs
 - `-s, --study`: cBioportal cancer study ID, i.e. `pbta_all`
 - `-t, --token`: File obtained from navigating to https://pedcbioportal.kidsfirstdrc.org/webAPI#using-data-access-tokens, then clicking on `Download Token`. File is reusable
 - `-d, --datasheet-dir`: Name of directory containing `data_clinical_patient.txt` and `data_clinical_sample.txt` being vetted for upload

## OUTPUTS:
Essentially two change log files, `patient_portal_v_build.txt` and `sample_portal_v_build.txt`.
For the patient and sample views, each file respectively has:
 - A list, one per line, per ID, per attribute, of what would change if the data were loaded
 - A list of IDs that would be removed from the portal, if any
 - A list of IDs that would be added if any
 - A summary of the number of changes of each attribute type printed to STDOUT

### patient_portal_v_build.txt example:
```
Patient attribute       before  after
PT_017WC8PS     ETHNICITY       NA      Not Available
PT_01HNFSBZ     CANCER_PREDISPOSITIONS  None documented NA
PT_01HNFSBZ     ETHNICITY       NA      Not Available
PT_01HNFSBZ     GERMLINE_SEX_ESTIMATE   Unknown NA
PT_01SH4F1X     AGE_IN_DAYS     3838    NA
PT_01SH4F1X     OS_MONTHS       45      54
PT_0324HWD5     AGE_IN_DAYS     3121    NA
PT_047YGDRW     ETHNICITY       NA      Not Available
PT_04V47WFC     AGE_IN_DAYS     5717    NA
PT_08M919BH     OS_MONTHS       44      62
PT_08M919BH     EFS_MONTHS      44      62
PT_0BSG3R3N     AGE_IN_DAYS     3431    NA
PT_0BVR16FK     ETHNICITY       NA      Not Available
PT_0CE0HFYB     GERMLINE_SEX_ESTIMATE   Male    NA
PT_0CVRX4SJ     OS_MONTHS       NA      149
```

### sample_portal_v_build.txt example:
```
Sample  attribute       before  after
16510-1 TUMOR_FRACTION  0.349951221921  0.34995122192100003
16510-15        TUMOR_FRACTION  0.892871847605  0.8928718476049999
16510-2 TUMOR_FRACTION  0.242536563786  0.24253656378600005
16510-8 TUMOR_FRACTION  0.557284218924  0.5572842189239999
7316-100        TUMOR_FRACTION  0.270649989118  0.27064998911800003
7316-1017       TUMOR_FRACTION  0.570184695999  0.559801637737
7316-104        TUMOR_FRACTION  0.664343255194  0.6643432551940001
7316-1045       TUMOR_FRACTION  0.477859261757  0.496989582389
7316-105        CNS_REGION      NA      Mixed
7316-105        CANCER_TYPE_DETAILED    NA      Low-grade glioma, BRAF V600E
7316-105        MOLECULAR_SUBTYPE       NA      LGG, BRAF V600E
7316-105        BROAD_HISTOLOGY NA      Low-grade astrocytic tumor
7316-105        CANCER_GROUP    NA      Low-grade glioma
7316-105        TUMOR_PLOIDY    NA      2
7316-105        PATHOLOGY_FREE_TEXT_DIAGNOSIS   NA      pilocytic astrocytoma ii
7316-105        TUMOR_FRACTION  NA      0.823344460708
7316-1052       CANCER_TYPE_DETAILED    Diffuse midline glioma, H3 K28-mutant   Diffuse midline glioma, H3 K28-altered
7316-1052       MOLECULAR_SUBTYPE       DMG, H3 K28     DMG, H3 K28, TP53
7316-1062       CANCER_TYPE_DETAILED    Diffuse midline glioma, H3 K28-mutant   Diffuse midline glioma, H3 K28-altered
7316-1068       CANCER_TYPE_DETAILED    Diffuse midline glioma, H3 K28-mutant   Diffuse midline glioma, H3 K28-altered
7316-1072       CANCER_TYPE_DETAILED    Glial-neuronal tumor NOS        Glial-neuronal tumor,  To be classified
7316-1072       BROAD_HISTOLOGY Low-grade astrocytic tumor      Neuronal and mixed neuronal-glial tumor
7316-1072       CANCER_GROUP    Glial-neuronal tumor    Glial-neuronal tumor NOS
```

### STDOUT:
```
Sample CHANGE SUMMARY:
27 Samples in build would be added to the portal: 1235928,1235929,1235930,1235931,1235932,1235933,1235934,1235935,1235936,1235937,1235938,1235939,1235940,1235941,1235981,1240110,1240112,1240114,1240116,1242273,1242274,1242276,1250775,1250776,1250777,1250778,1273223
TUMOR_FRACTION has 1005 change(s)
CNS_REGION has 410 change(s)
CANCER_TYPE_DETAILED has 847 change(s)
MOLECULAR_SUBTYPE has 488 change(s)
BROAD_HISTOLOGY has 390 change(s)
CANCER_GROUP has 517 change(s)
TUMOR_PLOIDY has 403 change(s)
PATHOLOGY_FREE_TEXT_DIAGNOSIS has 507 change(s)
ONCOTREE_CODE has 7 change(s)
CANCER_TYPE has 8 change(s)
TUMOR_TYPE has 8 change(s)
TUMOR_TISSUE_TYPE has 17 change(s)
EXPERIMENT_STRATEGY has 1 change(s)
SPECIMEN_ID has 1 change(s)
CBTN_TUMOR_TYPE has 6 change(s)
SAMPLE_TYPE has 2 change(s)

Patient CHANGE SUMMARY:
ETHNICITY has 358 change(s)
CANCER_PREDISPOSITIONS has 29 change(s)
GERMLINE_SEX_ESTIMATE has 220 change(s)
AGE_IN_DAYS has 147 change(s)
OS_MONTHS has 99 change(s)
EFS_MONTHS has 60 change(s)
EFS_STATUS has 18 change(s)
SEX has 9 change(s)
AGE has 6 change(s)
OS_STATUS has 4 change(s)
```