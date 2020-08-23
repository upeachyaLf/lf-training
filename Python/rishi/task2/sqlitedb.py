import sqlite3
from contextlib import contextmanager

from sql import *
from config import OUTPUT_FILE
from utils import get_filepath_name

DB_FILE = 'products.db'
FILEPATH = get_filepath_name(OUTPUT_FILE)

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
                        
    except Exception as error:
        connection.rollback()
        print('Error: Connection Cursor"%s"', error)
        raise
