import argparse
import csv
import os
from datetime import datetime

def display_records(headers, records):
    result = ''
    for row in records:
        result += f"Name: {row[0]}".format() + "\n"
        result += f"Date of Birth: {row[1]}\n" 
        result += f"{row[2]}:\n"
        result += f"\tScore: {row[3]}\n"
        result += f"\tTotal: {row[4]}\n"
        result += f"Percentage: {row[5]}\n"
        result += "-----------------"+ "\n\n"
    print(result)

def read_records(filename):
    try:
        records = {}
        lists = []
        with open(filename, mode='r') as f:
            readers = csv.reader(f)
            headers = next(readers)
            for row in readers:
                lists.append(row)
            return (headers, lists)
    except IOError:
        raise

def get_args(args=None):
    parser = argparse.ArgumentParser(prog='Show User Info', description='CLI to Show User Info')
    user_information = parser.add_argument( 
        "--store", required=True, help="File Name")
    return parser.parse_args(args)

def main(args=None):
    args = get_args()
    return args.store

if __name__ == "__main__":
    filename = main()
    if not os.path.exists(filename):
        raise FileNotFoundError("Create Record!")
    get_records = read_records(filename)
    display_records(get_records[0], get_records[1])
    
