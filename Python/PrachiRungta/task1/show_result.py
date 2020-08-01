import sys
import argparse
from datetime import datetime 

parser = argparse.ArgumentParser(prog='Result Display')
parser.add_argument('FILENAME', type=str, help='Name of the file you want to view to in txt format/ please add .txt at the end')
args = parser.parse_args()

filename=args.FILENAME
resultfile=None
try:
    resultfile=open(filename,"r") 
    print(resultfile.read())
    resultfile.close()

except IOError: 
    print ("File does not appear to exist.")
    #return 





