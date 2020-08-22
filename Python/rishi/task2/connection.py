import psycopg2
from psycopg2 import pool
import os
from config import connection_string

connection_string = connection_string
print(connection_string)

def initialize_pool():
    global connection_pool
    MIN_POOL_SIZE = 1
    MAX_POOL_SIZE = 1
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(MIN_POOL_SIZE, MAX_POOL_SIZE, **connection_string)
        print('Initialized Connection Pool')
    except Exception as error:
        print('Could Not setup Connection Pool')
        raise

def get_connection():
    return connection_pool.getconn()

def put_connection(connection):
    return connection_pool.putconn(connection)
