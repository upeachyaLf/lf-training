import sys
import argparse
from datetime import datetime 

def dob_parser(value):
   return datetime.strptime(value,'%d/%m/%Y')

def percentage_cal(score, total):
   return ((score/total)*100)

parser = argparse.ArgumentParser(prog='Result Generation')
parser.add_argument('name', type=str, help='Name of user')
parser.add_argument('dob', type=dob_parser, help='DOB of user in dd/mm/yyyy format')
parser.add_argument('score', type=float, help='Score of the user')
parser.add_argument('total', type=float, help='Total marks')
parser.add_argument('subject', choices=['English','Mathematics','Nepali','Science'], help='One of the subjects')
parser.add_argument('FILENAME', type=str, help='Name of the file you want to write to in txt format')

args = parser.parse_args()

per=percentage_cal(args.score,args.total)
record = args.__dict__
record.update( {'percentage' : per})
filename=record['FILENAME']

try:
   with open(filename, 'at') as f: 
      for key, value in record.items():
         f.write('%s:%s\n' % (key, value))
      f.write('\n')

except IOError: 
    print ("The file creation failed")

#f.close(f)

