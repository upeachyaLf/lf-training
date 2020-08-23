from contextlib import contextmanager

from connection import initialize_pool, get_connection, put_connection
from sql import *

def create_table():
    initialize_pool()
    try:
        with define_connection() as connection:
            with connection.cursor() as cur:
                print('Creating Tables')
                cur.execute(DROP_BRANDS_TABLE)
                cur.execute(DROP_BRANDS_TABLE)
                cur.execute(DROP_SEARCH_TERM_TABLE)
                cur.execute(CREATE_SEARCH_TERM_TABLE)
                cur.execute(CREATE_BRANDS_TABLE)
                cur.execute(CREATE_PRODUCTS_TABLE)
    except Exception as error:
        connection.rollback()
        print('Error: Connection Cursor')
        raise

def insert_into_table(statement, data):
    try:
        with define_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(statement, data)
    except Exception as error:
        print('Insert Error')
        conn.rollback()
        raise

def store_data(key, data):
    INSERT_INTO_STATEMENT = table_insert_statement_mapping[key]
    insert_into_table(INSERT_INTO_STATEMENT, data)

@contextmanager
def define_connection():
    conn = get_connection()
    conn.autocommit = True
    try:
        yield conn
    finally:
        try:
            print('Putting Connection Back to the pool')
            put_connection(conn)
        except Exception as error:
            print(f'Error: While Putting Connection Cursor back to pool\n{error}')
            raise

