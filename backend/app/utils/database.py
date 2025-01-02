from ..database.connection import Connection
from sqlalchemy.orm import Session
import os


def Connect_to_database() -> Connection:

    # get environment variables
    HOST, PORT = os.environ.get("DOCFIND_DB_HOST"), os.environ.get("DOCFIND_DB_PORT")
    if HOST is None or PORT is None:
        raise ValueError("Database URL is not set")

    DBNAME = os.environ.get("POSTGRES_DB")
    USER = os.environ.get("POSTGRES_USER")
    PASSWORD = os.environ.get("POSTGRES_PASSWORD")

    if DBNAME is None or USER is None or PASSWORD is None:
        raise ValueError("Invalid DATABASE_URL")

    # connect to the database
    db = Connection(
        dbname=DBNAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=int(PORT),
    )
    db.connect()

    return db
