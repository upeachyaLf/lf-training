#!/usr/bin/env python

import csv
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

def get_avg_percentage(total, subject_count):
    percentage = total / subject_count

    return round(percentage, 2)

def get_formatted_date(date_str):
    date_object = datetime.datetime.strptime(date_str, '%d-%m-%Y')
    
    return datetime.datetime.strftime(date_object, '%B %d, %Y')

def check_file_existance(file_name):
    if not pathlib.Path(file_name).exists():
        raise SystemExit('The store file does not exist.')

def get_records(file_name):
    with open(file_name, 'r', newline='') as result_file:
        result_file_reader = csv.DictReader(result_file)

        return sorted(result_file_reader, key=lambda i: i['name'])

def display_resluts(results):
    for result in results:
        print('***************************')
        print(result['display_str'])
        print(f"Total Percentage: {get_avg_percentage(result['total_percentage'], len(result['subjects']))}")
        print('***************************')

def get_display_string(result, is_initital):
    _str = ""

    if is_initital:
        _str += f"Name: {result['name']}\nDOB: {get_formatted_date(result['dob'])}\n"
    
    _str += f"{result['subject']}:\n\tScore: {result['score']}\n\tTotal: {result['total']}\n\tPercentage: {result['percentage']}\n"

    return _str

if __name__ == "__main__":
    opts = parser.parse_args()
    arg_dict = opts.__dict__

    check_file_existance(arg_dict['store'])

    sorted_result = get_records(arg_dict['store'])
    result_list = []

    for row in sorted_result:
        len_of_list = len(result_list)
        if len_of_list < 1 or row['name'] != result_list[len_of_list - 1]['name']:
            result_list.append({
                "name": row['name'],
                "dob": row['dob'],
                "subjects": [
                    {
                        "name": row['subject'],
                        "percentage": float(row['percentage'])
                    }
                ],
                "display_str": get_display_string(row, True),
                "total_percentage": float(row['percentage'])
            })
        else:
            subjects_len = len(result_list[len_of_list - 1]['subjects'])
            result_list[len_of_list-1]['subjects'].append({
                "name": row['subject'],
                "percentage": float(row['percentage'])
            })
            result_list[len_of_list - 1]['total_percentage'] += float(row['percentage']) 
            result_list[len_of_list - 1]['display_str'] += get_display_string(row, False)

    display_resluts(result_list)
