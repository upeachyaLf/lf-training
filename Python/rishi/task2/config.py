from dotenv import load_dotenv
load_dotenv()

import os

connection_string = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME')
}


test_connection_string = {
    'user': os.getenv('TEST_DB_USER'),
    'password': os.getenv('TEST_DB_PASSWORD'),
    'host': os.getenv('TEST_DB_HOST'),
    'port': os.getenv('TEST_DB_PORT'),
    'database': os.getenv('TEST_DB_NAME')
}
