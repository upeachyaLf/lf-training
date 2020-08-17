import os
import csv
import time
import json

import requests
from bs4 import BeautifulSoup

from utils import CsvCreator

FileName = 'search.csv'

#https://www.daraz.com.np/catalog/?q=speaker&_keyori=ss&from=input&spm=a2a0e.11779170.search.go.287d2d2bFvrk5D
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

def write_to_file(html):
    with open('daraz.html', mode='w') as debug_file:
        debug_file.write(str(html))


def write_to_csv(data):
    print(data.title)
    csv_to = CsvCreator('searched_data.csv', fieldname)
    # csv_to.write_to_file(data)

def scrape_product(product_url):
    title = ''
    price = ''
    url_link = ''
    image_url = ''
    description = ''
    ratings = 0
    brand = ''

    soup = request_and_get_soup(product_url)
    if not soup:
        return

    searched_result = json.loads(soup.find_all('script', type='application/ld+json')[0].string)
    
    try:
        title = soup.find('span', class_="breadcrumb_item_anchor breadcrumb_item_anchor_last").text
        price = searched_result['offers']['priceCurrency'] + ': ' + str(max(searched_result['offers']['lowPrice'], searched_result['offers']['highPrice']))  
        url_link = searched_result['url']
        image_url = searched_result['image']
        description = searched_result['description']
        ratings = searched_result['aggregateRating']
        brand = searched_result['brand']['name']
    except AttributeError:
        pass
    
    return ConcernedFields(title, price, url_link, image_url, description, ratings, brand)

def scrape_from_page(soup):
    searched_result = json.loads(soup.find_all('script', type='application/ld+json')[1].string)

    assert "itemListElement" in searched_result

    for i in searched_result["itemListElement"]:
        product_url = i["url"]
        concerned_data = scrape_product(product_url)
        write_to_csv(concerned_data)
        break
        
def get_search_terms_from_file(filename):
    with open(filename, mode='r') as fp:
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
            break


if __name__ == "__main__":
    if not os.path.isfile(FileName):
        CsvCreator(FileName, 'Search Term')
        print('Input Your Search Terms for Daraz')
    else:
        get_search_terms_from_file(FileName)
        
    

