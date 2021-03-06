import os
import csv
import argparse
import datetime as dt

POSSIBLE_SUBJECTS = ["english", "nepali", "mathematics", "science"]

def is_valid_date (date):
    try:
        dt.datetime.strptime(date, '%Y/%m/%d')
        return True
    except ValueError: 
        return False

def get_valid_record(args):
    if is_valid_date(args.dob):
        return [args.name, args.dob, args.subject, args.score, args.total]
    else:
        raise Exception(args.dob+" is not a valid date. Please enter in yyyy/mm/dd format")

def write_to_file(file, args, isFirstRecord):
    record_adder = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    try:
        # adding header row in case of new file
        if isFirstRecord:
            record_adder.writerow(["name", "dob", "subject", "score", "total"])
        record_adder.writerow(get_valid_record(args))
    except ValueError as error:
        print("ERROR: ",error)

def is_duplicate_record (args):
    with open(args.store, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["name"] == args.name and row["subject"].lower() == args.subject.lower():
                return True
    return False
            
def main():
    parser = argparse.ArgumentParser(prog="Task 1", description="Program to Store student information")
    parser.add_argument("-n","--name", help="Enter your full name")
    parser.add_argument("--dob", help="Enter date of birth in yyyy/mm/dd format")
    parser.add_argument("-s","--score", help="Enter score in subject you entered", type=float)
    parser.add_argument("-t","--total", help="Enter total score in subject you entered", type=int)
    parser.add_argument("-sub","--subject", help="Enter subject, Should be on of English, Nepali, Mathematics or Science", choices=POSSIBLE_SUBJECTS, type = lambda s : s.lower())
    parser.add_argument("--store", help="Enter filename to store entered record. Use file_name.csv")

    args = parser.parse_args()

    store = args.store
    if not store:
        print("Please enter a file name!")
    elif os.path.exists(store):
        # open file in append mode if it already exists
        file=open(store,"a")
        # check if current record already exists
        if is_duplicate_record(args):
            # TODO: append to existing record if duplicate
            print("Record already exists")
        else:
            write_to_file(file, args, False)
    else:
        # open file in write mode if filename dosent exist
        file = open(store, "w")
        write_to_file(file, args, True)

if __name__ == "__main__":
    main()
    