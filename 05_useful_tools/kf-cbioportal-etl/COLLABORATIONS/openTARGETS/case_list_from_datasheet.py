import sys
import argparse
import pandas as pd
import pdb

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate extra cases lists based on cBio datasheet')
    parser.add_argument('-d', '--datasheet', action='store', dest='datasheet',
                    help='cBio sample datasheet')
    parser.add_argument('-s', '--study-id', action='store', dest='study_id',
                    help='cBio cancer_study_identifier')
    parser.add_argument('-c', '--cohort-csv', action='store', dest='cohorts',
                    help='add a special case for a cohort-specific case list using a csv list')
    parser.add_argument('-m', '--min-sample', action='store', dest='samp_min',
                    help='min number of samples a cohort must have to generate a case list for. recommend 3', type=int)
    
    args = parser.parse_args()
    # skip first 4 header rows
    cbio_ds = pd.read_csv(args.datasheet, sep="\t", skiprows=4)
    
    # skip cohorts for hist split given in arg c
    skip_cohort_list = []
    if args.cohorts:
        skip_cohort_list = args.cohorts.split(',')
    process_cohorts_df = cbio_ds[~cbio_ds['COHORT'].isin(skip_cohort_list)]
    skip_cohorts_df = cbio_ds[cbio_ds['COHORT'].isin(skip_cohort_list)]
    hist_list = process_cohorts_df.HISTOLOGY.unique()
    cohort_list = process_cohorts_df.COHORT.unique()

    # iterate through histologies with at least 5 samples
    for hist in hist_list:
        samp_ids = cbio_ds[cbio_ds['HISTOLOGY'].isin([hist])].SAMPLE_ID.to_list()
        if len(samp_ids) >= args.samp_min:
            # print(hist)
            try:
                suffix = hist.lower().replace(" ", "_").replace("/", "_")
                cur = open("cases_" + suffix + ".txt", "w")
                cur.write("cancer_study_identifier: " + args.study_id + "\n" 
                + "stable_id: " + args.study_id + "_" + suffix + "\n" 
                + "case_list_name: " + hist + " samples\n" 
                + "case_list_description:  " + hist + " samples (" + str(len(samp_ids)) + ")\n"
                + "case_list_category: other\ncase_list_ids: " + "\t".join(samp_ids) + "\n")
                cur.close()
                # Also collapse on the cohort level
                for cohort in cohort_list:
                    subset = process_cohorts_df.loc[process_cohorts_df['COHORT'] == cohort,]
                    subset_samp = subset[subset['HISTOLOGY'].isin([hist])].SAMPLE_ID.to_list()
                    if len(subset_samp) >= args.samp_min:
                        cohort_stable = cohort.lower().replace(" ", "_").replace("/", "_")
                        cur = open("cases_" + cohort_stable + "_" + suffix + ".txt", "w")
                        cur.write("cancer_study_identifier: " + args.study_id + "\n" 
                        + "stable_id: " + args.study_id + "_" + cohort_stable +  "_" + suffix + "\n" 
                        + "case_list_name: " + cohort + " " + hist + " samples\n" 
                        + "case_list_description:  " + cohort + " " + hist + " samples (" + str(len(subset_samp)) + ")\n"
                        + "case_list_category: other\ncase_list_ids: " + "\t".join(subset_samp) + "\n")
                        cur.close()
                    else:
                        sys.stderr.write("Skipping " + hist + " for cohort " + cohort + ", less than " + str(args.samp_min) + " entries\n")

            except Exception as e:
                print(e)
                sys.stderr.write("Error encountered - likely a blank histology, skipping\n")
        else:
            sys.stderr.write("Skipping " + hist + " less than " + str(args.samp_min) + " entries\n")
    if args.cohorts:
        for cohort in skip_cohort_list:
            subset = skip_cohorts_df.loc[skip_cohorts_df['COHORT'] == cohort,]
            subset_samp = subset.SAMPLE_ID.to_list()
            cohort_stable = cohort.lower().replace(" ", "_").replace("/", "_")
            cur = open("cases_" + cohort_stable + ".txt", "w")
            cur.write("cancer_study_identifier: " + args.study_id + "\n" 
            + "stable_id: " + args.study_id + "_" + cohort_stable + "\n" 
            + "case_list_name: " + cohort + " samples\n" 
            + "case_list_description:  " + cohort + " samples (" + str(len(subset_samp)) + ")\n"
            + "case_list_category: other\ncase_list_ids: " + "\t".join(subset_samp) + "\n")
            cur.close()


    #pdb.set_trace()
    #hold=1