import sqlite3

top_rated_db = 'sqlite_dbs/top_rated_movies.db'

table_all_columns = {
    "top_rated_movies": "(rank, title, release_year, imdb_rating)"
}

table_all_column_binds = {
    "top_rated_movies": "(?, ?, ?, ?)"
}


def genarate_tuple_list(dict_list):
    tuple_list = []
    for _dict in dict_list:
        tuple_list.append(tuple(_dict.values()))

    return tuple_list


def dict_factory(cursor, row):
    row_dict = {}
    for idx, col in enumerate(cursor.description):
        row_dict[col[0]] = row[idx]

    return row_dict


if __name__ == "sqlite_handler":
    def insert_many(table_name, dict_list):
        tuple_list = genarate_tuple_list(dict_list)

        conn = sqlite3.connect(top_rated_db)
        conn.executemany(f'''
                INSERT INTO {table_name} {table_all_columns[table_name]} VALUES{table_all_column_binds[table_name]}
        ''', tuple_list)

        conn.commit()
        conn.close()

    def fetch_all(table_name):
        conn = sqlite3.connect(top_rated_db)
        conn.row_factory = dict_factory
        cur = conn.cursor()

        dict_list = []
        for row in cur.execute(f'SELECT * FROM {table_name}'):
            dict_list.append(row)

        conn.close()

        return dict_list
