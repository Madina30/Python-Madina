import psycopg2
from config import DB_CONFIG


def connect():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection

    except Exception as error:
        print("Database connection error:", error)
        return None