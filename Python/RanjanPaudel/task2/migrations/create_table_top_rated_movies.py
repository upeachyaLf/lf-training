import sqlite3

top_rated_movies_db = 'sqlite_dbs/top_rated_movies.db'

connection = sqlite3.connect(top_rated_movies_db)

cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS top_rated_movies
                    (id INTEGER PRIMARY KEY ASC, rank INTEGER UNIQUE, title TEXT, release_year INTEGER, imdb_rating REAL)
                ''')

cursor.close()
