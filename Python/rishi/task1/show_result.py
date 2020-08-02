import argparse
import csv
import os

def display_records(headers, records):
    result = ''
    for row in records:
        result += f"Name: {row[0]}".format() + "\n"
        result += f"Date of Birth: {row[1].split(' ')[0]}\n" 
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
            # map_row_to_headers = {header: '' for header in headers} 
            # print(map_row_to_headers)
            for row in readers:
                lists.append(row)
            return display_records(headers, lists)
    except FileNotFoundError:
        raise Exception('csv format file only')

def main(args=None):
    parser = argparse.ArgumentParser(prog='Show User Info', description='CLI to Show User Info')
    user_information = parser.add_argument( 
        "--store", required=True, help="Output User Info")

    args = parser.parse_args(args)
    filename = args.store

    if not os.path.exists(filename):
        print("Please Enter Records First")
    
    read_records(filename)

main()
