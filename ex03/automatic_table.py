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



def Create_Table(conn, titles):
    with conn.cursor() as cur:
        create_table_query = """
            CREATE TABLE data_2022_dec (
                event_time TIMESTAMPTZ NOT NULL,
                event_type VARCHAR(50),
                product_id INT,
                price NUMERIC(10,2),
                user_id BIGINT,
                user_session UUID
            );
        """
        cur.execute(create_table_query)
        print("Table 'data_2022_dec' created successfully.")
        conn.commit()
        cur.close()
        conn.close()


def get_titles_from_csv(file_path):

    """
    this function supposed to get the titles from the csv files
    this will help create the database table properly
    """

    titles = []

    with open(file_path, "r") as f:
        titles = f.readline().strip().split(",")
        print(f"Getting titles from {file_path}")

    return titles


def main():
    files = subprocess.check_output(['ls', CUSTOMER_PATH]).decode('utf-8').replace(".csv", "").splitlines()
    print(files)
    titles = get_titles_from_csv(os.path.join(CUSTOMER_PATH, files[0] + ".csv"))

    print(titles)

if __name__ == "__main__":
    main()