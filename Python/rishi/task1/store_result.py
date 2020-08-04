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

def get_current_file_contents(f, args):
    data_lists = []
    with open(f, mode='r') as reader:
        csv_reader = csv.reader(reader)
        for row in csv_reader:
            data_lists.append(row)
            if row[0] == args.name and row[2] == args.subject:
                data_lists.remove(row)
        return data_lists

def write_to_file(filepath, writelines):
    with open(filepath, mode='w') as writefile:
        try:
            writer = csv.writer(writefile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(writelines)
        except IOError:
            raise Exception('Error while writing to the file') 

def addheader(filepath, writeline):
    with open(filepath, mode='w') as writefile:
        writer = csv.writer(writefile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(writeline)
    return 

def store_user_info(filepath, args):
    content = get_current_file_contents(filepath, args)
    content.append([args.name, args.dob, args.subject, args.score, args.totalscore,  str(calc_percent(args.totalscore,args.score)) + '%'])
    write_to_file(filepath, content)
        
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
    store_user_info(filename, args)

    return 
main()