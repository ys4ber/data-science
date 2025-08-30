import time
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv("../.env")

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")


CUSTOMER_DEC_PATH = "../subject/customer/data_2022_dec.csv"
CUSTOMER_NOV_PATH = "../subject/customer/data_2022_nov.csv"
CUSTOMER_OCT_PATH = "../subject/customer/data_2022_oct.csv"
CUSTOMER_JAN_PATH = "../subject/customer/data_2023_jan.csv"




def get_titles_from_csv():

    """
    this function supposed to get the titles from the csv files
    this will help create the database table properly
    """

    titles = []
    
    with open(CUSTOMER_OCT_PATH, "r") as f:
        titles = f.readline().strip().split(",")
        print(f"Getting titles from {CUSTOMER_OCT_PATH}")

    return titles



def create_table(conn, table_name, titles):
    """
    this function creates a table in the database with the given name and columns
    """

    with conn.cursor() as cur:
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{title} TEXT' for title in titles])});")
        conn.commit()

def main():
    titles = get_titles_from_csv()
    print(titles)
    for csv_file in [CUSTOMER_DEC_PATH, CUSTOMER_NOV_PATH, CUSTOMER_OCT_PATH, CUSTOMER_JAN_PATH]:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        create_table(conn, csv_file, titles)

if __name__ == "__main__":
    main()