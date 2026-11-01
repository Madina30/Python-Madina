import psycopg2
from config import DB_CONFIG


def connect():
    """Connect to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection

    except psycopg2.Error as error:
        print("Database connection error:", error)
        return None