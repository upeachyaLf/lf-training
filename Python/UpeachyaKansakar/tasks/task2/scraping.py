import time
import requests
import urllib.request
from bs4 import BeautifulSoup

URL = 'https://www.opencodez.com/category/web-development'

def scrapPagetitle(soupObject):
    title_divs = soupObject.findAll('h2',{'class':'title'})
    titles = []
    for title in title_divs:
        titles.append(title.get_text())   
    return titles  

def getTotalPages(soupObject):
    pagination_div = soupObject.find('div',{'class':'pagination'})
    return len(pagination_div.findAll('li'))

def main():
    all_titles = []
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser') 
    all_titles = scrapPagetitle(soup)
    time.sleep(3)
    # NOTE: looping to scrape all pages
    total_pages = getTotalPages(soup)
    # NOTE: page 0 is already fetched so starting from 1
    for pageNumber in range(1, total_pages-1):
        url_with_pagination = URL + '/page/' + str(pageNumber)
        response = requests.get(url_with_pagination)
        soup = BeautifulSoup(response.text, 'html.parser') 
        all_titles = all_titles + scrapPagetitle(soup)
        time.sleep(3)

    
    import pdb
    pdb.set_trace()


if __name__ == "__main__":
    main()