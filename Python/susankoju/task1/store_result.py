''' Task 1 CLI application to include user information adn save it in file. '''
import argparse
import datetime


def dob_parser(value):
    ''' Date of birth parser '''
    try:
        return datetime.datetime.strptime(value, "%m/%d/%Y")
    except (ValueError, TypeError):
        return False

def parse_data(args):
    ''' Parse data from args '''
    data = args.name \
           + ',' + str(args.dob)
    data += ',' + str(args.score) + ',' + str(args.total) + ',0,0,0,0' if args.subject.lower() == 'english'\
            else ',0,0,' + str(args.score) + ',' + str(args.total) + ',0,0' if args.subject.lower() == 'nepali'\
                 else ',0,0,0,0,' + str(args.score) + ',' + str(args.total) + ',' + str(args.subject)
    
    return data+",\n"
    
def store_result(args):
    ''' Store user information '''
    file_data = False
    try:
        with open(args.store, 'r+') as store:
            old_data = store.readlines()
            for row in old_data:
                if not row:
                    break
                data  = row.split(',')
                if data[0].lower() == args.name.lower() and data[1] == str(args.dob):
                    new = parse_data(args)
                    new_data = new.split(',')
                    for key in range(len(new_data)):
                        try:
                            if float(new_data[key]) < 1:
                                new_data[key] = data[key]
                        except Exception as e:
                            pass
                    file_data =  ''.join(old_data).replace(row , ','.join(new_data))
    except Exception as e:
        print(str(e))
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
    parser.add_argument('--subject', type=str, help='a name of subject')
    parser.add_argument('--store', type=str, help='name of file to store')

    args= parser.parse_args()

    store_result(args)

    exit(0)

