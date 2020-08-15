import re
import pdb
import requests
from bs4 import BeautifulSoup

import file_handler as fh

imdb_base_url = "https://www.imdb.com"
search_top_rated_movies = "/chart/top/?ref_=nv_mv_250"

# top_rated_file = 'imdb_top_rated.html'
top_rated_csv = './output/file.csv'
top_rated_json = './output/file.json'
top_rated_xml = './output/file.xml'
top_rated_yaml = './output/file.yaml'


def read_file_and_get_soup(filename):
    html_str = ''

    with open(filename, 'r') as html_file:
        html_str = html_file.read()

    return BeautifulSoup(html_str, 'html.parser')


def get_movie_list(soup):
    table_body = soup.find('tbody', {'class': 'lister-list'})
    table_rows = table_body.find_all('tr')
    movie_list = []

    for tr in table_rows:
        title_column = tr.find('td', {'class': 'titleColumn'})
        rank_column = tr.find('td', {'class': 'ratingColumn imdbRating'})

        title_texts = title_column.get_text(
            separator='_//\\_', strip=True).split('_//\\_')

        rank = title_texts[0].replace('.', '')
        title = title_texts[1]
        year = re.sub("^\(|\)$", "", title_texts[2])
        rating_text = rank_column.get_text(strip=True)

        movie_list.append({
            "rank": rank,
            "title": title,
            "release_year": year,
            "imdb_rating": rating_text
        })

    return movie_list


def store_in_files(data_list):
    fh.store_in_csv(data_list, top_rated_csv)
    fh.store_in_json(data_list, top_rated_json)
    fh.store_in_xml(data_list, top_rated_xml)
    fh.store_in_yaml(data_list, top_rated_yaml)


def request_and_get_soup(url):
    response_content = ''

    with requests.get(url=url) as req:
        response_content = req.content

    return BeautifulSoup(response_content, 'html.parser')


def main():
    imdb_top_rated_movies_url = imdb_base_url + search_top_rated_movies
    soup = request_and_get_soup(imdb_top_rated_movies_url)

    # soup = read_file_and_get_soup(top_rated_file)
    movie_list = get_movie_list(soup)

    store_in_files(movie_list)
    # pdb.set_trace()


if __name__ == "__main__":
    main()
