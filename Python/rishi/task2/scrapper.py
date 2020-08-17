import os
import csv
import time
import json

import requests
from bs4 import BeautifulSoup

from utils import CsvCreator

inputfile = 'search.csv'
outputfile = 'searchedData.csv'

DARAZ_BASE_URL = "https://www.daraz.com.np/"
DARAZ_SEARCH_URL = f"{DARAZ_BASE_URL}catalog/?q="

fieldname = ['title',
             'brand', 
             'price',
             'aggregateRating',
             'image_url',
             'description',
             'url_link'
             ]

class ConcernedFields:
    def __init__(self, title, price, url_link, image_url, description, ratings, brand):
        self.title = title
        self.brand = brand
        self.price = price
        self.description = description
        self.aggregateRating = ratings
        self.image_url = image_url
        self.url_link = url_link

def request_and_get_soup(url):
    if not url.startswith('https'):
        url = f"{DARAZ_SEARCH_URL}{url}" 
    response = requests.get(url)
    if not response.ok:
        return 

    return BeautifulSoup(response.text, 'lxml')

def debug_html(html):
    with open('daraz.html', mode='w') as debug_file:
        debug_file.write(str(html))

def write_to_csv(data):
    csv_to = CsvCreator(outputfile, fieldname)
    csv_to.write_to_file(data)

def scrape_product(product_url):
    row = {}
    row["title"] = 'UnKnown'
    row["price"] = 'UnKnown'
    row["url_link"] = 'UnKnown'
    row["image_url"] = 'UnKnown'
    row["description"] = 'UnKnown'
    row["aggregateRating"] = 0
    row["brand"] = 'UnKnown'

    soup = request_and_get_soup(product_url)
    if not soup:
        return

    searched_result = json.loads(soup.find_all('script', type='application/ld+json')[0].string)
    
    try:
        row["title"] = soup.find('span', class_="breadcrumb_item_anchor breadcrumb_item_anchor_last").text
        row["price"] = searched_result['offers']['priceCurrency'] + ': ' + str(max(searched_result['offers']['lowPrice'], searched_result['offers']['highPrice']))  
        row["url_link"] = searched_result['url']
        row["image_url"] = searched_result['image']
        row["description"] = searched_result['description']
        row["aggregateRating"] = searched_result['aggregateRating']
        row["brand"] = searched_result['brand']['name']
    except KeyError:
        pass
    
    return row 
    #ConcernedFields(title, price, url_link, image_url, description, ratings, brand)

def scrape_from_page(soup):
    searched_result = json.loads(soup.find_all('script', type='application/ld+json')[1].string)

    assert "itemListElement" in searched_result

    for i in searched_result["itemListElement"]:
        product_url = i["url"]
        concerned_data = scrape_product(product_url)
        write_to_csv(concerned_data)
        
def get_search_terms_from_file(inputfile):
    with open(inputfile, mode='r') as fp:
        csv_reader = csv.reader(fp, delimiter=',')
        line_count = 0
        for search_term in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            search_url = DARAZ_SEARCH_URL.replace("?q=", f"?q={search_term[0]}")
            print(search_url)
            soup = request_and_get_soup(search_url)
            if not soup:
                return 
            scrape_from_page(soup)
            time.sleep(5)

if __name__ == "__main__":
    if not os.path.isfile(inputfile):
        CsvCreator(inputfile, ['Search Term'])
        print('Input Your Search Terms for Daraz')
    else:
        get_search_terms_from_file(inputfile)
        
    

