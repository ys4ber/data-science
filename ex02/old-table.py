import time
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv("../.env")

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")


CUSTOMER_DEC_PATH = "../subject/customer/data_2022_dec.csv"
CUSTOMER_NOV_PATH = "../subject/customer/data_2022_nov.csv"
CUSTOMER_OCT_PATH = "../subject/customer/data_2022_oct.csv"
CUSTOMER_JAN_PATH = "../subject/customer/data_2023_jan.csv"

CUSTOMER_PATH = "../subject/customer/"

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
    this function parse the name of the files so we can create every table with the right
    file name
    """

    for name in [CUSTOMER_DEC_PATH, CUSTOMER_NOV_PATH, CUSTOMER_OCT_PATH, CUSTOMER_JAN_PATH]:
        if name == table_name:
            table_name = name.split("/")[-1].replace(".csv", "")
            print(f"Creating table \"{table_name}\"...")
            time.sleep(2)
            break

    with conn.cursor() as cur:
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{title} TEXT' for title in titles])});")
        conn.commit()


def verify_database(conn):
    """
    Verify that tables were created successfully
    """
    with conn.cursor() as cur:
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cur.fetchall()
        print("\nTables in database:")
        for table in tables:
            print(f"  - {table[0]}")
        
        for table in tables:
            table_name = table[0]
            cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}';")
            columns = cur.fetchall()
            print(f"\nColumns in {table_name}:")
            for c in columns:
                print(f"  - {c[0]} ({c[1]})")

def main():
    titles = get_titles_from_csv()
    print(titles)
    for csv_file in [CUSTOMER_DEC_PATH, CUSTOMER_NOV_PATH, CUSTOMER_OCT_PATH, CUSTOMER_JAN_PATH]:
        conn = psycopg2.connect(
            host=HOST,
            port=PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        create_table(conn, csv_file, titles)

        verify_database(conn)

        conn.close()

if __name__ == "__main__":
    main()