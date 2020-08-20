import sqlite3

imdb_movies_db = 'sqlite_dbs/imdb_movies.db'


def drop_table():
    with sqlite3.connect(imdb_movies_db) as connection:
        connection.execute('DROP TABLE most_popular_tv_shows')
        connection.commit()


if __name__ == "__main__":
    drop_table()
