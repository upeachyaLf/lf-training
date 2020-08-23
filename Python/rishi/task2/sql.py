DROP_SEARCH_TERM_TABLE = """DROP TABLE IF EXISTS search_terms;"""
DROP_BRANDS_TABLE =      """DROP TABLE IF EXISTS brands;"""
DROP_PRODUCTS_TABLE =      """DROP TABLE IF EXISTS products;"""


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

CREATE_PRODUCTS_TABLE = """ CREATE TABLE products(product_id INT GENERATED ALWAYS AS IDENTITY,
                                                                brand_name VARCHAR(30), 
                                                                title text,
                                                                price float,
                                                                aggregateRating VARCHAR(7),
                                                                image_url text,
                                                                description text,
                                                                url_link text,
                                                                PRIMARY KEY(product_id)
                                                                );"""

INSERT_INTO_PRODUCTS_STATEMENT = """INSERT INTO products(title,price,url_link,image_url,description,aggregateRating,brand_name) VALUES (%s,%s,%s,%s,%s,%s,%s);"""
INSERT_INTO_SEARCH_TABLE = """INSERT INTO search_terms(search_name) VALUES (%s);"""

table_insert_statement_mapping = {
    'search_term': INSERT_INTO_SEARCH_TABLE,
    'contents': INSERT_INTO_PRODUCTS_STATEMENT
}
