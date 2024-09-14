#!/usr/bin/env python3

import sys
from requests import request
import argparse
import concurrent.futures
import json
from time import sleep
import pdb


def mt_query_calls(line):
    """
    This function collates information obtained from GET requests to the data service for tumor and normal samples
    """
    try:
        info = line.rstrip('\n').split('\t')
        (tum_bs_id, norm_bs_id) = (info[0], info[1])
        norm_str = ''
        if norm_bs_id != 'NA' and norm_bs_id not in norm_seen:
            bs_info = query_dataservice_bs_id(url, norm_bs_id, bs_attrs, pt_attrs, dx_attrs, outcome_attrs)
            norm_str = norm_bs_id + '\t' + '\t'.join(bs_info) + '\n'
            norm_seen[norm_bs_id] = 1
        bs_info = query_dataservice_bs_id(url, tum_bs_id, bs_attrs, pt_attrs, dx_attrs, outcome_attrs)
        tum_str = tum_bs_id + '\t' + '\t'.join(bs_info) + '\n'
        return tum_str, norm_str
    except Exception as e:
        sys.stderr.write('Error ' + str(e) + ' occurred while trying to process ' + line)
        exit(1)


def get_obj(src_url):
    """
    GET requested object from url. It will occassionally fail so pausing, and trying again remedies the situation
    """
    try:
        req_info = request('GET', src_url)
        return req_info
    except Exception as e:
        sys.stderr.write('Got error ' + str(e) + ',could not retrieve info from ' + src_url + ', pausing and retrying\n')
        sys.stderr.flush()
        sleep(1)
        req_info = request('GET', src_url)
        return req_info


def process_attr_dict(attr_dict, info_dict):
    """
    Iterate through a requested attribute dictionary and append to an output string (a list that wil be converted to tsv)
    """
    temp = []
    for attr in attr_dict:
        res = info_dict.json()['results'][attr]
        if res is None:
            res = 'NULL'
        temp.append(res)
    return temp


def query_dataservice_bs_id(url, bs_id, bs_attrs, pt_attrs, dx_attrs, outcome_attrs):
    """
    This function queries various data service endpoints in order to populate patient and sample metadata
    """
    bs_url = url + '/biospecimens/' + bs_id
    bs_info = get_obj(bs_url)

    result = []
    if bs_info.json()['_status']['code'] == 404:
        result.append(bs_info.json()['_status']['message'])
        sys.stderr.write(bs_id + ' not found!\n')
        sys.stderr.flush()
        return result
    # elif not bs_info.json()['results']['visible']:
    #     sys.stderr.write(bs_id + ' was set to hide.  skipping!\n')
    #     sys.stderr.flush()
    #     return result
    dx_url = url + bs_info.json()['_links']['diagnoses']
    # dx can sometimes have multiple values, so dict is used to store them all
    dx_dict = {}
    dx_obj = get_obj(dx_url) if len(dx_attrs) > 0 else 'NoDX'

    pt_url = url + bs_info.json()['_links']['participant']
    pt_info = get_obj(pt_url)
    result.append(pt_info.json()['results']['kf_id'])

    outcome_url = url + pt_info.json()['_links']['outcomes']
    outcome_info = get_obj(outcome_url)
    
    result.extend(process_attr_dict(bs_attrs, bs_info))
    result.extend(process_attr_dict(pt_attrs, pt_info))

    for attr in dx_attrs:
        dx_dict[attr] = []
        for cur_res in dx_obj.json()['results']:
            dx_dict[attr].append(str(cur_res[attr]))
        result.append(';'.join(dx_dict[attr]))
    # default to last outcome in list
    try:
        if len(outcome_info.json()['results']):
            for attr in outcome_attrs:
                res = outcome_info.json()['results'][-1][attr]
                if res is None:
                    res = 'NULL'
                result.append(str(res))
        else:
            for attr in outcome_attrs:
                res = 'NULL'
                result.append(str(res))
                sys.stderr.write("WARN: " + pt_info.json()['results']['kf_id'] + " has no outcome data\n")
    except Exception as e:
        sys.stderr.write(str(e) + "\n")
    return result


parser = argparse.ArgumentParser(description='Script to walk through data service and grab all relevant metadata'
                                             ' by bs id.')
parser.add_argument('-u', '--kf-url', action='store', dest='url',
                    help='Kids First data service url', default='https://kf-api-dataservice.kidsfirstdrc.org/')
parser.add_argument('-c', '--cavatica', action='store', dest='cav',
                    help='file with task info from cavatica (see step 1)')
parser.add_argument('-j', '--config', action='store', dest='config_file', help='json config file with data types and '
                                                                               'data locations')

args = parser.parse_args()
with open(args.config_file) as f:
    config_data = json.load(f)
file_list = args.cav
bs_attrs = ['external_aliquot_id', 'analyte_type', 'source_text_tissue_type', 'source_text_tumor_descriptor',
            'composition', 'external_sample_id']
pt_attrs = ['external_id', 'gender', 'ethnicity', 'race']
outcome_attrs = ['age_at_event_days', 'vital_status']
dx_attrs = ['source_text_diagnosis', 'source_text_tumor_location', 'age_at_event_days']
url = args.url

norm_out_fh = open('norm_bs_ds_info.txt', 'w')
tum_out_fh = open('tum_bs_ds_info.txt', 'w')
norm_out_fh.write('BS_ID\tPT_ID\t' + '\t'.join(bs_attrs) + '\t' + '\t'.join(pt_attrs))
tum_out_fh.write('BS_ID\tPT_ID\t' + '\t'.join(bs_attrs) + '\t' + '\t'.join(pt_attrs))
if len(dx_attrs) > 0:
    norm_out_fh.write('\t' + '\t'.join(dx_attrs))
    tum_out_fh.write('\t' + '\t'.join(dx_attrs))
# tack on outcome data, renaming the age field
norm_out_fh.write('\toutcome_age_at_event_days\tvital_status\n')
tum_out_fh.write('\toutcome_age_at_event_days\tvital_status\n')


x = 1
m = 100
task_fh = open(file_list)
head = next(task_fh)
norm_seen = {}
with concurrent.futures.ThreadPoolExecutor(config_data['threads']) as executor:
    results = {executor.submit(mt_query_calls, entry): entry for entry in task_fh}
    for result in concurrent.futures.as_completed(results):
        if x % m == 0:
            sys.stderr.write('Processed ' + str(x) + ' lines\n')
            sys.stderr.flush()
        (tum_info, norm_info) = result.result()
        tum_out_fh.write(tum_info)
        if norm_info != '':
            norm_out_fh.write(norm_info)
        x += 1

# debug mode
# for entry in task_fh:
#     mt_query_calls(entry)

norm_out_fh.close()
tum_out_fh.close()
sys.stderr.write('Done!')
