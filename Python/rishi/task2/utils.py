import csv

from config import DIRECTORY_PATH

def get_filepath_name(name):
    filename = ''.join(s.strip() for s in name)
    return f"{DIRECTORY_PATH}/{filename}"

def format_price(data):
    if data.get('price'):
        price = data['price']
        result = float(price.split(':')[1].strip())
        data['price'] = result
    return data

def flatten_brand_as_key(acc, product_content):
    if acc.get(product_content['brand']):
        value = acc.get(product_content['brand'])
        content = value
        content.append(product_content)
        acc[product_content['brand']] = content 
        return acc
    acc[product_content['brand']] = [product_content]
    return acc
    
class CsvCreator:
    def __init__(self, filename, headers):
        self.filename = filename + '.csv' if not filename.endswith('.csv') else filename
        self.headers = headers
        self.createfile()
    
    def createfile(self):
        with open(self.filename, mode='w', encoding='utf8') as csv_file:
            writer =csv.DictWriter(csv_file, fieldnames=self.headers)
            writer.writeheader()
    
    def write_to_file(self, row):
        with open(self.filename, mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.headers)
            writer.writerow(row)