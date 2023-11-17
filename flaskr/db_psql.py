import os
import psycopg2

# this is to configure the connection
conn = psycopg2.connect(
    host="localhost", database="postgres_db", user=os.environ["DB_USERNAME"], password=os.environ["DB_PASSWORD"]
)

# create a cursor to perform databse operations
cur = conn.cursor()
