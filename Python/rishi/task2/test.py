import pytest
import psycopg2
import os
import logging

from scrapper import get_filepath_name

def test_get_filepath_name():
    filename = 'searchfile'
    filepath = 'home/lf/rishi'

    result = get_filepath_name(filepath, filename)
    assert result == 'home/lf/rishi/searchfile'

@pytest.fixture(scope='module')
def cursor(conx):
    cursor = conx.cursor()
    logging.info('Created A cursor')
    yield cursor
    conx.rollback()

@pytest.fixture
def test_create_table(cursor):
    logging.info('Create Table')
    statement = """create table test_tables(id INT, name varchar(20))"""
    cursor.execute(statement)

def test_table_exists(cursor, test_create_table):
    logging.info('Running Test')
    cursor.execute('select * from test_tables')
    result = cursor.fetchall()

    assert len(result) == 0