import os, json
import argparse

#load json contents into an object
def get_result(filename):
    if os.path.exists(filename) and os.path.isfile(filename):
        with open(filename, 'r') as results:
            data = json.load(results)
            print_result(data)
    
#Ask for valid filename to the user
    else:
        print("File does not exist.")
        filename = input("Enter filename:")
        get_result(filename)

#print result in required format
def print_result(data):
    for x in data:
        print(" Name:", x['name'],\
        "\n DOB:", x['dob'],)

        total_percentage = 0
        
        # Loop through the multiple subject data for same student
        for y in range(len(x['subject'])):
            print("\n",x['subject'][y]['sub_name'],"Score:", x['subject'][y]['score'],\
            "\n",x['subject'][y]['sub_name'],"Total:", x['subject'][y]['total'],\
            "\n",x['subject'][y]['sub_name'],"Percentage:", x['subject'][y]['percentage'])

            # Calculate total percentage
            total_percentage += x['subject'][y]['percentage']

    # Print total percentage of all subject
        print(" Total percentage =", total_percentage)
        print("------------------------------------")

parser = argparse.ArgumentParser(description= "Shows the results")

parser.add_argument("--store", \
    help = "Enter filename to view the result")

args = parser.parse_args()
filename = args.store

get_result(filename)
