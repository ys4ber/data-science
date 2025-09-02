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



CUSTOMER_PATH = "/goinfre/ysaber/subject/customer"


def get_titles_from_csv(file_path):

    """
    this function used to get the titles from the csv files
    this will help create the database table properly
    """

    titles = []
    with open(file_path, "r") as f:
        titles = f.readline().strip().split(",")
        print(f"Getting titles from {file_path}")
    return titles

def Create_Table(conn, titles, month, cur):
    create_table_query = """
        CREATE TABLE {0} (
            {1} TIMESTAMPTZ NOT NULL,
            {2} VARCHAR(50),
            {3} INT,
            {4} NUMERIC(10,2),
            {5} BIGINT,
            {6} UUID
        );
    """.format(month, *titles)
    cur.execute(create_table_query)
    conn.commit()

def main():
    try:
        files = subprocess.check_output(['ls', CUSTOMER_PATH]).decode('utf-8').replace(".csv", "").splitlines()
        titles = get_titles_from_csv(os.path.join(CUSTOMER_PATH, files[0] + ".csv"))

        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=HOST,
            port=PORT
        )

        with conn.cursor() as cur:
            for month in files:
                Create_Table(conn, titles, month, cur)
                print(f"Table created for {month}")
                time.sleep(2)
            
            cur.close()
            conn.close()

    except Exception as e:
        print(f"Error getting titles from CSV: {e}")

if __name__ == "__main__":
    main()