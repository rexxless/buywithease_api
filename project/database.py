import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import Error

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

try:
    db = psycopg2.connect(
        dbname=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = db.cursor()
except (Exception, Error) as error:
    print(f"Error while connecting to PostgreSQL: {error}")
    raise
