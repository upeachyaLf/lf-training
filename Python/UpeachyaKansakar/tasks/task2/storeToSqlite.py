import csv
import sqlite3

def main():
    # File path.
    filePath = 'output/articles.csv'
    # Database.
    database = '/home/upeachya/training'

    connect = sqlite3.connect(database)
    cursor = connect.cursor()

    # Creating a new table
    cursor.execute("""
        CREATE TABLE articles(
        title text,
        author text
    )
    """)

    # SQL to insert person information.
    sqlInsert = \
    "INSERT INTO articles (title, author)  \
    VALUES (?, ?)"

    with open(filePath, 'r') as f:
        reader = csv.DictReader(f)
        # NOTE: for skippin the header row.
        next(reader) 
        for row in reader:
            cursor.execute(sqlInsert, (row['title'],row['authors']))

    connect.commit()

    connect.close()

if __name__ == "__main__":
    main()