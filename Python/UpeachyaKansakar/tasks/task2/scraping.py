import time
import pandas 
import requests
import urllib.request
from bs4 import BeautifulSoup

URL = 'https://www.opencodez.com/category/web-development'

def scrap_page_title(soupObject):
    title_divs = soupObject.findAll('h2',{'class':'title'})
    titles = []
    for title in title_divs:
        titles.append(title.get_text())   
    return titles  

def get_total_pages(soupObject):
    pagination_div = soupObject.find('div',{'class':'pagination'})
    return len(pagination_div.findAll('li'))

def save_as_csv (all_titles):
    df = pandas.DataFrame({'title':all_titles}) 
    df.to_csv('output/articles.csv', index=False, encoding='utf-8')

def main():
    all_titles = []
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser') 
    all_titles = scrap_page_title(soup)
    time.sleep(3)
    # NOTE: looping to scrape all pages
    total_pages = get_total_pages(soup)
    # NOTE: page 0 is already fetched so starting from 1
    for pageNumber in range(1, total_pages-1):
        url_with_pagination = URL + '/page/' + str(pageNumber)
        response = requests.get(url_with_pagination)
        soup = BeautifulSoup(response.text, 'html.parser') 
        all_titles = all_titles + scrap_page_title(soup)
        time.sleep(3)

    save_as_csv(all_titles)
    import pdb
    pdb.set_trace()


if __name__ == "__main__":
    main()