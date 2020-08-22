from connection import initialize_pool, get_connection, put_connection

DROP_SEARCH_TERM_TABLE = """DROP TABLE IF EXISTS search_terms;"""
DROP_BRANDS_TABLE = """DROP TABLE IF EXISTS brands;"""
DROP_RESULT_TABLE = """DROP TABLE IF EXISTS results;"""


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
                                                                search_id INT, 
                                                                brand_name VARCHAR(30), 
                                                                title text,
                                                                price float,
                                                                aggregateRating float,
                                                                image_url text,
                                                                description text,
                                                                url_link text,
                                                                PRIMARY KEY(result_id),
                                                                CONSTRAINT fk_search_trem_result 
                                                                    FOREIGN KEY(search_id)
                                                                    REFERENCES search_terms(search_id));"""

table_mapping = {
    'search_term': 'search_terms',
    'brands': 'brands',
    'contents': 'results'
}

def create_table():
    initialize_pool()
    connection = get_connection()
    connection.autocommit = True
    try:
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
    
    finally:
        try:
            print('Putting Connection Back to the pool')
            put_connection(connection)
        except Exception as error:
            print('Error: While Putting Connection Cursor back to pool')

def insert_into_table(statement, data):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.executemany(statement % data)
    except Exception as error:
        print('Insert Error')
        conn.rollback()
        raise
    finally:
        try:
            print('Putting Connection Back to the pool')
            put_connection(connection)
        except Exception as error:
            print('Error: While Putting Connection Cursor back to pool')

def store_data(tablename, data):
    table = table_mapping[tablename]
    
    INSERT_STATEMENT = f"""INSERT INTO {table} (search_name) VALUES (%%s)"""
    insert_into_table(INSERT_STATEMENT, data)



