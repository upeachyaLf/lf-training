import argparse
from datetime import datetime

def validate_date(date):
    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except (ValueError,TypeError):
        error_msg = f"Invalid date or format: {date}"
        raise argparse.ArgumentTypeError(error_msg)

def user_info(group):
    group.add_argument('--name', required=True, metavar='', help='Name of user')
    group.add_argument('--dob', required=True, type=validate_date, help="Date of Birth with format YYYY-MM-DD")

def result_info(group):

    group.add_argument('--score', type=int, required=True, metavar='', help='Score of user in particular subject')
    group.add_argument('--total', type=int, required=True, metavar='', help='Total marks of subject')
    group.add_argument('--subject', choices=['English', 'Nepali', 'Mathematics','Science'], required=True, metavar='', help='Name of subject. Options: English, Neplai, Mathematics or Science')
    group.add_argument("--store", required=True, metavar='', help='Name of file to store output.')

def percentage(args):
    try:
        return float(args.score/args.total*100)
    except ZeroDivisionError:
        print("Division by zero error")


def output_file(filename, args):
    with open(filename, "a+") as newfile:
        newfile.write("\nName:"+args.name)
        newfile.write("\nDOB:"+str(args.dob))
        newfile.write("\n"+args.subject+"Score:"+str(args.score))
        newfile.write("\n"+args.subject+"Total:"+str(args.total))
        newfile.write("\n"+args.subject+"Percentage:"+str(percentage(args))+"\n")

def main():
    parser = argparse.ArgumentParser(description='Store user info using CLI')
    user_information = parser.add_argument_group('user')
    result_information = parser.add_argument_group('result')
    user_info(user_information)
    result_info(result_information)
    args = parser.parse_args()
    filename = args.store
    
    output_file(filename, args)
    

main()