import argparse
from datetime import datetime
import csv
import os

SUBJECT_CHOICES = ['English', 'Nepali', 'Mathematics']
HEADERS = ["name", "dob", "subject","score", "total", "percentage"]
# UNIQUE_DATA = ["name", "subject"]

def date_validation(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        error_msg = f"Not a valid date: {s}"
        raise argparse.ArgumentTypeError(error_msg) 

def calc_percent(total, score):
    try:
        return score/total*100 
    except ZeroDivisionError:
        raise Exception('division by zero')

def numeric_type(num):
    try:
        return float(num)
    except ValueError:
        error_msg = "Must be a number type"
        raise argparse.ArgumentTypeError(error_msg)  

def validate_choice(sub):
    try:
        subject = sub.strip().capitalize()
        if subject in SUBJECT_CHOICES:
            return subject
        raise argparse.ArgumentError(f'Invalid Choice: {sub} (choose from {tuple(SUBJECT_CHOICES)})')
    except ValueError:
        raise argparse.ArgumentTypeError('Not a valid Type')

def add_subcommand_get_user_info(group):
    group.add_argument(
        '-n' , "--name", help="Name", required=True
    )
    group.add_argument(
        '--dob', "--dateofbirth", help="Date Of Birth - format YYYY-MM-DD", 
                    required=True, 
                    type=date_validation
    )
    group.add_argument(
        '-sub', '--subject', choices=['English', 'Nepali', 'Mathematics'], required=True, type=validate_choice
    )
    group.add_argument(
        '--score', type=numeric_type, required=True
    )
    group.add_argument(
        '-total', '--totalscore', type=int, required=True
    )

def add_subcommand_store_data(group):
    group.add_argument(
        # "--store", type=argparse.FileType('w', encoding='UTF-8'), help="Output User Info", required=True
        "--store", required=True, help="Output User Info"
    )

def isDuplicateRecord(f, args):
    with open(f, mode='r') as reader:
        csv_reader = csv.DictReader(reader)
        for row in csv_reader:
            if row["name"] == args.name and row["subject"] == args.subject:
                return True
        return False

def write_to_file(file, args):
    try:
        thewriter = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        thewriter.writerow([args.name, args.dob, args.subject, args.score, args.totalscore,  str(calc_percent(args.totalscore,args.score)) + '%'])
    except IOError:
        raise Exception('Error while writing to the file') 

def addheader(file, headers):
    with open(file, mode='w') as f:
        thewriter = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        thewriter.writerow(headers)
    return 

def store_user_info(file, args):
    if isDuplicateRecord(args.store, args):
        print('Duplicate Record Found')
        return 
    else:
        write_to_file(file, args)
        return

        
def main(args=None):
    parser = argparse.ArgumentParser(prog='user_info', description='CLI to store User Info')
    user_information = parser.add_argument_group('user_info')
    store_info = parser.add_argument_group('store_info')
    add_subcommand_get_user_info(user_information)
    add_subcommand_store_data(store_info)

    args = parser.parse_args(args)
    filename = args.store
    # writer = csv.writer(args.store)

    if not os.path.exists(filename):
        addheader(filename, HEADERS)
    file=open(filename,"a")
    store_user_info(file, args)

    return 
main()