#!/usr/bin/env python

import csv
import argparse
import datetime
import pathlib

USAGE_EXAMPLE = "Usage example:\n python3 store_result.py --name John Doe --dob 01-11-2001 --subject Nepali --total 100 --score 65.25 --store store.csv"
NAME_HELP = "Name of student: 'FIRST MIDDLE(optional) LAST'"
DOB_HELP = "Student's Date of Birth in DD-MM-YYYY format."
SUBJECT_HELP = "Value should be from the set."
TOTAL_HELP = "Total/full marks for the subject."
SCORE_HELP = "Score of the selected subject. Value should be a floating point number and can not be greater than full/total marks of the subject or less than 0."
STORE_HELP = "File name to store the result. e.g. store.csv"

FIELD_NAMES = ['name', 'dob', 'subject', 'total', 'score', 'percentage']

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

parser = argparse.ArgumentParser(description=USAGE_EXAMPLE,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--name",
                    help=NAME_HELP,
                    required=True)
parser.add_argument("--dob", type=validate_date,
                    help=DOB_HELP,
                    required=True)
parser.add_argument("--subject",
                    choices=['Nepali', 'English', 'Math', 'Science', 'Social'],
                    help=SUBJECT_HELP,
                    required=True)
parser.add_argument("--total", type=int,
                    help=TOTAL_HELP,
                    required=True)
parser.add_argument("--score", type=float,
                    help=SCORE_HELP,
                    required=True)
parser.add_argument("--store",
                    help=STORE_HELP,
                    required=True)


if __name__ == "__main__":
    opts = parser.parse_args()
    result_dict = opts.__dict__
    file_name = result_dict.pop('store')

    validate_score(result_dict)
    validate_file_type(file_name)

    result_dict['percentage'] = get_percentage(result_dict)

    if not pathlib.Path(file_name).exists():
        create_new_file(file_name)
        write_new_record(file_name, result_dict)
        exit()

    check_for_duplicate_record(file_name, result_dict)
    write_new_record(file_name, result_dict)
