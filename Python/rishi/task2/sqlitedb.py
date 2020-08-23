import sqlite3
from contextlib import contextmanager
import csv

from config import OUTPUT_FILE
from utils import get_filepath_name, build_db_format, format_price

DB_FILE = 'products.db'
FILEPATH = get_filepath_name(OUTPUT_FILE)

CREATE_PRODUCTS_TABLE = """ CREATE TABLE products(product_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                brand_name VARCHAR(30), 
                                                                title text,
                                                                price float,
                                                                aggregateRating VARCHAR(7),
                                                                image_url text,
                                                                description text,
                                                                url_link text
                                                                );"""

DROP_PRODUCTS_TABLE = """DROP TABLE IF EXISTS products;"""
INSERT_INTO_PRODUCTS_STATEMENT = """INSERT INTO products(brand_name,title,price,aggregateRating,image_url,description,url_link) VALUES (?,?,?,?,?,?,?);"""

@contextmanager
def get_connection():
    connection = sqlite3.connect(DB_FILE)
    yield connection
    connection.close()

def store_in_sqlite():
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(DROP_PRODUCTS_TABLE)
            cursor.execute(CREATE_PRODUCTS_TABLE)
            with open(FILEPATH, 'r') as reader:
                values = []
                contents = csv.DictReader(reader)
                for i in contents:
                    data = format_price(i)
                    values.append(build_db_format(data))
            cursor.executemany(INSERT_INTO_PRODUCTS_STATEMENT, values)
    except Exception as error:
        connection.rollback()
        print('Error: Connection Cursor"%s"', error)
        raise
