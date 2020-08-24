import csv
import sqlite3

db_filename='bookstore.db'
data_filename='output/filename.csv'
conn=sqlite3.connect(db_filename)

#create table
with conn:
    conn.execute('''create table if not exists book_stock
                 (book_name text, price real)''')

#open the data file and store the data into db using insert query
with open(data_filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    next(reader) 
    for row in reader:
        with conn:
            conn.execute(("insert into book_stock(book_name, price)values(:book_name,:price)"), 
            (row['book_name'],row['price']))  

#select table data from book_stock
for row in conn.execute("select book_name, price from book_stock"):
    print (row)

conn.commit()
conn.close()
