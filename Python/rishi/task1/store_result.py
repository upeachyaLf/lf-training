import argparse
from datetime import date
import csv
import os

SUBJECT_CHOICES = ['English', 'Nepali', 'Mathematics']
HEADERS = ["name", "dob", "subject","score", "total", "percentage"]
# UNIQUE_DATA = ["name", "subject"]

def date_validation(s):
    try:
        return date.fromisoformat(s)
    except ValueError:
        error_msg = f"Not a valid date: {s}"
        raise argparse.ArgumentTypeError(error_msg) 

def calc_percent(total, score):
    try:
        return score/total*100 
    except ZeroDivisionError:
        raise ZeroDivisionError('division by zero')

def numeric_type(num):
    try:
        return float(num)
    except ValueError:
        error_msg = "Must be a number type"
        raise argparse.ArgumentTypeError(error_msg)  

def validate_choice(sub):
    try:
        return sub.strip().capitalize()
    except AttributeError:
        raise argparse.ArgumentTypeError('Not a valid Type')

def add_subcommand_get_user_info(group):
    group.add_argument(
        '-n' , "--name", help="Name", required=True
    )
    group.add_argument(
        '--dob', help="Date Of Birth - format YYYY-MM-DD", 
                    
                    type=date_validation
    )
    group.add_argument(
        '-sub', '--subject', choices=['English', 'Nepali', 'Mathematics'], type=validate_choice, default='English'
    )
    group.add_argument(
        '--score', type=numeric_type, default=40
    )
    group.add_argument(
        '-total', '--totalscore', type=int, default=100
    )

def add_subcommand_store_data(group):
    group.add_argument(
        # "--store", type=argparse.FileType('w', encoding='UTF-8'), help="Output User Info", required=True
        "--store", help="Output User Info", default='user_info.csv'
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

def make_list(args):
    return [args.name, args.dob, args.subject, args.score, args.totalscore, str(calc_percent(args.totalscore,args.score)) + '%']

def append_contents(content, args):
    content.append([*args])
    return content

def get_args(args=None):
    parser = argparse.ArgumentParser(prog='user_info', description='CLI to store User Info')
    user_information = parser.add_argument_group('user_info')
    store_info = parser.add_argument_group('store_info')
    add_subcommand_get_user_info(user_information)
    add_subcommand_store_data(store_info)

    return parser.parse_args(args)

def main(args=None):
    args = get_args(args)
    return args

if __name__ == "__main__":
    args = main()
    filename = args.store
    if not os.path.exists(filename):
        addheader(filename, HEADERS)
    args_list = make_list(args)
    current_content = get_current_file_contents(filename, args)
    new_content = append_contents(current_content, args_list)
    write_to_file(filename,new_content)