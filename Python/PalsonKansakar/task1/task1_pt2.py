import argparse
parser = argparse.ArgumentParser(description='CLI to print User Info')
parser.add_argument('--store',required=True, metavar='', help='Name of file to print output.')
args= parser.parse_args()

with open(args.store) as myfile:
    myfile.seek(0)
    content = myfile.read()
print(content)