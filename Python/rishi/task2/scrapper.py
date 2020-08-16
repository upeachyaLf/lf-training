import os
import csv
import time

import requests
from bs4 import BeautifulSoup

HAMROBAZAR_BASE_URL = "https://hamrobazaar.com/"
HAMROBAZER_SEARCH = f"{HAMROBAZAR_BASE_URL}search.php" 

CARS_CATID = 48
MOBILE_CATID = 2
ELECTRONICS_CATID = 4

HB_CAR_BRANDS = ["Madza", "Hyundai", "Chevrolet", "Daihatsu"]

SEARCH_LOCATION = "Kathmandu"
AUTO_MOBILE_SEARCH_URL = f"{HAMROBAZER_SEARCH}?do_search=Search&order=&way=&searchword=&catid_search={CARS_CATID}&city_search={SEARCH_LOCATION}&do_search=Search"

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

CAR_INFO = [
    "Name",
    "Make Year",
    "Kilometers Run",
    "Fuel Type",
    "Price",
    "Location",
    "Seller",
    "Condition"
]

def request_and_get_soup(url, headers=None):
    res = requests.get(url, headers= headers)
    if not res.ok:
        return 
    return BeautifulSoup(res.text, 'lxml')

def get_per_car_url_list(brands):
    listed_cars_url = []
    for car_brand in HB_CAR_BRANDS:
        if car_brand in brands:
            listed_cars_url.append(AUTO_MOBILE_SEARCH_URL.replace('&searchword=', f'&searchword={car_brand.lower()}'))
        else:
            print(f"Brand:{car_brand} Not found")
    
    return listed_cars_url

def scrape_for_cars(soup):
    parent_table = soup.find_all('table', {"align": "center" })
    write_to_file(str(parent_table))

def write_to_file(html):
    with open('hamrobazar.html', mode='w') as debug_file:
        debug_file.write(html)

def scrape_from_page(url):
    if not url.startswith("https"):
        url = f"{HAMROBAZAR_BASE_URL}{url}"
    
    soup1 = request_and_get_soup(url, HEADERS)
    if not soup1:
        return 

    categories = soup1.find('select', {"name": "catid_search"}).findChildren()
    brands = [category.get_text(strip=True) for category in categories]
    url_list = get_per_car_url_list(brands[3:])
    
    for url in url_list:
        soup = request_and_get_soup(url, HEADERS)
        scrape_for_cars(soup)
        break

    return 

if __name__ == "__main__":
    scrape_from_page(AUTO_MOBILE_SEARCH_URL)
    
