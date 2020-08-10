''' Task 1 CLI application to show information saved in file. '''
import os
import argparse
import datetime

index = {'name': 0, 'dob': 1, 'English': 2, 'Nepali': 4, 'optional': 6, 'optionalSubject': 8}


def show_result(filename):
    ''' Show result form file '''
    if not os.path.isfile(filename):
        print('File doesn\'t exist! Please enter valid stored filename... (Use --help for help)')
        exit(1)
    with open(filename, 'r') as store:
        data = store.readlines()
        for result in data:
            result = result.split(',')
            print(f'Name: {result[index.get("name")]}')
            print(f'DOB: {datetime.datetime.strptime(result[index.get("dob")], "%Y-%m-%d %H:%M:%S").strftime( "%d %B, %Y")}')
            if float(result[index.get('English')]) > 0:
                print(f"English:")
                print(f"    Score: {result[index.get('English')]}")
                print(f"    Total: {result[index.get('English') + 1]}")
                print(f"    Percentage: {float(result[index.get('English')]) / float(result[index.get('English') + 1]) * 100}")
            if float(result[index.get('Nepali')]) > 0:
                print(f"Nepali:")
                print(f"    Score: {result[index.get('Nepali')]}")
                print(f"    Total: {result[index.get('Nepali') + 1]}")
                print(f"    Percentage: {float(result[index.get('Nepali')]) / float(result[index.get('Nepali') + 1]) * 100}")
            if float(result[index.get('optional')]) > 0:
                print(f"{result[index.get('optionalSubject')]}:")
                print(f"    Score: {result[index.get('optional')]}")
                print(f"    Total: {result[index.get('optional') + 1]}")
                print(f"    Percentage: {float(result[index.get('optional')]) / float(result[index.get('optional') + 1]) * 100}")
            print('……..')
            percentage = (float(result[index.get('English')]) + float(result[index.get('Nepali')]) + float(result[index.get('optional')])) / (float(result[index.get('English') + 1]) + float(result[index.get('Nepali') + 1]) + float(result[index.get('optional') + 1])) * 100
            print(f"Total Percentage: {percentage}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Show user information')
    parser.add_argument('--store', type=str, help='information stored file name')

    args = parser.parse_args()
    if args.store:
        show_result(args.store)
    else:
        print('Specify target file using --store')
    
    exit(0)
