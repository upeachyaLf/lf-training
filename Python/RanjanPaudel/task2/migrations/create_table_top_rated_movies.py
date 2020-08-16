import sqlite3

imdb_movies_db = 'sqlite_dbs/imdb_movies.db'


def create_table():
    connection = sqlite3.connect(imdb_movies_db)
    connection.execute('''CREATE TABLE IF NOT EXISTS top_rated_movies
                        (id INTEGER PRIMARY KEY ASC, 
                        rank INTEGER UNIQUE, 
                        title TEXT, 
                        release_year INTEGER, 
                        imdb_rating REAL)
                    ''')
    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_table()
