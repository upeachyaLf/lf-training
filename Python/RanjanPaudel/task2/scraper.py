import re
import time
import requests
import pdb
from bs4 import BeautifulSoup

import file_handler as fh
import sqlite_handler as sh

imdb_base_url = "https://www.imdb.com"
search_map = {
    "top_rated": "/chart/top/?ref_=nv_mv_250",
    "most_popular": "/chart/moviemeter/?ref_=nv_mv_mpm"
}

table_map = {
    "top_rated": "top_rated_movies",
    "most_popular": "most_popular_movies"
}


def get_top_rated_movie_list(table_rows):
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


def get_most_popular_movie_list(table_rows):
    movie_list = []
    for tr in table_rows:
        title_column = tr.find('td', {'class': 'titleColumn'})
        rank_column = tr.find('td', {'class': 'ratingColumn imdbRating'})

        title_texts = title_column.get_text(
            separator='_//\\_', strip=True).replace('\n', '_//\\_').split('_//\\_')

        title = title_texts[0]
        year = re.sub("^\(|\)$", "", title_texts[1])
        position = title_texts[2].replace(',', '')
        pre_position = re.sub(
            "^\(|\)$", "", title_texts[len(title_texts) - 1]).replace(',', '')
        rating_text = rank_column.get_text(strip=True) or 'NOT RATED'
        popularity = ''

        if pre_position == 'no change':
            popularity = pre_position.upper()
            pre_position = position
        elif int(position) < int(pre_position):
            popularity = 'INCREASED'
        else:
            popularity = 'DECREASED'

        movie_list.append({
            "title": title,
            "release_year": year,
            "imdb_rating": rating_text,
            "position": position,
            "pre_position": pre_position,
            "popularity": popularity
        })

    return movie_list


def get_movie_list(soup, _type):
    table_body = soup.find('tbody', {'class': 'lister-list'})
    table_rows = table_body.find_all('tr')

    if _type == 'top_rated':
        return get_top_rated_movie_list(table_rows)

    if _type == 'most_popular':
        return get_most_popular_movie_list(table_rows)


def store_in_files(data_list, list_type):
    print('    ** Writing CSV file...')
    fh.store_in_csv(data_list, f'./{list_type}_movies/file.csv')
    print('    ** Writing JSON file...')
    fh.store_in_json(data_list, f'./{list_type}_movies/file.json')
    print('    ** Writing XML file...')
    fh.store_in_xml(data_list, f'./{list_type}_movies/file.xml')
    print('    ** Writing YAML file...')
    fh.store_in_yaml(data_list, f'./{list_type}_movies/file.yaml')
    print('*** Done.')


def store_in_sqlite(table_name, data_list):
    sh.insert_many(table_name, data_list)


def read_from_sqlite(table_name):
    data = sh.fetch_all(table_name)

    for row in data:
        print(row)


def request_and_get_soup(url):
    response_content = ''

    with requests.get(url=url) as req:
        response_content = req.content

    return BeautifulSoup(response_content, 'html.parser')


def scrape_movies(_type):
    imdb_movie_list_url = imdb_base_url + search_map[_type]
    print('*** Fetching movie list...')
    soup = request_and_get_soup(imdb_movie_list_url)
    print('*** List fetched')
    movie_list = get_movie_list(soup, _type)
    print('*** Saving to files...')
    store_in_files(movie_list, _type)
    print('*** Storing in SQLite DB...')
    store_in_sqlite(table_map[_type], movie_list)
    print('*** Done.')
    # read_from_sqlite(table_map[_type])


def main():
    print('Scraping Top rated movies:')
    scrape_movies('top_rated')
    print('\nPlease Wait for 10 seconds ...\n')
    time.sleep(10)
    print('Scraping Top rated movies:')
    scrape_movies('most_popular')
    print('\nScraping Completed')


if __name__ == "__main__":
    main()
