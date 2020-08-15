import csv
import psycopg2

def main():
    conn = psycopg2.connect("host=localhost dbname=python_training user=postgresuser password=root")
    cur = conn.cursor()

    # NOTE: Query for creating table
    cur.execute("""
        CREATE TABLE articles(
        title text,
        author text
    )
    """)

    # NOTE: Retreving csv data and saving to db
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

if __name__ == "__main__":
    main()
