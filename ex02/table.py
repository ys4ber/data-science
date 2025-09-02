import time
import psycopg2
from dotenv import load_dotenv
import os
import subprocess

load_dotenv("../.env")

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")

CUSTOMER_PATH = "../subject/customer/"

def get_titles_from_csv(file_path):

    """
    this function supposed to get the titles from the csv files
    this will help create the database table properly
    """

    titles = []

    with open(file_path, "r") as f:
        titles = f.readline().strip().split(",")

    return titles

def Create_Table(conn, titles):
    with conn.cursor() as cur:
        create_table_query = """
            CREATE TABLE data_2022_dec (
                {0} TIMESTAMPTZ NOT NULL,
                {1} VARCHAR(50),
                {2} INT,
                {3} NUMERIC(10,2),
                {4} BIGINT,
                {5} UUID
            );
        """.format(*titles)
        cur.execute(create_table_query)
        print("Table 'data_2022_dec' created successfully.")
        conn.commit()
        cur.close()
        conn.close()

def main():
    try:
        file = "data_2022_oct.csv"
        titles = get_titles_from_csv(os.path.join(CUSTOMER_PATH, file))

        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=HOST,
            port=PORT
        )

        Create_Table(conn, titles)
    except Exception as e:
        print(f"Error creating table: {e}")


if __name__ == "__main__":
    main()