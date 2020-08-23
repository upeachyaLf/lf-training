from contextlib import contextmanager

from connection import initialize_pool, get_connection, put_connection

DROP_SEARCH_TERM_TABLE = """DROP TABLE IF EXISTS search_terms;"""
DROP_BRANDS_TABLE =      """DROP TABLE IF EXISTS brands;"""
DROP_RESULT_TABLE =      """DROP TABLE IF EXISTS results;"""


CREATE_SEARCH_TERM_TABLE = """CREATE TABLE search_terms(search_id INT GENERATED ALWAYS AS IDENTITY, search_name VARCHAR(100), PRIMARY KEY(search_id));"""
CREATE_BRANDS_TABLE = """
      CREATE TABLE 
        brands(brand_id INT GENERATED ALWAYS AS IDENTITY, 
        search_id INT,
        brand_name VARCHAR(30), 
        PRIMARY KEY(brand_id),
        CONSTRAINT fk_search_terms
            FOREIGN KEY(search_id) 
	            REFERENCES search_terms(search_id)
                ON DELETE CASCADE );"""

CREATE_RESULTS_TABLE = """ CREATE TABLE results(result_id INT GENERATED ALWAYS AS IDENTITY,
                                                                brand_name VARCHAR(30), 
                                                                title text,
                                                                price float,
                                                                aggregateRating VARCHAR(7),
                                                                image_url text,
                                                                description text,
                                                                url_link text,
                                                                PRIMARY KEY(result_id)
                                                                );"""

INSERT_STATEMENT = """INSERT INTO results(title,price,url_link,image_url,description,aggregateRating,brand_name) VALUES (%s,%s,%s,%s,%s,%s,%s);"""
INSERT_INTO_SEARCH_TABLE = """INSERT INTO search_terms(search_name) VALUES (%s);"""

table_insert_statement_mapping = {
    'search_term': INSERT_INTO_SEARCH_TABLE,
    'contents': INSERT_STATEMENT
}

def create_table():
    initialize_pool()
    try:
        with define_connection() as connection:
            with connection.cursor() as cur:
                print('Creating Tables')
                cur.execute(DROP_RESULT_TABLE)
                cur.execute(DROP_BRANDS_TABLE)
                cur.execute(DROP_SEARCH_TERM_TABLE)
                cur.execute(CREATE_SEARCH_TERM_TABLE)
                cur.execute(CREATE_BRANDS_TABLE)
                cur.execute(CREATE_RESULTS_TABLE)
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

