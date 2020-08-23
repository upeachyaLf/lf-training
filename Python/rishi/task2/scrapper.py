import os
import csv
import time
import json
import urllib.parse as up
from functools import reduce
import yaml

import requests
from bs4 import BeautifulSoup

from utils import CsvCreator
from db import create_table, store_data 

inputfile = 'searchfile.csv'
directory_name = 'searchResults'
base_dir_path = os.getcwd()

directory_path = f"{base_dir_path}/{directory_name}" 

if not os.path.exists(directory_name):
    os.makedirs(directory_name)

DARAZ_BASE_URL = "https://www.daraz.com.np/"
DARAZ_SEARCH_URL = f"{DARAZ_BASE_URL}catalog/?q="

fieldname = [
             'brand',
             'title',
             'price',
             'aggregateRating',
             'image_url',
             'description',
             'url_link'
             ]

def request_and_get_soup(search_url):
    if not search_url.startswith('https'):
        search_url = f"{DARAZ_SEARCH_URL}{search_url}" 
    response = requests.get(search_url)
    if not response.ok:
        return

    return BeautifulSoup(response.text, 'lxml')

def debug_html(html):
    with open('daraz.html', mode='w') as debug_file:
        debug_file.write(str(html))

def get_filepath_name(path, name):
    filename = ''.join(s.strip() for s in name)
    return f"{path}/{filename}"

def format_price(data):
    if data.get('price'):
        price = data['price']
        result = float(price.split(':')[1].strip())
        data['price'] = result
    return data

def store_to_database(result):
    values = []
    search_terms = [(i,) for i in result.keys()]
    print(search_terms)
    store_data('search_term', search_terms)
    for key, contents in result.items():
        for x in contents.keys():
            for data_ in contents[x]:
                data = format_price(data_)
                value = tuple(i for i in data.values())  # + (1,) static Foreign Keys Reference Value
                print(value)
                values.append(value)
    store_data('contents',values)

def write_to_csv(fp, contents):
    filepath = get_filepath_name(directory_path, fp)
    output_file_handle = CsvCreator(filepath, fieldname)
    for brand, rows in contents.items():
        for row in rows:
            output_file_handle.write_to_file(row)
    return

def write_to_yaml(fp, contents):
    filepath = get_filepath_name(directory_path,fp) + '.yaml'
    with open(filepath, 'w') as file_:
        yaml.dump(contents, file_)

def scrape_product(soup):
    searched_result = json.loads(soup.find_all('script', type='application/ld+json')[0].string)
    row = {}
    try:
        row["title"] = soup.find('span', class_="breadcrumb_item_anchor breadcrumb_item_anchor_last").text
        row["price"] = searched_result['offers']['priceCurrency'] + ': ' + str(max(searched_result['offers']['lowPrice'], searched_result['offers']['highPrice']))  
        row["url_link"] = searched_result['url']
        row["image_url"] = searched_result['image']
        row["description"] = 'No Description'
        row["aggregateRating"] = searched_result['aggregateRating']['ratingValue'] if 'aggregateRating' in searched_result else 'N/A'
        row["brand"] = searched_result['brand']['name']
    except KeyError as err:
        print(f'KeyError:***\n{err}')
        raise
    return row 

def search_for_items(soup):
    searched_result = json.loads(soup.find_all('script', type='application/ld+json')[1].string)

    assert "itemListElement" in searched_result
    product_url =[]
    for item in searched_result["itemListElement"]:
        product_url.append(item["url"])
    
    return product_url
        
def get_search_terms_from_file(inputfile):
    with open(inputfile, mode='r') as fp:
        csv_reader = csv.DictReader(fp, delimiter=',')
        search_urls = {}
        for reader in csv_reader:
            query = reader['SearchTerm']

            #Encode query param string
            query_param = up.quote(query) 
            search_url = DARAZ_SEARCH_URL.replace("?q=", f"?q={query_param}")
            search_urls[query] = search_url  
        return search_urls

def flatten_brand_as_key(acc, product_content):
    if acc.get(product_content['brand']):
        value = acc.get(product_content['brand'])
        content = value
        content.append(product_content)
        acc[product_content['brand']] = content 
        return acc
    acc[product_content['brand']] = [product_content]
    return acc

def scrapper():
    search_urls = get_search_terms_from_file(inputfile)
    products = {}
    for search_term, search_url in search_urls.items():
        soup = request_and_get_soup(search_url)

        if not soup:
            return
        
        searched_products_list = search_for_items(soup)
        products[search_term] = searched_products_list 
        time.sleep(5)
    product_contents ={}
    for product, product_urls in products.items():
        info = []
        for url in product_urls:
            soup = request_and_get_soup(url)

            if not soup:
                return
            
            info.append(scrape_product(soup))
            time.sleep(3)
        product_contents[product] = info
    result = {}
    for product, contents in product_contents.items():
        get_result = reduce(flatten_brand_as_key,contents, {})
        result[product] = get_result

    for brand, content in result.items():
        write_to_csv(brand, content)
        write_to_yaml(brand, content)
    
    store_to_database(result)
    return

if __name__ == "__main__":
    if not os.path.isfile(inputfile):
        CsvCreator(inputfile, ['SearchTerm'])
        print('Input Your Search Terms for Daraz')
    create_table()
    scrapper()
