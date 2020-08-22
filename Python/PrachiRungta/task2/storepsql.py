#!/usr/bin/python
import psycopg2
import csv

conn = psycopg2.connect("host=localhost dbname=bookstore user=prachi_test password=mypassword")
data_filename='output/filename.csv'
cursor= conn.cursor()

# create table
with cursor:
    cursor.execute("""
        CREATE TABLE if not exists books_stock(
        book_name text, 
        price varchar)
    """)

#open file and insert data 
with open(data_filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) 
    for row in reader:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO books_stock VALUES (%s, %s)",row)

#to select and view records
with conn.cursor() as cursor:
    cursor.execute("select book_name, price from books_stock")
    allrecords = cursor.fetchall()         
    print(allrecords)  

conn.commit()
