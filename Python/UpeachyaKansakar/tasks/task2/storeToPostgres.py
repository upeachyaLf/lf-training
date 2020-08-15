import csv
import psycopg2

conn = psycopg2.connect("host=localhost dbname=python_training user=postgresuser password=root")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE articles(
    title text,
    author text
)
""")

with open('output/articles.csv', 'r') as f:
    reader = csv.reader(f)
    # NOTE: for skippin the header row.
    next(reader) 
    for row in reader:
        cur.execute(
        "INSERT INTO articles VALUES (%s, %s)",
        row
    )

# NOTE: commit needs to be run at end of our transaction
conn.commit()
