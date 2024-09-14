#!/usr/bin/env python3
"""
Script to pull patient IDs from a study on pedcbioportal 
"""

import argparse
from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient
from urllib.parse import urlparse

def main():
    parser = argparse.ArgumentParser(
        description="Pull patient IDs from a study on pedcbioportal"
    )
    parser.add_argument(
        "-u", "--url", action="store", dest="url", help="url to search against", default="https://pedcbioportal.kidsfirstdrc.org/api/v2/api-docs"
    )
    parser.add_argument(
        "-s", "--study", action="store", dest="study", help="Cancer study ID to compare on server"
    )
    parser.add_argument(
        "-t", "--token", action="store", dest="token", help="Token file obtained from Web API"
    )

    args = parser.parse_args()
    with open(args.token, 'r') as token_file:
        token = token_file.read().rstrip().split(': ')[1]

    url_object = urlparse(args.url)

    http_client = RequestsClient()
    http_client.set_api_key(
        '{}'.format(url_object.hostname), 'Bearer {}'.format(token),
        param_name='Authorization', param_in='header'
    )

    cbioportal = SwaggerClient.from_url(args.url,
                                        http_client=http_client,
                                        config={"validate_requests":False,
                                                "validate_responses":False,
                                                "validate_swagger_spec": False}
    )
    
    pt_list = cbioportal.Patients.getAllPatientsInStudyUsingGET(studyId=args.study).result()
    print("\n".join([x.patientId for x in pt_list]))

if __name__ == '__main__':
    main()