import csv
import sqlite3

db_filename='bookstore.db'
data_filename='output/filename.csv'
conn=sqlite3.connect(db_filename)

cursor=conn.cursor()

#create table
cursor.execute('''create table if not exists book_stock
             (book_name text, price real)''')

#insert query
insertbooks=("insert into book_stock(book_name, price)values(:book_name,:price)")

#open the data file and store the data into db
with open(data_filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    next(reader) 
    for row in reader:
        cursor.execute(insertbooks, (row['book_name'],row['price']))   

#select table data from book_stock
for row in conn.execute("select book_name, price from book_stock"):
    print (row)

conn.commit()
conn.close()