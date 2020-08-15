import argparse
from datetime import datetime
import json
from pathlib import Path

#Validate if entered date is valid or not
#Then return date in string format
def valid_date(date_input):
    return datetime.strptime(date_input, "%Y/%m/%d").strftime("%Y/%m/%d")

#Calculate percentage
def perc(score, total):
    return (score / total) * 100

#Creates and overwrites if exists
def writeFile(filename, content):
    with open(filename, 'w') as f:
        json.dump(content, f, indent = 2)

parser = argparse.ArgumentParser(description = 'View result')

parser.add_argument("--name",\
    help = "Specify your name here")
parser.add_argument("--dob",\
    help = "Specify your dob here in YYYY/MM/DD format",\
    type = valid_date)
parser.add_argument("--score", \
    type = float,\
    help = "Score in the subject")
parser.add_argument("--total", \
    type = int,\
    default = 100,\
    help = "Calculated total marks")
parser.add_argument("--subject", \
    choices = ['English', 'Math', 'Science'],\
    help = "Specify the subject")
parser.add_argument("--store", \
    help = "Enter a filename")

args = parser.parse_args()

filename = args.store

values = args.__dict__


#Delete filename information from values
del values['store']

#Insert percentage key and values in the dictionary
values.update({"percentage": perc(values['score'], values['total'])})
print(values)

newdict = {
    'name' : values['name'],
    'dob' : values['dob'],
    'subject' : [{
        'sub_name' : values['subject'],
        'score' : values['score'],
        'total' : values['total'],
        'percentage' : values['percentage']
        }]
    }

sub_values = values['subject']

#If the file already exists then append to the existing file
if Path.is_file(Path(Path.cwd(),filename)):
    with open(filename, 'r') as file1:
        file_content = json.load(file1)

        #Get index from the list, if the student info already exist
        def get_index(file_content):
            for num, d in enumerate(file_content):
                if d['name'] == values['name']:
                    index_of = num
                    print(index_of)
                    print(file_content)
                    return index_of
        
        index_of = get_index(file_content)

        # If the student record doesnot exist, append to the subject list
        if index_of is not None:
            file_content[index_of]['subject'].append({
                    'sub_name' : values['subject'],
                    'score' : values['score'],
                    'total' : values['total'],
                    'percentage' : values['percentage']
                })

        #otherwise append to the original list
        else:
            file_content.append(newdict)

        writeFile(filename, file_content)

#If filename is new, create and write to new file
else:
    writeFile(filename, [newdict])
