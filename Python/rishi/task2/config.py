from dotenv import load_dotenv
load_dotenv()

import os, glob

BASE_DIR_PATH=os.getcwd()
OUTPUT_FILE='search_result.csv'
DIRECTORY_NAME='searchResults'

if not os.path.exists(DIRECTORY_NAME):
    os.makedirs(DIRECTORY_NAME)

DIRECTORY_PATH = f"{BASE_DIR_PATH}/{DIRECTORY_NAME}"

files = glob.glob(f"{DIRECTORY_PATH}/*")
for i in files:
    os.remove(i)

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
