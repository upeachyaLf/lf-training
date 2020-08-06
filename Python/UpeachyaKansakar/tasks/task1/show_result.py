import os
import csv
import argparse
import operator
import datetime as dt

def calculate_percentage (score, total):
    if score and total :
        return (float(score)/int(total) * 100)
    else:
        return 0

def display_records(fileName):
    with open (fileName,"r") as file:
        csv_reader = csv.DictReader(file)
        records = ''
        for row in csv_reader:
            records += "Name: {}".format(row["name"]) + "\n"
            date = dt.datetime.strptime(row["dob"], '%Y/%m/%d')
            records += "Date of birth: {}".format(date) + "\n"
            records += row["subject"] + ":\n"
            records += "\t"+"Score: {}".format(row["score"]) + "\n"
            records += "\t"+"Total: {}]".format(row["total"]) + "\n"
            records += "Percentage: {}".format(calculate_percentage(row["score"],row["total"])) + "\n"
            records += "-----------------"+ "\n\n"
        return records

def store_result(result):
    with open ("result.txt", "w") as resultFile:
        resultFile.write(result)

def main ():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--store", help="Enter filename to read its content")

    args = parser.parse_args()

    store = args.store
    if not store:
        print("Please enter a file name!")
    elif os.path.exists(store):
        print(display_records(store));  
        store_result(display_records(store))
    else:
        print("File with name %s not found" %(store))

if __name__=="__main__":
    main()