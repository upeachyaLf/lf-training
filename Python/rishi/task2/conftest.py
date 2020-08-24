import pytest
import psycopg2
import os
import logging

@pytest.fixture(scope='session')
def conx():
    db_setting = {
    'user': os.getenv('TEST_DB_USER'),
    'password': os.getenv('TEST_DB_PASSWORD'),
    'host': os.getenv('TEST_DB_HOST'),
    'port': os.getenv('TEST_DB_PORT'),
    'database': os.getenv('TEST_DB_NAME')
    }

    connection = psycopg2.connect(**db_setting)
    logging.info('Connection Setup')
    yield connection
    connection.close()
    logging.info('Connection Close')