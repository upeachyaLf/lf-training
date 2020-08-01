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
        datetime.datetime.strptime(date_string, '%d-%m-%Y')
        return date_string
    except (ValueError):
        raise SystemExit('Invalid date format. Should be DD-MM-YYYY.')


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

    if result_dict['score'] > result_dict['total'] or result_dict['score'] < 0 or result_dict['score'] == -0.0:
        raise SystemExit(
            'Score not in valid range. \npython3 store_result.py --help, for detail.')

    if not pathlib.Path(file_name).exists():
        if file_name.find('.csv') == -1:
            raise SystemExit('File extension should be .csv')

        with open(file_name, 'w', newline='') as new_file:
            new_file_writer = csv.writer(new_file, delimiter=',')
            new_file_writer.writerow(FIELD_NAMES)

    print(result_dict)

    with open(file_name, 'r', newline='') as result_file:
        result_file_reader = csv.DictReader(result_file)
        for row in result_file_reader:
            if row['name'] == result_dict['name'] and row['dob'] == result_dict['dob'] and row['subject'] == result_dict['subject']:
                raise SystemExit('Result already exists.')
    result_dict['percentage'] = (
        result_dict['score'] / result_dict['total']) * 100
    with open(file_name, 'a', newline='') as result_file:
        result_file_writer = csv.DictWriter(
            result_file, fieldnames=FIELD_NAMES)
        result_file_writer.writerow(result_dict)
