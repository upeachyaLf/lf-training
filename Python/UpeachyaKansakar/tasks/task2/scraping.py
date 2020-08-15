import time
import requests
import urllib.request
from bs4 import BeautifulSoup

def scrapPagetitle(soupObject):
    title_divs = soupObject.findAll('h2',{'class':'title'})
    titles = []
    for title in title_divs:
        titles.append(title.get_text())   
    return titles  


def main():
    # set the url to the website and access the site with our requests library
    url = 'https://www.opencodez.com/category/web-development'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser') 

    # For finding total number of pages
    pagination_div = soup.find('div',{'class':'pagination'})
    total_pages = len(pagination_div.findAll('li'))
    all_titles = scrapPagetitle(soup)
    time.sleep(5)
    print("all titles",all_titles)


if __name__ == "__main__":
    main()
