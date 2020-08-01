import os
import csv
import argparse

POSSIBLE_SUBJECTS = ["english", "nepali", "mathematics", "science"]

def isValidSubject (subject):
    if subject and subject.lower() in POSSIBLE_SUBJECTS:
        return True
    return False

def getValidRecord(args):
    if isValidSubject(args.subject):
        return [args.name, args.dob, args.subject, args.score, args.total]
    else:
        raise Exception(args.subject+" is not a valid subject")

def writeToFile(file, args, isFirstRecord):
    record_adder = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    try:
        # adding header row in case of new file
        if isFirstRecord:
            record_adder.writerow(["name", "dob", "subject", "score", "total"])
        record_adder.writerow(getValidRecord(args))
    except ValueError as error:
        print("ERROR: ",error)

def isDuplicateRecord (args):
    with open(args.store, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["name"] == args.name and row["subject"].lower() == args.subject.lower():
                return True
    csv_file.close()
    return False
            

parser = argparse.ArgumentParser()
parser.add_argument("-n","--name", help="Enter your full name")
parser.add_argument("--dob", help="Enter date of birth in yyyy-mm-dd format")
parser.add_argument("-s","--score", help="Enter score in subject you entered", type=float)
parser.add_argument("-t","--total", help="Enter total score in subject you entered", type=int)
parser.add_argument("-sub","--subject", help="Enter subject, Should be on of English, Nepali, Mathematics or Science")
parser.add_argument("--store", help="Enter filename to store entered record. Use file_name.csv")

args = parser.parse_args()

store = args.store
if not store:
    print("Please enter a file name!")
elif os.path.exists(store):
    # open file in append mode if it already exists
    file=open(store,"a")
      # check if current record already exists
    if isDuplicateRecord(args):
        # TODO: append to existing record if duplicate
        print("Record already exists")
    else:
        writeToFile(file, args, False)
else:
    # open file in write mode if filename dosent exist
    file = open(store, "w")
    writeToFile(file, args, True)
    