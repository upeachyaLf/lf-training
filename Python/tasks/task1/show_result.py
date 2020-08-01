import os
import csv
import argparse
import operator
import datetime as dt

def calculatePercentage (score, total):
    return (float(score)/int(total) * 100)

def displayRecords(fileName):
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
            records += "Percentage: {}".format(calculatePercentage(row["score"],row["total"])) + "\n"
            records += "-----------------"+ "\n\n"
        file.close()
        return records

def storeResult(result):
    with open ("result.txt", "w") as resultFile:
        resultFile.write(result)
        resultFile.close()

parser = argparse.ArgumentParser()
parser.add_argument("-s","--store", help="Enter filename to read its content")

args = parser.parse_args()

store = args.store
if not store:
    print("Please enter a file name!")
elif os.path.exists(store):
    print(displayRecords(store));  
    storeResult(displayRecords(store))
else:
    print("File with name %s not found" %(store))