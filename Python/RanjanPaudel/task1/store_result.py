#!/usr/bin/env python

import csv
import argparse
import datetime
import pathlib

from text_constants import (
    STORE_RESULT_USAGE_EXAMPLE, 
    STORE_RESULT_NAME_HELP, 
    STORE_RESULT_DOB_HELP, 
    STORE_RESULT_SUBJECT_HELP, 
    STORE_RESULT_TOTAL_HELP, 
    STORE_RESULT_SCORE_HELP, 
    STORE_RESULT_STORE_HELP
)

FIELD_NAMES = ['name', 'dob', 'subject', 'total', 'score', 'percentage']
SUBJECT_CHOICES = ['Nepali', 'English', 'Math', 'Science', 'Social']

def validate_date(date_string):
    try:
        return f"{datetime.datetime.strptime(date_string, '%d-%m-%Y')}".split(' ')[0]
    except (ValueError):
        raise SystemExit('Invalid date format. Should be DD-MM-YYYY.')

def validate_score(result):
    if result['score'] > result['total'] or result['score'] < 0 or result['score'] == -0.0:
        raise SystemExit(
            'Score not in valid range. \npython3 store_result.py --help, for detail.')
    
def validate_file_type(file_name):
    if file_name.find('.csv') == -1:
        raise SystemExit('File extension should be .csv')

def create_new_file(file_name):
    with open(file_name, 'w', newline='') as new_file:
        new_file_writer = csv.writer(new_file, delimiter=',')
        new_file_writer.writerow(FIELD_NAMES)
    print(f"New file {file_name}, created.")

def check_for_duplicate_record(file_name, result):
    with open(file_name, 'r', newline='') as result_file:
        result_file_reader = csv.DictReader(result_file)
        for row in result_file_reader:
            if row['name'] == result['name'] and row['dob'] == result['dob'] and row['subject'] == result['subject']:
                raise SystemExit('Result already exists.')

def write_new_record(file_name, result):
    with open(file_name, 'a', newline='') as result_file:
        result_file_writer = csv.DictWriter(
            result_file, fieldnames=FIELD_NAMES)
        result_file_writer.writerow(result)
    print(f"New record added:\n{result}")

def get_percentage(result):
    percentage = (result['score'] / result['total']) * 100
    
    return round(percentage, 2)

parser = argparse.ArgumentParser(description=STORE_RESULT_USAGE_EXAMPLE,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--name",
                    help=STORE_RESULT_NAME_HELP,
                    required=True)
parser.add_argument("--dob", type=validate_date,
                    help=STORE_RESULT_DOB_HELP,
                    required=True)
parser.add_argument("--subject",
                    choices=SUBJECT_CHOICES,
                    help=STORE_RESULT_SUBJECT_HELP,
                    required=True)
parser.add_argument("--total", type=int,
                    help=STORE_RESULT_TOTAL_HELP,
                    required=True)
parser.add_argument("--score", type=float,
                    help=STORE_RESULT_SCORE_HELP,
                    required=True)
parser.add_argument("--store",
                    help=STORE_RESULT_STORE_HELP,
                    required=True)


def main(result_dict):
    file_name = result_dict.pop('store')

    validate_score(result_dict)
    validate_file_type(file_name)

    result_dict['percentage'] = get_percentage(result_dict)

    if not pathlib.Path(file_name).exists():
        create_new_file(file_name)
        write_new_record(file_name, result_dict)
        return

    check_for_duplicate_record(file_name, result_dict)
    write_new_record(file_name, result_dict)

if __name__ == "__main__":
    opts = parser.parse_args()

    main(opts.__dict__)
