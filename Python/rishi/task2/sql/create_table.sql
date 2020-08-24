DROP TABLE IF EXISTS search_terms;
DROP TABLE IF EXISTS brands;
DROP TABLE IF EXISTS results;

CREATE TABLE results(result_id INT GENERATED ALWAYS AS IDENTITY, 
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
                                                                    REFERENCES search_terms(search_id));
                                                        
CREATE TABLE 
        brands(brand_id INT GENERATED ALWAYS AS IDENTITY, 
        search_id INT,
        brand_name VARCHAR(30), 
        PRIMARY KEY(brand_id),
        CONSTRAINT fk_search_terms
            FOREIGN KEY(search_id) 
	            REFERENCES search_terms(search_id)
                ON DELETE CASCADE );

CREATE TABLE search_terms(search_id INT GENERATED ALWAYS AS IDENTITY, search_name VARCHAR(100), PRIMARY KEY(search_id));