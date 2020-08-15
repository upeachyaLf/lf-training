import sqlite3

conn = sqlite3.connect('output/results.db')
cursor = conn.cursor()
for row in cursor.execute('SELECT * FROM data'):
    print(row)
