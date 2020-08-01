#!/usr/bin/env python

import csv
import pprint
import argparse
import datetime
import pathlib

USAGE_EXAMPLE = "Usage example:\n python3 store_result.py --store store.csv"
STORE_HELP = "File name to retrieve the results. e.g. store.csv"

FIELD_NAMES = ['name', 'dob', 'subject', 'total', 'score', 'percentage']

parser = argparse.ArgumentParser(description=USAGE_EXAMPLE,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--store",
                    help=STORE_HELP,
                    required=True)

if __name__ == "__main__":
    opts = parser.parse_args()
    arg_dict = opts.__dict__

    if not pathlib.Path(arg_dict['store']).exists():
        raise SystemExit('The store file does not exist.')

    result_list = []

    with open(arg_dict['store'], 'r', newline='') as result_file:
        result_file_reader = csv.DictReader(result_file)
        sorted_result = sorted(result_file_reader, key=lambda i: i['name'])
        for row in sorted_result:
            len_of_list = len(result_list)
            if len_of_list < 1 or row['name'] != result_list[len_of_list - 1]['name']:
                result_list.append({
                    "name": row['name'],
                    "dob": row['dob'],
                    "subjects": [
                        {
                            "name": row['subject'],
                            "total": row['total'],
                            "score": row['score'],
                            "percentage": row['percentage']
                        }
                    ]
                })
            else:
                subjects_len = len(result_list[len_of_list - 1]['subjects'])
                result_list[len_of_list-1]['subjects'].append({
                    "name": row['subject'],
                    "total": row['total'],
                    "score": row['score'],
                    "percentage": row['percentage']
                })
        pprint.pprint(result_list)
