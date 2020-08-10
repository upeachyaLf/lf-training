''' Task 1 CLI application to include user information adn save it in file. '''
import argparse
import datetime


def dob_parser(value):
    ''' Date of birth parser '''
    try:
        if not value:
            print('Please enter valid DOB(day/month/year)')
            exit(1)
        return datetime.datetime.strptime(value, "%m/%d/%Y")
    except (ValueError, TypeError):
        print('Please enter valid DOB(day/month/year)')
        exit(1)

def parse_data(args):
    ''' Parse data from args '''
    data = str(args.name) \
           + ',' + str(args.dob)
    data += ',' + str(args.score) + ',' + str(args.total) + ',0,0,0,0' if str(args.subject).lower() == 'english'\
            else ',0,0,' + str(args.score) + ',' + str(args.total) + ',0,0' if str(args.subject).lower() == 'nepali'\
                 else ',0,0,0,0,' + str(args.score if args.score else 0) + ',' + str(args.total if args.total else 100) + ',' + str(args.subject).lower()
    
    return data+",\n"

def is_valid_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def store_result(args):
    ''' Store user information '''
    if not args.store:
        print('Please enter valid filename for store! (Use --store)')
    if not args.dob:
        print('Please enter DOB using --dob')
    file_data = False
    try:
        with open(args.store, 'r+') as store:
            old_data = store.readlines()
            for row in old_data:
                if not row:
                    break
                data  = row.split(',')
                if str(data[0]).lower() == str(args.name).lower() and data[1] == str(args.dob):
                    new = parse_data(args)
                    new_data = new.split(',')
                    for key in range(len(new_data)):
                        try:
                            if is_valid_number(new_data[key]) and float(new_data[key]) < 1:
                                new_data[key] = data[key]
                        except Exception as e:
                            print("Error occured: {0}".format(e))
                            raise
                    file_data =  ''.join(old_data).replace(row , ','.join(new_data))
    except Exception as e:
        print(e)
        print('Creating new store file...')
    if file_data:
        with open(args.store, 'w') as store:
            store.write(file_data)
    else:
        insert(args)

        
def insert(args):
    ''' Insert new data '''
    with open(args.store, 'a+') as store:
        data = parse_data(args)
        store.write(data)

        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Store user information')
    
    parser.add_argument('--name', type=str, help='a name')
    parser.add_argument('--dob', help='a date of birth(day/month/year)', type=dob_parser)
    parser.add_argument('--score', type=float, help='the score in the subject')
    parser.add_argument('--total', type=int, help='the total score in subject')
    parser.add_argument('--subject', choices=['English', 'Nepali', 'Mathematics', 'Science'], help='a name of subject(English, Nepali, [Mathematics/Science])')
    parser.add_argument('--store', type=str, help='name of file to store')

    args= parser.parse_args()

    store_result(args)

    exit(0)
